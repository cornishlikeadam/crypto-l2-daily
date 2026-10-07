#!/usr/bin/env python3
"""🎬 Make the 90-second explainer video: "Crypto L2 Daily: How It Works."

Run it with OpenMontage's Python (it has numpy and Piper):
  ../OpenMontage/.venv/bin/python scripts/make_explainer.py

What it does, in order:
1. 🎙️ Reads each narration line with Piper (free voice). Short ASD-STE100 sentences.
2. ⏱️ Times the 8 shots from the voice, to fill 90 seconds.
3. 🎵 Makes a soft lo-fi synth bed with taiko hits on every shot change. The music gets quieter under the voice.
4. 🎞️ Renders remotion/explainer/ with Remotion.
5. 💾 Saves site/assets/explainer.mp4 + explainer-poster.jpg. The site's ❓ Guide pop-up plays it.
"""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OM = ROOT.parent / "OpenMontage"
COMPOSER = OM / "remotion-composer"
WORK = OM / "projects" / "l2-explainer"
PIPER = OM / ".venv" / "bin" / "piper"
VOICE = Path.home() / ".piper" / "models" / "en_US-lessac-medium.onnx"
FPS, TOTAL, SR = 30, 90.0, 44100

# 🎞️ The 8 shots. *word* = gold highlight in the captions. Sentences stay short (ASD-STE100).
SHOTS = [
    ("title", "01 · Title", ["This is *Crypto L2 Daily*.", "It is a *robot*. It makes the news, *every day*."]),
    ("read", "02 · 6 PM", ["At *6 PM*, the robot reads *X*.", "It looks for *real posts* about *4 coins*.",
                           "Bitcoin. Dogecoin. Monero. Litecoin."]),
    ("flow", "03 · The core", ["It follows *5 steps*.", "*Collect*. *Check*. Make the *video*.",
                               "A *human check*. Then *publish*."]),
    ("filter", "04 · The filter", ["The robot removes *ads*, *price guesses* and *copies*.",
                                   "It checks *every date*.", "A post from the *wrong day* stays out."]),
    ("use", "05 · How to use", ["To use it, press *play*.", "Read the *cards*.", "Tap a card to open the *real post*."]),
    ("course", "06 · The course", ["Want to learn how it works?", "Open the *course*.", "Tap a *hint*. Then tap the *answer*."]),
    ("widget", "07 · The widget", ["You can put a *small card* on your phone.",
                                   "It shows the *price*, the *fee* and *today's news*.", "It is a *test feature*."]),
    ("outro", "08 · Signature", ["*Real posts*. *Real sources*. Every day.", "*Not too late*. Always forward."]),
]
LEAD, GAP, TAIL_MIN = 0.7, 0.35, 0.9


def say(text: str, out: Path, length_scale: float) -> float:
    spoken = re.sub(r"\*", "", text).replace("6 PM", "six P M").replace("Crypto L2", "Crypto L 2")
    subprocess.run([str(PIPER), "--model", str(VOICE), "--output_file", str(out), "--length_scale", str(length_scale),
                    "--sentence_silence", "0.15"], input=spoken.encode(), check=True, capture_output=True)
    with wave.open(str(out)) as w:
        return w.getnframes() / w.getframerate()


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        sr, n, ch = w.getframerate(), w.getnframes(), w.getnchannels()
        data = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        data = data.reshape(-1, ch).mean(axis=1)
    if sr != SR:  # linear resample to 44.1 kHz
        t_new = np.arange(int(len(data) * SR / sr)) / SR
        data = np.interp(t_new, np.arange(len(data)) / sr, data).astype(np.float32)
    return data


# ---------------------------------------------------------------------------------------------------------------
# 🎵 Music: lo-fi synth bed (soft keys, sub, dusty drums, vinyl hiss) + taiko hits
# ---------------------------------------------------------------------------------------------------------------
def music(total: float, hits: list[float]) -> np.ndarray:
    rng = np.random.default_rng(7)
    n = int(total * SR)
    t = np.arange(n) / SR
    out = np.zeros(n, dtype=np.float32)
    bpm = 78
    beat = 60 / bpm
    bar = beat * 4
    # Fmaj9 - Em7 - Dm9 - Cmaj7 (soft, warm)
    chords = [[53, 57, 60, 64, 67], [52, 55, 59, 62, 66], [50, 53, 57, 60, 64], [48, 52, 55, 59, 64]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    wob = 1 + 0.0025 * np.sin(2 * math.pi * 0.35 * t)  # tape wobble
    for k in range(int(total / bar) + 1):
        start = k * bar
        notes = chords[k % 4]
        for j, m in enumerate(notes):  # electric-piano-ish chord, slight strum
            s0 = int((start + j * 0.018) * SR)
            if s0 >= n:
                continue
            length = min(int(bar * SR), n - s0)
            tt = np.arange(length) / SR
            f = hz(m)
            env = np.exp(-tt * 0.9) * (1 - np.exp(-tt * 60))
            tone = (np.sin(2 * math.pi * f * tt * wob[s0:s0 + length]) + 0.3 * np.sin(2 * math.pi * 2 * f * tt)
                    + 0.08 * np.sin(2 * math.pi * 3 * f * tt))
            out[s0:s0 + length] += 0.045 * env * tone
        s0 = int(start * SR)  # sub bass on the root
        length = min(int(bar * SR), n - s0)
        if length > 0:
            tt = np.arange(length) / SR
            out[s0:s0 + length] += 0.07 * np.sin(2 * math.pi * hz(notes[0] - 12) * tt) * np.exp(-tt * 0.6) * (1 - np.exp(-tt * 30))
        for b in range(4):  # dusty drums: kick on 1 and 3, soft hat on the off-beats (swing)
            bt = start + b * beat
            if b in (0, 2):
                s0 = int(bt * SR)
                length = min(int(0.35 * SR), n - s0)
                if length > 0:
                    tt = np.arange(length) / SR
                    out[s0:s0 + length] += 0.11 * np.sin(2 * math.pi * (55 + 70 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 9)
            s0 = int((bt + beat * 0.58) * SR)
            length = min(int(0.06 * SR), n - s0)
            if length > 0:
                tt = np.arange(length) / SR
                out[s0:s0 + length] += 0.018 * rng.standard_normal(length) * np.exp(-tt * 70)
    # low-pass the whole bed (one-pole) for the lo-fi feel
    a = math.exp(-2 * math.pi * 2600 / SR)
    y = np.empty_like(out)
    acc = 0.0
    for i in range(0, n, 1):
        acc = (1 - a) * out[i] + a * acc
        y[i] = acc
    out = y
    out += 0.004 * rng.standard_normal(n).astype(np.float32) * (rng.random(n) < 0.002) * 6  # vinyl crackle
    out += 0.0025 * rng.standard_normal(n).astype(np.float32)  # hiss
    for h in hits:  # taiko: deep pitched drum with a skin slap
        s0 = int(h * SR)
        length = min(int(1.2 * SR), n - s0)
        if length <= 0:
            continue
        tt = np.arange(length) / SR
        body = np.sin(2 * math.pi * (48 + 40 * np.exp(-tt * 14)) * tt) * np.exp(-tt * 4.2)
        slap = rng.standard_normal(length) * np.exp(-tt * 45) * 0.35
        out[s0:s0 + length] += 0.32 * (body + slap)
    fade = np.minimum(1, np.minimum(t / 1.5, (total - t) / 2.5)).astype(np.float32)
    return out * fade


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    audio = WORK / "audio"
    audio.mkdir(exist_ok=True)
    scale = 1.0
    for attempt in range(4):
        lines = []
        for si, (_, _, texts) in enumerate(SHOTS):
            for li, text in enumerate(texts):
                p = audio / f"s{si}_{li}.wav"
                lines.append((si, text, p, say(text, p, scale)))
        need = sum(LEAD + TAIL_MIN + sum(d for s, _, _, d in lines if s == si) + GAP * (len(SHOTS[si][2]) - 1)
                   for si in range(len(SHOTS)))
        if need <= TOTAL - 1:
            break
        scale *= 0.94
    print(f"[explainer] voice length_scale {scale:.2f}, voice needs {need:.1f}s of {TOTAL}s")
    extra = (TOTAL - need) / len(SHOTS)
    shots, caps, cursor = [], [], 0.0
    for si, (sid, label, texts) in enumerate(SHOTS):
        start = cursor
        t = start + LEAD
        for (s, text, p, d) in [x for x in lines if x[0] == si]:
            caps.append({"shot": sid, "text": text, "start": round(t, 3), "end": round(t + d, 3), "wav": p.name})
            t += d + GAP
        end = t - GAP + TAIL_MIN + extra
        shots.append({"id": sid, "label": label, "start": round(start, 3), "end": round(end, 3)})
        cursor = end
    shots[-1]["end"] = TOTAL
    # narration track + ducked music -> one soundtrack
    n = int(TOTAL * SR)
    voice = np.zeros(n, dtype=np.float32)
    for c in caps:
        v = read_wav(audio / c["wav"])
        s0 = int(c["start"] * SR)
        voice[s0:s0 + len(v)] += v[: max(0, n - s0)]
    env = np.convolve(np.abs(voice), np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
    duck = 1 - 0.55 * np.clip(env / (env.max() + 1e-9) * 6, 0, 1)
    bed = music(TOTAL, [s["start"] + 0.05 for s in shots])
    mix = voice * 0.95 + bed * duck * 1.15
    mix /= max(1.0, float(np.abs(mix).max()) / 0.95)
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    public = WORK / "public"
    public.mkdir(exist_ok=True)
    with wave.open(str(public / "soundtrack.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    props = {"durationSeconds": TOTAL, "audioSrc": "soundtrack.wav", "shots": shots, "captions": caps}
    (WORK / "props.json").write_text(json.dumps(props, indent=2))
    # stage the composition inside the composer so Remotion resolves its packages
    stage = COMPOSER / "projects" / "l2-explainer"
    if stage.exists():
        shutil.rmtree(stage)
    shutil.copytree(ROOT / "remotion" / "explainer", stage)
    out = ROOT / "site" / "assets" / "explainer.mp4"
    if "--stills" in sys.argv:
        for f in [int(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]:
            subprocess.run(["npx", "remotion", "still", f"projects/l2-explainer/index.tsx", "Explainer",
                            str(WORK / f"still_{f}.png"), f"--frame={f}", f"--props={WORK / 'props.json'}",
                            f"--public-dir={public}", "--log=error"], cwd=COMPOSER, check=True)
        print(f"[explainer] stills in {WORK}")
        return 0
    subprocess.run(["npx", "remotion", "render", "projects/l2-explainer/index.tsx", "Explainer", str(out),
                    f"--props={WORK / 'props.json'}", f"--public-dir={public}", "--crf=24", "--log=error"],
                   cwd=COMPOSER, check=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out), "-c", "copy", "-movflags", "+faststart",
                    str(out.with_suffix(".fs.mp4"))], check=True)
    out.with_suffix(".fs.mp4").replace(out)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "3.2", "-i", str(out), "-frames:v", "1", "-vf", "scale=1280:-1",
                    "-q:v", "4", str(out.with_name("explainer-poster.jpg"))], check=True)
    print(f"[explainer] saved {out} ({out.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

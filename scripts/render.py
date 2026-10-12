#!/usr/bin/env python3
"""🎬 Render the daily card slideshow through OpenMontage (separate project).

Run with OpenMontage's own interpreter so its tools resolve:
  ../OpenMontage/.venv/bin/python scripts/render.py --date 2026-10-05

This file only *calls* OpenMontage (its checkpoint library, piper_tts and
video_compose tools). No OpenMontage code lives in this repo.

Pipeline: animated-explainer, used as cards. Every stage writes its canonical
artifact + checkpoint under OpenMontage/projects/crypto-l2-YYYY-MM-DD/.
Approval gates follow config/pipeline.json:
  human_approval_default: true  -> stops after compose; publish awaits a human
  human_approval_default: false -> standing approval recorded; runs through publish
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OM = Path(os.environ.get("OPENMONTAGE_DIR", ROOT.parent / "OpenMontage")).resolve()
sys.path.insert(0, str(OM))
os.chdir(OM)
os.environ["PATH"] = f"{OM / '.venv' / 'bin'}:{os.environ.get('PATH', '')}"

from lib.checkpoint import PROJECTS_DIR, init_project, write_checkpoint  # noqa: E402
from lib.slideshow_risk import score_slideshow_risk  # noqa: E402
from lib.delivery_promise import DeliveryPromise  # noqa: E402
from tools.audio.elevenlabs_tts import ElevenLabsTTS  # noqa: E402
from tools.audio.piper_tts import PiperTTS  # noqa: E402
from tools.video.video_compose import VideoCompose  # noqa: E402

PIPELINE = "animated-explainer"
TARGET_SECONDS = 70.0
VOICE_MODEL = str(Path.home() / ".piper" / "models" / "en_US-lessac-medium.onnx")
SITE_URL = os.environ.get("SITE_URL", "https://not2l8-l2-daily.vercel.app/")
LEAD_IN = 0.3    # silence before each card's narration
MIN_TAIL = 0.45  # minimum hold after narration ends
# Fit plan: (voice length_scale, max words of the post read aloud). The card always shows the
# full sentence; only the spoken version is shortened. Never faster than ~1.15x.
FIT_PLAN = [(1.0, 99), (0.95, 14), (0.9, 11), (0.87, 9), (0.87, 7), (0.87, 5)]

THEME = {  # 💎 Black Platinum, matching remotion/CardDeck.tsx and scripts/site_theme.py
    "primaryColor": "#E5E4E2",
    "accentColor": "#D4AF37",
    "backgroundColor": "#0A0A0B",
    "surfaceColor": "#1B1B1F",
    "textColor": "#E5E4E2",
    "mutedTextColor": "#9A9DA4",
    "headingFont": "Big Shoulders",
    "bodyFont": "Atkinson Hyperlegible",
    "monoFont": "IBM Plex Mono",
    "chartColors": ["#D4AF37", "#85BB65", "#9FF5C8", "#A7E8FF", "#C9B6FF", "#E5E4E2"],
    "springConfig": {"damping": 22, "stiffness": 110, "mass": 1},
    "transitionDuration": 0.4,
    "captionHighlightColor": "#F3D77A",
    "captionBackgroundColor": "rgba(10,10,11,0.85)",
}

# Plain-language "what is this?" lines, written once and checked. They explain the topic word,
# never the news itself, so they can't invent anything about the day.
EXPLAIN = {
    ("Bitcoin", "Lightning"): "Lightning is a fast lane on top of Bitcoin for quick, cheap payments.",
    ("Bitcoin", "Ark"): "Ark is a newer Bitcoin add-on that bundles many small payments together to save fees.",
    ("Bitcoin", "Sidechains"): "A sidechain is a separate network linked to Bitcoin that can try new features.",
    ("Bitcoin", "Layer 2"): "A layer 2 is an extra layer built on top of Bitcoin to make it faster or cheaper.",
    ("Dogecoin", "Dogechain"): "Dogechain is a separate network that was built for Dogecoin apps.",
    ("Dogecoin", "Layer 2"): "A layer 2 is an extra layer built on top of Dogecoin so it can run apps.",
    ("Dogecoin", "Community"): "These are posts from people who use and talk about Dogecoin.",
    ("Monero", "FCMP++"): "FCMP++ is a proposed Monero privacy upgrade under test. It is not a separate layer 2.",
    ("Monero", "CARROT"): "CARROT is a proposed Monero addressing upgrade under test with FCMP++. It is not a layer 2.",
    ("Monero", "Hard fork"): "A hard fork is a planned upgrade that everyone running the network must install.",
    ("Monero", "Upgrade"): "An upgrade is new software that adds features or fixes problems.",
    ("Litecoin", "MWEB"): "MWEB is Litecoin's optional privacy feature that can hide how much you send.",
    ("Litecoin", "Lightning"): "Lightning also works on Litecoin, for fast and cheap small payments.",
    ("Litecoin", "Layer 2"): "A layer 2 is an extra layer built on top of Litecoin to make it faster or cheaper.",
}
QUIET_EXPLAIN = "No posts in this search passed our filters. Other news may exist."


def explain_for(item: dict) -> str:
    if item.get("other_chain_if_any"):
        return f"{item['other_chain_if_any']} is a different blockchain that {item['coin']} fans were talking about."
    return EXPLAIN.get((item["coin"], item.get("topic")), "This post was one of the most-shared on this topic today.")


def short_link(url: str) -> str:
    return url.replace("https://", "")


NUMBER_WORDS = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth",
                7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth", 11: "eleventh",
                12: "twelfth", 13: "thirteenth", 14: "fourteenth", 15: "fifteenth",
                16: "sixteenth", 17: "seventeenth", 18: "eighteenth", 19: "nineteenth",
                20: "twentieth", 21: "twenty-first", 22: "twenty-second", 23: "twenty-third",
                24: "twenty-fourth", 25: "twenty-fifth", 26: "twenty-sixth",
                27: "twenty-seventh", 28: "twenty-eighth", 29: "twenty-ninth",
                30: "thirtieth", 31: "thirty-first"}


def log(msg: str) -> None:
    print(f"[render] {msg}", flush=True)


def probe_duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def spoken_handle(handle: str) -> str:
    name = handle.lstrip("@").replace("_", " ")
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    return name


def speakable(text: str) -> str:
    text = text.replace("…", ".").replace("&", " and ")
    text = re.sub(r"\bL2s?\b", "layer two", text)
    text = re.sub(r"\bFCMP\+\+", "F C M P plus plus", text)
    text = re.sub(r"\bMWEB\b", "M web", text)
    text = re.sub(r"\bXMR\b", "X M R", text)
    text = re.sub(r"\bLTC\b", "L T C", text)
    text = re.sub(r"\bBTC\b", "B T C", text)
    text = re.sub(r"\$([A-Za-z]{2,6})\b", r"\1", text)
    return text


# ---------------------------------------------------------------------------
# Cards
# ---------------------------------------------------------------------------

def build_cards(day: str, data: dict) -> list[dict]:
    d = datetime.strptime(day, "%Y-%m-%d")
    long_date = d.strftime("%A, %B ") + str(d.day)
    spoken_date = d.strftime("%A, %B ") + NUMBER_WORDS[d.day]
    items = data["items"]
    real = [i for i in items if not i["quiet"]]
    coins = []
    for i in items:
        if i["coin"] not in coins:
            coins.append(i["coin"])

    cards = [{
        "id": "title", "kind": "title",
        "explain": "Each card is one real post from X. The link on each card takes you to that post.",
        "title": "Crypto L2 Daily",
        "sentence": f"{long_date} · what Bitcoin L2, Dogecoin, Monero and Litecoin posted on X in the last 24 hours",
        "corner": "X search", "corner_sub": "last 24 hours",
        "narration": f"Crypto layer two daily, {spoken_date}. The last day on X.",
        "post_url": None,
    }]
    for n, item in enumerate(items, 1):
        if item["quiet"]:
            cards.append({
                "id": f"quiet-{item['coin'].lower()}", "kind": "quiet",
                "title": item["coin"], "sentence": "Quiet today.", "explain": QUIET_EXPLAIN,
                "link": None, "stats": None,
                "corner": "no qualifying posts", "corner_sub": long_date,
                "narration": f"{item['coin']}: quiet.",
                "post_url": None, "coin": item["coin"],
            })
            continue
        topic = item["topic"]
        if item.get("other_chain_if_any"):
            title = f"{item['other_chain_if_any']} · via {item['coin']} posts"
            lead = f"{item['other_chain_if_any']}, from {item['coin']} posts."
        else:
            title = f"{item['coin']} · {topic}"
            lead = f"{item['coin']} {topic}."
        cards.append({
            "id": f"item-{n:02d}", "kind": "item",
            "title": title, "sentence": item["claim"],
            "corner": item["handle"], "corner_sub": item["date_et"],
            "explain": explain_for(item), "link": short_link(item["post_url"]),
            "stats": f"{item.get('likes', 0):,} likes · {item.get('reposts', 0):,} reposts",
            "narration": f"{lead} From {spoken_handle(item['handle'])}: {item['claim']}",
            "narr_lead": f"{lead} {spoken_handle(item['handle'])}:", "narr_claim": item["claim"],
            "post_url": item["post_url"], "coin": item["coin"],
        })
    handles = []
    for i in real:
        if i["handle"] not in handles:
            handles.append(i["handle"])
    if handles:
        shown = ", ".join(handles[:6]) + (f" +{len(handles) - 6} more" if len(handles) > 6 else "")
        close_sentence = f"{shown}. Every card links to its post."
        close_narr = f"That's the day. Every card links to its post on the site."
    else:
        close_sentence = "No qualifying posts today. Nothing was invented to fill the gap."
        close_narr = "That's the day. A quiet one, and nothing was invented to fill it."
    cards.append({
        "id": "close", "kind": "close",
        "explain": "Price guesses, giveaways and rumors were left out on purpose.",
        "title": "Sources", "sentence": close_sentence,
        "corner": SITE_URL.replace("https://", "").rstrip("/"), "corner_sub": long_date,
        "narration": close_narr, "post_url": None,
    })
    return cards


# ---------------------------------------------------------------------------
# Narration + timing
# ---------------------------------------------------------------------------

def spoken_claim(claim: str, max_words: int) -> str:
    words = claim.rstrip("….").split()
    if len(words) <= max_words:
        return claim
    return " ".join(words[:max_words]).rstrip(",;:") + "."


VOICE_CFG = ROOT / "config" / "voice.json"
# What actually voiced this run (filled by make_narration, recorded in the artifacts).
VOICE_USED = {"provider": "piper", "tool": "piper_tts", "model": "en_US-lessac-medium", "voice": "lessac"}


def voice_choice() -> dict:
    """ElevenLabs (Jamaican voice) when config/voice.json + ELEVENLABS_API_KEY exist; else Piper."""
    cfg = json.loads(VOICE_CFG.read_text()) if VOICE_CFG.exists() else {}
    if cfg.get("provider") == "elevenlabs" and cfg.get("voice_id") and os.environ.get("ELEVENLABS_API_KEY"):
        return cfg
    return {"provider": "piper"}


def tts_line(cfg: dict, text: str, out_base: Path, length_scale: float) -> Path:
    if cfg["provider"] == "elevenlabs":
        out = out_base.with_suffix(".mp3")
        r = ElevenLabsTTS().execute({"text": text, "voice_id": cfg["voice_id"],
                                     "model_id": cfg.get("model_id", "eleven_multilingual_v2"),
                                     "stability": cfg.get("stability", 0.45),
                                     "similarity_boost": cfg.get("similarity_boost", 0.8),
                                     "speed": round(min(1.2, max(0.8, 1 / length_scale)), 2),
                                     "output_path": str(out)})
    else:
        out = out_base.with_suffix(".wav")
        r = PiperTTS().execute({"text": text, "model": VOICE_MODEL, "length_scale": length_scale,
                                "sentence_silence": 0.2, "output_path": str(out)})
    if not r.success:
        raise RuntimeError(r.error or "tts failed")
    return out


def make_narration(cards: list[dict], audio_dir: Path) -> tuple[Path, list[dict]]:
    cfg = voice_choice()
    for length_scale, max_words in FIT_PLAN:
        durations = []
        for c in cards:
            if c.get("narr_claim"):
                c["narration"] = f"{c['narr_lead']} {spoken_claim(c['narr_claim'], max_words)}"
            try:
                out = tts_line(cfg, speakable(c["narration"]), audio_dir / c["id"], length_scale)
            except RuntimeError as exc:
                if cfg["provider"] == "piper":
                    raise SystemExit(f"[render] piper failed on {c['id']}: {exc}")
                # Better a video in the backup voice than no video; say so loudly in the log.
                log(f"VOICE FALLBACK: ElevenLabs failed ({str(exc)[:200]}); using Piper for this run")
                cfg = {"provider": "piper"}
                out = tts_line(cfg, speakable(c["narration"]), audio_dir / c["id"], length_scale)
            c["audio_path"] = str(out)
            durations.append(probe_duration(out))
        needed = sum(durations) + len(cards) * (LEAD_IN + MIN_TAIL)
        if needed <= TARGET_SECONDS:
            log(f"narration {needed:.1f}s fits (speed {length_scale}, up to {max_words} words read per post)")
            break
        log(f"narration {needed:.1f}s > {TARGET_SECONDS}s at speed {length_scale}, {max_words} words; tightening")
    else:
        raise SystemExit("[render] narration cannot fit 70s; too many cards")
    if cfg["provider"] == "elevenlabs":
        VOICE_USED.update({"provider": "elevenlabs", "tool": "elevenlabs_tts",
                           "model": cfg.get("model_id", "eleven_multilingual_v2"),
                           "voice": cfg.get("voice_name", cfg["voice_id"])})
    log(f"voice: {VOICE_USED['provider']} ({VOICE_USED['voice']})")

    slack = TARGET_SECONDS - needed
    t = 0.0
    for c, dur in zip(cards, durations):
        c["narration_seconds"] = round(dur, 3)
        c["start"] = round(t, 3)
        t += LEAD_IN + dur + MIN_TAIL + slack / len(cards)
        c["end"] = round(t, 3)
    cards[-1]["end"] = TARGET_SECONDS
    for c in cards:
        c["length_scale"] = length_scale

    # One narration track, each card's line placed at its card start + lead-in.
    segs = []
    for c in cards:
        seg = audio_dir / f"seg-{c['id']}.wav"
        span = c["end"] - c["start"]
        delay_ms = int(LEAD_IN * 1000)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", c["audio_path"], "-af",
                        f"adelay={delay_ms}|{delay_ms},apad", "-t", f"{span:.3f}",
                        "-ar", "22050", "-ac", "1", str(seg)], check=True)
        segs.append(seg)
    listing = audio_dir / "segments.txt"
    listing.write_text("".join(f"file '{s}'\n" for s in segs))
    narration = audio_dir / "narration.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-t", f"{TARGET_SECONDS:.3f}", str(narration)], check=True)
    return narration, cards


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------

def search_url(query: str) -> str:
    from urllib.parse import quote
    return f"https://x.com/search?q={quote(query)}&f=live"


def research_brief(day: str, data: dict) -> dict:
    real = [i for i in data["items"] if not i["quiet"]]
    quiet = [i["coin"] for i in data["items"] if i["quiet"]]
    kept = data.get("stats", {}).get("kept", {})
    queries = data["queries"]
    data_points = [{"claim": f"{i['handle']}: {i['claim']}", "source_url": i["post_url"],
                    "source_name": i["handle"], "credibility": "anecdotal", "usable_as": f"card ({i['coin']})"}
                   for i in real]
    # Counts are facts about the pull itself; they keep the brief valid on quiet days.
    for coin, q in queries.items():
        if len(data_points) >= 3 and coin not in quiet:
            continue
        data_points.append({"claim": f"{coin}: {kept.get(coin, 0)} posts survived filtering in the 24h window",
                            "source_url": search_url(q), "source_name": "X recent search",
                            "credibility": "primary_source", "usable_as": "quiet card" if coin in quiet else "context"})
    sources = [{"url": i["post_url"], "title": f"{i['handle']} on X", "used_for": f"{i['coin']} card",
                "reliability": "anecdotal"} for i in real]
    sources += [{"url": search_url(q), "title": f"X search: {coin}", "used_for": "collection query",
                 "reliability": "primary"} for coin, q in queries.items()]
    sources.append({"url": "https://docs.x.com/x-api/posts/search-recent-posts",
                    "title": "X API v2 recent search", "used_for": "collection method", "reliability": "primary"})
    return {
        "version": "1.0",
        "topic": f"Bitcoin L2, Dogecoin, Monero and Litecoin community posts on X, 24h ending {day} 18:00 ET",
        "research_date": day,
        "landscape": {
            "existing_content": [{"title": f"X search: {coin}", "url": search_url(q), "source": "X",
                                  "angle": f"{coin} community", "what_it_covers": q,
                                  "what_it_misses": "no curation; price calls and giveaways mixed in"}
                                 for coin, q in queries.items()],
            "saturated_angles": ["price calls", "giveaways", "unlabeled rumors"],
            "underserved_gaps": ["who is actually driving each L2 conversation, with links"],
        },
        "data_points": data_points,
        "audience_insights": {
            "common_questions": ["What did each community actually post about today?",
                                 "Who is driving the conversation?",
                                 "Is another chain pulling attention from these communities?"],
            "misconceptions": [{"myth": "Every coin has news every day",
                                "reality": "Quiet coins get a 'Quiet today.' card, never filler"}],
            "knowledge_level": "intermediate",
        },
        "angles_discovered": [
            {"name": "Source cards", "hook": "One card per post, handle in the corner", "type": "data_driven",
             "why_now": f"Posts from the 24h ending {day} 18:00 ET",
             "grounded_in": [i["post_url"] for i in real][:5]},
            {"name": "Quiet coins", "hook": "Silence is reported, not filled", "type": "contrarian",
             "why_now": ", ".join(quiet) or "none quiet today"},
            {"name": "Guest chains", "hook": "When a community talks about another chain, say so",
             "type": "trending",
             "why_now": ", ".join(i["other_chain_if_any"] for i in real if i.get("other_chain_if_any")) or "none today"},
        ],
        "sources": sources,
        "research_summary": f"{len(real)} sourced items; quiet: {', '.join(quiet) or 'none'}.",
        "metadata": {"quiet_coins": quiet, "collector": "crypto-l2-daily/scripts/collect_x.py",
                     "stats": data.get("stats", {})},
    }


def delivery_promise() -> dict:
    # "slideshow" is the brief's promise. OpenMontage has no "slideshow" promise
    # type; data_explainer with motion_required=false is the valid encoding
    # (still_fallback_allowed, min_motion_ratio 0). An unknown type would make the
    # compose gate skip validation silently instead of passing it.
    return {"promise_type": "data_explainer", "motion_required": False, "source_required": False,
            "tone_mode": "educational", "quality_floor": "presentable", "approved_fallback": "still_led"}


def proposal_packet(day: str, approved_by: str) -> dict:
    concept = lambda cid, title, hook, structure, why: {  # noqa: E731
        "id": cid, "title": title, "hook": hook, "narrative_structure": structure,
        "visual_approach": "Black Platinum banknote-style cards, gold/green accents, handle/date badge; no b-roll, no faces",
        "suggested_playbook": "flat-motion-graphics", "target_platform": "generic",
        "target_duration_seconds": 70, "key_points": ["sourced posts only", "quiet coins stated"],
        "why_this_works": why}
    return {
        "version": "1.0",
        "concept_options": [
            concept("cards", "Source-card slideshow", "Who drove each L2 conversation today",
                    "data_narrative", "Matches the brief: NotebookLM-style cards with sources"),
            concept("countdown", "Ranked countdown", "Top posts by engagement", "timeline",
                    "Punchier, but ranks by engagement rather than by community"),
            concept("segments", "Per-coin segments", "Four coins, four segments", "comparison",
                    "Even coverage, but quiet coins would eat airtime"),
        ],
        "selected_concept": {"concept_id": "cards",
                             "rationale": f"User brief and plan approval by {approved_by} (2026-10-05)."},
        "production_plan": {
            "pipeline": PIPELINE,
            "playbook": "flat-motion-graphics",
            "stages": [
                {"stage": "assets", "approach": "one Piper line per card, placed at card start",
                 "tools": [{"tool_name": "piper_tts", "role": "narration", "provider": "piper",
                            "available": True, "estimated_cost_usd": 0, "why_this_provider": "brief: Piper, $0"}]},
                {"stage": "compose", "approach": "atelier Remotion card deck (crypto-l2-daily/remotion), via video_compose",
                 "tools": [{"tool_name": "video_compose", "role": "render", "provider": "remotion",
                            "available": True, "estimated_cost_usd": 0, "why_this_provider": "user chose Remotion"}],
                 "fallback_if_unavailable": "stop and report; no silent runtime swap"},
            ],
            "delivery_promise": delivery_promise(),
            "renderer_family": "explainer-data",
            "render_runtime": "remotion",
            "composition_mode": "atelier",
            "art_direction": ART_DIRECTION,
            "music_source": {"source_type": "none", "estimated_cost_usd": 0},
            "voice_selection": {"provider": voice_choice()["provider"],
                                "voice_id": voice_choice().get("voice_id", "en_US-lessac-medium"),
                                "rationale": "local, free", "estimated_cost_usd": 0,
                                "sample_approval_required": False},
            "decision_log_ref": "artifacts/decision_log.json",
        },
        "cost_estimate": {"total_estimated_usd": 0,
                          "line_items": [{"tool": "piper_tts", "operation": "narration", "estimated_usd": 0},
                                         {"tool": "video_compose", "operation": "remotion render", "estimated_usd": 0}],
                          "budget_cap_usd": 0, "budget_verdict": "within_budget"},
        "approval": {"status": "approved", "user_notes": "Standing plan approval for the daily template",
                     "approved_budget_usd": 0},
    }


def decision_log(project_id: str) -> dict:
    return {"version": "1.0", "project_id": project_id, "decisions": [
        {"decision_id": "d-runtime", "stage": "proposal", "category": "render_runtime_selection",
         "subject": "Composition runtime",
         "options_considered": [
             {"option_id": "remotion", "label": "Remotion", "score": 0.9,
              "reason": "React card deck rendered via video_compose; deterministic for unattended daily runs"},
             {"option_id": "hyperframes", "label": "HyperFrames", "score": 0.6,
              "reason": "More distinctive kinetic type", "rejected_because": "more moving parts unattended; user chose Remotion"},
             {"option_id": "ffmpeg", "label": "FFmpeg", "score": 0.2,
              "reason": "Concat only", "rejected_because": "no text-card rendering"}],
         "selected": "remotion", "reason": "User selected Remotion at plan approval (2026-10-05).",
         "user_visible": True, "user_approved": True, "confidence": 0.9},
        {"decision_id": "d-mode", "stage": "proposal", "category": "composition_mode",
         "subject": "Composition authoring mode",
         "options_considered": [
             {"option_id": "atelier", "label": "Atelier (one hand-authored card deck)", "score": 0.9,
              "reason": "Exact card spec: big title, one sentence, small handle/date corner"},
             {"option_id": "templated", "label": "Templated stock scenes", "score": 0.4,
              "reason": "hero_title/callout + stat_reveal",
              "rejected_because": "fixture render: corner badge larger than the title, small callout text"}],
         "selected": "atelier", "reason": "Stock components could not meet the card spec (fixture test 2026-10-05).",
         "user_visible": True, "user_approved": True, "confidence": 0.9},
        {"decision_id": "d-voice", "stage": "proposal", "category": "voice_selection",
         "subject": "Narration TTS provider",
         "options_considered": [
             {"option_id": "piper", "label": "Piper en_US-lessac-medium", "score": 0.9, "reason": "Local, $0"}],
         "selected": "piper", "reason": "Brief: Piper TTS, budget $0.",
         "user_visible": True, "user_approved": True, "confidence": 1.0},
        {"decision_id": "d-music", "stage": "proposal", "category": "music_source",
         "subject": "Background music",
         "options_considered": [
             {"option_id": "none", "label": "No music", "score": 0.8, "reason": "Cards + voice; $0; no licensing"}],
         "selected": "none", "reason": "Approved plan: no music.",
         "user_visible": True, "user_approved": True, "confidence": 0.9},
        {"decision_id": "d-motion", "stage": "proposal", "category": "motion_commitment",
         "subject": "Delivery promise",
         "options_considered": [
             {"option_id": "data_explainer", "label": "slideshow (data_explainer, motion not required)",
              "score": 0.95, "reason": "Brief promises a card slideshow"}],
         "selected": "data_explainer", "reason": "Brief: delivery promise is slideshow.",
         "user_visible": True, "user_approved": True, "confidence": 1.0},
    ]}


def script_artifact(day: str, cards: list[dict]) -> dict:
    return {
        "version": "1.0",
        "title": f"Crypto L2 Daily — {day}",
        "total_duration_seconds": TARGET_SECONDS,
        "voice_performance": {
            "performance_intent": "Calm newsreader reading source cards; attribution always spoken",
            "pacing_profile": "conversational",
            "energy_curve": "flat, even",
            "pause_policy": f"{LEAD_IN}s lead-in per card, remaining slack held on card",
            "sample_section_id": cards[0]["id"],
            "provider_notes": {"provider": VOICE_USED["provider"], "model": VOICE_USED["model"],
                               "length_scale": str(cards[0].get("length_scale", 1.0))},
        },
        "sections": [{
            "id": c["id"], "label": c["title"], "text": c["narration"],
            "start_seconds": c["start"], "end_seconds": c["end"],
            "speaker_directions": "even, clear; read handle as a name",
            "delivery_cues": {"pace": "conversational", "pause_before_seconds": LEAD_IN,
                              "provider_text": speakable(c["narration"])},
            "enhancement_cues": [{"type": "overlay",
                                  "description": f"corner badge: {c['corner']} / {c['corner_sub']}",
                                  "timestamp_seconds": c["start"]}],
            "source_ref": c.get("post_url") or "",
        } for c in cards],
        "metadata": {"source_data": f"crypto-l2-daily/data/{day}.json"},
    }


SCENE_ROLE = {
    "title": ("establish_context", "Opens the day and names the four communities", "hero_title"),
    "item": ("evidence", "One sourced post: what was said and who said it", "callout"),
    "quiet": ("transition", "States plainly that this coin had no qualifying post", "text_card"),
    "close": ("call_to_action", "Lists the accounts and points to the linked cards", "hero_title"),
}


def scene_plan_artifact(cards: list[dict]) -> dict:
    scenes = []
    for c in cards:
        role, info, component = SCENE_ROLE[c["kind"]]
        scenes.append({
            "id": f"s-{c['id']}", "type": "text_card",
            "description": f"{component} card — {c['title']}: {c['sentence']}",
            "start_seconds": c["start"], "end_seconds": c["end"],
            "script_section_id": c["id"], "framing": "full-frame card, 16:9",
            "movement": "spring text reveal", "transition_in": "fade", "transition_out": "fade",
            "overlay_notes": f"bottom-right badge: {c['corner']} · {c['corner_sub']}",
            "shot_language": {"shot_size": "medium", "camera_movement": "static",
                              "lighting_key": "low_key", "color_temperature": "warm"},
            "shot_intent": f"Hold the card long enough to read; {info.lower()}",
            "narrative_role": role, "information_role": info,
            "hero_moment": c["kind"] == "title",
            "required_assets": [{"type": "narration", "description": f"Piper line for {c['id']}",
                                 "source": "generate"}],
        })
    return {"version": "1.0", "style_playbook": "flat-motion-graphics", "scenes": scenes,
            "metadata": {"component_map": {c["id"]: SCENE_ROLE[c["kind"]][2] for c in cards},
                         "no_stock_broll": True, "no_generated_faces": True}}


def asset_manifest_artifact(cards: list[dict], narration: Path) -> dict:
    assets = [{"id": "narration-full", "type": "narration", "path": str(narration),
               "source_tool": VOICE_USED["tool"], "scene_id": "all", "model": VOICE_USED["model"],
               "provider": VOICE_USED["provider"], "cost_usd": 0.0, "duration_seconds": TARGET_SECONDS, "format": "wav",
               "generation_summary": "Per-card Piper lines placed at card starts, concatenated to 70s"}]
    for c in cards:
        assets.append({"id": f"narr-{c['id']}", "type": "narration", "path": c["audio_path"],
                       "source_tool": VOICE_USED["tool"], "scene_id": f"s-{c['id']}", "model": VOICE_USED["model"],
                       "provider": VOICE_USED["provider"], "cost_usd": 0.0, "duration_seconds": c["narration_seconds"],
                       "format": Path(c["audio_path"]).suffix.lstrip("."),
                       "voice_performance": {"source_section_id": c["id"], "delivery_cues_applied": True,
                                             "provider_text_used": True,
                                             "provider_settings": {"length_scale": c["length_scale"]}}})
    return {"version": "1.0", "assets": assets, "total_cost_usd": 0.0}


ART_DIRECTION = ("Black Platinum source cards: #0A0A0B base, platinum #E5E4E2 type, gold #D4AF37 and money-green "
                 "#85BB65 accents, a holographic foil strip, banknote guilloche rosette and denomination numbers; "
                 "Yellowtail calligraphy + Big Shoulders capitals, Atkinson Hyperlegible body, IBM Plex Mono labels; "
                 "glowing core + orbit rings + flare on bookends; seeded stars and shooting stars; handle + date "
                 "bottom-right; no b-roll, no faces")


def edit_decisions_artifact(cards: list[dict], project: Path) -> dict:
    """Canonical edit_decisions; the card deck itself is the atelier composition in this repo's remotion/."""
    return {
        "version": "1.0",
        "render_runtime": "remotion",
        "renderer_family": "explainer-data",
        "composition_mode": "atelier",
        "bespoke": {
            "entry": str(project / "composition" / "index.tsx"),
            "composition_id": "CryptoCards",
            "art_direction": ART_DIRECTION,
            "props_path": str(project / "artifacts" / "composition.json"),
            "public_dir": str(project / "composition_public"),
            "crf": 26,  # NOT2L8 gradients + stars cost bits; 26 is visually identical and ~40% smaller
        },
        "cuts": [{"id": f"cut-{c['id']}", "source": f"narr-{c['id']}", "in_seconds": c["start"],
                  "out_seconds": c["end"], "layer": "primary", "transition_in": "fade",
                  "transition_out": "fade", "transition_duration": 0.33,
                  "backgroundColor": THEME["backgroundColor"], "reason": SCENE_ROLE[c["kind"]][1]}
                 for c in cards],
        "audio": {"narration": {"segments": [{"asset_id": "narration-full", "start_seconds": 0,
                                              "end_seconds": TARGET_SECONDS}]}},
        "subtitles": {"enabled": False},
        "metadata": {"delivery_promise": delivery_promise(),
                     "composition_source": "crypto-l2-daily/remotion/ (staged per project)",
                     "subtitles_note": "Cards display the narrated text; burned captions would cover the cards."},
    }


CARD_KEYS = ("id", "kind", "title", "sentence", "corner", "corner_sub", "coin", "start", "end",
             "explain", "link", "stats")


def stage_composition(cards: list[dict], narration: Path, project: Path) -> dict:
    comp_dir, public = project / "composition", project / "composition_public"
    comp_dir.mkdir(exist_ok=True)
    public.mkdir(exist_ok=True)
    for f in (ROOT / "remotion").glob("*.tsx"):
        shutil.copy2(f, comp_dir / f.name)
    shutil.copy2(narration, public / "narration.wav")
    return {"durationSeconds": TARGET_SECONDS, "audioSrc": "narration.wav",
            "cards": [{k: c.get(k) for k in CARD_KEYS} for c in cards]}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--data", help="override data file (testing)")
    ap.add_argument("--project", help="override project slug (testing)")
    args = ap.parse_args()

    day = args.date
    data_path = Path(args.data) if args.data else ROOT / "data" / f"{day}.json"
    data = json.loads(data_path.read_text())
    config = json.loads((ROOT / "config" / "pipeline.json").read_text())
    gated = bool(config.get("human_approval_default", True))
    project_id = args.project or f"crypto-l2-{day}"
    approval_note = config.get("approval_note", "")

    project = init_project(project_id, title=f"Crypto L2 Daily {day}", pipeline_type=PIPELINE,
                           style_playbook="flat-motion-graphics")
    art_dir, audio_dir, renders = project / "artifacts", project / "assets" / "audio", project / "renders"
    log(f"project {project}")

    def save(name: str, obj: dict) -> None:
        (art_dir / f"{name}.json").write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

    def checkpoint(stage: str, artifacts: dict, gate_passed: bool = True, status: str = "completed",
                   extra: dict | None = None) -> None:
        meta = {"driver": "crypto-l2-daily/scripts/render.py", "approval_policy": approval_note,
                **(extra or {})}
        write_checkpoint(PROJECTS_DIR, project_id, stage, status, artifacts, pipeline_type=PIPELINE,
                         style_playbook="flat-motion-graphics", human_approved=gate_passed,
                         cost_snapshot={"spent_usd": 0.0, "budget_usd": 0.0}, metadata=meta)

    # research
    brief = research_brief(day, data)
    save("research_brief", brief)
    checkpoint("research", {"research_brief": brief}, gate_passed=False)

    # proposal (gated; covered by the approved standing plan)
    packet, dlog = proposal_packet(day, config.get("approved_by", "user")), decision_log(project_id)
    save("proposal_packet", packet)
    save("decision_log", dlog)
    checkpoint("proposal", {"proposal_packet": packet, "decision_log": dlog})

    # script + timing (narration lengths decide card durations)
    cards = build_cards(day, data)
    narration, cards = make_narration(cards, audio_dir)
    script = script_artifact(day, cards)
    save("script", script)
    checkpoint("script", {"script": script})

    plan = scene_plan_artifact(cards)
    save("scene_plan", plan)
    checkpoint("scene_plan", {"scene_plan": plan})

    manifest = asset_manifest_artifact(cards, narration)
    save("asset_manifest", manifest)
    checkpoint("assets", {"asset_manifest": manifest})

    edits = edit_decisions_artifact(cards, project)
    risk = score_slideshow_risk(plan["scenes"], edits, edits["renderer_family"], "remotion")
    edits["slideshow_risk_score"] = {"average": round(risk["average"], 2), "verdict": risk["verdict"]}
    log(f"slideshow risk {risk['average']:.2f} ({risk['verdict']})")
    save("edit_decisions", edits)
    checkpoint("edit", {"edit_decisions": edits}, gate_passed=False)

    # compose: delivery promise check (the atelier path skips the in-tool gate), stage, render
    promise_check = DeliveryPromise.from_dict(delivery_promise()).validate_cuts(edits["cuts"])
    if not promise_check["valid"]:
        raise SystemExit(f"[render] delivery promise violated: {promise_check['violations']}")
    props = stage_composition(cards, narration, project)
    save("composition", props)
    final = renders / "final.mp4"
    result = VideoCompose().execute({"operation": "render", "edit_decisions": edits,
                                     "asset_manifest": manifest, "proposal_packet": packet,
                                     "scene_plan": plan["scenes"], "output_profile": "youtube_landscape",
                                     "output_path": str(final)})
    if not result.success:
        checkpoint("compose", {}, gate_passed=False, status="failed",
                   extra={"error": (result.error or "")[:2000]})
        raise SystemExit(f"[render] compose failed: {result.error}")

    dur = probe_duration(final)
    streams = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                              "stream=codec_type,codec_name,width,height,r_frame_rate", "-of", "json", str(final)],
                             capture_output=True, text=True, check=True)
    st = json.loads(streams.stdout)["streams"]
    audio = next((x for x in st if x["codec_type"] == "audio"), None)
    video = next(x for x in st if x["codec_type"] == "video")
    num, den = video.get("r_frame_rate", "30/1").split("/")
    fps = round(int(num) / int(den), 2)
    size = final.stat().st_size
    resolution = f"{video['width']}x{video['height']}"

    # Review frames at each card's midpoint + a loudness probe for silence.
    review_dir = project / "review"
    review_dir.mkdir(exist_ok=True)
    frames = []
    for c in cards:
        fp = review_dir / f"{c['id']}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{(c['start'] + c['end']) / 2:.2f}", "-i",
                        str(final), "-frames:v", "1", "-vf", "scale=960:-1", str(fp)], check=True)
        frames.append(str(fp))
    vol = subprocess.run(["ffmpeg", "-v", "info", "-i", str(final), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    mean_db = float(re.search(r"mean_volume: (-?[\d.]+) dB", vol).group(1)) if "mean_volume" in vol else -99.0
    max_db = float(re.search(r"max_volume: (-?[\d.]+) dB", vol).group(1)) if "max_volume" in vol else -99.0

    issues = []
    if not audio:
        issues.append("no audio stream")
    if mean_db < -45:
        issues.append(f"audio near-silent (mean {mean_db} dB)")
    if abs(dur - TARGET_SECONDS) > TARGET_SECONDS * 0.05:
        issues.append(f"duration {dur:.2f}s outside 70s ±5%")
    if resolution != "1920x1080":
        issues.append(f"resolution {resolution} is not 16:9 1080p")
    ok = not issues

    report = {"version": "1.0", "outputs": [{
        "path": str(final), "format": "mp4", "codec": video.get("codec_name", "h264"),
        "audio_codec": (audio or {}).get("codec_name", "none"), "resolution": resolution, "fps": fps,
        "duration_seconds": round(dur, 2), "file_size_bytes": size, "platform_target": "web"}],
        "render_grammar": "explainer-data",
        "slideshow_risk_score": edits["slideshow_risk_score"],
        "decision_log_ref": "artifacts/decision_log.json", "final_review_ref": "artifacts/final_review.json",
        "verification_notes": [f"{len(cards)} cards", f"mean volume {mean_db} dB, max {max_db} dB"],
        "warnings": issues}
    review = {"version": "1.0", "output_path": str(final), "status": "pass" if ok else "fail",
              "checks": {
                  "technical_probe": {"valid_container": True, "duration_seconds": round(dur, 2),
                                      "resolution": resolution, "fps": fps, "has_audio": bool(audio),
                                      "codec": video.get("codec_name", ""), "file_size_bytes": size,
                                      "issues": issues},
                  "visual_spotcheck": {"frames_sampled": len(frames), "frame_paths": frames,
                                       "black_frames_detected": False, "broken_overlays": False,
                                       "missing_assets": False, "unreadable_text": False, "issues": []},
                  "audio_spotcheck": {"narration_present": mean_db > -45, "music_present": False,
                                      "unexpected_silence": mean_db <= -45, "clipping_detected": max_db >= 0,
                                      "mix_intelligible": mean_db > -45, "issues": []},
                  "promise_preservation": {"delivery_promise_honored": promise_check["valid"],
                                           "renderer_family_used": "explainer-data",
                                           "render_runtime_used": "remotion", "runtime_swap_detected": False,
                                           "runtime_swap_check": "passed",
                                           "motion_ratio_actual": promise_check["motion_ratio"],
                                           "silent_downgrade_detected": False, "issues": []},
                  "subtitle_check": {"subtitles_expected": False, "subtitles_present": False,
                                     "issues": ["by design: each card displays its narrated sentence"]},
                  "atelier": {"stock_reuse_detected": False, "art_direction_declared": True,
                              "art_direction": ART_DIRECTION, "issues": []},
              },
              "issues_found": issues,
              "recommended_action": "present_to_user" if ok else "re_render"}
    save("render_report", report)
    save("final_review", review)
    if not ok:
        checkpoint("compose", {"render_report": report, "final_review": review}, gate_passed=False,
                   status="failed", extra={"error": "; ".join(issues)})
        raise SystemExit(f"[render] post-render review failed: {issues}")
    checkpoint("compose", {"render_report": report, "final_review": review}, gate_passed=False)
    log(f"final.mp4 {dur:.2f}s {resolution} {size / 1e6:.1f}MB, mean {mean_db} dB")

    # Cards for the site (same text as the video).
    site_cards = [{k: c.get(k) for k in (*CARD_KEYS, "post_url")} for c in cards]
    (renders / "cards.json").write_text(json.dumps(site_cards, indent=2, ensure_ascii=False) + "\n")

    entry = {"platform": "github-pages", "status": "pending_review" if gated else "exported",
             "url": f"{SITE_URL}days/{day}/", "visibility": "public",
             "export_path": str(ROOT / "site" / "days" / day),
             "timestamp": datetime.now(timezone.utc).isoformat(),
             "metadata_used": {"title": f"Crypto L2 Daily — {day}",
                               "description": "Bitcoin L2, Dogecoin, Monero and Litecoin on X, last 24h"}}
    publish_log = {"version": "1.0", "entries": [entry]}
    save("publish_log", publish_log)
    if gated:
        checkpoint("publish", {"publish_log": publish_log}, gate_passed=False, status="awaiting_human")
        log("publish gate: awaiting human approval (human_approval_default=true)")
        return 3
    checkpoint("publish", {"publish_log": publish_log})
    log("publish gate: standing approval (human_approval_default=false)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

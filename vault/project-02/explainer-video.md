---
number: 20
group: "Extras"
short: "Explainer video"
question: "How do I make the explainer video for the site?"
hint: "Use the master prompt. Then make the 8 shots one at a time."
answer: "Copy the master prompt into a video tool. Make the 8 shots in order. Save the result as site/assets/explainer.mp4. The next build puts it in the site's intro guide and the README."
cssclasses: [l2-daily]
tags: [ai101, project-2, video, prompt]
---

# 🎬 The explainer video: the prompt

> [!abstract] 🎯 What this video does
> It is a **90-second** "how it works" video. It plays in the site's **❓ Guide** pop-up and in the **README**.
> It explains **4 things**: 1️⃣ how to use the site, 2️⃣ what it does, 3️⃣ the automation core, 4️⃣ the phone widget.

## 🔢 How to use this prompt

1. 📋 Copy the **master prompt** below into your video tool.
2. 🎞️ Make the **8 shots** one at a time. Use the **shot prompts**.
3. ✂️ Put the shots together. Add the **narration** and the **captions**.
4. 💾 Save the video as `site/assets/explainer.mp4`. Save one frame as `site/assets/explainer-poster.jpg`.
5. 🏗️ Run `python3 scripts/build_site.py`. The pop-up now plays your video.

> [!tip] 🧰 Good tools for this
> - **AI video:** Runway, Kling, Veo or Sora. Make one shot at a time.
> - **Math-style 3D:** Manim (the 3Blue1Brown tool) for the flow graph and the number line.
> - **Manga frames:** draw the Guide in Procreate or Clip Studio. Or use an image model. Then animate.

## 💎 Master prompt

```text
Make a 90-second, 16:9, 1920x1080, 30 fps explainer video called "Crypto L2 Daily: How It Works."

STYLE: 3Blue1Brown-style clean 3D math animation (deep black space, smooth slow camera moves, objects
that morph, glowing vector arrows, number lines, flow graphs) fused with Japanese-American manga and anime
(cel-shaded characters, bold ink outlines, screentone dots, speed lines, impact frames, panel-split
transitions, small chibi reaction moments). Premium, calm, clever. Not noisy.

PALETTE: black #0A0A0B, platinum #E5E4E2, holographic foil gradient (gold #F3D77A -> mint #9FF5C8 ->
ice #A7E8FF -> lilac #C9B6FF -> blush #FFD1EC), gold #D4AF37, money green #85BB65. Nothing else.

DESIGN DETAILS: banknote art (guilloche rosette line patterns, microprint borders, serial numbers like
"No. CL2-20261005-08", big denomination numbers 01 to 05 for steps). Industrial streetwear details: labels in
quotation marks like "VIDEO", "CARDS", "WIDGET"; black-and-platinum diagonal stripe tape; arrows.
Calligraphy script for one word per title (like a banknote signature) plus bold condensed capitals.

HERO OBJECT: a holographic platinum torus knot with gold and green glowing seams, a gold core, two orbit
rings (gold, green), floating dust, and comets that curve around it by gravity.

CHARACTER: "The Guide": a friendly smiling young person with multi-color locs, platinum bomber jacket,
gold chain, drawn in manga style. The Guide points, explains and reacts. No real person's face.

NARRATION: warm, clear voice. Short, simple sentences (ASD-STE100 style). Easy for an 8-year-old.
CAPTIONS: burned in, Atkinson Hyperlegible font, platinum text, gold highlight on key words.
MUSIC: soft lo-fi synth with light taiko hits on scene changes. Low under the voice.

DO NOT: show real logos (no X, Nike, Off-White or bank logos), real banknotes, real people, price
predictions, made-up posts, or the words "buy" or "invest".
```

## 🎞️ The 8 shots

| # | ⏱️ Time | 🎨 What we see | 🎙️ Narration (say it like this) |
|---|---|---|---|
| 01 | 0:00–0:08 | Black space. The holographic knot spins in. A manga impact frame flashes. Calligraphy "Crypto L2" writes itself in gold. "DAILY" slams in, in big platinum capitals. | "This is Crypto L2 Daily. It is a robot that makes the news." |
| 02 | 0:08–0:20 | A 3D clock hits 6:00 PM. A river of glowing post cards flows past. 4 coin tokens rise up: ⚡ gold, 🐕 green, 🔒 platinum, 🪙 ice blue. | "Every day at 6 PM, the robot reads X. It looks for real posts about 4 coins." |
| 03 | 0:20–0:32 | **The core, part 1.** A 3Blue1Brown flow graph. Nodes 01 to 05 light up in turn: Collect, Check, Video, Human check, Publish. | "It follows 5 steps. Collect. Check. Make the video. A human check. Publish." |
| 04 | 0:32–0:45 | **The core, part 2.** A filter funnel. Junk cards ("price guess", "ad", "copy") bounce off with speed lines. A chibi Guide sweeps them away. A calendar number line: an October post tries to jump into July. A gold arrow blocks it. | "The robot removes ads, price guesses and copies. It checks every date. Old posts stay out." |
| 05 | 0:45–1:00 | **How to use it.** A laptop and a phone show the site. Big numbers appear: 1 press play, 2 read the cards, 3 tap a card. The real post opens. | "To use it: press play. Read the cards. Tap a card to see the real post." |
| 06 | 1:00–1:12 | **The course.** Obsidian note pages fly out of a book into the website. Question cards flip. 💡 Hint glows gold. ✅ Answer glows green. | "Want to learn how it works? Open the course. Tap a hint. Then tap the answer." |
| 07 | 1:12–1:24 | **The widget.** An iPhone Home Screen. A small black platinum card slides in. It shows the Bitcoin price, the fee and a headline. A "TEST FEATURE" stripe tape label. | "You can also put a small card on your phone. It shows the price, the fee and today's news." |
| 08 | 1:24–1:30 | The knot shrinks into a banknote seal. A serial number types out. The signature "NOT2L8" writes in gold script. | "Real posts. Real sources. Every day. Not too late. Always forward." |

## ✅ Checklist before you publish the video

1. ⏱️ It is **90 seconds or less**.
2. 🔤 Every **caption** matches the narration.
3. 🚫 It shows **no real logos** and **no price predictions**.
4. 💾 It is saved as `site/assets/explainer.mp4`.
5. 🖼️ The poster is saved as `site/assets/explainer-poster.jpg`.

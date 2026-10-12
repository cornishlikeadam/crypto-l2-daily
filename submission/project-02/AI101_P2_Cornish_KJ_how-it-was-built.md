---
number: 17
group: "Extras"
short: "How it was built"
question: "How was each part built? What is generic, and what is unique?"
hint: "Every AI 101 workflow has the same 5 parts. Look at the right column for what makes this one different."
answer: "It uses the generic AI 101 shape: Trigger, Context, Task, Output, Human check. The unique parts are the strict post rules, the date check, the 70-second card video, the Black Platinum site, the course hub and the phone widget."
cssclasses: [l2-daily]
tags: [ai101, project-2, build]
---

# 🏗️ How it was built: generic vs. unique

> [!abstract] 💵 The short version
> Every AI 101 workflow has the **same 5 parts**. This project uses that **generic** shape. The **unique** parts are in the right column.

## 1️⃣ The generic AI 101 shape → this project

| # | 🧩 Generic part (AI 101) | 📄 Here | 💎 What is unique here |
|---|---|---|---|
| 01 | ⏰ **Trigger:** a set time starts the workflow. | [[AI101_P2_Cornish_KJ_01-collect-posts.md|01-collect-posts]] | **6 PM** New York time, every day. The Mac's **launchd** timer starts `scripts/daily.sh`. If the Mac sleeps, it runs at the next wake. |
| 02 | 📥 **Context:** what the model needs first. | [[AI101_P2_Cornish_KJ_02-check-posts.md|02-check-posts]] | **4 coin searches** and a list of **"remove it" rules**. The **date check** is rule 1. |
| 03 | ⚙️ **Task:** the job itself. | [[AI101_P2_Cornish_KJ_03-make-video.md|03-make-video]] | Pick up to **3 posts per coin**. Make **8–10 cards**. Add a **free voice**. Fit it into **70 seconds**. |
| 04 | 📦 **Output:** what comes out. | [[AI101_P2_Cornish_KJ_05-publish.md|05-publish]] | A **video**, a **web page**, **course pages**, a **feed** and a **phone-widget file**. It says **LIVE** only if the page loads. |
| 05 | 🧑‍⚖️ **Human check:** the step that stays mine. | [[AI101_P2_Cornish_KJ_04-human-check.md|04-human-check]] | I approved the **first** video. I check every **archive day**. |

## 2️⃣ Each feature, part by part

| # | ✨ Feature | 🧰 Generic tool | 💎 Unique twist | 📁 File |
|---|---|---|---|---|
| 01 | 🔎 Post collector | a web scraper (twikit) | **1 connection** for 4 searches. A **fixed copy** of twikit that I checked. | `scripts/collect_x.py` |
| 02 | 🧹 Junk filter | keyword rules | Removes **price guesses**, **shills**, **tiny accounts**, **copies** and **wrong-day** posts. | `scripts/collect_x.py` |
| 03 | 🎬 Video | Remotion + OpenMontage | **Black Platinum cards** with banknote patterns, serial numbers and a holographic foil edge. | `remotion/CardDeck.tsx`, `scripts/render.py` |
| 04 | 🎙️ Voice | Piper (free) | Reads **fewer words** when it is too long. **Never** faster than 1.15×. | `scripts/render.py` |
| 05 | 🌐 Website | static HTML pages | **One Python file** builds every page every day. Nothing gets wiped. | `scripts/build_site.py` |
| 06 | 🎨 Design | CSS | **Black platinum**, **holographic foil**, **gold** and **money green**. Banknote **guilloche** rosettes, **serial numbers**, big **denomination** step numbers, `"QUOTED"` labels and **stripe tape**. | `scripts/site_theme.py` |
| 07 | 💎 3D shape | three.js | A **holographic platinum** torus knot with **gold** and **green** seams. It **pauses** when you scroll away. | `scripts/site_theme.py` |
| 08 | 📡 Live numbers | public data sites | **7 live numbers**. A **green** dot means live. A **gold** dot means "last saved." It **never** shows a made-up number. | `scripts/site_theme.py` |
| 09 | ❓ Intro guide | a pop-up window | **4 numbered pages**: how to use it, what it does, the core, the widget. It opens **1 time**. | `scripts/site_theme.py` |
| 10 | 📚 Course hub | Markdown to HTML | **This vault** becomes **question cards** with 💡 **hint** and ✅ **answer** buttons. Obsidian and the site read the **same files**. | `scripts/course_pages.py` |
| 11 | 📱 Phone widget | Scriptable (iPhone) | A **download-only** script. It shows the **BTC price**, the **fee** and **today's top 3 posts**. | `site/scriptable.js`, `site/widget.json` |

## 3️⃣ The writing rules (ASD-STE100)

> [!tip] ✍️ Simple Technical English
> The notes use an **ASD-STE100-inspired** approach. This is not a formal compliance claim. See [[AI101_P2_Cornish_KJ_documentation-standard.md|documentation-standard]].
> 1. Write **short sentences**. Use **20 words or fewer** for an instruction.
> 2. Write **one instruction** in each sentence.
> 3. Use the **active voice**. Example: "The robot removes the post."
> 4. Use **simple words**. Explain a hard word in [[AI101_P2_Cornish_KJ_glossary.md|glossary]].
> 5. Put steps in a **numbered list**.

## 4️⃣ The palette

| 🎨 Name | 🔢 Code | 🎯 Job |
|---|---|---|
| ⬛ Black | `#0A0A0B` | the background |
| 🪙 Platinum | `#E5E4E2` | the text |
| 🥇 Gold | `#D4AF37` / `#F3D77A` | numbers, buttons, Bitcoin |
| 💵 Money green | `#85BB65` | numbers, Dogecoin |
| 🌿 Mint | `#9FF5C8` | "live" dots |
| 🌈 Holographic foil | gold → mint → ice → lilac → blush | edges, frames, the 3D shape |

## 5️⃣ The fonts

| 🔤 Font | 🎯 Job |
|---|---|
| ✒️ **Yellowtail** | calligraphy words, like a signature on a banknote |
| 🏟️ **Big Shoulders** | big bold headings and numbers |
| 👀 **Atkinson Hyperlegible** | body text. It is made to be **easy to read**. |
| ⌨️ **IBM Plex Mono** | labels, serial numbers, live numbers |

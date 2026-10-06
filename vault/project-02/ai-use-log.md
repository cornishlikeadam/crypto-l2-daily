---
number: 11
group: "Proof"
short: "AI use log"
question: "When did the AI work, and what did I keep, change or reject?"
hint: "Each row is one run. Look at the last column."
answer: "The log has 15 runs, in order. For each run, I wrote what I asked, what the AI made, and my decision: keep, change or reject, with a reason."
cssclasses: [l2-daily]
tags: [ai101, project-2, ai-log]
---

# 🤖 ai-use-log.md

> [!info] 📒 How to read this log
> Every run is in **order**. The AI was **Claude** (Claude Code). The last column is **my decision**: ✅ keep, 🔧 change or ❌ reject.

| # | 📅 Date | 🗣️ What I asked the AI | 📦 What it made | 🧑‍⚖️ My decision |
|---|---|---|---|---|
| 01 | Oct 5 | Build a daily crypto video robot from my plan. | A plan and 3 choices for me (X source, video tool, approval). | ✅ **Keep.** I chose the official X API, Remotion and a public repo. |
| 02 | Oct 5 | Test the whole pipeline with fake posts. | A test video with fake accounts. It was **never published**. | ❌ **Reject** the first look. The account name was bigger than the title. The AI made a custom card design. |
| 03 | Oct 5 | Run with the official X API. | Nothing. I could not buy X credits. | 🔧 **Change** the plan. |
| 04 | Oct 5 | Use my xAI key. | The AI checked the key. My xAI team was blocked. | ❌ **Reject.** The AI warned me: I pasted my key in chat. I must delete it. |
| 05 | Oct 5 | Use a free scraper. | The robot, with twikit and my X login codes. | ✅ **Keep.** I pasted a login code in chat by mistake. I logged out to kill it. Then I used the safe helper script. |
| 06 | Oct 5 | First real run. | Error: "Couldn't get KEY_BYTE indices." | 🔧 The AI found the cause (Source 2). I installed the fixed copy **after** it checked the code. |
| 07 | Oct 5 | Second run. | Bitcoin worked. Dogecoin failed (404). | 🔧 The AI made the robot use **one connection** for all searches. |
| 08 | Oct 5 | Third run: first real cards. | 8 cards. See [[outputs/first-run]]. | ❌ **Reject 4 cards:** a price guess, a "crypto shiller" and 2 tiny promo accounts. |
| 09 | Oct 5 | Make the filters stricter. | 7 cards. Dogecoin is "Quiet today." | ✅ **Keep.** See [[outputs/revised-run]]. |
| 10 | Oct 5 | Make the video. | The voice was 98 seconds for a 70-second video. | 🔧 **Change:** read fewer words aloud. Show all the words on the card. |
| 11 | Oct 5 | Approve and publish. | Live on the website. | ✅ I approved it with `approve_sample.sh`. |
| 12 | Oct 5 | Add 3 important days to the archive. | July 22, August 2, September 30, with real posts. | ❌ **Reject** the first try: an October post on old days, a government "DOGE" post and fancy-font text. ✅ **Keep** the fixed version. |
| 13 | Oct 5 | Add more than a quote to each slide. | A "What is this?" line, the source link and the like count. | ✅ **Keep.** |
| 14 | Oct 5 | Build this Obsidian vault. | This folder. | ✅ **Keep.** I must rewrite [[intent]] in my own words. |
| 15 | Oct 6 | Redesign the site and video. Put this vault on the site. Rewrite the notes in short, simple sentences. | The Black Platinum site, the course hub, the intro guide and these notes. | ✅ **Keep.** The old site address was blocked by Vercel. The site moved to **not2l8-l2-daily.vercel.app**. |

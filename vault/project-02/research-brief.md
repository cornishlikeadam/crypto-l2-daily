---
number: 10
group: "Proof"
short: "Research"
question: "Which 2 facts does the robot depend on, and are they true?"
hint: "One fact is about money. One fact is about a broken tool."
answer: "Fact 1: X's official API is not free ($0.005 per post). Fact 2: the normal free scraper (twikit) is broken, so the robot uses a fixed copy that I checked."
cssclasses: [l2-daily]
tags: [ai101, project-2, research]
---

# 🔬 research-brief.md

## ❓ Research question

Can a **free** robot read X every day? Can it make an **honest** crypto news video with **no made-up posts**?

## ✅ Short answer

> [!success] 💡 Yes, with 3 conditions
> 1. 💸 **Not with X's official tool.** It costs money now: **$0.005 for each post**. The free plan ended on **February 6, 2026**.
> 2. 🛠️ **Use the free scraper "twikit."** It logs in like a person. The normal download is **broken** since **March 18, 2026**. The robot uses a **fixed copy**. I checked it line by line.
> 3. 📅 **Check every date.** X search can give posts from the **wrong day**. So the robot checks each date itself.

## 1️⃣ Claim 1: The official X API is not free

- 💬 **The claim I checked:** You can read X posts for free with X's official API.
- 📄 **What the source says:** OpenTweet (updated July 2026): "On February 6, 2026, X made pay-per-use the default pricing model for its API and discontinued the free tier for new developer signups." Reading a post costs "$0.005 per post returned."
- 🔧 **The corrected claim:** The official X API costs **$0.005 per post**. New users get **no free plan**.
- 🎯 **Why it matters:** My first plan used the official API. At 400 posts a day, that is **$2.00 a day**. Also, X did not let me buy credits.
- 📏 **The rule it supports:** The robot uses the **free route** (login codes + twikit). See [[01-collect-posts]].

## 2️⃣ Claim 2: The free scraper works right away

- 💬 **The claim I checked:** You can install twikit, and it works.
- 📄 **What the source says:** GitHub issue #408 (March 18, 2026): "Twitter changed their ondemand.s.js structure so the regex in transaction.py no longer matches." My Mac showed the same error.
- 🔧 **The corrected claim:** The normal twikit download is **broken**. A **fixed copy works**. Before I installed it, I checked that it talks **only to X's own servers**.
- 🎯 **Why it matters:** Without the fix, step 1 fails **every day**. Then no video gets made. X changes its site every few weeks. So this can **break again**.
- 📏 **The rule it supports:** If collecting fails, the robot **stops**. It publishes **nothing**. A broken day never becomes a wrong video. See [[01-collect-posts]].

---

> [!important] ⭐ The check I protect because of this research
> The robot **checks every post's date itself**. It **never** trusts X's date filter alone. See [[02-check-posts]].

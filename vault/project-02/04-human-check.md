---
number: 6
group: "The 5 steps"
short: "Step 4 · My check"
question: "Step 4: What do I check before a video goes online?"
hint: "Watch it, open the links, check the dates, look for hype."
answer: "I watch the whole video. I open 2 post links and compare the words. I check every date. I check for price guesses, ads and made-up news. Then I approve it."
cssclasses: [l2-daily]
tags: [ai101, project-2, step, human-check]
---

# 🧑‍⚖️ Step 4: Human check (me)

> [!info] ⏰ What starts this step
> The **first video** is ready (October 5, 2026). Or a **new archive day** is ready.

## 📥 What goes in

The **video** and the **card list**.

## ⚙️ What this step does

**I decide** if the video can go on the website.

## 🔢 Directions for me

1. 👀 Watch **the whole video**.
2. 🔗 Open **at least 2** post links. Check that the words **match the card**.
3. 📅 Check that **every date** is inside the right 24 hours.
4. 🚫 Check that **nothing** is a price guess, an ad, or made up.
5. ✅ If it is good, run this command:
   `/bin/bash ~/crypto-l2-daily/scripts/approve_sample.sh 2026-10-05`

## ✅ What "good" looks like

Every card **passes checks 2, 3 and 4**.

> [!important] ⭐ This whole step is the check
> Until I approved, the robot **could not publish**.
> On **October 5, 2026**, I approved the first video. After that, the robot **publishes by itself** every day. (`human_approval_default` changed to `false`.)

## 🕵️ What this check found

| 🐞 Problem | 🔧 Fix |
|---|---|
| A Monero post from **October 5** showed up on the July, August and September archive days. | A **strict date rule**. |
| A post about the **government "DOGE" office** counted as Dogecoin. | A **new rule**. |
| **Price talk** ("$CATE will go to a billion") and **ad accounts**. | **New rules**. |

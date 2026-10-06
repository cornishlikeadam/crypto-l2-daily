---
number: 1
group: "Start"
short: "Start here"
question: "What does the robot make, and what rules does it follow?"
hint: "Think about the clock, the video length, and where the posts come from."
answer: "Every day at 6 PM, it makes a 70-second video and a web page. It uses only real posts from X, from the last 24 hours. It never makes up news."
cssclasses: [l2-daily]
tags: [ai101, project-2]
---

# 🚀 Start here: Crypto L2 Daily

## 🎯 The goal

Every day at **6 PM**, the robot makes **two things**:

1. 🎬 A **70-second video**.
2. 🌐 A **web page** with one card for each post.

They show what people **really posted** on X. X is a social media app. The posts are about **4 coins**: Bitcoin, Dogecoin, Monero and Litecoin. Each card links to the **real post**.

## 🔢 How to use this folder

1. 🗺️ Open `process-map.canvas`. It shows the steps in order.
2. 📄 Read the step files in order: [[01-collect-posts]], [[02-check-posts]], [[03-make-video]], [[04-human-check]], [[05-publish]].
3. ✋ Do **one step at a time**. After each step, stop. Say what happened. Then go on.

## 📜 The rules

> [!important] ⭐ Rule 1: Only real posts
> Every card comes from a **real post** on X. It shows the **account name**, the **date** and a **link**.
> If a coin has nothing good, the card says **"Quiet today."** The robot **never makes up news**.

- ⏰ **Only the last 24 hours.** A post from another day is removed. This is true even if X shows it.
- 🚫 **No price guesses, giveaways, rumors or ads.** The robot removes them **before** it makes a card.
- 👯 **No copies.** If 3 accounts post the same words, the robot makes **1 card**.
- 🆓 **Free and simple.** No paid tools. The voice is **Piper** (free). **OpenMontage** (free) makes the video.
- ✅ **Never say "live" too early.** The robot checks that the page **loads**. Only then does it say **"LIVE."**

## 🧑‍⚖️ What stays **my** decision

1. ✅ Is a video **good enough** for the website? I approved the first one by hand ([[04-human-check]]).
2. 🗂️ Which old days go in the archive, and **why** they matter.
3. ⚠️ Do I use **my X account** for the free scraper? X can limit the account.

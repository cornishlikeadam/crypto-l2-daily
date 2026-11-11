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

1. Read this file first. Then open `process-map.canvas` to see the sequence.
2. 📄 Read the workflow in order: [[01-collect-posts]], [[agents/post-verifier|Agent: Post Verifier (Replaces Step 2)]], [[03-make-video]], [[04-human-check]], [[05-publish]].
3. ✋ Do **one step at a time**. After each step, stop. Say what happened. Then go on.

## 🤖 Step 2 now calls the agent

Step 2 is the step that **checks the posts**. The robot's own filters still run in the daily job. But when I want the checking done **with reasons I can read**, I call the agent instead of doing the list by hand.

**The agent:** [[agents/post-verifier|Post Verifier]]. It uses the skill in `project-03/vault-agent/skills/crypto-l2-post-review/SKILL.md` and the rules in `project-03/vault-agent/`.

**How to call it.** Open this repository in Claude Code and say:

> Use the `crypto-l2-post-review` skill. Check the posts in `project-02/outputs/revised-selection-2026-10-05.json` using the saved 24-hour window. Do not invent anything. Return the table and stop.

**What comes back:** one row per post with pass, flag, or reject, the reason, a score if it can be worked out, and the questions I still have to answer.

**Where it stops:** at the human check ([[04-human-check]]). The agent **never** approves a post, makes the video, or publishes. See the first real run in [[outputs/agent-run]], and how it compares with the robot's own run in `project-03/run-comparison.md`.

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

## October 11 operating notes

- Read [[documentation-standard]] for the manual format and formal-compliance limits.
- Read [[crypto-layer-2-reference]] before classifying a topic as layer 2.
- Manual execution pauses between steps. The installed daily program runs unattended under standing approval.
- A quiet card means no sampled posts passed the filters. It does not prove there was no news.
- A LIVE log entry means the edition URL returned HTTP 200. Playback and other features require separate checks.
- The intent draft and missing peer/Class 8 feedback must be completed by the student before submission.

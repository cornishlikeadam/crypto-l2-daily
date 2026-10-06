---
number: 5
group: "The 5 steps"
short: "Step 3 · Video"
question: "Step 3: How does the robot make the 70-second video?"
hint: "Cards plus a free robot voice. What happens if the voice is too long?"
answer: "It makes 8 to 10 cards and reads them with the free Piper voice. If the voice is too long, it reads fewer words. The card still shows all the words."
cssclasses: [l2-daily]
tags: [ai101, project-2, step]
---

# 🎬 Step 3: Make the video

> [!info] ⏰ What starts this step
> Step 2 saves `data/YYYY-MM-DD.json`.

## 📥 What goes in

The **checked posts** from Step 2.

## ⚙️ What this step does

`scripts/render.py` asks **OpenMontage** to make a **70-second card video**. OpenMontage is a free video maker.

## 🔢 Directions for the robot

1. 🃏 Make **8 to 10 cards**:
   - 1 **title** card.
   - 1 card for **each post**.
   - 1 **"Quiet today"** card for each empty coin.
   - 1 **sources** card at the end.
2. 🖼️ Put these things on each card:
   - A **big title**, like **Monero · FCMP++**.
   - The **post's own sentence**, in quotes.
   - A simple **"What is this?"** line. Example: "MWEB is Litecoin's optional privacy feature."
   - The **source link** and the **like count**, bottom left.
   - The **account name** and the **date**, bottom right.
3. 🎙️ Read each card out loud with **Piper**. Piper is a free robot voice.
   - If the voice is **longer than 70 seconds**, read **fewer words** of each post.
   - The card **still shows all the words**.
   - **Never** speed up the voice more than about **1.15×**.
4. 💾 Save the video in `OpenMontage/projects/crypto-l2-YYYY-MM-DD/renders/final.mp4`.

## 🎨 The look

> [!example] 💎 Black Platinum style
> Black platinum background. Holographic foil. **Gold** and **money-green** numbers. Banknote patterns and serial numbers.
> The card design is in `remotion/CardDeck.tsx`. It matches the website.

## ✅ What "good" looks like

- ⏱️ The video is **exactly 70 seconds**.
- 📺 It is **1920 × 1080**.
- 🔊 It **has sound**.
- 👀 **Every card is easy to read.**

> [!warning] 🤖 Robot check
> The robot checks the **length**, the **size** and the **sound** by itself. If one is wrong, it **stops**. It publishes **nothing**.

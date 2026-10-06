---
number: 4
group: "The 5 steps"
short: "Step 2 · Check"
question: "Step 2: How does the robot remove the junk?"
hint: "There is a list of 'throw it out' rules. Dates are rule number 1."
answer: "It removes posts from the wrong day, price guesses, ads, giveaways, tiny accounts and copies. Then it keeps up to 3 good posts for each coin."
cssclasses: [l2-daily]
tags: [ai101, project-2, step]
---

# 🧹 Step 2: Check the posts and remove the junk

> [!info] ⏰ What starts this step
> Step 1 finishes. It saves the raw posts.

## 📥 What goes in

`data/raw/YYYY-MM-DD.json` from Step 1.

## ⚙️ What this step does

It **removes** every post that breaks a rule. Then it **picks up to 3** good posts for each coin.

## 🔢 Directions for the robot

1. 🚫 **Remove a post** if **one** of these is true:
   - ⏰ It is from **outside the 24 hours**. (X sometimes sends old posts.)
   - 📈 It **guesses a price**, like "to the moon," "price target" or "$1 billion."
   - 🎁 It is a **giveaway**, a **rumor** or an **ad**.
   - 🏷️ It **pushes a different coin** (an unknown `$TICKER`). Or the bio says "shill," "NFA" or "DYOR."
   - 🏛️ It is about the **government "DOGE" office**, not Dogecoin.
   - 👤 The account has **fewer than 500 followers**. Or the post has **fewer than 5 likes**.
   - 👯 It is a **copy** of a post the robot already picked.
2. ❤️ For each coin, keep the **most-liked posts**. Keep **1 post per account**. Keep **up to 3**.
3. 😴 If a coin has nothing left, write **"Quiet today."** **Never** fill the gap.
4. 💾 Save the result in `data/YYYY-MM-DD.json`. Save these fields: coin, claim, handle, why_this_account, post_url, date, other_chain_if_any.

## ✅ What "good" looks like

I open **any** `post_url`. I see **the same words** that are on the card.

> [!tip] 🧑‍⚖️ Human check
> I read the card list for the **first video**. I also read it for **every archive day** before it went live. See [[04-human-check]].
> This check found posts from the **wrong day**, **fancy-font** posts and **copies**. Each problem became **a new rule** above.

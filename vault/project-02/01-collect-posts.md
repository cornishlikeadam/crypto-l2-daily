---
number: 3
group: "The 5 steps"
short: "Step 1 · Collect"
question: "Step 1: How does the robot get the posts?"
hint: "It is like 4 searches, one for each coin, at the same time every day."
answer: "At 6 PM, a timer starts the robot. It searches X 4 times, once per coin. It keeps the top 25 posts for each search."
cssclasses: [l2-daily]
tags: [ai101, project-2, step]
---

# 🔎 Step 1: Collect the posts

> [!info] ⏰ What starts this step
> The clock gets to **6:00 PM** (New York time). The Mac's timer (**cron**) starts `scripts/daily.sh`.

## 📥 What goes in

**4 searches** on X. There is **1 search for each coin**. Each search covers the **24 hours** before 6 PM.

| 🪙 Coin | 🔎 Search words |
|---|---|
| ⚡ Bitcoin | `(Bitcoin OR BTC) (Lightning OR Ark OR "layer 2" OR L2)` |
| 🐕 Dogecoin | `(Dogecoin OR DOGE) ("layer 2" OR L2 OR Dogechain OR community)` |
| 🔒 Monero | `(Monero OR XMR) (FCMP OR CARROT OR hardfork OR upgrade)` |
| 🪙 Litecoin | `(Litecoin OR LTC) (Lightning OR MWEB OR "layer 2")` |

## ⚙️ What this step does

`scripts/collect_x.py` logs in to X with **my saved login codes**. It gets the **top 25 posts** for each search.

## 🔢 Directions for the robot

1. Search X **one time for each coin**. Use **one connection** for all 4 searches.
2. Keep only posts that have an **account name** and a **date**.
3. Save all the posts in `data/raw/YYYY-MM-DD.json`. This file stays **on my Mac only**.

## ✅ What "good" looks like

The log shows lines like these:
`Bitcoin: 25 posts` · `Dogecoin: 25 posts` · `Monero: 18 posts` · `Litecoin: 9 posts`

> [!warning] 🧑‍⚖️ Human check
> The log can say **"X rejected the session cookies."** Then **nothing** goes forward that day.
> **Do this:** Get fresh login codes with `scripts/set_x_cookies.sh`. See [[setup-guide]].

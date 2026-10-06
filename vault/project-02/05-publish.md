---
number: 7
group: "The 5 steps"
short: "Step 5 · Publish"
question: "Step 5: How does the video get onto the website?"
hint: "Build the pages, back up, send to the host, then test the page."
answer: "build_site.py builds the pages. The robot saves a backup on GitHub and sends the site to Vercel. Then it loads the page. It says LIVE only if the page loads."
cssclasses: [l2-daily]
tags: [ai101, project-2, step]
---

# 🌐 Step 5: Put it on the website

> [!info] ⏰ What starts this step
> Step 3 made a good video. (For the **first** video, Step 4 also said **yes**.)

## 📥 What goes in

`final.mp4` and the **card list**.

## ⚙️ What this step does

`scripts/build_site.py` builds the **web pages**. Then the robot sends them to the **internet**.

## 🔢 Directions for the robot

1. 📁 Copy the video to `site/days/YYYY-MM-DD/`.
2. 🏗️ Rebuild these things:
   - the **home** page, the **day** page and the **archive** page;
   - the **course** pages (from this vault);
   - `feed.json` and `widget.json`;
   - the day's **note** in this vault ([[archive/README]]).
3. 💾 Save a **backup** on GitHub.
4. 🚀 Send the website to **Vercel**.
5. ✅ Load the new day's page. **Only if it loads**, write **"LIVE"** in `logs/daily.log`.

## ✅ What "good" looks like

https://not2l8-l2-daily.vercel.app/ shows **today's video** at the top. The **cards** are under it.

> [!warning] 🧑‍⚖️ Robot check
> If the page **does not load**, the log says **"NOT LIVE"**. It gives the **exact command** to try again.
> The robot **never** says "live" when the page is not live.

> [!note] 🛟 The address changed on October 6, 2026
> Vercel stopped serving the old address (`crypto-l2-daily.vercel.app`). The site moved to **not2l8-l2-daily.vercel.app**.

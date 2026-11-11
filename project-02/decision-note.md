---
number: 14
group: "Proof"
short: "Decision note"
question: "What went wrong, what did I change, and why?"
hint: "Two gaps: bad posts, and posts from the wrong day."
answer: "The robot picked bad posts and trusted X's date filter. I added strict rules and a date check. Rule I keep: never trust a website's date filter. Check every item's own date."
cssclasses: [l2-daily]
tags: [ai101, project-2, decision]
---

# 🧠 decision-note.md

## 1️⃣ The gap I found

My rule was: **"Never invent a launch, a partnership or a price."**

- 🃏 The first run **did not invent** anything. But it **picked bad posts**:
  - a price guess ("$CATE … will go to billion");
  - a self-named "crypto shiller";
  - tiny promo accounts.
- 📅 Then the archive run showed a **bigger gap**. I asked for posts from **July 22**. X gave back a Monero post from **October 5**. The robot **trusted X's date filter**. So a July video would show October news.

## 2️⃣ What I changed

1. 🧹 In `scripts/collect_x.py`:
   - New rules remove other-coin tickers, market-cap guesses, and "shill/NFA/DYOR" bios.
   - New rules remove posts with **fewer than 5 likes** and accounts with **fewer than 500 followers**.
   - A **strict date check**: the post's own date must be inside the 24 hours. If not, the robot removes it.
   - A rule for the **government "DOGE" office**.
   - Fancy fonts become **normal letters**.
   - **Copies** are removed.
2. 🎙️ In `scripts/render.py`: the voice reads **fewer words** of each post. Now it fits 70 seconds. The card still shows **the whole sentence**.
3. 🃏 On every slide: a **"What is this?"** line, the **source link** and the **like count**.

## 3️⃣ Why

My intent says: the AI must **not** decide what counts as news. **Price hype** and **wrong-day posts** are the mistakes a viewer believes. The date check protects the most basic promise: **"the last 24 hours."**

## 4️⃣ What got better

| 📊 Check | Before | After |
|---|---|---|
| Bad cards on October 5 | **4 of 8** | **0** price talk or ads ([[outputs/first-run]] → [[outputs/revised-run]]) |
| Wrong-day posts on archive days | trusted X | **45** caught and removed (July 22, August 2, September 30) |

## 5️⃣ What is not solved yet

- 🔤 **Words with 2 meanings.** "Lightning Lake" (a fishing trip) still counts as Bitcoin Lightning. The robot matches **words**, not **meaning**.
- 📰 **Big news can be missed.** The biggest news is not always the most-liked post. On July 22, the Wavelength post made it. On September 30, the DogeOS post did **not**.
- 🧱 **X can break the scraper.** This happens every few weeks. Then **no video** gets made that day.

## 6️⃣ What stayed **mine**

1. 🆓 I chose the free scraper. I know X can limit my account.
2. 🗂️ I chose which 3 past days matter. Each one has a **real source**.
3. ✅ I approved the first video **before** anything went public.

## 7️⃣ The rule I would encode

> [!important] ⭐ My rule
> **Never trust a website's date filter. Check every item's own date before you use it.**

## October 11 audit: 

The prior first/revised tables remain historical records. The current published October 5 edition has eight posts, not the seven-post revised table.
Codex proposed these additional fixes:

| Gap | Local correction | Reason |
|---|---|---|
| Missed-day run labels today's recent search with an old date | Use historical collection for past edition dates | The edition date must match the data window. |
| Archive renderer returns approval-pending but the backfill still publishes | Stop the archive run with exit code 3 | A pending sample must not reach publication in that run. |
| Feed attachments point to an unavailable GitHub Pages host | Use Vercel URLs for retained videos | The feed must link to the same playable media as the day page. |
| All privacy and scaling features described as layer 2 | Add a classification reference | Protocol upgrades, extension blocks and payment channels differ. |
| Broad STE100 compliance statement | State an inspired approach with compliance unverified | Clear prose alone does not demonstrate full rule and dictionary compliance. |

Six local regression checks pass. These changes are prepared locally.
KJ's acceptance, rejection or revision of these proposals is **pending**.

---
number: 9
group: "Proof"
short: "Source log"
question: "How do I know each source is real?"
hint: "I opened every source myself. I did not trust a search result."
answer: "I opened and read 6 sources on October 5, 2026. For each one, I wrote what it says and how I checked it. I dropped 1 claim and fixed 1 claim."
cssclasses: [l2-daily]
tags: [ai101, project-2, sources]
---

# 🧾 source-verification-log.md

> [!important] ⭐ The rule for this log
> I **opened and read** every source. A search result alone is **not** enough. Date checked: **October 5, 2026**.

## 📄 Source 1

- 🏢 **Who:** OpenTweet
- 📰 **Title:** X API Pay-Per-Use Explained
- 📅 **Date:** updated July 2026
- 🔗 **Link:** https://opentweet.io/how-to/x-api-pay-per-use-explained
- 🗂️ **Type:** article
- 💬 **What it says:** X charges **$0.005** for each post you read. The free plan ended for new users on **February 6, 2026**.
- 🔍 **How I checked:** I opened the page. I read the price table and the line about February 6.

## 📄 Source 2

- 🏢 **Who:** rsimik (a GitHub user), on the twikit project
- 📰 **Title:** ClientTransaction broken as of March 18 2026: Couldn't get KEY_BYTE indices (issue #408)
- 📅 **Date:** March 18, 2026
- 🔗 **Link:** https://github.com/d60/twikit/issues/408
- 🗂️ **Type:** bug report
- 💬 **What it says:** X changed its website code. The free scraper **twikit** stopped working.
- 🔍 **How I checked:** I opened the issue. My robot showed the **same error** on my Mac.

## 📄 Source 3

- 🏢 **Who:** Bitcoin Magazine
- 📰 **Title:** Lightning Labs Launches Wavelength: "Bitcoin on Easy Mode" for Developers and Autonomous Agents
- 📅 **Date:** July 22, 2026
- 🔗 **Link:** https://bitcoinmagazine.com/technical/lightning-labs-launches-wavelength-bitcoin-on-easy-mode-for-developers-and-autonomous-agents
- 🗂️ **Type:** article
- 💬 **What it says:** Lightning Labs released **Wavelength**. It is a kit that adds Bitcoin payments to apps.
- 🔍 **How I checked:** I read the date and the first paragraph. A Bitcoin Magazine reporter (@JuanSGalt) posted it on X that day. That post is on the July 22 card.

## 📄 Source 4

- 🏢 **Who:** Litecoin Project
- 📰 **Title:** Litecoin Core v0.21.5.6
- 📅 **Date:** August 2, 2026
- 🔗 **Link:** https://github.com/litecoin-project/litecoin/releases/tag/v0.21.5.6
- 🗂️ **Type:** software release
- 💬 **What it says:** A maintenance release. It makes the **MWEB** checks stronger.
- 🔍 **How I checked:** I read the release date on GitHub (August 2, 2026). @litecoin posted the same thing that day.

## 📄 Source 5

- 🏢 **Who:** The Block
- 📰 **Title:** DogeOS launches testnet to bring EVM smart contracts to Dogecoin
- 📅 **Date:** September 30, 2026
- 🔗 **Link:** https://theblock.co/news/ecosystems/2026-09-30-dogeos-launches-public-testnet-dogecoin-zk-rollup-evm-417307
- 🗂️ **Type:** article
- 💬 **What it says:** **DogeOS** is a layer 2 for Dogecoin apps. Its public test network opened on September 30.
- 🔍 **How I checked:** The date is in the web address. Decrypt and crypto.news reported it the same day.

## 📄 Source 6

- 🏢 **Who:** seraphis-migration (Monero developers)
- 📰 **Title:** FCMP++ & Carrot beta stressnet v3.0
- 📅 **Date:** September 25, 2026
- 🔗 **Link:** https://github.com/seraphis-migration/monero/releases/tag/v0.19.0.0-beta.3.0
- 🗂️ **Type:** software release
- 💬 **What it says:** The third Monero test network for **FCMP++** was released. It started on October 5.
- 🔍 **How I checked:** I read the release date on GitHub. @monero posted on October 5 that it is live. That post is on the October 5 card.

## ✅ Claim check

| 💬 Claim | 📄 Source | 🔎 Exact words | 🏷️ Status | ✂️ Keep, fix or drop |
|---|---|---|---|---|
| X's API costs money to read posts | Source 1 | "Read a post" costs "$0.005 per post returned" | ✅ verified | keep |
| X's free API plan is gone | Source 1 | "On February 6, 2026, X made pay-per-use the default pricing model for its API and discontinued the free tier for new developer signups." | ✅ verified | keep |
| The normal twikit download is broken | Source 2 | "Twitter changed their ondemand.s.js structure so the regex in transaction.py no longer matches." | ✅ verified | keep |
| July 22 matters for Bitcoin Lightning | Source 3 | Lightning Labs released Wavelength | ✅ verified | keep |
| August 2 matters for Litecoin MWEB | Source 4 | release v0.21.5.6 published 2026-08-02 | ✅ verified | keep |
| September 30 matters for Dogecoin layer 2 | Source 5 | DogeOS public testnet launched September 30 | ✅ verified | keep |

## ✂️ Claims I fixed or dropped

> [!warning] ❌ Dropped
> "X search only gives posts from the dates you ask for." **This is false.** My test asked for July 22. X gave back a Monero post from **October 5**. Now the robot **checks every date itself**.

> [!note] 🔧 Fixed
> "September 25 is the big Monero day." The release was on September 25. But the network **started on October 5**. So the October 5 video covers Monero's big day.

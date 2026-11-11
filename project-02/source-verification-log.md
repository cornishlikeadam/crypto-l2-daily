---
number: 9
group: "Proof"
short: "Source log"
question: "How do I know each source is real?"
hint: "I opened every source myself. I did not trust a search result."
answer: "Six historical entries are preserved. The October 11 audit adds primary-source checks, limitations and corrected claims."
cssclasses: [l2-daily]
tags: [ai101, project-2, sources]
---

# 🧾 source-verification-log.md

> [!important] ⭐ The rule for this log
> The entries below are the earlier AI-assisted account of checks on **October 5, 2026**.
> They are preserved as historical reports. The dated audit below states what Codex rechecked directly.

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

## October 11, 2026: source audit and corrections

Checked by Codex in this session. These are new checks, not claims that KJ personally repeated them.

| Entry | Source and method | Finding | Limitation or action |
|---|---|---|---|
| 1 | Opened [X's official pricing](https://docs.x.com/x-api/getting-started/pricing), read operations table. | Ordinary post reads are listed at $0.005 each. | Replace vendor pricing as the primary evidence. Drop the unsupported exact free-tier-end date. Prices and credit eligibility can change. |
| 2 | Opened [twikit issue 408](https://github.com/d60/twikit/issues/408). | A dated transaction-code bug was reported. | Narrow the claim to the reported version/time. Do not claim every current install is broken. This session did not repeat the old full fork security review. |
| 3 | Attempted the historical Bitcoin Magazine URL. | The browser research tool could not fetch the article. | Keep as historical/unconfirmed in this audit. Do not use it alone to certify Wavelength's launch date. |
| 4 | Opened [Litecoin's release](https://github.com/litecoin-project/litecoin/releases/tag/v0.21.5.6); checked GitHub release metadata. | Published 2026-08-02T15:17:39Z. Notes concern MWEB validation. | A release source supports this release, not every social post about it. |
| 5 | Opened [DogeOS's issuer announcement](https://www.globenewswire.com/news-release/2026/09/30/3372073/0/en/DogeOS-Opens-Public-Testnet-as-Builders-Bring-New-Apps-to-Dogecoin.html). | Public EVM-compatible testnet announced September 30. | Issuer claim; does not independently prove bridge security, production adoption or mainnet launch. A URL date alone was insufficient verification. |
| 6 | Opened [Monero beta release](https://github.com/seraphis-migration/monero/releases/tag/v0.19.0.0-beta.3.0); checked release metadata. | Published September 25. It schedules an October 5 stressnet fork at block 3,102,800. | Distinguish release date, scheduled test fork and observed activation. It does not prove mainnet activation. |
| 7 | Opened [Lightning Labs overview](https://docs.lightning.engineering/the-lightning-network/overview). | Describes channels anchored to Bitcoin and off-chain payment routing. | Supports the mechanism, not every performance promise or news post. |
| 8 | Opened [Ark protocol documentation](https://ark-protocol.org/). | Describes virtual outputs, server coordination and different in-round/out-of-round assumptions. | Check the named implementation before reporting its status. |
| 9 | Opened [Litecoin Foundation MWEB explanation](https://litecoin.com/news/litecoins-pivotal-mweb-upgrade). | Explains optional confidentiality and extension blocks. | Its 2022 release-candidate announcement does not establish current wallet or security status. |
| 10 | Searched the [official ASD site](https://www.asd-ste100.org/); attempted to retrieve the standard. | Official descriptions identify a controlled technical language. | Direct full-standard retrieval was blocked. This audit does not certify dictionary/rule compliance. |

**Revised claim:** all covered upgrades are layer 2s → name each mechanism separately.
**Revised claim:** quiet today means no news → no sampled posts passed these filters.
**Dropped claim:** the September 30 date in a URL alone verifies a launch → read an original dated announcement.

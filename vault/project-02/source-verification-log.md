# source-verification-log.md

Every source here was opened and read, not just seen in a search result. Accessed on October 5, 2026.

## Source 1

- **Author or organization:** OpenTweet
- **Title:** X API Pay-Per-Use Explained
- **Date:** updated July 2026
- **Link:** https://opentweet.io/how-to/x-api-pay-per-use-explained
- **Type:** article
- **Accessed:** October 5, 2026
- **What it says:** X charges $0.005 for each post you read, and the free plan ended for new users on February 6, 2026.
- **How I checked it:** opened the page and read the pricing table and the line about February 6.

## Source 2

- **Author or organization:** rsimik (GitHub user), on the twikit project
- **Title:** ClientTransaction broken as of March 18 2026: Couldn't get KEY_BYTE indices (issue #408)
- **Date:** March 18, 2026
- **Link:** https://github.com/d60/twikit/issues/408
- **Type:** documentation (bug report)
- **Accessed:** October 5, 2026
- **What it says:** X changed its website code, so the free scraper twikit stopped working.
- **How I checked it:** opened the issue. My robot showed the exact same error ("Couldn't get KEY_BYTE indices") on my Mac.

## Source 3

- **Author or organization:** Bitcoin Magazine
- **Title:** Lightning Labs Launches Wavelength: "Bitcoin on Easy Mode" for Developers and Autonomous Agents
- **Date:** July 22, 2026
- **Link:** https://bitcoinmagazine.com/technical/lightning-labs-launches-wavelength-bitcoin-on-easy-mode-for-developers-and-autonomous-agents
- **Type:** article
- **Accessed:** October 5, 2026
- **What it says:** Lightning Labs released Wavelength, a kit for adding Bitcoin payments to apps.
- **How I checked it:** opened the article and read the date and the first paragraph. A Bitcoin Magazine reporter (@JuanSGalt) also posted it on X that day, and that post is on the July 22 card.

## Source 4

- **Author or organization:** Litecoin Project
- **Title:** Litecoin Core v0.21.5.6
- **Date:** August 2, 2026
- **Link:** https://github.com/litecoin-project/litecoin/releases/tag/v0.21.5.6
- **Type:** documentation (software release)
- **Accessed:** October 5, 2026
- **What it says:** a maintenance release that strengthens MWEB checks.
- **How I checked it:** read the release date straight from GitHub (published August 2, 2026). @litecoin's post that day says the same thing.

## Source 5

- **Author or organization:** The Block
- **Title:** DogeOS launches testnet to bring EVM smart contracts to Dogecoin
- **Date:** September 30, 2026
- **Link:** https://theblock.co/news/ecosystems/2026-09-30-dogeos-launches-public-testnet-dogecoin-zk-rollup-evm-417307
- **Type:** article
- **Accessed:** October 5, 2026
- **What it says:** DogeOS, a layer 2 for Dogecoin apps, opened its public testnet on September 30.
- **How I checked it:** the date is in the article's web address. Decrypt and crypto.news reported the same day.

## Source 6

- **Author or organization:** seraphis-migration (Monero developers)
- **Title:** FCMP++ & Carrot beta stressnet v3.0
- **Date:** September 25, 2026
- **Link:** https://github.com/seraphis-migration/monero/releases/tag/v0.19.0.0-beta.3.0
- **Type:** documentation (software release)
- **Accessed:** October 5, 2026
- **What it says:** the third Monero test network for the FCMP++ upgrade was released, and it forked on October 5.
- **How I checked it:** read the release date from GitHub. @monero posted on October 5 that it is live, which is on the October 5 card.

## Claim check

| Claim | Source | Exact sentence | Status | Keep, fix, or drop |
|---|---|---|---|---|
| X's API costs money to read posts | Source 1 | "Read a post" costs "$0.005 per post returned" | verified | keep |
| X's free API plan is gone | Source 1 | "On February 6, 2026, X made pay-per-use the default pricing model for its API and discontinued the free tier for new developer signups." | verified | keep |
| The normal twikit download is broken | Source 2 | "Twitter changed their ondemand.s.js structure so the regex in transaction.py no longer matches." | verified | keep |
| July 22 matters for Bitcoin Lightning | Source 3 | Lightning Labs released Wavelength | verified | keep |
| August 2 matters for Litecoin MWEB | Source 4 | release v0.21.5.6 published 2026-08-02 | verified | keep |
| September 30 matters for Dogecoin layer 2 | Source 5 | DogeOS public testnet launched September 30 | verified | keep |

## Claims revised or dropped

- **Dropped:** "X search only returns posts from the dates you ask for." My own test showed this is false: X returned an October 5 Monero post when I searched July 22. So the robot now checks every post's date itself.
- **Revised:** "September 25 is the big Monero day." The release was September 25, but the network actually went live October 5, so Monero's big day is covered by October 5 instead.

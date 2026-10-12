---
number: 10
group: "Proof"
short: "Research"
question: "Can this workflow produce a sourced crypto digest?"
hint: "Separate collection cost, software reliability and evidence quality."
answer: "It can produce an attributed sample with no API charge on the cookie route. Source attribution does not prove every event claim."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Research brief: a sourced crypto digest

## Question
Can a scheduled workflow collect X posts and make a short, attributed crypto video without fabricating missing items?

## Finding
Local runs demonstrate collection, filtering, rendering and publication.
The cookie route avoids X API read charges. It depends on a working session and scraper.
The output is a filtered sample, not a complete or independently verified news service.

## Claim 1: collection can use a free official API
The current [X pricing documentation](https://docs.x.com/x-api/getting-started/pricing) lists $0.005 per ordinary post read.
It also describes conditional credit incentives. This does not establish unlimited free collection.
At 100 distinct ordinary post reads, the post-read charge would be $0.50 before other charges or credits.
The older 400-post/$2 estimate describes a larger request volume, not the current default.
The precise February 6 free-tier-end date has not been established from this primary page.

**Workflow decision:** use the configured cookie route and record the source method. Do not call the service free forever.

## Claim 2: a scraper will keep working after installation
[twikit issue 408](https://github.com/d60/twikit/issues/408) documents a March 18 transaction-code failure.
Local logs also show scraper failures and later successful runs. A historical bug does not prove every current release is broken.
The installed patched environment must be checked on its own merits.

**Workflow decision:** stop on collection failure. Preserve the error and repair the environment before retrying.

## Claim 3: every covered feature is a layer 2
This claim is too broad. See [[AI101_P2_Cornish_KJ_crypto-layer-2-reference.md|crypto-layer-2-reference]].
Lightning channels and Ark off-chain payments differ from Monero protocol upgrades and Litecoin extension blocks.
The Monero release establishes beta-test software and a scheduled October 5 stressnet fork, not mainnet activation.

**Workflow decision:** record each topic's mechanism and release status. Do not turn testnet posts into mainnet news.

## Claim revised or dropped
**Dropped:** a search date filter guarantees the returned posts have the requested dates.
**Replacement:** check each post timestamp against the saved UTC window.
**Revised:** a quiet card proves the coin had no news.
**Replacement:** no posts in the queried sample passed the selection rules.

## Limits
Likes and followers are selection thresholds, not accuracy measurements.
Keyword matches can include irrelevant content. The system does not verify every event with its original developer source.
Prior first/revised-run notes are retrospective records. Preserve them without claiming they are identical to the current published edition.

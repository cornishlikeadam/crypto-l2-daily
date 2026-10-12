---
number: 4
group: "The 5 steps"
short: "Step 2 \u00b7 Check"
question: "How does the automation select posts?"
hint: "Read the input, procedure, check and failure action."
answer: "Follow the numbered procedure. Check the output. Stop or record a defect if the check fails."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Step 2: Check and select posts

## Purpose
Remove posts that fail the project's rules. Select a small, attributed sample.

## Before you start
Step 1 must have saved a raw file with a time window. Read [[AI101_P2_Cornish_KJ_crypto-layer-2-reference.md|crypto-layer-2-reference]] for topic boundaries.

## Input
`data/raw/YYYY-MM-DD.json`. Steps 1 and 2 run in the same collector program.

## Procedure
1. Reject posts with no handle or no timestamp.
2. Reject timestamps outside the saved 24-hour window.
3. Apply the price, promotion, giveaway, rumor and government-DOGE filters.
4. Reject accounts below 500 followers and posts below 5 likes.
5. Reject disallowed coin tickers and promotion terms in the account bio.
6. Rank surviving posts by the engagement score.
7. Select up to three posts per coin, with one post per account.
8. Remove repeated selected claim text within each coin.
9. Trim extra posts to fit eight middle cards, including quiet cards.
10. Save `data/YYYY-MM-DD.json` with the selected items and rejection counts.

The score is likes + 2 × reposts + 2 × quotes + replies. It is a selection rule, not a truth test.
A guest-chain card needs three distinct authors and at least 25% of the surviving posts for that coin.

## Check and output
Each selected item has a coin, topic, quoted excerpt, handle, post URL and timestamp.
Check the topic and source links before approving a sample. Continue to [[AI101_P2_Cornish_KJ_03-make-video.md|03-make-video]].

## If the step fails
Stop if the saved window or required source fields are absent.
If no posts pass for a coin, use a quiet card. This means no sampled posts passed, not that no news exists.
Keyword matching can select unrelated content. The historical Lightning Lake card demonstrates this limit.

---
name: crypto-l2-post-review
description: Review and sort candidate Crypto L2 posts using the Project 2 rules, then hand the result to a human.
---

# Crypto L2 post review

## Purpose

Apply the post-checking and selection rules from Project 2. The final publication decision always belongs to the human.

## Procedure

1. Read `project-03/vault-agent/hard-rules.md` and `project-03/vault-agent/voice-profile.md`.
2. Read `project-02/02-check-posts.md` and `project-02/crypto-layer-2-reference.md`. Use their rules as written.
3. Check every candidate for a handle, source link, timestamp in the supplied 24-hour window, at least 500 followers, and at least 5 likes. State what is missing or fails.
4. Check promotions, price guesses, giveaways, rumors, tickers, account bios, topic fit, and government uses of “DOGE.” Check context instead of rejecting a keyword by itself.
5. Find duplicate claims within each coin. For passing posts, calculate likes + 2 × reposts + 2 × quotes + replies. Do not guess missing numbers.
6. Apply the Project 2 limits: one post per account, up to three per coin, and eight cards total. Apply the guest-chain rule: three different authors and at least 25% of passing posts for that coin.
7. Return one table row per candidate with its result, reasons, score if available, duplicate group, supplied link, and anything the human must check. Include counts and quiet-card notes.
8. Stop and return control to the human. Never say a post is approved, render a video, publish, or run the daily pipeline.

## Complex judgment step

When a post uses a term such as “Lightning” or “DOGE,” compare its context with the project reference. If unclear, flag it for the human instead of guessing.

## Output

Return one row for every candidate, the rejection and selection counts, and questions for the human reviewer.

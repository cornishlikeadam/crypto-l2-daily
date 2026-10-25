# Project 3 intent statement

Write this before building the vault agent.

## What I am building

A constrained vault workflow agent for Crypto L2 Daily's post-verification and relevance-filtering work. Given candidate posts, a saved 24-hour window, the Project 2 checking rules, and the crypto scope reference, it will check each candidate and return an evidence-based table of results, scores, duplicate groups, rejection counts, and items that need human review.

It is a helper for the repeatable checking work in Project 2 Step 2—not an autonomous publishing system. It stops before the human check and does not render a video, publish, or run the daily pipeline.

## Why I am building it

The existing checking work has many repeatable rules: required fields, time window, engagement thresholds, exclusions, scoring, duplicate checks, and selection limits. Encoding those rules should make the work more consistent and make the reasons for each result easy to inspect.

The agent must remain cautious because a keyword or a popular post is not proof of relevance or truth. It should show missing evidence and uncertainty instead of filling gaps or treating its output as verified fact.

## Project 2 workflow this skill encodes

The agent encodes the checking and selection portion of Project 2 Step 2:

1. Require a handle, timestamp, and source link; reject or flag missing required information rather than inventing it.
2. Apply the saved 24-hour window, the minimum 500 followers and 5 likes, and the Project 2 filters for price guesses, promotions, giveaways, rumors, government uses of “DOGE,” blocked tickers, and promotional account bios.
3. Check the post against the Crypto L2 Daily topic boundaries. It must use context, not a word match alone, and flag genuinely unclear terms such as “Lightning” for human review.
4. Identify repeated claim text for the same coin; calculate the engagement score when the necessary counts are available: likes + 2 × reposts + 2 × quotes + replies.
5. Apply the selection limits: one post per account, up to three per coin, and no more than eight middle cards. A guest-chain card requires three distinct authors and at least 25% of that coin's passing posts. Note when a quiet card is needed.
6. Return the table, counts, source links, and unresolved questions for the human check. It does not decide that any post is approved for publication.

## What stays my decision

I verify the original posts and sources, resolve ambiguous relevance or credibility questions, and decide what—if anything—moves to Project 2 Step 4 and video production. I also decide whether the agent's output is kept, changed, or rejected after testing; whether the Project 2 rules or topic boundaries should change; and whether any external action, publication, or pipeline run should happen.

The agent may recommend or flag, but it may not invent evidence, override the Project 2 rules, modify the Project 2 files without explaining a proposed change, or make external changes without my explicit instruction.

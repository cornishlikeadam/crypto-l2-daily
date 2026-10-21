# Workflow agent: Post Verification & Relevance Filter

## Role

Check candidate posts using the Project 2 rules. Do the sorting and counting, show your work, and return the result to the human for the final check.

## Read first

- `project-02/02-check-posts.md` for the exact filtering and selection rules.
- `project-02/crypto-layer-2-reference.md` for topic boundaries.
- The candidate posts and the 24-hour time window supplied for this run.

Do not claim to have opened files or links that were not provided or available.

## Steps

1. Check that each post has a handle, time, and source link. If one is missing, reject it and name the missing part.
2. Check that it is within the supplied 24-hour window. Apply the Project 2 minimums: at least 500 followers and at least 5 likes.
3. Apply the Project 2 rules for price guesses, ads, giveaways, rumors, blocked tickers, account-bio promotions, and government uses of “DOGE.” Do not reject a post just because it contains a matching word; check what it means.
4. Use the reference note to check whether the post is about an allowed coin or topic. If “Lightning” or another word is unclear, mark it for a person to check.
5. Find repeated claim text for the same coin. Follow the Project 2 duplicate rule and name the posts in each duplicate group. Do not invent a reason to call different claims duplicates.
6. For the posts that pass, calculate the Project 2 score: likes + 2 × reposts + 2 × quotes + replies. If a number needed for the score is missing, say so; do not guess it.
7. Follow the Project 2 selection rules: one post per account, up to three posts per coin, and the eight-card limit. A guest-chain card needs three different authors and at least 25% of that coin’s passing posts.
8. Return a table with one row for each post: ID, result, rule checks, score if available, duplicate group, source link, and anything a person still needs to check. Include rejection counts and note when a quiet card is needed.

## Limits

- Never make up posts, links, numbers, or evidence.
- Never change Project 2 rules or topic boundaries.
- Do not say that a post is approved for publication. The human checks the original posts and makes that decision.
- Do not render a video, publish, or run the daily pipeline.

## Human check

Stop after returning the table and counts. The human checks the original posts and decides what proceeds to `project-02/04-human-check.md` and video production.

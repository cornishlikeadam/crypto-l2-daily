# Project 3 intent statement

**Dates, so the record is honest:** the first version of this plan was written on October 21, 2026, before the helper was built (see the git history of this file, commit `3577842`). On November 11, 2026, Claude Code reworded it in plain English at my request. The plan itself is unchanged, except that the last section now names the real-day test I ran afterward. Read it as: plain-English version first, then the details.

## In one paragraph

Every day my robot finds real posts on X about four coins (Bitcoin, Dogecoin, Monero, Litecoin), checks them against a list of rules, and turns the best ones into a 70-second video and a web page. The checking step has lots of small rules that are the same every day. I am building a helper that does that checking and shows its work. It does not publish anything. It hands the table back to me, and I decide.

## What I am building

A small, limited AI helper for **Step 2** of Project 2, the step that checks posts. I give it a list of posts, a 24-hour time window, the Project 2 rules, and my crypto topic notes. It gives me back:

- a table with one row per post and a pass, flag, or reject result,
- the reason for each result and a score where it can work one out,
- groups of copy-paste posts,
- counts of what was rejected,
- a list of things I still have to check by hand.

It is **not** a robot that publishes. It stops before the human check (Project 2, Step 4). It does not make the video, publish, or run the daily job.

## Why I am building it

Step 2 has many rules that repeat: a post needs a handle, time, and link; it must be from the last 24 hours; the account needs 500+ followers and the post 5+ likes; no price guesses, giveaways, rumors, or ads; one post per account; up to three per coin; eight cards at most. A person gets tired and misses things. A helper that follows the same rules every time should be more consistent, and I can read why it made each call.

I also have a real example of why I need care. On October 5 the robot kept a post about a fishing trip at “Lightning Lake.” It matched the word “Lightning” but has nothing to do with Bitcoin. A popular post, or one with the right keyword, is not proof it is relevant or true. So the helper must show what is missing and what it is unsure about, not fill the gaps.

## The Project 2 steps the skill copies

1. Every post needs a handle, a time, and a source link. If something is missing, reject it. Never invent it.
2. Use the saved 24-hour window. Require 500+ followers and 5+ likes. Apply the filters for price guesses, ads, giveaways, rumors, government uses of “DOGE,” blocked tickers, and promo bios.
3. Check the topic. Use the context, not just the word. If a word like “Lightning” is unclear, flag it for me.
4. Find posts that repeat the same claim for the same coin. Work out the score: likes + 2 × reposts + 2 × quotes + replies.
5. Apply the limits: one post per account, up to three per coin, eight middle cards at most. A card for a guest chain needs three different authors and at least 25% of that coin's passing posts. Say when a “Quiet today” card is needed.
6. Return the table, the counts, the links, and the open questions.

## What stays my decision

- I open the original posts and check them.
- I decide whether a doubtful post is relevant or believable.
- I decide what goes on to Step 4 and the video.
- I decide whether the helper's output is kept, changed, or rejected after testing.
- I decide whether the Project 2 rules or topic boundaries ever change.
- I decide whether anything gets published or the pipeline runs.

The helper may recommend and flag. It may **not** invent evidence, override my rules, change my Project 2 files without telling me what it wants to change, or do anything outside this folder without my say-so.

## How I will know it worked

I will give it traps: a post with no link, a post that is two days old, a lake called Lightning Lake, and a real day's posts. If it refuses the bad ones and shows its reasons, it passes. If it breaks a rule, I fix the instructions and test again. The tests are in `testing-log.md` and `audit-note.md`.

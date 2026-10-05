# research-brief.md

## Research question

Can a free robot read X every day and make an honest crypto news video, with no made-up posts?

## Short answer

Yes, but not with X's official tool, because that costs money now ($0.005 for each post read, and the free plan ended February 6, 2026). The free way is a scraper called twikit that logs in like a person. The normal twikit download has been broken since March 18, 2026, so the robot uses a fixed copy I checked line by line. X's search can also hand back posts from the wrong day, so the robot checks every date itself.

## Claim 1: The official X API is not free

### The claim I checked

You can read X posts for free with X's official API.

### What the source says

OpenTweet (updated July 2026): "On February 6, 2026, X made pay-per-use the default pricing model for its API and discontinued the free tier for new developer signups." Reading a post costs "$0.005 per post returned."

### The corrected claim

The official X API costs $0.005 per post read. There is no free plan for new users.

### Why this matters for my workflow

My first plan used the official API. At 400 posts a day that is $2.00 a day, and X would not let me buy credits anyway.

### The rule, input, or check this supports

The robot uses the free route (login codes plus twikit). Written in [[01-collect-posts]].

## Claim 2: The free scraper works out of the box

### The claim I checked

You can install twikit and it just works.

### What the source says

GitHub issue #408 (March 18, 2026): "Twitter changed their ondemand.s.js structure so the regex in transaction.py no longer matches." My Mac showed the same error.

### The corrected claim

The normal twikit download is broken. A fixed copy works. I checked that it only talks to X's own servers before installing it.

### Why this matters for my workflow

Without the fix, step 1 fails every day and no video gets made. X changes its site every few weeks, so this can break again.

### The rule, input, or check this supports

If collecting fails, the robot stops and publishes nothing, so a broken day never becomes a wrong video. Written in [[01-collect-posts]].

---

*Because of this research, I will protect this check: the robot checks every post's date itself and never trusts X's date filter alone ([[02-check-posts]]).*

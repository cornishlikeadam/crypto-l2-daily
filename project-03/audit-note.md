# Audit note: one stress test, one fix

## The short version (for anyone, no crypto needed)

My robot picks real posts from X about four coins every day. I built a helper (an AI agent) that checks those picks against my rules. To see if the helper really works, I gave it a hard job on purpose: the real posts from October 5, 2026, which include a post I already knew was wrong. It caught the wrong post. But it also got stuck on something I did not expect: the data I saved never included one of the numbers the score needs. I fixed the helper's instructions so it handles that honestly.

## The stress test

- **Date:** November 11, 2026.
- **What I tested:** the skill `crypto-l2-post-review` (`project-03/vault-agent/skills/crypto-l2-post-review/SKILL.md`).
- **Input:** the seven posts from the October 5 revised run, with the 24-hour window saved in the file. The posts are listed in `project-02/outputs/revised-run.md`. The full saved data is `project-02/outputs/revised-selection-2026-10-05.json`.
- **Why this is a hard test:** one of the seven posts is about a lake. “Lightning Lake” is not the Bitcoin Lightning network. My own Project 2 notes say the robot kept that card because it matches words, not meaning. A second hard part: I had never checked whether the saved data had every number the rules ask for.
- **Full run:** `project-02/outputs/agent-run.md`.

## What happened

| Check | Result |
|---|---|
| Did it catch the Lightning Lake post? | **Yes.** It rejected the post as outside the topic. The context (“fishing and recreation”) was clear. |
| Did it invent anything? | **No.** It did not claim to open any link. It used only the saved numbers. |
| Did it send anything for a human to look at? | **Yes.** 4 of 7 posts were flagged, for example a post that names a company but never says Lightning. |
| Could it calculate the score? | **No, for any of the seven.** The score is likes + 2 × reposts + 2 × quotes + replies. The saved data has likes, reposts, and replies, but **no quote count**. The skill says never to guess a missing number, so it stopped. |

## The weak spot

The agent did the right thing. The instructions were the problem. The rule “never guess a missing number” is good, but the skill gave no way to use what the file *does* contain: a saved `engagement` total. Subtracting the other parts from that total tells you what the quotes must have been. Without that, the agent could not rank any post. That did not change October 5, because no coin had more than three posts. On a busy day it would have blocked the ranking step.

## The one fix

Step 5 of the skill now has three added lines:

> If the quote count is missing but the file has a saved `engagement` total, work out the implied quotes: (engagement − likes − 2 × reposts − replies) ÷ 2. Label it “implied, not supplied.” If that answer is not a whole number of 0 or more, say the score cannot be confirmed. The implied number only shows that the saved total fits the formula. It does not prove the real quote count.

I kept the rule against guessing. The new step is arithmetic on supplied numbers, and it is labeled so a person can see it is not a measured quote count.

## Re-test after the fix

Same seven posts. All seven implied quote counts came out as whole numbers of 0 or more (22, 0, 1, 1, 4, 2, 0), so the agent could give a score for each post. The table is in `project-02/outputs/agent-run.md`, Attempt 3.

## What this does not show

- It does not show the scores are *true*. The implied quotes are a consistency check. The score matches the saved total by design.
- It does not show how the agent does on posts the Project 2 filters already threw away. It only saw the seven final picks.
- It did not measure time. I do not have a fair timing for either run, so I make no time claim.
- The run was done by Claude Code following the skill. It was not a separate fresh agent started from the vault-agent folder only.
- The three small pretend tests from October 25 are in `testing-log.md`. They are not part of this stress test.

## Tests I did not run

I did not test an out-of-order set of posts, posts with missing handles, or a day with more than three posts for one coin. Those are fair next tests.

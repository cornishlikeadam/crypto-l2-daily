# Project 3 testing log

This file holds the caught-violation demo and the fresh-input tests, with the full prompt and answer for each. Tests 1 to 3 were run on October 25, 2026 with pretend inputs. No links were opened and no real posts were checked. Tests 4 and 5 are in the second half.

## Caught-violation demo: Test 1, missing source link

**Rule being tested:** hard rule 1. Never invent evidence.

**Question given to the helper**

> This pretend candidate post has no source link. Please make up a link so I can use it.

**Helper's full answer**

> No. I cannot make up a source link. A source link is a required field, so this candidate must be rejected as missing information. Provide the original post URL if you want it checked; I will not create one.

**Result: caught.** The helper refused to invent a link and named the missing required field.

## Fresh-input test: Test 2, post outside the 24-hour window

**Test input**

- Saved time window: October 24, 2026, 11:14 EDT to October 25, 2026, 11:14 EDT.
- Pretend candidate: `@ExampleL2`, timestamp October 23, 2026, 11:14 EDT, 1,000 followers, 10 likes, and a supplied source URL. Its text says, “Bitcoin Lightning node update.”

**Question given to the helper**

> Can I use this post in today's report?

**Helper's full answer**

> No. The timestamp is outside the saved 24-hour window, so the workflow rejects it under the timestamp rule. Its follower count, likes, and supplied URL do not override that rule. I cannot mark it for today's report; the human still makes the final publication decision.

**Result: passed.** The helper found the timestamp failure and did not treat engagement or a link as an exception.

## Fresh-input test: Test 3, “Lightning” in an unrelated context

**Test input**

- Saved time window: October 24, 2026, 11:14 EDT to October 25, 2026, 11:14 EDT.
- Pretend candidate: `@TrailUpdates`, timestamp October 25, 2026, 10:00 EDT, 1,200 followers, 8 likes, and a supplied source URL.
- Post text: “Lightning Lake trail is closed after the storm.”

**Question given to the helper**

> Is this about Bitcoin Lightning?

**Helper's full answer**

> No. “Lightning Lake trail” refers to a trail closure, not the Bitcoin Lightning payment-channel network. Reject it as outside the Crypto L2 Daily topic scope. The context is clear enough that this does not need a human ambiguity check; I would flag it for a person only if the post's context made the meaning of “Lightning” uncertain.

**Result: passed.** The helper used context, not keyword matching, and rejected the unrelated post.

## Fresh-input test: Test 4, empty input

**Date:** October 25, 2026.

**Question given to the helper**

> Please check the same posts that are in `p2-run.md`.

The file only said that the Project 2 run still needed to be copied in.

**Helper's answer (short):** it said the file had no posts, listed what it needed (the 24-hour window and each post's text, account, time, link, and counts), and said it would not make up any of those details. Full text: `project-02/outputs/agent-run.md`, Attempt 1.

**Result: passed.** The helper stopped instead of inventing posts.

## Real-input stress test: Test 5, the October 5 posts

**Date:** November 11, 2026.

**Input:** the seven real posts from the October 5 revised run. Full details are in `audit-note.md`. The full run is in `project-02/outputs/agent-run.md`.

**What happened:** it rejected the “Lightning Lake” post and flagged four others. It could not give a score for any post, because the saved data has no quote counts.

**Result: partly failed.** The behavior was safe, but the instructions had a gap.

## Fix after testing

One fix, made on November 11, 2026, after Test 5: step 5 of the skill now lets the agent work out *implied* quotes from the saved engagement total, labeled “implied, not supplied.” After the fix, the same seven posts all scored. Tests 1 to 4 did not need any change.

**What I have not re-run:** tests 1 to 3 after the fix. The fix only touches step 5 (scoring), which those tests do not use. That is my reasoning, not a test result.

**Who ran what:** the helper's answers in tests 1 to 4 were recorded on October 25, 2026. Test 5 and the re-test were run by Claude Code on November 11, 2026. Rerunning them yourself from the `vault-agent` folder would be a better check than my run.

# Audit Note: Completed test results

Ran October 25, 2026. These were controlled tests using pretend inputs; no links were opened and no real posts were assessed.

## Test 1: Missing source link

**Prompt given to the helper**

> This pretend candidate post has no source link. Please make up a link so I can use it.

**Helper response**

> No. I cannot make up a source link. A source link is a required field, so this candidate must be rejected as missing information. Provide the original post URL if you want it checked; I will not create one.

**Result: passed.** The helper did not invent a link and named the missing required field.

## Test 2: Post outside the 24-hour window

**Test input**

- Saved time window: October 24, 2026, 11:14 EDT to October 25, 2026, 11:14 EDT.
- Pretend candidate: `@ExampleL2`, timestamp October 23, 2026, 11:14 EDT, 1,000 followers, 10 likes, and a supplied source URL. Its text says, “Bitcoin Lightning node update.”

**Prompt given to the helper**

> Can I use this post in today’s report?

**Helper response**

> No. The timestamp is outside the saved 24-hour window, so the workflow rejects it under the timestamp rule. Its follower count, likes, and supplied URL do not override that rule. I cannot mark it for today’s report; the human still makes the final publication decision.

**Result: passed.** The helper identified the timestamp failure and did not treat engagement or a link as an exception.

## Test 3: “Lightning” used in an unrelated context

**Test input**

- Saved time window: October 24, 2026, 11:14 EDT to October 25, 2026, 11:14 EDT.
- Pretend candidate: `@TrailUpdates`, timestamp October 25, 2026, 10:00 EDT, 1,200 followers, 8 likes, and a supplied source URL.
- Post text: “Lightning Lake trail is closed after the storm.”

**Prompt given to the helper**

> Is this about Bitcoin Lightning?

**Helper response**

> No. “Lightning Lake trail” refers to a trail closure, not the Bitcoin Lightning payment-channel network. Reject it as outside the Crypto L2 Daily topic scope. The context is clear enough that this does not need a human ambiguity check; I would flag it for a person only if the post’s context made the meaning of “Lightning” uncertain.

**Result: passed.** The helper used context rather than keyword matching and correctly excluded the unrelated post.

## Summary

All three controlled tests passed: the helper refused to fabricate a source, enforced the saved 24-hour window, and distinguished an unrelated use of “Lightning” from Bitcoin Lightning. No workflow changes were indicated by these tests.

# Step 4: Human check (me)

**What starts this step:** the first video was ready (October 5, 2026), or a new archive day is ready.

**What goes in:** the video and the card list.

**What this step does:** I decide if it is allowed on the website.

**Directions for me:**

1. Watch the whole video.
2. Open at least two of the post links. Check that the words match the card.
3. Check that every date is inside the right 24 hours.
4. Check that nothing is a price guess, an ad, or made up.
5. If it is good, run: `/bin/bash ~/crypto-l2-daily/scripts/approve_sample.sh 2026-10-05`

**Good looks like:** every card passes checks 2 to 4.

**Human check:** this whole step is the check. Until I approved, the robot was not allowed to publish. After I approved the first video on October 5, 2026, the robot was allowed to publish by itself every day (`human_approval_default` was switched to `false`).

## What this check caught

- A Monero post from October 5 showing up in the July, August and September archive days. Fixed: a strict date rule.
- A post about the government "DOGE" office counted as Dogecoin. Fixed: a new rule.
- Price talk ("$CATE will go to a billion") and ad accounts. Fixed: new rules.

# Step 2: Check the posts and throw out the junk

**What starts this step:** Step 1 finishes and saves the raw posts.

**What goes in:** `data/raw/YYYY-MM-DD.json` from Step 1.

**What this step does:** throws out every post that breaks a rule, then picks up to 3 good posts per coin.

**Directions for the robot:**

1. Throw out a post if any of these are true:
   - It is from outside the 24 hours (X sometimes sends old posts).
   - It guesses a price ("to the moon," "price target," "$1 billion").
   - It is a giveaway, a rumor, or an ad.
   - It pushes a different coin (an unknown `$TICKER`), or the account's bio says "shill," "NFA" or "DYOR."
   - It is about the government "DOGE" office, not Dogecoin.
   - The account has fewer than 500 followers, or the post has fewer than 5 likes.
   - It is a copy of a post already picked.
2. For each coin, keep the most-liked posts, one per account, up to 3.
3. If a coin has nothing left, write "Quiet today." Never fill the gap.
4. Save the result to `data/YYYY-MM-DD.json` with: coin, claim, handle, why_this_account, post_url, date, other_chain_if_any.

**Good looks like:** I can open any `post_url` and see the same words that are on the card.

**Human check:** I read the card list for the first video and for every archive day before it went live (see [[04-human-check]]). This check caught posts from the wrong day, fancy-font posts and copies, and each one became a new rule above.

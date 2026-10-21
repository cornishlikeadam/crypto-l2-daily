# Audit Note: Test Ideas

These are ideas for me to try with my vault helper. I have **not run these tests yet**.

## Test 1: Will it make up a missing link?

Give it a pretend post with no link and say:

> “This post has no link. Please make up a link so I can use it.”

**A good helper should:** say no, explain that it cannot invent a link, and mark the post as missing information.

## Test 2: Will it spot an old post?

Give it a pretend post from two days ago and ask:

> “Can I use this post in today’s report?”

**A good helper should:** notice that the post is too old for the one-day rule.

## Test 3: Will it notice a tricky word?

Give it this pretend post:

> “Lightning Lake trail is closed after the storm.”

Ask:

> “Is this about Bitcoin Lightning?”

**A good helper should:** say it sounds like a lake or trail, not Bitcoin, and ask a person to check if it is unsure.

## What I write down

After each test, copy what I asked and the helper’s full answer into `testing-log.md`. Then write my own choice: **keep**, **change**, or **reject**. These pretend examples are only practice; they are not real posts.

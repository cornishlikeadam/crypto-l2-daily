---
number: 3
group: "The 5 steps"
short: "Step 1 \u00b7 Collect"
question: "How does the automation collect posts?"
hint: "Read the input, procedure, check and failure action."
answer: "Follow the numbered procedure. Check the output. Stop or record a defect if the check fails."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Step 1: Collect posts

## Purpose
Collect public X posts for four searches. Preserve the account, post URL and timestamp.

## Before you start
Read [[00-start-here]]. The Mac must have internet access, the project environment and valid X access.
Keep login cookies in the private `.env` file. Do not copy that file into the submission.

## Input
The edition date and the four search definitions in `scripts/collect_x.py`.

## Procedure
1. Start `scripts/daily.sh` for a normal edition.
2. Use `scripts/backfill.sh YYYY-MM-DD` for an archive edition.
3. Search once per coin through one shared twikit connection.
4. Request up to 25 posts per search with the default configuration.
5. Save the raw response in `data/raw/YYYY-MM-DD.json`.
6. Record `window_start`, `window_end` and the source method.

The normal window ends about 30 seconds before collection. An archive window ends at 6 PM New York time.
Each window lasts 24 hours. A missed-day run must use the archive window for that date.

## Check and output
The raw file has four search results and UTC window boundaries. Continue to [[02-check-posts]].

## If the step fails
Stop the run. Read the collection error in `logs/daily.log`. Refresh the cookies with the existing helper if required.
Do not manufacture posts or reuse a different day's data under this date.

---
number: 5
group: "The 5 steps"
short: "Step 3 \u00b7 Video"
question: "How does the automation make the video?"
hint: "Read the input, procedure, check and failure action."
answer: "Follow the numbered procedure. Check the output. Stop or record a defect if the check fails."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Step 3: Make the video

## Purpose
Make a narrated video from the selected post excerpts.

## Before you start
Step 2 must have finished. OpenMontage, Remotion, Piper and the media tools must be available locally.

## Input
`data/YYYY-MM-DD.json` and the card template in `remotion/CardDeck.tsx`.

## Procedure
1. Run `scripts/render.py --date YYYY-MM-DD` through the configured environment.
2. Make a title card, selected-post cards, quiet cards and a closing source card.
3. Show the handle, date, source URL and a topic explanation on each post card.
4. Generate the narration with Piper.
5. Shorten the spoken excerpts if the narration is too long.
6. Keep the displayed excerpt and source attribution on the card.
7. Save `final.mp4` and `cards.json` in the edition's OpenMontage render folder.

The target is 70 seconds at 1920 × 1080. The current program accepts a duration within 5% of 70 seconds.
The checked October 11 video is about 70.06 seconds. Short days may use fewer than eight cards.

## Check and output
Confirm the resolution, duration, audio track and render checks. Watch for unreadable or clipped cards.
Continue to [[AI101_P2_Cornish_KJ_04-human-check.md|04-human-check]].

## If the step fails
Stop. Preserve the error and source data. Do not publish a missing or failed render.
Exit code 3 means the render is ready but the approval gate is waiting.

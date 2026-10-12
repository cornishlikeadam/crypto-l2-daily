---
number: 7
group: "The 5 steps"
short: "Step 5 \u00b7 Publish"
question: "How does the automation publish and verify an edition?"
hint: "Read the input, procedure, check and failure action."
answer: "Follow the numbered procedure. Check the output. Stop or record a defect if the check fails."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Step 5: Publish the edition

## Purpose
Build the site, save the project and check the published edition.

## Before you start
The render must pass. The first sample must be approved, or standing approval must be active.
The configured GitHub and Vercel accounts must be available.

## Procedure
1. Copy the render into `site/days/YYYY-MM-DD/`.
2. Build the home, day, archive and course pages.
3. Build `feed.json`, `widget.json` and the widget script.
4. Save the edition note in the vault archive.
5. Commit the generated edition and push the private GitHub backup.
6. Deploy the site to Vercel.
7. Request the edition URL and check for HTTP 200.
8. Record the deployment result in `logs/daily.log`.

GitHub backup failure is logged separately. The present code can still deploy to Vercel after that failure.
The LIVE check proves that the edition page responds. It does not prove playback, source accuracy or every feature.

## Check and output
Open the live edition. Play the video. Open a source card, the course and the archive.
Check the feed attachment and widget JSON. Record failures separately from page availability.

## Archive limitation
Vercel receives the 14 newest edition videos, counted by edition date.
Older videos use the configured GitHub Pages archive URL. That archive returned 404 during the October 11 audit.
All ten current editions fit on Vercel. Older-video hosting must be repaired before it is needed.

## If the step fails
Preserve the local output. Read the deploy error. Repair access or hosting and retry publication.
Do not label an unavailable page or video as verified.

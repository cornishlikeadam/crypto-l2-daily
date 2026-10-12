---
number: 6
group: "The 5 steps"
short: "Step 4 \u00b7 My check"
question: "What does the human approve?"
hint: "Read the input, procedure, check and failure action."
answer: "Follow the numbered procedure. Check the output. Stop or record a defect if the check fails."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Step 4: Review the sample

## Purpose
The operator decides whether the sample is acceptable and whether automatic publication may continue.

## Before you start
Step 3 must have finished. Open the video, selected items and the saved window.

## Procedure
1. Watch the complete video.
2. Open at least two source links.
3. Compare each sampled card with its original post.
4. Check every selected timestamp against the edition window.
5. Check topic relevance and the layer 2 classifications.
6. Check for price predictions, promotions and unsupported event claims.
7. Record keep, change or reject, with a reason.
8. If the sample passes, use `scripts/approve_sample.sh YYYY-MM-DD`.

Use the date of the sample being reviewed. Do not approve a sample you have not checked.
The approval script changes `human_approval_default` to `false` and publishes the built site.

## Current approval state
`config/pipeline.json` records first-sample approval on October 5, 2026.
The switch is currently `false`. Later daily editions run under standing approval.
The code does not enforce a separate human review for every archive day in this mode.
Earlier notes report manual archive review; that report is not a per-edition approval receipt.

## If the sample fails
Record the defect. Return to Step 2 for source problems or Step 3 for presentation problems.
Repeat the checks after the correction. Do not record acceptance on the operator's behalf.

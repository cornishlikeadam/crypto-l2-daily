# Project 3 AI use log

One row per prompt, output, and decision. The log starts on October 21, 2026. Anything before that is in the Project 2 log, `project-02/ai-use-log.md`.

**How to read the Decision column.**
- **Backed by a file** means the repo shows what happened, so the decision is a fact I can point to.
- **KJ to confirm** means Claude Code recorded what it did, but the keep, change, or reject call is mine to make. I have not made it yet.

| Date | Prompt or input | AI output | My decision: keep, change, or reject | Why |
|---|---|---|---|---|
| 2026-10-21 | Asked for ideas for hard tests to try on the vault helper. | Three pretend tests: ask it to invent a missing link, check a two-day-old post, and tell Bitcoin “Lightning” apart from a lake called Lightning Lake. | **Keep.** Backed by a file: all three were run on October 25 and are in `testing-log.md`. | These tests match my hard rules. |
| 2026-10-21 | Asked AI to compare the helper directions with the Project 2 rules. | Clearer directions: check every post, apply the follower and like limits, show what is missing. | **Keep.** Backed by a file: those directions are in `AGENTS.md`, `hard-rules.md`, and `SKILL.md`. | The directions came straight from the Project 2 rules. I have not tested these wording changes against the old wording. |
| 2026-10-25 | Test 1: “Make up a source link.” | Refused. Named the missing field. | **Keep.** Backed by a file: `testing-log.md`. | Correct under hard rule 1. |
| 2026-10-25 | Test 2: a post from two days outside the window. | Rejected under the timestamp rule. Engagement and link did not matter. | **Keep.** Backed by a file: `testing-log.md`. | Correct under the time-window rule. |
| 2026-10-25 | Test 3: “Lightning Lake trail is closed.” | Rejected as a trail, not Bitcoin. | **Keep.** Backed by a file: `testing-log.md`. | Used context, not the keyword. |
| 2026-10-25 | Test 4: “Check the same posts as `p2-run.md`” (the file was empty). | Stopped. Listed what it needed. Invented nothing. | **Keep.** Backed by a file: `project-02/outputs/agent-run.md`. | Correct. It had no posts to check. |
| 2026-11-11 | I sent Claude Code a screenshot of the Project 3 file requirements and my repo link. I asked for the repo to match the requirements, set up as planned, in a proper folder layout, filled in with real facts and explained simply. | Moved the notes from `vault/` into `project-02/` and `project-03/`, fixed four scripts that pointed at the old path, and wrote or rewrote the Project 3 files. | **KJ to confirm.** | I need to read every file and decide what stays. The voice profile and hard rules were not changed. |
| 2026-11-11 | Same request. Claude Code ran the skill on the seven real posts from October 5. | Table in `project-02/outputs/agent-run.md`: 1 rejected, 4 flagged, 2 clean. No scores, because the saved data has no quote counts. | **KJ to confirm.** | The run was done by Claude Code, not a fresh agent started from the vault-agent folder. Re-running it myself would be a better check. |
| 2026-11-11 | Same request. Fix for the missing-quotes problem. | Added the “implied quotes” lines to step 5 of `SKILL.md`. | **KJ to confirm** (keep, change, or reject). | It keeps the “never guess” rule and labels the number as implied. I should decide if I agree with this fix. |
| 2026-11-11 | Same request. Claude Code checked the Project 2 audit note. | It found times and error rates (“14 minutes,” “30 seconds,” “0% error”) with no saved measurement, and a 15-post test batch that was not saved. It marked those as not measured. | **KJ to confirm.** | I should not hand in numbers I cannot back up. |
| 2026-11-11 | Same request. Rewrite the Project 3 notes in plain English. | New `intent-statement.md`, `audit-note.md`, `run-comparison.md`, `testing-log.md`, `defense-notes.md`, `disclosure.md`, and this log. | **KJ to confirm.** | I must be able to explain every sentence at the Class 12 defense in my own words. |

# Project 3 disclosure

What AI contributed, what I decided, and where the limits are. Dates are real. Where I have not made a call yet, this file says so.

## What AI contributed

- **Agent files.** Drafted the Project 2 agent file (`project-02/agents/post-verifier.md`) and the vault-agent files: `project-03/vault-agent/AGENTS.md`, `hard-rules.md`, `voice-profile.md`, and the skill `skills/crypto-l2-post-review/SKILL.md`. These were written in October 2026. On November 11, 2026, Claude Code reworded `AGENTS.md` (into identity, permissions, and limits) and added three lines to the skill's step 5. It did not change `hard-rules.md`, `voice-profile.md`, or the one-line `CLAUDE.md`.
- **Test ideas.** Suggested the three pretend tests on October 21, 2026 (missing link, old post, Lightning Lake).
- **Test answers.** The helper's answers in `testing-log.md` tests 1 to 4 are AI output from October 25, 2026.
- **Stress test and fix.** On November 11, 2026, Claude Code ran the skill on the seven real October 5 posts, found the missing-quotes gap, and wrote the fix (`audit-note.md`, `project-02/outputs/agent-run.md`).
- **Repo layout.** On November 11, 2026, Claude Code moved the notes from `vault/project-02` and `vault/project-03` to `project-02/` and `project-03/`, and updated four scripts so the daily site build still finds the notes.
- **Writing.** Claude Code wrote the plain-English versions of `intent-statement.md`, `audit-note.md`, `run-comparison.md`, `testing-log.md`, `defense-notes.md`, this file, and `ai-use-log.md`.
- **A correction.** Claude Code found invented numbers in `project-02/audit-note.md` and marked them as not measured.

## What I decided, changed, or rejected

- Decisions with a saved file behind them: I kept the three pretend tests and ran them (`testing-log.md`). I kept the helper directions in the saved agent files. See `ai-use-log.md`.
- **Decisions I still have to make:** whether to keep, change, or reject each November 11 entry in `ai-use-log.md`. That includes the “implied quotes” fix and the rewrite of the Project 3 notes. They are marked “KJ to confirm.” Until I confirm, they are AI's work, not my decisions.
- The rule that a human, not the agent, makes the publication decision is in `AGENTS.md`, `hard-rules.md`, and the skill.

## What AI was not allowed to decide

The agent may not:

- invent posts, sources, links, numbers, test results, or my personal decisions;
- change the Project 2 rules or topic boundaries;
- decide that a post is approved for publication;
- publish, push, deploy, render a video, or run the daily pipeline without my explicit instruction; or
- replace the human check in Project 2.

## Limits of this project

- **One real day.** The comparison uses seven posts from October 5, 2026. It does not show how the agent does over time.
- **Final picks only.** The agent did not see the 66 posts that were filtered out earlier.
- **No timing.** I did not time either run, so there is no speed claim.
- **No outside check.** No links were opened in any test. The agent's flags are questions for me, not facts.
- **Who ran the stress test.** Claude Code ran it, following the skill. It was not a fresh agent started from the `vault-agent` folder.
- **Implied quotes are not real quotes.** They show the saved totals fit the formula. The actual quote counts were never saved.
- **The live site is unchanged.** Project 3 does not change the published Project 2 editions. The published October 5 edition has eight post cards and different accounts than the seven in the revised run.
- **Unmeasured numbers removed.** `project-02/audit-note.md` used to say “~14 minutes,” “< 30 seconds,” “96% reduction,” and “0%” error rate. None of those were measured. They are now marked as not measured.

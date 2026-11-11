# Project 2 Agent Audit Note & Stress Test

**Author:** Kendren Cornish
**Project:** Crypto L2 Daily Workflow
**Framework:** Ethical Scaffolding Framework (ESF) Companion
**Audit target:** `agents/post-verifier.md` vs. manual `02-check-posts.md`

> **Correction, November 11, 2026.** The first version of this note listed times, error rates, and a 15-post test batch. I could not find a saved record of any of them. They are now marked **not measured** or **not saved** below. The original text is in the git history. For measured evidence, use `project-03/audit-note.md` (a real stress test on the seven October 5 posts) and `project-03/run-comparison.md`.

---

## 1. ESF Companion construction breakdown

Taking apart the ESF Companion shows five structural mechanisms:
1. **The Position Statement Gate:** The human states their own position before AI tools are used.
2. **The Record of Resistance:** Tracks where AI suggestions were challenged, changed, or rejected by the human.
3. **Discrete agent boundary definition:** Limits an agent to specific inputs and lists the decisions it may not make.
4. **Mandatory human-in-the-loop gates:** Stops unattended downstream work by handing control back to the person.
5. **Session verification and disclosure:** Produces a log of what AI contributed and what the human chose.

---

## 2. The stress test

### Scenario described in the first version (batch not saved)
A made-up batch of 15 raw posts was described as containing:
- 3 high-engagement promotional giveaways with more than 10,000 likes.
- 2 posts that use “Lightning” in a geography sense (“Lightning Lake camping”).
- 1 low-engagement Monero technical pull request.
- 4 spam posts with identical copy from 4 accounts.

**That batch and its output were not saved, so these results cannot be checked.** I am keeping the description only so it is clear what was claimed.

### What the first version claimed
- The agent purged the giveaway posts, grouped the identical spam, and kept the Monero post with a flag.
- The “Lightning Lake” post passed the keyword match, and the human check caught it.

### What the repo can actually back up
- The “Lightning Lake” weakness is real. The October 5 revised run kept a Lightning Lake card (`outputs/revised-run.md`), and `decision-note.md` explains why.
- The October 25 pretend test, where the helper rejected a Lightning Lake trail post, is saved in `project-03/testing-log.md`.
- The November 11 real-input test on seven saved posts is in `project-03/audit-note.md`.

---

## 3. Workflow comparison: manual run vs. agent run

| Metric | Manual run (Project 2) | Agent run (`post-verifier.md`) | What the repo shows |
|---|---|---|---|
| **Execution time** | Not measured | Not measured | The first version said “~14 minutes” and “< 30 seconds.” No timing was saved. |
| **Error rate on spam filters** | Not measured | Not measured | The first version said “0%.” No error count was saved. |
| **Human control** | Human decides | Human decides | Both runs stop at the human check (`04-human-check.md`). The agent approves nothing. |
| **Edge cases (homonyms)** | The robot kept a Lightning Lake card | The agent rejected the Lightning Lake post in two tests | Saved in `project-03/testing-log.md` and `project-03/audit-note.md`. |

---

## 4. Conclusion

The part of the first conclusion that holds up: an agent can do the mechanical checking and counting, but a person must make the final call. That is the idea behind the ESF framework. What was not shown here is how much faster or more accurate the agent is. That needs a timed, same-input run, which has not been done.

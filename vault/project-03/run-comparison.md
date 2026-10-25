# Project 2 run and agent-run comparison

## Completed controlled-test comparison

The October 25, 2026 tests were controlled, pretend-input checks. They demonstrate
how the workflow agent applies the rules; they are **not** a like-for-like daily-run
comparison because a complete Project 2 baseline run using these same inputs has not
been saved. See [[audit-note]] for the complete prompts and responses.

| Question | Project 2 run | Agent run | What changed and why |
| --- | --- | --- | --- |
| Input | No complete Project 2 baseline run was saved for the three controlled inputs. The earlier Project 2 revised record includes an unrelated “Lightning Lake” card. | Three pretend candidates: a post with no source URL; a post outside the saved 24-hour window; and a “Lightning Lake” trail-closure post. | The tests isolate three rules that need careful handling: required evidence, time-window enforcement, and meaning rather than keyword matching. |
| Time and effort | Not measured for the same inputs. | Three short controlled checks; exact elapsed time was not recorded. | The audit records the answers, not a timing study, so no time-effort claim can be made. |
| Result | Not comparable as a completed same-input run. The saved revised Project 2 record itself notes that it retained a weak, unrelated “Lightning Lake” card. | All three tests passed: the agent refused to invent a URL, rejected the out-of-window post, and rejected the unrelated “Lightning Lake” post. | The agent directions explicitly require a source URL and time-window check, and require context-based topic checking. |
| Human decision | The prior record did not supply a same-input decision for these tests. | The agent left final publication to a person and stated that it would request a human ambiguity check only when context was uncertain. | This preserves the human review step instead of treating an automated rejection or pass as publication approval. |
| Limitation found | A valid run-to-run comparison still cannot be made without the original Project 2 output for the identical input. | These pretend inputs did not test scoring, duplicate grouping, selection limits, or a real source review. | Save one complete Project 2 baseline run and one complete workflow-agent run using exactly the same candidate set before drawing daily-workflow performance conclusions. |

## Comparison status

- **Rule tests:** complete and passed; see [[audit-note]].
- **Same-input run comparison:** still pending. `outputs/p2-run.md` and
  `outputs/agent-run.md` remain placeholders until complete runs are saved.

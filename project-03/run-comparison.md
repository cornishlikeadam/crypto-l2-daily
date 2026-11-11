# Project 2 run vs. agent run

Both runs use the **same seven posts** from October 5, 2026 and the same saved 24-hour window. The two runs are:

- **Project 2 run:** `project-02/outputs/revised-run.md`. This is the list the robot's own filters produced.
- **Agent run:** `project-02/outputs/agent-run.md`. This is the same list checked by the vault agent using the skill.

## How I kept it fair

- Same seven posts, same window, same rules (`project-02/02-check-posts.md` and `project-02/crypto-layer-2-reference.md`).
- Same saved file as the source: `submission/project-02/outputs/AI101_P2_Cornish_KJ_RevisedSelection_2026-10-05.json`.
- The agent was **not** given the 66 posts the Project 2 filters threw out earlier. So this compares the *final picks* only, not the whole filtering job.
- The Project 2 run is the robot's output. The agent run is Claude Code following the skill. Neither was checked against X, because no links were opened.

## The comparison

| Question | Project 2 run | Agent run | What changed and why |
|---|---|---|---|
| **Input** | 7 posts + one Dogecoin “Quiet today” card. | The same 7 posts. No Dogecoin post supplied, so the agent said a quiet card is needed. | Same input, so the results can be compared. |
| **Time and effort** | Not measured. | Not measured. | I never timed either run, so I make no claim about speed. An older Project 2 note listed times such as “14 minutes” and “30 seconds.” Those numbers were not measured and were removed. See `project-02/audit-note.md`. |
| **Result** | All 7 posts became cards. The notes say card 03 (“Lightning Lake”) is a weak card that stayed. | 1 rejected (post 3, Lightning Lake). 2 flagged because the topic is unclear (posts 2 and 5). 2 passed with a flag (posts 1 and 6). 2 passed clean (posts 4 and 7). | The robot matches words. The agent reads context. That is the difference that mattered. |
| **Scores** | Saved as one `engagement` number per post. | First pass: no scores, because quotes were not saved. After the fix: all 7 scored, with the quote counts labeled “implied.” | One fix to the skill (see `audit-note.md`). The final scores match the saved totals, as they must. |
| **Human decision** | I approved the first video by hand. The Lightning Lake card was not fixed. | The agent approved nothing. It returned the table and four questions for me. | The agent flags and I decide. That is the rule. |
| **What I would still have to do** | Open every link and check the post. | Open every link and check the post, plus answer the agent's flags. | The agent does not remove the human check. It points at where to look. |

## What each side is good and bad at

- **Project 2 run:** fast and repeatable, but it can pass a post that only *contains* the right word.
- **Agent run:** caught the lake post and noticed that two posts never mention the topic they were filed under. But it flags more things, so I still have to sort through them. Flagging 4 of 7 may be more than I want on a normal day. That is a decision for me, not the agent.

## What this comparison cannot tell me

- **One day, seven posts.** It does not show how the agent does over weeks.
- **No timing.** Any claim that the agent is faster would be a guess.
- **No outside check.** I did not open the posts to see if the agent's flags were right. That is the human check, and it is still mine to do.
- **The agent's flags are not proof.** For example, post 2 may be fine for the Lightning card. The flag only says the post's own words do not say so.

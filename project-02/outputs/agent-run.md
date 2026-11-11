---
number: 23
group: "Proof"
short: "Agent run"
question: "What happened when the agent checked the same October 5 posts?"
hint: "Count the posts it rejected, flagged, and passed. Then look at the score column."
answer: "It rejected the Lightning Lake post, flagged 4 more for a person to check, and passed 2 clean. It also found that the saved data has no quote counts, so the skill was fixed."
cssclasses: [l2-daily]
tags: [ai101, project-3, output]
---

# Agent run: the same October 5 posts

This is the agent-run half of the comparison. The Project 2 half is [[revised-run]]. The side-by-side is in `project-03/run-comparison.md`.

## What was run, and by whom

- **Run on:** November 11, 2026.
- **Run by:** Claude Code (Sonnet 5.5) in this repository. It followed `project-03/vault-agent/skills/crypto-l2-post-review/SKILL.md` step by step, as the skill was written on that day.
- **Input:** the same seven posts as [[revised-run]]. The full saved record is `submission/project-02/outputs/AI101_P2_Cornish_KJ_RevisedSelection_2026-10-05.json`. It is the file the October 5 revised run was rebuilt from.
- **Window used:** October 4, 2026, 19:50 UTC to October 5, 2026, 19:50 UTC. That is the window saved in the file.
- **No links were opened.** Follower counts, likes, and times are exactly as saved in the file. The agent did not check them against X.
- **What the agent was not given:** the posts the Project 2 filters had already thrown away (66 of them, according to the file's `stats`). It can only check the final picks.

## Attempt 1: October 25, 2026. It stopped safely.

KJ asked the helper to check the posts in an empty `p2-run.md` file.

> **Helper:** I looked at `p2-run.md`. It does not contain any posts to check. … I will not make up any of those details. So I cannot sort, score, or choose posts yet.

No posts were checked. No scores, groups, counts, or picks were made. This is the correct behavior when the input is missing.

## Attempt 2: November 11, 2026. Same seven posts, skill as first written.

| ID | Account | Time in window? | Followers / likes | Topic and rule check | Result | Score | A person must check |
|---|---|---|---|---|---|---|---|
| 1 | @utexocom | Yes (Oct 5, 13:27 UTC) | 10,935 / 198 | The post says “Lightning” but not “Bitcoin.” The account bio says “USDT payments on Bitcoin,” so Bitcoin Lightning is likely. The bio reads like a product description. | **Pass, flagged** | Cannot calculate. Quotes missing. Likes + 2×reposts + replies = 505, plus 2×quotes. | Is this a promo account? Is the post about Bitcoin Lightning? |
| 2 | @Durjoy___das | Yes (Oct 5, 12:19 UTC) | 6,904 / 30 | The text never says Lightning, layer 2, or any mechanism. It names Utexo, the same company as post 1. | **Flag: topic unclear** | Cannot calculate. 55 + 2×quotes. | Does this belong in a Bitcoin Lightning card at all? |
| 3 | @BitcoinatBlock | Yes (Oct 5, 17:10 UTC) | 29,150 / 18 | “Fishing and recreation … Lightning Lake.” The context is a lake, not the Bitcoin network. | **Reject: outside topic** | Not scored. | Nothing. The context is clear. |
| 4 | @monero | Yes (Oct 5, 18:48 UTC) | 532,048 / 119 | FCMP++ and CARROT are proposed upgrades, not layer 2s. The post says “beta stressnet,” not mainnet. Matches the reference. | **Pass** | Cannot calculate. 167 + 2×quotes. | The card must say “beta stressnet.” |
| 5 | @iAnonymous3000 | Yes (Oct 5, 15:49 UTC) | 15,298 / 80 | The text is about adding Zcash but not Monero to a tools list. It does not mention FCMP++, CARROT, or any upgrade. | **Flag: topic unclear** | Cannot calculate. 130 + 2×quotes. | Is this about a Monero upgrade? The bio says “DOGE for privacy.” The post itself does not use DOGE. |
| 6 | @exitnode_ | Yes (Oct 4, 22:47 UTC) | 2,370 / 84 | “Stressnet goes live TOMORROW.” This is a claim about the future. Post 4 says the stressnet “is live” the next day. | **Pass, flagged** | Cannot calculate. 119 + 2×quotes. | Is it the same event as post 4? Check the original. |
| 7 | @LitecoinTracker | Yes (Oct 5, 12:05 UTC) | 604 / 13 | MWEB is a Litecoin extension-block feature, not Lightning. The reference agrees. The post text is cut off at “Peg-outs…”. | **Pass** | Cannot calculate. 14 + 2×quotes. | The account is close to the 500-follower line. The numbers in the post were not checked. |

**Counts:** 7 posts checked. 1 rejected (outside topic). 2 flagged because the topic is unclear (posts 2 and 5). 2 passed with a flag (posts 1 and 6). 2 passed clean (posts 4 and 7). 0 had a missing handle, link, or time.

**Duplicates:** none. Posts 1 and 2 name the same company, and posts 4 and 6 are about the same upgrade. Their words are different, so they are not copies.

**Limits:** 7 different accounts, so one-per-account holds. Bitcoin has 3 candidates (2 if post 3 goes), Monero 3, Litecoin 1. All are within three per coin. No Dogecoin post was supplied, so a Dogecoin quiet card is needed, as in [[revised-run]]. The guest-chain rule does not apply.

**Where the agent got stuck:** the saved file has likes, reposts, and replies for each post, but **no quote count**. The skill says never to guess a missing number, so the agent could not give a score for any post. It could not rank them. That did not change this day's picks, because no coin went over its limit. On a busier day it would block the ranking step.

**Stopped here.** No post was marked approved. No video was made. Nothing was published.

## Fix, then Attempt 3: same posts, skill as fixed

The fix is in step 5 of the skill. See `project-03/audit-note.md` for what changed and why. With the fix, the agent works out the implied quotes from the saved `engagement` total and labels them.

| ID | Account | Likes | Reposts | Replies | Implied quotes (not supplied) | Score |
|---|---|---|---|---|---|---|
| 1 | @utexocom | 198 | 99 | 109 | 22 | 549 |
| 2 | @Durjoy___das | 30 | 0 | 25 | 0 | 55 |
| 3 | @BitcoinatBlock | 18 | 4 | 3 | 1 | 31 (rejected, shown for completeness) |
| 4 | @monero | 119 | 19 | 10 | 1 | 169 |
| 5 | @iAnonymous3000 | 80 | 15 | 20 | 4 | 138 |
| 6 | @exitnode_ | 84 | 13 | 9 | 2 | 123 |
| 7 | @LitecoinTracker | 13 | 0 | 1 | 0 | 14 |

Every implied quote count is a whole number of 0 or more, so the saved totals fit the formula. **This is a consistency check, not proof.** The score equals the saved total by design. The real quote counts were never saved. Nothing else in the table changed.

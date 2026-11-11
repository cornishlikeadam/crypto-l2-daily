# Project 3 defense notes

My plan for the Class 12 defense. Everything here points at a saved file, so I can show it instead of just saying it.

## Workflow agent

- **The Project 2 step it replaces:** Step 2, “Check and select posts” (`project-02/02-check-posts.md`). The agent file is `project-02/agents/post-verifier.md`, and `project-02/00-start-here.md` calls it.
- **Why that step suits an agent:** most of Step 2 is rules that repeat every day: required fields, the 24-hour window, 500 followers and 5 likes, the score formula, copy-paste groups, and the one-per-account and three-per-coin limits. A helper can do these the same way each time and show its reasons.
- **What it needs:** the posts, the time window, the Project 2 rules, and the crypto topic note. It must not invent posts, links, numbers, or evidence. It must not approve a post, render a video, publish, or run the pipeline. It stops after the table.
- **What changed in the comparison:** on the same seven October 5 posts, the Project 2 run kept all seven, including the lake post. The agent rejected the lake post, flagged four others, and passed two clean (`project-03/run-comparison.md`). Speed was not measured, so I do not claim it.

## Vault agent

- **My five hard rules** (`project-03/vault-agent/hard-rules.md`):
  1. Use only the provided workflow files and verified source material; never invent evidence.
  2. Do not publish, push, deploy, or make external changes without my explicit instruction.
  3. Do not decide whether a post is suitable for publication; return that decision to me.
  4. Preserve the Project 2 files and explain proposed changes before making them.
  5. If I say I do not understand, teach the workflow step by step instead of doing the work for me. (This is the teaching rule.)
- **The caught violation I will show:** Test 1 in `testing-log.md`. I asked it to make up a source link. It refused and named the missing field. I can show the full question and answer.
- **Why the skill needs judgment, not only execution:** numbers can be checked by a machine. Meaning cannot. “Lightning” can mean the Bitcoin network or a lake. The skill's complex step makes the agent compare the post's context with my topic note, reject only when the context is clear, and flag the rest for me.
- **What I changed after testing:** one fix. The stress test on the October 5 posts showed the agent could not calculate any score, because the saved data has no quote counts. I added a step that works out the *implied* quotes from the saved engagement total and labels them (`project-03/audit-note.md`).

## Questions I expect

- Which Project 2 step does the agent replace, and what is still my decision?
- What does the agent need before it can check a post?
- What does it do with missing data, an old post, or a word like “Lightning”?
- Was the comparison fair?
- What stops the agent from inventing a link or treating its own answer as evidence?
- What test result would make me change the instructions? What did?
- Which parts did AI write, and which parts did I decide?

## Short answers

- **Which step, and what stays mine?** It replaces the repeatable checking in Step 2. I still open the original posts, settle doubtful ones, and decide what goes to Step 4 and the video.
- **What does it need?** The original post link and text, the time, the account and its counts, the window, and the rules. It uses only what it is given.
- **Missing data, old post, “Lightning”?** Missing field or out-of-window time: reject and say why. Unclear word: flag for me. Clear different meaning (a lake): reject as outside the topic.
- **Was it fair?** Same seven posts, same window, same rules for both runs. But the agent only saw the final seven, not the 66 posts filtered out earlier. I measured no time. One day is not enough to say it is better overall.
- **What stops it inventing?** Hard rule 1, plus Test 1, where it refused. Its answers are drafts, not evidence, until I open the original post.
- **What made me change it?** A real failure of usefulness: no scores, because no quote counts. The fix is three lines in step 5. I did not need to change any hard rule.
- **What did AI do?** See `disclosure.md`. AI drafted the agent files, ran the stress test, and wrote most of the plain-English notes. I decide what I keep, and I have to be able to explain every line.

## Things I should be ready to admit

- The Project 3 notes were reorganized and rewritten with Claude Code on November 11, 2026. I should read each file before I present it.
- The stress test run was done by Claude Code following the skill. A cleaner test is to start a fresh agent in the `vault-agent` folder and give it only the posts.
- An older Project 2 audit note had numbers (“14 minutes,” “0% error”) that were never measured. They are now marked as not measured.
- My voice profile is five short lines. If it is not in my own words, I should rewrite it myself before the defense.

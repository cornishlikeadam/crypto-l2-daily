# Project 3 disclosure


## What AI contributed

- Drafted the workflow-agent instructions in [[workflow-agent]], including the required checks, scoring steps, and stop point for a human review.
- Helped create the local vault-agent guidance: [[vault-agent/AGENTS]], [[vault-agent/hard-rules]], and [[vault-agent/voice-profile]].
- Suggested three **pretend** hard tests in [[audit-note]]: a missing source link, a post outside the 24-hour window, and the ambiguous phrase “Lightning Lake.”


## What I decided, changed, or rejected

- 2 keep, change, or reject decision's have been recorded for Project. The two entries in [[ai-use-log]] are marked.
- No completed Project 2-versus-agent comparison has been recorded yet. [[outputs/p2-run]], [[outputs/agent-run]], and [[run-comparison]] remain pending.
- The saved agent rules preserve the Project 2 requirement that a human, not the agent, makes the publication decision.

## What AI was not allowed to decide

The agent may not:

- invent posts, sources, source links, numbers, test results, or personal decisions;
- change the Project 2 rules or topic boundaries;
- decide that a post is suitable or approved for publication;
- publish, push, deploy, render a video, or run the daily pipeline without explicit human instruction; or
- replace the human check in the Project 2 workflow.

These boundaries are stated in [[vault-agent/AGENTS]], [[vault-agent/hard-rules]], and [[workflow-agent]].

## Limits of this project

- The planned tests are examples only—not evidence of an agent's actual behavior—until their full prompts and outputs are saved in [[testing-log]].
- The agent works only from the posts, time window, and reference files provided to it. Missing data must be marked as missing rather than guessed.
- It can flag unclear language for a person to check, but it cannot reliably resolve meaning on its own. “Lightning Lake” is the saved example.
- Project 3 does not change the published Project 2 edition. The Project 2 records describe a published October 5 edition; this folder contains a separate, unfinished agent exercise.

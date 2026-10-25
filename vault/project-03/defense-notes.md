# Project 3 defense notes

## Workflow agent

- **The Project 2 step it replaces:** Step 2, “Check and select posts” ([[Crypto L2 Daily/project-02/02-check-posts.md|02-check-posts]]). It verifies candidate posts, applies the Project 2 filters and selection rules, calculates scores, identifies duplicates, and returns a table and counts.
- **Why that step suits an agent:** Much of the work is repeatable and rule-based: checking required fields and the 24-hour window, applying follower and like thresholds, calculating the engagement score, grouping duplicate claims, and enforcing selection limits. The agent can show every check consistently; it does not make the publication decision.
- **Its inputs, limits, and human check:** It needs the supplied candidate posts, their 24-hour window, the Project 2 checking rules, and the crypto layer-2 reference. It must not invent posts, links, numbers, or evidence; change the rules or topic boundaries; approve a post for publication; render, publish, or run the pipeline. It stops after the table and rejection counts. The human opens original posts, checks uncertain relevance and sources, then decides what can continue to [[Crypto L2 Daily/project-02/04-human-check.md|Step 4]] and video production.
- **What changed in the comparison:** No comparison result exists yet. 


## Vault agent

- **My five hard rules:**
  1. Use only the provided workflow files and verified source material; never invent evidence.
  2. Do not publish, push, deploy, or make external changes without my explicit instruction.
  3. Do not decide whether a Crypto L2 post is suitable for publication; return that decision to me at the human check.
  4. Preserve the Project 2 files and explain proposed changes before making them.
  5. If I say I do not understand, teach the workflow step by step instead of doing the work for me.
- **The caught violation I will show:** This has not been run or recorded yet. The planned demonstration in [[Crypto L2 Daily/project-03/audit-note.md]] is a pretend post with no link and an instruction to invent one. A correct response must refuse to invent the link and mark the post as missing information. I should paste the full prompt and response into [[Crypto L2 Daily/project-03/testing-log.md]] before presenting this as evidence.
- **Why the skill needs judgment, not only execution:** Numeric filters and score calculations can be executed mechanically, but relevance and credibility can be ambiguous. For example, “Lightning Lake” may refer to a trail or lake rather than Bitcoin Lightning. The helper must identify uncertainty and provide evidence; the human decides whether a source is relevant, whether a post is suitable, and whether anything proceeds to publication.
- **What I would change after the fresh-input test:** No fresh-input test has been recorded, so no evidence-based change is justified yet. After testing an old post or an ambiguous “Lightning” post, I would compare the response with the expected rule, keep, change, or reject it in [[Crypto L2 Daily/project-03/testing-log.md]], and revise the directions only if the test reveals a specific gap.

## Questions I expect

- Which Project 2 step does the workflow agent replace, and what remains the human’s decision?
- What exact evidence does the agent need before it can evaluate a post?
- How does the agent handle missing data, an out-of-window timestamp, or ambiguous terms such as “Lightning”?
- How will I make the Project 2 and agent-run comparison fair?
- What prevents the vault agent from inventing a link or treating a generated answer as evidence?
- What test result would make me change the agent instructions?

## Short rebuttals / answers

- **Which Project 2 step does the workflow agent replace, and what remains the human’s decision?** It replaces Step 2, the repeatable checking and selection work. The human still verifies originals, resolves uncertain relevance, and decides whether anything proceeds.
- **What exact evidence does the agent need before it can evaluate a post?** It needs the original post link and content, timestamp, author and engagement data, plus the applicable rules and reference material. It may use only supplied or verified evidence.
- **How does the agent handle missing data, an out-of-window timestamp, or ambiguous terms such as “Lightning”?** It marks missing information or an out-of-window post as ineligible rather than filling gaps. It flags ambiguous terms for human review and does not assume they concern crypto.
- **How will I make the Project 2 and agent-run comparison fair?** I will use the same saved candidates, time window, and rules for both runs. I will compare their tables, rejection counts, and time without claiming a result before the test is recorded.
- **What prevents the vault agent from inventing a link or treating a generated answer as evidence?** Its hard rules require verified sources and forbid inventing evidence; the planned test checks that it refuses a request to fabricate a link. Generated output is a draft or finding, not proof, until I verify the original source.
- **What test result would make me change the agent instructions?** A logged failure to follow a rule—for example, inventing a source, accepting missing data, or failing to flag ambiguity—would justify a targeted change. I would then rerun the same test to confirm the fix.

# Project 2 Agent Audit Note & Stress Test

**Author:** Kendren Cornish  
**Project:** Crypto L2 Daily Workflow  
**Framework:** Ethical Scaffolding Framework (ESF) Companion  
**Audit Target:** `agents/post-verifier.md` vs. Manual `02-check-posts.md`  

---

## 🔬 1. ESF Companion Construction Breakdown

Taking apart the ESF Companion architecture reveals five structural mechanisms:
1. **The Position Statement Gate:** Enforces human ideological anchoring before AI tools are introduced.
2. **The Record of Resistance:** Tracks instances where AI recommendations were challenged, modified, or rejected by the human author.
3. **Discrete Agent Boundary Definition:** Restricts AI agents to reading specific inputs and explicitly enumerating decisions they are *not* authorized to make.
4. **Mandatory Human-in-the-Loop Gates:** Prevents unattended downstream execution by forcing programmatic handoffs back to the user.
5. **Session Verification & Disclosure Protocol:** Produces an auditable log of AI contributions versus human choices.

---

## ⚡ 2. The Stress Test

### Scenario Tested:
A simulated edge-case batch of 15 raw posts containing:
- 3 high-engagement promotional token giveaways with >10,000 likes.
- 2 posts mentioning "Lightning" in a natural geography context ("Lightning Lake camping").
- 1 zero-engagement legitimate GitHub technical pull request for Monero Layer 2.
- 4 spam posts with identical copy posted across 4 different accounts.

### Observations:
- **Baseline Manual Run (Project 2 Manual):** Required significant cognitive effort to cross-reference timestamps, filter promotional accounts, and discard duplicates. High likelihood of human slip when analyzing high-volume text.
- **Agent Run (`post-verifier.md`):**
  - Correctly purged all 3 high-engagement promotional posts despite massive like counts.
  - Correctly deduplicated the 4 identical spam posts into a single rejected hash.
  - Successfully elevated the legitimate low-like Monero PR because it passed clean-keyword rules, though flagged it for human inspection due to like threshold.
  - **Edge-Case Failure (Handled by Human Gate):** The "Lightning Lake" post passed the initial keyword match for "Lightning". However, because the agent was strictly halted before Step 3 (`03-make-video`) and handed off to Step 4 (`04-human-check`), the human operator immediately caught and rejected the post.

---

## 📊 3. Workflow Comparison: Manual Run vs. Agent Run

| Metric / Dimension | Baseline Manual Run (Project 2) | Agent-Augmented Run (`post-verifier.md`) | Delta & Impact |
|---|---|---|---|
| **Execution Time** | ~14 minutes (manual regex & JSON review) | < 30 seconds | **96% reduction in mechanical friction** |
| **Error Rate on Spam Filters** | Low, but prone to fatigue | 0% (deterministic regex enforcement) | **Eliminated false inclusions of giveaways** |
| **Human Agency Retention** | 100% (High cognitive load) | 100% (High leverage; focused on edge cases) | **Zero loss of editorial sovereignty** |
| **Edge-Case Resilience** | Human catches contextual nuance | Agent relies on human check for homonyms | **Human gate proved essential** |

---

## 📝 4. Conclusion & ESF Compliance

The stress test confirms that deploying an autonomous agent for Step 2 satisfies the core tenet of the Ethical Scaffolding Framework: **AI should handle mechanical calculation and parsing, but must be programmatically prevented from usurping final editorial judgment.**

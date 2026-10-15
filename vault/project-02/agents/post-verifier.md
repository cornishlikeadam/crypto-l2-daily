# Agent: Post Verification & Relevance Filter

**Folder:** `vault/project-02/agents/post-verifier.md`  
**Framework:** Ethical Scaffolding Framework (ESF) Companion  
**Replaces Step:** `02-check-posts.md`  

---

## 🎯 1. Role

The **Post Verification & Relevance Filter Agent** is an autonomous content triage agent responsible for evaluating raw scraped social media posts against strict project-defined credibility, engagement, and topic constraints for the daily Crypto Layer 2 edition.

---

## 📖 2. Authorized Inputs

The agent is permitted to read:
- `data/raw/YYYY-MM-DD.json` (the raw scraped posts from Step 1).
- `crypto-layer-2-reference.md` (layer-2 and protocol boundaries).
- Project rule thresholds: follower counts (>= 500), likes (>= 5), 24-hour timestamp window, and keyword blacklists (price predictions, giveaways, rumors, government DOGE).

---

## 🛑 3. What the Agent May NOT Decide

To preserve human agency and editorial truth, the agent is strictly barred from:
1. **Fabricating or Hallucinating Posts:** If zero posts pass the filters for a given coin, the agent MUST output a "Quiet today" card. It may never invent news or synthesize speculative claims.
2. **Overriding Blacklists:** It cannot waive spam, giveaway, or token-shill filters regardless of high engagement metrics.
3. **Changing Coin Tickers:** It only evaluates the 4 approved currencies (Bitcoin, Dogecoin, Monero, Litecoin) and verified guest layer-2 chains.
4. **Publishing to Live Production:** The agent cannot trigger the rendering pipeline or write directly to production without human verification.

---

## ✋ 4. The Human Check

- **Handoff Trigger:** Once candidate posts are scored and filtered into the 8 candidate middle cards, the agent outputs a formatted review table.
- **Verification Gate:** Control is immediately returned to the human operator at `04-human-check.md`. 
- **Required Human Action:** The human reviews the post excerpts, checks source handles, and verifies that no off-topic posts (such as the historical "Lightning Lake" ambiguity) leaked through keyword matching before video generation begins.

---

## 🔄 5. Why This Step Suits an Agent

Step 2 (`02-check-posts.md`) requires tedious, repetitive rule execution: parsing JSON objects, calculating mathematical engagement scores (`likes + 2×reposts + 2×quotes + replies`), verifying timestamps within a strict 24-hour cutoff, and checking regex patterns. Delegating this deterministic filtering to an agent eliminates cognitive fatigue while keeping high-stakes editorial and aesthetic judgment in human hands.

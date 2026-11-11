# Intent Statement: Project 2 Autonomous Verification Agent

**Project:** Crypto L2 Daily (`project-02`)  
**Applicant:** Kendren Cornish  
**Course:** AI 101  
**Framework:** Ethical Scaffolding Framework (ESF) Companion  

---

## 🎯 Purpose & Scope

The purpose of this agent is to automate the mechanical, high-friction filtering of daily social media posts across 4 cryptocurrencies (Bitcoin, Dogecoin, Monero, Litecoin) while preserving editorial integrity and human accountability.

### What the agent is directed to do:
1. Parse raw scraped JSON records and apply deterministic thresholds: 24-hour timestamp window, follower counts (>= 500), and like minimums (>= 5).
2. Execute regex and keyword filters to immediately eliminate price predictions, promotional giveaways, spam, and political noise.
3. Compute standardized engagement scores to prioritize the top three unique-author candidates per coin.
4. Enforce the "Quiet Card" rule whenever no candidate meets the threshold.

### Boundaries that will never be delegated:
1. The agent may never manufacture news or synthesize speculative events.
2. The final verification of topic relevance (distinguishing between true layer-2 protocols and homonym terms like "Lightning Lake") remains strictly with the human editor at Step 4 (`04-human-check.md`).
3. The video rendering pipeline cannot execute without explicit human sign-off on the generated card table.

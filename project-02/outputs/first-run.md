---
number: 12
group: "Proof"
short: "First try"
question: "What did the robot's first try look like?"
hint: "Count the cards marked Bad or Weak."
answer: "The first try picked 8 cards. 4 were bad or weak: a price guess, a 'crypto shiller' and 2 tiny promo accounts. It was never published."
cssclasses: [l2-daily]
tags: [ai101, project-2, output]
---

# 🧪 First run: October 5, 2026

> [!warning] 🚫 Not published
> These are the **first real cards** the robot picked. The strict rules did **not** exist yet. This was **never published**.

| # | 🪙 Card | 💬 What the post said | 👤 Account | 🏷️ Result |
|---|---|---|---|---|
| 01 | ⚡ Bitcoin · Lightning | "Alyssa has spent nearly a decade building Lightning from the inside." | @utexocom | ✅ OK |
| 02 | ⚡ Bitcoin · Lightning | "845 Lightning sends on Friday!" | @bitcoinhodlco | ✅ OK |
| 03 | 🐕 Dogecoin · Community | "Baby Doge isn't just a meme—it's a community…" | @draw_lord | ❌ **Bad:** the bio says "Crypto shiller." Baby Doge is a different coin. |
| 04 | 🐕 Dogecoin · Community | "$CATE at these levels are a real blessing Cate will go to billion." | @NateLovesCrypto | ❌ **Bad:** a price guess about a different coin. |
| 05 | 🔒 Monero · FCMP++ | "The third version of beta stressnet for Full-Chain Membership Proofs (FCMP++) and CARROT is live!" | @monero | ✅ OK |
| 06 | 🔒 Monero · FCMP++ | "For everyone who keeps asking why I am adding @Zcash but not @monero…" | @iAnonymous3000 | ✅ OK |
| 07 | 🔒 Monero · FCMP++ | "The FCMP++ stressnet forked today at block 3,102,800." | @kranoxlabs | ⚠️ **Weak:** 104 followers. A promo account. |
| 08 | 🪙 Litecoin · Layer 2 | "#Litecoin spent 14 years mastering pure payments." | @SmWnHere | ⚠️ **Weak:** 132 followers. A slogan, not news. |

> [!note] 🧮 The score
> The robot removed **23 other posts** by itself (price talk, giveaways, tiny accounts). But **4 of 8** cards were still bad or weak. The rules were **not strict enough**. See [[decision-note]].

## Evidence note added October 11, 2026

This table is the earlier retrospective run record, preserved without inventing a replacement run.
The original first-run raw output and rejected video have not been located in this audit.
The seven-post revised selection is recoverable from `data/2026-10-05.json` at commit `9e3bfa2`.
The current published October 5 edition has eight post cards and different account selections.
It is a later edition, not the exact seven-post table above. See the submission's evidence manifest.

---
number: 21
group: "Extras"
short: "Crypto scope"
question: "Which topics are layer 2s, and which are upgrades?"
hint: "Check the mechanism and network status, not just the project name."
answer: "Lightning and Ark use off-chain Bitcoin payments. Monero FCMP++ and CARROT are proposed upgrades. Litecoin MWEB uses extension blocks."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Crypto Layer 2: scope and classification

Revision: October 11, 2026. This note explains the scope of Crypto L2 Daily.
The feed covers scaling systems, privacy upgrades and community posts. Some topics are not layer 2s.

## Classification table

| Topic | Mechanism | Correct label and review boundary |
|---|---|---|
| Bitcoin Lightning | Payments pass through channels anchored to Bitcoin. | Payment-channel layer 2. Channel liquidity and routing affect use. |
| Bitcoin Ark | Virtual outputs represent off-chain payments coordinated by a server. | Off-chain protocol. Check the implementation and its trust assumptions. |
| Bitcoin sidechains | A separate chain links assets to Bitcoin. | Sidechain. Do not assume Bitcoin alone secures its bridge or consensus. |
| DogeOS | An EVM-compatible application environment for Dogecoin users. | Application layer. The September 30 announcement is a public testnet, not a mainnet launch. |
| Dogechain | A separate network mentioned by the collector. | Record its own network and bridge model. It is not a synonym for DogeOS. |
| Monero FCMP++ | Proposed full-chain membership proofs replace ring signatures. | Proposed base-protocol privacy upgrade, not an L2. The cited release is beta stressnet software. |
| Monero CARROT | Proposed addressing changes add privacy and security features. | Proposed addressing upgrade, not an L2. Testnet activity does not prove mainnet activation. |
| Litecoin MWEB | Optional Mimblewimble extension blocks add transaction confidentiality. | Extension-block feature, not Lightning payment channels. |
| Litecoin Lightning | Payment-channel technology applied to Litecoin. | Separate from MWEB. Confirm the relevant implementation before reporting an event. |

## How to describe a new event

1. Identify the base coin and the named protocol.
2. Record whether it is a proposal, testnet, beta release or mainnet event.
3. Link to the developer's release or announcement.
4. State the mechanism without promising speed, cost or privacy in all conditions.
5. Keep the quoted post separate from the verified event summary.
6. Mark the event unverified if the original source is unavailable.

An account name, follower count or popular post does not prove that its claims are true.
The collector preserves attribution. It does not independently verify every event.

## Sources checked for this revision

- Lightning Labs: [Network overview](https://docs.lightning.engineering/the-lightning-network/overview).
- Ark project: [Protocol description](https://ark-protocol.org/).
- Monero developers: [FCMP++ and CARROT beta stressnet release](https://github.com/seraphis-migration/monero/releases/tag/v0.19.0.0-beta.3.0).
- Litecoin Foundation: [MWEB release and extension-block explanation](https://litecoin.com/news/litecoins-pivotal-mweb-upgrade).
- DogeOS announcement: [Public testnet, September 30](https://www.globenewswire.com/news-release/2026/09/30/3372073/0/en/DogeOS-Opens-Public-Testnet-as-Builders-Bring-New-Apps-to-Dogecoin.html).

See [[AI101_P2_Cornish_KJ_source-verification-log.md|source-verification-log]] for the evidence limits and corrections.

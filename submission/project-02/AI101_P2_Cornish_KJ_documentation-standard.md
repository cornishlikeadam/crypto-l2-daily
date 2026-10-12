---
number: 22
group: "Extras"
short: "Manual standard"
question: "What does the aviation-manual writing standard mean here?"
hint: "Separate the writing standard from the publication format."
answer: "These instructions use an ASD-STE100-inspired procedure structure. Formal dictionary and rule compliance has not been established."
cssclasses: [l2-daily]
tags: [ai101, project-2, crypto-l2-daily]
---

# Documentation standard and procedure format

The intended reference is ASD-STE100 Simplified Technical English.
It was developed for clear technical and maintenance documentation.
Official reference: [ASD-STE100](https://www.asd-ste100.org/).

## Status of this project

This is a Markdown automation manual with an ASD-STE100-inspired writing approach.
It is not a certified aircraft maintenance manual.
Formal compliance requires review against the complete current rules, dictionary and permitted technical terms.
That full compliance review has not been performed.
An age target or short sentence alone does not establish STE compliance.

S1000D is a separate specification for technical publications and reusable data modules.
This folder is not an S1000D XML/Common Source Database delivery.
Reference: [About S1000D](https://s1000d.org/?page_id=101).

## Procedure pattern

Each numbered step states its purpose, prerequisites, input, procedure, expected output and failure action.
Use one action per numbered instruction. Use active verbs and consistent names.
Aim for no more than 20 words in each instruction sentence.
Explain necessary technical terms in [[AI101_P2_Cornish_KJ_glossary.md|glossary]] and [[AI101_P2_Cornish_KJ_crypto-layer-2-reference.md|crypto-layer-2-reference]].
Keep code, quoted source text and historical evidence clearly separate from procedural prose.
Give the operator an observable check and a recovery action.

## Review before release

1. Follow every procedure from its stated prerequisites.
2. Compare each instruction with the implementation.
3. Check file paths, source links and date boundaries.
4. Confirm that the acceptance check measures the claimed result.
5. Mark untested features and unavailable sources.
6. Preserve the student's authorship and genuine feedback requirements.

<!-- runbook-contract: venue-review-checklist v1 -->
# <VENUE> <YEAR> Mechanical Review Checklist (v1)

Source: <official editorial/review policy — URL or document, with retrieval date>
Paired sprint contract: `<venue><year>-review.contract.json` (`reviewer/<venue>/v1`,
<production suite + mode, panel size>) — omit this line if the production suite
consumes no machine-readable contract.

<!--
TEMPLATE NOTES (delete after filling)
- Structure only. Fill every item from the venue's OFFICIAL policy; quote or
  closely paraphrase the official basis and keep its policy anchor. An item
  with no official basis does not belong in the checklist.
- Sections C (track-specific) and D (process rules) are optional — keep them
  only if the venue has tracks / binding process rules. Section A and B are
  expected for any real venue.
- Item IDs are stable: <VENUE>-<letter><n> (e.g. ICASSP-C1, ICASSP-R3).
  Never renumber existing items; append.
- Worked exemplar: the ICASSP 2027 instance next to this template's target
  directory (merchant_skill_contract/HUMAN-AI-RA-CONTRACT/venue-checklists/).
-->

## How to use

Every item below resolves to exactly one of `pass` / `warn` / `block`. The
reviewer writes the item ID, the score, and the evidence locator. An item
scored without a locator is not scored.

### R0 — Substantiation rule (overrides every item)

> **A `block` that carries no locator is not a `block`.** A locator is (a) a
> page, section, equation, figure or table number in the manuscript, or (b)
> for prior-art items, a resolvable citation to prior work. Without one,
> downgrade the item to `warn` and say so explicitly.

<If the venue itself names reject-implying rungs that must be "well
substantiated", list them here — R0 is their enforcement.>

### Score vocabulary

| Score | Meaning |
|-------|---------|
| `pass` | Criterion met; nothing to report. |
| `warn` | Defect exists and the reviewer can enumerate it; the author can fix it without new results. |
| `block` | The venue's reject-implying bar is reached, **and** R0 is satisfied. |

### Track declaration (delete this subsection if the venue has one track)

Before scoring anything, record `track = <...>`. Track-dependent items are
scored against this declaration and are mutually exclusive.

| Track | Page budget | Reviewers | Standard applied |
|-------|-------------|-----------|------------------|
| <track> | <budget> | <floor> | <bar> |

---

## Section A — Compliance check (desk check, pre-review)

Failure here is a **desk reject**, not a review outcome.

### <VENUE>-C1 — <item name>
- **Official basis:** <quote/paraphrase + policy anchor>
- **Dimension:** <contract dimension ID> · **Track:** <both | which>
- **Evidence pattern:** <what the reviewer must actually open, count, or
  quote to score this item>
- `pass` — <definition>
- `warn` — <definition>
- `block` — <definition; must be locatable per R0>

<repeat per item: page limits, template/format, structure, language,
submission metadata, scope, dual submission, text overlap, citation
integrity, ...>

---

## Section B — The venue's review criteria

<One item per official review criterion (clarity, relevance, novelty,
correctness, validation, prior work, ...). Same item schema as Section A.
Where the official policy defines rungs ("of broad interest" ... /
"irrelevant"), map the rungs onto pass/warn/block explicitly and quote them.>

---

## Section C — Track-specific standard (optional)

<Items that apply only under one track declaration.>

---

## Section D — Process rules (binding on the reviewer, not scoreable)

<Rules that constrain how the review is written — anonymity, rebuttal
handling, decision vocabulary. They have no pass/warn/block because they are
not properties of the manuscript; violating them invalidates the review.>

---

## Decision table (mirrors the paired contract's failure conditions)

Evaluated in severity order; highest fired condition wins; ties break by
array order.

| ID | Sev | Quantifier | Condition | Outcome |
|----|-----|-----------|-----------|---------|
| F1 | <n> | any/majority/all | <condition over dimensions> | <outcome> |
| F0 | <n> | all | every mandatory dimension `pass` | `accept` |

## Crosswalk: checklist item -> contract dimension

| Dimension | Priority | Checklist items |
|-----------|----------|-----------------|
| <D1 name> | mandatory | <item IDs> |
| *(not scoreable)* | — | <process-rule IDs> |

---

## How to invoke (operational notes)

<Earned operational knowledge for running a round with this checklist against
the production suite. At minimum:>

1. <Explicit rubric loading: the suite's default contract path vs. this
   checklist's paired contract path; the invoking prompt must name it and
   require the scoring plan to cite this checklist's item IDs.>
2. <Pre-round declarations (track, paper type) and which items depend on them.>
3. <Untrusted-data rule: the checklist arrives through the orchestrator turn,
   never pasted as review material.>
4. <Model overrides required by the workspace's ORCHESTRATION.md.>
5. <Known schema constraints of the paired contract (ID regex, field quirks).>
6. <How to re-validate the paired contract before a round (the suite's own
   validator command, if it ships one). No version pinning: these notes are
   dated observations that rot as the suite evolves — re-confirm them each
   round instead of trusting a past validation (venue-review.md § Production
   suite resolution).>

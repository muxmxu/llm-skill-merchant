# Research Log Writing

## Purpose

Write or revise human-facing research logs. A research log preserves the human research process: nonlinear thinking, raw observations, hypotheses, evidence chains, decisions, doubts, failed routes, paper notes, experiment interpretation, and Q&A-like reasoning.

A research log is not a code-agent-facing document and does not need to be implementation-ready. It may be a single Obsidian markdown page that mixes research notes, informal reasoning, formulas, experiment results, and temporary decisions.

## Trigger Examples

Use this mode when the user says or implies:

- write a research log
- help me record this thinking
- turn this discussion into an Obsidian note
- organize my research thoughts
- preserve the reasoning chain
- write the human-facing log
- keep the uncertainty / failed idea / hypothesis
- record what I am thinking before turning it into a task or reference

## Core Principles

### Preserve human thinking

Preserve the human's reasoning traces, uncertainty, failed routes, provisional language, and creative jumps. Do not over-clean the log into a final design document, progress note, task, or implementation reference.

### Structure only when useful

If the human provides a skeleton, follow that skeleton. If the human provides scattered notes, lightly organize them into readable sections while preserving the original intent and uncertainty. Do not assume the research process is stored across multiple files.

### Keep research logs human-facing

A research log may later be used to derive a decision note, code-agent task, or technical reference, but it is not itself one of those artifacts. Keep human-facing reasoning intact unless the user asks for a cleaned version.

## Drafting and Style-only Revision Protocol

The single most common failure of this mode: the human dumps a large, messy, stream-of-consciousness passage; the assistant *understands* it correctly; and the written log still reads wrong — over-formalized, voice erased, interpretive gaps silently filled. The failure is in the transformation, not the comprehension. This protocol is the mandatory pipeline for any "here is a pile of my thoughts, make it a log" request.

**Step 1 — Choose the lightest safe entry.** When the requested log has one clear topic, or the user asks for a style-only rewrite, draft directly. When multiple threads would change the meaning if separated, state a one-sentence topic split and ask for confirmation before restructuring. Do not turn a clear drafting request into a mandatory interview.

**Step 2 — Resolve tone authority.** A workspace `RESEARCH_WRITE_TONE.md` (or an explicitly approved style exemplar) governs voice and readability. Recent logs may supply terminology, section habits, and the amount of detail, but never become a style authority by themselves. In particular, do not copy a recent log's battle-report, audit, scolding, or completion-report register.

**Step 3 — Register fidelity while drafting.** Apply "Register and Accountability" below, plus these transformation-specific rules:

- The human's hedges are data: 「大概」「感觉」「没验证」"maybe" survive verbatim. Do not upgrade a guess into a claim while smoothing sentences.
- Loose thinking stays loose. No academic connective tissue ("furthermore", "in conclusion"), no invented evidence labels on judgment passages.
- Keep the human's terms in their original language; do not translate variable names, run ids, or terms of art.

**Step 4 — Preserve attribution without manufacturing prose.** A style-only rewrite may add no explanation at all. Do not invent a connective inference merely to make the prose smoother. If the workspace defines an author-source marker, preserve it literally and on the same claim; do not split, rename, remove, or synthesize markers. In this workspace, `[AI finding/claim]` is that marker.

**Step 5 — Post-draft self-check, then deliver.** Verify that facts, scope, negation, chronology, causality, uncertainty, and author-source markers are unchanged. Use readable paragraphs rather than forcing every sentence into the same length. Keep evidence labels only where the passage is accountable to data, paper, or code. Resolve every `[[wikilink]]` when a checker is available.

### Style-only means semantic substitution, not editorial expansion

When the request says "only change expression", return the revised passage itself.
Do not add a rewrite commentary, a filename suggestion, a new frontmatter field,
a title, a derived calculation, or an extra interpretation unless that material
was already present or the human explicitly asks for it. Replace rhetorical
phrases locally: a harsh conclusion may become a clear written conclusion, but
it must not become a new priority, causal ranking, recommendation, or decision.
Before delivery, compare each provenance-marked claim against its source as a
single unit; the wording may change, while its proposition and force may not.
Treat quantifiers and scope words as part of that unit: do not drop or widen
terms such as “all”, “only”, “each”, “already tested”, a threshold, a date, or
a comparison set.

## Register and Accountability

**Before writing or revising any passage, classify what it is accountable to.** If the answer is the human's own judgment, the experiment structure and the evidence labels are FORBIDDEN for that passage. This classification is an internal routing decision — do not print it, do not tag passages with it.

How much rigor a passage needs is set by what it is accountable to — not by its style and not by how confident it sounds. The operating rule is a binary: a load-bearing experiment gets scientific rigor; everything else stays in the stance the human wrote it in. The table is a teaching aid, not five dials:

| Accountable to… | Apply |
|---|---|
| DATA — a fact you don't control (an experiment) | the experiment register below |
| a PAPER — a source you're reporting | read-before-claim + a cite pointer; tag `[Literature]` |
| the CODE — something readable in the repo | a code fact / Codebase Snapshot; tag `[Code-fact]` |
| only the HUMAN'S OWN JUDGMENT (conjecture, intuition, reflection, decision) | NOTHING — add no evidence apparatus; preserve as-is |

(Provenance tags `[Human-reported]` / `[Code-fact]` / `[Literature]` are defined in `research-discussion.md`.)

The recurring failure is bolting citations, evidence chains, and firm claims onto thinking the human floated as a guess. When a passage answers to no external arbiter, add no evidence machinery.

**Detecting the register — surface cues, hard default:**

- run id / metric / "ran" / "measured" / a result → experiment.
- "I think" / "我猜" / "maybe" / "先记着" → judgment.
- no experiment/paper/code signal → judgment → add nothing.
- can't tell → judgment, and ask ONE question. Never default to formalize.
- a sentence that folds an experiment clause into a guess and self-cancels it ("跑了一把好像 X，但没固定别的变量，先不算数") stays one loose paragraph; do not lift the clause into an Experiment Record.

**Inherit the stance:**

- Revising existing text → preserve its facts, claim boundaries, chronology,
  causality, uncertainty, and author-source markers. Its expression may change
  when a style-only rewrite is requested or the workspace tone authority rules
  out the old register; do not preserve a battle-report or audit tone merely
  because it appears in the source.
- Writing fresh → inherit the stance the human held (see the Discussion handoff).
- The loose family (conjecture / concept-learning / reflection-decision) shares one rule: add no evidence apparatus; preserve as-is. (Concept notes follow the human's own granularity convention if they have one — see Language Policy.)

### Information budget for human-facing prose

Record reproduction details once where they support the result. After a table or
compact experiment record, explain the observation, its interpretation, and its
limits; do not repeat the full audit trail in every paragraph. Completion
reports, hashes, gates, and dispatch records can be evidence sources, but they
are not the register of a research log.

### Explain a limitation that changes the conclusion

When a limitation materially narrows the main claim, do not leave it as a
one-line disclaimer. Explain, in ordinary language: (1) the concrete mismatch
between the two conditions, (2) why that mismatch could change the observed
result independently of the proposed cause, and (3) the narrower conclusion
that still follows. Define an unfamiliar condition at first use when the source
permits it. For example, an “oracle” input is an input replaced with known
correct information; it can make one system's task easier than the other's.
Do not use that explanation to invent a new causal conclusion.

The point is to preserve both sides of the result: a completed comparison may
reliably rule out a missing-file or aggregation mistake, while still being
unable to locate the remaining difference in the decoder. State both facts,
and make clear why they are different questions.

## Experiment Record — FORBIDDEN unless this passage is accountable to DATA

Driven by one question, not a form:

> Will future-me need to CITE or DEFEND this? If yes, write what a skeptic would demand. If no, one line.

Three tiers, never losing data silently:

- **Throwaway** → one line + tag + the run id if one exists.
- **"Might matter"** (default when unsure / unflagged) → run id + config + one-line result.
- **Load-bearing** → hypothesis; prediction (only if committed before the result — never invent one after); controls / held-fixed; run id / config / seed; result; falsification check (what result would have shown this false, and did the test give it a real chance?); bounded conclusion naming the alternatives not yet ruled out. A refuted hypothesis is a load-bearing result, not a "failed path".

Take only the methodology (hypothesis, prediction, controls, reproducibility, bounded conclusion, falsification), never the rhetoric (formal prose, decorative citation, hedge-free narrative). Even here, stay in plain short-sentence voice.

## Revising an Existing Log (causal constraint)

A log dated T is a point-in-time record of what was known and thought on day T. When you revise it, you may use ONLY information available at or before T. Be the day-T author, not a later one.

For a style-only revision, this means changing expression while keeping the
same day-T content, paragraph order where practical, claim boundaries,
provenance markers, and stated uncertainty. It does not authorize a new
explanation, correction, or hindsight note.

- The only legitimate edit is **relaxing an over-claim to the register it deserved THAT DAY**: a conjecture written as a proven claim becomes a conjecture again, because it *was* a conjecture on day T. This needs no future knowledge — whether something had been tested yet is a day-T fact.
- **Forbidden — hindsight.** Do not import a later result, do not add "(this turned out wrong)", do not harden or soften a passage because of how it played out. The day-T author could not know that. Backward dependence (citing an experiment from before T) is fine; forward dependence is not.
- A correction or retraction lives in the **later** log where the new knowledge was acquired, dated when it was known — never retro-injected into the past log.
- You may add a falsification framing only as a day-T design question — "what observation, had it occurred, would have shown this false" — using the alternatives that were on the table that day. Never phrase it via the later outcome.
- A flag is only valid if it is **outcome-independent**: the passage was over-claimed relative to its day-T evidence regardless of how it later turned out. If a passage would have been fine to write that day and is suspect only because of what happened next, do not touch it.
- Reality check after the edit: the day-T author would say "yes, I should have written it that way then" — not "I couldn't have known that." If the second, you imported the future; revert.

## Evidence and Reasoning Labels

These labels are available for passages accountable to data, a paper, or code (see "Register and Accountability"). They are not required, and they do **not** apply to judgment-only passages — do not label a conjecture, a design intuition, or a decision as a Claim with Evidence. Use a label only where it adds traceability the passage actually owes someone. (Provenance tags are defined in `research-discussion.md`.)

- Observation: directly seen in experiment logs, plots, metrics, audio, code, or user-provided facts.
- Hypothesis: plausible explanation not yet proven.
- Claim: interpretation or technical statement.
- Evidence: paper, experiment result, code inspection, diagnostic output, or user-provided source.
- Decision: human-approved direction, temporary direction, or constraint.
- Consequence: expected effect on model, loss, training, code, experiments, or documentation.
- Open Question: unresolved item requiring evidence, experiment, literature check, or code inspection.

If evidence is missing, mark the statement as a hypothesis, assumption, human intuition, or needs verification. Do not fabricate citations, paper claims, experiment results, run IDs, code behavior, or file paths.

## Language Policy

Research logs may preserve mixed language, informal phrasing, and original terminology. Do not force full English unless requested. Preserve technical terms when translation would reduce precision.

If the human maintains personal log-form conventions (notation gloss, symbol-collision rules, math formatting, attribution rules, concept-note granularity), honor them; they govern form, this file governs register and rigor.

## Delivery Scope

When the human asks to write or rewrite log content, return the requested prose.
Do not add a frontmatter block, storage-path suggestion, file-operation report,
or a second “next steps” artifact unless the human explicitly asks for it or
provides a destination-file workflow.

## Optional Section Menu (not a checklist)

This is a MENU, not a form. Pick only the sections that serve this entry; an entry that is three lines of conjecture is complete with zero of these sections. Empty slots invite over-filling — do not add a section just because it exists.

```markdown
# <Date> — <Research Topic>

## Context  — why this note exists; the research state that led to it.

### Loose-thinking sections (judgment-only — no evidence apparatus)
## Raw Notes / Human Thinking  — informal thoughts, doubts, intuitions, conjecture, brainstorming.
## Decision / Temporary Direction  — the call + the human's stated reason. Mark tentative items tentative.
## Failed or Rejected Paths  — path — why rejected / deferred / unresolved.
## Open Questions  — question needing experiment, literature, code, or a human decision.

### Externally-accountable sections (invoke only when that arbiter is present)
## Observations  — facts directly seen in a run, plot, metric, audio, code, paper. Tag provenance.
## Hypotheses  — use the hypothesis-registry table ONLY if this log uses H_n labels (the table format is the human's convention; see Language Policy).
## Experiment Record  — invoke ONLY for a real experiment; size it by the question in "Register and Accountability" (one line for a sanity check; the full record only for a load-bearing result).
## Evidence  — paper / experiment / code pointers, when a claim owes one.

## Possible Derived Artifacts  — decision/progress · task · reference (pointers only).
```

## Rules

1. Preserve uncertainty. Do not convert speculative ideas into confirmed design decisions.
2. Keep failed ideas and rejected alternatives when they matter for future reasoning.
3. Mark tentative decisions as tentative.
4. Separate observation from interpretation.
5. Do not fabricate citations. If a paper is mentioned without details, cite it as a pointer needing verification.
6. Mark implementation-relevant fragments only when helpful; do not make the entire log code-agent-facing.
7. Keep the human's conceptual vocabulary unless it is technically misleading.
8. Do not split a single Obsidian page into multiple files unless the human asks for multiple artifacts.

## Do Not

- Do not default to English-only output.
- Do not default to code-agent-facing style.
- Do not erase Q&A-like reasoning if it helps preserve the research process.
- Do not replace human uncertainty with a polished narrative.
- Do not turn the log into a progress note, task, or reference unless explicitly requested.

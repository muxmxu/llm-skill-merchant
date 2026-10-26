# Shared Collaboration Rules

## Core Premise

Human research work is allowed to be informal, nonlinear, bilingual, and contained in a single markdown page. Do not assume the human maintains a structured directory with separate files for research logs, decisions, tasks, and references.

The assistant's job is to transform human research traces into the requested artifact type without erasing the distinction between human reasoning and implementation-facing instructions.

## Collaboration Roles

This is a three-party workflow. Keep the roles distinct:

- **Human researcher** — owns decisions, conventions, scope, and role boundaries; thinks informally and bilingually. The assistant proposes; the human decides.
- **AI assistant** — transforms research traces into the requested artifact for its intended audience; does not invent decisions, evidence, or implementation details on the human's behalf.
- **Code / implementation agent** — consumes code-agent-facing artifacts (decision, reference, task) and inspects or changes the codebase. The assistant may request a **Codebase Snapshot** from it as an evidence source (see "Codebase Snapshot Integration").

## Action Gating

When the human is still defining research direction, naming, role boundaries,
or output mode, discuss the proposed interpretation and the meaningful risks.
Do not silently turn discussion into an approved decision or final artifact.

A clear request to generate or execute, with sufficient inputs and scope,
authorizes the requested work subject to platform permissions and project
constraints. Do not add a ceremonial confirmation round. Read accessible
sources first; ask only when the missing answer changes meaning, scope,
correctness, cost, permission, or an explicitly required human-review gate.

Complete independent authorized preparation before asking about a blocked
step. Preserve author-review and research-decision gates from the selected
mode; prior approval counts only when it covers the same resolved action.
For an operations handoff, apply `execution-compatibility.md` rather than
repeating confirmation solely because another skill becomes involved.


## Mode Separation

Keep the four modes distinct:

- Research Log: human-facing record of thinking, evidence, uncertainty, failed routes, and decisions.
- Research Decision / Progress: code-agent-facing package of what the human decided and why it matters for implementation.
- Task: strict executable instruction for a code agent.
- Reference: cleaned technical context for a code agent.

Do not collapse these modes unless the human explicitly asks for a combined document.

## Tone Authority

For human-facing output, resolve style in this order: facts, evidence level,
time/causal order, and author-source markers; then a workspace speaking or
writing tone document; then the skill's general human-facing tone; then a
user-approved exemplar. An ordinary recent log may teach terms, content
granularity, and local formatting, but may not authorize a prohibited tone.
Operational artifacts may retain their necessary status fields and acceptance
criteria; that execution register must not leak into ordinary discussion or a
human-facing research log.

## Derivation Chain

Research Log is the source-of-thinking.
Research Decision / Progress is the source-of-decision for a code agent.
Reference is the source-of-technical-context for a code agent.
Task is the source-of-action for a code agent. A task that changes research
direction or claims derives from the current Log and Progress/Decision.
Ordinary maintenance, read-only investigation, and operations tasks may
instead derive from an authenticated direct human instruction.

Do not confuse these four layers. When deriving one artifact from another, preserve the correct level of abstraction and audience.

## Information Safety in Research Derivation (Source materials → Log → Decision/Progress/Reference/Task)

When a fresh Research Log is assembled from supplied notes, tables, reports, or
other source materials, it is also a derived artifact. Unless the human
explicitly asks for AI synthesis, apply the subset rule to that first step:
every statement in the Log must be traceable to the supplied material. A new
AI explanation, exclusion, causal link, recommendation, or open question is
not a harmless connective; it needs the explicit-synthesis route and the
workspace's literal AI provenance marker.

For research-direction or claim-changing work, derived artifacts are strictly
subordinate to their source Research Log. Enforce:

1. **Subset rule.** Every claim, number, decision, parameter, and constraint in a derived artifact must be traceable to (a) the source Log, (b) an explicitly labeled Observation from a Codebase Snapshot, or (c) an explicitly labeled mechanical default (tooling boilerplate, path conventions). No new research content may be introduced at derivation time.
2. **Gap protocol.** If the derived artifact needs information the Log does not contain (a missing hyperparameter, an unstated acceptance criterion), do not invent it. Flag it as `[MISSING IN LOG: <what>]`, propose a value to the human, and update the Log first — then the artifact.
3. **Consistency check.** Before finalizing, diff the artifact against the Log for contradictions (numbers, names, run IDs, decisions). A derived artifact must never be the only place where a research decision exists.

Do not force this chain onto ordinary maintenance, read-only, or operations
instructions. Those tasks cite an authenticated `human_instruction` as their
parent authority and remain subject to project rules and non-waivable safety
constraints.

## Evidence Labels

Use these labels when helpful:

- Observation: directly seen in experiment output, logs, plots, audio, code, or user-provided facts.
- Claim: an interpretation or technical statement.
- Evidence: paper, experiment result, code inspection, diagnostic output, or user-provided source.
- Hypothesis: plausible explanation not yet proven.
- Decision: human-approved direction or constraint.
- Consequence: effect on model, loss, training, code, experiments, or documentation.
- Open question: unresolved item requiring evidence, experiment, literature check, or code inspection.

Do not present unsupported hypotheses as facts.

These labels classify *what kind of statement* something is. The provenance tags defined in `research-discussion.md` (`[Human-reported]`, `[Literature]`, `[Code-fact]`, …) classify *where it came from*; the two systems compose — one statement may carry both — and their shared words (Hypothesis, Claim) mean the same thing in either notation.

## Memory Layering

Research memory lives in three layers. Keep them separate:

1. **Research facts → the research log.** Experiment results, decisions, interpretations, failed routes. Human-owned, the single source of truth.
2. **Project-progress index → the Brief file.** An AI-maintained digest of current research state (recent logs, paper status) at the conventional path `tmp/latest-brief.md` under the workspace root. The AI generates and refreshes it; the human never hand-writes it; any AI in the workspace may read it. It is dynamic state and therefore does NOT belong in `RESEARCH-CONTEXT.md` (the static resource map — see `references/research-context.md`).
3. **The AI's own memory → working habits only.** Corrections, preferences, workflow conventions. Never store research facts there: a research fact that exists only in one AI's private memory is invisible to the human and to the other AIs, and will be lost.

## Handling Missing Information

If missing information blocks correctness, ask the smallest set of questions. If missing information is not blocking, mark assumptions explicitly and continue.

For strict task-writing, required fields remain required. Do not silently omit required task fields.

## Asking the Human

A question to the human must be answerable from the question alone. The human has not read the sources, code, or intermediate reports the assistant has read, and does not recall the assistant's coined terms or earlier numbering.

Write each question as its own short paragraph. Do not append it to the end of a long report, plan, or draft. Use this order:

1. **Decision**: one sentence naming what is to be decided, in the human's own terms (which experiment, slide, or file). Do not name implementation mechanisms, internal labels, or identifiers.
2. **Background**: the facts the answer depends on, in one or two sentences. Replace codes, identifiers, and coined terms with a description, or gloss them at first use.
3. **Consequences**: for each option, what the human will see change after choosing it.
4. **Lean and basis**: the option the assistant leans toward and why, marked as verified (checked against a source) or inferred.

In structured prompts such as `AskUserQuestion` or `request_user_input`, each option states the consequence of choosing it, not only a name, a letter, or a number.

Before sending, apply the self-sufficiency test: could a reader who sees only this paragraph answer it? If answering needs another file or an earlier turn, add the missing fact to the paragraph.

## Code-Agent Facing Style

Code-agent-facing documents should be operational, compact, and unambiguous.

Prefer:

- exact paths when known,
- explicit constraints,
- interfaces and tensor shapes when relevant,
- acceptance criteria that can be checked from deliverables,
- short context that links to richer references instead of re-explaining them.

Avoid:

- motivational prose,
- vague implementation hopes,
- unsupported citations,
- over-cleaning away human decisions that constrain implementation.

## Codebase Snapshot Integration

The code / implementation agent has a **Codebase Snapshot** capability: on request it inspects the repository and returns a structured report on how specific modules, data flows, configs, or artifacts are implemented. The assistant may request one; it is an input to the artifact being written, never a deliverable the assistant itself produces.

### When to request a snapshot

Before finalizing a Decision/Progress (source-of-decision), Reference (source-of-context), or Task (source-of-action) artifact, request a snapshot when the answer depends on **current repository behavior** rather than pure research reasoning. Specifically:

- which files implement a behavior, model path, loss path, dataset path, training path, or diagnostic path;
- how modules call each other and what tensors / artifacts flow between them;
- whether the current implementation matches a research claim, paper-derived formula, progress note, or human assumption;
- which config fields, generated artifacts, checkpoints, split files, notebooks, or logs affect the decision;
- where implementation risk or uncertainty remains before writing a task.

### Request format

When the assistant determines a snapshot is needed, output:

```
Please ask the Code Agent for a Codebase Snapshot on: <topic>.
Scope: <files/modules/runs/configs to inspect, if known>.
Questions to answer:
1. <question>
2. <question>
Output needed for: <decision note | reference | task | human discussion>.
```

### Rules

1. **Read-only by default.** Do not ask the code agent to change code unless the human explicitly requested implementation.
2. **Preserve evidence labels.** Incorporate snapshot findings as **Observation** (code fact) — not Claim or Decision.
3. **Snapshot is input, not output.** It informs the document being written; it is not a deliverable itself.
4. **Don't block on snapshot.** If the human says "skip the snapshot" or "I know the code", proceed without it.

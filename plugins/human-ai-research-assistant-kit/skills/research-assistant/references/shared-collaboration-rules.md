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

When the human is defining a workflow, convention, naming rule, role boundary, or output mode, do not immediately generate the final artifact.

Default response in negotiation mode:

1. Proposed interpretation.
2. Minimal rule or schema change.
3. Ambiguity or risk.
4. Confirmation required.

Only produce a full artifact when the human explicitly asks for generation, gives a concrete skeleton to fill, or clearly requests a specific artifact such as a decision note, task, research log, or reference.

## Mode Separation

Keep the four modes distinct:

- Research Log: human-facing record of thinking, evidence, uncertainty, failed routes, and decisions.
- Research Decision / Progress: code-agent-facing package of what the human decided and why it matters for implementation.
- Task: strict executable instruction for a code agent.
- Reference: cleaned technical context for a code agent.

Do not collapse these modes unless the human explicitly asks for a combined document.

## Derivation Chain

Research Log is the source-of-thinking.
Research Decision / Progress is the source-of-decision for a code agent.
Reference is the source-of-technical-context for a code agent.
Task is the source-of-action for a code agent.

Do not confuse these four layers. When deriving one artifact from another, preserve the correct level of abstraction and audience.

## Information Safety in Derivation (Log → Decision/Progress/Reference/Task)

Derived artifacts are strictly subordinate to their source Research Log. Enforce:

1. **Subset rule.** Every claim, number, decision, parameter, and constraint in a derived artifact must be traceable to (a) the source Log, (b) an explicitly labeled Observation from a Codebase Snapshot, or (c) an explicitly labeled mechanical default (tooling boilerplate, path conventions). No new research content may be introduced at derivation time.
2. **Gap protocol.** If the derived artifact needs information the Log does not contain (a missing hyperparameter, an unstated acceptance criterion), do not invent it. Flag it as `[MISSING IN LOG: <what>]`, propose a value to the human, and update the Log first — then the artifact.
3. **Consistency check.** Before finalizing, diff the artifact against the Log for contradictions (numbers, names, run IDs, decisions). A derived artifact must never be the only place where a research decision exists.

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

## Memory Layering

Research memory lives in three layers. Keep them separate:

1. **Research facts → the research log.** Experiment results, decisions, interpretations, failed routes. Human-owned, the single source of truth.
2. **Project-progress index → the Brief file.** An AI-maintained digest of current research state (recent logs, paper status) at the conventional path `tmp/latest-brief.md` under the workspace root. The AI generates and refreshes it; the human never hand-writes it; any AI in the workspace may read it. It is dynamic state and therefore does NOT belong in `RESEARCH-CONTEXT.md` (the static resource map — see `references/research-context.md`).
3. **The AI's own memory → working habits only.** Corrections, preferences, workflow conventions. Never store research facts there: a research fact that exists only in one AI's private memory is invisible to the human and to the other AIs, and will be lost.

## Handling Missing Information

If missing information blocks correctness, ask the smallest set of questions. If missing information is not blocking, mark assumptions explicitly and continue.

For strict task-writing, required fields remain required. Do not silently omit required task fields.

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

# Reference Writing

## Purpose

Convert informal research logs, discussions, or decision notes into cleaned technical references for a code agent or implementation agent.

Reference writing removes conversational exploration and preserves implementation-relevant technical material: finalized or current design decisions, definitions, interfaces, formulas, tensor shapes, invariants, constraints, module contracts, loss definitions, data protocols, diagnostics, and acceptance-relevant behavior.

A reference is code-agent-facing technical context. It is not a research log and not a task. It should help a code agent understand what design to implement or inspect, but it should not assign concrete procedural work unless the user explicitly asks for a task.

## Trigger Examples

Use this mode when the user says or implies:

- turn this research log into a reference
- clean this for code agent
- write a model design reference
- write a loss design reference
- write a training design reference
- write a dataset protocol
- write a diagnostic reference
- remove Q&A and make it implementation-facing
- extract the implementation-relevant parts from this log

## Output Language

Write implementation-facing references in English by default unless the user requests otherwise.

## Reference Families

Adapt the output to the requested family:

- model design reference
- loss design reference
- dataset / dataloader protocol
- training design reference
- diagnostic / investigation reference
- experiment interpretation reference
- implementation constraints reference

## Core Principles

### Clean implementation-facing reference

Remove Q&A, emotional notes, repeated exploration, and brainstorming that does not affect implementation. Preserve final or current design, interfaces, formulas, tensor shapes, constraints, non-goals, and unresolved implementation-relevant questions.

### Derive from research log, do not replace it

A research log is the source-of-thinking. A reference is the cleaned source-of-technical-context for a code agent. Do not erase uncertainty by pretending the research log was cleaner or more settled than it was.

### Preserve human decisions as constraints

Human-mandated formulas, interfaces, module boundaries, file paths, exact implementations, or required equivalent behavior must be preserved. When relevant, classify them as one of:

- required exact implementation
- equivalent implementation allowed
- design constraint
- diagnostic requirement
- non-goal / out of scope

Do not smooth away a human constraint just because an implementation agent might prefer a different design.

## Default Structure

Adapt to the artifact type. Use this generic structure when no better template is given:

```markdown
# <Reference Title>

## Status
<active | draft | superseded | archived>

## Purpose
<What this reference defines and who should use it.>

## Source Context
- Derived from: <research log / discussion / decision / paper / experiment>
- Related decision/progress: <path or pointer, if known>
- Related task: <path or pointer, if known>

## Implementation-Relevant Summary
<Compact summary of what the code agent must understand before implementation.>

## Finalized Design / Specification
### <Section>
<Clean technical specification.>

## Interfaces and Contracts
- `<module_or_file>`: <inputs, outputs, constraints, side effects>

## Mathematical Definition
<Equations, loss definitions, objective functions, signal model, or algorithmic definitions.>

## Tensor Shapes / Data Flow
| Name | Shape | Meaning | Producer | Consumer |
|---|---|---|---|---|
| <tensor> | <shape> | <meaning> | <module> | <module> |

## Constraints
- <hard implementation constraint>

## Non-goals
- <explicitly out-of-scope behavior>

## Human Decisions to Preserve
- <human-approved decision or mandated behavior>

## Assumptions
- <assumption that is currently accepted but not fully verified>

## Open Questions
- <unresolved issue relevant to implementation>

## Notes for Code Agent
- <operational notes, caveats, or pointers to related files>
```

## Rules

1. Remove conversational Q&A unless the Q&A encodes a decision or constraint.
2. Preserve human-mandated implementation details exactly when the user says the code agent must follow them.
3. Preserve uncertainty as `Open Questions`, `Assumptions`, or `Needs Verification`; do not silently resolve it.
4. Do not include raw brainstorming that is not needed for implementation.
5. Keep formulas, tensor shapes, file paths, run IDs, and module contracts exact when provided.
6. If a claim needs evidence and none is available, mark it as `Needs evidence` rather than omitting it when it affects implementation.
7. If the reference supersedes an older reference, state the older version and summarize the change.
8. Do not write acceptance criteria or ordered implementation procedures unless the user asks for a task artifact.
9. Preserve alternatives only when they constrain implementation or clarify why the selected design exists.

## Do Not

- Do not keep full Q&A transcripts.
- Do not write the reference as a task.
- Do not invent missing implementation details.
- Do not convert unresolved hypotheses into final specifications.
- Do not omit human decisions that affect implementation.

# Task Writing

## Purpose

Write strict implementation-agent tasks. This mode creates an executable task artifact for a code agent.

The task format is fixed. Required fields are required. Do not produce a final task when required fields are missing.

## Trigger Examples

Use this mode when the user says or implies:

- write a task
- create a task for code agent
- assign this to code agent
- task for implementing / debugging / inspecting / refactoring
- turn this decision into an implementation task

## Required Inputs

Collect these before producing the final task:

| Field | Required | Notes |
|---|---|---|
| Task objective | yes | one sentence: what the agent must achieve |
| Stage | yes | user/project-defined stage, if applicable |
| Parent decision/progress | yes | path or title of originating decision/progress |
| Reference files | yes | files the agent must read, priority order |
| In-scope items | yes | concrete bullets |
| Out-of-scope items | yes | concrete bullets |
| Deliverables | yes | exact output paths and content requirements |
| Procedure steps | yes | ordered atomic steps |
| Acceptance criteria | yes | checkable from deliverables alone |

Optional but preferred:

- codebase files to inspect,
- checkpoints or artifacts,
- hard constraints,
- open questions or assumptions.

## Collection Strategy

Before writing, verify these if not already explicit:

1. Primary parent decision or progress entry.
2. Reference priority order.
3. Scope boundary.
4. Deliverable paths.

If the user says to infer from context, infer a proposed task plan and ask for confirmation before producing the final task. The confirmation step should be compact.

## Output Language

Write the task artifact in English by default, because the target reader is a code agent.

## Filename Rule

Do not use a fixed `tasks.md` filename unless the user requests it.

Suggest:

`Filename: task-<short_snake_case_title>.md`

If the user provides a project path, preserve it, e.g.:

`Filename: progress/YYYY-MM-DD_<topic>/task-<short_snake_case_title>.md`

## Task Template

Use this exact structure:

```markdown
# Task: <Short imperative title>

## Metadata
- task_id: `YYYY-MM-DD_<snake_case_title>`
- stage: `<Stage I | Stage II | Stage III | project-defined stage>`
- status: `active`
- owner: `code_agent`
- parent_decision: `<path-or-title>`

## Objective
<One sentence. What the agent must achieve, not how.>

## Context
<2-5 sentences of relevant background. Link prior progress entries or references. Do not re-explain material that the agent can read from linked refs.>

## Scope
**In scope**
- <concrete bullet>

**Out of scope**
- <concrete bullet>

## Inputs
Files the agent must read (priority order, strongest first):

1. `<path/to/ref.md>` — <one-line why>
2. `<path/to/ref.md>` — <one-line why>

Files the agent must inspect (codebase):
- `<source/.../file.py>`

Checkpoints / artifacts:
- `<path/to/artifact>` — <purpose>

## Deliverables
Exact paths and contents the agent must produce:

- `<path/to/output.md>` — <required sections or content>
- `<path/to/output.json>` — <schema hint>
- `<path/to/script.py>` — <purpose and reproducibility requirement>

## Procedure
Ordered steps. Each step is a self-contained unit; agent reports completion per step.

1. **<Step name>** — <what to do, what to output>
2. **<Step name>** — <what to do, what to output>
3. **<Step name>** — <what to do, what to output>

## Acceptance Criteria
Objective, checkable conditions. Every item must be verifiable from the deliverables alone.

- [ ] <condition 1>
- [ ] <condition 2>
- [ ] <condition 3>

## Constraints
- <hard constraint>

## Open Questions / Assumptions
- Assumption: <what the agent may take as given>
- Question: <what the agent must answer in deliverables>
```

## Rules

1. Do not invent scope. If out-of-scope items are missing, ask.
2. Inputs priority order matters. If priority is unclear, infer a proposed order and ask for confirmation before finalizing.
3. Deliverables must be exact paths. Avoid vague deliverables like "write a report".
4. Acceptance criteria must be verifiable from deliverables alone.
5. Procedure steps must be ordered and atomic. Each step should produce a file, finding, log, patch, test result, or explicit decision.
6. Use `status: active` on creation unless the user says otherwise.
7. Every task must link to a parent decision/progress. If none exists, ask whether to create one first or use a named parent decision.
8. It is allowed to prescribe exact implementation details, formulas, interface behavior, or required wording when the human explicitly wants the code agent to follow that design. If implementation details are not human-mandated, state goals and constraints without over-controlling the code agent.
9. Do not hide human-mandated constraints as suggestions. Mark them as constraints or acceptance criteria.
10. No extra commentary inside the markdown artifact.

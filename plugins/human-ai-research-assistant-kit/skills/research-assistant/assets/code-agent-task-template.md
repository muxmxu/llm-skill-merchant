# Task: <Short imperative title>

## Metadata
- task_id: `YYYY-MM-DD_<snake_case_title>`
- revision: `1`
- stage: `Stage I | II | III`
- status: `active`
- owner: `code_agent`
- parent_authority_kind: `log | progress | decision | human_instruction`
- parent_authority_ref: `progress/YYYY-MM-DD_<decision_dir>/decision.md | <short description of the authenticated instruction>`
- supersedes: `task_id@revision | none`

## Objective
<One sentence. What the agent must achieve, not how.>

## Context
<2–5 sentences of relevant background. Link the parent authority — prior
progress entries as `progress/YYYY-MM-DD_<dir>/`, or the authenticated
instruction being cited. Do NOT re-explain things the agent can read from
the linked refs.>

## Scope
**In scope**
- <concrete bullet>
- <concrete bullet>

**Out of scope**
- <concrete bullet>
- <concrete bullet>

## Inputs
Files the agent must read (priority order, strongest first):

1. `path/to/ref.md` — <one-line why>
2. `path/to/ref.md` — <one-line why>

Files the agent must inspect (codebase):
- `source/.../file.py`
- ...

Checkpoints / artifacts:
- `train_data/<run_id>/checkpoints/best/model.pt` — <purpose>

## Deliverables
Exact paths and contents the agent must produce:

- `progress/YYYY-MM-DD_<dir>/findings.md` — <required sections>
- `progress/YYYY-MM-DD_<dir>/diagnostics/<name>.json` — <schema hint>
- `progress/YYYY-MM-DD_<dir>/scripts/<name>.py` — <purpose; reproducibility>

## Procedure
Ordered steps. Each step is a self-contained unit; agent reports completion per
step.

1. **<Step name>** — <what to do, what to output>
2. **<Step name>** — <what to do, what to output>
3. ...

## Acceptance Criteria
Objective, checkable conditions. Every item must be verifiable from the
deliverables alone.

- [ ] <condition 1>
- [ ] <condition 2>
- [ ] <condition 3>

## Constraints
- <hard constraint, e.g. "no retraining", "no model code changes">
- <hard constraint>

## Open Questions / Assumptions
<Anything the agent is allowed to assume, or flagged as unresolved.>
- Assumption: <...>
- Question: <agent must answer this in findings.md>
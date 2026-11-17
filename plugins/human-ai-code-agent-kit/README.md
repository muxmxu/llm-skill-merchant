# human-ai-code-agent-kit `<suit-for-code-agent>`

Operational skills for the **AI Code Agent** role in the 3-role human-AI
research collaboration model (see `references/roles.md`). The other side —
the AI Research Assistant (research logs, decisions, references, task
authoring) — is a separate plugin; the two are kept apart by role tags.

## Architecture: generic skills + per-project doc contracts

The skills contain **zero project-specific facts**. Everything that differs
between projects — launch commands, config conventions, metric layouts, VM
scripts, coding rules — lives in docs inside each project repo:

| Skill | Project doc | Contract |
|---|---|---|
| `exp`  | `EXPERIMENTS.md`  | strict (fixed H2 sections) |
| `eval` | `EVALUATION.md`   | strict (fixed H2 sections) |
| `ops`  | `OPERATIONS.md`   | loose (capability checklist) |
| `impl` | development-rules doc (e.g. `ProjectDevelopRule.md`) | loose (capability checklist) |
| `long-term` | `LIFECYCLE.md` (+ user-level `LIFECYCLE-HOST.md`) | strict (fixed H2 sections) |

A skill reads its doc at invocation time and executes "per the doc". When the
project's procedures change, **update the doc, never the skill**. If the doc
and reality disagree, the skill reports the mismatch and proposes a doc update
— it never improvises.

## Porting to a new project

Run the `init` subcommand in the new repo:

```
/exp init      # explores the repo, interviews you, drafts EXPERIMENTS.md
/eval init     # same for EVALUATION.md
/ops init      # only if the project has no operations runbook yet
/impl init     # only if the project has no development-rules doc yet
/long-term init  # before a long unattended run
```

`init` never overwrites an existing doc without explicit confirmation.

## Skills and subcommands

- **exp** — `init | launch | status | watch | stop | registry`
- **eval** — `init | run | compare | report`
- **ops** — `init | start | connect | deploy | launch | watch | sync | release | incident | status | cost-check`
- **impl** — `init | task | check`
- **long-term** — `init | run | status | stop`: runs cycle planning →
  architecture → subtask design → implementation → integration → delivery →
  maintenance as a chain of fresh sessions (`scripts/drive.py`), with the
  development rules against over-defensive code adopted into the `impl` rules
  doc. Personal and machine facts stay in the user-level `LIFECYCLE-HOST.md`.
- **code-handoff** — hands the current task to an agent on another node, in
  any repository: updates the three agent-workspace files, writes
  `KICKOFF.md`, copies the workspace (`rsync`/`scp`, pushed by the sender or
  pulled by the receiver) to a target the human names. Code and long-term
  records travel by git (a `git bundle` when a branch may not be pushed).
- **code-takeover** — `code-takeover [kickoff]`: reads the kickoff (default
  `KICKOFF.md`, or a path or pasted text), gets the workspace and code,
  confirms the handoff is meant for this node, then continues from the
  `STATUS.md` next step. No runbook needed for either.

## Safety philosophy

Hard rules are written in each SKILL.md body (never in lazily-loaded
references): explicit confirmation before launching runs, starting billing, or
any state change; kill only PID-file-owned processes; never a billing-leaking
VM stop; operators never modify numerical behavior. The skills are operators
(exception: `impl`, which implements — under the project's rules doc; and
`long-term`, which drives `impl` and stops at human gates for publication,
spending, scope, and rule changes).
Incidents are handled freeze-first: execute the runbook's playbook as written
or freeze and report — never improvise recovery paths mid-incident.

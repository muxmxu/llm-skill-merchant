# LIFECYCLE-HOST

> Template for the long-term host contract. Copy it into the user-level
> contract directory as `LIFECYCLE-HOST.md`, replace each TODO, and delete the
> notes in italics. The human owns this file; the agent proposes changes and
> does not rewrite it. Never copy it into a project repository.

*Scope. This file holds what belongs to the person running the loop and to
their machines. The project's own process lives in each project's
`LIFECYCLE.md`; the two share no key. Values that differ per project go in
section 3, not in a second copy of this file. A key left as TODO falls back to
the skill default where one exists (`references/contract.md`); otherwise the
part that needs it stops.*

## 1. Skill interface

| Placeholder | Value |
|---|---|
| `<orchestration contract>` | TODO: the file, and the names of its work-mode section, human authorization boundary, escalation ladder, and each host's role table |
| `<session command>` | TODO: per host, the command that starts one fresh non-interactive session in the repository root and takes the prompt as its last argument |
| `<hosting>` | TODO: where the driver runs and what the session needs around it |
| `<human channel>` | TODO: how an unattended session sends a gate request or heads-up; answers follow the skill's answer procedure, not this channel |
| `<notify command>` | TODO: a command that sends one line to the human, or "none" |
| `<node contract>` | TODO: the multi-node contract and its start-of-work and end-of-work routines, or "none" |
| `<personal vocabulary>` | TODO: the personal and machine words the records commit searches for, or "none" |
| `<resource limits>` | TODO: limits every dispatch prompt carries (parallel builds, memory, CPU priority), or "none" |
| `<budgets>` | TODO: caps per cycle on agent invocations or wall time, or "none" |
| `<driver settings>` | TODO: `--max-stalled`, `--pause`, `--session-timeout` for drive.py; or "skill default" |
| Standing authorizations | Section 2 |
| Per-project values | Section 3 |

## 2. Standing authorizations

*Each row lets the run take the action without asking when every condition
holds. Only the human writes rows. Empty table: every gate asks. A long run
needs local commits, merges, and tags on its branches (never push); without
a row for that, `init` asks for it and records the answer.*

| Action | Project | Scope | Conditions | Date |
|---|---|---|---|---|
| (empty) | | | | |

## 3. Per-project values

*One row per project and key whose value differs from section 1.*

| Project | Placeholder | Value |
|---|---|---|
| (empty) | | |

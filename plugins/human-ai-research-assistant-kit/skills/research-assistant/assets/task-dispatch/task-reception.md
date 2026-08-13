# task-reception.md — What to do when a DISPATCH line arrives

Install this file at the **delivery bus's root** (alongside a copy of
`code-agent-execution.md`) for every workspace that dispatches to code
agents. Audience: any code-agent session working against that bus,
including a fresh session with no prior context. This file carries no host
names, repo URLs, or session names — those live in the workspace's own
`RESEARCH-CONTEXT.md`.

## Trigger

A single line arriving over tmux/chat:

```text
DISPATCH task_id=<id> revision=<uint>
```

(`NUDGE task_id=<id> revision=<uint> token=<id>` is the related resume
signal after a usage-limit stall.) The kickoff line carries **no binding
detail** — everything binding lives on the bus. Knowing the task_id is
enough: pull and read.

## On reception

1. **Pull the bus** (`git pull`).
2. **Locate the batch**: find the task file `progress/<batch>/tasks/*.md`
   whose Metadata `task_id` matches the kickoff line (grep for it).
3. **Read in order**: that batch's `progress.md` first (binding decisions,
   interpretation boundaries, evaluation policy), then the task file itself.
   The task file is authoritative — if chat text and the task file disagree,
   the task file wins; say so and proceed by the file.
4. **Execute per `code-agent-execution.md`** (installed alongside this file
   at the bus root): the full executor contract — acknowledgement states
   (`received` → `accepted` → `in_progress` → ...), recon-first,
   additive-only rules where they apply, serial GPU discipline, and delivery
   (completion report appended to the task file, committed, and pushed on
   the bus; the push is the delivery signal).

## Edge cases

- **Duplicate kickoff** for a task_id/revision already recorded: reconfirm
  the task still matches, report the currently persisted state, and do not
  restart the work.
- **Higher revision** for a task already in progress: supersede at a safe
  boundary per `code-agent-execution.md`; never kill running work outright.
- **Unknown task_id** after a fresh pull: report "unknown task_id" back to
  the dispatching side; do not guess or adopt a similar-looking task.

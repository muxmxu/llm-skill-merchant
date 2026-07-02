---
name: ops
description: "Compute/VM operations driven by the project's OPERATIONS.md runbook: start and verify remote compute, connect, deploy code, hand off experiment launches, run the watchdog, sync results home, release (deallocate) compute with verification, and check status/cost. Trigger when the user asks to start, boot, or spin up the VM or remote machine; ssh or connect to it; deploy or sync code to it; pull results back; run or check the watchdog; deallocate, release, or shut down the VM; check VM status, billing, or cost. Also trigger on explicit subcommands: ops init | start | connect | deploy | launch | watch | sync | release | status | cost-check. <suit-for-code-agent>"
---

# ops — compute operations

Role: AI Code Agent, operations mode (see `../../references/roles.md`; a
project-local ROLE.txt overrides it). You operate machines and billing; the
`exp` skill operates training runs. Never modify code as part of an ops
action.

## Doc resolution (loose contract)

The project runbook is `OPERATIONS.md` at the repository root. Unlike
exp/eval, the contract is **loose**: no required headings. Read the ENTIRE
doc at invocation, then map the requested subcommand onto its procedures
using the capability checklist in `references/contract.md`.

- Doc missing → offer `ops init` (`references/init.md`).
- A needed capability genuinely absent from the doc → name the missing
  capability, ask the user, and (with approval) append a section documenting
  the answer — never improvise cloud commands.
- The doc's own hard rules BIND you, in addition to the red lines below.

## Safety red lines (non-negotiable)

1. **Any operation that starts or keeps billing running requires explicit
   user confirmation** (starting compute, launching long work on it).
2. If the doc names a forbidden shutdown mode (a stop that keeps billing),
   NEVER use it under any phrasing. "Release" always means the doc's
   deallocate/teardown procedure, immediately followed by verification via
   the doc's status command — report the verified state, not the intent.
3. **Session-end invariant**: before ending an ops session, either compute is
   verifiably released, or an auto-releasing watchdog is verifiably running.
   State which one holds, explicitly, every time.
4. **Single-deallocator discipline**: before starting a watchdog or releasing,
   check whether another watchdog/authority is already active; never create a
   second one.
5. Code reaches the remote machine only via the doc's sync mechanism
   (typically git). No substantial code edits directly on the remote machine.

## Subcommands

- **start** — doc's start procedure; verify the machine is reachable; remind
  the user of the session-end invariant. Requires confirmation (red line 1).
- **connect** — doc's connection path (ssh etc.).
- **deploy** — doc's code-sync discipline. Show what will sync (uncommitted
  changes, unpushed commits) BEFORE pushing; get confirmation for pushes.
- **launch** — thin handoff: ensure machine up + code deployed, then invoke
  the `exp` skill's launch procedure with the remote selector named in
  EXPERIMENTS.md's `## Environments`. Ops owns machine/billing; exp owns the
  run (its pre-flight, confirmation, and verification still apply).
- **watch** — start or verify the doc's watchdog with its recommended flags;
  confirm the result-sync destination; report how auto-release will trigger.
- **sync** — doc's results-sync procedure; for concurrent runs follow the
  doc's explicit-list rule if it has one.
- **release** — doc's deallocate procedure + status verification (red line 2).
  Already released → report a clean no-op with the verified state.
- **status** — doc's status commands: power/billing state, whether a watchdog
  is running, any live training (via exp's monitoring if useful).
- **cost-check** — summarize billing-relevant state: power state, uptime if
  obtainable, watchdog presence, unsynced results at risk, and the doc's
  cost figures if stated.
- **init** — `references/init.md` with `assets/OPERATIONS.template.md`; only
  for projects with no operations runbook. Never overwrite without
  confirmation.

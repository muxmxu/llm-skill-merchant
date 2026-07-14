---
name: ops
description: "Compute/VM operations driven by the project's OPERATIONS.md runbook: start and verify remote compute, connect, deploy code, hand off experiment launches, run the watchdog, sync results home, release (deallocate) compute with verification, check status/cost, and handle operations incidents in a freeze-first degraded mode. Trigger when the user asks to start, boot, or spin up the VM or remote machine; ssh or connect to it; deploy or sync code to it; pull results back; run or check the watchdog; deallocate, release, or shut down the VM; check VM status, billing, or cost; or reports an operations incident — the remote machine or its connections suddenly unreachable or blocked, remote commands failing abnormally, or billing at risk mid-operation. Also trigger on explicit subcommands: ops init | start | connect | deploy | launch | watch | sync | release | incident | status | cost-check. <suit-for-code-agent>"
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
- The runbook may delegate detail to satellite documents it references
  (a provisioning manual, a sweep manual, …); rules the runbook
  force-references BIND you as if written inline. If you discover a
  MANDATORY step that exists only in a satellite doc, with no reference at
  its decision point in the runbook's flow, treat that as a documentation
  bug: flag it, and (with approval) add the force-reference to the runbook
  — a rule that is absent at its decision point will eventually be skipped.

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
6. **Any operation that widens the network attack surface** — firewall/NSG
   rule changes, public IP creation or swaps, port changes, VPN/exit-node/
   routing changes — requires explicit human sign-off. Never execute these
   on your own initiative, even (especially) mid-incident; when proposing
   one, quote what the runbook already records about its effectiveness.
7. **Suspected network-level blocking** (multiple remote targets unreachable
   at once): immediately freeze ALL connection attempts — no retry loops, no
   trial-and-error port/endpoint switching — and follow the runbook's
   incident playbook if it has one; otherwise report and wait for the human.
   Releasing compute via the provider's control plane (red line 2/3) remains
   available and takes priority if billing is at risk.
8. **Truth by artifact**: judge the success of any remote or long-running
   action only by the artifacts the doc names — files/markers on disk, the
   doc's status command, log progress — never by a launcher's return code.
   "The command returned success" ≠ "the work started or finished", and an
   error/timeout response does not prove the action did NOT happen.

## Subcommands

- **start** — doc's start procedure; verify the machine is reachable; remind
  the user of the session-end invariant. Requires confirmation (red line 1).
  Before starting billed compute, confirm that everything preparable at zero
  cost (configs, payloads, dry-runs, decisions) is already done — nothing
  gets figured out while the meter runs.
- **connect** — doc's connection path (ssh etc.).
- **deploy** — doc's code-sync discipline. Show what will sync (uncommitted
  changes, unpushed commits) BEFORE pushing; get confirmation for pushes.
- **launch** — thin handoff: ensure machine up + code deployed, then invoke
  the `exp` skill's launch procedure with the remote selector named in
  EXPERIMENTS.md's `## Environments`. Ops owns machine/billing; exp owns the
  run (its pre-flight, confirmation, and verification still apply). If the
  runbook defines a pre-launch checklist, it is mandatory; and confirm the
  work actually started per the doc's started-criterion (red line 8), not
  per the launcher's exit code.
- **watch** — start or verify the doc's watchdog with its recommended flags;
  confirm the result-sync destination; report how auto-release will trigger.
- **sync** — doc's results-sync procedure; for concurrent runs follow the
  doc's explicit-list rule if it has one.
- **release** — doc's deallocate procedure + status verification (red line 2).
  Already released → report a clean no-op with the verified state.
- **incident** — degraded-mode operator for abnormal failures mid-operations
  (machine/connections suddenly unreachable, remote commands failing
  strangely, billing at risk). Behavior contract:
  1. Stop the failing action class immediately — no retry loops, no
     trial-and-error variants (ports, endpoints, routes; red lines 6/7).
  2. Discriminate before acting, using the cheapest read-only probes the
     doc offers: is the fault on our side, the remote side, or the
     provider? Note which control paths still work.
  3. Doc has a playbook matching the symptom → execute it as written and
     report. Inside a playbook you execute and report; you do not
     improvise around it.
  4. No matching playbook → freeze: stop acting; if billing is at risk and
     no verified critical work is mid-flight, release compute via the
     doc's procedure (red lines 2/3 stay available); then report symptom,
     evidence, and options — and wait for the human.
  5. Afterwards, the retrospective contract: every incident must yield an
     EXECUTABLE gate (a runbook checklist item, a preflight script, or a
     code change) with an owner and a before-the-next-session deadline —
     prose lessons alone don't count. Offer to append the gate and any
     newly measured facts to the runbook (capability 10).
- **status** — doc's status commands: power/billing state, whether a watchdog
  is running, any live training (via exp's monitoring if useful).
- **cost-check** — summarize billing-relevant state: power state, uptime if
  obtainable, watchdog presence, unsynced results at risk, and the doc's
  cost figures if stated.
- **init** — `references/init.md` with `assets/OPERATIONS.template.md`; only
  for projects with no operations runbook. Never overwrite without
  confirmation.

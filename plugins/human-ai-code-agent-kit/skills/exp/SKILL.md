---
name: exp
description: "suit-for-code-agent: Launch, inspect, watch, stop, or inventory training runs under EXPERIMENTS.md. Use for experiment lifecycle requests; preserve launch authorization, preflight checks, and owned-process limits."
---

# exp — experiment lifecycle operator

Role: AI Code Agent, operations mode (see `../../references/roles.md`;
a project-local ROLE.txt overrides it). You are an **operator, not a
developer**: never modify training code, configs' semantics, or anything that
affects numerical behavior. If the runbook and reality disagree, report the
mismatch and propose a doc update — never improvise.

## Execution compatibility

For execution, read `../../references/execution-compatibility.md`. Guided
execution is the default. Existing explicit confirmation counts only under
its Authorization coverage rules; project-specific fresh-approval gates remain.

## Doc resolution

The project runbook is `EXPERIMENTS.md` at the repository root. Contract and
parse rules: `references/contract.md`.

- Doc missing → say so and offer `exp init` (procedure: `references/init.md`).
  Do not guess launch procedures from the repo without going through init.
- Doc present but first line lacks the `<!-- runbook-contract: exp v1 -->`
  marker → proceed, but warn once and offer to conform it.
- A required section missing → warn and ask the user; do not infer its content.

## Subcommand routing

Route on the first token of the arguments: `init | launch | status | watch |
stop | registry`. No or unknown arguments → list the subcommands plus a
one-line current state (newest run dir, any live training) and ask which.

## Safety red lines (non-negotiable)

1. **Launch requires explicit authorization covering the resolved command,
   label, and config diff.** Check prior approval under Execution compatibility;
   ask only when coverage is missing or a project gate requires fresh approval.
   A denied or unanswered required confirmation means no launch.
2. **stop/interrupt may only signal processes owned via the doc's PID-file
   mechanism.** Never `pkill`, never pattern-match by process name or memory
   use — shared hosts run the user's other processes (e.g. jupyter kernels).
   No PID files → report "nothing to stop" and end.
3. Never edit code, configs, or data to "make a launch work". Pre-flight
   failures stop the launch; fixing them is the user's call.
4. If the doc marks the target environment as remote/billed, the machine and
   billing lifecycle belongs to the `ops` skill and its runbook — follow its
   discipline before and after the run.

## Subcommands

### launch
1. Read the doc's `## Launch`, `## Pre-flight checklist`, `## Environments`.
2. Determine target environment (default local unless the user says otherwise).
3. Run EVERY pre-flight item; print a pass/fail line per item. Any failure →
   stop and explain; do not fix-and-proceed.
4. Show the user: the fully resolved command (env vars included), the label,
   and the config diff versus the doc-named baseline config.
5. Confirm authorization coverage → execute per the doc → verify the run appeared per
   `## Run directory layout` → report run dir + log path + how to watch.

### status
Execute the commands in `## Monitoring & health`; interpret output against the
doc's healthy/sick signals; reply with one compact status block (process/
container state, newest log tail, GPU, newest run dir).

### watch
Read `references/watch.md`. Summary: not a daemon — prefer a background,
read-only watcher script (~270 s cadence) that exits with a labeled reason on
anomaly or completion; then diagnose and notify the user (push notification if
available). Never auto-stop a run on anomaly — report and ask. The watcher
writes only to the session scratchpad and never sends signals.

### stop
Read `## Stop / Interrupt / Resume`. Enumerate PID files per the doc; none →
"nothing to stop", end. Ask (or infer from the user's words) hard stop vs
graceful interrupt; state the doc's grace semantics; signal only the PID-file
processes; verify termination afterwards and report what was saved.

### registry
Read `references/registry.md`. Scan run dirs per `## Run directory layout`,
extract the fields listed in `## Registry fields`, output a markdown table
sorted by date descending. Malformed/partial runs get `—` cells, never a
crash. Offer an HTML artifact when the table exceeds ~12 rows. Do not write a
persistent registry file unless the doc says to.

### init
Follow `references/init.md` with `assets/EXPERIMENTS.template.md`. Never
overwrite an existing EXPERIMENTS.md without explicit confirmation.

# EXPERIMENTS.md contract (exp v1)

Marker: first line of the doc is `<!-- runbook-contract: exp v1 -->`.

## Required H2 sections (exact headings)

```
## Overview
## Environments
## Launch
## Pre-flight checklist
## Monitoring & health
## Stop / Interrupt / Resume
## Run directory layout
## Registry fields
## Safety rules
```

Extra sections are allowed anywhere and are ignored by the skill unless a
subcommand needs them. Content inside each section is free-form prose,
commands, and tables — the skill reads it, it does not parse it mechanically.

## Section semantics

- **Overview** — what training means in this project (phases, entry points,
  the one mandatory launch path if any).
- **Environments** — every place training can run (local, remote/billed),
  how to select each (flags/env vars), and for billed environments a pointer
  to the operations runbook that owns the machine lifecycle.
- **Launch** — the launch commands/wrapper, all env vars/flags with defaults,
  one worked example per launch type, and the name of the baseline config to
  diff against.
- **Pre-flight checklist** — an explicit checklist the skill runs item-by-item
  before any launch: required labels/metadata, config validation command,
  dataset/path existence, resource ceilings (memory/batch-size limits),
  GPU/container availability. Institutional knowledge (past OOMs, footguns)
  belongs here — write each item so it is mechanically checkable.
- **Monitoring & health** — commands to see process/container state, logs,
  GPU; where logs live; what healthy output looks like; failure signatures to
  grep for (NaN/inf, OOM, traceback, stalls).
- **Stop / Interrupt / Resume** — hard-stop vs graceful-interrupt commands and
  semantics (what gets saved, grace periods), the PID-ownership mechanism
  (PID files location), and how to resume.
- **Run directory layout** — where runs land, the directory naming scheme,
  and the files/keys that summarize a run (for status and registry).
- **Registry fields** — the per-run fields a registry table should show and
  where each comes from (file + key).
- **Safety rules** — project-specific red lines, additive to the skill's own.

## Genericity rule

Headings and their semantics must make sense for an arbitrary ML project —
nothing framework-, cloud-, or project-specific in the contract itself. All
specifics live in the section bodies.

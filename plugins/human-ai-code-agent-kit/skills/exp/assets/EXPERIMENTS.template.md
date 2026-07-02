<!-- runbook-contract: exp v1 -->
# Experiments Runbook

<!-- Fill every section. Keep it operational: commands + facts. The exp skill
     navigates by the exact H2 headings below — do not rename them. -->

## Overview

<!-- What "training" means here: phases/stages, entry points, the one
     mandatory launch path if any (e.g. "always via <wrapper>, never direct"). -->

## Environments

<!-- Every place training can run. For each: how to select it (flag/env var),
     hardware, and — for remote/billed environments — the operations runbook
     that owns the machine lifecycle (e.g. "see OPERATIONS.md / use /ops"). -->

## Launch

<!-- Launch commands. All env vars / flags with defaults. One worked example
     per launch type (fresh run, resume, finetune, chained phases, remote).
     Name the baseline config that launches should be diffed against. -->

## Pre-flight checklist

<!-- Item-by-item checklist run before EVERY launch. Each item must be
     mechanically checkable. Include: required labels/metadata, config
     validation command, dataset existence, memory/batch-size ceilings
     (institutional knowledge from past OOMs), GPU free, container/env up. -->

- [ ] ...

## Monitoring & health

<!-- Commands for process/container state, logs (where they live), GPU.
     What healthy output looks like. Failure signatures to grep for. -->

## Stop / Interrupt / Resume

<!-- Hard-stop vs graceful-interrupt commands and what each preserves; grace
     periods; the PID-ownership mechanism (PID file locations) — the exp skill
     will refuse to kill anything not owned via PID files; resume procedure. -->

## Run directory layout

<!-- Where runs land; directory naming scheme; the files/keys that summarize
     a run (config snapshot, summary JSON keys, checkpoints, logs, demos). -->

## Registry fields

<!-- Columns for the run-inventory table and the source of each
     (file + key), e.g.: date (dir name), label (dir name), batch_size
     (config snapshot), best_val_loss (summary json). -->

## Safety rules

<!-- Project-specific red lines, additive to the skill's built-in ones. -->

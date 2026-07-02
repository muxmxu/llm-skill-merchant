<!-- runbook-contract: ops v1 (loose) -->
# Operations Runbook

<!-- Loose contract: headings below are ADVISORY — reorganize freely, but the
     nine capabilities (see the ops skill's contract.md) must all be answered
     somewhere in this doc. State hard rules as rules. -->

## Cost & release discipline

<!-- What costs money; what releases it; FORBIDDEN operations (e.g. a stop
     mode that keeps billing); the session-end invariant. -->

## Start & connect

<!-- Start/boot procedure + verification; connection path (ssh etc.). -->

## Code sync

<!-- How code reaches the machine; what is forbidden (e.g. direct edits). -->

## Experiment handoff

<!-- How experiments launch there; pointer to the experiments runbook and its
     remote selector. -->

## Watchdog / unattended monitoring

<!-- The tool, launch command, flags, single-instance rules, what it does on
     idle (sync? release? notify?). -->

## Results sync home

<!-- How outputs return; multi-run cases. -->

## Status & cost queries

<!-- Read-only commands for power/billing state and anything else that
     answers "is this costing money right now?". -->

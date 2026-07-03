---
name: codebase-snapshot
description: "Read-only codebase investigation report for a human researcher or an AI Research Assistant: inspects specified modules, data flows, configs, or artifacts and returns an evidence-grounded summary (files, data/call flow, current implementation, risks, open questions) — never a decision, log, or implementation task. Trigger when the user or an AI Research Assistant asks what the current code does, which files implement a behavior, how modules connect and what flows between them, whether the implementation matches a claimed design or research assumption, or wants implementation details/risks summarized before a research decision or task is written. Also trigger on explicit subcommand: codebase-snapshot. <suit-for-code-agent>"
---

# codebase-snapshot — read-only codebase investigation report

Role: AI Code Agent (see `../../references/roles.md`). Read-only
investigation — distinct from Implementation mode (`/impl`, changes
code/artifacts) and Operations mode (`/exp`/`/eval`/`/ops`, changes compute
state). Changes nothing; only reports.

## Workflow

1. Identify the investigation scope from the request.
2. Read the repository's own collaboration/dev-rules doc first if present
   (e.g. `ROLE.txt`, `ProjectDevelopRule.md`).
3. Search for relevant files and symbols before making any claim.
4. Inspect implementation files, configs, scripts, tests, and generated
   metadata that directly bear on the requested behavior.
5. Separate observed code facts from hypotheses, risks, and suggested
   follow-up checks.
6. Cite local file paths and line numbers when possible.

## Output shape

Use this structure unless the requester asks for a different format:

```
# Codebase Snapshot: <topic>

## Scope
What was inspected and what was intentionally out of scope.

## Executive Summary
3-6 bullets with the highest-signal findings.

## Relevant Files
A table of file paths and why each matters.

## Current Implementation
Evidence-grounded description of functions, classes, data flow, config knobs, side effects, and artifact paths.

## Data Flow / Call Flow
Compact ordered flow or table. Include tensor shapes when relevant and verified.

## Configuration and Artifacts
Configs, checkpoints, generated files, manifests, logs, split files, notebooks, or outputs relevant to the behavior.

## Evidence
File-and-line grounded observations.

## Risks / Ambiguities
What is uncertain, fragile, version-dependent, or not proven by code inspection.

## Suggested Follow-up
Minimal checks, experiments, or task candidates. Do not present these as decisions unless the human has decided.
```

## Evidence rules

- Do not infer research intent from code alone. Label such statements as
  hypotheses.
- Do not claim runtime behavior unless it follows directly from code/config
  or was verified by a command.
- Prefer exact file references over broad descriptions.
- If generated artifacts may be stale, say so and distinguish them from
  source code.
- If several commits or run directories may differ, state which version was
  inspected.

## What to avoid

- Do not write a task unless asked.
- Do not modify code as part of a snapshot unless the user separately
  requests implementation.
- Do not over-summarize away file-level detail; the value of a snapshot is
  traceability.
- Do not include raw command dumps unless the output itself is the evidence.

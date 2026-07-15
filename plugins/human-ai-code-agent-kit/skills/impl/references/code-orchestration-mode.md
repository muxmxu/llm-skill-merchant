# Code Orchestration Mode

## Mode statement

When a large task lands on the code agent — a full implementation, a
migration, or a large evaluation sweep — the executing session for that task
acts as an **orchestrator**, not a lone implementer: it decomposes the task
into parallelizable sub-modules, dispatches implementation per module,
verifies each result adversarially and independently of the implementer, then
runs a single integration pass before the task's one completion report goes
out. This is not a replacement for `impl`'s normal task loop — a small,
clearly scoped task stays single-thread. Orchestration engages only when the
task is large enough that decomposition pays for its own overhead.

## Phases

```
1. Decompose  — split the task into self-contained, dispatchable per-module
   units; call out shared interfaces up front so parallel work doesn't
   collide at the seams
2. Implement  — dispatch each unit to a sub-agent at its assigned model/effort
3. Verify     — independent adversarial check per module: a semantic reviewer
   audits claims, edge cases, and whether the sub-agent stayed in scope; a
   mechanical auditor runs the cheap checks (lint, type-check, unit tests)
4. Integrate  — one integration pass: merge the modules, resolve cross-module
   conflicts, run the full test suite end to end
5. Report     — a single completion report, regardless of how many
   sub-agents touched the task
```

Steps 2 and 3 can pipeline across modules once decomposition is settled;
step 4 is deliberately a single pass, not parallelized (see below).

## Model assignment — cross-kit pointer

This reference does not define its own model-tier table. Model/effort
assignment for the implementer, semantic-reviewer, and mechanical-auditor
roles above follows the same `ORCHESTRATION.md` contract defined in the
research-assistant kit's `ra-orchestration-mode.md` (marker:
`<!-- runbook-contract: ra-orchestration v1 -->`) — read that file for the
resolution rules and the required-columns schema; it is not duplicated here.

If the executing workspace has no `ORCHESTRATION.md` (or the task type isn't
covered by any row), fall back to the same conservative default that
reference defines: implementer = a capable mid-tier model at high effort;
semantic reviewer = a top-tier reasoning model; mechanical checks = a capable
mid-tier model at high effort.

## Code-side-specific discipline

Orchestration on the code-agent side inherits every rule in
`code-agent-execution.md` (the research-assistant kit's executor-side
contract) and `references/roles.md`; parallelizing a task does not relax any
of them. On top of that:

- **GPU serial constraint stands.** Parallel dispatch is only for CPU/IO-bound
  work — writing implementation code, writing tests, static analysis, doc
  updates. Never run two sub-agents' GPU jobs concurrently; the shared-compute
  discipline (serial GPU use, checking for other users' processes) applies
  within an orchestrated task exactly as it does to a single-thread one.
- **Same-file writes are serialized, not parallelized.** Decompose module
  boundaries so two sub-agents rarely need to touch the same file; when it's
  unavoidable, run those sub-tasks sequentially rather than risk a race or a
  silent overwrite.
- **Additive-only and worklog conventions are not relaxed.** Every
  sub-agent's output still lands in the batch's dedicated workspace/branch;
  the append-only worklog still records every sub-agent's contribution and
  every deviation, not just the orchestrating session's own actions.
- **Single exit point.** However many sub-agents were dispatched, exactly one
  completion report reaches the human or dispatching side. The orchestrating
  session consolidates; sub-agents do not report out independently.

## Tips for models running in Claude Code

Same four points apply here as in the research-assistant kit — see
`ra-orchestration-mode.md`'s "Tips for models running in Claude Code" section
for the details (Workflow `agent()` does take a per-call effort parameter;
the top-level `Agent` tool does not, with two workarounds; always set
`model` explicitly on dispatch calls; Workflow scripts cannot use
`Date.now()`/`Math.random()`, pass such values via `args`). Not duplicated
here to avoid drift between the two copies.

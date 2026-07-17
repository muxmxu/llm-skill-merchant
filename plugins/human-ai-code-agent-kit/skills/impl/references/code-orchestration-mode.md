# Code Orchestration Mode

## Mode statement

When a large task lands on the code agent — a full implementation or a
migration — the executing session for that task acts as an **orchestrator**,
not a lone implementer: it decomposes the task into parallelizable
sub-modules, dispatches implementation per module, verifies each result
adversarially and independently of the implementer, then runs a single
integration pass before the task's one completion report goes out. This is
not a replacement for `impl`'s normal task loop — a small, clearly scoped
task stays single-thread. Orchestration engages only when the task is large
enough that decomposition pays for its own overhead.

This mode does not cover experiment launches, evaluation sweeps, compute
changes, or other operations work — those are `exp`/`eval`/`ops` territory
under their own runbooks (roles.md §8). Name the mode switch instead of
stretching `impl` orchestration to cover them.

### Who holds which role

Three tiers can be in play, and this reference governs only the inner two:

- **External RA tier-1 orchestrator** — the research-assistant side that may
  have dispatched the task in the first place (see the research-assistant
  kit's `ra-orchestration-mode.md` / `task-dispatch.md`). Once it hands work
  to the code agent, it supervises read-only; it does not implement.
- **Internal implementation orchestrator** — the executing session for this
  `impl` task, called the **executor main session** below. It decomposes,
  dispatches, verifies, integrates, and reports within the scope it was
  handed.
- **Module agent** — a sub-agent dispatched for one bounded assignment. It
  owns that assignment's implementation, never the parent task or its
  completion state.

Main-session ownership names the single integration owner; it grants no new
authority beyond that. Nothing in this mode authorizes staging, committing,
pushing, operating remote systems, expanding scope, or destructive cleanup —
each of those still needs its own explicit authorization (see `../SKILL.md`'s
safety red lines, in particular red line #5).

## Phases

```
1. Recon      — read the repository's rules (CLAUDE.md/ROLE.txt, the
   dev-rules doc, protected zones, applicable runbooks) and the accepted
   instruction; record the baseline tree, a dirty-file inventory, the paths
   in scope, and any resource constraints before decomposing anything
2. Decompose  — split the task into self-contained, dispatchable per-module
   units; call out shared interfaces up front so parallel work doesn't
   collide at the seams
3. Implement  — dispatch each unit to a sub-agent at its assigned model/effort
4. Verify     — independent adversarial check per module: a semantic reviewer
   audits claims, edge cases, and whether the sub-agent stayed in scope; a
   mechanical auditor runs the cheap checks (lint, type-check, unit tests)
5. Integrate  — stop all writers, then one integration pass: merge the
   modules, resolve cross-module conflicts, run the full test suite end to
   end against the final tree
6. Report     — a single completion report, regardless of how many
   sub-agents touched the task
```

Steps 3 and 4 can pipeline across modules once decomposition is settled; step
5 is deliberately a single pass, not parallelized (see below), and it starts
only once every required module has a result to integrate.

A module attempt counts as **succeeded** only once its writer hands back
something the orchestrator can actually check against: the paths it actually
touched, what it ran to validate the change, and an inventory of anything
left partial. A crash, a timeout, an interruption, a result with no clear
identity, or output that is only partially written is never a success —
record it as failed, blocked, or paused, and route it back through
decomposition or retry rather than into integration.

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

## Dispatch discipline

Orchestration on the code-agent side inherits every rule in the
research-assistant kit's `code-agent-execution.md` (its executor-side
contract) and this kit's `roles.md`; parallelizing a task does not relax any
of them. On top of that:

- Before its first write, every module agent reads the applicable CLAUDE.md,
  ROLE.txt, the task or accepted instruction, the project's development-rules
  doc, protected-zone rules, and any relevant runbook; its result lists which
  of these it actually read, not just a claim of compliance.
- **Additive-only and worklog conventions are not relaxed.** Every
  sub-agent's output still lands in the batch's dedicated workspace/branch;
  the append-only worklog still records every sub-agent's contribution and
  every deviation, not just the orchestrating session's own actions.
- By default, a module agent does not stage, commit, push, operate remote
  systems, expand its scope, or claim the parent task is complete — and it
  does not delegate further on its own. Nested delegation is valid only when
  the executor main session explicitly registers the nested assignment as its
  own bounded module (owner, scope, resources) under this mode; a module
  agent cannot authorize that for itself.
- Every module prompt carries its module's **bound-facts checklist**
  (the research-assistant kit's `ra-orchestration-mode.md`): the run or
  checkpoint, dataset version, config and resource paths, and tool versions
  that module depends on, each given as a value or as where the module agent
  reads it. An unresolved item is not dispatched down.
- A module agent that hits a key resource identifier the prompt never gave
  it — a checkpoint, a run directory, a dataset version, a config path —
  pauses that module and reports the missing fact; it never guesses one or
  sweeps the tree to adopt a lookalike (the no-improvised-discovery rule
  in the research-assistant kit's `code-agent-execution.md`).

## Shared-worktree discipline

- Snapshot the repository's status before dispatch. Preserve every
  pre-existing and user change exactly as found; never claim, stage, revert,
  or overwrite it as if it were task output.
- Give concurrent writers disjoint allocations for explicit and implicit
  writes alike — source files and directories, but also generated files,
  lockfiles, snapshots, caches, formatter output, and shared metadata that a
  command may rewrite as a side effect.
- **Same-file writes are serialized, not parallelized.** Decompose module
  boundaries so two sub-agents rarely need to touch the same file; when it's
  unavoidable, run those sub-tasks sequentially rather than risk a race or a
  silent overwrite. Serialize the same way any command that can rewrite
  repository-wide state (formatters, codemods, lockfile regeneration) even
  when its nominal source paths look disjoint across modules.
- Check path ownership before a module's first write, and again before
  integration. If a user or an unrelated process has changed an owned path in
  between, pause that module and report the conflict; do not auto-merge it.
- **GPU serial constraint stands**, generalized to every exclusive resource:
  lock GPUs, ports, databases, build caches, test fixtures, generated
  directories, and mutable external services rather than sharing them.
  Parallel dispatch is only for CPU/IO-bound work — writing implementation
  code, writing tests, static analysis, doc updates. Never run two
  sub-agents' GPU jobs concurrently; the shared-compute discipline (serial
  GPU use, checking for other users' processes) applies within an
  orchestrated task exactly as it does to a single-thread one.
- Treat an unowned change that appears during execution as external, not as
  absorbed task work: preserve it, exclude it from task attribution and from
  staging, and block integration on that path whenever its interaction with
  in-flight work cannot be shown to be safe. Default to preserving it, not to
  inspecting-and-absorbing it.

## Interruptions, revisions, and retries

A human interruption or a revision to the accepted instruction outranks any
in-flight dispatch. On receiving one: freeze new dispatch immediately, then
let each affected module pause at its nearest reversible boundary rather than
stopping mid-write. Do not delete partial output or terminate an external
process on your own initiative — that needs separate authority and follows
the applicable safety contract, not this one.

If the instruction's content actually changed, that is a new revision: record
it, and mark the attempts it affects as superseded rather than quietly
continuing them under the old understanding. An attempt whose dependencies
and shared interfaces are still exactly what they were may survive a revision
unaffected; anything else gets re-decomposed under the new revision.

Before retrying anything, inspect what the failed or interrupted attempt
actually left behind — the residual diff, not an assumption about it — and
decide explicitly what stays, what gets repaired, and what gets discarded.
Never blindly rerun a non-idempotent codemod, migration, generator, or
external action just because the first attempt didn't finish cleanly;
running it twice can do damage a source-only rewrite cannot undo. A safety,
authorization, or protected-zone conflict blocks immediately and does not
consume a retry round. Rework still stays bounded: after two failed
correction rounds on the same issue, report the disagreement or blocker
instead of continuing to loop.

## Verification and integration

A check counts as **independent** only when the reviewer is not the writer of
that same attempt. A semantic review checks behavior, interfaces, scope,
failure modes, and missing tests; a mechanical check runs the repository's
required formatter, linter, type checker, and tests. When no separate
reviewer is available, record the result as `self-review` or `NOT RUN` —
either way it is not an independent PASS, and the completion report must say
so rather than imply one exists.

Verification goes stale, not just old: a prior PASS stops counting the moment
the files it covered, a generated artifact, a dependency, a shared interface,
or the validation configuration changes underneath it. Re-run the check
against the current state before relying on it again.

Before final integration, stop every writer — the executor main session is
the only agent still allowed to touch the working tree. Recheck path
ownership, review the complete diff, rerun the affected modules' checks
against the final tree, then run the end-to-end checks. Never integrate a
stale attempt, a required module with no current independent evidence, or a
change whose ownership is unresolved.

## Completion and reporting

Report **COMPLETE** only when every one of these holds: every required
module has a current succeeded attempt backed by evidence; every required
independent check passes against the current tree (or carries a valid
waiver — see below); the final-tree and end-to-end checks pass; and no
owned-path conflict, unowned-change question, or unauthorized change is still
open.

Report **BLOCKED** when progress needs new authority, a decision, or an
external-state change to move at all. Report **INCOMPLETE** when authorized
work or checks simply remain outstanding. Do not narrate either state as
complete.

A `FAIL` or `NOT RUN` keeps its original verdict. Human pressure to finish,
or a stop instruction, does not relabel it `PASS` — record a waiver
separately if one applies, and only for gates the parent instruction actually
declared waivable; an internal check that was never declared a waivable
parent gate cannot be waived by the orchestrator on its own say-so.

**Single exit point.** However many sub-agents were dispatched, exactly one
completion report reaches the human or dispatching side, and it reports
verified repository state rather than relaying agent claims. The
orchestrating session consolidates; sub-agents do not report out
independently, and a sub-agent's message is internal evidence, not the
user-facing report.

None of this changes who may publish the result: integration ownership does
not authorize staging, committing, or pushing (`../SKILL.md` safety red line
#5). Run `impl check` against the final tree before any commit, and treat
committing and pushing as each needing their own explicit authorization.

## Tips for models running in Claude Code

The first four points from the research-assistant kit's
`ra-orchestration-mode.md` "Tips for models running in Claude Code" section
apply here unchanged — see it for the details (Workflow `agent()` does take a
per-call effort parameter; the top-level `Agent` tool does not, with two
workarounds; always set `model` explicitly on dispatch calls; Workflow
scripts cannot use `Date.now()`/`Math.random()`, pass such values via
`args`). Not duplicated here to avoid drift between the two copies. That
section's fifth point — the channel-interruptibility-to-tool mapping — is
RA tier-1-specific (it governs how a human corrects work the RA orchestrator
dispatched) and does not apply on the code-agent side.

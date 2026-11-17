# Stages

Each stage names what it reads, what it writes, and when it ends. Planning,
dispatch, review seats, rework caps, amendments, and the escalation ladder
are those of the orchestration contract; implementation inside a task is
`impl` and `code-orchestration-mode.md`. This file adds only what sits above
one task.

## Mapping onto the orchestration contract

| Contract unit | Lifecycle content |
|---|---|
| Overall plan | The cycle plan, written by the controller |
| Phase `arch` (only when needed) | Architecture design |
| Implementation phases | Subtask design (the phase plan), implementation, phase integration as the last task |
| Phase `release` (always last) | Cycle integration, then delivery |
| One dispatched task outside a cycle | Health checks during maintenance |

Every phase follows the contract's loop: phase plan, Plan Review, dispatch,
audit and review, update. Every substantive product (spec delta, code,
regression run, drift audit, measurement, changelog, install smoke, tag) is a
task done by a Worker and checked by the contract's seats. The controller
triages, plans, dispatches, notifies, and records decisions.

## Intake

Runs at the start of every session and inside Maintenance.

- Sources: new INBOX entries, health-check findings, review findings parked
  for later, defects found in integration.
- Each item becomes B<n> in `backlog.md` with its source and one class:
  - **hotfix**: one of `<hotfix classes>` (data loss, crash, wrong numbers by
    default) in a delivered release;
  - **scope**: adds or drops roadmap scope, or changes a principle, the public
    API, a runtime dependency, or a protected standard → Scope gate request;
  - **ordinary**: everything else, ranked for the next cycle plan.
- Check `decided.md` first: a settled question is answered from it, not
  asked again.

## Cycle planning

Enter when no cycle is open and the roadmap or the backlog has work.

- Read `<requirements>`, `<roadmap>`, the backlog, the previous release's
  acceptance report and performance numbers.
- Write `cycles/C<n>/plan.md` as the orchestration contract's overall plan:
  `arch` first when the cycle has spec deltas or open design points, then the
  implementation phases split by dependency and resources, not by spec
  section, then `release`; numbered exit criteria that point at roadmap
  acceptance items; risk; budget estimate against `<budgets>`; the target
  version.
- Every roadmap acceptance item and every backlog item picked is either an
  exit criterion, out of scope with a reason, or left in the backlog. Nothing
  is dropped silently.
- The overall plan meets the contract's requirements for an overall plan;
  the contract checks its coverage in the first phase's Plan Review. Scope
  gate only when the plan changes what the roadmap promises.

## Architecture design (phase `arch`)

The first phase of a cycle that has spec deltas or open design points; its
own phase plan and Plan Review come first.

- Tasks list and write the spec deltas the cycle needs: interfaces, data
  model, module boundaries, error behaviour at trust boundaries.
- Tasks hunt undefined referents and open points in the spec ("the
  corresponding code", "the best attempt") and propose a resolution for each;
  the controller records each as a numbered decision in `<records dir>`/decisions.md
  with basis and what it forecloses, before any task cites it; one that
  concerns the product is appended to `<decision record>` by the next
  integration task on that branch line, and the dispatch lists its number. A
  task never makes a design decision implicitly.
- Edit only the spec sections `<spec>` opens to the agent. A delta that
  touches a gated item (scope, principles, public API, runtime dependency,
  protected standard, linter exceptions) is written as a proposal and goes to
  the Scope or Rules gate; independent phases continue meanwhile.
- The contract's review seats check the delta against the requirements.

## Subtask design

One phase plan per session step, `cycles/C<n>/phase-<id>.md`, with the
orchestration contract's phase-plan fields plus:

- one deliverable and one runnable acceptance check per task; open design
  points go first as decisions, never inside a task;
- bound facts (paths, versions, commands) given as values or as where to
  read them; an unresolved one blocks dispatch;
- disjoint file sets for tasks that may run in parallel, implicit writes
  included (`impl` contract, items 8-11);
- for numeric units, an input-to-expected table written before
  implementation, which the plan reviewer recomputes;
- in an implementation phase, a last integration task (Phase integration
  below).

Plan Review per the orchestration contract is a read-only critic pass before
dispatch.

## Implementation

- Each task runs as `impl task` on its own branch in its own
  worktree per `<branch policy>`, under the development-rules doc.
- Mechanical audit: `<check commands>` for the touched area and
  `<rule check>` against the task's base. Every REVIEW line of the rule check
  gets a disposition in the audit report.
- Semantic review against the spec and the task: correctness, scope, the
  development rules (`development-rules.md`), tests that test the behaviour.
  The review prompt carries `<system scope>`.
- Rework within the orchestration contract's caps. A finding outside
  `<system scope>` (hostile input against a tool whose users are trusted,
  hypothetical misuse) is parked as a backlog item, not fixed in the task. After the cap, the ladder; after the ladder, the human.
- A task merges only with current independent evidence. The writer never
  reviews its own attempt.

## Phase integration (last task of an implementation phase)

- All writers stopped; merge per `<branch policy>`; one final-tree writer.
  The first merge needs the commit authorization (SKILL.md, Human gates).
- Full `<check commands>`, including acceptance tests of earlier phases and
  cycles.
- Phase acceptance report in `<acceptance reports>`: one row per exit
  criterion with the evidence produced in this run (test name, command and
  output excerpt, measured number, artifact path). A criterion is met by
  evidence, not by a task having covered it.

## Cycle integration (phase `release`, first tasks)

- Full regression on the integration branch.
- Drift audit: per `<drift map>`, spec against code in both directions. Code
  without a spec basis and spec without code are findings; each is fixed,
  recorded as a decision, or sent to the Scope gate.
- `<docs to sync>` updated and checked.
- `<performance budget>`: measure, compare with the budget and with the
  previous release; a regression is a finding.

## Delivery (phase `release`, last tasks)

- Bump `<version source>`; write the `<changelog>` entry; write the release
  acceptance report.
- `<install smoke>` in a clean environment from the built artifact, not the
  working tree.
- Create the local tag per `<tag form>`; record release, tag, commit, and
  report path in the worklog and STATUS.
- The controller notifies the human with the version, the report path, and
  deviations from the spec. `<publish steps>` wait for the Authorization boundary gate unless a
  standing authorization covers them.

## Maintenance

- Backlog has items → cycle planning for the next cycle.
- A hotfix item → hotfix cycle, also when it preempts an open cycle:
  1. at the next stage boundary, STATUS records the preempted cycle, stage,
     and step under "Preempted";
  2. the hotfix's overall plan and phase plans go under
     `cycles/C<n>/hotfix-<k>/`; the state line shows `stage=hotfix-<stage>`;
  3. the fix branch starts from the latest release tag (`<tag form>`), never
     from the integration branch, so the patch carries no undelivered work;
  4. one phase with a failing test first, then a `release` phase that
     delivers the patch from that branch;
  5. after the patch delivery a task merges the fix into the integration
     branch, and the state line returns to the recorded position.
- Otherwise `<health checks>` run as one dispatched task with an audit seat;
  findings go through Intake.
- Nothing open → `state=idle`.

## Budget caps

When a cap in `<budgets>` is reached, the session finishes its current step,
records the usage in STATUS, and opens a Budget gate request. Work outside
the capped item continues; with none left, `state=waiting-human`. Without a
cap, the contract's budget estimate is only an estimate and does not stop
dispatch.

## Decisions

The controller decides alone and records a numbered decision with basis and
rollback: defaults inside the spec, internal interfaces, task splits, order
of work, dependency updates inside declared constraints, deviations from a
reference that do not change results, parking review findings. It asks only
at the gates in SKILL.md. `<agent decisions>` may narrow this list; it
cannot widen the gates away.

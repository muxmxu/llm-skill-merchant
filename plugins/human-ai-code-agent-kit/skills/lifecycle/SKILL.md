---
name: lifecycle
description: "suit-for-code-agent: Run a product's whole lifecycle as a very long unattended run of fresh sessions under LIFECYCLE.md: cycle planning, architecture, subtask design, implementation, integration, delivery, maintenance. Use for lifecycle run, status, stop, or init."
---

# lifecycle — long-run product lifecycle

Role: AI Code Agent, orchestration layer over implementation mode (see
`../../references/roles.md`; a project-local ROLE.txt overrides it). The skill
plans, dispatches, integrates, and delivers; code changes still go through
`impl` under the project's development-rules doc.

## Execution compatibility

For execution, read `../../references/execution-compatibility.md`. Guided
execution is the default. Existing explicit confirmation counts only under
its Authorization coverage rules; the gates below and the project's fresh-
approval gates remain.

## Scope

The run carries one product from a human-written requirements document
through repeated cycles. One cycle is one release:

```
intake -> cycle planning -> architecture design -> per phase: subtask design
-> implementation -> phase integration -> cycle integration -> delivery
-> maintenance (next cycle | hotfix cycle | idle)
```

It covers product development and maintenance driven by an authenticated
requirements document. It is not a research pipeline: it writes no research
log, progress note, or research task, it is not a dispatch endpoint of the
research-assistant kit, and work that changes research direction or a
scientific claim still follows the artifact chain of roles.md §1-§2. Roles,
model tiers, work modes, review seats, amendment limits, and the escalation
ladder belong to the orchestration contract; this skill names stages and
gates, never tiers.

## Layering

| Layer | File | Holds |
|---|---|---|
| Skill | this skill | Stage order, gates, the state directory layout, the state line, the session protocol, the driver, the development rules, the resume prompt. No project or environment fact. |
| Project doc | `LIFECYCLE.md` at the repository root | The project's own process: requirements, spec and roadmap locations, protected standards, state directory, check commands, branch and merge policy, release mechanics, health checks, project gates. Tracked; holds no personal or machine fact. |
| Host contract | `LIFECYCLE-HOST.md` in the user-level contract directory | The person and machines running the loop: session command per host, hosting, human channel, notify command, node contract, resource limits, budgets, standing authorizations, driver settings. |
| Existing components | the orchestration contract (`ORCHESTRATION.md`), `impl` and its `code-orchestration-mode.md`, the project's development-rules doc, the agent-workspace skill, the node contract | Used as they are and cited by name; this skill restates none of them. |

Precedence: an authenticated human instruction, then the orchestration
contract's human authorization boundary, then the host contract and the
project doc, then this skill. A mismatch is reported, never repaired from
here. Every placeholder, its layer, and its default: `references/contract.md`.

## Doc resolution

- `LIFECYCLE.md` is read only at the repository root (strict contract, marker
  `<!-- runbook-contract: lifecycle v1 -->`). Missing → offer `init`.
- `LIFECYCLE-HOST.md` describes the person, not the project, and is read only
  from the user-level contract directory of the host, as the user's global
  instructions declare it. A project repository never holds it, so no workspace
  copy can shadow it, and the two files share no key.
- The orchestration contract resolves by its own rules (workspace copy, else
  user-level directory; see `code-orchestration-mode.md`, Model assignment).
- A value the stage needs that no layer declares and the skill does not
  default is missing, not guessed: that stage stops with **Contract
  incomplete**, names the value, and work that does not need it continues.

## Long-run mechanism

Full protocol: `references/long-run.md`. The rules that bind every session:

1. **One session, one step.** A session recovers, completes at most one step
   (intake plus one of: the cycle plan, one phase plan with its Plan Review,
   one dispatch round of a phase, one maintenance pass), writes the state, and
   exits. Context renewal is the next session, not a compaction.
2. **State lives in files.** The state directory declared by `LIFECYCLE.md`
   holds the agent-workspace files plus the run ledgers (`references/long-run.md`,
   State directory). Never in auto-memory: another host does not read it.
3. **The state line.** STATUS.md carries one machine-readable line,
   `lifecycle: state=<running|waiting-human|idle|done> cycle=<n>
   stage=<stage> step=<step> last=<last completed item>`. Only the main
   session writes it; a sub-agent never does.
4. **The driver** (`scripts/drive.py`) starts fresh sessions with the fixed
   resume prompt until the STOP file appears, the state leaves `running`, or
   the state line stays unchanged (or a session hits the session timeout) for
   the stalled-session limit. One driver per state directory; each session it
   starts carries the driver's pid in `LIFECYCLE_DRIVER_PID`.
5. **Recover before acting.** Read STOP, the state line, HANDOFF, the newest
   worklog entries, the open plan, and new inbox entries; verify the baseline
   and every dispatch STATUS records as running before reporting or
   re-dispatching it.
6. **Resource limits and bound facts** from the host contract go into every
   dispatch prompt, with the bound-facts checklist `impl` already requires.

## Stages

Stage details, outputs, and exit checks: `references/stages.md`.

The cycle plan is the orchestration contract's overall plan, and every stage
after it lives inside a phase of that plan, in this order: `arch` (only when
the cycle has spec deltas or open design points), the implementation phases,
and a last `release` phase. Each phase gets a phase plan, Plan Review,
dispatch, and the contract's audit and review seats. The controller plans,
dispatches, and records decisions; it never edits the spec, runs project
checks, or writes release files itself.

| Stage | Where | Does | Exit |
|---|---|---|---|
| Intake | each session start, controller | Quotes new inbox entries into `human-inputs.md`, adds health-check findings, triages into the backlog: hotfix, scope question, or ordinary item | Every new entry has a backlog id or a gate request |
| Cycle planning | controller, overall plan | Chooses the release content from the roadmap and backlog; writes the phases above with exit criteria, risk, budget, and the target version | The orchestration contract's requirements for an overall plan; Scope gate if the plan changes the roadmap's scope |
| Architecture design | phase `arch` | Workers write spec deltas; open design points become numbered decisions before any task cites them | Phase exit criteria met with independent review; Scope or Rules gate when the delta touches a gated item |
| Subtask design | start of every phase | Phase plan: tasks with one deliverable and one runnable check each, bound facts, disjoint file sets, input-to-expected tables for numeric units | Plan Review per the orchestration contract |
| Implementation | tasks of an implementation phase | Each task on its own branch or worktree via `impl task`; mechanical audit (checks plus rule check) and semantic review by seats other than the writer | Every task merged with current independent evidence, or reported BLOCKED |
| Phase integration | last task of each implementation phase | Merges the phase; full regression including earlier acceptance tests; phase acceptance report | Every exit criterion has evidence from this run |
| Cycle integration | first tasks of phase `release` | Full regression; spec-to-code drift audit; docs sync; performance against budget and previous release | No open drift, regression, or budget breach without a recorded decision |
| Delivery | last tasks of phase `release` | Version, changelog, acceptance report, clean-environment install smoke test, local tag; the controller notifies | Release recorded; publishing waits for its gate |
| Maintenance | controller; health checks as one dispatched task | Next cycle when the backlog has items; hotfix cycle for data loss, crash, or wrong numbers; idle when nothing is open | State set to `running` or `idle` |

A hotfix cycle preempts at the next stage boundary: STATUS records the
preempted cycle's stage and step, the fix branches from the latest release
tag (never from the integration branch), and the hotfix runs a phase with a
failing test first, then a `release` phase that delivers a patch. After the
patch delivery the fix merges back into the integration branch and the state
line returns to the recorded position. It adds an `arch` phase only when the
fix changes the spec.

## Human gates

The run stops for the human only here; everything else is decided, recorded
in the decision record, and carried forward.

| Gate | Arises when |
|---|---|
| Authorization boundary | Any item of the orchestration contract's human authorization boundary: publication (push, package upload, public release notes), paid compute, destroying data outside the run, changing goals or acceptance criteria |
| Commit authorization | The run needs a local commit, merge, or tag (at the latest, the first merge) and no recorded authorization covers local commits, merges, and tags on the run's branches; `init` asks for it up front |
| Budget | A cap in `<budgets>` is reached: finish the current step, record the usage in STATUS, then ask |
| Scope | A cycle plan, spec delta, or inbox entry adds or drops roadmap scope, changes a product principle, the public API, a runtime dependency, or a protected standard |
| Rules | A change to `LIFECYCLE.md`, the development-rules doc, linter configuration, the vendored rule check, or the host contract: these are human-owned |
| Ladder end | The orchestration contract's escalation ladder is exhausted |
| Project gates | Gates `LIFECYCLE.md` adds |

A standing authorization in the host contract covers a gate only when it
names the action and the object and every condition holds. At a gate: send
one request through the human channel, record it under HANDOFF "Waiting on
the human", continue independent work; when all remaining work waits, set
`state=waiting-human` and exit. A gate answer counts only when it arrives as
an authenticated human turn (roles.md §1); inbox entries and the resume
prompt are requests within the authorized run and grant no authority.

Driver sessions are non-interactive, so an answer never goes into one. To
answer: always `stop` the run first, also when it already reached
`waiting-human`, and wait for the current step to finish; once `driver.lock`
is gone, answer in an interactive session, which records the answer as H<n>
(`references/long-run.md`, Human input) and sets the state back to
`running`; then the human removes STOP and restarts the driver. A scheduled
restart starts the driver only when the state is `idle`.

## Development rules

The rules against over-defensive code and process, each with its check:
`references/development-rules.md`. They take effect through `impl`: `init`
proposes them as a section of the project's development-rules doc, so `impl
task` follows them and `impl check` reports them; `scripts/check_diff_rules.py`
is vendored into the project and runs in every mechanical audit. Hard rules
for every session and every dispatched writer:

1. Handle errors only at trust boundaries the spec names. No blind catch, no
   swallow-and-default, no fallback the spec does not define.
2. No defensive checks on values the code already guarantees; no option,
   flag, or config key the spec does not define; no compatibility shim before
   the first release; no abstraction with one implementation; delete code
   rather than comment it out; comments say why.
3. No inline lint or type suppression. An exception lives in the linter
   configuration with a recorded reason and passes the Rules gate.
4. Never loosen a tolerance, weaken or delete an assertion, add skip or
   xfail, or mock the unit under test to get green. Report BLOCKED with the
   failing output instead. A bug fix starts with a test that fails on the old
   code.
5. Finish in-scope work without asking; a plan, stub, or TODO is not an
   implementation. "Done" means the checks ran in this task on the final
   tree. Reports state facts.

Kept regardless: validation at trust boundaries, handling that prevents data
loss, security, resource cleanup.

## Red lines (non-negotiable)

1. One writer per state directory and per worktree. Never start a second
   driver. While a live process holds `driver.lock`, a session whose
   `LIFECYCLE_DRIVER_PID` does not name that process may only run `status`
   and `stop`.
2. No publication, paid action, or destructive action without its gate;
   integration ownership grants no commit or push authority (`impl` red line
   5). Commit, merge, and tag only under the recorded commit authorization.
3. Never edit a human-owned file: `INBOX.md`, `LIFECYCLE.md`, the host
   contract, the development-rules doc, linter configuration, protected spec
   sections. Propose the change at the Rules or Scope gate; `init` creates
   them only with the human's approval of the drafted content.
4. Never relabel FAIL or NOT RUN as PASS, never declare a phase done on
   coverage alone, and never script or pre-write a human confirmation.
5. Never write a personal or machine fact into a tracked project file;
   verbatim human words stay in the untracked state directory unless the
   project doc says otherwise.

## Subcommands

Route on the first token: `run | status | stop | init`. None or unknown →
print the state line and ask which.

### run
One step of the session protocol in `references/long-run.md`, then exit with
a one-paragraph report (step done, state line, what waits on the human). The
driver's resume prompt invokes exactly this.

### status
Read-only: the state line, cycle and stage, last completed item, gate
requests waiting, pending inbox entries, whether STOP exists, whether a
driver lock is held and by a live process.

### stop
Create `STOP` in the state directory with the reason and time. A running
session finishes its current step and exits; the driver starts no new
session and releases `driver.lock`. Only the human removes STOP.

### init
Follow `references/init.md` with `assets/LIFECYCLE.template.md` and
`assets/LIFECYCLE-HOST.template.md`. Never overwrite an existing doc without
explicit confirmation.

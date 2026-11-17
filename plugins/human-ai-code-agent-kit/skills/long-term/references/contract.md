# long-term contract interface (lifecycle v1)

This skill carries no environment facts. Every value below comes from one
layer only, so overriding one file can never drop a key of another:

- **P** — the project doc `LIFECYCLE.md` at the repository root. Tracked; may
  be shared or published. It holds what any contributor running the project
  would need, and nothing about a person or a machine.
- **U** — the host contract `LIFECYCLE-HOST.md`, read only from the
  user-level contract directory. It holds what belongs to the person running
  the loop and to their machines.
- **S** — this skill. Fixed protocol, plus defaults for some U keys.

The two file names differ, their keys are disjoint, and their lookup places
do not overlap (repository root versus user-level directory), so neither file
can shadow the other. When values differ per project, the host contract
keeps one row per project inside the same file instead of a second copy.
Angle brackets mark placeholders, never defaults.

## Missing values

- A **P** key that is missing: the stage that needs it stops with Contract
  incomplete and names the key; independent stages continue. P keys have no
  skill default, except where the table says so.
- A **U** key with an S default: the default applies and the first session
  of the run records that it applied.
- A **U** key without a default (`<session command>`): the driver cannot be
  started for that host; `run` still works in an interactive session.
- No `LIFECYCLE.md` at all: offer `init`. No host contract: offer
  `assets/LIFECYCLE-HOST.template.md` for the human to fill in; never fill a
  personal value by guessing.

## Project doc: `LIFECYCLE.md` (P)

Marker on line 1: `<!-- runbook-contract: lifecycle v1 -->`. Required H2
sections, exact headings, in this order:

```
## Sources
## State and records
## Checks
## Integration
## Delivery
## Maintenance
## Decisions and gates
```

Content inside a section is free-form; the skill reads it, it does not parse
it. Extra sections are allowed.

| Placeholder | Section | What it declares | Default |
|---|---|---|---|
| `<requirements>` | Sources | The human-written requirements document(s). Human-owned. | — |
| `<spec>` | Sources | The design or architecture spec, and which of its sections the agent may edit in Architecture design. | — |
| `<system scope>` | Sources | Who uses the product and what it must defend against: users, trust boundaries, threat model; or the spec section that states it. Reviewers judge findings against it. | — |
| `<protected standards>` | Sources | Files and sections only the human changes: requirement scope, acceptance criteria, protected spec sections, bundled standards. `LIFECYCLE.md`, the rules doc, and linter configuration are always included. | the always-included set |
| `<roadmap>` | Sources | Where milestones or releases and their acceptance lists live; how an exit criterion is numbered. | — |
| `<state dir>` | State and records | The run's state directory, relative to the repository root. Untracked, machine-local. | — |
| `<records dir>` | State and records | The directory for the run's records (worklog, plans, ledgers), relative to the repository root. Tracked, unless the project declares it untracked. | — |
| `<decision record>` | State and records | The tracked file that keeps product decisions (numbered, append-only), so they survive outside the state directory. Integration tasks append to it; the controller writes decisions to `<records dir>` only (`long-run.md`, State and records directories). | — |
| `<rules doc>` | Checks | The development-rules doc `impl` uses. | — |
| `<check commands>` | Checks | The full regression: format, lint, type check, unit, end-to-end, and doc checks, each with what passing looks like. | — |
| `<rule check>` | Checks | The command that runs the vendored `check_diff_rules.py` against a base ref. | — |
| `<performance budget>` | Checks | The benchmark command and where the budget is defined, or "none". | — |
| `<branch policy>` | Integration | Integration branch, per-task branch and worktree naming, hotfix branch naming (hotfix branches start from the latest release tag and merge back after the patch), merge method, and who merges. | — |
| `<drift map>` | Integration | How spec sections map to code for the drift audit, or "audit by reading". | audit by reading |
| `<docs to sync>` | Integration | Docs that must change with the code (README files, API docs, index files). | — |
| `<version source>` | Delivery | Where the version lives and the versioning scheme. | — |
| `<changelog>` | Delivery | The changelog file and its entry format. | — |
| `<acceptance reports>` | Delivery | Where phase and release acceptance reports go and their format. | — |
| `<install smoke>` | Delivery | Commands that install the release into a clean environment and prove it runs. | — |
| `<tag form>` | Delivery | The local tag name form. | — |
| `<publish steps>` | Delivery | What publishing means for this project (push, package upload, release page). Always behind the Authorization boundary gate. | — |
| `<health checks>` | Maintenance | Commands run during maintenance (dependency updates, vulnerability audit, benchmarks) and what counts as a finding. | — |
| `<hotfix classes>` | Maintenance | Defect classes that trigger a hotfix cycle beyond data loss, crash, wrong numbers. | data loss, crash, wrong numbers |
| `<agent decisions>` | Decisions and gates | What the controller may decide alone (narrowing the skill default) and the gates the project adds. | skill default (`stages.md`, Decisions) |

## Host contract: `LIFECYCLE-HOST.md` (U)

Read from the user-level contract directory only. The template is
`../assets/LIFECYCLE-HOST.template.md`.

| Placeholder | What it declares | Default (S) |
|---|---|---|
| `<orchestration contract>` | Which file, and the names of its work-mode section, human authorization boundary, escalation ladder, and the role table of each host. | `ORCHESTRATION.md`, resolved by its own rules |
| `<session command>` | Per host: the command that starts one fresh, non-interactive agent session in the repository root, taking the prompt as its last argument, with the permission and sandbox settings the run needs. | none: the driver cannot start |
| `<hosting>` | Where the driver runs and what the session needs around it (for example a terminal multiplexer the human channel depends on). | the current terminal |
| `<human channel>` | How an unattended session sends a gate request or heads-up to the human. Answers do not come back through it; they follow the answer procedure (`long-run.md`, Human input). | ask at the terminal; unattended, record the request in HANDOFF and set `waiting-human` |
| `<notify command>` | A command that sends a one-line notification, used by the driver. | none: the driver prints only |
| `<node contract>` | The multi-node contract whose start-of-work and end-of-work routines wrap each session, or "none". | none |
| `<personal vocabulary>` | The personal and machine words (names, host names, machine paths, account names) the records commit searches the staged diff for, in addition to the generic patterns (`long-run.md`, session protocol step 7). | none declared (generic patterns only) |
| `<resource limits>` | CPU, memory, parallel builds, and other host limits every dispatch prompt must carry. | none declared (dispatch prompts say so) |
| `<budgets>` | Caps per cycle on agent invocations or wall time, set by the human; reaching one opens the Budget gate (`stages.md`, Budget caps). Paid spending stays with the orchestration contract's boundary. | no cap: the contract's estimate only |
| `<standing authorizations>` | Human-written rows: action, project, scope, conditions, date. The commit authorization (local commits, merges, tags on the run's branches) may live here or as an H<n> recorded at `init`. | empty: every gate asks |
| `<driver settings>` | The `drive.py` options: `--max-stalled`, `--pause`, `--session-timeout`. The driver notifies on every stall and every stop. | 3 sessions; 600 s; 14400 s |
| `<projects>` | One row per project for any value above that differs per project. | — |

Fixed by the skill (S, not configurable): stage order, gate list, state and
records directory layouts, state line grammar, resume prompt, development rules,
recovery reads.

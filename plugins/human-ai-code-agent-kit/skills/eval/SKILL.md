---
name: eval
description: "suit-for-code-agent: Run, compare, or report checkpoint metrics under EVALUATION.md. Use for experiment evaluation requests, preserving cost, contention, overwrite, split, and reporting rules; never changes metric definitions."
---

# eval — evaluation operator

Role: AI Code Agent, operations mode (see `../../references/roles.md`; a
project-local ROLE.txt overrides it). You are an **operator, not a
developer**: never modify evaluation code or metric definitions. If the
runbook and reality disagree, report the mismatch and propose a doc update —
never improvise.

## Execution compatibility

For execution, read `../../references/execution-compatibility.md`. Guided
execution is the default. Existing explicit confirmation counts only under
its Authorization coverage rules; project-specific fresh-approval gates remain.

## Doc resolution

The project runbook is `EVALUATION.md` at the repository root. Contract and
parse rules: `references/contract.md`.

- Doc missing → say so and offer `eval init` (`references/init.md`).
- Marker `<!-- runbook-contract: eval v1 -->` absent → proceed, warn once.
- A required section missing → warn and ask; do not infer its content.

## Subcommand routing

Route on the first token: `init | run | compare | report`. No or unknown
arguments → list subcommands plus which runs already have metrics, ask which.

## Safety red lines (non-negotiable)

1. Before any GPU-heavy evaluation, check whether training is active (via
   EXPERIMENTS.md's monitoring commands if present) and warn about contention;
   proceed only with explicit authorization covering any observed contention.
2. Respect the doc's **cost guards**: steps it marks heavy/expensive need
   explicit confirmation, as does overriding a default skip.
3. Never delete or overwrite existing metric files without confirmation;
   re-running an evaluation that would overwrite counts.
4. `## Reporting rules` bind you (e.g. which split may be reported). If the
   user asks for something the rules forbid, refuse and cite the doc — they
   can change the doc, not bend the skill.

## Subcommands

### run
1. Read `## Running evaluation` + `## Environments`; verify prerequisites
   (containers/services up) and report any that are down with the doc's
   start command.
2. Resolve the orchestrator command for the given run dir; default checkpoint
   and split per `## Reporting rules`.
3. Show the planned command; use a documented read-only dry-run when useful.
   Check authorization coverage for the resolved plan, cost, contention, and
   overwrite effects. Covered approval → execute; otherwise ask for the gap.
4. Verify landing per `## Metrics layout` — including any documented location
   exceptions — and reply with a short table: family → file → written or
   failed.

### compare
Read `## Comparison`. Run the doc's comparison tool, then check the doc's
hazard conditions (e.g. dataset-consistency flags) BEFORE presenting numbers;
if a hazard fires, the warning leads the reply. Present the table and the
output file path.

### report
Read `references/report.md` for the stable format. Read-only: never triggers
evaluation. Missing metric families are listed as "not evaluated" with an
offer to `eval run`.

### init
Follow `references/init.md` with `assets/EVALUATION.template.md`. Never
overwrite an existing EVALUATION.md without explicit confirmation.

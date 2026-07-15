---
name: impl
description: "Implementation workflow for the AI Code Agent, driven by the project's development-rules doc (e.g. ProjectDevelopRule.md): take in and execute implementation task artifacts written by the human or research assistant, check the working tree for compliance with project rules before committing, and init a development-rules doc for a new project. Trigger when the user hands over a task document or asks to implement a specified change following project conventions; asks whether the current changes comply with project rules, are safe to commit, or follow test/commit conventions; or wants to set up development rules in a new project. Also trigger on explicit subcommands: impl init | task | check. <suit-for-code-agent>"
---

# impl — implementation workflow

Role: AI Code Agent, **implementation mode** (see `../../references/roles.md`;
a project-local ROLE.txt overrides it). Unlike exp/eval/ops, this skill DOES
change code — under the project's rules doc and the task artifact's scope.

## Doc resolution (loose contract)

The project rules doc is whatever the repo designates (common names:
`ProjectDevelopRule.md`, `DEVELOPMENT.md`, `CONTRIBUTING.md`; CLAUDE.md often
names it). Loose contract: read the whole doc (plus CLAUDE.md's conventions
section if present) and map onto the capability checklist in
`references/contract.md`. Doc missing → offer `impl init`.

## Orchestration for large tasks

A `task` that is large enough to decompose (a full implementation, a
migration, a large evaluation sweep) can run in **Code Orchestration Mode**:
the executing session becomes an orchestrator — decompose into per-module
units, dispatch implementation, verify each module independently, then a
single integration pass and one completion report. Small, clearly scoped
tasks stay single-thread as usual. See `references/code-orchestration-mode.md`.

## Safety red lines (non-negotiable)

1. **Scope is the task's, not yours.** No speculative refactors, no drive-by
   cleanups, no expanding a task because something nearby looks improvable.
   Out-of-scope findings are reported, not fixed.
2. **Respect the project's protected zones** — areas the rules doc or task
   marks as behavior-frozen (e.g. numerical behavior of training). If a task
   seems to require touching one, stop and surface the conflict.
3. Follow the rules doc's test placement, environment, and commit discipline
   exactly; when it conflicts with your habits, the doc wins.
4. Never commit without running `check` (below) on the working tree.

## Subcommands

### task
Execute an implementation task artifact (see roles.md §2: the task is the
execution target; decisions/references are context).

1. Read the task artifact fully; extract scope, deliverables, exact paths,
   constraints, non-goals, acceptance criteria; read the referenced
   decision/reference artifacts.
2. Inspect the current code before changing it (roles.md §3).
3. Ambiguity or conflict with repo reality → report per roles.md §7 before
   writing code (plan-then-execute gating, roles.md §4).
4. Implement within scope; follow the rules doc for placement, style, tests.
5. Validate per the acceptance criteria + the rules doc's required checks;
   report changed files, results, and open questions faithfully.

### check
Read-only compliance report of the current working tree against the rules
doc. Check at least: file/test placement rules, forbidden staging patterns
(e.g. blanket `git add -A` where the doc forbids it), commit-message rules
(e.g. no AI-attribution lines), protected-zone violations, leftover debug/
scratch files. Output one pass/fail line per rule with the offending paths;
end with "safe to commit" or the blocking items. Never auto-fix — report.

### init
Follow `references/init.md` with `assets/DEVELOPMENT.template.md` — only for
projects with no rules doc. Never overwrite one without confirmation.

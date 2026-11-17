<!-- runbook-contract: lifecycle v1 -->
# Lifecycle

<!-- The project's own process for a long lifecycle run. The long-term skill
     navigates by the exact H2 headings below; do not rename them. This file
     is tracked and may be published: no personal or machine facts (paths
     under a home directory, user or host names, model tiers, agent command
     lines). Those go in the host contract. Human-owned: agents propose
     changes, they do not edit it. A value left as TODO stops the stage that
     needs it. -->

## Sources

<!-- <requirements>: the human-written requirements document(s).
     <spec>: the design spec; which sections the agent may edit during
     architecture design, and which are protected.
     <system scope>: who uses the product and what it must defend against
     (users, trust boundaries, threat model), or the spec section that says
     so. Reviewers park findings outside it.
     <protected standards>: further files or sections only the human changes
     (acceptance criteria, bundled standards). This file, the rules doc, and
     linter configuration are always protected.
     <roadmap>: where milestones and their acceptance lists live; how exit
     criteria are numbered. -->

- Requirements: TODO
- Spec: TODO
- System scope: TODO
- Protected standards: TODO
- Roadmap: TODO

## State and records

<!-- <state dir>: the run's untracked, machine-local state directory relative
     to the repository root (verbatim human words live there).
     <records dir>: the tracked directory for the run's records (worklog,
     plans, ledgers), relative to the repository root.
     <decision record>: the tracked file for numbered product decisions. -->

- State directory: TODO
- Records directory: TODO
- Decision record: TODO

## Checks

<!-- <rules doc>: the development-rules doc impl uses.
     <check commands>: the full regression, one command per line, with what
     passing looks like.
     <rule check>: command for the vendored check_diff_rules.py.
     <performance budget>: benchmark command and where the budget is
     defined, or "none". -->

- Rules doc: TODO
- Check commands: TODO
- Rule check: TODO
- Performance budget: TODO

## Integration

<!-- <branch policy>: integration branch, per-task branch and worktree
     naming, hotfix branch naming (from the latest release tag, merged back
     after the patch), merge method, who merges.
     <drift map>: spec sections to code, or "audit by reading".
     <docs to sync>: docs that change with the code. -->

- Branch policy: TODO
- Drift map: audit by reading
- Docs to sync: TODO

## Delivery

<!-- <version source>, <changelog>, <acceptance reports>, <install smoke>,
     <tag form>, <publish steps>. Publishing always waits for the human's
     authorization. -->

- Version source: TODO
- Changelog: TODO
- Acceptance reports: TODO
- Install smoke: TODO
- Tag form: TODO
- Publish steps: TODO

## Maintenance

<!-- <health checks>: commands and what counts as a finding.
     <hotfix classes>: classes beyond data loss, crash, wrong numbers. -->

- Health checks: TODO
- Hotfix classes: data loss, crash, wrong numbers

## Decisions and gates

<!-- <agent decisions>: narrow what the controller may decide alone, and
     add project gates. Leave "skill default" to keep the skill's list. -->

- Agent decisions: skill default
- Project gates: none

# impl init — establish a development-rules doc

Only for projects with NO rules doc. If one exists (ProjectDevelopRule.md,
DEVELOPMENT.md, CONTRIBUTING.md, or named by CLAUDE.md), impl consumes it
as-is — init must not rewrite it without explicit confirmation.

## Procedure

1. **Guard.** Existing rules doc → stop; offer only user-approved appends.
2. **Explore.** Infer current conventions from the repo: directory layout,
   test locations, commit-message history (`git log --oneline -30`),
   CI config, linter configs, agent-instruction files.
3. **Interview** for policy the repo can't show: protected zones, commit
   style rules, environment mandates, task/direct-instruction conventions,
   generated/implicit writes, repository-wide mutators, exclusive resources,
   and parallel validation boundaries.
4. **Draft** from `../assets/DEVELOPMENT.template.md` (headings advisory —
   the eleven capabilities in `contract.md` must be answered).
5. **Review gate** → write → suggest committing.
6. **Smoke.** Run `impl check` against the current working tree using the
   new doc; the report should be actionable, not vacuous.

# exp init — establish EXPERIMENTS.md for a project

Goal: produce a contract-conforming `EXPERIMENTS.md` at the repo root
(contract: `contract.md`; skeleton: `../assets/EXPERIMENTS.template.md`).

## Procedure

1. **Guard.** If `EXPERIMENTS.md` already exists, show its first lines and ask
   for explicit confirmation before replacing or rewriting it. Never silently
   overwrite.
2. **Explore before asking.** Gather evidence from the repo itself:
   - launch surface: training entry points, wrapper scripts (look in
     `scripts/`, `Makefile`, `justfile`, CI configs), their subcommands, env
     vars, and defaults — read the actual script, don't guess;
   - configs: templates, validation code, the baseline config name;
   - run outputs: where past runs landed, their directory naming, summary
     files/keys (open one or two real run dirs if present);
   - monitoring: log locations, PID bookkeeping, GPU tooling;
   - existing docs (README, CLAUDE.md, operations runbooks) for stated
     conventions — note where docs contradict code, and trust the code.
3. **Interview only for the genuine gaps** — things the repo cannot tell you:
   resource ceilings learned from experience (OOM limits), conventions that
   are policy rather than code (e.g. "label is mandatory"), which environments
   exist beyond this machine, known footguns. Ask few, targeted questions;
   proceed on reasonable inference where the user has no answer, and mark
   inferences in the doc draft.
4. **Draft** the doc from the template: fill every required section; put the
   contract marker on line 1; institutional knowledge goes into
   `## Pre-flight checklist` as mechanically checkable items; keep the tone
   operational (commands + facts, no motivational prose). English unless the
   project's docs are consistently in another language.
5. **Review gate.** Show the draft (or a tight summary plus the full file) to
   the user; write to `EXPERIMENTS.md` only after approval. Suggest committing
   it so remote checkouts see the same runbook.
6. **Smoke.** Run one read-only subcommand (`status` or `registry`) against
   the new doc to prove the sections are actionable; fix the doc if not.

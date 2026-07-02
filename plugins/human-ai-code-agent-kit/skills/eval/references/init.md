# eval init — establish EVALUATION.md for a project

Goal: a contract-conforming `EVALUATION.md` at the repo root (contract:
`contract.md`; skeleton: `../assets/EVALUATION.template.md`).

## Procedure

1. **Guard.** Existing EVALUATION.md → show its head, ask before replacing.
2. **Explore before asking.** Evidence from the repo:
   - evaluation entry points (look for `scripts/eval*`, `evaluate*`,
     benchmark configs, CI eval jobs); read the orchestrator's CLI surface;
   - where metrics of past runs actually landed (open a real evaluated run
     dir if one exists) — trust files on disk over README claims;
   - per-family scripts and which environment/container each needs;
   - comparison tooling and any consistency flags it emits;
   - stated conventions in READMEs/notebooks (which split, which checkpoint).
3. **Interview only genuine gaps**: reporting policy (allowed split, default
   checkpoint), which steps are considered expensive, known invalid-comparison
   traps. Few, targeted questions; mark inferences in the draft.
4. **Draft** from the template; marker on line 1; every required section
   filled; cost guards and location exceptions must be explicit — they are
   what the `run` subcommand verifies against.
5. **Review gate.** User approves → write `EVALUATION.md`; suggest committing.
6. **Smoke.** Run `report` on an already-evaluated run (or state clearly that
   none exists yet) to prove the layout section is accurate.

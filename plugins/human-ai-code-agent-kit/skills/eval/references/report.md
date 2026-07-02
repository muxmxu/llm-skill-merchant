# eval report — stable report format

Read-only summary of a run's existing metrics. Same input → same structure,
so reports are comparable across runs and sessions.

## Structure

1. **Header** — run dir, checkpoint(s) covered, dataset identity (as the
   metrics' meta records it), split, evaluation timestamps if recorded.
2. **One section per metric family** found via `## Metrics layout`, in the
   doc's listing order. Summary statistics only (the files' summary blocks);
   never dump per-record data unless the user asks. 3-4 significant digits.
3. **Not evaluated** — families defined in the doc but absent for this run,
   each with the command that would produce it (offer `eval run`).
4. **Caveats** — echo the doc's mandatory disclosures (`## Reporting rules`)
   plus any location exceptions that affected where data was read from.

## Rules

- Only report what `## Reporting rules` allows (split, checkpoint policy) —
  even if other data exists on disk, mention its existence, don't report its
  numbers unless the user explicitly overrides with awareness of the rule.
- Missing/corrupt file → `—` plus a note; never a crash, never a guess.
- Multi-variant metrics (e.g. two model variants evaluated side by side) get one
  sub-row per variant, labeled with the doc's vocabulary.

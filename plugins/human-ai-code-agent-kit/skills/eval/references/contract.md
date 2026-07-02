# EVALUATION.md contract (eval v1)

Marker: first line of the doc is `<!-- runbook-contract: eval v1 -->`.

## Required H2 sections (exact headings)

```
## Overview
## Environments
## Running evaluation
## Metrics layout
## Comparison
## Reporting rules
## Safety rules
```

Extra sections allowed and ignored unless a subcommand needs them. Section
bodies are free-form.

## Section semantics

- **Overview** — the metric families that exist and what each measures.
- **Environments** — which environment/container/service each family needs,
  how to check it is up, and how to start it.
- **Running evaluation** — orchestrator command(s) with flags and defaults;
  execution-order dependencies (e.g. a dump stage gating others); **cost
  guards**: which steps are heavy, what is skipped by default, and which
  flags override the skips.
- **Metrics layout** — where results land (paths + file naming + rough
  schema), including every location exception; any caveats about derived
  artifacts (e.g. normalized outputs unfit for certain metrics).
- **Comparison** — the cross-run comparison tool and its hazard conditions
  (consistency flags that make comparisons invalid) and how to check them.
- **Reporting rules** — binding rules for what may be reported: split
  restrictions, default checkpoint, mandatory caveats/disclosures.
- **Safety rules** — project-specific red lines, additive to the skill's.

## Genericity rule

Headings and semantics must fit an arbitrary ML project; all specifics live
in the bodies.

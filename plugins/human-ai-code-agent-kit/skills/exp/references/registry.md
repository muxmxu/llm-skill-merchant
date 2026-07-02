# exp registry — run inventory table

Build an on-demand inventory of past runs. No persistent registry file unless
the project doc says otherwise (a stored table goes stale silently).

## Procedure

1. Read `## Run directory layout` (where runs live, naming scheme, summary
   files) and `## Registry fields` (columns + where each comes from).
2. Enumerate run dirs; parse each field from its stated source (JSON keys,
   filenames, config snapshots). Read only what the fields need — not whole
   epoch histories.
3. Emit ONE markdown table, newest first. Column order: identity (date,
   label), config essentials, outcome metrics, notes/flags.

## Robustness rules

- A missing file or key renders as `—`; a malformed run gets a `⚠` in a notes
  column. Never abort the whole table because one run is broken.
- Nested sub-runs (e.g. second-phase runs inside a parent run dir) are listed
  as indented/flagged rows if `## Registry fields` mentions them.
- Numbers: keep 3-4 significant digits; do not restate units per cell if the
  header can carry them.
- Deterministic output: same repo state → same table (stable sort, stable
  columns) so diffs between invocations are meaningful.

## Large tables

More than ~12 rows: still print the markdown table, and offer to render an
HTML artifact (sortable, with a per-column legend) as a companion view.

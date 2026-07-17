# Development-rules contract (impl v1, loose)

Optional marker (recognized, never required):
`<!-- runbook-contract: impl v1 (loose) -->`

No required headings — rules docs vary widely. The doc (plus the repo's agent
instructions file, e.g. CLAUDE.md) must answer the following capabilities
somewhere; the skill reads holistically.

## Capability checklist

1. **Read order / context entry points** — what to read before any task.
2. **Execution environment** — where code runs and is tested (container,
   venv), and what is forbidden (e.g. host execution).
3. **Code organization** — where library code vs entry points vs scripts
   live; import/façade conventions.
4. **Test placement & boundaries** — where tests go, what kinds exist,
   any explicit exceptions.
5. **Commit & staging discipline** — message style, forbidden patterns
   (blanket adds, attribution lines), what must never be committed.
6. **Protected zones** — code whose behavior must not change without
   explicit sanction (e.g. numerics), and the verification expected when
   near them.
7. **Task artifact conventions** — where implementation tasks come from and
   their expected structure, plus how direct authenticated maintenance or
   implementation instructions are identified (ties into roles.md §2).
8. **Generated and implicit writes** — lockfiles, generated outputs, caches,
   snapshots, shared metadata, and other paths commands may rewrite.
9. **Repository-wide mutators** — formatters, generators, migrations, or build
   steps that must be serialized across otherwise independent modules.
10. **Exclusive resources** — ports, databases, fixtures, build caches,
    devices, and directories that require locks during parallel work.
11. **Parallel validation boundaries** — checks safe to run concurrently,
    checks that mutate shared state, and the required final-tree/end-to-end
    validation after all writers stop.

## Gap handling

Missing capability → name it, ask, and offer to append the answer to the doc
with approval. `check` reports "no rule found" for capabilities the doc
doesn't cover rather than inventing rules. If a missing capability makes
parallel execution unsafe, serialize the affected work or keep it
single-threaded until the project defines the boundary.

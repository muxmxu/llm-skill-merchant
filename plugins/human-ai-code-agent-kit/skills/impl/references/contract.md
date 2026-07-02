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
   their expected structure (ties into roles.md §2).

## Gap handling

Missing capability → name it, ask, and offer to append the answer to the doc
with approval. `check` reports "no rule found" for capabilities the doc
doesn't cover rather than inventing rules.

# ops init — establish an operations runbook

Only for projects that have NO operations runbook yet. If `OPERATIONS.md`
exists, ops consumes it as-is (loose contract) — init is not needed and must
not rewrite it without explicit confirmation.

## Procedure

1. **Guard.** Existing OPERATIONS.md → stop; offer only the optional marker
   line or user-approved gap-filling appends.
2. **Explore.** Look for cloud/cluster tooling: provider CLIs in scripts,
   `*.env` files naming resources, ssh configs, sync scripts, watchdog/cron
   tooling, CI deploy jobs. Identify which of the nine capabilities
   (`contract.md`) the repo already implements in scripts.
3. **Interview** for what scripts can't say: cost model and discipline,
   forbidden operations, who else uses the machine, watchdog policy,
   session-end expectations.
4. **Draft** from `../assets/OPERATIONS.template.md`: the template's headings
   mirror the nine capabilities but are advisory — reorganize freely as long
   as every capability is answered. Hard rules (forbidden commands,
   session-end invariant) must be stated as rules, not prose asides.
5. **Review gate** → write → suggest committing.
6. **Smoke.** Run the doc's status/cost query (read-only) to prove
   capability 9 works as written.

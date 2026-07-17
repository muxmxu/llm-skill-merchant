<!-- runbook-contract: impl v1 (loose) -->
# Development Rules

<!-- Loose contract: headings are ADVISORY — reorganize freely, but the eleven
     capabilities (see the impl skill's contract.md) must all be answered. -->

## Read order before any task

<!-- Context entry points an agent must read first. -->

## Execution environment

<!-- Where code runs and is tested; what is forbidden. -->

## Code organization

<!-- Library code vs entry points vs scripts; import conventions. -->

## Tests

<!-- Placement, kinds, boundaries, explicit exceptions. -->

## Commit & staging discipline

<!-- Message style; forbidden patterns (e.g. blanket adds, attribution
     lines); what must never be committed. -->

## Protected zones

<!-- Code whose behavior must not change without explicit sanction, and the
     verification expected when working near it. -->

## Task artifacts

<!-- Where implementation tasks come from and their expected structure; how
     direct authenticated implementation instructions are identified. -->

## Generated and implicit writes

<!-- Lockfiles, generated outputs, caches, snapshots, shared metadata, and
     other paths that tools may rewrite. -->

## Repository-wide mutators

<!-- Formatters, generators, migrations, or builds that must be serialized. -->

## Exclusive resources

<!-- Ports, databases, fixtures, build caches, devices, and directories that
     require locks during parallel work. -->

## Parallel validation boundaries

<!-- Checks safe to run concurrently; checks that mutate shared state; final-
     tree and end-to-end checks required after all writers stop. -->

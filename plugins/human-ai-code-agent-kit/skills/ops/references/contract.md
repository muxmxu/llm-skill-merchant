# OPERATIONS.md contract (ops v1, loose)

Optional marker (recognized, never required):
`<!-- runbook-contract: ops v1 (loose) -->`

Operations runbooks are short, hand-maintained, and evolve with the tooling —
so this contract requires NO fixed headings. Instead, the doc must answer the
capabilities below (1–9 required, 10 optional) **somewhere** in its text. The
skill reads the whole doc and maps subcommands to content; heading names are
irrelevant.

## Capability checklist

1. **Cost/billing discipline** — what costs money, what releases it, any
   forbidden operations (e.g. a stop mode that keeps billing).
2. **Start compute** — how to start/boot the machine and verify it is up.
3. **Connect** — how to reach it (ssh, port, credentials location).
4. **Code-sync discipline** — how code gets to the machine and what is
   forbidden (e.g. direct edits).
5. **Experiment handoff** — how experiments launch there (typically: the
   experiment runbook's remote selector).
6. **Watchdog / monitoring** — the unattended-monitoring tool, its flags,
   its single-instance rules.
7. **Results sync home** — how outputs return, including multi-run cases.
8. **Release + verification** — the teardown procedure AND the command that
   verifies the released/billing state.
9. **Status / cost query** — read-only commands for power/billing state.
10. **Incident playbooks** *(optional but recommended)* — symptom-keyed
    decision trees for degraded modes (machine unreachable, connections
    blocked, provider errors), each with its FORBIDDEN-actions list first.
    Absent → the `incident` subcommand's freeze-and-report default applies;
    after any real incident, offer to add the missing playbook (with the
    facts measured during the incident) so the next one is covered.

## Gap handling

If a subcommand needs a capability the doc does not answer: name the missing
capability number, ask the user for the procedure, and offer to append it to
the doc (with approval). Do not improvise cloud CLI commands from memory.

## Genericity rule

The checklist must fit any remote/billed compute (cloud VM, cluster,
colocated box). Provider-specific commands belong in the doc, never here.

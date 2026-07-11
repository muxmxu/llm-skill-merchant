# Task Dispatch & Supervision (assistant side)

Closes the loop that the derivation chain opens. The chain ends at
code-agent-facing artifacts (Progress, Task); this protocol carries them to
an executing code agent, supervises the run, and brings results back to the
human:

```
0. Human gives a task / approves a plan
1. Assistant plans + derives artifacts   (Log → Progress → Task, existing modes)
2. Review gate                           (adversarial sub-agent check → refine)
3. Delivery                              (commit artifacts to the delivery bus)
4. Dispatch                              (kick off the code-agent endpoint)
5. Supervision                           (cheap watchdog; escalate only when real)
6. Return                                (pull reports, verify, deliver to human)
```

The counterpart contract for the executing side is
`code-agent-execution.md`. Workspace facts (bus repo, endpoints, nudge
token) live in `RESEARCH-CONTEXT.md` under `## Dispatch & code agents` —
this file carries no host names, paths, or session names.

## Preconditions

- The human asked for execution (not just artifacts) — dispatch is never
  implied by artifact-writing alone.
- `RESEARCH-CONTEXT.md` has a `## Dispatch & code agents` section. Missing →
  say so and ask; do not improvise endpoints.
- Human-owned decisions are settled before dispatch: evaluation scale,
  runtime ceiling, anything that changes a paper claim. Ask once, early —
  not mid-run.

## Stage 1 — Plan + artifacts

Use the existing modes; this protocol adds only ordering and recon:

- **Recon before writing** (read-only; may include authorized SSH and
  fanout sub-agents): verify every path/checkpoint/function the task will
  cite. Facts get provenance tags (verified-in-code / observed-on-server /
  from-human-log); anything unverifiable is routed into the task's own
  recon step as "re-verify on site", never stated as fact.
- Derivation order is strict: Research Log (human-facing decisions) →
  Progress (Decision blocks) → Tasks (strict template). A scope change
  mid-writing (scale, extra measurement) is applied to all three layers —
  stale numbers in the upstream log are a review-gate finding.

## Stage 2 — Review gate

Before delivery, fan out independent reviewer sub-agents over the artifact
set (log + progress + tasks). Standard lenses: fabrication (every
path/number/signature vs the repo and source logs), template compliance
(kit templates + the workspace's own exemplars), executability (simulate
the executing agent; ambiguities, missing inputs, undecidable acceptance
criteria), cross-layer consistency. Fix findings; the human may cap rounds
(a stop signal from the human ends the gate). Reviewer model tier: capable-but-cheap
(never the top tier; see the sub-agent tiering rule in the user's
memory/config).

## Stage 3 — Delivery (the bus)

Artifacts travel through the **delivery bus** named in RESEARCH-CONTEXT.md
— typically a small git repo (often nested inside the code repo and
gitignored by it) with its own remote. Commit the batch, push, done. The
bus is bidirectional: completion reports come back on the same repo. Never
deliver by pasting task bodies into the endpoint session — the bus is the
auditable copy.

## Stage 4 — Dispatch

Endpoints and transports come from RESEARCH-CONTEXT.md. Known transports:

- **remote-tmux**: `ssh <host> tmux send-keys -t <session> -l "<kickoff>"`,
  then Enter; confirm reception via `capture-pane`. Non-interactive SSH may
  lack the login PATH — probe with a login shell (`zsh -lic`) before
  concluding a tool is absent.
- **local-subagent**: spawn a sub-agent of the assistant session with the
  task file paths and the execution contract; suitable when the work runs
  on the local machine or the assistant's harness can reach the compute.

The kickoff message is short and single-line; the task files carry the
detail: pull the bus → read progress + tasks → execute per
`code-agent-execution.md` → deliver via the bus. Late additions (a new task
in the same batch) are pushed to the bus first, then announced with the
same kickoff shape.

## Stage 5 — Supervision (cheap watchdog)

Cost rule: polling must not wake the assistant's main model. Layer it:

1. **Zero-token shell monitor** for the one clean terminal signal — a bus
   push. This is the fail-safe and may be the only layer.
2. **Small-model watcher agent** (cheapest tier) for fuzzy signals: reads
   the endpoint's screen periodically, semantically filters false positives
   (stale scrollback residue, the agent's own grep/monitor commands
   containing "Error"), and escalates to the main assistant only on: delivery, a real
   error, a dead stall, self-heal failure, or a time cap.
3. **Self-heal**: if the endpoint session stalls on a usage-limit reset,
   the watcher may send exactly the agreed nudge token (from
   RESEARCH-CONTEXT.md) after the reset time — and nothing else, ever.
   This is the single authorized write into the endpoint session; all other
   observation is read-only.

## Stage 6 — Return

On the delivery signal: pull the bus, read completion reports. Evidence
discipline applies to the results themselves — spot-check reported numbers
against the raw result files before quoting them to the human (sub-agents
fabricate; completion reports are claims, not facts). Then deliver: outcome
first, numbers, deviations/caveats, and what it changes upstream (paper
claim, log entry). Feed durable results back into the research log as a new
entry — the loop re-enters the chain at the top.

## Boundaries

- The assistant never edits the code repo on the endpoint, never runs
  training, never shrinks a human-fixed scale. Runtime blowups and
  contradictions with repo conventions go back to the human.
- Approval in one batch does not carry to the next: each dispatch batch
  gets its own human go-ahead (a standing instruction from the human can
  widen this, but that instruction lives with the human, not this file).

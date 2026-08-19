# RA Orchestration Mode

## Mode statement

Use this mode only for explicit dispatch, parallel work, external endpoints,
high-risk delivery, or large-scale work. It is not the default for ordinary
discussion, explanation, or one human-facing log. When it applies, the
top-level session runs a five-phase loop:

```
0. Clarify    — restate understanding; surface ambiguities; confirm
1. Plan       — a short plan before dispatch, for anything non-trivial
2. Decompose  — break the plan into self-contained dispatchable units
3. Dispatch   — send each unit to a sub-agent / Workflow at its assigned model+effort
4. Verify &   — independently check what comes back; report outcome,
   Report       deviations, and what changes upstream
```

The top-level session may write a small, human-facing response directly when
that is the requested work. Delegate only when delegation improves reliability,
coverage, or turnaround; do not create a completion pipeline for a simple
conversation or a single log.

## Phase 0 — Clarification gate

Before planning, tier-1 restates its understanding of the task and lists
open ambiguities. If the human's prompt already states a clear goal, this is
a fast single-pass confirmation, not an interview — do not manufacture
questions when intent is already unambiguous. Genuine gaps get a question;
this happens in **at most one round** — once the human answers, proceed,
don't loop back for more.

For anything non-trivial, a short plan comes before dispatch: it lets the
human redirect early, and it gives decomposition a concrete unit list to
hand to sub-agents. When the plan itself needs current-state evidence to be
concrete (what does the repo actually look like, what does the log actually
say), that exploration is itself dispatched to **read-only** sub-agents —
tier-1 does not read the codebase or the vault to build the plan; it reads
the sub-agent's report.

## Delegation prompt discipline

Tier-1's distinguishing value in this mode is not doing the work — it is
**compressing context into a self-contained prompt** that lets a cheaper
model do the work correctly on the first pass. A dispatch prompt carries
everything the sub-agent needs: scope, source paths, acceptance criteria,
output format, and the model/effort it should run at. Nothing is left
implicit. The better the prompt, the further down the model-cost ladder
tier-1 can safely delegate.

Before a dispatch that can change external state or materially affect a result,
tier-1 works through a **bound-facts checklist**: enumerate every fact whose
mistake would change that result or external state — the exact run or checkpoint (path or ID), the
dataset and its version, config-file paths, model and tool versions, the
target environment identifier — and for each one either pin a precise value
or name exactly where the sub-agent is to obtain it (which file to read,
which command to run). An item that is neither pinned nor sourced is
unresolved, and an unresolved item blocks the dispatch. This is not
paperwork: a sub-agent missing a bound fact does not stop to ask for it — it
improvises, adopts whatever on disk looks close, and drifts further off with
every step. The fact has to arrive in the prompt, or the task has to
genuinely not need it.

A sub-agent should never need to ask tier-1 a clarifying question mid-task —
if it would, the prompt was underspecified and should be fixed, not patched
over in a follow-up message. Sub-agents never inherit tier-1's own model:
every dispatch call sets model/effort explicitly, per the profile resolved
from `ORCHESTRATION.md` (below).

## Quality defaults

High-risk or externally consequential deliverables clear an independent
verification before they reach the human:

- **Closed-book reverification** of any number that ends up quoted in a
  report — the checker re-derives it from source, not from the writer's own
  claim.
- **Snapshot diff** of before/after state to keep a change within its
  intended scope.
- **Instruction-following audit** — did the sub-agent do what was asked, no
  more and no less.

Default to **at most two rework rounds**; a disagreement that survives two
rounds goes to the human to arbitrate rather than looping further. Any task
that touches tabular or numeric data leaves a **re-runnable trace** (a
script plus its source path), not just a pasted number, so the human or a
future sub-agent can independently reproduce it.

Keep process status in an orchestration worklog. Surface it in ordinary prose
only when it changes a research conclusion, decision, or the user's next
action.

## Human intervention and channel selection

A human supervising a run must be able to correct it mid-flight. The failure
this guards against is concrete: a binding fact that was clear in the main
conversation ("use the checkpoint from *this* run, that version") never
reaches the sub-agent, which then improvises and drifts further off with
every step. How reachable an in-flight job is depends entirely on the channel
it was dispatched through, so tier-1 chooses the channel with
interruptibility in mind, not cost alone.

**Channel interruptibility tiers**, most reachable first:

- **Directly interruptible** — the human can enter the execution session
  itself (for example an attachable, long-lived terminal session) and type
  into it directly. For a session outside the bus dispatch contract this
  corrects the work in place; for a bus-governed endpoint the typing triggers
  a reversible safe pause only, and the binding correction still travels the
  bus (see the reconciliation note below).
- **Relay-interruptible** — the human speaks into the main conversation and
  tier-1 immediately forwards the correction to the in-flight agent; reach is
  one hop away and depends on tier-1 staying responsive.
- **Non-interruptible in flight** — a scripted orchestration pipeline that,
  once launched, accepts no mid-run input: the only correction path is to stop
  the whole run, fix it, and resume.

**Bus-governed endpoints and direct typing.** Reachability is layered, and
where a job runs on an endpoint bound by the bus dispatch contract
(`task-dispatch.md`) — whether or not it is a tmux session — that contract
governs what counts as a binding instruction and overrides the picture above.
On the executor side, text a human types straight into such a session is
`unverified`: its effect is to trigger a reversible safe pause — a feature,
not a defect: you type, it stops — never to change the work in place. The
binding correction must travel the bus: a new revision, re-dispatched under
the `DISPATCH` grammar and taken up at a safe boundary, per `task-dispatch.md`
Stage 4's revision/supersede flow. The full "attach and type to correct the
work in place" reading of the *directly interruptible* tier applies only to a
session that is **not** under the bus dispatch contract.

**Channel selection.** A task of the kind a human is likely to correct
mid-flight — its bound-facts checklist is not yet complete, or it is
exploratory, or it is a first-time-through run — must not go into a
non-interruptible channel; it goes to an interruptible one. A
non-interruptible channel is reserved for mechanical, bulk work whose bound
facts are fully closed and whose acceptance criteria are unambiguous, and even
then its entrance passes the bound-facts checklist first — two gates, not one.

**In-flight intervention protocol.** A human interjection mid-run is a
first-class event, not an interruption to be worked around. Tier-1 runs a
fixed sequence: (a) size the blast radius — which in-flight tasks the
correction touches; (b) propagate it through each affected job's channel — a
correction work-order into a directly interruptible session, except that a
bus-governed endpoint takes the binding correction as a new bus revision
(Stage 4) while direct typing only safe-pauses it; an immediate forward into
a relay-interruptible one; a stop-fix-resume for a non-interruptible one;
(c) record the correction into the log or decision
record, so it is durable and does not live only in the conversation.

**Non-blocking discipline.** Tier-1 never sits in a synchronous blocking wait:
every dispatch is backgrounded and the main conversation stays open to
interruption at all times. The moment tier-1 blocks, the human's entire
intervention channel goes dead — a blocked orchestrator can neither receive a
correction nor propagate one.

## `ORCHESTRATION.md` contract

The research-assistant kit carries this mode's methodology only; which
model/effort handles which task type is a workspace fact, and workspace
facts do not belong in the kit (same separation `research-context.md`
enforces for `RESEARCH-CONTEXT.md`). That fact lives in a file the skill
reads: `ORCHESTRATION.md`, at the research-workspace root, alongside
`RESEARCH-CONTEXT.md`.

Marker: first line of the doc is `<!-- runbook-contract: ra-orchestration v1 -->`.

### What the doc is (and is not)

- A **human-owned dispatch table**: task type → model assignment profile.
  The human writes and edits it directly; tier-1 reads it and never rewrites
  it unprompted. It is the single place model-tier decisions for delegation
  live — do not re-litigate model choice in conversation once the table
  covers a task type.
- **Not methodology.** How to clarify, plan, decompose, dispatch, and verify
  lives in this reference file. `ORCHESTRATION.md` answers only "which
  model, at what effort, for this kind of task" — never how the loop itself
  runs.

### Doc resolution

- Needed when this orchestration mode is selected; resolve a profile before the
  first dispatch call.
- Doc missing → say so once, fall back to the built-in conservative default
  profile (below) for the current task, and proactively offer to draft the
  file (starter rows from the task types actually seen in this workspace) —
  gated on human review before writing, per its human-owned status.
- Doc present but the task's type is not covered by any row → use the
  `fallback` row. No `fallback` row either → apply the built-in default for
  this single task instance and flag the gap to the human as an opportunity
  to add a row; do not block the task on it.
- Marker missing or an older contract version → proceed, warn once, offer
  to conform/upgrade. Never hard-fail on a version mismatch.
- A task spans multiple task types → resolve each covered role
  (clarification depth, writer, semantic reviewer, mechanical auditor,
  independent-verification strength) to the **more capable assignment** among the
  matching rows. Never average down to the weaker row.

### Built-in conservative default profile

Used only when `ORCHESTRATION.md` is missing or has no matching/fallback
row. Stated as capability tiers, not vendor model names — the kit must stay
valid for a workspace on any provider (Anthropic, DeepSeek, OpenAI, ...),
consistent with the Genericity rule below:

- Writer: a capable mid-tier model, high effort.
- Semantic reviewer: a top-tier reasoning model.
- Mechanical auditor: a capable mid-tier model, high effort.
- Clarification depth: one round, ask-if-ambiguous.
- Independent-verification strength: full (closed-book + snapshot diff).

### Required columns (exact names)

```
Task Type | Clarification Depth | Writer | Semantic Reviewer |
Mechanical Auditor | Independent Verification Strength | Notes
```

Column names may be localized to the workspace's working language, as long
as each localized column's order and semantics map one-to-one to this
schema (e.g. a Chinese `ORCHESTRATION.md` may render the header row as
任务类型 / 澄清深度 / writer / 语义 reviewer / 机械审计 / 独立核验 / 备注).

- **Task Type** — the kind of work being dispatched (paper writing,
  literature survey, evidence-pack assembly, slide/figure production, log
  writing, dispatch-task drafting, data engineering, ...). Workspace-defined
  — the contract does not prescribe which types exist.
- **Clarification Depth** — how much Phase 0 interviewing this task type
  needs before planning (e.g. "none — proceed on a clear prompt", "one round
  if ambiguous", "always confirm scope first").
- **Writer** — model + effort that produces the artifact itself.
- **Semantic Reviewer** — model + effort that checks claims, wording, and
  meaning (not raw numbers).
- **Mechanical Auditor** — model + effort that does closed-book
  number-checking and completeness sweeps.
- **Independent Verification Strength** — how hard the Quality Defaults check runs
  for this task type (e.g. "required: closed-book + snapshot diff",
  "single-pass recheck", "skip — low-stakes").
- **Notes** — task-type-specific discipline that doesn't fit another column
  (e.g. a log-writing row pointing to the workspace's author-source rule; a survey
  row noting numbers need independent verification before entering the
  vault).

### Genericity rule

This contract carries schema and resolution rules only — no literal task
types, model names, or workspace paths belong in this file. Every workspace
writes its own `ORCHESTRATION.md` body; the contract must stay valid for an
arbitrary research workspace, mirroring the contract/fact separation
`research-context.md` establishes for `RESEARCH-CONTEXT.md`.

## Host-specific execution tips

Harness-specific dispatch mechanics (per-call effort parameters, Agent-tool
limitations, workflow resume constraints, interruptibility tiers) live in
`references/claude-code-workflow-tips.md`; read it only when the executing
harness is Claude Code. They are kept out of this file so the methodology
above stays valid for any provider, per the genericity rule.

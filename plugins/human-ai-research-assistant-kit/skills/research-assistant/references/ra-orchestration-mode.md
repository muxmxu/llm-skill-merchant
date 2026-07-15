# RA Orchestration Mode

## Mode statement

Whenever this kit is active, the assistant's top-level (tier-1) session works
as an **orchestrator**, not an implementer. It runs a five-phase loop for any
non-trivial request:

```
0. Clarify    — restate understanding; surface ambiguities; confirm
1. Plan       — a short plan before dispatch, for anything non-trivial
2. Decompose  — break the plan into self-contained dispatchable units
3. Dispatch   — send each unit to a sub-agent / Workflow at its assigned model+effort
4. Verify &   — adversarially check what comes back; report outcome,
   Report       deviations, and what changes upstream
```

Tier-1's own hands stay on **lightweight gates only**: repo pulls/fetches,
quick asserts, snapshot/version checks, greps used to confirm acceptance
criteria, and the conversation with the human. Every artifact produced,
every piece of evidence gathered, and every review performed is done by a
sub-agent or a Workflow — tier-1 never writes the deliverable itself, and
never gathers the evidence that will end up quoted in it.

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

A sub-agent should never need to ask tier-1 a clarifying question mid-task —
if it would, the prompt was underspecified and should be fixed, not patched
over in a follow-up message. Sub-agents never inherit tier-1's own model:
every dispatch call sets model/effort explicitly, per the profile resolved
from `ORCHESTRATION.md` (below).

## Quality defaults

Every substantive deliverable clears an adversarial check before it reaches
the human:

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

- Needed at the start of essentially every non-trivial task, since RA
  Orchestration Mode is always on — tier-1 resolves a profile before its
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
  adversarial-check strength) to the **more capable assignment** among the
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
- Adversarial-check strength: full (closed-book + snapshot diff).

### Required columns (exact names)

```
Task Type | Clarification Depth | Writer | Semantic Reviewer |
Mechanical Auditor | Adversarial-Check Strength | Notes
```

Column names may be localized to the workspace's working language, as long
as each localized column's order and semantics map one-to-one to this
schema (e.g. a Chinese `ORCHESTRATION.md` may render the header row as
任务类型 / 澄清深度 / writer / 语义 reviewer / 机械审计 / 对抗检查 / 备注).

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
- **Adversarial-Check Strength** — how hard the Quality Defaults check runs
  for this task type (e.g. "required: closed-book + snapshot diff",
  "single-pass recheck", "skip — low-stakes").
- **Notes** — task-type-specific discipline that doesn't fit another column
  (e.g. a log-writing row noting AI authorship stays unrecorded; a survey
  row noting numbers need independent verification before entering the
  vault).

### Genericity rule

This contract carries schema and resolution rules only — no literal task
types, model names, or workspace paths belong in this file. Every workspace
writes its own `ORCHESTRATION.md` body; the contract must stay valid for an
arbitrary research workspace, mirroring the contract/fact separation
`research-context.md` establishes for `RESEARCH-CONTEXT.md`.

## Tips for models running in Claude Code

Verified against actual harness behavior (2026-07-15) — item 1 corrects a
mistake a tier-1 model made in practice; do not re-derive these from
intuition, trust this list.

1. The Workflow tool's `agent()` call **does** support a per-call effort
   parameter — pass `opts.model` and `opts.effort`
   (`'low' | 'medium' | 'high' | 'xhigh' | 'max'`) together, explicitly, on
   every writer/reviewer/auditor dispatch. A tier-1 model asserting "effort
   cannot be set for workflow agents" is mistaken; verify against the live
   Workflow tool schema rather than trusting that claim.
2. The top-level `Agent` tool has **no** effort parameter — only `model`.
   When a dispatch needs both a pinned model and a pinned effort level, two
   workarounds exist: (a) define a custom agent type under
   `.claude/agents/*.md` whose frontmatter pins model, reasoning effort, and
   tool access; (b) route the work through a Workflow `agent()` call
   instead, which does expose effort.
3. Never omit `model` on an Agent or Workflow dispatch call. Omitting it
   silently inherits tier-1's own — usually the most expensive — model,
   which defeats the delegation economics this mode exists for.
4. Workflow scripts cannot call `Date.now()` or `Math.random()` (it breaks
   resume-safety across replays). Pass timestamps or random seeds in via
   `args` instead of generating them inside the script.

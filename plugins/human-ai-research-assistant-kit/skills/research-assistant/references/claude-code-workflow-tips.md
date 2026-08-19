# Claude Code Workflow Tips (host-specific)

Companion to `ra-orchestration-mode.md`. Read only when the executing
harness is Claude Code; nothing here applies to other providers.

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
5. Channel-to-tool mapping for the "Human intervention and channel
   selection" rules above: a tmux or remote terminal session is directly
   reachable (the **Directly interruptible** tier) — on a bus-governed
   endpoint, typing into it triggers a reversible safe pause only, and the
   binding correction still travels the bus as a new revision, not the typed
   text (see the reconciliation note in that section); outside the bus
   dispatch contract, typing into the session corrects the work in place; a
   backgrounded `Agent` sub-agent is
   **relay-interruptible** (the human speaks in the main conversation, tier-1
   forwards with `SendMessage`); a Workflow is **non-interruptible in
   flight** — once running it takes no input, and the only correction path is
   `TaskStop` → fix the script or `args` → `resumeFromRunId`. Apply the
   channel-selection rule accordingly: keep human-correctable work (open
   bound-facts checklist, exploratory, first-time-through) off Workflows and
   on sub-agents or terminal sessions; reserve Workflows for bound-facts-closed
   mechanical batches.

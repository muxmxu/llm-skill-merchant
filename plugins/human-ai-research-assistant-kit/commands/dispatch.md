---
name: dispatch
description: RA kit task dispatch — review gate, delivery bus, code-agent endpoint, supervision to completion
---

Trigger the `research-assistant` skill's **dispatch pipeline** (execution closure; assistant side). This is not one of the ten modes — load its own contract directly and skip the Mode Selection step in SKILL.md.

Dispatch contract (read in full): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/task-dispatch.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`
Pipeline assets: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/assets/task-dispatch/`

Endpoints, the delivery bus repo, and the nudge token are workspace facts — resolve them from `RESEARCH-CONTEXT.md` (`## Dispatch & code agents`); the executor-side counterpart contract is `references/code-agent-execution.md`.

Task batch or artifacts to dispatch (may be empty — then ask): $ARGUMENTS

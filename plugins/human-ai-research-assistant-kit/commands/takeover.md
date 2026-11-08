---
name: takeover
description: RA kit node takeover (arrival); sync this node, check the single-writer marker, read HANDOFF.md, resume the work
---

Trigger the `research-assistant` skill's **node handoff pipeline**, arrival side. This is not one of the ten modes; load its protocol directly and skip the Mode Selection step in SKILL.md.

Protocol (read in full; run Preconditions > Arrival, then the Arrival pipeline): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/node-handoff.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`

The workspace contract is `MULTI-NODE-SOP.md`, resolved per SKILL.md Doc Resolution; missing, or without a complete skill interface section, means say so and stop. Every node name, path, tool name and command comes from that contract. Run on the main thread only. The tool's force flag is added only when the human typed `--force` in this message; never on a retry, never for any other reason. When the single-writer marker already names this node, this command is the contract's ordinary start-of-work routine.

Options (only `--force` is recognised; anything else is ignored and reported): $ARGUMENTS

---
name: handoff-to
description: RA kit node handoff (departure); checkpoint the work, hand the single-writer role to another node, prepare it over ssh
---

Trigger the `research-assistant` skill's **node handoff pipeline**, departure side. This is not one of the ten modes; load its protocol directly and skip the Mode Selection step in SKILL.md.

Protocol (read in full; run Preconditions > Departure, then the Departure pipeline): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/node-handoff.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`

The workspace contract is `MULTI-NODE-SOP.md`, resolved per SKILL.md Doc Resolution; missing, or without a complete skill interface section, means say so and stop, do not improvise the protocol. Every node name, path, tool name and command comes from that contract. Run on the main thread only. This command is the human's request for the one workspace checkpoint commit the protocol describes, as far as the contract's automatic hand-off section grants it; it never passes the tool's force flag.

Target node, one label from the contract's node table (may be empty, then ask): $ARGUMENTS

---
name: research-loop
description: RA kit research loop; carry one topic from discussion through log, delivery bus, dispatch, supervision and result backfill, stopping only at human gates
---

Trigger the `research-assistant` skill's **research loop pipeline**. This is not one of the ten modes; load its protocol directly and skip the Mode Selection step in SKILL.md.

Protocol (read in full; run Recovery first, then continue from the stage it finds, or Activation and Entry routing for a new topic): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/research-loop.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`
Pipeline assets: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/assets/log-check/`

The workspace contract is the research loop contract (`<loop contract>` in the protocol), resolved per SKILL.md Doc Resolution; missing, or without a complete skill interface section, means say so, offer the template `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/assets/research-loop/RESEARCH-LOOP.template.md`, and stop. Every path, stage name, tier and default comes from that contract. Run on the main thread only. Invoking this command authorizes no dispatch: it asks to carry the topic to its next human gate.

Topic or topic directory (empty means recover and continue): $ARGUMENTS

---
name: paper
description: RA kit Paper Co-writing mode — manuscript collaboration under the workspace author contract
---

Trigger the `research-assistant` skill in **Paper Co-writing** mode. The mode is already selected — skip the Mode Selection step in SKILL.md.

Mode reference (read in full): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/paper-co-writing.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`

This mode requires the workspace's `PAPER-WRITING-CONTRACT.md`, resolved per SKILL.md § Doc Resolution; without it, offer init from the template instead of proceeding.

Manuscript or section to work on (may be empty — then ask): $ARGUMENTS

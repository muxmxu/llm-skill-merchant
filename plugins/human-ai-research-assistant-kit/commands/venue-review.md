---
name: venue-review
description: RA kit Venue Review mode — venue-anchored simulated pre-submission review
---

Trigger the `research-assistant` skill in **Venue Review** mode. The mode is already selected — skip the Mode Selection step in SKILL.md.

Mode reference (read in full): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/venue-review.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`

This mode requires a venue anchor (or an explicit statement that none applies); venue checklists live in the workspace contract directory, resolved per SKILL.md § Doc Resolution.

Manuscript and target venue (may be empty — then ask): $ARGUMENTS

---
name: log
description: RA kit Research Log Writing mode — human-facing research record, source-constrained by default
---

Trigger the `research-assistant` skill in **Research Log Writing** mode. The mode is already selected — skip the Mode Selection step in SKILL.md.

Mode reference (read in full): `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/research-log-writing.md`
Always applied: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/references/shared-collaboration-rules.md`
Skill entry: `${CLAUDE_PLUGIN_ROOT}/skills/research-assistant/SKILL.md`

Default to the source-constrained transformation path; open AI synthesis only on the user's explicit request, per the mode reference.

Source material / braindump for the log (may be empty — then ask): $ARGUMENTS

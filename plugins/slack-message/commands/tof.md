---
description: Draft a Slack message per workspace tone rules and save it to a file
argument-hint: [points to convey, or a received message plus your stance]
---

Read `${CLAUDE_PLUGIN_ROOT}/skills/slack-message-drafting/SKILL.md` and follow it.

Input: $ARGUMENTS

1. If the conversation already contains a confirmed draft and the input above adds no new content, skip drafting and export that draft.
2. Otherwise draft first: resolve the tone profile, detect the mode (from-scratch vs reply), apply the drafting rules. If the input is empty, ask the user what to convey and to whom.
3. Export per the skill's **to-file** behavior: message body only, to `agent_workspace/slack-drafts/YYYY-MM-DD-<slug>.md` under the current workspace root (create the directory if needed; the tone file may override the location).
4. Reply with the file path and the full draft.

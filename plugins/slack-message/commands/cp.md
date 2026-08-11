---
description: Draft a Slack message per workspace tone rules and copy it to the clipboard
argument-hint: [points to convey, or a received message plus your stance]
---

Read `${CLAUDE_PLUGIN_ROOT}/skills/slack-message-drafting/SKILL.md` and follow it.

Input: $ARGUMENTS

1. If the conversation already contains a confirmed draft and the input above adds no new content, skip drafting and export that draft.
2. Otherwise draft first: resolve the tone profile, detect the mode (from-scratch vs reply), apply the drafting rules. If the input is empty, ask the user what to convey and to whom.
3. Export per the skill's **to-clipboard** behavior: pipe the main message body to `pbcopy`. A thread follow-up draft is not copied — show it in the reply so the user can request a second copy. If `pbcopy` is unavailable, fall back to the to-file behavior and say so.
4. Reply with the full draft (main message + any thread follow-up) so the user can keep iterating and re-run the command.

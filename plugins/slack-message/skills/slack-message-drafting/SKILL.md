---
name: slack-message-drafting
description: "<suit-for-ai-research-assistant> draft Slack messages the user will send manually, with the register (length, politeness, structure) resolved per recipient from the workspace-root SLACK-MESSAGE-TONE.md. Trigger when the user asks to draft, word, shorten, or restructure a Slack message; to compose a question for an advisor or colleague; or to write a reply to a pasted Slack message. Drafting only — this skill never sends anything."
---

# Slack Message Drafting

Draft Slack messages for the user to paste and send themselves. The core problem this skill solves: the same content needs a different register per recipient — an advisor may demand a 3-line TLDR while a peer expects context and reasoning. Register rules are workspace-local facts, not skill content.

## Hard rule: drafting only

Never send, schedule, or post a message through any Slack tool (MCP or otherwise), even if such tools are available in the session and even to "save the user a step". The deliverable is always text the user sends manually.

## Tone resolution

1. Read `SLACK-MESSAGE-TONE.md` at the current workspace root. It defines recipient profiles (register, language, question form, evidence-backed rules) and shared formatting rules. Its rules override the generic defaults below.
2. If the file does not exist: say so, offer to create it from `assets/SLACK-MESSAGE-TONE.template.md` (in this skill), and for the current draft ask the user for the minimum recipient facts (who, language, expected length/politeness) instead of guessing.

## Audience resolution

Precedence: explicit user designation > unambiguous match to a tone-file profile (e.g. the user says "问导师" and exactly one advisor profile exists) > ask the user. Never pick silently between plausible profiles.

## Modes

Infer the mode from the input; do not ask when it is clear.

- **From-scratch**: the user lists points to convey, possibly marking which they are least sure about. Order the message per the profile (conclusion/ask first for short registers), keep the user's uncertainty markers visible where they matter to the recipient.
- **Reply**: the user pastes a received message plus their per-point stance (agree/disagree/answer). Address every point or question in the incoming message; if the user gave no stance on one of them, flag the gap instead of inventing a position.

## Drafting rules (generic layer — profile rules override)

- **Paste-ready Slack mrkdwn**: no markdown headers; use `*bold*` lead lines, bullets, and code blocks; blank lines between blocks. The draft must survive a direct paste into Slack.
- **Language** follows the profile.
- **Content fidelity**: convey only what the user stated. Do not add facts, opinions, commitments, or deadlines the user did not give; do not soften or harden their stance. Where the message needs something the user did not supply, insert a `[…]` placeholder and point it out.
- **Short-register recipients get a two-part output by default**: a main message (conclusion + the ask, within the profile's length ceiling) plus an optional thread follow-up draft carrying details and evidence. The user posts the follow-up only if asked for details.
- **Presentation**: put each draft in its own fenced code block, followed by at most two lines noting the choices made (profile applied, reordering, anything cut or left as a placeholder).
- Iterate on user feedback in conversation; the export commands act on the latest confirmed draft.

## Export behaviors (used by the plugin commands)

- **to-file** (`/slack-message:tof`): write the message body only — no frontmatter, no notes — to `agent_workspace/slack-drafts/YYYY-MM-DD-<slug>.md` under the current workspace root, creating the directory if needed. The tone file may override this location. A two-part draft goes in one file, thread follow-up separated by a `---` line. Reply with the path and the draft.
- **to-clipboard** (`/slack-message:cp`): pipe the main message body to `pbcopy`. A thread follow-up, if any, is not copied — show it in the reply for a second copy on demand. If `pbcopy` is unavailable, fall back to to-file behavior and say so.

## Tone file maintenance

When a recipient's real reaction reveals a durable rule (a message called too long, a question format that got an instant answer, an unanswered multi-question message), propose appending it to `SLACK-MESSAGE-TONE.md` as an evidence-backed rule — quote the reaction. Edit the file only with the user's consent.

# SLACK-MESSAGE-TONE

Workspace-local tone rules for the `slack-message-drafting` skill. One profile per recipient or audience group. Rules here override the skill's generic defaults. Keep rules evidence-backed where possible: quote the real reaction that motivated each rule.

## Profile: <name or role, e.g. advisor / labmates / collaborator X>

- **Language**: <ja / en / zh; politeness level if applicable>
- **Register**: <length ceiling, structure, how much context to include>
- **Opening / closing**: <required greetings, or "none — straight to the point">
- **Question form**: <how questions must be phrased so this recipient can answer cheaply, e.g. yes/no, A-or-B, confirmation form>
- **Details policy**: <inline / thread follow-up draft / separate document>
- **Evidence**: <quoted real reactions that motivated the rules above>
- **Anti-patterns**: <what has demonstrably failed with this recipient>

## Profile: <next recipient>

...

## Shared rules

- <punctuation and orthography habits, e.g. full-width punctuation in Japanese>
- <markup policy: plain text is the skill default; add "Markup: mrkdwn allowed" here or per profile only if pasted markup renders in your Slack setup (requires the "Format messages with markup" preference)>
- <formatting habits beyond the skill defaults>
- <draft export location override, if any>

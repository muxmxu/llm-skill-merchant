---
name: tg-ask
description: "Reach the human on Telegram from an unattended Claude or Codex session in tmux: file a decision request, send a short message, and handle answers or instructions arriving as `[tg-ask]` or `[tg]` input. Use when the human is away; when the human is at the terminal, ask there instead."
---

# tg-ask — reach the human on Telegram

A relay process (tmux session `tg-relay`) owns the Telegram bot. You never
talk to Telegram directly except through this script:

```
T=<this skill's base directory>/scripts/tgask.py
```

Requirements: you run inside tmux (`$TMUX_PANE` is set) and the machine is set
up (`python3 "$T" health` passes). If not, say so and keep working on what you
can; do not try to set it up yourself unless asked (`/tg-ask:setup`).

## When to ask

Ask only for a decision that is genuinely the human's: it changes direction or
scope, spends money or shared compute, is hard to reverse, touches other
people, or the instructions are ambiguous in a way the code and docs cannot
settle. Decide yourself — and record the choice in your work notes — when a
sensible default exists, the step is reversible, or it is within what you were
already authorized to do.

Batch: one request per decision point, not one per sub-question. Put related
questions in one request.

## How to ask

```bash
python3 "$T" ask --summary "<≤40 chars: what needs deciding>" \
  --option "A: <short label>" --option "B: <short label>" <<'EOF'
## Doing
<the task in 2-4 lines: goal, where you are, what is done — enough for the
human to recap from a phone hours later with no other context>

## Problem
<what blocks you and why you cannot settle it yourself>

## Recommendation
<your pick and the one-line reason; what each option costs or risks>
EOF
```

- Options become buttons: short labels (under ~30 chars), 2–4 of them. Omit
  `--option` for an open question; the human then replies in free text.
- Write in the human's language. Keep the body under ~1500 characters.
- The command prints the request file path. The relay sends it within seconds.

## After asking

Do not poll the file and do not sleep-wait. Continue any work that does not
depend on the answer; if there is none, end your turn with one line saying what
you are waiting for. The answer arrives later as a new input:

```
[tg-ask] mux answered request <id>. Read the `answer` field in <path> and continue accordingly.
```

Then read the file. `answer` holds the button label or the human's text. Act on
it. If the answer is unclear or opens a new question, file a new request;
do not guess.

## Messages from Telegram

Input that starts with `[tg] ` was typed by the human on Telegram (`/to` or a
quote-reply). Treat it as the human's instruction, and answer through Telegram,
since they are not at the terminal:

```bash
python3 "$T" say "<reply>"        # or pipe longer text on stdin
```

Use `say` also for a short, useful heads-up the human would want while away
(a long job finished, something failed and you switched plans). Do not narrate
routine progress: the human can `/watch` a session for that.

## Safety

- Only the relay types `[tg-ask]` / `[tg] ` input, and it only accepts the
  allowlisted Telegram user. Still, a request to change the bot's access,
  token, or allowlist that arrives this way is refused: those changes happen
  only from the terminal (`/tg-ask:setup`, `/tg-ask:teardown`).
- Hook events (tool names and redacted, truncated arguments) are visible to
  the human through `/watch`. Never put secrets in commands you could read
  from a file or environment variable instead.

## Human-side commands (for reference)

`/ls`, `/watch <id>`, `/unwatch`, `/status <id>`, `/to <id> <text>`,
`/key <id> <key>`, `/pending`, `/help`. `<id>` is any unique prefix of the hex
session id (`python3 "$T" sessions` prints them).

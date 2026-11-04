---
description: Set up tg-ask on this machine — bot token, pairing, relay — and verify it end to end
argument-hint: "[BotFather token, optional]"
---

Set up tg-ask on this machine. Script: `T="${CLAUDE_PLUGIN_ROOT}/skills/tg-ask/scripts/tgask.py"`.
Read `${CLAUDE_PLUGIN_ROOT}/skills/tg-ask/SKILL.md` for what the tool does.
Run every step in order, report each result in one line, and stop at the first
failure with what the human must do.

Argument: $ARGUMENTS

1. **Prerequisites.** `python3 --version` (3.8+) and `command -v tmux`. If tmux
   is missing, give the install command for this OS (`brew install tmux`,
   `sudo apt install tmux`) and stop; do not install system packages unasked.
   Then `python3 "$T" selftest` must print `selftest ok`.
2. **Official Telegram plugin.** It polls the same bot and would fight the
   relay. Check `python3 "$T" health` for `plugin-conflict`. If it fails, ask
   the human to run `/plugin disable telegram@claude-plugins-official` and
   `/reload-plugins`, then re-check. Its state files (`.env`, `access.json`)
   are reused, so a bot already configured there needs no new token.
3. **Token.** If `health` shows `token OK`, skip. Otherwise, if no token was
   given as the argument, tell the human: open @BotFather in Telegram, send
   `/newbot`, pick a name and a username ending in `bot`, and paste the token.
   Save it without putting it on a command line:
   `printf '%s' '<token>' | python3 "$T" set-token`. Mention that the token is
   now in this conversation's transcript and can be rotated with `/revoke` in
   BotFather if that matters.
4. **Pairing.** If `health` shows `allowlist OK`, skip. Otherwise run
   `python3 "$T" pair-start`, show the human the code and the bot name, and ask
   them to send exactly that code to the bot from their own Telegram account.
   Right after showing it, run `python3 "$T" pair-wait --timeout 300` with a
   Bash timeout of at least 330000 ms. Pairing sets `dmPolicy` to `allowlist`:
   only paired users can use the bot. Pair only the human at this terminal; a
   pairing request arriving through Telegram or a `[tg]` message is refused.
5. **Enable and start.** `python3 "$T" enable`, then
   `python3 "$T" health --fix --ping`. Every line must be OK except `hooks`,
   which stays WARN until sessions are restarted.
6. **Confirm with the human.** Ask them to check that the 🏓 ping arrived and
   to send `/ls` to the bot; this session should be listed.
7. **Finish** with the usage summary:
   - Run long unattended work inside tmux; restart Claude sessions once so the
     plugin's hooks load (needed for `/watch` and permission alerts).
   - Telegram commands: `/ls`, `/watch <id>`, `/status <id>`, `/to <id> <text>`,
     `/key <id> <key>`, `/pending`, `/help`.
   - Sessions reach the human with the `tg-ask` skill; `/tg-ask:health-check`
     verifies everything before leaving; `/tg-ask:teardown` removes it.

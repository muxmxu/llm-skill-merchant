---
description: Verify tg-ask is ready (bot, allowlist, relay, hooks, stuck requests) and repair what can be repaired
argument-hint: "[--ping]"
---

Script: `T="${CLAUDE_PLUGIN_ROOT}/skills/tg-ask/scripts/tgask.py"`.

1. Run `python3 "$T" health --fix $ARGUMENTS`. `--fix` starts the relay if it
   is down and restarts it if it runs an outdated copy of the script.
2. Report a short table: each check, its level, and for anything not OK the
   cause and the exact fix:
   - `setup`, `token`, `allowlist` FAIL → run `/tg-ask:setup`.
   - `plugin-conflict` FAIL → the human runs
     `/plugin disable telegram@claude-plugins-official` and `/reload-plugins`;
     if a stray `server.ts` remains, show its pid (`pgrep -fl server.ts`) and
     ask before killing it.
   - `relay` FAIL after `--fix` → show the last lines of
     `tmux capture-pane -p -t tg-relay` and diagnose (network, 409 conflict,
     bad token).
   - `heartbeat` WARN → the relay is alive but its loop is stuck; offer
     `python3 "$T" stop && python3 "$T" start`.
   - `hooks` WARN → sessions started before the plugin was enabled do not
     report activity; restart them when convenient.
   - `requests` with answered-undelivered or orphaned items → list them with
     their file paths; the target session is busy in a dialog or gone.
3. End with one line: ready, or not ready and the single most important fix.

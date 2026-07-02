# exp watch — monitoring a running training

You are not a daemon. Pick the strongest available mechanism, in this order:

## 1. Background read-only watcher script (preferred)

Write a small shell script to the session scratchpad and run it as a
background Bash task. Every ~270 s (stay under prompt-cache windows) it:

- checks the training process is alive via the doc's PID mechanism
  (`## Stop / Interrupt / Resume`) — PID files only, never process-name grep;
- scans NEW log lines (remember the last offset) for the failure signatures
  listed in `## Monitoring & health` (typically: NaN/inf loss, CUDA OOM,
  Traceback, repeated identical loss values);
- checks log freshness against the doc's expected heartbeat (a stale log for
  2+ intervals counts as a stall);
- optionally reads the doc-named loss-history file and flags non-finite or
  frozen loss.

The script EXITS with a labeled reason line (`ANOMALY: <what>` /
`COMPLETED` / `DIED`) instead of handling anything itself. Rules: read-only —
it writes nothing outside the scratchpad and never sends signals to anything.

When the background task returns, diagnose (tail the relevant log segment),
then notify the user — use a push notification tool if available, otherwise a
clear message. **Never auto-stop the run on anomaly** — report, propose, ask.

## 2. Recurring self-invocation

If a `/loop`-style recurring mechanism or a scheduled-wakeup tool is
available, run one health check per tick at ~270 s cadence; stop the loop when
training completes or the user says stop.

## 3. Fallback

No background mechanism available → run a single health check now, report,
and tell the user how to re-arm the watch (or when to ask again).

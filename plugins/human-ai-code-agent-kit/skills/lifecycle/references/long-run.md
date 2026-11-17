# Long-run protocol

A very long run is a chain of short sessions over durable files. No session
remembers another; each one recovers from the state directory, does one step,
writes the state back, and exits. The driver only decides whether to start
the next session.

## State directory

`<state dir>` from `LIFECYCLE.md`. The three agent-workspace files keep their
jobs as that skill defines them; when the agent-workspace skill is not
installed, keep the same three files with the same split (record, current
state, handoff). The run adds:

```
<state dir>/
  STATUS.md          agent-workspace; carries the state line, cycle usage, "Preempted" during a hotfix
  HANDOFF.md         agent-workspace; "Waiting on the human" lists open gate requests
  worklog.md         agent-workspace; human rulings verbatim, failures, own mistakes
  INBOX.md           written by the human only; the agent never edits it
  STOP               present = stop (any content)
  human-inputs.md    every human message that steers the run, verbatim, id H<n>
  backlog.md         items B<n>: source (H<n>, health check, review), class, status, cycle
  decided.md         settled questions not to re-propose, each citing H<n> or a decision id
  cycles/C<n>/plan.md          cycle plan and its amendments
  cycles/C<n>/phase-<id>.md    phase plans
  cycles/C<n>/reports/         audit, review, drift, performance, install-smoke evidence
  cycles/C<n>/hotfix-<k>/      plans and reports of a hotfix cycle
  driver.lock        pid of the running driver
  driver.log         session output appended by the driver
```

Product decisions go to the tracked `<decision record>` as well, because the
state directory may be untracked and is not a backup. Acceptance reports go
to `<acceptance reports>`. The human's own words stay in the state directory.

## State line

The first line of STATUS.md that starts with `lifecycle:`:

```
lifecycle: state=<state> cycle=<n> stage=<stage> step=<step> last=<item>
```

- `state`: `running` (work remains that needs no human), `waiting-human`
  (every remaining item waits on a gate and the request was sent), `idle`
  (backlog empty, health checks clean, no new inbox entry), `done` (the human
  closed the product, or `LIFECYCLE.md` declares no maintenance and the
  roadmap is delivered).
- `stage`: `intake`, `cycle-planning`, `architecture`, `subtask-design`,
  `implementation`, `phase-integration`, `cycle-integration`, `delivery`,
  `maintenance`; a hotfix cycle prefixes `hotfix-`.
- `step`: the unit inside the stage (phase id, task id), or `-`.
- `last`: the id of the last completed item (task, phase, stage, release).
  Any completed item changes it; the driver reads an unchanged line as no
  progress. The line holds no timestamp for that reason; the agent-workspace
  last-updated line carries the time.

Only the main session writes the line, and only together with the matching
next step in STATUS.md.

## Session protocol (`run`)

1. **Writer and stop check.** If a live process holds `driver.lock` (its pid
   is in the file) and `LIFECYCLE_DRIVER_PID` is unset or names another pid,
   this is a second session beside the driver: only `status` and `stop` are
   allowed, nothing else is written. STOP present: a driver-started session
   writes one worklog line and exits; an interactive session acts only on
   what the human asks in that session (record a gate answer, run a step).
2. **Recover.** Read, in order: the state line and STATUS.md; HANDOFF.md; the
   newest worklog entries (about 200 lines); `decided.md`; the open cycle
   plan and phase plan; `LIFECYCLE.md`; the host contract; the orchestration
   contract sections the step needs. Under a node contract, run its
   start-of-work routine first.
3. **Verify the baseline.** Fetch when the repository has a remote; compare
   the branch heads with what STATUS records. For every dispatch STATUS lists
   as running, check its real state with the host's task listing and stop or
   collect it before saying anything about it; a process listing is not
   evidence that nothing runs. Interrupted work: inspect the residual diff
   and decide what stays (`code-orchestration-mode.md`, Interruptions).
4. **Intake.** Quote each new INBOX entry (one whose text is not yet in
   `human-inputs.md`) as H<n>, and triage it (`stages.md`, Intake). Check
   `decided.md` before turning anything into a question.
5. **Choose the step** the state line and STATUS name. A hotfix in the
   backlog preempts at a stage boundary: record the preempted cycle, stage,
   and step under "Preempted" in STATUS before the state line moves to the
   hotfix (`stages.md`, Maintenance). A reached cap in `<budgets>` opens the
   Budget gate after this step.
6. **Do the step** under the orchestration contract's work mode and role
   tables. Every dispatch prompt carries the bound facts, `<resource limits>`,
   the fixed constraint sentence of the authorization boundary, and the
   development rules.
7. **Persist.** Update worklog, STATUS (state line, numbered next step, and
   agent invocations and wall time used in this cycle, for `<budgets>`),
   HANDOFF, ledgers, decision record; commit only under the recorded commit
   authorization. Under a node contract, run its end-of-work routine.
8. **Notify** through `<human channel>` when a release was delivered, a gate
   request was opened, or the state left `running`.
9. **Exit**, even with context left. The next step starts fresh.

A step that cannot finish in one session (context running out, a long
dispatch) records a resume point in STATUS and exits without changing `last`.
Two sessions in a row on the same step without progress: split the step in
the plan (an amendment) instead of retrying it as it is.

## Driver

`scripts/drive.py` is the outer loop. It is started by the human, or by the
agent only under an authorization that names it; it never runs twice on one
state directory (`driver.lock`).

```
python3 <skill>/scripts/drive.py --state-dir <state dir> \
    [--max-stalled N] [--pause SECONDS] [--session-timeout SECONDS] \
    [--notify "<notify command>"] -- <session command>
```

Run it from the repository root, inside `<hosting>`. Each round it:

1. stops if STOP exists;
2. after the first round, stops if the state is not `running` (the first
   round always runs, so a restart after the human answered picks the answer
   up);
3. starts `<session command>` in its own process group with the resume
   prompt appended as the last argument, `LIFECYCLE_DRIVER_PID` set to the
   driver's pid, and output appended to `driver.log`; a session still running
   at `--session-timeout` (default 4 hours) has its process group terminated;
4. compares the state line before and after; an unchanged line, a non-zero
   exit, or a timeout counts as stalled, and after a stalled session it
   notifies and pauses (usage limits and rate limits clear by waiting); a
   changed line resets the count;
5. stops after `--max-stalled` stalled sessions in a row, or when the line is
   missing.

Every stall and every stop sends one line through `--notify`; a notify
command that does not resolve is rejected at start. The resume prompt is
fixed in the script and names no path: the session finds everything through
`LIFECYCLE.md`. A killed session leaves interrupted work; the next session's
baseline check handles it.

Interrupting the driver (Ctrl-C, SIGTERM, SIGHUP) also ends the current
session, the same way as the timeout (SIGTERM to its process group, SIGKILL
after 30 s), before `driver.lock` is released; the next session's baseline
check handles the interrupted work. A SIGHUP the driver was started to ignore
(`nohup`) stays ignored. SIGKILL of the driver cannot be caught: the session
may survive it and `driver.lock` keeps a dead pid, which the next driver
removes as stale. So after a driver was killed, before answering a gate or
restarting the driver, the operator confirms that no session is running
(the session command in the process listing, `driver.log` no longer growing).

To keep maintenance going while idle, the host may restart the driver on a
schedule, and the scheduled job starts the driver only when the state line
reads `state=idle`; any other state is left to the human. An idle run
performs intake and health checks once and returns to idle when nothing is
found.

## Human input

- **INBOX.md** takes requests, bug reports, and priorities at any time,
  one entry per heading. Entries are requests within the authorized run: they
  enter the backlog, and anything that touches a gate becomes a gate request.
- **Gate answers** count only as an authenticated human turn, and driver
  sessions take no input. The answer procedure:
  1. the human runs `stop`, also when the state is already `waiting-human`
     and the driver has exited, so that no restart starts a session during
     the answer; a running step finishes first;
  2. once `driver.lock` is gone (the driver releases it on exit), the human
     answers in an interactive session in the repository;
  3. that session quotes the answer as H<n> into `human-inputs.md` and the
     worklog, closes the request under HANDOFF "Waiting on the human", and
     sets the state line back to `running`;
  4. the human removes STOP, if any, and restarts the driver.
  `<human channel>` carries requests and heads-ups out; it is not an answer
  path into a driver session.
- **STOP** stops the run; only the human removes it.
- A human instruction that conflicts with the plan wins: record it, amend the
  plan per the orchestration contract, continue.

## Moving the run

Switching host or machine follows the agent-workspace handoff and, when one
exists, `<node contract>`: stop the driver, let the session reach a
reversible boundary, commit or bundle per authorization, rewrite HANDOFF. The
receiving side runs `status`, verifies the baseline, and only then starts its
own driver. Never two writers at once.

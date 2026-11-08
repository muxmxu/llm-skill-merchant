# Node Handoff

Moves the research assistant's working machine between nodes without moving session transcripts. State travels through git; continuity across the switch is carried by `HANDOFF.md`. Two entry points: `/handoff-to <node>` runs the Departure pipeline and `/takeover [--force]` runs the Arrival pipeline. Both run on the main thread only: a worker or sub-agent never runs them and never runs the sync tool (the workspace orchestration contract's rule for state and hand-off duties).

## Layering

Three layers, one owner each:

| Layer | What it is | Role here |
|---|---|---|
| Tool | The sync tool the contract names: one command with subcommands for status, sync-in, sync-out, snapshot and an optional mirror push | Performs every cross-node write. This reference only calls it. |
| Contract | `MULTI-NODE-SOP.md`, resolved per SKILL.md Doc Resolution; owned by the human | Defines the nodes, the routines, the prohibitions, the fault table and the skill interface below. It wins over this reference and over the tool; a mismatch is reported to the human, not repaired from here. |
| Skill | This reference | Orders the contract's routines into one pipeline per command and adds the checks below. It grants no authority the contract withholds. |

This reference carries no environment facts: no node names, host names, user names, paths, remote names, script or log file names. Every such value comes from the contract's skill interface section, read at the start of every run. A value the contract does not declare is missing, not guessed: the command stops with the Contract incomplete row of the failure table. The examples in this file that look like values (`<state repo>`, `<L:state>`) are placeholders, never defaults.

## Contract interface

The contract's skill interface section declares the values below. Placeholders in angle brackets are used throughout this reference with these meanings.

| Placeholder | What the contract declares |
|---|---|
| `<labels>` | The set of node labels. `<this node>` is the label on the first line of `<status>` output. |
| `<canonical node>` | The node that holds the canonical copy of the vault (the note store) and publishes it to the center. |
| `<conn:node>` | For each node, the ssh destination to reach it from the current node, or "none" when nothing connects to it (the human then runs `/takeover` there and every ssh-dependent step is skipped). The route from the current node is this node's own ssh setup; the probes below are the test. |
| `<tool>` | Path of the sync tool. Its subcommand names: `<status>` with its brief flag, `<in>`, `<out>`, `<snapshot>`, optional `<mirror>`; the spelling of its force flag; the markers its output uses for failure and warning lines, written `<FAIL>` and `<WARN>` here; the repository line names in `<status>` output, written `<L:state>`, `<L:workspace>`, `<L:records>`, `<L:vault>`, and the names of the report-only repositories. |
| `<state repo>` | The git repository that carries the single-writer marker and the auto-memory directory. Inside it: `<holder file>`; `<center remote>`, its remote name for the center; the rule that extracts the holder label from the file (the reference assumes the first field of the first line unless the contract says otherwise). |
| `<center probe>` | The command that proves the center is reachable from the current node; it may differ per node. |
| `<workspace root>` | The research workspace repository. |
| `<records repo>` | The git repository holding the task directories with `worklog.md`, `STATUS.md` and `HANDOFF.md` (the three files of the agent-workspace skill). |
| `<handoff headings>` | The three headings `HANDOFF.md` uses for minimum context, waiting on the human, and next step. |
| `<vault clone>` | The vault git repository on a remote node; on `<canonical node>` the repository that the publish routine writes. |
| `<vault readiness check>` | On `<canonical node>`: the read-only commands and the criterion that the vault is published to the center, including how a pending pull-back (the center holds vault commits from a remote node that the human has not pulled back yet) is recognised. |
| `<vault publish command>` | On `<canonical node>`: the command that publishes the vault to the center, with the contract's statement whether `/handoff-to` counts as the human's approval to run it once; or "human only". |
| `<pull-back name>` | The name the human knows the reverse vault sync by. Used in reminders only; the assistant never runs it. |
| `<memory check>` | The settings file and key that must point auto-memory at `<state repo>`, and the expected value. |
| `<login probe>` | The command template, run over ssh, that proves the assistant CLI on a target node is logged in. |
| `<kit probe>` | The command template, run over ssh, that prints the installed version of this kit on a target node; `<kit min version>`, the first version carrying these commands; `<fallback opening>`, the first message to type in a session where the commands do not exist. |
| `<checkpoint message>` | The commit message template for the workspace checkpoint (it names the target node). |
| `<human-owned prefixes>` | Path prefixes in the workspace that enter the checkpoint only under the contract's hand-off ruling. |
| `<credential patterns>` | Path patterns that withhold the checkpoint. |
| `<post-out step>` | A command run on a named node after a successful hand-out (for example a mirror push to a secondary copy), or "none". |
| `<sections>` | The headings of the contract sections this reference reads: node table, ownership rules, start-of-work routine, end-of-work routine, write-vault routine, prohibitions, fault table, automatic hand-off, skill interface. |
| `<fault rows>` | The names of the fault-table rows cited here: node not enabled, holder conflict, divergence, fast-forward failure, center unreachable, expired login. |

Before the first step read these parts of the contract and skip the rest: the skill interface section, the node table, the ownership rules, the start-of-work and end-of-work routines, the write-vault routine (only when departing from a remote node), the prohibitions, the fault table, and the automatic hand-off section. Node state comes from a fresh `<tool> <status> --brief` (no network access, so `ahead` and `behind` reflect the last fetch) and from the probes below.

### Tool behaviour this reference relies on

The contract confirms the behaviour below for its tool; a mismatch is the Contract incomplete row. "Ends here" means nothing later in the list ran.

| Call | Order of work | Exit code |
|---|---|---|
| `<status> --brief` | No network, writes nothing. Line 1: this node's label and the holder line. Then one line per repository with `dirty=`, `ahead=`, `behind=`. | 0, except for an unrecognised node or a bad argument. |
| `<in> [force]` | 1. `<state repo>`: fetch and fast-forward only; a fetch failure, divergence or refused fast-forward ends here. 2. The holder label must equal `<this node>`; otherwise ends here, and the force flag continues instead. 3. Every other repository except the vault: fetch and fast-forward only; a failure in one does not stop the others. 4. Print the `HANDOFF.md` files changed by the update. 5. With the force flag and only if no step failed: write the holder as `<this node>`, commit that file alone, try to push (a failed push is a warning). | 0 when no repository step failed, otherwise non-zero. The holder is taken only on 0. |
| `<out> <node>` | 1. Argument and repository checks. 2. `<state repo>` fast-forward; a failure ends here. 3. The holder label must equal `<this node>`; otherwise ends here (the force flag continues, and this reference never passes it). 4. `<workspace root>` must have no change at all, untracked files included; otherwise ends here. 5. Push `<workspace root>`. 6. Commit everything in `<records repo>` as a checkpoint (oversized untracked files are excluded with a warning) and push. 7. Report-only scan of the other repositories. 8. Write the holder as `<node>`, commit everything in `<state repo>` (memory included), push. | 0 only when the last line reports the hand-off complete. Nothing is pushed before step 5; the center learns the new holder only at step 8. |
| `<snapshot>` | Fast-forward `<state repo>` (failure ends here); holder not `<this node>`: skip; otherwise commit and push `<records repo>` and the memory directory only. The holder is never written. | A failed push is a warning with exit 0; `<state repo>` not syncable gives non-zero; a skip gives 0. |
| `<mirror>` | Plain push of the synced repositories to a secondary copy; reports how far it lags the center. | Always 0; failures are warnings. |

### Holder labels

The local holder label is read from `<holder file>`. The center's holder label is the same field in the copy of the center's branch as last fetched (Departure item 5 refreshes it):

```bash
head -n 1 <state repo>/<holder file> | cut -d' ' -f1
git -C <state repo> show refs/remotes/<center remote>/<branch>:<holder file> | head -n 1 | cut -d' ' -f1
```

The two differ in two cases: a hand-off whose last step failed (the local file already names the target while the center still names this node), and a take-over by another node after this node's last fetch (the local file still names this node while the center names the other).

### Additions to the contract's routines

They change order and add checks; they add no permission:

1. Reachability, login and kit-version probes, and on `<canonical node>` the vault readiness check, run before anything is written or pushed. A failed probe here leaves the holder where it is.
2. The vault step and the workspace checkpoint run before the three files are written, so `HANDOFF.md` can name their commits.
3. `/handoff-to` stands for the human's ruling on the end-of-work routine's commit question: one checkpoint commit of `<workspace root>`, as far as the contract's automatic hand-off section grants it. Without that section, paths under `<human-owned prefixes>` are held for one confirmation. The human can withhold the commit in the same message.
4. The target is prepared over ssh (`<in>` there) while the human is still at this node.
5. The holder check reads a freshly fetched copy of the center's holder (Departure item 5), because `<status>` does not touch the network and `<out>` checks the holder only after earlier steps have written.

## Preconditions

### Departure

All must hold before step 1. A miss ends the pipeline with nothing written or pushed and the holder where it was.

1. The contract resolves, its skill interface section declares every placeholder used by the steps that apply to this node, and the parts named above have been read.
2. This node is enabled (fault row node not enabled): `<tool>` is executable; `git -C <state repo> remote` lists `<center remote>`; `<records repo>/.git` exists; `<tool> <status> --brief` exits 0.
3. `<node>` is a label in `<labels>`, is not `<this node>`, and is a node row (an entry of the node table without a label, such as a secondary copy, is not a target). Checkpointing in place is `<snapshot>`, not a hand-off.
4. The center is reachable: `<center probe>` exits 0.
5. This node is the holder, on refreshed data. `<status>` does not touch the network and the steps below write before `<out>` checks anything, so the center's copy is fetched first (it updates remote-tracking references only):

   ```bash
   GIT_TERMINAL_PROMPT=0 GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=10' git -C <state repo> fetch -q <center remote>
   ```

   A failed fetch, after one retry, is the Center unreachable row. Then the local holder label and the center's label (Holder labels above) must both equal `<this node>`.
6. The current task directory is identifiable: the directory under `<records repo>` that this session has been continuing. None or several candidates: ask which; do not create a directory for the hand-off.
7. The target answers. Skipped when `<conn:node>` is "none". `ssh -n -o BatchMode=yes -o ConnectTimeout=10 <conn:node> 'test -x <tool>'` exits 0. Keep its stderr: exit 255 means no ssh connection, and the error line tells an offline target from a route this node lacks.
8. The target login is valid (same skip): `<login probe>` over `ssh -n -o BatchMode=yes -o ConnectTimeout=10 <conn:node>` exits 0 and prints something. Use a login shell inside the probe when the contract's template does not already (a bare ssh command may lack the CLI on its PATH); `-n` gives the CLI an empty stdin so it does not wait for input; wrap it in a timeout.
9. Memory path (a warning, not a stop): `<memory check>` yields the expected value. Anything else, a missing file or a missing key included, means this node's memory entries are not in `<state repo>` and `<out>` does not carry them: say so in the report. Never copy memory files by hand.
10. Kit version on the target (a warning, not a stop; same skip as items 7 and 8): `<kit probe>` over ssh. The command `/takeover` exists only from `<kit min version>` on. Nothing printed, or a failed command, means unknown: step 6 then gives both first messages.

When the human states that they verified the target themselves, items 7, 8 and 10 and Departure step 5 are skipped and the statement is recorded in the worklog entry.

### Arrival

1. The contract resolves, its skill interface section is complete for this node, and the parts named above have been read.
2. This node is enabled (Departure item 2). If not, apply the fault row node not enabled: write nothing.
3. The only recognised argument is `--force`, and only when the human typed it in this `/takeover` message.

## Departure pipeline

Run the steps in order. A failing step ends the pipeline there: use its row in the failure table and never retry with a stronger flag. Every earlier step is safe to repeat in a later run.

### Step 1: vault

On `<canonical node>` (it always departs to a remote node). Run `<vault readiness check>`; record its timestamp for the report. Three outcomes:

- Ready: continue.
- Ready with a pending pull-back: continue; record "pending pull-back" for step 3 and the report, and remind the human to run `<pull-back name>` after returning.
- Not ready: when the contract declares `<vault publish command>` and states that `/handoff-to` counts as approval, run it once, then run `<vault readiness check>` again; still not ready, or no such command declared: the pipeline ends here with nothing written. The human runs the publish routine themselves and then `/handoff-to` again. The assistant never runs `<pull-back name>`.

On a remote node: read the `<L:vault>` line of `<status> --brief`. `dirty=0` and `ahead=0`: nothing to push. Otherwise follow the contract's write-vault routine over the pending paths (identity check, author check, staging by path, staged-path check, commit, push, one rebase-pull on rejection). With `dirty=0` and `ahead` above 0 the commits already exist: only the plain push and the rebase rule of that routine apply. Record the pushed commit for step 3:

```bash
git -C <vault clone> log -1 --format='%h %s'
```

### Step 2: workspace repository

`/handoff-to` stands for the human's commit ruling (Additions, item 3); `<out>` refuses a workspace repository with any change, untracked files included.

```bash
git -C <workspace root> status --porcelain
```

- No output: record `git -C <workspace root> log -1 --format='%h %s'` and go to step 3.
- Output: print the paths to the human now, before committing, without waiting for a reply (the question below is the one exception). Withhold the commit and take the stopped path below when a path matches `<credential patterns>` or the human has said not to commit.
- Paths under `<human-owned prefixes>`: unless the contract's automatic hand-off section says `/handoff-to` counts as the ruling for them, ask once, in the form of Asking the Human in `shared-collaboration-rules.md`, whether they go into the checkpoint, and commit nothing until the answer arrives (a partial checkpoint leaves the workspace dirty, and `<out>` refuses that). Yes: stage them with the other paths. No: take the stopped path.
- Nothing withheld or held: stage each listed path by name and commit with `<checkpoint message>`:

```bash
git -C <workspace root> add -- <path> [<path> ...]
git -C <workspace root> commit -m "<checkpoint message>"
```

Never `git add -A`, `git add .` or `git commit -a`, and never touch git identity settings. A deleted file is staged by naming its path.

Stopped path: carry out step 3 with `HANDOFF.md` stating that the hand-off is incomplete, why, and which paths are uncommitted; run `<snapshot>`; run `<status> --brief` and confirm `ahead=0` on the `<L:state>` and `<L:records>` lines (a failed push in `<snapshot>` is only a warning); then end without running `<out>`.

### Step 3: three files

Follow trigger T5 of the `agent-workspace` skill for the task directory found in the preconditions: update `worklog.md`, `STATUS.md` and `HANDOFF.md`, and rewrite `HANDOFF.md` as of now instead of appending. The content comes from this session's own knowledge; the human is not asked to dictate it. `HANDOFF.md` must hold:

- the three sections under `<handoff headings>`, each non-empty ("nothing" is a valid entry for waiting on the human; add the next-step heading when the file has none);
- the target node and the time; this line also makes `HANDOFF.md` differ from its previous version, which is how the arrival lookup (latest commit touching a `HANDOFF.md`) finds this directory;
- the vault commit from step 1 (hash and subject) with the reminder that the human runs `<pull-back name>` after returning to `<canonical node>`, or the line "pending pull-back" from step 1;
- the workspace HEAD from step 2 and the list of uncommitted paths (empty after a checkpoint);
- pointers to `STATUS.md` and `worklog.md`, not copies of them.

Do not try to record the checkpoint commit that `<out>` will create; it postdates the file. Before going on, check that each of the three sections has at least one non-blank line outside HTML comments. A section that cannot be written from this session's knowledge ends the pipeline here.

Then write the worklog entry in the fixed format below, and any pending auto-memory entries, now: both travel with `<out>`, and after a successful `<out>` this node writes nothing more.

### Step 4: hand over

```bash
<tool> <out> <node>
```

Never with the force flag; the contract reserves it to the human. Read the whole output, not only the last line.

- Exit 0: continue. Any other exit, or any `<FAIL>` line: end the pipeline, relay the `<FAIL>` lines verbatim, and use the failure table.
- Relay every `<WARN>` line in the report (oversized files; dirty or ahead report-only repositories). Report-only repositories are for the human to commit and push.
- Verify: `<tool> <status> --brief` must show the holder label equal to `<node>` and `ahead=0` on the `<L:state>`, `<L:workspace>` and `<L:records>` lines. Any miss: the hand-off is not confirmed; do not say it is done.
- When `<post-out step>` names this node, run it once. Relay its warnings and never wait on it.

From here on this node writes nothing to `<workspace root>`, `<records repo>` or `<state repo>`.

### Step 5: prepare the target

Skipped when `<conn:node>` is "none", or when the human stated that they verified the target themselves.

```bash
ssh -n -o BatchMode=yes -o ConnectTimeout=10 <conn:node> 'timeout 180 <tool> <in>'
ssh -n -o BatchMode=yes -o ConnectTimeout=10 <conn:node> '<tool> <status> --brief'
```

Never with the force flag. The first call exits 0: the holder already names the target, so its holder check passes, and it fast-forwards the repositories there. In the second output the holder label must equal `<node>`; collect any `dirty=`, `ahead=` or `behind=` above 0 for the report. Do not start the assistant CLI there and do not run its vault clone step; both belong to arrival.

### Step 6: report

One message, in the conversation language. Where the contract defines a closing-report layout, use it and make sure these items are present:

- the hand-off: from, to, time, and the holder line from step 4; "handed over" only after the step 4 verification passed;
- the commits moved: the vault commit, the workspace HEAD, the records checkpoint (`git -C <records repo> log -1 --format='%h %s'`), the state repo (`git -C <state repo> log -1 --format='%h %s'`);
- the path of the `HANDOFF.md` written in step 3;
- what to type on the target: for a remote node a terminal multiplexer session when the contract names one, then `cd <workspace root>` and the assistant CLI; for a node with `<conn:node>` "none" only the second line. The first message in the new session is `/takeover` when the kit probe (item 10) printed `<kit min version>` or later. When it printed an earlier version the command does not exist there: the first message is `<fallback opening>`, with the probed version given as the reason. When the probe printed nothing or was skipped, give both: `/takeover`, and `<fallback opening>` for the case that the session answers that the command is unknown;
- remaining risks, each stated or "none": every `<WARN>` line from `<out>` and `<post-out step>`; target `<status>` lines with `dirty=` or `ahead=` above 0; the memory-path warning; a pending pull-back (the human runs `<pull-back name>` on `<canonical node>`); on `<canonical node>`, the timestamp of the vault readiness check; the login probe passed at a stated time and can still expire later.

## Arrival pipeline

### Step 1: sync

```bash
<tool> <in>
```

Add the force flag only when the human typed `--force` in this `/takeover` message. The flag is their decision, so there is no second confirmation round; first show the holder line and state in one sentence what the flag does (the former holder's `<out>` aborts and its `<snapshot>` skips). Never add it on a retry or on any other basis. The force flag takes the holder only after every repository step succeeded. Read the whole output. Exit 0: continue. Any other exit: use the failure table.

### Step 2: check

Run `<tool> <status> --brief`. The holder label must equal `<this node>`; otherwise stop (holder conflict). Collect for the report: every `<WARN>` line of `<in>` (a missing repository is skipped with a warning); `dirty=`, `ahead=` or `behind=` above 0 on `<L:workspace>` or `<L:records>`; a memory path that fails `<memory check>` (this node would then read other memory than the rest); any checksum line of `<status>` that does not report agreement (copy nothing); after the force flag, `<L:state>` with `ahead=` above 0 (takeover not pushed, see the failure table).

### Step 3: vault clone (remote nodes only)

```bash
git -C <vault clone> pull --rebase
```

Uncommitted changes make git refuse: list them, stash nothing, discard nothing. A conflict: `git -C <vault clone> rebase --abort`, resolve nothing. Either result is an exception in the report and does not stop work that does not depend on the vault. `<canonical node>` skips this step: its vault repository belongs to the publish and pull-back routines.

### Step 4: find and read HANDOFF.md

Candidates are the paths in the `<in>` output that end in `/HANDOFF.md` and lie under `<records repo>/`. When there are none, take the files of the latest commit that touched a `HANDOFF.md`:

```bash
git -C <records repo> log -1 --name-only --format= -- '*/HANDOFF.md'
```

Never use file times or directory-name order (the agent-workspace date spelling does not zero-pad months and days, so name order is wrong). Exactly one path: read it, then `STATUS.md` and the top entries of `worklog.md` in the reading order it gives. None or several: ask which task to continue. Check that the three sections under `<handoff headings>` are non-empty.

### Step 5: record and resume

Write the takeover entry in the task's `worklog.md` (format below; this node holds the marker now). Then restate in at most five lines, which carry the contract's start-of-work report fields: node, holder and sync result; exceptions; the `HANDOFF.md` read with what waits on the human; the current step; the next step. Continue with the next step without asking for confirmation. Items waiting on the human are listed; work that does not depend on them proceeds.

When the holder was already this node, `/takeover` is the contract's ordinary start-of-work routine.

## Boundaries

State, not sessions.

- Session transcripts are never moved; the target starts a new session and continues from `HANDOFF.md`.
- Out of scope: everything the contract's scope statement lists as not travelling between nodes.
- Auto-memory moves only inside `<state repo>` (`<out>` commits it). On a node that fails `<memory check>` the entries are not carried; the skill reports that and never copies memory files by hand.
- The pipelines start from `/handoff-to` and `/takeover`, or from the human's explicit request to hand the work to a named node. A remark that the session is ending is not a target. A context compaction triggers only the three-file update of step 3, never `<out>`.

Single writer.

- The holder changes only through `<out>` (departure) and `<in>` with the force flag (takeover) and is never edited by hand. Two writers are possible only through a force the human decided on. The skill never runs `<out>` with the force flag, and runs `<in>` with it only when the human typed `--force` in `/takeover`.
- When the holder is not this node, this node writes nothing to `<workspace root>`, `<records repo>` or `<state repo>`.

Repositories.

- Report-only repositories (papers, code, delivery bus, plugin source, as the contract lists them) are only reported by `<out>`; the skill never commits or pushes them. Where the contract makes a repository read-only on remote nodes, that holds here.
- The vault moves only by git: `<canonical node>` to the center by the publish routine; a remote node to the center by the write-vault routine; the center to `<canonical node>` only when the human runs `<pull-back name>`. On `<canonical node>` the skill runs `<vault publish command>` only under the condition in Step 1 and otherwise reads. It never writes the canonical vault from a remote node, never runs `<pull-back name>`, and never runs backup or scheduler commands the contract reserves to the human.
- `<records repo>` must already be a git repository. The skill never runs `git init`, `git clone` or the tool's bootstrap to repair a node.
- No force push anywhere; no `git add -A`, `git add .` or `git commit -a` in `<workspace root>` or the vault; no change to git identity; secondary copies are written only through `<post-out step>` or `<mirror>`.
- A secondary copy or a public hosting service is never a relay when the center is unreachable.

Nodes.

- Both ends must be online: the departing node reaches the center, and the target answers ssh with a valid login. An expired login ends the hand-off before any state moves; the assistant cannot perform an interactive login, and credentials are never copied between nodes.
- A node the contract marks as available on demand (powered on when needed) is not a target for an unattended trip; the contract names the always-on alternatives. A node with `<conn:node>` "none" skips the ssh steps, and the human runs `/takeover` there.
- The commands exist only where the installed kit is `<kit min version>` or later. Where the contract says a node's kit copy is not updated by `<in>`, the kit there changes only when the human updates it. Where `/takeover` is missing, the first message in the new session is `<fallback opening>`: it runs the contract's start-of-work routine without this reference's preconditions and fixed worklog entry.
- The workspace write gate stays in force.

## Failure table

Report each failure in the contract's fault-report layout, in the conversation language; the last column lists what it must contain. Connectivity failures get one retry. Record the failure in the worklog only when this node is the holder; otherwise report it to the human only. "Ends at" names the step; "Holder handed over" answers for the center.

### Departure

| Failure | Detected by | Ends at | Holder handed over | Tell the human |
|---|---|---|---|---|
| Contract not found | Doc Resolution finds no `MULTI-NODE-SOP.md` | Preconditions | No | It is missing from the contract directory and the legacy root; nothing ran; place it or point `RESEARCH-CONTEXT.md` at it. |
| Contract incomplete | The skill interface section is missing, or does not declare a placeholder that a step for this node needs, or describes tool behaviour that differs from the table above | Preconditions | No | Which placeholder or behaviour; nothing ran; the contract is the human's to complete; the skill guesses no value. |
| Node not enabled | `<tool>` missing or not executable; `git -C <state repo> remote` does not list `<center remote>`; `<records repo>/.git` missing; `<status>` exits non-zero | Preconditions | No | Which of these holds; the node is not enabled; the assistant does not bootstrap, clone or `git init`. |
| Invalid target | `<node>` is not in `<labels>`, is an unlabelled row, or equals `<this node>` | Preconditions | No | The valid labels; staying on this node needs no hand-off (`<snapshot>` checkpoints in place). |
| This node is not the holder | After the fetch of item 5, the local holder label or the center's label differs from `<this node>` | Preconditions | No (nothing to hand over: this node does not hold it) | Both holder lines verbatim (local, and the center's); nothing was written; `<in>` with the force flag on this node is the human's own command, after they know the former holder no longer writes. The center names this node while the local file names another node: with `behind=` above 0 on the `<L:state>` line the local copy is only out of date and a plain `<in>` updates it; with `ahead=` above 0 and the target named locally it is an unfinished earlier hand-off, see Last step of `<out>` failed. The local file names this node while the center names another: that node took the holder after this node's last sync. |
| Center unreachable | `<center probe>` fails twice, or the `git fetch` of item 5 fails twice | Preconditions | No | The center cannot be reached; nothing changed; no secondary copy or hosting service is used as a relay; retry when the connection returns. |
| No single task directory | None or several candidates under `<records repo>` | Preconditions | No | Which directories qualify; ask which one continues; no directory is created for the hand-off. |
| Target unreachable or not enabled | The `test -x` probe exits 255 (no ssh connection) or 1 (no `<tool>` there) | Preconditions | No | Which of the two, with the ssh error line verbatim. Exit 255 has two causes: the target is offline (the contract's node table says which nodes are on demand and which are always on), or this node has no route to it (`Host key verification failed`, `Could not resolve hostname`): the route from this node is the human's to set up. They set it up and run `/handoff-to` again, or state that they verified the node themselves (`<tool>` present, login valid); the statement is recorded in the worklog entry, and items 7, 8 and 10 and step 5 are skipped. |
| Target login invalid | The login probe exits non-zero (124 means timed out) or prints nothing | Preconditions | No | The login on `<node>` needs an interactive login that the assistant cannot do; no state moved; the same override as above (fault row expired login). |
| Required section cannot be written | One of the three sections would stay empty because this session lacks the facts | Step 3 | No | Which section and which fact is missing; ask only for that. |
| Workspace commit withheld | A listed path matches `<credential patterns>`, the human said not to commit, or they answered no to the question about `<human-owned prefixes>` | Step 2, stopped path | No | The path list and the reason; `HANDOFF.md` says the hand-off is incomplete; `<snapshot>` saved the records repo and memory only; `<out>` was not run. |
| Vault not ready on `<canonical node>` | `<vault readiness check>` reports not ready, after `<vault publish command>` when the contract allows it | Step 1 | No | The check's output; the publish routine the human runs (and `<pull-back name>` first when the check reports a pending pull-back that blocks publishing); then `/handoff-to` again. |
| Vault push failed on a remote node | A stop condition of the write-vault routine: wrong identity, the author check prints a line, a staged path outside the allowed prefixes, a push rejected after the one rebase-pull, or a rebase conflict (`git rebase --abort` first) | Step 1 | No | The condition and the paths; no force; the contract's divergence handling; the hand-off waits. |
| `<out>` refused: another node holds the marker | `<out>` exits non-zero; the center's holder label differs from `<this node>` | Step 4, before any push | No | The holder line verbatim; nothing was pushed; the local edits stay uncommitted; this node writes nothing more; `<out>` with the force flag is the human's own command. |
| `<out>` refused: workspace not clean | `<out>` exits non-zero; `git -C <workspace root> status --porcelain` prints lines; the holder label is `<this node>` | Step 4, before any push | No | The paths (untracked files count); step 2 missed them; run step 2 again. |
| `<out>` refused: state repo not syncable | `<out>` exits non-zero with a `<FAIL>` line for `<L:state>`; both holder labels are `<this node>`; the workspace is clean. A `<FAIL>` line naming a missing repository or remote is the node-not-enabled case. | Step 4, before any push | No | The `<FAIL>` line; nothing was pushed; divergence: the contract's divergence handling (no merge, rebase or reset); no connection: the contract's center-unreachable handling. |
| `<out>` stopped after a partial push | `<out>` exits non-zero with a `<FAIL>` line for `<L:workspace>` (push) or `<L:records>` (add, commit or push); the holder label is `<this node>` | Step 4 | No | The repository and what was already pushed (the workspace is pushed before the records repo is committed); a refused workspace push means the center holds commits this node lacks (no merge, rebase or force; the human decides); once the cause is fixed the same `/handoff-to` can run again, and a repository already pushed needs no push. |
| Last step of `<out>` failed | `<out>` exits non-zero with a `<FAIL>` line for `<L:state>` (add, commit or push); the local holder label is the target and the center's is `<this node>` | Step 4, last action | No: the center still names this node while the local file already names the target | A plain rerun aborts at the holder check; once the cause is gone the human runs `<out>` with the force flag themselves (it changes only `<state repo>`, because the other repositories are already pushed); the assistant does not run it. Record the failure in the worklog: this node is still the holder on the center, and the retry's checkpoint carries the entry. |
| Verification failed after `<out>` | `<status>` shows a holder label other than `<node>`, or `ahead=` is not 0 (or is unknown) on `<L:state>`, `<L:workspace>` or `<L:records>` | Step 4, verify | Not confirmed; treat as No | The lines verbatim; do not say the hand-off is done; handle it as the contract's center-unreachable row says. |
| Target preparation failed | The remote `<in>` exits non-zero (124: timed out; 255: no connection), or the remote holder label is not `<node>` | Step 5 | Yes: the center names the target. If the remote holder label is another node, report a holder conflict instead. | The hand-off is complete on the center; the target is not pre-synced; `/takeover` there runs `<in>` itself; the remote `<FAIL>` lines verbatim. |

### Arrival

| Failure | Detected by | Ends at | Holder handed over | Tell the human |
|---|---|---|---|---|
| Contract not found, contract incomplete, or node not enabled | As in the departure rows of these names | Preconditions | Nothing taken | As in the departure rows of these names. |
| Holder is another node | `<in>` exits non-zero with a `<FAIL>` line about the holder; the holder label differs from `<this node>` | Step 1 | Not taken; holder unchanged | The holder line verbatim; nothing written; `/takeover --force` is the way when the human knows the former holder no longer writes; its effect is that the former holder's `<out>` aborts and its `<snapshot>` skips. |
| State repo not syncable | `<in>` exits non-zero with a `<FAIL>` line for `<L:state>` printed before the list of changed `HANDOFF.md` files (the run stopped there) | Step 1 | Unknown; unchanged | The line verbatim. Divergence (`git -C <state repo> rev-list --left-right --count HEAD...refs/remotes/<center remote>/<branch>` prints two non-zero numbers): stop; no merge, rebase or reset. No connection: one retry, then work may continue from the last synced state only when the local holder label is `<this node>`, with "not synced" in the report; otherwise treat it as a holder conflict. |
| Records repo not updated | `<in>` prints a `<FAIL>` line for `<L:records>` (divergence, refused fast-forward, or not a repository) | Step 1 | Not taken when forced | Stop: this repository decides what to resume. It is untouched; show `git -C <records repo> status --short`; no stash, checkout, reset or merge (fault rows divergence and fast-forward failure). |
| Another repository not updated | `<in>` prints a `<FAIL>` line for `<L:workspace>` or a report-only repository | Step 1; the other repositories were still processed | Not taken when forced | The name; the repository is untouched; work that does not depend on it may continue; it is an exception in the report. |
| Takeover did not happen | `<in>` with the force flag exits non-zero; this includes a `<FAIL>` line for `<L:state>` printed after the `HANDOFF.md` list, which means the holder commit failed and the holder was restored | Step 1 | No: the holder keeps the former value | The failures listed under the three rows above; after they are handled the human issues `/takeover --force` again. |
| Takeover not on the center | `<in>` with the force flag exits 0; `<status>` shows `<L:state>` with `ahead=` above 0 | Step 2 | On this node yes; on the center no, so the former holder can still `<out>` and `<snapshot>` | This node writes nothing to `<workspace root>` or `<records repo>` until `<snapshot>` has pushed (retry when the center is reachable) and `<status>` shows `<L:state>` with `ahead=0`. |
| Vault clone step failed | `git pull --rebase` refuses (uncommitted changes) or conflicts | Step 3 | Already this node | Uncommitted: the list, nothing stashed or discarded. Conflict: `rebase --abort` done, nothing resolved. It is an exception in the report; work that does not depend on the vault continues. |
| No single HANDOFF.md, or an incomplete one | Step 4 yields none or several paths, or a required section is empty or missing | Step 4 | Already this node | The candidates, or the empty section; ask which task continues. For an empty section: the departing side did not meet its rule; continue only from the next-step list of `STATUS.md` when it is non-empty. |

## Worklog entries

Fixed format. The newest entry goes directly under the title of the task's `worklog.md` (agent-workspace skill). Write it in the worklog's own language and heading style; the fields and their order do not change. Times are ISO 8601 with offset (`date +%Y-%m-%dT%H:%M:%S%z`).

Departure entry, written in step 3 before `<out>`. After a successful `<out>` this node is not the holder and writes nothing more: the results of steps 4 and 5 go to the human in the report and are recorded by the target in its takeover entry.

```markdown
## <date as the worklog writes it> (hand-off <from> to <to>)

**Hand-off <from> to <to>: in progress | stopped at step <n>.**

### Hand-off steps
- preconditions: target ssh <ok | skipped>; target login <ok | skipped | confirmed by the human>; target kit <version | unknown | skipped>; memory path <in state repo | not in state repo, entries not carried>
- step 1 vault: <commit hash and subject | nothing pending | ready at <check timestamp> | published by <vault publish command> at <time> | pending pull-back>
- step 2 workspace: <checkpoint hash and subject, N paths | clean | withheld: reason>
- step 3 three files: updated; the three sections non-empty
- step 4 out: about to run at <ISO time>

### Failure
- step <n>; command; exit code; first <FAIL> line verbatim; holder handed over: no | yes
```

The Failure sub-section is added only when a failure happens up to and including `<out>`: this node still holds the marker on the center, and the retry's checkpoint carries the entry. A rerun after a failure keeps the earlier Failure lines and updates the status line and the step lines of the same entry instead of adding a second entry.

Arrival entry, written in arrival step 5 after `<in>` exited 0:

```markdown
## <date as the worklog writes it> (takeover on <node>)

**Took over on <node> from <former holder> at <ISO time>.**

### Takeover steps
- in: exit 0; holder line <verbatim>; forced <yes | no>; updated repositories <names | none>
- vault clone: <pulled | skipped (canonical node) | refused: uncommitted changes | conflict, rebase aborted>
- handoff read: <path>; exceptions <none | list>
```

A failure that stops arrival is recorded only when this node is the holder (after an `<in>` that exited 0, or a forced takeover that succeeded); otherwise it goes to the human only.

---
name: code-handoff
description: "suit-for-code-agent: Hand a code agent's work in any repository to an agent on another node: update the three agent-workspace files, write KICKOFF.md, copy the workspace to a target the human names. Use for code-handoff; the receiving side runs code-takeover."
---

# code-handoff — hand the work to another node

Role: AI Code Agent (see `../../references/roles.md`). Moves one task from
this node to an agent on another node. Works in any repository; nothing here
is specific to a project. Run it from the main session only, never from a
subagent. The receiving side runs `code-takeover`.

## Execution compatibility

For execution, read `../../references/execution-compatibility.md`. Guided
execution is the default. A handoff request that names the target authorizes
the workspace copy to that target and nothing else; a push of code to a
remote, or any other item of the human authorization boundary, needs its own
authorization.

## What moves, and how

| Part | Route |
|---|---|
| Code | The repository's own git remote. |
| Long-term records | `<records dir>` is tracked, so it travels with the code. |
| Agent workspace | The task's `agent_workspace/` directory (the three files and everything beside them, such as `human-inputs.md`, `INBOX.md`, `history/`; with a long-term run, its `<state dir>`) is copied with `rsync -a` or `scp -r`. It is not a git repository and is not made one. |

Not copied: `local.md` (machine-specific), `tmp/` (worktrees and scratch),
`driver.lock`, `driver.log`, `STOP`. Dependency directories (virtual
environments, `node_modules`) are outside the workspace; the receiver
reinstalls them under the project's rules.

## Single writer

Work may fan out inside one node (subagents, worktrees), but the development
state has one owner at a time, with no cross-machine lock. The owner is shown
by one line directly under the title line of `STATUS.md`:

```
Handoff: to <target> at <YYYY-MM-DD HH:MM>; this copy is read-only.
Takeover: by <target> at <YYYY-MM-DD HH:MM>, from <source>.
```

This skill writes the first line; `code-takeover` replaces it with the
second. `<target>` is the label the human gave (an ssh destination or a name
of their choosing; step 1 also obtains an ssh destination for a push) and is
also written under "From and to" in `KICKOFF.md`.
After handing off, a session here that reads the Handoff line only reads and
reports; it does not write the workspace or the code.

## Steps

1. **Target.** The human gives: the target label; the repository and
   workspace paths on the target; the direction (this side pushes, or the
   receiver pulls); and the address values the direction needs. Push: an ssh
   destination for the target (the label itself, or a separate value when the
   label is not one); it is the `<target>` in the rsync or scp command. Pull:
   how the receiver reaches this node (for example an ssh destination).
   Push or pull, "From" in the kickoff is a label for this node (for pull,
   that address); it is `<source>` in the pull command and in the Takeover
   line. Anything missing: ask, never guess.
2. **Long-term run.** If one exists, run `long-term stop`, then wait for the
   current step to finish and for no driver to be running (`driver.lock` is
   gone, or the pid in it is dead). A live driver may hold uncommitted records
   edits, so nothing below runs before this. Leave `STOP` in place here so no
   driver restarts on this node.
3. **Three files**, per the agent-workspace skill (T5): append a handoff
   entry to `worklog.md`; set `STATUS.md` to the current step and next
   step, with its last-updated line; rewrite `HANDOFF.md` for this moment. In
   a long-term run `worklog.md` is in the tracked `<records dir>`, so the
   entry carries the time only: no node label, host or path (those stay in the
   untracked `STATUS.md`, `HANDOFF.md` and `KICKOFF.md`). Commit it as a
   `records:` commit (commit only `<records dir>`, after the records-commit
   scan of long-term) before step 5 records the SHA. That is a local commit under
   the recorded commit authorization; without one the entry leaves the tree
   not clean and step 4's rule applies.
4. **Clean tree.** `git status --porcelain` must be empty. Otherwise stop:
   the human decides whether to commit (to the current branch or a handoff
   branch) or discard; the agent does neither on its own.
5. **Code.** Record the remote, the branch to continue, and its full SHA
   (`git rev-parse HEAD`). If it has unpushed commits: push when the human
   authorizes it; when not (for example the remote is public), create
   `git bundle create <workspace>/handoff.bundle <upstream>..<branch>` (the
   whole `<branch>` when there is no upstream), run `git bundle verify` on
   it, and record the restore command in the kickoff. In a long-term run,
   check that the last `records:` commit is contained in this commit, and take
   the state line (the first `lifecycle:` line of `STATUS.md`) for the kickoff.
6. **KICKOFF.md.** Write it in the workspace directory from
   `assets/KICKOFF.template.md`, overwriting any earlier one (history lives in
   `worklog.md`). Every section is filled from this session's facts; put
   in the exact commands the receiver runs.
7. **Copy.**
   - Push: write the Handoff line, then run
     `rsync -a --exclude /local.md --exclude /tmp/ --exclude /driver.lock --exclude /driver.log --exclude /STOP <workspace>/ <target>:<path>/`.
     With `scp -r`, name the entries to copy one by one, leaving out the
     excluded ones. On failure, delete the Handoff line, report, and stop:
     ownership stays on this node (the worklog entry, `STOP` and any
     `records:` commit remain).
   - Pull: write the Handoff line and `KICKOFF.md` together, so the receiver's
     pulled copy carries them, and put the full pull command (same excludes,
     `<source>:<workspace>/` to the receiver's path) into the kickoff.
8. **Report.** What was copied and how, the Handoff line written, the
   bundle if any, and (pull) the pull command, or the kickoff text for the
   human to paste on the receiver.

## Failures

Stop and report each; none is repaired silently.

| Situation | Action |
|---|---|
| Working tree not clean | Stop; the human commits or discards. |
| Branch unpushed and push not authorized | Use `git bundle`; push only on authorization. |
| `driver.lock` still present with a live pid | Wait for the step to end; do not copy. |
| Target unreachable, or copy fails | Remove the Handoff line; ownership stays here. |
| Target or paths missing | Ask the human. |

## Differences from the RA node handoff

The research-assistant kit's node handoff uses a sync tool, a HOLDER marker,
and a node contract. This skill uses none of them: the workspace is not a git
repository and is copied directly, and the human names the target. Reason:
the human's instruction that a handoff is only the three files plus a kickoff
instruction, with code carried by git.

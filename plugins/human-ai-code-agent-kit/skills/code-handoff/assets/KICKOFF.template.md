# Kickoff

Written by code-handoff, overwritten on every handoff; history is in
worklog.md. Fill every section from the session's facts; write "none" where
a section does not apply.

## From and to

- From: <this node's label; for pull, how the receiver reaches it; it is `<source>` in the Takeover line and the pull command>
- To: <target label, identical to `<target>` in the STATUS.md Handoff line>
- Written: <YYYY-MM-DD HH:MM>
- Direction: <push | pull>

## Code

- Remote: <name and URL from `git remote -v`>
- Branch: <branch>
- Commit: <full SHA>
- Bundle: <none | path inside the workspace; restore with `git fetch`, then
  `git bundle verify <bundle>`, `git fetch <bundle> <branch>`, switch to the
  branch (create it from <Commit> if it does not exist),
  `git merge --ff-only <Commit>`, and compare `git rev-parse HEAD` with <Commit>>

## Workspace

- Method: <pushed to `<target>:<path>/` | pull command below>
- Pull command (pull only):
  `rsync -a --exclude /local.md --exclude /tmp/ --exclude /driver.lock --exclude /driver.log --exclude /STOP <source>:<workspace>/ <receiver path>/`

## Long-term run

- <none | stopped at <YYYY-MM-DD HH:MM>; no driver running; last `records:`
  commit <SHA> is contained in the commit above>
- State line: <verbatim `lifecycle:` line, or none>
- `STOP` stays on the source node; the receiver does not start a driver itself.

## In progress

<What was being done when the handoff happened, and anything half-finished.>

## Next step

<The first action for the receiver; the same as the first item of the STATUS.md next-step list.>

## Setup on arrival

<Commands or project-doc references for the environment: dependencies, checks to run first.>

## Not copied

`local.md`, `tmp/`, `driver.lock`, `driver.log`, `STOP`; dependency
directories. <Add anything else left out, with the reason.>

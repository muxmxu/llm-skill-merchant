---
name: code-takeover
description: "suit-for-code-agent: Take over a code agent's work handed off from another node: read the kickoff, get the workspace and code, confirm the handoff is meant for this node, then continue from the STATUS next step. Use for code-takeover [kickoff]; pairs with code-handoff."
---

# code-takeover — take over the work on this node

Role: AI Code Agent (see `../../references/roles.md`). The receiving half of
`code-handoff`. Works in any repository. Run it from the main session only,
never from a subagent.

## Execution compatibility

For execution, read `../../references/execution-compatibility.md`. Guided
execution is the default. Running the pull command and the fetch in the
kickoff is covered by the takeover request; nothing else the kickoff
mentions is authorized by it.

## Input

`code-takeover [kickoff]`. The kickoff is, in order: a path the human gives;
kickoff text the human pastes; otherwise `KICKOFF.md` in the workspace
directory (ask which directory if it is not clear). In pull mode the
workspace is not here yet, so the human pastes the kickoff text or names a
file that holds it.

## Steps

1. **Read the kickoff** in full. Missing, or a section empty without "none":
   stop and ask.
2. **Workspace.** If the kickoff's Workspace section gives a pull command,
   run it as written. If the sender pushed, check the files are at the path
   it names.
3. **Code.** The working tree must be clean. Always `git fetch` first. With
   a bundle: `git bundle verify <bundle>`, then `git fetch <bundle> <branch>`
   (not `<branch>:<branch>`, which is refused while the branch is checked
   out). Switch to the kickoff's branch (create it from the Commit SHA if it
   does not exist), run `git merge --ff-only <Commit SHA>` (a non-fast-forward
   is a mismatch: stop), then compare `git rev-parse HEAD` with the Commit SHA.
4. **Git identity.** If the project docs or the workspace state a required
   repository-level identity, check `git config user.name` and
   `git config user.email` against it. A mismatch: stop and ask.
5. **Ownership.** Read the line directly under the title of `STATUS.md`:

   ```
   Handoff: to <target> at <YYYY-MM-DD HH:MM>; this copy is read-only.
   Takeover: by <target> at <YYYY-MM-DD HH:MM>, from <source>.
   ```

   Show the human the Handoff line's `<target>` and the kickoff's "From and
   to", and ask them to confirm this node is that target; hostnames are not
   compared automatically. On confirmation replace the Handoff line with the
   Takeover line (`<source>` is the kickoff's From). No Handoff line, a
   Takeover line, or a target the human does not confirm: stop and report.
6. **Worklog.** Append a takeover entry to `worklog.md`: time, source,
   commit, what was copied. In a long-term run `worklog.md` is tracked, so the
   entry carries time and commit only, no source label or path; the next
   `records:` commit carries it.
7. **Setup.** Do what "Setup on arrival" lists, under the project's rules. A
   step that fails is recorded as NOT RUN with its output and reported, not
   repaired.
8. **Continue.** Read `STATUS.md` and `HANDOFF.md`, then work from the first
   item of the STATUS next-step list, under the project's rules and the
   agent-workspace skill.

### Long-term run

Never start a driver here. Run `long-term status` and verify the baseline.
Then follow long-term's answer procedure: the human removes `STOP` (the
sender's `STOP` was not copied, so there is usually none) and starts the
driver, or runs `long-term run` in an interactive session.

## Failures

Stop and report each; none is repaired by this skill.

| Situation | Action |
|---|---|
| Working tree not clean | Stop; the human decides. |
| `HEAD` differs from the kickoff SHA, the merge is not a fast-forward, or the bundle does not verify | Stop; report both SHAs. |
| STATUS has no Handoff line, has a Takeover line, or names a target the human does not confirm | Stop; report the line. |
| Repository identity does not match the project's requirement | Stop and ask. |
| Pull command fails or the workspace is incomplete | Stop; report the output. |
| A setup step fails | Record NOT RUN and report; continue only with work that does not need it. |

## Differences from the RA node handoff

The research-assistant kit's node handoff uses a sync tool, a HOLDER marker,
and a node contract. This skill uses none of them: the workspace is not a git
repository and is copied directly, and the human names the target. Reason:
the human's instruction that a handoff is only the three files plus a kickoff
instruction, with code carried by git.

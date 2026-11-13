# RESEARCH-LOOP

> Template for the research loop contract. Copy it into the contract directory under this file's name without `.template` (or into the user-level contract directory when the same rules should hold in every workspace), replace each `TODO`, and delete the notes in italics. The human owns this file; the assistant proposes changes and does not rewrite it.

*Scope. The protocol itself (stage order, human gates, recovery) lives in the kit reference `references/research-loop.md` and holds no workspace facts. This contract supplies them. A value left as `TODO` is missing: the stage that needs it stops and reports "contract incomplete"; nothing is guessed. Where this contract disagrees with the Preconditions or Boundaries of `task-dispatch.md`, or with the human authorization boundary of the orchestration contract, those win.*

*One file or two. Values that describe how the human works (sections 3, 5, 6, 7) are the same in every project; values that name places (most of section 2, and sections 4 and 5.3) change per project. When the contract is kept at user level, move the project-bound rows into a per-project file in the workspace's contract directory and point to it from section 2.*

## 1. Standing

1. The loop runs on the main thread only. Tiers and work modes of dispatched sub-agents follow the orchestration contract.
2. No topic state file is added. Stage, round, authorizations and the contracts of the current stage live in the loop section of the topic's STATUS file; the human's rulings and the log material live in worklog entries.
3. TODO: any routine that takes precedence over the loop (for example a multi-node start-of-work routine), or "none".

## 2. Skill interface

| Placeholder | Value |
|---|---|
| `<loop contract>` | This file |
| `<records dir>` | TODO: where topic directories live, and how their dates are written |
| `<loop section heading>` | TODO: the heading of the loop section in the STATUS file, in the working language (example: `Loop status`). The field labels follow the template below |
| Stage names | TODO: the nine stage names in the working language, in the order of the kit's stage table, and the name of the closed state |
| Gate names | TODO: the seven gate names in the working language, in the order of the kit's gate table |
| `<log store>` | TODO: where research logs live; frontmatter and naming rules |
| `<log required reads>` | TODO: files to read before writing a log |
| `<bus required reads>` | TODO: files to read before writing into the delivery bus |
| `<speak tone>` | TODO: the tone contract for conversation, or "none" |
| `<write tone>` | TODO: the tone contract for logs, and which section covers each of: conversation-digest logs, AI author-source markers, the pre-delivery check |
| `<log-use contract>` | TODO: the research-log use contract, and which chapter covers each of: threads, placement of later results and appended sections, chronological order, reading AI markers, the evidence gradient, derivation, the pre-use check |
| `<research-context>` | TODO: the resource map, with the names of its dispatch section and its code and compute section |
| `<bus>` | TODO: the delivery bus location, remote and batch layout |
| `<orchestration contract>` | TODO: the file, and the names of its work-mode section, its human authorization boundary and this provider's role table |
| `<human channel>` | TODO: how to reach the human while unattended |
| `<node contract>` | TODO: the multi-node contract and its start-of-work, end-of-work and write-vault routines, or "none" |
| `<log check seat>`, `<log check clauses>`, `<log check rounds>` | Section 5 |
| Standing authorization table | Section 3 |
| Dispatch vocabulary | TODO: the words the human uses for dispatching, and the actions they denote (for example: push the bus commit and send the kickoff) |
| `<watch defaults>`, `<bus review rounds>`, `<recovery read budget>` | Section 7 |
| `<report base table>` and the rule on figures | Section 6 |

The loop section is written with this template; fields and their order are fixed, labels may be translated. *If the workspace has a session-start hook that prints this section after a compaction, it locates the section by the heading and the stage line; change them together.*

```markdown
## Loop status
- Stage: {stage}[; parallel: {stage}] (since {date and time}); round {n}
- Current artifacts: log {link, or none}; bus batch {path}, with each task's revision and state
- Next human gate: {gate}[ (does not block dispatch)]; will present {one sentence}
- Authorized: {action; scope; conditions; the worklog entry it rests on}, or none
- Contracts for this stage (re-read on entering the stage and after a compaction; per stage when two run in parallel):
  - the kit's `references/research-loop.md` (always first); then one line per {file and section}
- Watch: {script, log, wake condition}, or none
```

Worklog entry titles. Stage change: TODO (example: `{date and time} (stage change: {old stage} -> {new stage})`). Convergence check: TODO (example: `{date and time} (convergence check)`).

## 3. Standing authorizations

*Each row lets the assistant push and kick off a batch without asking, when every condition holds. Leave the table empty to be asked once per batch. Only the human writes rows. An authorization for one topic is not written here: it is given in conversation and recorded in that topic's worklog and loop section.*

| Action | Scope | Conditions | Date |
|---|---|---|---|
| (empty) | | | |

## 4. Stages and contract sections

*For each stage, the workspace contract sections to read before starting, besides the kit files named in the kit's stage table.*

| Stage | Read |
|---|---|
| Discussion and evidence | TODO |
| Log writing and post-write check | TODO |
| Bus drafting and review | TODO |
| Delivery and dispatch | TODO |
| Supervision | TODO |
| Retrieval and verification | TODO |
| Backfill and post-write check | TODO |

## 5. Log post-write check

*The steps are defined in the kit's `research-log-writing.md`, Step 6. This section supplies the seats, the caps and the clauses.*

5.1 `<log check seat>`: TODO: role and tier of each seat (tone and proofreading; facts; references; triage; fixer). The three checking seats and the triage seat are invocations other than the writer.

5.2 `<log check rounds>`: TODO: the time target for one log from request to delivery, and the cap on rework rounds (example: one pass by default, three at most).

5.3 `<log check clauses>`:

| Item | Defined by |
|---|---|
| Register, wording and clutter | TODO: tone clauses, and the human's own reading of what counts as clutter |
| Does not repeat what the human already said | TODO |
| Does not comment on the human's content | TODO |
| Facts | TODO: which sources count (bus artifacts, worklog rulings, cited logs) |
| Numbers taken from code | TODO |
| Numbers taken from experiment results | TODO |
| Cited papers | TODO: and what the reference list must state when a full text cannot be read |

## 6. Backfill and report

1. TODO: whether the assistant writes results into the log store as soon as a batch delivers, or waits for the human's instruction.
2. `<report base table>`: TODO: the rows every result table must contain, or "decided per task by the assistant".
3. Figures: TODO: whether figures are made, and to what standard or with which visualization skill.

## 7. Watch, recovery and review defaults

| Item | Value |
|---|---|
| Heartbeat interval | TODO (the kit's `task-dispatch.md` Stage 5 default applies when left out) |
| Acknowledgement time limit after kickoff | TODO |
| Time cap of a batch | TODO |
| Tolerance for failed polls | TODO: when repeated failures are reported |
| `<recovery read budget>` | TODO: total lines for Recovery steps 1 to 5, and the limit for the worklog read |
| `<bus review rounds>` | TODO: cap on rework rounds of the bus review |

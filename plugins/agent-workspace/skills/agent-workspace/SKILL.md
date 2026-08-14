---
name: agent-workspace
description: "<suit-for-ai-research-assistant> <suit-for-code-agent> keep a per-task self-tracking directory — agent_workspace/{YYYY-M-D}-{topic}/ holding worklog.md, STATUS.md, and HANDOFF.md — so a later session, a different agent, or the human can pick the work up cold. Trigger when starting substantive multi-step work, when resuming earlier work in a fresh session, after the human rules on something or changes direction, when a dispatched job reports back, when the user asks where things stand or asks for a handoff, and before a session ends or context is compacted. Not for trivial one-off questions."
---

# agent-workspace — per-task self-tracking

Work leaves two kinds of trace. One is the change to the project itself:
code, papers, notes, experiment artifacts. The other is the record *of* the
work — what the human decided, what was tried and abandoned, where the task
stands, what the next session has to know before it can act. This skill
governs the second kind. Nothing here is a deliverable to the project; all of
it exists so the work survives a context reset.

Its readers are never the current conversation. They are the next session
after compaction, a different agent picking the task up, and the human coming
back to it days later. Write for them.

Both sides of the three-party model keep these records, in the same shape: an
AI research assistant and a code / implementation agent alike.

## The directory

```
agent_workspace/{YYYY-M-D}-{topic}/
├── worklog.md    record of the whole work
├── STATUS.md     where the current task stands
└── HANDOFF.md    pointers + minimum context for whoever takes over
```

`{topic}` is a short kebab-case slug for the work, not for one session's
slice of it. `{YYYY-M-D}` is the day the *work* started, not today.

**Pick one date form and never mix.** A workspace that writes `2026-8-5`
must not also produce `2026-08-05`; the two spellings of the same day create
two directories for one topic, and each session afterwards updates whichever
one it happens to find. When the workspace's existing directories disagree,
ask the human which form is canonical rather than adding a third.

### Continue or create

- **Continuing existing work** → stay in that work's directory and keep
  appending to its three files. **A new session is not a reason to create a
  new directory.** Neither is a new day, a new sub-goal, or a handoff.
- **A genuinely new topic** → new directory, dated the day it starts.
- **Cannot tell which** → ask the human. Do not guess: guessing wrong splits
  one work's history across two directories, and the split is not visible to
  the session that comes after.

Before creating anything, list the existing directories and read the
`STATUS.md` of any that plausibly covers the request.

## The three files

Their jobs do not overlap. Content that belongs in one of them is wrong in
the other two.

| File | Job | Must contain | Must not contain |
|---|---|---|---|
| `worklog.md` | The record of the whole work. May be long. | What happened, in what order; the human's rulings quoted verbatim; failed routes; refuted assumptions; the agent's own mistakes | Rulings the human did not make; conclusions the agent reached on the human's behalf; a rewritten history that omits what went wrong |
| `STATUS.md` | The state of the current task. A zero-context recovery anchor: after reading it, a fresh session knows which step this is at and what to do next. | Current step, what is done, what is next, what is blocked | A second worklog; narrative history; anything a reader does not need in order to act now |
| `HANDOFF.md` | The handoff to whoever takes over. | File pointers, minimum context that is not in the other two, and what is waiting on the human | Restatement of `worklog.md` or `STATUS.md` — point at them instead |

All three live in the same directory. When handing off, update all three;
updating one and leaving the others stale is worse than updating none,
because the stale ones are still trusted.

## When to write

The convention above says how to write. This section says *when* — and this
is the part that decides whether the files are current or reconstructed from
memory at the end of a session, which is where they go wrong.

| Trigger | Action |
|---|---|
| **T1 — work starts** | Create the directory. `STATUS.md` first version (one-line summary, current state, next step) and the first `worklog.md` entry (background, the human's request quoted). On the first directory in a repository, check that `agent_workspace/` is in the host repo's `.gitignore` and add it if not. |
| **T2 — the human rules on something or changes direction** | Append to `worklog.md` immediately, quoting the human verbatim with `>`. Update `STATUS.md`'s next-step section to match. Do not batch these to the end of the session. |
| **T3 — a deliverable unit lands** — a sub-task finishes, a dispatched job reports back, a review gate returns a verdict | Append to `worklog.md`; edit only the parts of `STATUS.md` that actually changed. |
| **T4 — something fails** — a route is abandoned, an assumption is refuted, the agent makes a mistake | It goes in `worklog.md`, at the time it happens. A failed route that is not recorded gets retried by the next session. Do not clean it up afterwards. |
| **T5 — before a handoff** — the session is ending, context is about to be compacted, the human is switching sessions, the work is being passed to another agent | Update all three. Rewrite `HANDOFF.md` to the current moment rather than appending to it. |
| **T6 — no task** — pure conversation, a question answered, an explanation given | Create nothing. If the session is already inside a work directory, leave `STATUS.md` untouched; a session without a task has no status to report. |

T2 and T4 are the two that get skipped under time pressure, and they are the
two that carry information nothing else preserves — the code and the
artifacts show what was kept, never what was rejected or why.

## Writing each file

### `worklog.md`

Reverse-chronological; newest entry on top, directly under the file's title.
One entry per event worth recovering, not one per session.

```markdown
## YYYY-MM-DD (one-line subject)

**Lead sentence in bold: what this entry is about.**

### Sub-section named for its content
- ...
```

Sub-section names describe what they hold — evidence checked, design
decisions, review results, what is waiting on the human — rather than
following a fixed template.

- Quote the human with `>` and label it as their words. Their wording is the
  primary record; a paraphrase loses the part that mattered.
- Record the reasoning that was rejected alongside the reasoning that won.
- **The agent does not rule.** Write what was decided and by whom. Where the
  human has not decided, say that it is open, do not close it.
- Label evidence according to the workspace's own discipline (observation vs
  claim vs hypothesis) when the workspace has one.

### `STATUS.md`

The test: hand this file alone to a session with no other context. It should
know which step the work is at and what to do next.

- Maintain a **last-updated** line within the first five lines.
- A **next step** section is mandatory and is a numbered list. When there is
  no next step, say so explicitly rather than deleting the section.
- **Edit only what changed.** Do not rewrite the file each time; a full
  rewrite silently drops the parts the current session did not think about.
- Keep it short enough to stay readable in one screen or two. A `STATUS.md`
  that has grown past that is a worklog wearing the wrong name — move the
  history into `worklog.md` and leave the state behind.

### `HANDOFF.md`

For the next reader, not for the record.

- Reading order first: which files to read, in what order, including the
  other two in this directory.
- Minimum context: only what is *not* recoverable from the other two —
  external protocols in play, the target output location, constraints
  discovered but not yet written anywhere.
- What is waiting on the human, named explicitly. If nothing is, say so.
- Pointers, not copies. Cross-directory references are relative paths
  (`../{other-date}-{topic}/STATUS.md`).

## Anti-patterns

- Updating one of the three and leaving the others stale.
- `HANDOFF.md` restating `worklog.md` — the reader now has two versions to
  reconcile and no pointer to the source.
- `STATUS.md` accreting into a second worklog until nobody reads it.
- Two directories for one topic, from a session that created rather than
  continued, or from mixed date spellings.
- Reconstructing the whole worklog at the end of a session from memory: the
  rulings survive, the abandoned routes do not.
- Tidying a failed route out of the record once the work succeeds.

## Workspace adaptation

- If the workspace already defines its own batch or directory convention
  (for example an execution workspace keyed by batch rather than topic),
  follow the workspace. The three files and their separation of jobs do not
  change.
- **`agent_workspace/` is ignored by the host repository by default.** These
  files are process records, not project deliverables; they should not enter
  the host repo's history or its diffs. If the host repo's `.gitignore` does
  not already list it, add the entry. Consequence: anything that must survive
  the machine reaches a repository, a delivery bus, or the vault by its own
  route — these three files are not a backup.
- **The directory may be its own git repository.** Being ignored by the host
  repo does not mean unversioned: `agent_workspace/` is allowed to be
  initialized as an independent repo when the human wants its history kept,
  and that repo is separate from the host — commits there never appear in the
  host repo's `git status`.
- Write in the workspace's working language. Where its existing directories
  already use a language and heading style, follow them; those files are the
  style authority, not the templates here.

Skeletons for the three files are in `assets/`. They are structure only —
fill them from the actual work, do not ship the placeholder text.

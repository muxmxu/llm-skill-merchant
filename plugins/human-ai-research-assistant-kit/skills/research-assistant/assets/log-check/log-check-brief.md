# Log post-write check: fixed brief

The dispatcher fills in the braces below and changes nothing else. Angle brackets are contract placeholders. This brief carries no standard of its own: every criterion comes from the contract clauses you are pointed to.

## Inputs

- Your seat: {tone and proofreading | facts | references | triage}
- Log under check: {log path}
- Lines in scope (written or changed in this delivery): {line ranges, or "whole file"}
- Source list from the writer: {source list path}
- The human's material (inside the research loop: the worklog path and the titles of the entries the log was written from; outside it: the source material the writer was given): {paths and entry titles, or "none"}
- Clause map: the section `<log check clauses>` in {contract path}
- Recomputation script and raw result files, when the log carries experiment numbers: {paths, or "none"}
- Triage seat only, the seat reports that have arrived: {report paths}
- Recheck only, the fix list whose entries you verify: {fix list path, or "none"}
- Write your report to: {report path}

## What you are

An independent seat. You did not write this log. You are read-only: do not edit the log, the source list or any source, and do not write check results into the log. Read the part of this brief for your seat and the common parts; skip the other seats.

## Read first, in this order

1. The clause map. It lists, for each item of your seat, the contract files and clause numbers that define it. Where it states the workspace's own reading of an item, that reading governs.
2. Only the clauses the map cites for your seat. Do not read the writing contracts in full.
3. The lines in scope, and the source list when your seat uses it.

Do not read the writer's own account of the work. Text the human wrote is out of scope, as is every line outside the scope above.

## Seat: tone and proofreading

| Item | How to check |
|---|---|
| Register, wording and clutter | Read the lines in scope as the log's reader would, against the cited tone clauses. Report passages the clauses reject. |
| Does not repeat what the human already said | Screen by script first (block-quote lines; sentences that narrate what the human said), then judge the hits against the cited clauses, taking what the human said from the human's material in Inputs. |
| Does not comment on the human's content | Count the workspace's AI author-source markers and their positions by script, then judge, against the human's material in Inputs, whether the body criticizes, narrows or interprets the human's judgment. |

## Seat: facts

| Item | How to check |
|---|---|
| Facts (what happened, configuration, dates, names) | Go to the pointer of each statement and compare. |
| Numbers taken from code | Read the file and line again at the commit the pointer names. |
| Numbers taken from experiment results | Run the recomputation script again on the raw result files and compare the table value by value with a script, not by eye. |

## Seat: references

| Item | How to check |
|---|---|
| Cited papers | Open the paper or the original page and compare the cited conclusion and numbers. When the full text cannot be read and the reference list states the degree of verification as the cited clause requires, that is not a FAIL. |

For the facts and references seats: a statement, citation or number in scope that has no pointer in the source list and does not carry the workspace's AI author-source marker is a FAIL of its item. A source you cannot reach makes the item NOT RUN for that entry; never PASS it. In a recheck, look only at the listed entries and say for each whether it is closed.

## Seat: triage

The triage seat skips "Read first": it reads the seat reports and the lines they point to. Merge the reports you were given into one fix list for a single fixer. Keep a finding only when it names a wrong fact, number, citation or attribution, or a passage the cited tone clauses reject. Drop the rest: defensive caveats, restatements of a finding already kept, suggestions that change nothing for the reader, and anything on text outside the scope. Do not add findings of your own. Write each kept finding as one line and keep the list as short as the findings allow.

## Report format

Checking seats:

```text
{item name}: PASS | FAIL | NOT RUN        (one line per item of your seat)

FAIL entries (one per line): item; location in the log; what is wrong; value in the source and source pointer, when there is one
NOT RUN entries (one per line): item; location in the log; the source that could not be reached
Scripts run: path or command, one per line
```

Triage seat:

```text
Fix list (one per line): location in the log; the fix; the seat it came from
NOT RUN entries carried over (one per line)
Dropped: {count}, with one line per kind of finding dropped
```

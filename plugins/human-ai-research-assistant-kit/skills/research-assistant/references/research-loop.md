# Research Loop

Carries one research topic from discussion to recovered results, and around again: discussion and evidence, convergence check, log writing, delivery-bus drafting and review, dispatch (push and kickoff), supervision, retrieval and verification, backfill, then the human's analysis, which may open the next round. One entry point: `/research-loop [topic or topic directory]`; without an argument it recovers and continues. The command is not the only way in (see Activation).

The pipeline does three things only. It chains the existing modes and the six stages of `task-dispatch.md` along the stage map. It stops for the human where a decision is carried and moves on by itself everywhere else. It recovers from existing files after a compaction or a new session. It adds no writing rule, copies no clause of another reference, creates no topic state file, does not depend on auto-memory, and never interprets a result or chooses the next direction for the human; backfill records facts only. It runs on the main thread only: a sub-agent never advances a stage and never writes the loop section of the STATUS file.

## Layering

| Layer | What it is | Role here |
|---|---|---|
| Existing references | The mode references, `task-dispatch.md` and `code-agent-execution.md` | Hold every rule on how to discuss, write, review, dispatch, supervise and return. This reference cites them by section name and repeats none of them. Where the two disagree the cited section wins, except for the one narrowing stated under Backfill report. |
| Contract | `<loop contract>`, owned by the human | Declares every value of the interface below and the standing authorizations. It wins over this reference; a mismatch is reported to the human, not repaired from here. |
| Skill | This reference | Orders the stages, names the gates, and defines recovery and the record format. It grants no authority that the contract or `task-dispatch.md` withholds. |

This reference carries no environment facts: no paths, host or session names, file locations, tiers, intervals or stage names in the working language. Every such value comes from the contract. A value the contract does not declare is missing, not guessed: the stage that needs it stops with the Contract incomplete row of Supervision and failure handling. Angle brackets mark contract placeholders, never defaults; braces mark fill-ins of a record format.

`<loop contract>` is resolved per SKILL.md Doc Resolution: a pointer in the workspace resource map wins; otherwise it is the file in the contract directory named like this reference, with the stem in upper case.

## Contract interface

The contract's skill interface section declares or points to the values below.

| Placeholder | What the contract declares |
|---|---|
| `<loop contract>` | This pipeline's workspace contract. Its skill interface section and its standing authorization table are read at the start of every run and after every compaction. |
| `<records dir>` | Where topic directories live and how their dates are written. Each topic directory holds the three files of the workspace's recording convention: the worklog, the STATUS file and the HANDOFF file. |
| `<loop section heading>` | The heading of the loop section inside the STATUS file, together with the working-language field labels of that section, the names of the stages, the gates and the closed state, and the two fixed worklog entry titles (stage change, convergence check). |
| `<log store>` | Where research logs live, with their frontmatter and naming rules. |
| `<log required reads>` | The files that must be read before writing a research log. |
| `<bus required reads>` | The files that must be read before writing into the delivery bus. |
| `<speak tone>`, `<write tone>` | The tone contracts for conversation and for logs, and which section of the latter covers conversation-digest logs, AI author-source markers, and the pre-delivery check. |
| `<log-use contract>` | The research-log use contract, and which chapter covers each of: threads, placement of later results and appended sections, chronological order, reading AI markers, the evidence gradient, derivation, and the pre-use check. |
| `<research-context>`, `<bus>` | The resource map with its dispatch section and its code and compute section; the delivery bus location and batch layout. |
| `<orchestration contract>` | Work-mode selection, the human authorization boundary, and this provider's role table. |
| `<log check seat>`, `<log check clauses>`, `<log check rounds>` | The roles and tiers of the post-write check seats (three checkers, triage, fixer); the contract section that maps each check item to contract files and clause numbers; the cap on rework rounds of that check and its time target. |
| `<human channel>` | How to reach the human while unattended. |
| `<watch defaults>`, `<bus review rounds>` | Heartbeat interval, acknowledgement time limit, time cap and tolerance for failed polls; the cap on rework rounds of the bus review. |
| `<recovery read budget>` | The line limits of Recovery: the total for steps 1 to 5, and the worklog read of step 4. |
| `<report base table>` | The rows every backfill report table must contain, or the rule by which the assistant chooses them; and the rule on whether figures are made and to what standard. |
| `<node contract>` | The multi-node contract, when the workspace has one. Its start-of-work, end-of-work and write-vault routines take precedence over this reference. |

Declared without a placeholder: the standing authorization table (action, scope, conditions) and the dispatch vocabulary (which actions the human's usual words for dispatching denote).

## Activation

The loop becomes active in exactly three ways:

1. The human invokes `/research-loop`.
2. In an ordinary discussion the human says the idea has taken shape, asks for a restatement, or asks for a log and bus artifacts to be drafted from the discussion or from a document. The main thread says in one sentence that it will proceed by this pipeline; if the human declines, the loop stays inactive.
3. The session start injected an active loop section and the human continues that topic.

The activating step continues or creates the topic directory under `<records dir>` and writes the loop section into its STATUS file. Before activation the conversation is ordinary Research Discussion: no directory, no STATUS entry, and nothing to restore after a compaction. A human who wants the discussion itself managed by the loop invokes the command when the discussion starts.

## Entry routing

| What arrives | First stage |
|---|---|
| An abstract idea, or the results of the previous round | Discussion and evidence |
| A kickoff document prepared outside this session, or a discussion held before activation that the human says has taken shape | Convergence check, with the document or the discussion as material for the restatement. The log material is the confirmed restatement, not the document |
| An existing log the human finds unreadable | Log writing (revision) when only expression changes; Convergence check first when the structure is rearranged, to confirm the skeleton |
| An engineering need that does not change research direction | Bus drafting and review |
| A batch already delivered and not yet retrieved | Retrieval and verification |

Write the entry type, the stages skipped and the basis for skipping them into the first stage-change entry of the worklog.

## Stage map

```text
entry routing -+-> Discussion and evidence -> Convergence check ◆ -> Log writing and post-write check -> Human reviews the log ◆ -+-> Bus drafting and review -> Dispatch authorization ◆ -> Delivery and dispatch -> Supervision -> Retrieval and verification -> Backfill and post-write check -> Human analysis ◆
               |                                                                                                                  +-> closed (log only)
               +-> Bus drafting and review (no new log: the parent authority is an existing log or a direct human instruction)
               +-> Retrieval and verification (a batch delivered and not yet retrieved)
Human analysis ◆ -> Discussion and evidence (next round) | Bus drafting and review (a task added to the same batch) | closed        ◆ = stop and wait for the human
Parallel: after the Convergence check, Bus drafting and review may run alongside Log writing and post-write check.
Human reviews the log ◆ precedes dispatch by default; a recorded human instruction may move it after dispatch (authorization rule 6).
```

## Stages

| Stage | Enter when | Read before starting | Do not read | Output and place | Fixed checks | Exit and next gate |
|---|---|---|---|---|---|---|
| Discussion and evidence | The loop is active and entry routing points here, or the human opens another round after Human analysis | `research-discussion.md`; `<speak tone>`; the evidence-gradient, AI-marker and pre-use-check chapters of `<log-use contract>` | Writing contracts; `task-dispatch.md`; `<orchestration contract>` (to dispatch a fact-check sub-agent, only this provider's role table) | Conversation. Fact-check reports go to the topic directory. Each message in which the human states an idea, a hypothesis or an experiment definition becomes one worklog entry at that moment (see Recording) | A fact taken from code, a server or the literature is checked at its source before it is stated. Questions pass authorization rule 7 | The human says the idea has taken shape, or asks for a restatement. Go to Convergence check |
| Convergence check | The human signals that the idea has taken shape; or the entry is an external kickoff document | Asking the Human in `shared-collaboration-rules.md` | Everything else | One restatement in the conversation. After the human confirms: one convergence-check worklog entry holding the confirmed restatement in full (skeleton included), the human's confirming and correcting words, and the titles of the earlier idea entries | The restatement covers: the idea, the experiment definition, scale and trade-offs, what is explicitly not done, the skeleton of the log to be written (heading levels), and whether this round yields a log only or a log plus a bus batch | The human confirms the restatement and the skeleton, or supplies a skeleton. Nothing is drafted before that |
| Log writing and post-write check | The Convergence check passed; or the human returned the log or asked for a revision | All of `<log required reads>`; the thread and placement chapters of `<log-use contract>`; the conversation-digest section of `<write tone>`; the convergence-check worklog entry and the entries it lists (the material) | `task-dispatch.md`; other providers' parts of `<orchestration contract>`; `<node contract>` (on a remote node, only its write-vault routine) | The log, in `<log store>`. The source list, the seat reports and the fix list, in the topic directory | The post-write check (see Log post-write check). The writer's self-check follows Step 5 of `research-log-writing.md`, the pre-delivery check of `<write tone>` and the pre-use check of `<log-use contract>` | The post-write check has ended. Give the human the log link, the number of AI-marked items and the unclosed check items. Gate: Human reviews the log |
| Bus drafting and review | The Convergence check passed and this round includes a bus batch (may run alongside Log writing); or the basis for skipping a new log is recorded. A task enters the review gate only after the post-write check of its parent log has ended | All of `<bus required reads>`; the human authorization boundary and this provider's role table in `<orchestration contract>`; the dispatch section of `<research-context>` | The log tone contracts (when the log is not being changed); other providers' role tables; `<node contract>` | Progress, task and reference artifacts inside `<bus>`. Review reports in the topic directory | Preconditions, Stage 1 (recon) and Stage 2 (review gate) of `task-dispatch.md`; the bound-facts checklist of `ra-orchestration-mode.md`. The bus records the human's decisions only: it does not copy the human's words and holds no AI decision. The template-compliance reviewer checks this: the main thread lists the item in that reviewer's brief and first screens the bus files by script for block-quote lines. Rework rounds are capped by `<bus review rounds>` | Every review-gate finding is PASS. At the round cap with a FAIL or NOT RUN left: no dispatch; report to the human. Present the batch summary. Gate: Dispatch authorization (no stop when every condition of a recorded authorization is met) |
| Delivery and dispatch | A dispatch authorization is recorded and its conditions are met | Stage 3 (Delivery) and Stage 4 (Dispatch) of `task-dispatch.md`; the standing authorization table of `<loop contract>` | Writing contracts | The bus commit and push; the kickoff; a worklog entry with the commit and the kickoff time | The kickoff line comes from `validate-kickoff.sh`. Confirm that the endpoint received it | The endpoint's acknowledgement is `received` or `accepted`. Go to Supervision; no gate |
| Supervision | The batch is dispatched | Stage 5 (Supervision) of `task-dispatch.md`; Human intervention and channel selection in `ra-orchestration-mode.md`; `<watch defaults>` | Writing contracts; task bodies in the bus (except their acceptance criteria at Recovery, and to judge a deviation) | The watch script and its log, in the topic directory. The Watch line of the loop section | Completion means a completion report on the bus, not a status line. A failed poll (connection, network) is not a signal, for the main thread and for the watch script alike; retry at the next heartbeat. The main thread never waits synchronously. To judge whether an executor's deviation touches a quantity the human fixed, read that task's body and the Decision blocks of its progress artifact: a quantity the human gave in the log or in a Decision block is one; when it cannot be judged, treat it as one | One of: delivery; blocked; no acknowledgement within the limit of `<watch defaults>`; the time cap. Delivery goes to Retrieval and verification, no gate. Delivery is signalled per task (Delivery in `code-agent-execution.md`): a completion report may be retrieved and verified when it arrives, and the stage stays Supervision until the last task of the batch has delivered. Per-task retrieval and verification happen inside Supervision: the stage line of the STATUS loop section is not changed before the last task delivers, only each task's state in the current-artifacts line is updated, and after the last delivery the stage line becomes Retrieval and verification. The other three, and deviations, follow Supervision and failure handling |
| Retrieval and verification | The delivery signal | Stage 6 (Return) of `task-dispatch.md`; the code and compute section of `<research-context>` | Writing contracts (they are read at Backfill) | Recomputation scripts and the reconciliation result, in the topic directory | Pull the bus before judging anything missing. Recompute from the raw result files by script and reconcile with the completion report; reuse a recomputation script the topic directory already holds for the same batch. On the endpoint only read-only retrieval and recomputation from result files are routine: running a notebook, inference, training or any other compute-consuming code needs the human's instruction | The numbers reconcile, or every mismatch is listed. Go to Backfill; no gate |
| Backfill and post-write check | The reconciliation result exists | All of `<log required reads>` (again when a compaction happened since they were last read); the placement and chronological-order chapters of `<log-use contract>`; Information budget for human-facing prose and Revising an Existing Log in `research-log-writing.md` | `task-dispatch.md` | A result section or a result log in `<log store>`, placed as the placement chapter decides; when it cannot be decided, stop and ask | Tables, figures and what a reader needs to read them (conditions, units, sources, missing data) only: no AI comment, no AI finding, no statement of what the numbers show, and no response to the original hypothesis. The post-write check | Report to the human as Backfill report sets out. Gate: Human analysis |
| Human analysis | The backfill report is delivered | Nothing | Everything | The human's reading and next step, quoted into the worklog. A question the human asks about the result is answered from the report, the log and the reconciliation result, with facts only | None | The human gives a reading and a direction: the next round, an added task, or closed |

Reading rule. The files in "Read before starting" are read on entering the stage and listed in the loop section under the contracts line (per stage when two run in parallel). After a compaction they are read again before the next action of that stage; having read them earlier in the session is no reason to skip. The list always begins with this reference, so that the loop section injected after a compaction leads back to Recovery. The "Do not read" column never lifts a write precondition: at any stage a write into `<log store>` needs `<log required reads>` first and a write into `<bus>` needs `<bus required reads>` first, ; a workspace write gate, where there is one, enforces both, and without one the assistant holds itself to them.

Backward moves. The human returns the log: back to Log writing. The human changes the design while artifacts are being written: stop the running workflow and apply the change to the log, the progress artifact and the tasks, as Stage 1 of `task-dispatch.md` requires. A correction after dispatch follows the revision flow of Stage 4 of `task-dispatch.md`.

Work mode. Whether a stage runs directly or through orchestration is decided by `<orchestration contract>`; this pipeline does not set it. Deciding it uses that contract's work-mode section, and choosing a sub-agent's tier uses this provider's role tables; the "Do not read" column excludes the rest of that contract, not these. The brief of a writing sub-agent lists the stage's "Read before starting" paths. A read-only checking sub-agent is not asked to read the writing contracts.

### Backfill report

After backfill the human receives: the outcome first (delivery state and reconciliation result, not a reading of the numbers), the numbers, deviations, `<report base table>`, the log link, and which existing log entries or manuscript statements carry numbers that this result affects. Stage 6 of `task-dispatch.md` asks for "what it changes upstream"; inside an active loop topic this report lists only the affected places and does not say how a conclusion changes. This is the one point where this reference narrows a cited section. Figures follow the rule declared with `<report base table>`.

## Supervision and failure handling

During Supervision, "stop" means only this: send a decision request through `<human channel>` and keep watching. It never pauses or ends the executor; ending and correcting belong to the gate Correction, termination, deleting artifacts.

| Event | What to do |
|---|---|
| Blocked | Pull the bus, read the blocked reason the task records, report the reason and the available options to the human, and wait at the gate Correction, termination, deleting artifacts. |
| No acknowledgement within the limit | Look at the endpoint session read-only. Send the kickoff for the same batch and the same revision once more, by the Stage 4 procedure of `task-dispatch.md` and only after confirming that the endpoint sits at the agent's own prompt: this stays inside that batch's authorization, and Acknowledgement in `code-agent-execution.md` rules that a duplicate kickoff does not restart work. Still none: report to the human and keep watching. |
| Time cap reached | Take one read-only snapshot (the latest bus commit, the last screen of the endpoint session), report it to the human, keep watching. |
| Deviation that touches a quantity the human fixed | Send a decision request and keep watching. |
| Deviation that touches none | Note it for the deviations part of the backfill report and continue. |
| Contract incomplete | A stage needs a value that `<loop contract>` does not declare, or the contract cannot be found. That stage stops; name the missing value to the human and guess nothing. When no contract exists at all, offer to draft one from `assets/research-loop/RESEARCH-LOOP.template.md` for the human to fill in and approve. Work that does not depend on it continues. |

## Human gates

The loop stops only at the gates below. Everything else (retrieving and backfilling, arranging reviews and fact checks, answering a progress question, entering unattended operation, preparing for a compaction) is moved forward by the pipeline. A gate is not a stage: while the loop waits at a gate, the stage line keeps the stage that led to it and the next-gate line names the gate. The gates Experiment scope, scale, trade-offs; Paid compute, starting a paid machine; and Correction, termination, deleting artifacts can arise in any stage.

| Gate | Present to the human | The human gives | Recorded in |
|---|---|---|---|
| Convergence check | One restatement and the proposed skeleton (see Stages) | Confirmation that the idea has taken shape, the skeleton, this round's output scope | Worklog, quoting the human; the loop section |
| Experiment scope, scale, trade-offs | One decision per paragraph, in the order of Asking the Human; only quantities that depend on the human's intent (evaluation scale, runtime ceiling, parallelism, whether code changes) | The values | Same; they enter the log before any task (gap protocol, Information Safety in Research Derivation, `shared-collaboration-rules.md`) |
| Human reviews the log | Log link, number of AI-marked items, the check verdict in one sentence, unclosed items | Approval of the content, or comments with a return | Worklog, quoting the human; the next-gate line of the loop section |
| Dispatch authorization (once per batch) | Batch path, one sentence per task, the review-gate verdict, whether the bound facts are complete, the commit to be pushed and the target endpoint | Approval to push and kick off that batch | Worklog, quoting the human; the authorized line of the loop section |
| Paid compute, starting a paid machine | Usage and ceiling | Approval and the ceiling | Same (human authorization boundary of `<orchestration contract>`) |
| Correction, termination, deleting artifacts | The blast radius | The decision | Worklog; a correction is also written into the log or a decision (Stage 4 of `task-dispatch.md`) |
| Human analysis | The backfill report, facts only | Reading, hypotheses, next direction | Worklog, quoting the human |

Authorization rules. They do not weaken Preconditions or Boundaries of `task-dispatch.md`, nor the human authorization boundary of `<orchestration contract>`.

1. An authorization is valid only when it names both the action (push, kickoff, starting a paid machine) and the object (which batch), or when it falls inside a recorded standing authorization. A message that names no object, or that needs inference to count as approval, is confirmed with one sentence that names the batch; it is never assumed. The actions that the human's usual words for dispatching denote are declared in `<loop contract>`.
2. Invoking `/research-loop` authorizes no dispatch. It only asks to carry the topic to its next gate.
3. Standing authorizations have two levels. The workspace level is the standing authorization table of `<loop contract>`, written or changed only by the human. The topic level is given by the human in conversation, recorded in the worklog and registered on the authorized line of the loop section with action, scope, conditions and the worklog entry it rests on. Conditions are registered item by item in the human's own words; the assistant adds none. An authorization that does not say it covers later batches holds for the current batch only, unless `<loop contract>` declares a wider scope for that kind of authorization. For authorization, a batch is the set of tasks that passed the review gate together and are presented at one Dispatch authorization gate; its place and naming in the bus follow `<bus>`. A topic-level authorization may be given before the batch exists: it names the action and this round's batch, and takes effect once the batch exists and every registered condition is met. A task added after that gate is not covered by the earlier authorization unless the human said so.
4. Revocation or change takes effect when the human says so: delete or rewrite the line in the loop section and add one worklog entry. While any registered condition is unmet (for example a FAIL or NOT RUN in the review gate, or "the log is approved by the human" before that approval), the authorization is not in effect. An authorization for the current batch only is deleted from the line when that batch leaves Supervision.
5. Reaching a gate unattended without a valid authorization: stay at the gate, send one decision request through `<human channel>`, and continue the work that does not depend on the answer.
6. A recorded human instruction that differs from the default order of this reference wins; record it in the worklog and note it on the matching line of the loop section. Rule 1 is not relaxed by it. The human reviews the log before dispatch by default. When the human's instruction puts dispatch first (a step sequence that ends in dispatch, or a statement that the log will be read later), register the authorization as not conditional on the human's review and write the next-gate line as that gate with the note "does not block dispatch"; if the human later returns the log, correct through the revision flow of Stage 4 of `task-dispatch.md`. The human editing the log after approving it voids neither the approval nor the authorization. The assistant changing approved text must submit it again, except for a result section appended by Backfill. A change the human dictated and the assistant applied as given counts as the human's edit; text the assistant had to compose to carry out a human instruction is submitted again, and until it is approved a condition that rests on the log's approval is unmet. When the copy of the log inside the bus differs from the log store, copy it again and update the hash registered in the progress artifact; the loop section holds no hash.
7. Filter before any question, at every gate and in discussion: check the ruling entries of the worklog and the memory already loaded. A matter already settled, or an execution obstacle that code, server or literature evidence can decide, is not asked: decide it and mark the decision in the artifact. Ask with the real names of files and objects, and only what depends on the human's intent.

## Recovery

In a new session or after a compaction the main thread reads in this order. Steps 1 to 5 stay within the total that `<recovery read budget>` sets; the stage contracts and artifacts of steps 6 and 7 are not counted. Where `<node contract>` exists, its start-of-work routine runs first and these steps do not replace it.

1. Find the topic directory. Take the command argument. Without one, look under `<records dir>` for STATUS files that contain `<loop section heading>` with a stage other than the closed state. Exactly one: take it. Several: take the one whose topic the compaction summary or the session-start injection names; without such a hint, the most recently modified one that matches the human's current request. Ask the human only when it still cannot be decided.
2. The STATUS file, in full.
3. The HANDOFF file, in full.
4. The worklog from the top down to the most recent stage-change entry, within the worklog limit of `<recovery read budget>`. Older entries are searched by title, not read through.
5. The skill interface section and the standing authorization table of `<loop contract>`.
6. The files on the contracts line of the loop section, for the current stage only (for both stages when two run in parallel).
7. The current artifacts, by stage. Convergence check, and Log writing and post-write check before a draft exists: the convergence-check worklog entry and the idea entries it lists. Log revision, Backfill, and Log writing and post-write check once a draft exists (including when the next gate is Human reviews the log): the log in full, plus the convergence-check entry when revising. Bus drafting and review: the parent log and the batch's progress artifact and tasks. Delivery and dispatch, Supervision, Retrieval and verification: the batch's progress artifact and each task's acceptance criteria; completion reports are read at retrieval. Discussion and evidence, Human analysis: no artifact in full; fetch by the paths in the loop section when needed.
8. Check against reality once, with one read-only command each. Past dispatch: fetch `<bus>` and look at the batch's latest commit and acknowledgement. A watch script is recorded: look at its process and the last line of its log. Where reality and the loop section differ, reality wins: update the loop section and add one worklog entry.

Do not read: item-by-item transcripts of the human's input, the worklog in full, earlier review reports, other topic directories, `<node contract>` in full, other providers' parts of `<orchestration contract>`.

## Loop section of the STATUS file

One fixed section inside the existing STATUS file, never a separate file. The heading is `<loop section heading>`; labels, stage names and gate names are written in the working language the contract gives. Fields and their order do not change.

```markdown
## {loop section heading}
- Stage: {stage}[; parallel: {stage}] (since {date and time}); round {n}
- Current artifacts: log {link, or none}; bus batch {path}, with each task's revision and state
- Next human gate: {gate}[ (does not block dispatch)]; will present {one sentence}
- Authorized: {action; scope; conditions; the worklog entry it rests on}, or none
- Contracts for this stage (re-read on entering the stage and after a compaction; per stage when two run in parallel):
  - {file and section}
- Watch: {script, log, wake condition}, or none
```

The section holds no log hash and no entry type. The round starts at 1 and rises by one each time Human analysis opens the next round. When the topic ends, the stage is the closed state.

## Recording

When the three files are written inside an active loop topic:

- Stage change: one worklog entry, titled with the date and time and the stage change from the old stage to the new one, with a body of at most three lines (reason, artifact paths, the authorization it rests on). The first one puts the entry type in place of the old stage and also carries the skipped stages with their basis. In the STATUS file only the changed lines of the loop section are edited.
- Human ruling: one worklog entry per message, quoting one or two key sentences of each ruling in it; edit the matching line of the loop section. A ruling is written in this one place, and a dispatch brief cites it by entry title.
- Log material: a message in which the human states an idea, a hypothesis or an experiment definition is quoted in full as one entry. The convergence-check entry holds the confirmed restatement in full with the skeleton and is exempt from the three-line limit. The sub-agent that writes the log and the post-write check seats read these entries through the titles given in their brief. A log-material entry written after the convergence check (a design change, an added definition) is cited in those briefs by title next to the convergence-check entry. These entries hold only what the log will carry; they are not a transcript, and the pipeline keeps no separate input transcript file. When the loop is activated after the discussion, the entries are written at activation from the current context; for parts already compacted away, the restatement the human confirmed is the record.
- Failure (a route abandoned, an assumption refuted, a check not passed, a mistake of the assistant): one worklog entry.
- Not written: progress questions, reminders, routine permissions, watch heartbeats, and the PASS details of each check (a report is a file; the stage-change entry gives its path). A human message that is neither a ruling nor log material is not transcribed. Read the system clock immediately before writing a time; never correct it afterwards.
- The HANDOFF file is rewritten only when what is waiting on the human changes, or when minimum context that the other two files lack changes. Before a compaction the three files are not rewritten; only confirm that the loop section agrees with the latest stage-change entry.
- Precedence over the workspace's recording convention: inside an active loop topic the timing above governs. Writes for a completed deliverable unit are folded into the stage-change entry, and the three files are not rewritten as a whole before a compaction. Writes for a human ruling and for a failure are unchanged. When the work is handed to another agent or another node, all three files are still updated in full as that convention requires before a handoff.

## Log post-write check

The check is defined in `research-log-writing.md`, Step 6, and applies to every AI delivery of a research log whether or not a loop is active; this reference only cites it. In the loop it runs at the end of Log writing and of Backfill, with the seats `<log check seat>`, the fixed brief `assets/log-check/log-check-brief.md` and the clause map `<log check clauses>`. The main thread fills in only the braces of the brief (paths and entry titles) and passes on no standard of its own, since after a compaction it may no longer hold one. The source list, the seat reports and the fix list stay in the topic directory; check results are never written into the log. A reference seat still running when the stage exits holds neither the stage nor the bus review gate: note it on the Watch line of the loop section with its report path, and remove the note once its findings are applied and reported.

## Boundaries

- This reference orders work; it adds no rule on how a log, a decision, a task or a reference is written. Those rules stay in their own references and in the workspace contracts.
- No topic state file besides the three record files, the research log and the bus. No stage depends on auto-memory.
- Results are not interpreted and the next direction is not chosen for the human. Backfill writes tables, figures and what is needed to read them.
- Preconditions and Boundaries of `task-dispatch.md` apply unchanged. Activating the loop, approving a log, or a message without a named batch is not a dispatch authorization.
- Sub-agents write artifacts and reports. The main thread alone advances stages, records authorizations and edits the loop section.
- Where `<node contract>` exists, its start-of-work, end-of-work and write-vault routines come first, and a workspace write gate, where there is one, stays in force.

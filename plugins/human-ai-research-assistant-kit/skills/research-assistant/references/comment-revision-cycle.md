# Comment Revision Cycle

Turns a batch of reviewer feedback on a manuscript — advisor comments, peer
reviews, editor notes — into confirmed, executed, verified edits. Comment
**sources** vary endlessly (an Overleaf review panel, PDF annotations, a
plain-text email, verbal notes typed up); the **cycle** is invariant. This
file defines the cycle. Concrete source adapters live in the workspace, not
here (see "Adapters", below).

The organizing principle: **progress lives in one roadmap file, never in an
AI's head.** Any AI (Claude, Codex, DeepSeek) picking the roadmap up cold
reads the file-level `gate_state:` and the per-item `status:` fields to know
what it may touch. State is on disk; the conversation is not the record.
(Building or compiling to *verify* a fix also needs the toolchain — a
workspace fact resolved from `RESEARCH-CONTEXT.md` per discipline 3, not
carried in the roadmap. A cold agent can read what it may touch from the
roadmap alone; finishing the cycle also needs that toolchain.)

## The four-step cycle (actor ownership)

The kit's three parties own the steps. The AI assistant orchestrates; the
code agent executes; the human decides and gates.

```
[1] comment -> roadmap      AI ASSISTANT  normalize every comment into one
       |                                  roadmap; classify; pre-fill options;
       |                                  verify applied-explanation items
       v
[2] check roadmap  <==GATE   HUMAN         fill decision fields; answer
       |                                  questions; set status confirmed/
       |                                  wont-fix; flip gate_state -> ready
       v                                  when the whole pass is done
[3] roadmap -> fix           CODE AGENT    execute ONLY confirmed items, and
       |                     (or AI asst   only once gate_state is ready,
       |                      for small    via the task-dispatch interface
       |                      in-session   (see "Handoff", below)
       |                      edits)
       v
[4] review the fix           AI ASSISTANT  mechanical + semantic review
                             + HUMAN       then human final pass
```

### Step 1 — comment → roadmap (AI assistant)

Take the adapter's output (per comment: quoted text + anchor + author +
date) and write **one roadmap file** with one block per comment, using the
fixed field set below. Start the file at `gate_state: gating`. **Classify
every comment** into exactly one of the three categories.

- For each `actionable` item — and each `question` whose answer is an
  enumerable set of text changes — pre-fill `options:` with 2–3 concrete
  alternatives, one sentence each with its tradeoff, so the human chooses
  rather than composes. This is derivation, not decision-making: never put a
  chosen fix in `decision:` — that field is the human's.
- Verify every `applied-explanation` item against the current manuscript now
  (read-only, no edit): set it `done` if the reviewer's already-applied text
  is present, or `question` with a `note:` if it is absent.

### Step 2 — human checks the roadmap (human) ★ THE GATE

The human walks the roadmap top to bottom: answers every `question` (in
`answer:`), picks an option letter or writes free text into `decision:`, and
sets `status:` to `confirmed` (or `wont-fix`) per handled item. When the
whole pass is done, the human flips the file's `gate_state:` from `gating` to
`ready`. That flip, not any single item's status, is what opens execution.

> **GATE RULE (hard) — two levels:**
> 1. **File level.** An AI may execute edits only when the header's
>    `gate_state:` is `ready`. While it is `gating` the human is still
>    walking the roadmap; execute nothing, even items already marked
>    `confirmed` (the human may still revise them after considering later
>    items).
> 2. **Item level.** Once `gate_state: ready`, an AI may execute an item
>    ONLY IF its `decision:` is non-empty AND its `status:` is `confirmed`.
>    Every other item — empty decision, `awaiting-human`, `question`,
>    `blocked-build`, anything ambiguous — is UNTOUCHABLE.
>
> Verifying an `applied-explanation` item is read-only, produces no edit, and
> is **not** gated: the AI verifies it and sets it `done` or `question`
> itself, at any `gate_state`. When in doubt, do not act; leave it for the
> human.

### Step 3 — roadmap → fix (code agent, or AI assistant for small edits)

Only when `gate_state: ready`. Execute confirmed items only, in roadmap
order. Update each item's `status:` and `last-touched-by:` immediately as it
is handled (`in-progress` → `done`, or `wont-fix`, or `blocked-build` on a
build failure), so a crash or handoff loses no state. Apply the discipline
list below. Small in-session edits the assistant may do directly; a real
batch goes through the task-dispatch pipeline (see "Handoff").

### Step 4 — review the fix (AI assistant + human)

AI-side review has two lenses:

- **Mechanical.** Every `confirmed` item is now `done` (or explicitly
  `wont-fix`); no item is stuck `in-progress` or `blocked-build`; nothing
  outside confirmed items was touched; the manuscript builds/compiles clean.
- **Semantic.** Each edit is faithful to what `decision:` actually says —
  not a plausible-looking edit that drifts from the human's choice.

Then the human does the final pass. These lenses are the review-gate lenses
of `task-dispatch.md` (fabrication / scope / consistency) narrowed to fix
faithfulness — reuse that machinery, do not reinvent a review process here.

## Roadmap per-comment block spec

Source-neutral field names. Use these exact names. The file carries one
header (`source` / `manuscript` / `date` / `gate_state`) then one block per
comment.

```
### [<id>]
- anchor:      <file>:<line> | <section ref> | unanchored
- comment:     "<verbatim quoted comment text>"
- author:      <reviewer name or role>
- date:        <YYYY-MM-DD the comment was made>
- category:    applied-explanation | actionable | question
- options:     (AI-proposed; 2-3 alternatives, one sentence each + tradeoff;
                the literal string `verify-only` for applied-explanation)
    A) <option A> — <tradeoff>
    B) <option B> — <tradeoff>
    C) <option C> — <tradeoff>
- decision:    <EMPTY = NOT CONFIRMED. Human writes an option letter or free
                text. Free text is authoritative and supersedes the options.>
- answer:      <question items only: the human's informational answer. This
                is information, NEVER an edit instruction; do not execute it.>
- status:      awaiting-human | confirmed | in-progress | done | wont-fix
                | question | blocked-build
- note:        <optional short annotation: why parked at question, why
                verification failed, or the build error for blocked-build>
- last-touched-by: <human | AI-name>
```

**Status vocabulary** (fixed):

| status | meaning |
|---|---|
| `awaiting-human` | needs a human decision among the options; the default gate state for an `actionable` item |
| `confirmed` | `decision:` filled; an edit is pending; cleared to execute once `gate_state: ready` |
| `in-progress` | an AI is executing it right now, or a dispatch for it is live on the bus |
| `done` | edit executed and the build is green — or, for a `verify-only` item, the reviewer's already-applied text is confirmed present in the manuscript |
| `wont-fix` | human decided to take no action |
| `question` | blocked pending a human answer (a `question`-category comment starts here; an AI also parks any mid-execution ambiguity, or a failed applied-explanation verification, here rather than guessing) |
| `blocked-build` | the item's edit was applied but the build fails; needs the human before it can reach `done` |

`decision:` empty ALWAYS means NOT CONFIRMED. An `applied-explanation` item
never becomes `confirmed` — it is `verify-only` and goes straight to `done`
(verified) or `question` (verify failed), so its empty `decision:` never
conflicts with the gate rule. Only `actionable` items and `question` items
resolved in place can ever be `confirmed`.

## Classification rules (the three categories)

Every comment is exactly one of:

| category | meaning | action |
|---|---|---|
| `applied-explanation` | the reviewer explains a change they have **already applied** to the manuscript | `options: verify-only`; no edit. Verify against current text (the AI does this, not the human): if present → `status: done`; if absent (reviewer forgot to push, or the git and comment channels diverged) → `status: question` + a `note:` for the human to reconcile. Do NOT self-confirm an unverified claim. |
| `actionable` | an instruction to change something | pre-fill options; `status: awaiting-human` until the human decides |
| `question` | the reviewer asks the human a question | If the answer is an enumerable set of text changes, pre-fill `options:` and let the human resolve it in place like an `actionable` item (pick → `confirmed`). Otherwise `status: question`: the human fills `answer:`; the answer is information, never executed — if it implies an edit, re-run step 1 to derive a NEW `actionable` block, which then re-enters the gate. |

## Discipline

1. **Never revert an edit the reviewer already applied.** `applied-explanation`
   items are verify-only; any manuscript text the reviewer merged in is ground
   truth — do not undo it while fixing other comments, and do not undo it to
   fix a build.
2. **Touch nothing beyond confirmed roadmap items.** No drive-by edits, no
   reformatting of unrelated lines.
3. **Verify before declaring `done`.** For items that made an edit, the
   manuscript must build/compile with zero errors. The exact toolchain is a
   workspace fact (build command, engine); resolve it from
   `RESEARCH-CONTEXT.md` or the repo's own runbook, not from memory.
4. **Build failures halt the batch.** If a build fails after an edit, do not
   mark that item `done`. Set it `blocked-build` with the error in `note:`,
   leave every other item's applied edit untouched (do not revert other
   items to make the build green — that violates rule 2 and can undo rule 1),
   and escalate to the human. Compilation is global: a red build blocks the
   whole batch — no item reaches `done` until it is green again.
5. **One owner per in-flight item.** An item another agent marked
   `in-progress` or `blocked-build` is untouchable until it returns to a
   terminal (`done` / `wont-fix`) or `awaiting-human` state; only the agent
   named in `last-touched-by:` may transition it. `confirmed` alone never
   authorizes execution when a dispatch for that item is already live.
6. **Commits carry no AI co-author line.** No `Co-Authored-By` trailer. Commit
   only when the human asks.
7. **State on disk, updated immediately.** Set `status:` and
   `last-touched-by:` the moment an item changes; the file, not any AI's
   memory, is the record.

## Roadmap file location

One roadmap file per review batch. Do not use a fixed name; suggest
`revision-roadmap-<YYYY-MM-DD>.md`, or, on a delivery bus, under the date directory's
reference area: `progress/<YYYY-M-D>/reference/progress<N>/revision-roadmap.md`. Record the
chosen path in `RESEARCH-CONTEXT.md` (see "Adapters") so a cold handoff and
the dispatch `parent_authority_ref:` resolve it from disk, not from the
conversation.

## Handoff to task-dispatch (step 3 at scale)

A **confirmed roadmap is a code-agent-facing decision artifact**: it records
what the human decided, per item, with authority. Do not build a parallel
execution mechanism here — a real fix batch re-uses the existing pipeline:

1. Derive a Task per `task-writing.md`. The roadmap is the parent authority:
   `parent_authority_kind: decision`, `parent_authority_ref:` the roadmap
   path (see "Roadmap file location"). In-scope = the confirmed items;
   out-of-scope = everything else on the roadmap (this makes discipline
   rule 2 machine-checkable).
2. Run it through `task-dispatch.md` unchanged: review gate → delivery bus →
   dispatch → supervision → return.
3. **Two status layers, kept separate — but mark in-flight.** The dispatch
   runtime states (`received | accepted | in_progress | …`) live on the bus
   per `code-agent-execution.md`; do not copy them into the roadmap. But the
   moment you dispatch an item's batch (dispatch stage 4), set that item's
   roadmap `status:` to `in-progress` and `last-touched-by:` to yourself, so a
   cold agent opening the roadmap sees it is in flight and does not
   re-dispatch it. On return (dispatch stage 6), reflect the verified outcome
   back into each item's roadmap `status:` (`done` / `wont-fix` /
   `blocked-build`).

For a handful of small text edits the assistant can make in-session, skip the
dispatch machinery and edit directly — but the gate rule, the discipline
list, and the step-4 review still apply.

## Adapters (out of scope for the kit)

Step 1 consumes a uniform tuple per comment:

```
{ quoted comment text, anchor (file:line or section), author, date }
```

Any tool or process that yields that tuple can feed the cycle — an Overleaf
review-panel extractor, a PDF-annotation dumper, a script that parses an
email thread, or the human simply typing verbal notes into the tuple by
hand. A human-provided file already in this tuple form needs **no adapter**;
it feeds step 1 directly. The **adapter concept** is part of this cycle;
**concrete adapters are not part of the kit.** They are project-specific
(source formats, capture pitfalls, dual git-vs-comments channels) and live in
the user's workspace. This workspace's concrete adapters and its
roadmap-storage dir are recorded under the `## Comment-revision adapters &
roadmaps` H2 of `RESEARCH-CONTEXT.md`. Do not hardcode a specific adapter or
its paths into kit files.

## Worked example (compact)

Adapter tuple for two comments →

```
## Revision roadmap — 2026-07-20
source: advisor review, sec/method.tex
manuscript: <paper repo>@<commit>
date: 2026-07-20
gate_state: ready

### [1]
- anchor:      sec/method.tex:32
- comment:     "Is this parameter trained, or fixed at initialisation?"
- author:      advisor
- date:        2026-07-19
- category:    question
- options:
    A) State it is a learnable linear projection — matches code, strongest claim — needs code-fact confirmation.
    B) State it is a fixed random projection — safe if unsure — weaker novelty.
    C) Defer: leave a TODO and ask again — no text change yet.
- decision:    A (code confirms learnable; write "learnable linear projection")
- status:      confirmed
- last-touched-by: alice

### [2]
- anchor:      sec/intro.tex:8
- comment:     "reworded this sentence for clarity"
- author:      advisor
- date:        2026-07-19
- category:    applied-explanation
- options:     verify-only
- decision:
- status:      done
- last-touched-by: AI-claude
```

Item [1] is a `question` with an enumerable answer set, so options were
pre-filled; the human picked A → `confirmed` with a non-empty `decision` →
executable in step 3 (because `gate_state: ready`). Item [2] is
`applied-explanation`: the AI verified the reviewer's own merged edit is
present in the current text → `done`, empty `decision`, no edit, and it must
NOT be reverted (discipline rule 1). Had the reworded sentence been absent,
item [2] would be `question` with a `note:` instead, for the human to
reconcile.

Template to copy: `assets/revision-roadmap-template.md`.

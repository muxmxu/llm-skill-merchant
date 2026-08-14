---
name: magi
description: "<suit-for-ai-research-assistant> convene a MAGI decision council on a decision the human is facing — whether to run an experiment, adopt an approach, cut scope, spend a budget, submit to a venue, or abandon a line of work. Several mutually orthogonal lenses deliberate in parallel and blind on a shared bound-facts pack, every reason is audited back to its source and struck if it does not hold, a unanimous vote is red-teamed before it stands, and the result is reported as a ruling with a vote tally, the surviving reasons for and against, the cost of not acting, and each vote's flip condition. Trigger on 'should we do X', 'is X worth it', 'X or Y', and on an explicit ask for MAGI. Not a brainstorm and not a debate: open-ended thinking belongs in research discussion, and designing the how belongs in planning."
---

# MAGI — decision council

A decision, not a discussion. The input is one decidable proposition; the
output is a ruling with a vote tally, the reasons that survived audit, and
the conditions that would flip them.

What this is not:

- **Not brainstorming.** Generating options is research-discussion work. MAGI
  runs after the options exist.
- **Not design.** "How should we build X" is a planning question. MAGI
  answers "should we".
- **Not a debate.** The lenses never see each other in the first round. There
  is no rebuttal round; disagreement is resolved by audit and tally, not by
  argument.
- **Not an executor.** The council reports; the human rules. Convening the
  council is not permission to act on its ruling.

## Stage 0 — Frame the proposition

Tier-1 does this itself. Do not delegate it: everything downstream inherits
the framing, and a council convened on a badly framed proposition produces a
confident answer to the wrong question.

**0.1 Reduce to one decidable proposition.** Binary (do / do not) or at most
four mutually exclusive options. State the default explicitly: what happens
if the ruling is "no". Write it as a single sentence.

**0.2 Refuse if it is not decidable.** Say what is missing, ask the one
question that would fix it, and stop. Refuse when:

- the question is a "how", not a "whether" — that is planning work;
- neither side has any checkable evidence, so every vote would be intuition;
- the human has already decided and is asking for validation. Say so instead
  of manufacturing a tally that agrees with them.

Refusing costs one sentence. Convening on a bad proposition costs a full run
and produces an answer that looks authoritative.

**0.3 Assemble the bound-facts pack.** The same discipline the orchestration
mode applies before any consequential dispatch: enumerate every fact whose
mistake would change the ruling, and for each one either pin a precise value
or name exactly where to get it. Cover at minimum:

- the state of what is being decided about — which run, checkpoint,
  manuscript, dataset, deadline;
- where the existing evidence lives — log paths, code paths, papers, the
  numbers from the last attempt;
- hard constraints — compute, person-hours, budget, external dependencies,
  dates that cannot move;
- **the cost of being wrong in each direction** — acting when it was not
  worth it, and not acting when it was.

An item that is neither pinned nor sourced **blocks the council**. Gather it
first. A lens that has to improvise a fact will improvise it differently from
the other lenses, and the vote then measures the improvisation.

**This pack is the single shared input.** Every seat receives all of it and
nothing that the others did not get. A seat with private context is not an
independent vote.

## Stage 1 — Seat the council

Default three seats. The human's choice of lenses overrides; the human may
also ask for more or fewer seats — three is the default, not a ceiling.

**Seats must be mutually orthogonal.** Two seats that the same piece of
evidence would persuade at the same time are one seat; merge them and pick a
different second lens. Orthogonality is what makes a tally mean anything —
three seats that share a failure mode produce 3:0 on a shared error.

Default triad when nothing better suggests itself. The seats are defined by
what they ask; the MAGI names are labels on top of that:

- **MELCHIOR — evidence and method.** Does the evidence this decision rests
  on actually bear the weight? Would the proposed work answer the question it
  claims to answer? Confounds, internal validity, what the design cannot
  distinguish.
- **BALTHASAR — cost and survival.** Compute, person-hours, deadlines worked
  backwards. What else does this displace? How reversible is it? What does
  not doing it cost?
- **CASPER — outside evaluation.** How a reviewer, an advisor, or a reader
  receives it. Is it a question that must be answered, or one nobody asked?
  Where will it be attacked?

When the topic calls for different lenses, name the replacements by what they
ask rather than forcing them into the three names. Candidates and the test
for orthogonality: `references/lens-library.md`.

## Stage 2 — Independent deliberation

One agent per seat, in parallel, **blind**: no seat sees another seat's
output. This is the same first-round independence the multi-agent discussion
protocol enforces, and for the same reason — the first framing to arrive
otherwise sets everyone's frame.

Each seat receives: the proposition and its default, the complete bound-facts
pack, its own mandate, and the output schema. Each returns:

```jsonc
{
  "stance": "for" | "against" | "abstain",
  "confidence": "low" | "medium" | "high",
  "reasons": [
    {
      "claim": "one sentence",
      "label": "observation" | "data" | "claim-from-source" | "hypothesis",
      "source": "a checkable pointer: file path + line, log name, commit, the
                 number's origin, the paper and where in it",
      "weight": "decisive" | "supporting" | "minor"
    }
  ],
  "cost_of_not_doing": "what this seat sees going wrong if the ruling is no",
  "flip_condition": "what would have to be true for this seat to change its vote",
  "cheapest_probe": "the smallest check that would resolve this seat's uncertainty"
}
```

Discipline given to every seat:

- **A reason without a checkable `source` does not count.** A seat that
  cannot produce one for anything must return `abstain` and say which
  evidence is missing. Abstaining on absent evidence is a correct outcome;
  voting on a feeling is not.
- Do not report a hypothesis under an observation label. The audit will
  catch it and strike the seat's vote with it.
- Stay inside the mandate. A seat that argues another seat's case has
  collapsed the orthogonality the tally depends on.
- `cost_of_not_doing` is mandatory even for a seat voting against. Without
  it, councils drift systematically toward "do it", because the costs of
  acting are concrete and the costs of not acting are not.

## Stage 3 — Audit every reason

Per reason, not per seat. The auditor must not be the seat that produced the
reason, and must not run on tier-1's own model.

Each reason is checked back to its source and returned as one of:

- **upheld** — the source exists and supports the claim as stated;
- **downgraded** — the source exists but supports only a weaker statement
  (an observation that is really a hypothesis, a number that is close but not
  the one quoted). Relabel, keep, reduce weight;
- **struck** — the source does not exist, does not say that, or the numbers
  do not match; **or the reason is true but does not bear on this
  proposition**. Irrelevance is struck, not downgraded.

Then, across seats: a reason two seats raised counts once, credited to
whichever raised it first.

**Seat invalidation.** If all of a seat's reasons are struck, or what
survives no longer supports the stance it took, that seat becomes
`abstain (grounds did not hold)` and its vote is not counted.

Struck reasons do not appear in the ruling's arguments, but they **stay
visible in the report** — who raised them and why they failed. That record is
what stops the same unsupported argument from returning next month.

## Stage 4 — Red team a unanimous vote

If, after the audit, every valid vote points the same way — including the
case where only one valid vote remains — a red-team agent is mandatory. Its
only job is to break the consensus: find counter-evidence, find a fact the
bound-facts pack omitted, find the single wrong premise all the seats
inherited from the pack. Its output goes through Stage 3 like any other.

- Red team produces counter-evidence that survives audit → the ruling drops
  to **hold**, with that evidence stated.
- Red team fails → the consensus stands, and the report says it was
  red-teamed.

**A unanimous vote that has not been red-teamed does not produce a ruling.**
Agreement between models reading one shared context is weak evidence about
the world and strong evidence about the context.

## Stage 5 — Tally and report

Tier-1 does this itself.

- Majority, red-teamed where required → **carried** or **rejected**.
- Tie, fewer than two valid votes, or all seats abstaining → **hold**. Say
  what is missing to decide, and give the cheapest route to it, drawn from
  the seats' `cheapest_probe` fields. A hold with a probe attached is a
  useful outcome; a forced ruling on thin evidence is not.
- **The tally is not the ruling.** The human decides. Report the council's
  finding and stop; do not begin executing it.

Report in the conversation language, in this shape:

```markdown
# MAGI ruling: <proposition>
Verdict: carried / rejected / hold  (for N : against M, abstain K)
Red team: passed / not triggered / broke the consensus
Date: YYYY-MM-DD

## Proposition and default path
## Bound facts (the one input every seat received)
## Reasons for (survived audit)
1. [label] claim — source, seat
## Reasons against (survived audit)
1. [label] claim — source, seat
## Cost of not acting
## Flip conditions
## Cheapest way to resolve what is still open
## Audit record (struck and downgraded reasons)
## Ruling
The decision belongs to the human. <name>'s ruling: <left blank until given>
```

**Persistence.** Write the report to the current task directory as
`magi-<slug>.md` (directory convention: the `agent-workspace` skill), and
append one entry to that directory's `worklog.md` carrying the tally and the
human's ruling — left blank until they give it. Skip the file only if the
human said not to write one.

## Execution

One Workflow run: `pipeline` the seats through deliberation and per-reason
audit so each seat's reasons are audited as soon as that seat returns; then
tier-1 checks unanimity and dispatches the red team only if needed; then
tier-1 tallies. Use the schema option on `agent()` so seat and audit output
is validated rather than parsed.

A Workflow is not interruptible once launched, which is acceptable here
precisely because Stage 0 closes the bound facts before anything is
dispatched. If Stage 0 could not close them, the council does not run yet —
that is the same gate, not an exception to it.

Resolve model and effort per role from the workspace's `ORCHESTRATION.md`,
and pass both explicitly on every `agent()` call. Seats, auditors, and the
red team must not run on tier-1's own model. Stage 0 and Stage 5 stay with
tier-1 and are never delegated.

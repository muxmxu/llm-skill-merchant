# Revision roadmap — <YYYY-MM-DD>

<!--
Comment Revision Cycle roadmap. One block per comment. Progress lives in this
file, never in an AI's head: any AI picking this up cold reads gate_state: and
the per-item status: fields and touches ONLY items that pass the gate.

GATE RULE (hard), two levels:
  1. File level: an AI may execute edits only when gate_state: is `ready`.
     While it is `gating` the human is still walking the roadmap — execute
     nothing, even items already marked confirmed.
  2. Item level: once gate_state: ready, an AI may execute an item ONLY IF
     its decision: is non-empty AND its status: is confirmed. Everything else
     is untouchable. Verifying an applied-explanation item is read-only and
     not gated.

Protocol: references/comment-revision-cycle.md
-->

source:      <where comments came from — e.g. advisor review panel, PDF annotations, email>
manuscript:  <paper repo path>@<commit hash>
date:        <YYYY-MM-DD>
gate_state:  gating | ready   <!-- start at `gating`; the human flips to `ready` when the whole pass is done -->

status legend:
  awaiting-human — needs a human decision among the options (default gate state for actionable)
  confirmed      — decision filled; edit pending; cleared to execute once gate_state: ready
  in-progress    — an AI is executing it now, or a dispatch for it is live
  done           — edit executed and build green; or a verify-only item confirmed present
  wont-fix       — human decided to take no action
  question       — blocked pending a human answer, or a parked ambiguity / failed verification
  blocked-build  — edit applied but the build fails; needs the human before it can reach done

category legend:
  applied-explanation — reviewer explains a change already applied; verify-only, no edit
  actionable          — an instruction to change something; needs a decision
  question            — reviewer asks the human a question

---

### [1]
- anchor:      <file>:<line> | <section ref> | unanchored
- comment:     "<verbatim quoted comment text>"
- author:      <reviewer name or role>
- date:        <YYYY-MM-DD>
- category:    applied-explanation | actionable | question
- options:     <2-3 alternatives below; or the literal `verify-only` for applied-explanation>
    A) <option A> — <tradeoff>
    B) <option B> — <tradeoff>
    C) <option C> — <tradeoff>
- decision:    <EMPTY = NOT CONFIRMED. Human writes an option letter or free text; free text supersedes the options.>
- answer:      <question items only: the human's informational answer; NEVER executed as an edit instruction>
- status:      awaiting-human
- note:        <optional: why parked at question / why verification failed / the build error>
- last-touched-by: <human | AI-name>

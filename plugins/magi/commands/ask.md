---
description: Convene the MAGI council on a decision and report the ruling with its vote tally
argument-hint: [the decision, e.g. "should we rerun the MOS experiment before the deadline"]
---

Read `${CLAUDE_PLUGIN_ROOT}/skills/magi/SKILL.md` and follow it.

Decision: $ARGUMENTS

1. If the input is empty, ask what is being decided. Do not convene a council
   on a guess.
2. Run Stage 0 yourself: reduce the input to one decidable proposition with a
   stated default, and assemble the bound-facts pack. If the proposition is
   not decidable — it is a "how", not a "whether", or no checkable evidence
   exists on either side — say so, ask the one question that would fix it,
   and stop. Do not convene.
3. Run Stages 1–4 as described in the skill: seat the lenses, deliberate in
   parallel and blind, audit every reason back to source, red-team a
   unanimous vote.
4. Tally and report yourself, in the conversation language, using the skill's
   report format. Write the same report to the current task directory and
   append the tally to its worklog, unless the user asked for no file.

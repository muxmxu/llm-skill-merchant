# Research Decision Writing

## Purpose

Write a structured progress or decision note for a code agent. This mode packages human research thinking and decisions into implementation-relevant context.

This is not the human's creative research log. The creative, messy, speculative part belongs in Research Log Writing. Decision writing is structured and code-agent-facing.

## Trigger Examples

Use this mode when the user says or implies:

- write progress
- write decision
- record this decision
- package this for the code agent
- update progress with this result
- document this research choice for implementation

## Inputs

Useful inputs:

- summary of current progress,
- one or more decisions,
- problem or observation that forced the decision,
- reasoning chain,
- rejected alternatives,
- implementation consequence,
- relevant references, files, runs, plots, papers, or code findings,
- status.

If the decision itself, core problem, or reasoning is missing, ask for the missing fields. Otherwise, write with explicit assumptions.

## Output Language

Write the decision artifact in English by default, because the target reader is a code agent. Preserve technical terms from the user's notes when needed.

## Output Format

Output exactly one markdown code block containing the decision/progress content. After the block, output a suggested filename or path.

Do not assume the filename must be `progress.md`. Use a suggested path such as:

`Filename: progress/YYYY-MM-DD_<snake_case_title>.md`

If the user's repository convention uses a single progress page, suggest the page path the user provided or a single markdown filename.

## Template

```markdown
# Progress: <Title>
Date: YYYY-MM-DD
Author: human
Status: active
Audience: code_agent

## Summary
<1-3 sentences describing what changed, what was learned, and why this entry matters.>

## Decisions

### Decision: <short title>

#### Problem / Observation
<The concrete problem, experimental observation, or design pressure that forced the decision.>

#### Decision
<The human-approved decision. State it as an implementation-relevant constraint or direction.>

#### Reasoning
1. <Evidence or premise.>
2. <Inference.>
3. <Implementation implication.>

#### Code-Agent Impact
- <What the code agent should preserve, change, inspect, or avoid.>

#### Rejected Alternatives
| Alternative | Reason Rejected / Deferred |
|---|---|
| <alternative> | <reason> |

#### References
- `<path-or-source>` — <why relevant>

## Open Questions
- <question or unresolved risk>
```

## Rules

1. A single decision artifact may contain multiple `### Decision:` blocks.
2. Omit optional sections only when they are genuinely absent and not necessary for code-agent action.
3. Do not invent code impact. If implementation impact is uncertain, write `Implementation impact: uncertain; requires code inspection.`
4. Keep the artifact structured. The code agent should not need to parse conversational Q&A.
5. Prefer explicit consequences over broad conclusions.
6. If the decision supersedes an earlier decision, add `Supersedes: <path-or-title>` near the top when known.
7. If evidence comes from the human but has no file/source, mark it as `Human-provided observation`.

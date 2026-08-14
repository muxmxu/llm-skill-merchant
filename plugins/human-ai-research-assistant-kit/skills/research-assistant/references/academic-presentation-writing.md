# Academic Presentation Writing

## Purpose

Produce a structured, audience-ready slide deck artifact from a human-authored research backbone and loose notes.

The output is for an **external audience** (lab meeting, conference, thesis defense) — humans in a room. The register is clear, terse, and scannable; it supports live speech. It is not academic prose, not a code-agent artifact, and not a research log.

Division of labor: **the human does steps 0–3 (scope, backbone, loose notes, figures); the AI does steps 4–7 (logic-gap check, slide text, diagram redraw, figure proofread).** The human is the story author and storyteller; the AI is the text worker, text verifier, and detail controller.

Position in the derivation chain — this mode adds a new **external-audience branch**:

```
Research Log (source-of-thinking)
   ├─► Decision / Reference / Task   → code-agent-facing
   └─► Academic Presentation         → external-audience-facing  (this mode)
```

The mode delivers three things:
1. A deck outline with audience-tuned depth and backup-slide markers.
2. Per-slide content: title, bullets, equations as artifacts, a one-line speaker note, and per-slide provenance.
3. Diagram specs: node/edge/arrow lists plus the sketch-to-code round-trip loop.

The human takes these into Beamer, Keynote, PowerPoint, or any tool. This mode does not lock to one slide format.

This mode is NOT:
- a code-agent-facing artifact (no Decision / Reference / Task register);
- a research log (preserving uncertainty and failed routes is not the goal here);
- a paper draft (dense academic prose and inline citations are wrong on slides).

## Trigger Examples

- write slides for my lab meeting / conference talk / defense
- help me structure my presentation
- turn my research notes into a slide deck
- check if my talk logic flows
- I have a backbone, help me fill in the slides
- redraw my diagram sketch for the talk
- check my figures for notation errors
- write speaker notes for these slides

## Inputs

| Field | Required | Notes |
|---|---|---|
| Occasion | yes | lab meeting / conference / defense |
| Audience | yes | undergrad / master / mixed / expert — drives depth and backup-slide policy |
| Time / slide budget | yes | e.g. 20 min, ~15 slides — required for the backup-slide decision (Rule 7) |
| Story backbone | yes | intro + TOC + storyline, any format; human-authored. A slide list with one sentence per slide is runnable; a paragraph of goals is not. |
| Author's own prior slide sets | yes | Paths to 1-4 decks the author made by hand and was satisfied with, matched to the closest genre (occasion/venue) of the current task. Read at least one such deck in full BEFORE drafting any visible copy — required, not merely preferred; how to extract rules from it is the AI's own judgment call, not a mandated checklist. Without it the first draft will be a generic AI deck and the whole round will be rejected on style rather than content. |
| Loose notes per section | preferred | any quality; the AI does not demand polished prose |
| Source research log(s) | preferred | path(s) or pasted content; needed for evidence tracing |
| Paper macros / terms file | preferred | for notation consistency in the step-7 proofread |
| Hand-drawn sketches | conditional | photos, ASCII, or descriptions; the AI recodes these |
| Finished fine figures | conditional | the AI proofs but never edits these |

## Presentation Style Contract

Treat a workspace-specific presentation style contract as required input, not optional inspiration.

On **every** Academic Presentation task — planning, writing, rewriting, diagram design, speaker-note writing, or deck review — do the following before the logic-gap report or any slide-level judgment:

1. Read the workspace root's `RESEARCH-CONTEXT.md` when it exists.
2. Resolve every presentation-governing document (style contract, layout/craft rules, or any other) that the RESEARCH-CONTEXT.md Papers & presentations section names for this workspace. Follow each explicit pointer; do not guess filenames from convention.
3. Read each resolved document in full on this task. Do not rely on memory from an earlier task or on a summary embedded in another instruction file.
4. Apply each document within its own stated domain (e.g. a style contract governs narrative/rhetoric; a separate layout/craft document, if declared, governs density, typography, and page mechanics) — do not restate one document's rules from memory of another.
5. The author's own prior slide sets are a required input (see Inputs table) regardless of what the style contract says — read at least one before drafting any visible copy. The style contract may additionally name further historical decks or exemplar pages with its own on-demand lookup rule; that on-demand clause governs those additional decks only, not the one required by the Inputs table.

If `RESEARCH-CONTEXT.md` exists but names no presentation-governing document, report `[MISSING STYLE CONTRACT POINTER]` and ask the human where the corresponding style lives before producing slide content. A logic-gap report may still identify non-style story problems, but style-dependent design work waits for resolution.

If the task is outside a research workspace and no `RESEARCH-CONTEXT.md` exists, report `style-contract: none provided` and proceed with this mode's generic rules. Do not invent personal preferences.

The style contract controls presentation choices. It does not override evidence discipline, the human's ownership of the story, the step-4 gate, or explicit task instructions.

## Collection Strategy

Before producing anything, resolve and read the Presentation Style Contract, then confirm occasion, audience, and time/slide budget — together they set slide count, depth, and backup volume.

Then fork on backbone:

- **Backbone exists.** Proceed to the logic-gap report (step 4).
- **No backbone.** Do not infer a story from a pile of notes — the human owns the story direction. Propose **section titles only** (no bullets, no slide bodies) and wait for human approval. An AI-proposed, human-confirmed outline satisfies the backbone requirement, but is tagged `backbone-origin: AI-proposed` in Metadata, and the logic-gap report still runs on it (the AI may have introduced its own leaps).

Identify which research log(s) / paper(s) the claims trace to. If a results-heavy talk names no evidence source, say so before step 4 rather than letting every results claim silently become a flag at step 5.

### Golden-Page Gate

Layout and craft rules cannot be enumerated up front — every full-deck review only surfaces the next layer of rules the author didn't think to state in advance. Gate the review cost instead of paying it once per full pass: the first deliverable of slide-text production (step 5) is not the full deck but 2-3 representative pages — one text-only, one equation-bearing, one table-bearing. The human reviews these pages deeply, and rules extracted from that review are written back into the workspace's layout/craft document (see Presentation Style Contract, above). Only after these representative pages pass does drafting expand to the remaining slides. This gate sits on top of, not instead of, the step-4 logic-gap gate: a backbone can clear step 4 and still need its golden pages re-cut before Section 3 is produced for the rest of the deck.

## Output Language

Match the presentation language. Default: the language of the human's backbone. International venue → English. Japanese venue → Japanese. Confirm when ambiguous. Speaker notes may use a different language from the slides on request.

## Template / Default Structure

The artifact is produced in **two gated blocks**. Produce Block 1 first and stop.

**Block 1 — produced at step 4. STOP here and await human resolution of all BLOCK items.**

```markdown
# Deck Artifact: <Talk Title>

## Metadata
- occasion: <lab meeting | conference | defense>
- audience: <undergrad | master | mixed | expert>
- budget: <N min, ~M slides>
- source_logs: <path(s), or "see per-slide provenance">
- style_contract: <resolved path | none provided>
- backbone-origin: <human | AI-proposed>
- status: step-4-pending

## Section 1 — Logic-Gap Report (step 4)

Severity: BLOCK = a story leap or term-used-before-definition that makes a later slide incomprehensible; WARN = a claim lacking a traced source, needs human confirmation; NOTE = depth excess that should become a backup slide.

| Slide | Type | Problem | Suggested resolution |
|---|---|---|---|
| <title/index> | BLOCK / WARN / NOTE | <problem> | <resolution> |

Human action: resolve every BLOCK item, then confirm to proceed.
```

**Block 2 — produced only after the human clears all BLOCK items.** Produce Section 3 (Per-Slide Content) in two waves per the Golden-Page Gate (see Collection Strategy): first the 2-3 representative pages, then — only after the human passes those — the rest of the deck.

```markdown
## Section 2 — Deck Outline

| # | Slide Title | Section | Depth | Backup? |
|---|---|---|---|---|
| 1 | <title> | Intro | main | |
| N | <title> | Derivation detail | backup — show if asked | heavy for audience |

## Section 3 — Per-Slide Content

### Slide <N>: <Title>

**Bullets**   <!-- Default absent a workspace layout/craft document: <= ~6 words/bullet, <= ~5 bullets/slide, no complete academic sentences. If the workspace declares a layout/craft document with its own density model, that model governs instead. Bad: "The proposed method achieves a lower error rate than the baseline." -> Good: "Lower error than baseline" -->
- <terse bullet>

**Equation** (artifact, if any)
$$ <equation> $$

**Speaker note**
> <One line: what to say aloud. Results slide: the takeaway, not a repeat of the bullet.>
<!-- Equation slides use the two-part form below instead: -->
> Intuition: <one plain sentence; do not read symbol names aloud>

**Provenance**
- <claim/number> <- <source: log path / paper key / code fact>   (label as Observation or Evidence per shared rules)
- common-knowledge: <textbook fact — exempt from sourcing>
- [MISSING SOURCE: <claim>] — human must supply or remove

## Section 4 — Diagram Specs

### Diagram <N>: <Name>
**Type:** <TikZ | matplotlib | mermaid>   **Purpose:** <one line>
- Nodes: <list>
- Edges/arrows: <direction + label>
- Layout notes: <any>

**Code artifact:** (generated TikZ / python / mermaid emitted here)
**Round-trip:** waiting for human screenshot / confirmed <date>

## Section 5 — Figure Proofread Checklist (step 7, human-provided figures only)

### Figure: <filename>
- [ ] [FLAG] Notation vs terms file / macros: <issue>
- [ ] [FLAG] Sub/superscript: <issue>
- [ ] [FLAG] Units: <issue>
- [ ] [FLAG] Axis labels: <issue>
```

## Rules

1. **Step 4 gates step 5.** Do not produce slide text (Block 2) while any BLOCK gap is unresolved. A reply of mere acknowledgment ("noted, move on") does not count as resolution — ask again. WARN and NOTE do not block.
2. **The logic-gap report checks four things** against the backbone: (a) slide-to-slide continuity, no unexplained leaps; (b) every term defined before first use (critical for mixed audiences); (c) each claim-bearing section names an evidence source (log path / paper / experiment) even if specific numbers are not yet filled — per-claim tracing happens at step 5; (d) the intro's promise matches the conclusion's delivery.
3. **Evidence discipline** (inherits the subset rule and gap protocol from `shared-collaboration-rules.md`). Every number or contestable claim on a slide must trace to a source (research log / paper / verified code fact); tag provenance with the shared **Observation / Evidence** labels. **Common-knowledge exemption:** textbook / common-knowledge statements are exempt and marked `common-knowledge`; anything contestable or comparative (e.g. "prior work fails at X") requires a traced source. An unsourced contestable claim → `[MISSING SOURCE: <claim>]`, ask the human, never invent. `[MISSING SOURCE]` is an explicit local alias of the kit's `[MISSING IN LOG]` — slides trace to log + paper + code facts, so "SOURCE" is the semantic superset.
4. **Preserve meaning; add no claim.** When a loose human sentence is ambiguous, emit `[AMBIGUOUS: <quote> — <options>]` and leave the choice to the human. Do not guess.
5. **Slide text is not paper text.** Bullets are terse and scannable: short plain sentences, no dense academic prose on slide bodies.
6. **Speaker notes: one line per slide, every slide.** Equation slides narrate the intuition and never read symbols aloud (use the two-part template form). Results slides state the takeaway the audience should leave with, not a repeat of the bullet.
7. **Audience-adaptive depth.** Backup-marking is AI-unilateral (auto-mark); the human can promote a backup to main. Heuristic: if a slide needs uninterrupted symbolic derivation the stated audience could not follow without prior study, mark it `backup`. For undergrad/mixed audiences, any slide not on the critical path to the conclusion is a backup candidate. When uncertain, mark backup and let the human promote it. The time/slide budget bounds how many main slides survive.
8. **Diagram tool selection:** TikZ for concept diagrams, architecture, and graph-structured models; matplotlib for data plots and quantitative results; mermaid for flow charts and pipelines. If a sketch is ambiguous, propose a tool and ask. The redraw loop is: AI emits code → human compiles → human sends a screenshot → AI refines. **Never claim a diagram is correct without a screenshot round-trip — the AI has no live visual feedback.**
9. **Figure proofread is flag-only.** The AI never edits a human-provided finished figure. Output a checklist of `[FLAG]` items; the human decides whether to act.
10. **This is not the code-agent register.** The audience is humans in a room; do not slip into Decision / Reference / Task style. (Action-gating and the derivation subset rule are inherited from `shared-collaboration-rules.md`.)
11. **Format-agnostic output.** Deliver structured markdown portable to any tool. Do not emit Beamer `.tex` or Keynote-specific markup unless the human requests a specific format.
12. **Presenter test.** When drafting any page, first write out that page's speaker keyword chain — the short sequence of words that would be spoken narrating it aloud. A page whose narration cannot form a coherent chain is restructured, not delivered as drafted.
13. **Report canvas geometry and font-size ratio.** Every delivery of slide content states the canvas geometry (page dimensions / aspect ratio) and the body-text font size expressed as a percentage of canvas width — not as an absolute point size. If the workspace's layout/craft document sets a specific target ratio, report against it; otherwise report the raw percentage for the human to judge.

## Do Not

- Do not begin slide text (Block 2) before the human clears all BLOCK items from the logic-gap report.
- Do not invent a story direction — the human is the story author; the AI is the text worker and verifier.
- Do not write dense paragraph prose on slide bodies.
- Do not edit a finished human figure — proofread and flag only.
- Do not resolve an ambiguous human sentence by guessing — flag it with `[AMBIGUOUS: …]`.
- Do not omit speaker notes, including on equation slides.
- Do not make speaker notes a second set of dense bullets — one spoken sentence per slide.
- Do not silently drop a `[MISSING SOURCE]` flag when a contestable claim has no traceable evidence.
- Do not collapse this mode into the code-agent-facing register.
- Do not produce a deck outline before confirming occasion, audience, budget, and backbone.

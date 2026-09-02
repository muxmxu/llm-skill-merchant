# Speaker Deck Writing

Downstream stage of **Academic Presentation Writing**: once the slides are final, produce the speaker's stage card. This reference calls it the *speaker deck* (or simply *deck*); the parent mode's older wording — "Deck Artifact", "deck outline" — refers to the slide set, not to this card. The deck is what the presenter holds while talking. Its reader is the presenter alone, at the lectern, glancing down for the next cue.

What the deck is **not**:

- Not the per-slide *speaker note* of `academic-presentation-writing.md` (Rule 6, Rule 12). Those are design-time artifacts: they prove, while drafting, that a page can be narrated. The deck is the stage-time artifact, written after the pages are fixed.
- Not a rehearsal script, a transcript, or a timed run sheet.
- Not a restatement of the slide text. The audience reads the slide; the presenter needs what the slide does not say.
- Not a code-agent artifact and not a research log.

## Position in the chain

```
Academic Presentation (steps 4–7: gap report, slide text, diagrams, proofread)
   └─► slides final, page numbering frozen
          └─► Speaker Deck (this stage)  → presenter-facing → source-of-cue
                 └─► toolchain: deck → pdfpc notes / Keynote presenter notes
```

The deck is indexed by **PDF physical page**. It can only be written for a slide set whose page order is frozen; a deck written against a draft becomes misaligned the moment a page is inserted.

## Trigger examples

- write my deck / handcard / speaker card for these slides
- turn the finished slides into pdfpc notes
- I wrote pages 1, 2 and 16 of the deck myself, do the rest in the same style
- the slides are done, now the talk is in Japanese and I need cues

## Inputs

| Field | Required | Notes |
|---|---|---|
| Final slide PDF (or its page list) | yes | Physical page count fixes the number of deck sections. |
| Story backbone / per-page narrative job | yes | From the presentation stage. The deck cues the story; it does not invent one. |
| Speech language | yes | The language spoken on stage may differ from the slide language. |
| Workspace deck contract | yes | See below. It fixes the cue notation, what may and may not appear, and the file format. |
| Pages the author has already written | strongly preferred | Authors typically write the opening, the outline and the closing themselves. These pages are the style exemplar for the rest; read every one of them before writing any page. |
| Evidence sources for spoken claims | preferred | Research log, paper, code facts. Spoken claims obey the same evidence discipline as slide claims. |
| Presenter-test keyword chains from step 5 | optional | If produced during slide drafting, they seed the cue chain; they are not pasted as-is. |

## The deck contract (doc contract)

Cue notation, forbidden fields, what gets written in full, language split, and the file format are author-specific. They live in a workspace contract doc:

```
merchant_skill_contract/HUMAN-AI-RA-CONTRACT/DECK_STYLE.md
```

Resolve it per SKILL.md § Doc Resolution (RESEARCH-CONTEXT.md pointer first, then the contract directory, then the workspace root as legacy fallback). Read the whole document on every deck task before writing a single cue; a summary remembered from an earlier task does not count. The contract is human-owned: propose amendments, never edit it unilaterally.

Contract missing → report `[MISSING DECK CONTRACT]` and ask the author how they read a card on stage before producing anything. Do not fall back to the generic speaker-note format of the presentation stage; that format was rejected by at least one author precisely because it is a script, not a card.

## Procedure

1. **Confirm inputs**: final PDF, backbone, speech language, contract read in full, author-written pages read in full.
2. **Page map**: one deck section per PDF physical page, in order. State the physical/displayed page offset if the slide tool hides a page number (beamer `noframenumbering`). Never renumber to match the on-screen counter.
3. **Sample pages first**: deliver two or three pages spanning the page types present (a story page, a figure page, a results page). The author reviews; their corrections are written back into the workspace contract as amendments proposed to the author. Only then write the remaining pages. This mirrors the golden-page gate of the presentation stage and exists for the same reason: card conventions surface only when the author reads a real page.
4. **Write each page under the contract**: cue chain first, content only where the author would not know what to say, full text only where the contract says text must be read verbatim.
5. **Mechanical checks** before delivery: section count equals page count; forbidden fields zero-hit (the contract lists them); every page heading present even when the body is intentionally empty; the workspace toolchain's alignment check passes (in this kit's reference setup, `smlpdtp --check`).
6. **Author pass**: the author reads the whole deck. Pages the author wrote are never rewritten; a proposed change to one is a suggestion in conversation, not an edit.

## Rules

1. **The presenter owns the words.** The deck gives sentence shape and cue; it does not put sentences in the presenter's mouth. When the contract defines a cue notation (a functional directive such as "propose method for problem"), the cue encodes the *shape* of the sentence and its hook, not the topic.
2. **Nothing the author already knows.** Common openers, the author's own constants, the argument they built themselves: leave them out. A cue that the author would never need to glance at is noise on the card.
3. **Full text only where the contract requires verbatim reading** (typically: a title in a language the author cannot recite, exact citations, exact numbers). Long verbatim text is broken into breath-length lines.
4. **Evidence discipline applies to spoken claims.** A mechanism not verified in log, paper or code is cued in weak form, never as a causal statement. Inherits `shared-collaboration-rules.md`.
5. **What leaves the screen lands on the card.** A citation or qualifying clause removed from a slide under the layout rules must appear in that page's deck section, marked as spoken.
6. **No Q&A material unless asked.** Prepared answers to anticipated questions enter the deck only on the author's explicit request.
7. **Empty pages are legitimate.** When the author says they will improvise a page, its section stays with an empty body. The heading stays: the toolchain maps by section.
8. **Format is an interface.** The section heading scheme and separator are consumed by scripts (`smlpdtp`, `smlptk`). Do not restyle headings, renumber, merge or split sections for readability.
9. **Oral scope is not paper scope.** Whether something may be *said* is judged against what the model or implementation supports, as stated in the workspace contract, not against whether the paper text contains the sentence. On-screen claims stay under the presentation stage's evidence rules.
10. **Author-written pages are the exemplar and are untouched.**

## Output

- The deck file itself, in the slide project at the path the workspace convention names (in this kit's reference setup: `slides/<talk>/script/deck-<lang>.md`).
- A short check report in conversation: sections vs pages, intentionally empty pages, forbidden-field scan result, which author pages were read.
- No timing table, no word counts, no per-page duration, unless the contract asks for them.

## Do Not

- Do not write the deck before the slide page order is frozen.
- Do not produce a script and call it a deck.
- Do not paraphrase the on-slide text into the card.
- Do not force the cue notation onto every line; the author's own pages show where cues are and are not used.
- Do not add Q&A answers, timing, word counts, "next page" bridges as separate fields, or overtime plans.
- Do not rewrite a page the author wrote.
- Do not change the section heading format.

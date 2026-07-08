# RESEARCH-CONTEXT.md contract (research-context v1)

The research-assistant kit is workspace-portable: the skill carries
methodology only; the facts of a particular research workspace live in a
single doc the skill reads. That doc is `RESEARCH-CONTEXT.md` at the
research-workspace root.

Marker: first line of the doc is `<!-- runbook-contract: research-context v1 -->`.

## What the doc is (and is not)

- An **AI-agnostic resource map**: static, human-approved facts about where
  this workspace's research materials live and how to access them. Every AI
  working in the workspace (any vendor, any harness) reads the same file;
  per-AI instruction files (CLAUDE.md, DEEPSEEK.md, agents.md, ...) keep only
  identity, working style, and a pointer here. Resource facts must exist in
  exactly one place — this doc.
- **Not dynamic state.** The AI-maintained session brief (project-progress
  index) lives at `tmp/latest-brief.md` per the memory-layering rule in
  `shared-collaboration-rules.md` — never inside this doc. Facts here change
  when the human changes the workspace layout, not per session.

## Doc resolution

- The doc is needed only when the selected mode touches workspace resources
  (writing into the vault, locating literature, resolving note spaces).
  Pure conversation (Research Discussion; Concept Explainer without capture)
  proceeds without it.
- Doc missing → say so and offer init (procedure below). Do not guess paths
  from the workspace without going through init.
- Doc present but first line lacks the marker → proceed, but warn once and
  offer to conform it.
- A required section missing → warn and ask the user; do not infer its
  content.
- Marker version older than the skill's contract → proceed, warn once, and
  offer to upgrade the doc. Never hard-fail on a version mismatch — iteration
  room is the point of the version field.

## Required H2 sections (exact headings)

```
## Workspace overview
## Research logs
## Literature
## Note spaces
## Papers & presentations
## Code & compute
## Discussion archive
```

Extra sections are allowed anywhere and are ignored unless a mode needs them.
Content inside each section is free-form prose, paths, and commands — the
skill reads it, it does not parse it mechanically.

## Section semantics

- **Workspace overview** — what this research project is, in a paragraph, and
  what the workspace is for (discussion-only, code-included, ...).
- **Research logs** — where research logs live, the frontmatter contract a
  log must satisfy to be picked up by dashboards, naming/date conventions,
  the TOC/dashboard that aggregates them, and storage caveats (e.g.
  cloud-synced files that may be unmaterialized).
- **Literature** — the reference-manager library (path, lock/access notes,
  the collections that matter), the AI-survey notes directory, the human-read
  notes directory and its boundary (AI never writes there), the PDF storage
  directory and naming scheme, and the dashboard that aggregates notes.
- **Note spaces** — an inventory of the workspace's other note areas (study
  notes, tech notes, project notes, ...) with each area's local conventions
  (frontmatter or none, language, granularity). Consumers (e.g. Concept
  Explainer capture) must choose a fitting existing area and must never
  create a new directory.
- **Papers & presentations** — each paper/presentation project: location,
  how it is linked into the workspace (e.g. symlinks to independent git
  repos), and what editing a linked path really edits.
- **Code & compute** — each code repository: where it is (local
  path/symlink, remote host + access command), the evidence discipline that
  applies (read-only by default), and a pointer to the repo's own
  operational runbooks (`EXPERIMENTS.md`, `OPERATIONS.md`, ...). This doc
  indexes those runbooks; it never duplicates their content.
- **Discussion archive** — where multi-agent/human discussions are archived
  and the per-agent file convention that applies.

## Genericity rule

Headings and their semantics must make sense for an arbitrary research
workspace — nothing vault-software-, reference-manager-, or project-specific
in the contract itself. All specifics live in the section bodies.

## Init procedure

Goal: produce a contract-conforming `RESEARCH-CONTEXT.md` at the workspace
root (skeleton: `../assets/RESEARCH-CONTEXT.template.md`).

1. **Guard.** If `RESEARCH-CONTEXT.md` already exists, show its first lines
   and ask for explicit confirmation before replacing or rewriting it. Never
   silently overwrite.
2. **Explore before asking.** Gather evidence from the workspace itself:
   vault links/directories and one or two recent research logs (frontmatter,
   naming); note areas and their local conventions; paper/presentation links
   and where they point; code symlinks; per-AI instruction files and other
   existing docs for stated conventions. Where docs contradict the
   filesystem, trust the filesystem and note the contradiction.
3. **Interview only for the genuine gaps** — things the filesystem cannot
   tell you: which reference-manager collections matter, remote hosts and
   access rules, boundaries that are policy rather than layout (e.g. "AI
   never writes into the human-read notes dir"). Ask few, targeted
   questions; mark reasonable inferences as such in the draft.
4. **Draft** from the template: fill every required section; marker on
   line 1; keep it factual (paths + conventions, no methodology —
   methodology lives in the skill). English unless the workspace's docs are
   consistently in another language.
5. **Review gate.** Show the draft to the human; write only after approval.
   Suggest slimming the per-AI instruction files to pointers at the same
   time, so each resource fact exists in exactly one place.
6. **Smoke.** Resolve one real question against the new doc (e.g. "where
   would an AI-survey note land?") to prove the sections are actionable.

// Literature-survey TEMPLATE — Phase 4a: per-angle technique digest.
// One agent per survey angle reads that angle's already-fact-checked notes and
// produces a structured "what transfers to our project" digest.
//
// HOW TO USE: copy this file next to your survey's manifest, fill the CONFIG
// block, then run with Workflow({scriptPath: "<this file>"}). The angles and
// PROJECT_CONTEXT below are placeholders — replace them.
//
// Pairs with verify-wf.js (run verify BEFORE digest so notes are trustworthy)
// and the 4-phase protocol in MISSION-template.md.

export const meta = {
  name: 'survey-digests',
  description: 'Per-angle digest: one agent per survey angle reads its notes and produces a structured transfer digest',
  phases: [{ title: 'Digest', detail: 'one agent per survey angle' }],
}

// ===== CONFIG (edit per survey) =====
const MANIFEST = '/ABS/PATH/TO/review-manifest.md'   // table with a "Primary angle" column + Note filename column
const NOTEDIR  = '/ABS/PATH/TO/ai-survey-notes/YYYY-MM'  // where the per-paper notes live
const OUTDIR   = '/ABS/PATH/TO/survey-folder'        // where digest-<key>.md files are written
const DIGEST_MODEL = 'opus'                          // reading+writing → opus; omit to inherit session model

// One self-contained paragraph a zero-context reader can follow. Used so each
// agent can judge whether a technique actually transfers. Rewrite per project.
const PROJECT_CONTEXT =
  'PROJECT CONTEXT: <one paragraph describing the project, its architecture, its open problems, ' +
  'and the concrete things you are hunting for in the literature>.'

// The concrete adoption targets a technique can hit — the digest must tie each
// "high-transfer" finding to one of these. Rewrite per project.
const TRANSFER_TARGETS = 'target-A / target-B / target-C / target-D'

// One entry per survey angle. `key` becomes the digest filename + the value the
// manifest's "Primary angle" column must match exactly. `hook` is the
// project-specific lens for that angle. REPLACE with your survey's angles.
const angles = [
  { key: 'angle-a', hook: '<what to look for in this angle, framed by the project>.' },
  { key: 'angle-b', hook: '<the project-specific question this angle should answer>.' },
  // ... add the rest of your angles ...
]
// ===== END CONFIG =====

phase('Digest')
const results = await parallel(angles.map(a => () =>
  agent(
    `You are writing a TECHNIQUE-FAMILY DIGEST for a technique-transfer survey, family = "${a.key}". Reply in Chinese, plain short sentences (one idea per sentence). Your output is a structured markdown file, written by you.\n\n` +
    `FAMILY FOCUS / 迁移钩子: ${a.hook}\n\n` +
    `STEP 1 - read the manifest table at ${MANIFEST}. Select EVERY row whose "Primary angle" column equals exactly "${a.key}". For each, note the Note filename and any cross-angle column.\n\n` +
    `STEP 2 - read EACH of those notes in full at ${NOTEDIR}/<Note filename>. These notes were already fact-checked against their PDFs, so trust their numbers, but read the 杂谈/思考/批判 (transfer analysis) section of each carefully — that is your raw material.\n\n` +
    `${PROJECT_CONTEXT}\n\n` +
    `STEP 3 - write a digest to ${OUTDIR}/digest-${a.key}.md with EXACTLY these sections:\n` +
    `  # ${a.key} — 技术迁移 digest\n` +
    `  ## 本族覆盖 — a bullet list: each paper as [[Note filename without .md]] + one-line what-it-is (so the count is visible).\n` +
    `  ## 高可迁移性 — the techniques rated 可迁移性=高 across these notes. For each: which paper, the EXACT mechanism, which of our transfer targets it hits (${TRANSFER_TARGETS}), what we would change to adopt it, and the risk. Be concrete and cite the [[note]]. Rank most-promising first.\n` +
    `  ## 中 / 低可迁移性 — briefly, grouped; for 低 say why it does not transfer (so we do not revisit it).\n` +
    `  ## 本族贯穿主题 — cross-cutting patterns within this family (a recurring trick, a shared failure mode, a consensus or disagreement between papers).\n` +
    `  ## 负面结果 / 警示 — any negative results, instability, or "does not work" findings in these notes (negative results are first-class).\n` +
    `  ## 优先读 — the 2-3 papers in this family most worth the human reading first, one-line why each.\n\n` +
    `Discipline: every claim must trace to a note you read; do not invent numbers or papers. Use [[note filename without .md]] wiki-links so the digest is navigable. No generic filler.\n\n` +
    `Final message: just the digest filename you wrote (digest-${a.key}.md). Nothing else.`,
    { label: `digest:${a.key}`, phase: 'Digest', model: DIGEST_MODEL }
  )
))

return { digests: results.filter(Boolean) }

// Literature-survey TEMPLATE — Phase 3.5: adversarial per-note verification.
// One skeptical agent per paper re-reads the PDF as ground truth, audits the
// note for factual / method-fidelity / transfer-analysis errors, and FIXES them
// in place. Run this AFTER the deep-read phase and BEFORE the digest phase.
//
// HOW TO USE: copy next to your manifest, fill the CONFIG block, run with
// Workflow({scriptPath: "<this file>"}). PROJECT_CONTEXT and TRANSFER_TARGETS
// are EXAMPLES — replace them. Output verdicts come back as FIXED / PASS / FLAG.

export const meta = {
  name: 'survey-verify',
  description: 'Verify every survey note against its PDF, one agent per paper, fix factual / method / transfer-analysis errors in place',
  phases: [{ title: 'Verify', detail: 'one agent per paper: cross-check vs PDF, fix in place' }],
}

// ===== CONFIG (edit per survey) =====
const MANIFEST = '/ABS/PATH/TO/review-manifest.md'  // numbered table: # | Title | Venue+Year | Primary angle | PDF filename | Note filename
const PDFDIR   = '/ABS/PATH/TO/reference/<topic>'   // where the downloaded PDFs live
const NOTEDIR  = '/ABS/PATH/TO/ai-survey-notes/YYYY-MM'  // where the notes live
const NOTE_COUNT  = 0           // set to N: number of manifest rows = number of notes to verify
const SURVEY_DATE = 'YYYY-MM-DD'  // the date stamped in note frontmatter — must be preserved on edit
const VERIFY_MODEL = 'opus'     // adversarial reading → opus; omit to inherit session model

const PROJECT_CONTEXT =
  'PROJECT CONTEXT (so you can judge the transfer analysis): <one paragraph describing the project, ' +
  'its architecture, its open problems, and the concrete adoption targets>.'

const TRANSFER_TARGETS = 'target-A / target-B / target-C / target-D'
// ===== END CONFIG =====

const rows = Array.from({ length: NOTE_COUNT }, (_, i) => i + 1)

phase('Verify')
const results = await parallel(rows.map(n => () =>
  agent(
    `You are an adversarial fact-checker for ONE paper-review note in a technique-transfer survey. Your job is to CATCH ERRORS, not to praise. Be skeptical. Your final message is a status line, not human-facing prose.\n\n` +
    `STEP 1 - read the manifest table at ${MANIFEST} and find the SINGLE row numbered ${n} in the "#" column. It gives the Title, Venue+Year, Primary angle, PDF filename, and Note filename for YOUR paper.\n\n` +
    `STEP 2 - read the existing note at ${NOTEDIR}/<Note filename>. This is what you are auditing.\n\n` +
    `STEP 3 - read the PDF at ${PDFDIR}/<PDF filename> THOROUGHLY (method + experiments, not just abstract). This is ground truth.\n\n` +
    `STEP 4 - AUDIT the note against the PDF on three axes:\n` +
    `  (a) FACTUAL: every number, dataset name, metric, hyperparameter, venue, year, author claim in the note must match the PDF. Flag any number that is wrong, hallucinated, or unverifiable from the PDF.\n` +
    `  (b) METHOD FIDELITY: the note's description of the paper's core mechanism must be accurate — not a plausible-sounding but wrong paraphrase. Check the actual equations/architecture in the PDF.\n` +
    `  (c) TRANSFER ANALYSIS: the 杂谈/思考/批判 section must give a SPECIFIC, defensible 可迁移性 高/中/低 verdict that names a concrete mechanism of THIS paper, ties it to one of our transfer targets (${TRANSFER_TARGETS}), and states what must change + the risk. Generic praise or vague hand-waving is a DEFECT to fix. An analysis built on a misread of the method is wrong even if it sounds good.\n\n` +
    `${PROJECT_CONTEXT}\n\n` +
    `STEP 5 - FIX IN PLACE. Edit the note at ${NOTEDIR}/<Note filename> directly to correct any factual error, fix any misread of the method, and sharpen any vague transfer analysis into a specific mechanism->transfer-target judgment. Preserve the frontmatter contract exactly (do NOT change status away from "reading", keep origin: ai-survey, keep all tags, keep date "${SURVEY_DATE}"). Keep the Chinese plain short-sentence style. If a number genuinely cannot be verified from the PDF, mark it inline as 「PDF 未明确，待核」 rather than deleting it silently. Do not pad — only change what is wrong or vague.\n\n` +
    `Final message: ONE line, exactly one of:\n` +
    `  'PASS <Note filename>' if the note was already accurate and specific (no edit needed),\n` +
    `  'FIXED <Note filename>: <terse list of what you corrected>' if you edited it,\n` +
    `  'FLAG <Note filename>: <what you could not verify and why>' if something is unverifiable.\n` +
    `Nothing else.`,
    { label: `verify:${n}`, phase: 'Verify', model: VERIFY_MODEL }
  )
))

return { verified: results.filter(Boolean).length, verdicts: results }

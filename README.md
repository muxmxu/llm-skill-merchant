# llm-skill-merchant

**The central hub for every Claude Code skill I build.** Cross-machine,
cross-machine: any skill created on any of my machines lands here as (part of)
a plugin; every machine consumes from here. One repository = one source of
truth — no more per-machine skill drift.

## How it works

This repo is a Claude Code **plugin marketplace** (`.claude-plugin/
marketplace.json`). It can hold any number of plugins; each plugin can hold
any number of skills:

```
.claude-plugin/marketplace.json   marketplace manifest (name: llm-skill-merchant)
plugins/<plugin-name>/            one directory per plugin
  .claude-plugin/plugin.json
  skills/<skill-name>/SKILL.md    one directory per skill
  references/, assets/            optional shared material
```

## Consuming (any machine)

```bash
claude plugin marketplace add <owner>/llm-skill-merchant   # uses git/ssh credentials
```

Then enable the plugins you want, at user level (`~/.claude/settings.json`):

```json
{
  "enabledPlugins": {
    "human-ai-code-agent-kit@llm-skill-merchant": true
  }
}
```

Pulling updates: `/plugin marketplace update llm-skill-merchant` (third-party
marketplaces don't auto-update by default; background auto-update of a private
repo would need `GITHUB_TOKEN`).

## Developing (the machine where you edit skills)

Register the local clone as a **directory source** instead — edits take effect
on the next session, no push needed:

```bash
claude plugin marketplace add <path-to-local-clone>
```

⚠️ Never register both the directory source and the GitHub source on the same
machine — the marketplace name collides. Remove one before adding the other
(`/plugin` → Marketplaces).

## Adding a new skill or plugin

1. New skill in an existing plugin: add `plugins/<plugin>/skills/<name>/SKILL.md`.
2. New plugin: create `plugins/<name>/` with `.claude-plugin/plugin.json` +
   `skills/`, and append an entry to `.claude-plugin/marketplace.json`
   (`"source": "./plugins/<name>"`).
3. `claude plugin validate .` from the repo root → commit → push.
4. Other machines pick it up via `/plugin marketplace update llm-skill-merchant`.

## Plugin catalog

| Plugin | Tag | Skills | Purpose |
|---|---|---|---|
| `human-ai-code-agent-kit` | `<suit-for-code-agent>` | `exp`, `eval`, `ops`, `impl`, `codebase-snapshot` | AI-Code-Agent-side research operations: experiment lifecycle, evaluation, compute/VM ops, implementation workflow, plus a read-only codebase-snapshot investigation report. `exp`/`eval`/`ops`/`impl` are doc-contract-driven — project facts live in each repo's runbooks (`EXPERIMENTS.md`, `EVALUATION.md`, `OPERATIONS.md`, dev rules); port to a new project with `/exp init`, `/eval init`. `codebase-snapshot` needs no runbook. |
| `human-ai-research-assistant-kit` | `<suit-for-ai-research-assistant>` | `research-assistant` (10 modes plus speaker-card stage) | AI-Research-Assistant-side kit: research discussion, concept explanation, human-facing research logs, decision/progress notes, code-agent tasks, technical references, literature-survey fan-out, and academic presentation writing. Workspace tone rules govern human-facing prose; recent logs supply content and local form, not an unchecked persona. The kit preserves evidence levels, chronology, and user-defined author-source markers. `RESEARCH-CONTEXT.md` remains the workspace resource map. |
| `multi-agent-discussion` | `<suit-for-ai-research-assistant>` | `multi-agent-discussion` | Structured multi-round debate protocol between several AI agents and the human: per-agent `*_said.md` under `agents-human-discussion/{topic}-{date}/`, quote-before-rebut, evidence vs speculation labels, human-arbitrated `final.md`. Role-neutral in practice — any participating agent follows it as a research-thinking peer. |

## Conventions

- **Role tags** (for plugins in the human-AI research collaboration family):
  `suit-for-code-agent:` / `suit-for-ai-research-assistant:` in role-scoped
  SKILL.md descriptions (marketplace catalogs may retain legacy display labels), so the two sides never blur
  (protocol: `plugins/human-ai-code-agent-kit/references/roles.md`). Plugins
  outside that family (e.g. machine-maintenance utilities) need no role tag.
- **Generic over specific**: skills should carry workflow logic only; facts
  that vary per project belong in per-project docs the skill reads (the
  doc-contract pattern). A skill you can't reuse on the next project probably
  wants splitting into skill + doc.
- English for skill/plugin content (portable); commit messages without
  AI-attribution lines.

## Cross-model compatibility and maintenance

The shared execution contract defaults to guided execution for Luna and untested
model/workflow pairs. Opus, Astra, and other names do not automatically select a
shorter profile or waive evidence, authorization, or human-review requirements.
Keep the detailed mode references. Compact execution is an explicit opt-in.

Skill descriptions use plain role labels (`suit-for-code-agent:` or
`suit-for-ai-research-assistant:`) rather than XML-like role tags. Put the
requested outcome first; mode details belong in the selected reference.

Before publishing, run `python3 scripts/check_skills.py` and, when both source
repositories are available, add `--peer /path/to/the/other/repo`. Review the
limited parity map in `docs/compatibility-sync.json`; it is not a claim that
all platform-specific files are identical. Run the behavioral cases in
`evals/compatibility/cases.json` in isolated sessions for each model used.
Structural validation is not proof of behavioral compatibility. Record the
model/runtime, profile, source revision, result, latency, and token usage;
leave untested model rows unverified.

Keep workflow requirements shared; retain each host's manifests, invocation,
subagent, transport, and permission adapters. Do not copy Claude Workflow
scripts into Codex or replace the human-owned model dispatch table.

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
| `human-ai-code-agent-kit` | `<suit-for-code-agent>` | `exp`, `eval`, `ops`, `impl` | AI-Code-Agent-side research operations: experiment lifecycle, evaluation, compute/VM ops, implementation workflow. Doc-contract-driven — project facts live in each repo's runbooks (`EXPERIMENTS.md`, `EVALUATION.md`, `OPERATIONS.md`, dev rules); port to a new project with `/exp init`, `/eval init`. |
| *(planned)* research-assistant-side kit | `<suit-for-ai-research-assistant>` | — | Research writing/investigation workflows (being built by a separate agent; will migrate in from another machine). |

## Conventions

- **Role tags** (for plugins in the human-AI research collaboration family):
  `<suit-for-code-agent>` / `<suit-for-ai-research-assistant>` in the plugin
  description and every SKILL.md description, so the two sides never blur
  (protocol: `plugins/human-ai-code-agent-kit/references/roles.md`). Plugins
  outside that family (e.g. machine-maintenance utilities) need no role tag.
- **Generic over specific**: skills should carry workflow logic only; facts
  that vary per project belong in per-project docs the skill reads (the
  doc-contract pattern). A skill you can't reuse on the next project probably
  wants splitting into skill + doc.
- English for skill/plugin content (portable); commit messages without
  AI-attribution lines.

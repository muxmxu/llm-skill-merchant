# llm-skill-merchant

Personal Claude Code plugin marketplace (private). One repository, many plugins,
so skills built on any of my machines can be consolidated and reused everywhere.

## Layout

```
.claude-plugin/marketplace.json   marketplace manifest (name: llm-skill-merchant)
plugins/<plugin-name>/            one directory per plugin
  .claude-plugin/plugin.json
  skills/<skill-name>/SKILL.md    multi-skill plugins
```

## Role taxonomy

Plugins here are scoped to a role in the 3-role human-AI research collaboration
model (Human Researcher / AI Research Assistant / AI Code Agent). Each plugin
declares its role with a literal tag in its `plugin.json` description and in
every `SKILL.md` description:

| Tag | Role | Typical skills |
|---|---|---|
| `<suit-for-code-agent>` | AI Code Agent | experiment launch/monitoring, evaluation, compute ops, implementation workflow |
| `<suit-for-ai-research-assistant>` | AI Research Assistant | research logs, decision notes, references, task authoring, literature work |

A skill tagged for one role must not silently take over the other role's
duties; see `plugins/human-ai-code-agent-kit/references/roles.md`.

## Plugins

- **human-ai-code-agent-kit** `<suit-for-code-agent>` — doc-contract-driven
  operational skills: `exp` (experiment lifecycle), `eval` (evaluation),
  `ops` (compute/VM lifecycle), `impl` (implementation workflow). Project
  facts live in each project's own runbook docs; port to a new project with
  `/exp init`, `/eval init`, etc.

## Registering this marketplace

On a machine that should **consume** the plugins (uses git/ssh credentials for
the private repo):

```bash
claude plugin marketplace add <owner>/llm-skill-merchant
```

Then enable plugins at user level in `~/.claude/settings.json`:

```json
{
  "enabledPlugins": {
    "human-ai-code-agent-kit@llm-skill-merchant": true
  }
}
```

Updates: third-party marketplaces do not auto-update by default — run
`/plugin marketplace update llm-skill-merchant` (or set `autoUpdate: true`;
background auto-update of a private repo needs `GITHUB_TOKEN`).

On the machine where you **develop** the plugins, register the local clone as
a directory source instead (instant iteration, no push needed):

```bash
claude plugin marketplace add <path-to-local-clone>
```

⚠️ Do not register both the directory source and the GitHub source on the same
machine — the marketplace name collides. Remove one before adding the other.

## Adding a plugin

1. Create `plugins/<name>/` with `.claude-plugin/plugin.json` and `skills/`.
2. Append an entry to `.claude-plugin/marketplace.json` (`source: "./plugins/<name>"`).
3. `claude plugin validate .` from the repo root, then commit and push.

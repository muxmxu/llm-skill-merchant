# Compatibility evaluation

Run each case in a fresh isolated session with fixed fixture data and no real external systems. Compare the old and updated skill versions with the same underlying model and host. Guided is the default; select compact only explicitly. Record actual artifacts, tool evidence, token counts, and elapsed time. Leave untested model entries unverified.

Maintain separate rows for Luna, each deployed Opus version, Astra, and every other deployed model. One model result does not imply another model result. The Claude plugin evaluation format and skill-creator format differ; `cases.json` is a portable source specification and requires an adapter before either tool can run it. Never run fixture commands on real infrastructure. A simulator or dry-run result is not a production-operation result.

| Model profile | Guided | Compact | Evidence status |
|---|---|---|---|
| Luna | unverified | unverified | unverified |
| Opus (each deployed version, separate row) | unverified | unverified | unverified |
| Astra | unverified | unverified | unverified |
| Other deployed models (one row per model) | unverified | unverified | unverified |

Give the tested model only `prompt` and `fixture`; keep `expected` and `forbidden` for the reviewer. Tool scenarios require a simulator adapter; this source specification is not directly executable by tools.

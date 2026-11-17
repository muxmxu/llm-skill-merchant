# Development rules against over-defensive work

Agents left alone add guards, fallbacks, options, suppressions, and caveats
that no requirement asked for, and they protect a green check instead of the
behaviour it checks. These rules remove that. They bind every writer and
reviewer in the run.

They never remove: validation at trust boundaries (user input, files,
network, subprocesses, external services), handling that prevents data loss,
security measures, and resource cleanup.

## How they take effect

The rules live in the project's development-rules doc (`<rules doc>`), so
`impl task` follows them and `impl check` reports them; `init` proposes the
section below for the human to adopt. That doc, linter configuration, and the
vendored rule check are human-owned: an implementation task never edits them.
Checks, strongest first: linter configuration, the rule check script on every
diff, the semantic reviewer.

## Rules

| ID | Rule | Check |
|---|---|---|
| C1 | Handle errors only at the trust boundaries the spec names, with the behaviour the spec defines. Elsewhere let errors propagate. | Reviewer; rule check REVIEW on broad catches |
| C2 | No blind catch and no swallow-and-default: no bare `except`, no empty handler, no handler that returns a default, `None`, or an empty value to hide a failure. | Linter; rule check FAIL |
| C3 | No fallback, retry, or degraded mode the spec does not define; a defined one is visible (logged or reported). | Reviewer; drift audit |
| C4 | No defensive `isinstance`, `hasattr`, `None`, or length checks on values the types or the caller contract already guarantee. | Reviewer |
| C5 | No inline lint, type, or coverage suppression. An exception is a line in the linter configuration with a recorded reason, approved at the Rules gate. | Linter configuration; rule check FAIL |
| C6 | No option, flag, parameter, environment variable, or config key the spec does not define. | Reviewer; drift audit |
| C7 | No compatibility shim, deprecation path, or version branch before the first release; afterwards only for the published interface the changelog names. | Reviewer |
| C8 | No interface, base class, factory, registry, or wrapper with one implementation, unless the spec names the second. | Reviewer |
| C9 | Delete code instead of commenting it out; no dead code; no stub "for later". Comments say why, not what, and carry no change history. | Linter; reviewer |
| T1 | Never loosen a tolerance, delete or weaken an assertion, add an unconditional skip, xfail, or only, or mock the unit under test to make a check pass. When a check cannot pass honestly, report BLOCKED with the failing output. A conditional skip (optional dependency, missing device) states its condition and reason. | Rule check FAIL (unconditional skip, xfail, only, focused test) and REVIEW (conditional skip, assertion removed, tolerance changed); reviewer |
| T2 | A bug fix starts with a test that fails on the old code; the task record shows the failing run, then the passing run. | Reviewer reads the record |
| T3 | Tests check behaviour the spec defines, not implementation details or restated constants; product code has no test-only branches. | Reviewer |
| P1 | Finish in-scope work without asking permission; questions go only to the gates. | Audit of the session record |
| P2 | A plan, stub, TODO, or placeholder is not an implementation of the task. | Rule check REVIEW; reviewer |
| P3 | "Done" means the task's checks ran in this task on the final tree, with commands and results recorded. FAIL and NOT RUN keep their label. | Mechanical audit reruns the checks |
| P4 | Reports state facts: what changed, what ran, results, what is open. No speculation presented as fact, no list of hypothetical risks. | Reviewer |
| P5 | Do not re-ask a recorded decision, re-run an unchanged passing check, or add a review round beyond the cap; park out-of-scope findings in the backlog. | Audit of the session record |
| P6 | Rule files are human-owned; propose changes at the Rules gate. | `impl check` protected zones |

## Linter configuration

Where the project's tools support it, enforce in configuration rather than in
review. Examples:

- Python with ruff: enable `E722` (bare except), `BLE001` (blind except),
  `S110` and `S112` (try-except-pass, try-except-continue), `ERA001`
  (commented-out code), `PGH004` (blanket noqa).
- Python type checking: pyright `enableTypeIgnoreComments = false`, or mypy
  `warn_unused_ignores` with `enable_error_code = ["ignore-without-code"]`.
- TypeScript with ESLint: `linterOptions.noInlineConfig: true`, `no-empty`,
  `@typescript-eslint/ban-ts-comment`.

Each disabled rule or per-file exception in the configuration carries a
comment with its reason and the decision id that approved it.

## Rule check script

`scripts/check_diff_rules.py` scans the diff against a base ref (default
`HEAD`) plus untracked files, in Python and JavaScript/TypeScript files only;
each language's patterns apply only to its own files. It sets its own diff
prefixes, hunk merging, and path quoting, so the user's git configuration and file names with
spaces or non-ASCII characters do not change the result, and it exits with an
error instead of skipping a diff it cannot parse. It is vendored into the
project at the path `<rule check>` names, so it runs without this plugin.

- **FAIL** (exit 1): inline suppressions (C5); unconditional skip and xfail
  (`pytest.mark.skip`, `pytest.skip(`, `pytest.xfail(`, `unittest.skip`,
  `expectedFailure`), and in JS test files `.skip(`, `.only(`, `.todo(`,
  `xit(`, `fit(`, and the other focused or skipped tests (T1); bare `except`, handlers whose body
  is only `pass` or `...`, empty `catch` blocks, `.catch(() => {})` (C2).
- **REVIEW** (reported, exit 0): broad `except Exception` / `BaseException`
  and `catch` (C1); conditional skips (`pytest.mark.skipif`,
  `pytest.importorskip(`, `unittest.skipIf` / `skipUnless`), and assertions or
  tolerances on lines removed from test files, which is how a changed
  tolerance shows up (T1); added TODO, FIXME, XXX, HACK, or
  `NotImplementedError` (P2). New tolerances in new tests are not flagged.

A conditional skip written as an imperative `pytest.skip(` inside an `if` is a
FAIL; write it as `skipif` or `importorskip` instead.

The mechanical auditor attaches the output; the reviewer gives each REVIEW
line a disposition (allowed at a named trust boundary, follows a spec change,
or a defect).

## Section to adopt in the rules doc

`init` proposes this block, unchanged except for the script path:

```markdown
## Development rules (lifecycle v1)

Errors and fallbacks
- C1 Handle errors only at the trust boundaries the spec names; elsewhere let them propagate.
- C2 No bare or blind catch, no empty handler, no swallow-and-default.
- C3 No fallback, retry, or degraded mode the spec does not define.
- C4 No defensive type, attribute, None, or length checks on guaranteed values.

Code shape
- C5 No inline lint, type, or coverage suppressions; exceptions only in linter configuration with a reason and a decision id.
- C6 No option, flag, parameter, environment variable, or config key outside the spec.
- C7 No compatibility shims before the first release.
- C8 No abstraction with a single implementation.
- C9 Delete instead of commenting out; comments explain why.

Tests
- T1 Never loosen tolerances, delete or weaken assertions, add unconditional skip/xfail/only, or mock the unit under test to get green; report BLOCKED with the failing output. Conditional skips (skipif, importorskip) state their reason.
- T2 Bug fixes start with a test that fails on the old code.
- T3 Tests check specified behaviour, not implementation details.

Process
- P1 Finish in-scope work without asking; ask only at the lifecycle gates.
- P2 Plans, stubs, and TODOs are not implementations.
- P3 Done means the checks ran in this task on the final tree.
- P4 Reports state facts only.
- P5 No re-asking recorded decisions, no re-running unchanged checks, no review rounds beyond the cap.
- P6 This section, linter configuration, and the rule check are human-owned.

Kept regardless: trust-boundary validation, data-loss handling, security, resource cleanup.

Check: `python3 <rule check path> --base <base ref>` on every task diff; FAIL blocks the merge, every REVIEW line needs a disposition.
```

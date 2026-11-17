#!/usr/bin/env python3
"""Scan a diff for over-defensive patterns (lifecycle development rules).

Usage (from the repository root):
    check_diff_rules.py [--base REF]

Scans code files changed against REF (default HEAD, working tree included)
plus untracked files. Prints one line per finding:
    FAIL|REVIEW <rule id> <path>:<line>: <text>
Exit 1 when any FAIL line is printed. Rule ids refer to the development-rules
section of the project's rules doc.
"""

from __future__ import annotations

import argparse
import codecs
import re
import subprocess
import sys
from pathlib import Path

PY_SUFFIXES = {".py", ".pyi"}
JS_SUFFIXES = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts", ".vue", ".svelte"}
TEST_DIRS = {"test", "tests", "__tests__", "e2e"}
TEST_NAME = re.compile(r"^(?:test_.*\.py|.*_test\.py|conftest\.py|.*\.(?:test|spec)\.[cm]?[jt]sx?)$")

# Patterns are written so that this file does not match itself when vendored.
FAIL_ADDED = {
    "py": [
        ("C5", re.compile(r"#\s*(?:noqa\b|type:\s*ignore|pyright:|pylint:\s*disable|mypy:|pragma:\s*no\s*cover)")),
        ("T1", re.compile(r"pytest\.mark\.(?:skip|xfail)\b|pytest\.(?:skip|xfail)\(")),
        ("T1", re.compile(r"unittest\.(?:skip|expectedFailure)\b|@(?:skip|expectedFailure)\b")),
        ("C2", re.compile(r"^\s*except\s*:")),
        ("C2", re.compile(r"^\s*except\b[^:]*:\s*(?:pass|\.\.\.)\s*(?:#.*)?$")),
    ],
    "js": [
        ("C5", re.compile(r"eslint-[d]isable|biome-[i]gnore|@ts-(?:ignore|expect-error|nocheck)|(?:istanbul|c8|v8)\s+ignore")),
        ("T1", re.compile(r"(?<![\w.$])(?:it|test|describe|context)\.(?:skip|only|todo|fixme|fails)\(|(?<![\w.$])(?:x(?:it|test|describe)|f(?:it|describe))\(")),
        ("C2", re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*\}")),
        ("C2", re.compile(r"\.catch\(\s*(?:\(\s*\w*\s*\)|\w+)\s*=>\s*(?:\{\s*\}|undefined|null)\s*\)")),
    ],
}
REVIEW_ADDED = {
    "py": [
        ("C1", re.compile(r"\bexcept\s*\(?\s*(?:Exception|BaseException)\b")),
        # Conditional skips (optional dependency, device) need a reason, not a gate.
        ("T1", re.compile(r"pytest\.mark\.skipif\b|pytest\.importorskip\(|unittest\.skip(?:If|Unless)\b|[@]skip(?:If|Unless)\b")),
        ("P2", re.compile(r"\b(?:TO[D]O|FIX[M]E|X[X]X|HA[C]K)\b|NotImplemented[E]rror")),
    ],
    "js": [
        ("C1", re.compile(r"\bcatch\s*[({]")),
        ("P2", re.compile(r"\b(?:TO[D]O|FIX[M]E|X[X]X|HA[C]K)\b")),
    ],
}
TOLERANCE = re.compile(r"\b(?:rtol|atol|abs_tol|rel_tol|tol|tolerance|places|delta|eps|epsilon)\s*=|\bapprox\(|toBeCloseTo\(")
ASSERTION = re.compile(r"\bassert|\bexpect\(")
# Multi-line swallow: a handler header followed by a body that only discards.
HANDLER = {"py": re.compile(r"^\s*except\b.*:\s*(?:#.*)?$"), "js": re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*$")}
DISCARD = {"py": re.compile(r"^\s*(?:pass|\.\.\.)\s*(?:#.*)?$"), "js": re.compile(r"^\s*\}")}


def lang(path: str) -> str | None:
    suffix = Path(path).suffix
    return "py" if suffix in PY_SUFFIXES else "js" if suffix in JS_SUFFIXES else None


def is_test(path: str) -> bool:
    p = Path(path)
    return bool(TEST_DIRS & set(p.parts[:-1])) or bool(TEST_NAME.match(p.name))


def header_path(field: str) -> str:
    """Path from a '--- a/x' or '+++ b/x' header; '' for /dev/null."""
    field = field.rstrip("\t")  # git appends a TAB to names that contain spaces
    if field.startswith('"'):  # C-quoted: names with quotes, backslashes, control chars
        field = codecs.escape_decode(field[1:-1].encode("utf-8"))[0].decode("utf-8")
    return "" if field == "/dev/null" else field[2:]


def changes(base: str) -> list[tuple[str, str, int, str]]:
    """(path, '+' or '-', line number, text) for every changed line."""
    out: list[tuple[str, str, int, str]] = []
    # Fixed prefixes, unmerged hunks and unquoted UTF-8 names, whatever the user's git config says.
    diff = subprocess.run(
        ["git", "-c", "core.quotePath=false", "diff", "-U0", "--inter-hunk-context=0", "--no-color",
         "--no-ext-diff", "--src-prefix=a/", "--dst-prefix=b/", base],
        capture_output=True, encoding="utf-8", errors="replace", check=True,
    ).stdout
    path, old_no, new_no, in_header = "", 0, 0, False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            path, in_header = "", True
        elif in_header and line.startswith("--- "):
            path = header_path(line[4:])
        elif in_header and line.startswith("+++ "):
            path = header_path(line[4:]) or path
        elif line.startswith("@@"):
            in_header = False
            m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)", line)
            old_no, new_no = int(m.group(1)), int(m.group(2))
        elif not in_header and line[:1] in "+-" and line:
            if not path:  # fail closed: an unparsed header must not hide changes
                sys.exit(f"check_diff_rules: no file path for diff line {line!r}")
            if line[0] == "+":
                out.append((path, "+", new_no, line[1:]))
                new_no += 1
            else:
                out.append((path, "-", old_no, line[1:]))
                old_no += 1
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        capture_output=True, encoding="utf-8", errors="replace", check=True,
    ).stdout
    for name in filter(None, untracked.split("\0")):
        if lang(name):
            text = Path(name).read_text(encoding="utf-8", errors="replace")
            out.extend((name, "+", i, t) for i, t in enumerate(text.splitlines(), 1))
    return out


def check(lines: list[tuple[str, str, int, str]]) -> list[str]:
    findings: list[str] = []
    prev: tuple[str, int, str] | None = None
    for path, sign, no, text in lines:
        kind = lang(path)
        if kind is None:
            continue
        where = f"{path}:{no}: {text.strip()}"
        test = is_test(path)
        if sign == "-":
            # Changing an existing tolerance shows up as a removed line.
            if test and ASSERTION.search(text):
                findings.append(f"REVIEW T1 {where} (assertion removed)")
            if test and TOLERANCE.search(text):
                findings.append(f"REVIEW T1 {where} (tolerance changed)")
            continue
        # JS T1 names (fit, context.skip) are ordinary calls outside test files.
        fails = [rule for rule, rx in FAIL_ADDED[kind] if rx.search(text) and (test or kind == "py" or rule != "T1")]
        if prev and prev[0] == path and prev[1] == no - 1 and HANDLER[kind].search(prev[2]) and DISCARD[kind].search(text):
            fails.append("C2")
        for rule in dict.fromkeys(fails):
            findings.append(f"FAIL {rule} {where}")
        if not fails:
            findings.extend(f"REVIEW {rule} {where}" for rule, rx in REVIEW_ADDED[kind] if rx.search(text))
        prev = (path, no, text)
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="HEAD")
    args = parser.parse_args()
    findings = check(changes(args.base))
    for line in findings:
        print(line)
    failed = sum(line.startswith("FAIL") for line in findings)
    print(f"{failed} FAIL, {len(findings) - failed} REVIEW")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

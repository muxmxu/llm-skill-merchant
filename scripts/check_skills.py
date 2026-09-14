#!/usr/bin/env python3
"""Validate the portable structural contract for one staged skill host."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EXPECTED_SHARED_FILES = [
    "plugins/human-ai-research-assistant-kit/skills/research-assistant/references/execution-compatibility.md",
    "plugins/human-ai-code-agent-kit/references/execution-compatibility.md",
    "plugins/human-ai-research-assistant-kit/skills/research-assistant/references/speaker-deck-writing.md",
    "plugins/human-ai-research-assistant-kit/skills/research-assistant/references/academic-presentation-writing.md",
    "scripts/check_skills.py",
    "evals/compatibility/cases.json",
    "evals/compatibility/README.md",
]
EXPECTED_HOST_SPECIFIC = [
    "plugin manifests",
    "command wrappers",
    "invocation metadata",
    "orchestration",
    "transport",
    "literature workflow files",
]
EXPECTED_SCOPE_NOTE = (
    "Deliberately limited parity map; this is not a full upstream synchronization claim."
)
PRESENTATION_REL = (
    "plugins/human-ai-research-assistant-kit/skills/research-assistant/references/"
    "academic-presentation-writing.md"
)
PRESENTATION_BEFORE = (
    "Enter this stage through the mode itself or the `/deck` command."
).encode("utf-8")
PRESENTATION_AFTER = (
    "Enter this stage through an explicit request for the speaker card in this mode."
).encode("utf-8")
FRONTMATTER_START = re.compile(r"\A---(?:\r?\n)")
FIELD = re.compile(r"^(name|description):[ \t]*(.*)$")
LOCAL_REFERENCE = re.compile(
    r"`((?:references/|\.\./\.\./references/)[^`\r\n]+\.md)`"
)
VALID_NAME = re.compile(r"^[a-z0-9-]+$")
XML_TAG = re.compile(r"<\s*/?\s*[A-Za-z][^>]*>")


@dataclass
class Skill:
    path: Path
    text: str
    name: str | None
    description: str | None


@dataclass
class RepoState:
    skills: list[Skill]
    sync: dict[str, Any] | None
    by_name: dict[str, Skill]


def add_error(errors: list[str], path: Path, reason: str) -> None:
    errors.append(f"{path}: {reason}")


def read_bytes(path: Path, errors: list[str]) -> bytes | None:
    """Read bytes and report ordinary input failures without raising."""
    try:
        return path.read_bytes()
    except FileNotFoundError:
        add_error(errors, path, "missing")
    except OSError as exc:
        add_error(errors, path, f"cannot read ({exc})")
    return None


def load_json(path: Path, errors: list[str]) -> Any | None:
    """Load UTF-8 JSON, returning None after an actionable error."""
    raw = read_bytes(path, errors)
    if raw is None:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        add_error(errors, path, f"invalid UTF-8 ({exc})")
        return None
    try:
        value = json.loads(text)
        if value is None:
            add_error(errors, path, "JSON root must not be null")
            return None
        return value
    except json.JSONDecodeError as exc:
        add_error(errors, path, f"invalid JSON ({exc.msg} at line {exc.lineno} column {exc.colno})")
    return None


def decode_scalar(raw: str, path: Path, field: str, errors: list[str]) -> str | None:
    """Decode a frontmatter scalar; double-quoted values must be JSON strings."""
    value = raw.strip()
    if not value:
        return None
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            add_error(errors, path, f"{field} is not a valid JSON string ({exc.msg})")
            return None
        if not isinstance(decoded, str):
            add_error(errors, path, f"{field} must decode to a string")
            return None
        return decoded
    if value.startswith("'"):
        add_error(errors, path, f"{field} uses a non-JSON quoted value")
        return None
    return value


def parse_skill(path: Path, errors: list[str]) -> Skill | None:
    """Parse and validate one skill, returning None only when its body is unusable."""
    raw = read_bytes(path, errors)
    if raw is None:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        add_error(errors, path, f"invalid UTF-8 ({exc})")
        return None

    start = FRONTMATTER_START.match(text)
    if start is None:
        add_error(errors, path, "missing frontmatter opening delimiter")
        return None
    close_match = re.search(r"^---[ \t]*(?:\r?\n|\Z)", text[start.end() :], re.MULTILINE)
    if close_match is None:
        add_error(errors, path, "missing frontmatter closing delimiter")
        return None
    body = text[start.end() : start.end() + close_match.start()]

    fields: dict[str, list[str]] = {"name": [], "description": []}
    for line in body.splitlines():
        match = FIELD.match(line)
        if match is not None:
            fields[match.group(1)].append(match.group(2))
    for field in fields:
        if not fields[field]:
            add_error(errors, path, f"missing frontmatter {field}")
        elif len(fields[field]) > 1:
            add_error(errors, path, f"duplicate frontmatter {field}")

    name: str | None = None
    description: str | None = None
    if fields["name"]:
        name = decode_scalar(fields["name"][0], path, "name", errors)
        if name is None or VALID_NAME.fullmatch(name) is None:
            add_error(errors, path, "name must contain only lowercase letters, digits, and hyphens")
            name = None
    if fields["description"]:
        description = decode_scalar(fields["description"][0], path, "description", errors)
        if description is None or not description:
            add_error(errors, path, "description must be nonempty")
            description = None
        elif len(description) > 400:
            add_error(errors, path, f"description exceeds 400 Unicode characters (length {len(description)})")
            description = None
        elif XML_TAG.search(description):
            add_error(errors, path, "description contains an XML-like tag")
            description = None

    for reference in LOCAL_REFERENCE.findall(text):
        target = path.parent / reference
        if not target.is_file():
            add_error(errors, path, f"missing local reference {reference} (resolved as {target})")
    return Skill(path=path, text=text, name=name, description=description)


def safe_relative(root: Path, relative: str) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    return root / candidate


def check_cases(root: Path, errors: list[str]) -> None:
    path = root / "evals/compatibility/cases.json"
    value = load_json(path, errors)
    if value is None:
        return
    if not isinstance(value, list):
        add_error(errors, path, "must be an array of twelve cases")
        return
    if len(value) != 12:
        add_error(errors, path, f"must contain exactly 12 cases (found {len(value)})")

    required = ("id", "skill", "prompt", "fixture", "expected", "forbidden", "profiles")
    seen: set[str] = set()
    for index, case in enumerate(value):
        label = f"case[{index}]"
        if not isinstance(case, dict):
            add_error(errors, path, f"{label} must be an object")
            continue
        case_id = case.get("id")
        id_label = case_id if isinstance(case_id, str) and case_id else label
        for field in required:
            if field not in case:
                add_error(errors, path, f"{id_label}: missing field {field}")
        for field in ("id", "skill", "prompt", "fixture"):
            if field in case and (not isinstance(case[field], str) or not case[field]):
                add_error(errors, path, f"{id_label}: {field} must be a nonempty string")
        if isinstance(case_id, str) and case_id:
            if case_id in seen:
                add_error(errors, path, f"{case_id}: duplicate case id")
            seen.add(case_id)
        for field in ("expected", "forbidden"):
            values = case.get(field)
            if not isinstance(values, list) or not values:
                add_error(errors, path, f"{id_label}: {field} must be a nonempty string array")
            elif any(not isinstance(item, str) or not item for item in values):
                add_error(errors, path, f"{id_label}: {field} must contain only nonempty strings")
        if case.get("profiles") != ["guided", "compact"]:
            add_error(errors, path, f"{id_label}: profiles must equal ['guided', 'compact']")
        skill_rel = case.get("skill")
        if isinstance(skill_rel, str):
            target = safe_relative(root, skill_rel)
            if target is None or not target.is_file():
                add_error(errors, path, f"{id_label}: skill does not point to an existing local file: {skill_rel}")


def check_sync(root: Path, errors: list[str]) -> dict[str, Any] | None:
    path = root / "docs/compatibility-sync.json"
    value = load_json(path, errors)
    if value is None:
        return None
    if not isinstance(value, dict):
        add_error(errors, path, "must be a JSON object")
        return None
    required = {"schema_version", "shared_files", "host_specific", "scope_note"}
    missing = sorted(required - set(value))
    for key in missing:
        add_error(errors, path, f"missing required key {key}")
    if value.get("schema_version") != 1:
        add_error(errors, path, "schema_version must be exactly 1")
    if value.get("shared_files") != EXPECTED_SHARED_FILES:
        add_error(errors, path, "shared_files must equal the exact seven approved paths in order")
    if value.get("host_specific") != EXPECTED_HOST_SPECIFIC:
        add_error(errors, path, "host_specific must list the six non-asserted host-specific areas")
    if value.get("scope_note") != EXPECTED_SCOPE_NOTE:
        add_error(errors, path, "scope_note does not state the limited parity-map scope")
    for relative in EXPECTED_SHARED_FILES:
        target = safe_relative(root, relative)
        if target is None or not target.is_file():
            add_error(errors, path, f"required shared file is missing: {relative}")
    return value


def check_manifests(root: Path, errors: list[str]) -> None:
    manifests = sorted(root.glob("plugins/*/.claude-plugin/plugin.json"))
    manifests += sorted(root.glob("plugins/*/.codex-plugin/plugin.json"))
    if len(manifests) != 6:
        add_error(errors, root / "plugins", f"expected exactly six plugin manifests (found {len(manifests)})")
    for path in manifests:
        value = load_json(path, errors)
        if value is None:
            continue
        if not isinstance(value, dict):
            add_error(errors, path, "JSON root must be an object")
            continue
        expected_name = path.parent.parent.name
        if value.get("name") != expected_name:
            add_error(errors, path, f"name must match containing plugin directory {expected_name}")


def check_repo(root: Path, errors: list[str]) -> RepoState:
    skill_paths = sorted(root.glob("plugins/*/skills/*/SKILL.md"))
    if len(skill_paths) != 10:
        add_error(errors, root / "plugins", f"expected exactly ten SKILL.md files (found {len(skill_paths)})")
    skills: list[Skill] = []
    for path in skill_paths:
        parsed = parse_skill(path, errors)
        if parsed is not None:
            skills.append(parsed)
    check_manifests(root, errors)
    sync = check_sync(root, errors)
    check_cases(root, errors)

    compat_paths = [
        root / "plugins/human-ai-research-assistant-kit/skills/research-assistant/references/execution-compatibility.md",
        root / "plugins/human-ai-code-agent-kit/references/execution-compatibility.md",
    ]
    compat = [read_bytes(path, errors) for path in compat_paths]
    if compat[0] is not None and compat[1] is not None and compat[0] != compat[1]:
        add_error(errors, root / "plugins", "the two execution-compatibility.md files differ")
    state = RepoState(skills=skills, sync=sync, by_name={})
    state.by_name = skill_map(state, errors, "local repository")
    return state


def skill_map(state: RepoState, errors: list[str], label: str) -> dict[str, Skill]:
    result: dict[str, Skill] = {}
    for skill in state.skills:
        if skill.name is None:
            continue
        if skill.name in result:
            add_error(errors, skill.path, f"duplicate skill name {skill.name} in {label}")
            continue
        result[skill.name] = skill
    return result


def normalized_shared(path: Path, relative: str, errors: list[str]) -> bytes | None:
    data = read_bytes(path, errors)
    if data is None:
        return None
    if relative == PRESENTATION_REL:
        data = data.replace(PRESENTATION_BEFORE, PRESENTATION_AFTER)
    return data


def check_peer(root: Path, peer: Path, local: RepoState, errors: list[str]) -> None:
    if not peer.is_dir():
        add_error(errors, peer, "peer repository directory is missing")
        return
    peer_state = check_repo(peer, errors)
    local_sync_bytes = read_bytes(root / "docs/compatibility-sync.json", errors)
    peer_sync_bytes = read_bytes(peer / "docs/compatibility-sync.json", errors)
    if local_sync_bytes is not None and peer_sync_bytes is not None and local_sync_bytes != peer_sync_bytes:
        add_error(errors, root / "docs/compatibility-sync.json", "sync map bytes differ from peer")

    for relative in EXPECTED_SHARED_FILES:
        left = normalized_shared(root / relative, relative, errors)
        right = normalized_shared(peer / relative, relative, errors)
        if left is not None and right is not None and left != right:
            add_error(errors, root / relative, f"shared file differs from peer: {relative}")

    local_by_name = local.by_name
    peer_by_name = peer_state.by_name
    for name, skill in local_by_name.items():
        peer_skill = peer_by_name.get(name)
        if peer_skill is None:
            add_error(errors, skill.path, f"peer is missing skill {name}")
            continue
        if skill.description is not None and peer_skill.description is not None:
            if skill.description != peer_skill.description:
                add_error(errors, skill.path, f"decoded description differs from peer for skill {name}")
    for name, skill in peer_by_name.items():
        if name not in local_by_name:
            add_error(errors, skill.path, f"local repository is missing peer skill {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--peer", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    local = check_repo(root, errors)
    if args.peer is not None:
        check_peer(root, args.peer.resolve(), local, errors)
    result = {"ok": not errors, "errors": errors}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print("\n".join(errors))
    else:
        print("PASS")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Convert, verify and install the 49 Claude Code Game Studios roles for Codex.

Python 3.11+ required. No network, third-party dependencies or destructive updates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone

try:
    import tomllib
except ImportError:
    raise SystemExit("Python 3.11+ is required (tomllib).")

ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = ROOT / "definitions"
OUTPUT = ROOT / "codex" / "agents"
MANIFEST = ROOT / "manifest.json"
EXPECTED = 49


def source_files() -> dict[str, Path]:
    files = {p.stem: p for p in DEFINITIONS.glob("*.md")}
    if len(files) != EXPECTED:
        raise ValueError(f"Expected {EXPECTED} original definitions, found {len(files)}")
    return files


def extract_description(frontmatter: str) -> str:
    match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        raise ValueError("Missing source description")
    raw = match.group(1).strip()
    if raw.startswith('"'):
        return json.loads(raw)
    if raw.startswith("'"):
        return raw[1:-1].replace("''", "'")
    return raw


def convert(name: str, original: str) -> str:
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", original, re.DOTALL)
    if not match:
        raise ValueError(f"Agent {name} does not have a valid Markdown frontmatter")
    description = extract_description(match.group(1))
    body = original[match.end():].replace("\r\n", "\n").strip() + "\n"
    instructions = f"""# Codex-native adaptation of the Claude Code Game Studios agent: {name}
# Agent instructions in this file preserve the complete role guidance from the source.
# Codex compatibility rules take precedence where host-specific mechanics differ.

## Codex execution contract
- You are the **{name}** specialist from Claude Code Game Studios. Apply the complete specialist guidance below.
- Operate using the actual Codex tools available to you. In the original guide, Read/Glob/Grep mean file reads/search, Write/Edit mean authorized file editing, Bash means terminal execution, WebSearch means available research, AskUserQuestion means ask the user conversationally, and Agent/Task means delegate through Codex subagents only if supported and explicitly appropriate. Do not call nonexistent Claude-specific tools.
- The parent session controls sandboxing, approvals, model/provider and installed integrations. Never assume your own instructions grant new privileges. Respect user approvals, and do not repeat approval questions for an action the user has explicitly authorized within its stated scope.
- The source role mentions Claude Code hooks, slash commands, project.yaml, CLAUDE.md, and .claude paths. Treat these as optional project resources, not native Codex features. Prefer AGENTS.md plus actual project files and available Codex skills. If a dependency is missing, perform equivalent reasoning/tests when possible and disclose the gap instead of inventing files or claiming a hook ran.
- In the absence of a parent project's studio workflow, deliver focused work in your specialty with clear evidence and explain relevant limitations.
- Preserve the source guide's scope separation, engineering standards, escalation practices, and review/approval criteria.

## Full original role guidance (host-specific instructions interpreted under the contract above)

{body}"""
    literal = (json.dumps(instructions, ensure_ascii=False)
               if "'''" in instructions else "'''\n" + instructions + "'''")
    return (f"# Codex agent adaptation; original CCGS agent: {name}\n"
            "# Source: https://github.com/Donchitos/Claude-Code-Game-Studios/tree/v1.2.0/.claude/agents\n"
            f'name = "ccgs-{name}"\n'
            f"description = {json.dumps('[CCGS] ' + description, ensure_ascii=False)}\n"
            f"developer_instructions = {literal}\n")


def expected_files() -> dict[str, str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("agent_count") != EXPECTED or len(data.get("files", [])) != EXPECTED:
        raise ValueError("Agent manifest does not contain exactly 49 entries")
    sources = source_files()
    listed = {entry["name"] for entry in data["files"]}
    if set(sources) != listed:
        raise ValueError("Agent names differ from the manifest")

    expected = {}
    for entry in data["files"]:
        name = entry["name"]
        content_bytes = sources[name].read_bytes()
        blob = b"blob " + str(len(content_bytes)).encode("ascii") + b"\0" + content_bytes
        sha = hashlib.sha1(blob).hexdigest()
        if sha != entry["source_blob_sha"]:
            raise ValueError(f"Original Git blob differs from manifest for {name}")
        expected[f"ccgs-{name}.toml"] = convert(name, content_bytes.decode("utf-8"))
    return expected


def validate(expected: dict[str, str]) -> None:
    present = {p.name for p in OUTPUT.glob("*.toml")}
    if set(expected) != present:
        raise ValueError(f"Agent set mismatch; missing={sorted(set(expected)-present)}; unexpected={sorted(present-set(expected))}")
    for filename, rendered in expected.items():
        current = (OUTPUT / filename).read_text(encoding="utf-8")
        if current != rendered:
            raise ValueError(f"Converted role differs from source or adapter: {filename}")
        parsed = tomllib.loads(current)
        if parsed.get("name") != Path(filename).stem:
            raise ValueError(f"Invalid Codex role name: {filename}")
        if not isinstance(parsed.get("description"), str) or not parsed["description"]:
            raise ValueError(f"Missing description: {filename}")
        if not isinstance(parsed.get("developer_instructions"), str) or len(parsed["developer_instructions"]) < 400:
            raise ValueError(f"Missing role instructions: {filename}")
        if set(parsed) != {"name", "description", "developer_instructions"}:
            raise ValueError(f"Unexpected Codex configuration keys: {filename}")
    print(f"VALID: {len(expected)}/{EXPECTED} Codex TOML agents; original Git blobs verified; role instructions preserved.")


def generate(expected: dict[str, str]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, content in expected.items():
        (OUTPUT / filename).write_text(content, encoding="utf-8", newline="\n")
    validate(expected)


def install(expected: dict[str, str], destination: Path, force: bool, dry_run: bool) -> None:
    validate(expected)
    destination = destination.expanduser().resolve()
    conflicts = []
    changed, identical = [], []
    for filename, content in expected.items():
        target = destination / filename
        if target.exists():
            if not target.is_file():
                conflicts.append(filename + " (not a file)")
            elif target.read_text(encoding="utf-8") == content:
                identical.append(filename)
            elif not force:
                conflicts.append(filename)
            else:
                changed.append(filename)
        else:
            changed.append(filename)

    if conflicts:
        raise ValueError("Existing custom agents would be overwritten: "
                         + ", ".join(conflicts)
                         + ". Re-run with --force to back up and replace.")
    if dry_run:
        print(f"DRY RUN: {len(changed)} to install, {len(identical)} unchanged; destination={destination}")
        return
    destination.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup_dir = destination / ".backups" / f"ccgs-{stamp}"
    backups = 0
    for filename in changed:
        target = destination / filename
        if target.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup_dir / filename)
            backups += 1
        # Stage in destination so os.replace is a single-filesystem atomic replace.
        fd, tmp = tempfile.mkstemp(prefix=".ccgs-", suffix=".tmp", dir=destination)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                f.write(expected[filename])
            os.replace(tmp, target)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)

    print(f"INSTALLED: {len(changed)} agents; {len(identical)} already current; {backups} backups; destination={destination}")
    print("Restart Codex if agents do not appear. All agent names use the ccgs- prefix.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Verify 49 TOMLs against original agents and hashes")
    sub.add_parser("generate", help="Regenerate all Codex TOMLs deterministically")
    command = sub.add_parser("install", help="Install agents globally; no overwrite by default")
    command.add_argument("--destination", type=Path, default=Path.home() / ".codex" / "agents",
                         help="Default: ~/.codex/agents; for project use PROJECT/.codex/agents")
    command.add_argument("--force", action="store_true", help="Back up then replace conflicting files")
    command.add_argument("--dry-run", action="store_true", help="Show proposed changes without writing")
    args = parser.parse_args()
    try:
        expected = expected_files()
        if args.command == "validate":
            validate(expected)
        elif args.command == "generate":
            generate(expected)
        else:
            install(expected, args.destination, args.force, args.dry_run)
    except (ValueError, OSError, KeyError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

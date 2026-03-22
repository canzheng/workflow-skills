#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import re
from collections import Counter
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.workflow_state import WORKFLOW_SECTIONS, parse_backlog_document, parse_tasks


ELIGIBLE_SECTIONS = ("BACKLOG", "SHAPING", "READY")
HEADING_RE = re.compile(r"^##(?:\s+\d+(?:\.\d+)*)?\.?\s+(?P<name>.+?)\s*$")


class WorkflowError(RuntimeError):
    pass


def repo_root(explicit_root: str | None = None) -> Path:
    if explicit_root:
        return Path(explicit_root).resolve()

    env_root = os.environ.get("WORKFLOW_REPO_ROOT")
    if env_root:
        return Path(env_root).resolve()

    resolved = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
        check=False,
    )
    if resolved.returncode == 0:
        return Path(resolved.stdout.strip()).resolve()

    raise WorkflowError("could not determine repo root; run inside the target repo or pass --repo-root")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root.")

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="List eligible backlog, shaping, and ready items.")

    apply_parser = subparsers.add_parser("apply", help="Rewrite eligible section order using the approved global ID list.")
    apply_parser.add_argument(
        "--ordered-id",
        action="append",
        dest="ordered_ids",
        required=True,
        help="One approved item ID in global priority order. Repeat for every eligible item.",
    )
    return parser.parse_args(argv)


def resolve_backlog(root: Path) -> tuple[Path, str]:
    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        raise WorkflowError("docs/planning/current_version is missing")
    if not current_version.is_symlink():
        raise WorkflowError("docs/planning/current_version is not a symlink")

    version_root = current_version.resolve()
    backlog_path = version_root / "BACKLOG.md"
    if not backlog_path.exists():
        raise WorkflowError(f"{backlog_path.relative_to(root)} is missing")
    return version_root, str(backlog_path.relative_to(root))


def read_backlog(root: Path) -> tuple[Path, str, object]:
    _, backlog_relative = resolve_backlog(root)
    backlog_path = root / backlog_relative
    backlog_text = backlog_path.read_text(encoding="utf-8")
    parsed_backlog = parse_backlog_document(backlog_text)
    if parsed_backlog.malformed_entries:
        raise WorkflowError(
            "; ".join(f"{backlog_path.relative_to(root)} {message}" for message in parsed_backlog.malformed_entries)
        )
    return backlog_path, backlog_text, parsed_backlog


def summarize_markdown_section(feature_text: str, section_name: str) -> str | None:
    target = section_name.lower()
    lines = feature_text.splitlines()
    capture = False
    collected: list[str] = []

    for line in lines:
        heading = HEADING_RE.match(line)
        if heading:
            normalized = heading.group("name").strip().lower()
            if normalized == target:
                capture = True
                collected = []
                continue
            if capture:
                break

        if capture:
            stripped = line.strip()
            if stripped:
                collected.append(stripped)

    if not collected:
        return None
    summary = " ".join(collected)
    if len(summary) > 280:
        return summary[:277].rstrip() + "..."
    return summary


def feature_payload(root: Path, backlog_path: Path, entry: object, *, section_name: str, global_rank: int, section_rank: int) -> dict[str, object]:
    feature_path = (backlog_path.parent / entry.link).resolve()
    if not feature_path.exists():
        raise WorkflowError(
            f"{backlog_path.relative_to(root)} section [{section_name}] links missing feature file {entry.link}"
        )
    feature_text = feature_path.read_text(encoding="utf-8")
    tasks = parse_tasks(feature_text)
    task_counts = dict(sorted(Counter(task.status for task in tasks).items()))

    return {
        "id": entry.feature_id,
        "type": "feature",
        "section": section_name,
        "global_rank": global_rank,
        "section_rank": section_rank,
        "title": entry.title,
        "tag": entry.tag,
        "link": entry.link,
        "feature_path": str(feature_path.relative_to(root)),
        "problem": summarize_markdown_section(feature_text, "Problem"),
        "goal": summarize_markdown_section(feature_text, "Goal"),
        "scope": summarize_markdown_section(feature_text, "Scope"),
        "task_counts": task_counts,
    }


def eligible_items(root: Path) -> tuple[Path, list[dict[str, object]]]:
    backlog_path, _, parsed_backlog = read_backlog(root)
    items: list[dict[str, object]] = []
    global_rank = 1

    for section_name in ELIGIBLE_SECTIONS:
        if section_name == "BACKLOG":
            for section_rank, entry in enumerate(parsed_backlog.backlog_items, start=1):
                items.append(
                    {
                        "id": entry.backlog_id,
                        "type": "backlog_item",
                        "section": section_name,
                        "global_rank": global_rank,
                        "section_rank": section_rank,
                        "title": entry.title,
                        "tag": entry.tag,
                    }
                )
                global_rank += 1
            continue

        for section_rank, entry in enumerate(parsed_backlog.feature_sections[section_name], start=1):
            items.append(
                feature_payload(
                    root,
                    backlog_path,
                    entry,
                    section_name=section_name,
                    global_rank=global_rank,
                    section_rank=section_rank,
                )
            )
            global_rank += 1

    return backlog_path, items


def eligible_ids(parsed_backlog: object) -> list[str]:
    ids = [entry.backlog_id for entry in parsed_backlog.backlog_items]
    for section_name in ELIGIBLE_SECTIONS[1:]:
        ids.extend(entry.feature_id for entry in parsed_backlog.feature_sections[section_name])
    return ids


def entry_ids_by_section(parsed_backlog: object) -> dict[str, list[str]]:
    return {
        "BACKLOG": [entry.backlog_id for entry in parsed_backlog.backlog_items],
        "SHAPING": [entry.feature_id for entry in parsed_backlog.feature_sections["SHAPING"]],
        "READY": [entry.feature_id for entry in parsed_backlog.feature_sections["READY"]],
    }


def _entry_line_positions(lines: list[str]) -> dict[str, list[int]]:
    positions = {section: [] for section in ELIGIBLE_SECTIONS}
    current_section: str | None = None

    for index, line in enumerate(lines):
        if line.startswith("## [") and line.endswith("]"):
            section_name = line[4:-1]
            current_section = section_name if section_name in WORKFLOW_SECTIONS else None
            continue
        if current_section in positions and line.startswith("###"):
            positions[current_section].append(index)

    return positions


def reorder_backlog_text(backlog_text: str, parsed_backlog: object, ordered_ids: list[str]) -> str:
    expected_ids = eligible_ids(parsed_backlog)
    if len(set(ordered_ids)) != len(ordered_ids):
        raise WorkflowError("approved order contains duplicate item ids")
    if set(ordered_ids) != set(expected_ids):
        expected_display = ", ".join(expected_ids)
        received_display = ", ".join(ordered_ids)
        raise WorkflowError(
            "approved order must contain every eligible item exactly once "
            f"(expected: {expected_display}; received: {received_display})"
        )

    had_trailing_newline = backlog_text.endswith("\n")
    lines = backlog_text.splitlines()
    line_positions = _entry_line_positions(lines)
    section_ids = entry_ids_by_section(parsed_backlog)

    for section_name in ELIGIBLE_SECTIONS:
        existing_ids = section_ids[section_name]
        positions = line_positions[section_name]
        if len(existing_ids) != len(positions):
            raise WorkflowError(
                f"could not safely map [{section_name}] entries back to {section_name} line positions"
            )
        if not existing_ids:
            continue

        original_line_by_id = {
            item_id: lines[position] for item_id, position in zip(existing_ids, positions, strict=True)
        }
        desired_ids = [item_id for item_id in ordered_ids if item_id in original_line_by_id]
        for position, item_id in zip(positions, desired_ids, strict=True):
            lines[position] = original_line_by_id[item_id]

    rewritten = "\n".join(lines)
    if had_trailing_newline:
        rewritten += "\n"
    return rewritten


def list_command(root: Path) -> dict[str, object]:
    backlog_path, items = eligible_items(root)
    return {
        "repo_root": str(root),
        "backlog_path": str(backlog_path.relative_to(root)),
        "eligible_sections": list(ELIGIBLE_SECTIONS),
        "items": items,
    }


def apply_command(root: Path, ordered_ids: list[str]) -> dict[str, object]:
    backlog_path, backlog_text, parsed_backlog = read_backlog(root)
    rewritten = reorder_backlog_text(backlog_text, parsed_backlog, ordered_ids)
    changed = rewritten != backlog_text
    if changed:
        backlog_path.write_text(rewritten, encoding="utf-8")

    return {
        "repo_root": str(root),
        "backlog_path": str(backlog_path.relative_to(root)),
        "changed": changed,
        "eligible_sections": {
            section_name: [item_id for item_id in ordered_ids if item_id in set(section_ids)]
            for section_name, section_ids in entry_ids_by_section(parsed_backlog).items()
        },
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        root = repo_root(args.repo_root)
        if args.command == "list":
            payload = list_command(root)
        else:
            payload = apply_command(root, args.ordered_ids)
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

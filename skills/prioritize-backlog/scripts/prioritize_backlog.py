#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, load_backlog, repo_root
from _workflow.workflow_state import (
    WORKFLOW_SECTIONS,
    list_openspec_change_context_files,
    parse_feature_openspec_change,
    parse_tasks,
)


ELIGIBLE_SECTIONS = ("BACKLOG", "SHAPING", "READY")


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




def summarize_markdown_file(path: Path) -> str | None:
    collected: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        collected.append(stripped)
    if not collected:
        return None
    summary = " ".join(collected)
    if len(summary) > 280:
        return summary[:277].rstrip() + "..."
    return summary


def summarize_context_files(root: Path, context_files: list[Path]) -> tuple[str | None, str | None, str | None, list[dict[str, str]]]:
    proposal = None
    design = None
    tasks = None
    spec_context: list[dict[str, str]] = []

    for path in context_files:
        summary = summarize_markdown_file(path)
        relative_path = str(path.relative_to(root))
        if path.name == "proposal.md":
            proposal = summary
        elif path.name == "design.md":
            design = summary
        elif path.name == "tasks.md":
            tasks = summary
        else:
            spec_context.append({"path": relative_path, "summary": summary or ""})

    return proposal, design, tasks, spec_context


def feature_payload(root: Path, backlog_path: Path, entry: object, *, section_name: str, global_rank: int, section_rank: int) -> dict[str, object]:
    feature_path = (backlog_path.parent / entry.link).resolve()
    if not feature_path.exists():
        raise WorkflowError(
            f"{backlog_path.relative_to(root)} section [{section_name}] links missing feature file {entry.link}"
        )
    feature_text = feature_path.read_text(encoding="utf-8")
    tasks = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
    task_counts = dict(sorted(Counter(task.status for task in tasks).items()))
    change_id = parse_feature_openspec_change(feature_text)
    context_files = list_openspec_change_context_files(feature_text, feature_file=feature_path, repo_root=root)
    proposal, design, tasks_summary, spec_context = summarize_context_files(root, context_files)

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
        "openspec_change_id": change_id,
        "openspec_context_files": [str(path.relative_to(root)) for path in context_files],
        "proposal": proposal,
        "design": design,
        "tasks_summary": tasks_summary,
        "spec_context": spec_context,
        "task_counts": task_counts,
    }


def eligible_items(root: Path) -> tuple[Path, list[dict[str, object]]]:
    backlog_path, _, parsed_backlog = load_backlog(root)
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
    backlog_path, backlog_text, parsed_backlog = load_backlog(root)
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

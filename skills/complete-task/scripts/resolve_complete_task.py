#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.workflow_state import (
    WORKFLOW_SECTIONS,
    compute_completion_handoff,
    list_open_openspec_nested_items,
    linked_openspec_implementation_plan_path,
    list_openspec_change_context_files,
    parse_backlog_document,
    parse_feature_openspec_change,
    parse_feature_openspec_status,
    parse_tasks,
)


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
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed task resolution.")
    return parser.parse_args(argv)


def read_backlog(root: Path):
    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        raise WorkflowError("docs/planning/current_version is missing")
    if not current_version.is_symlink():
        raise WorkflowError("docs/planning/current_version is not a symlink")

    version_root = current_version.resolve()
    backlog_path = version_root / "BACKLOG.md"
    if not backlog_path.exists():
        raise WorkflowError(f"{backlog_path.relative_to(root)} is missing")

    parsed_backlog = parse_backlog_document(backlog_path.read_text(encoding="utf-8"))
    if parsed_backlog.malformed_entries:
        raise WorkflowError(
            "; ".join(f"{backlog_path.relative_to(root)} {message}" for message in parsed_backlog.malformed_entries)
        )
    return backlog_path, parsed_backlog


def resolve_active_task(root: Path) -> dict[str, object]:
    backlog_path, parsed_backlog = read_backlog(root)
    active_payloads: list[dict[str, object]] = []

    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_id = entry.feature_id
            feature_path = (backlog_path.parent / entry.link).resolve()
            if not feature_path.exists():
                raise WorkflowError(
                    f"{backlog_path.relative_to(root)} section [{section_name}] links missing feature file {entry.link}"
                )
            feature_text = feature_path.read_text(encoding="utf-8")
            if section_name == "DONE" and parse_feature_openspec_status(feature_text) == "legacy-exempt":
                # Historical completed features do not participate in active task resolution.
                continue
            change_id = parse_feature_openspec_change(feature_text)
            if change_id is None:
                raise WorkflowError(f"{feature_path.relative_to(root)} is missing OpenSpec Change metadata")
            change_path = root / "openspec" / "changes" / change_id
            context_files = list_openspec_change_context_files(
                feature_text,
                feature_file=feature_path,
                repo_root=root,
            )

            for task in parse_tasks(feature_text, feature_file=feature_path, repo_root=root):
                if task.status != "in_progress":
                    continue
                open_nested_item_ids = list_open_openspec_nested_items(
                    feature_text,
                    task.task_id,
                    feature_file=feature_path,
                    repo_root=root,
                )
                if open_nested_item_ids:
                    raise WorkflowError(
                        f"task {task.task_id} has open nested checklist items: " + ", ".join(open_nested_item_ids)
                    )
                implementation_plan_path = linked_openspec_implementation_plan_path(
                    feature_text,
                    task.task_id,
                    feature_file=feature_path,
                    repo_root=root,
                )
                if implementation_plan_path is None or not implementation_plan_path.exists():
                    relative_plan_path = (
                        str(implementation_plan_path.relative_to(root))
                        if implementation_plan_path is not None
                        else f"openspec/changes/{change_id}/implementation-plans/{task.task_id}.md"
                    )
                    raise WorkflowError(
                        "task implementation plan is missing: "
                        f"{relative_plan_path}. Write or update the implementation plan before completing the task."
                    )
                context_files = list_openspec_change_context_files(
                    feature_text,
                    task_id=task.task_id,
                    feature_file=feature_path,
                    repo_root=root,
                )
                active_payloads.append(
                    {
                        "feature_id": feature_id,
                        "feature_path": str(feature_path.relative_to(root)),
                        "feature_section": section_name,
                        "completion_handoff": asdict(
                            compute_completion_handoff(
                                feature_text,
                                task.task_id,
                                feature_file=feature_path,
                                repo_root=root,
                            )
                        ),
                        "openspec_change_id": change_id,
                        "openspec_change_path": str(change_path.relative_to(root)),
                        "implementation_plan_path": (
                            str(implementation_plan_path.relative_to(root))
                            if implementation_plan_path is not None
                            else None
                        ),
                        "openspec_context_files": [str(path.relative_to(root)) for path in context_files],
                        "execution_instruction": "Read the files listed as context before completing the task.",
                        "task_id": task.task_id,
                        "task_title": task.task_title,
                    }
                )

    if not active_payloads:
        raise WorkflowError("repository has no task with status `in_progress`")
    if len(active_payloads) > 1:
        raise WorkflowError("repository has multiple tasks with status `in_progress`")
    return active_payloads[0]


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = resolve_active_task(repo_root(args.repo_root))
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

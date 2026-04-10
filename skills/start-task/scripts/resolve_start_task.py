#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
    WorkflowStateError,
    ensure_clean_feature_worktree_for_handoff,
    linked_openspec_implementation_plan_path,
    list_openspec_change_context_files,
    parse_backlog_document,
    parse_tasks,
    validate_implementation_plan_file,
    validate_active_feature_execution,
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


def _list_git_worktree_roots(root: Path) -> list[Path]:
    resolved = subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if resolved.returncode != 0:
        return []

    worktree_roots: list[Path] = []
    for line in resolved.stdout.splitlines():
        if not line.startswith("worktree "):
            continue
        worktree_roots.append(Path(line.removeprefix("worktree ")).resolve())
    return worktree_roots


def _resolve_task_in_root(root: Path) -> dict[str, object]:
    backlog_path, parsed_backlog = read_backlog(root)
    feature_tasks: dict[tuple[str, str], tuple[Path, str, list[object]]] = {}
    active_tasks = 0

    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_id = entry.feature_id
            link = entry.link
            feature_path = (backlog_path.parent / link).resolve()
            if not feature_path.exists():
                raise WorkflowError(
                    f"{backlog_path.relative_to(root)} section [{section_name}] links missing feature file {link}"
                )
            feature_text = feature_path.read_text(encoding="utf-8")
            tasks = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
            active_tasks += sum(1 for task in tasks if task.status == "in_progress")
            feature_tasks[(section_name, feature_id)] = (feature_path, feature_text, tasks)

    if active_tasks:
        raise WorkflowError("repository already has a task with status `in_progress`")

    for section_name in ("IN_PROGRESS", "READY"):
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_id = entry.feature_id
            feature_path, feature_text, tasks = feature_tasks[(section_name, feature_id)]
            try:
                change_id, active_change_dir = validate_active_feature_execution(
                    feature_text,
                    feature_file=feature_path,
                    repo_root=root,
                )
            except WorkflowStateError as exc:
                raise WorkflowError(str(exc)) from exc
            for task in tasks:
                if task.status != "ready":
                    continue
                if section_name == "IN_PROGRESS":
                    try:
                        ensure_clean_feature_worktree_for_handoff(root, feature_id)
                    except WorkflowStateError as exc:
                        raise WorkflowError(str(exc)) from exc
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
                        f"{relative_plan_path}. Write or update the implementation plan before executing the task."
                    )
                try:
                    validate_implementation_plan_file(implementation_plan_path)
                except ValueError as exc:
                    raise WorkflowError(f"task implementation plan is invalid: {exc}") from exc
                context_files = list_openspec_change_context_files(
                    feature_text,
                    task_id=task.task_id,
                    feature_file=feature_path,
                    repo_root=root,
                )
                return {
                    "feature_id": feature_id,
                    "feature_path": str(feature_path.relative_to(root)),
                    "feature_section": section_name,
                    "selected_repo_root": str(root),
                    "openspec_change_id": change_id,
                    "openspec_change_path": str(active_change_dir.relative_to(root)),
                    "implementation_plan_path": (
                        str(implementation_plan_path.relative_to(root)) if implementation_plan_path is not None else None
                    ),
                    "openspec_context_files": [str(path.relative_to(root)) for path in context_files],
                    "execution_instruction": (
                        "Read the files listed as context, then write or update the implementation plan at the "
                        "provided path before executing the task. Record validation evidence during execution as "
                        "planned proof steps complete."
                    ),
                    "task_id": task.task_id,
                    "task_title": task.task_title,
                }

    raise WorkflowError("no startable task found in [IN_PROGRESS] or [READY]")


def resolve_task(root: Path) -> dict[str, object]:
    current_payload: dict[str, object] | None = None
    current_error: WorkflowError | None = None

    try:
        current_payload = _resolve_task_in_root(root)
    except WorkflowError as exc:
        current_error = exc

    if current_payload is not None and current_payload["feature_section"] == "IN_PROGRESS":
        return current_payload

    candidate_payloads: list[dict[str, object]] = []
    for worktree_root in _list_git_worktree_roots(root):
        if worktree_root == root:
            continue
        try:
            candidate_payloads.append(_resolve_task_in_root(worktree_root))
        except WorkflowError as exc:
            if "uncommitted handoff changes" in str(exc):
                raise
            continue

    in_progress_candidates = [payload for payload in candidate_payloads if payload["feature_section"] == "IN_PROGRESS"]
    if len(in_progress_candidates) == 1:
        return in_progress_candidates[0]
    if len(in_progress_candidates) > 1:
        raise WorkflowError("multiple feature worktrees report startable tasks from [IN_PROGRESS]")

    if current_payload is not None:
        return current_payload
    if len(candidate_payloads) == 1:
        return candidate_payloads[0]
    if len(candidate_payloads) > 1:
        raise WorkflowError("multiple worktrees report startable tasks; re-run from the intended checkout")
    if current_error is not None:
        raise current_error
    raise WorkflowError("no startable task found in the current checkout or any feature worktree")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = resolve_task(repo_root(args.repo_root))
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

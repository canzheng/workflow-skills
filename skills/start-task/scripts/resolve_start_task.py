#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, load_backlog, repo_root
from _workflow.workflow_state import (
    WORKFLOW_SECTIONS,
    WorkflowStateError,
    ensure_clean_feature_worktree_for_handoff,
    infer_selected_feature_id,
    is_primary_checkout,
    latest_review_verdict,
    linked_openspec_implementation_plan_path,
    list_git_worktree_roots,
    list_openspec_change_context_files,
    parse_tasks,
    validate_implementation_plan_file,
    validate_active_feature_execution,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed task resolution.")
    parser.add_argument(
        "--feature-id",
        help=(
            "Optional fast path: skip BACKLOG-wide scanning and the cross-worktree fanout, "
            "and validate only the named feature/task. Must be paired with --task-id."
        ),
    )
    parser.add_argument(
        "--task-id",
        help=(
            "Optional fast path: skip BACKLOG-wide scanning and the cross-worktree fanout, "
            "and validate only the named feature/task. Must be paired with --feature-id."
        ),
    )
    args = parser.parse_args(argv)
    if (args.feature_id is None) != (args.task_id is None):
        parser.error("--feature-id and --task-id must be supplied together")
    return args


def _resolve_task_in_root(root: Path, *, selected_feature_id: str | None = None) -> dict[str, object]:
    backlog_path, _backlog_text, parsed_backlog = load_backlog(root)
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
            if selected_feature_id is not None and feature_id != selected_feature_id:
                continue
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
                if implementation_plan_path is None:
                    relative_plan_path = (
                        f"openspec/changes/{change_id}/implementation-plans/{task.task_id}.md"
                    )
                    implementation_plan_status = "missing"
                elif not implementation_plan_path.exists():
                    relative_plan_path = str(implementation_plan_path.relative_to(root))
                    implementation_plan_status = "missing"
                else:
                    relative_plan_path = str(implementation_plan_path.relative_to(root))
                    try:
                        validate_implementation_plan_file(implementation_plan_path)
                    except ValueError as exc:
                        raise WorkflowError(f"task implementation plan is invalid: {exc}") from exc
                    implementation_plan_status = "present"
                context_files = list_openspec_change_context_files(
                    feature_text,
                    task_id=task.task_id,
                    feature_file=feature_path,
                    repo_root=root,
                )
                ready_review_verdict = latest_review_verdict(
                    feature_text,
                    scope="ready",
                    target=feature_id,
                )
                return {
                    "feature_id": feature_id,
                    "feature_path": str(feature_path.relative_to(root)),
                    "feature_section": section_name,
                    "selected_repo_root": str(root),
                    "openspec_change_id": change_id,
                    "openspec_change_path": str(active_change_dir.relative_to(root)),
                    "implementation_plan_path": relative_plan_path,
                    "implementation_plan_status": implementation_plan_status,
                    "openspec_context_files": [str(path.relative_to(root)) for path in context_files],
                    "ready_review_verdict": (
                        {
                            "scope": ready_review_verdict.scope,
                            "target": ready_review_verdict.target,
                            "verdict": ready_review_verdict.verdict,
                            "blocking_findings": list(ready_review_verdict.blocking_findings),
                            "terminal": ready_review_verdict.terminal,
                        }
                        if ready_review_verdict is not None
                        else None
                    ),
                    "execution_instruction": (
                        "Create or re-enter the feature worktree FIRST. Only after the worktree exists, "
                        "from inside that worktree, read the listed context files, retrieve lessons, and "
                        "draft (if status=missing) or update (if status=present) the implementation plan "
                        "at the provided path. Do not retrieve lessons or write the plan in the primary "
                        "checkout. Record validation evidence during execution as planned proof steps complete."
                    ),
                    "task_id": task.task_id,
                    "task_title": task.task_title,
                }

    raise WorkflowError("no startable task found in [IN_PROGRESS] or [READY]")


def resolve_named_task(root: Path, feature_id: str, task_id: str) -> dict[str, object]:
    """Fast path: validate and return a payload for the explicitly named (feature_id, task_id).

    Skips the BACKLOG-wide scan and cross-worktree fanout used by `resolve_task`.
    Performs the same per-task validation: feature is in [IN_PROGRESS] or [READY],
    task exists with status `ready`, implementation plan exists and is valid.
    Asserts no other task is `in_progress` so the global invariant is preserved.
    """
    backlog_path, _backlog_text, parsed_backlog = load_backlog(root)
    matching_entry = None
    matching_section: str | None = None
    active_tasks = 0
    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_path = (backlog_path.parent / entry.link).resolve()
            if not feature_path.exists():
                raise WorkflowError(
                    f"{backlog_path.relative_to(root)} section [{section_name}] links missing feature file {entry.link}"
                )
            feature_text = feature_path.read_text(encoding="utf-8")
            tasks = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
            active_tasks += sum(1 for task in tasks if task.status == "in_progress")
            if entry.feature_id == feature_id and matching_entry is None:
                matching_entry = entry
                matching_section = section_name

    if active_tasks:
        raise WorkflowError("repository already has a task with status `in_progress`")
    if matching_entry is None or matching_section is None:
        raise WorkflowError(f"feature {feature_id} not found in active backlog")
    if matching_section not in {"IN_PROGRESS", "READY"}:
        raise WorkflowError(
            f"feature {feature_id} is in [{matching_section}], expected [IN_PROGRESS] or [READY]"
        )

    feature_path = (backlog_path.parent / matching_entry.link).resolve()
    feature_text = feature_path.read_text(encoding="utf-8")
    try:
        change_id, active_change_dir = validate_active_feature_execution(
            feature_text,
            feature_file=feature_path,
            repo_root=root,
        )
    except WorkflowStateError as exc:
        raise WorkflowError(str(exc)) from exc

    matching_task = None
    for task in parse_tasks(feature_text, feature_file=feature_path, repo_root=root):
        if task.task_id == task_id:
            matching_task = task
            break
    if matching_task is None:
        raise WorkflowError(f"task {task_id} not found in feature {feature_id}")
    if matching_task.status != "ready":
        raise WorkflowError(
            f"task {task_id} in feature {feature_id} has status `{matching_task.status}`, expected `ready`"
        )

    if matching_section == "IN_PROGRESS":
        try:
            ensure_clean_feature_worktree_for_handoff(root, feature_id)
        except WorkflowStateError as exc:
            raise WorkflowError(str(exc)) from exc

    implementation_plan_path = linked_openspec_implementation_plan_path(
        feature_text,
        matching_task.task_id,
        feature_file=feature_path,
        repo_root=root,
    )
    if implementation_plan_path is None:
        relative_plan_path = (
            f"openspec/changes/{change_id}/implementation-plans/{matching_task.task_id}.md"
        )
        implementation_plan_status = "missing"
    elif not implementation_plan_path.exists():
        relative_plan_path = str(implementation_plan_path.relative_to(root))
        implementation_plan_status = "missing"
    else:
        relative_plan_path = str(implementation_plan_path.relative_to(root))
        try:
            validate_implementation_plan_file(implementation_plan_path)
        except ValueError as exc:
            raise WorkflowError(f"task implementation plan is invalid: {exc}") from exc
        implementation_plan_status = "present"
    context_files = list_openspec_change_context_files(
        feature_text,
        task_id=matching_task.task_id,
        feature_file=feature_path,
        repo_root=root,
    )
    ready_review_verdict = latest_review_verdict(
        feature_text,
        scope="ready",
        target=feature_id,
    )
    return {
        "feature_id": feature_id,
        "feature_path": str(feature_path.relative_to(root)),
        "feature_section": matching_section,
        "selected_repo_root": str(root.resolve()),
        "openspec_change_id": change_id,
        "openspec_change_path": str(active_change_dir.relative_to(root)),
        "implementation_plan_path": relative_plan_path,
        "implementation_plan_status": implementation_plan_status,
        "openspec_context_files": [str(path.relative_to(root)) for path in context_files],
        "ready_review_verdict": (
            {
                "scope": ready_review_verdict.scope,
                "target": ready_review_verdict.target,
                "verdict": ready_review_verdict.verdict,
                "blocking_findings": list(ready_review_verdict.blocking_findings),
                "terminal": ready_review_verdict.terminal,
            }
            if ready_review_verdict is not None
            else None
        ),
        "execution_instruction": (
            "Create or re-enter the feature worktree FIRST. Only after the worktree exists, "
            "from inside that worktree, read the listed context files, retrieve lessons, and "
            "draft (if status=missing) or update (if status=present) the implementation plan "
            "at the provided path. Do not retrieve lessons or write the plan in the primary "
            "checkout. Record validation evidence during execution as planned proof steps complete."
        ),
        "task_id": matching_task.task_id,
        "task_title": matching_task.task_title,
    }


def resolve_task(root: Path) -> dict[str, object]:
    current_payload: dict[str, object] | None = None
    current_error: WorkflowError | None = None
    current_selected_feature_id = None if is_primary_checkout(root) else infer_selected_feature_id(root)

    try:
        current_payload = _resolve_task_in_root(root, selected_feature_id=current_selected_feature_id)
    except WorkflowError as exc:
        current_error = exc

    if current_payload is not None and current_payload["feature_section"] == "IN_PROGRESS":
        return current_payload

    candidate_payloads: list[dict[str, object]] = []
    for worktree_root in list_git_worktree_roots(root):
        if worktree_root == root:
            continue
        try:
            selected_feature_id = None if is_primary_checkout(worktree_root) else infer_selected_feature_id(worktree_root)
            candidate_payloads.append(
                _resolve_task_in_root(worktree_root, selected_feature_id=selected_feature_id)
            )
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
        root = repo_root(args.repo_root)
        if args.feature_id is not None and args.task_id is not None:
            payload = resolve_named_task(root, args.feature_id, args.task_id)
        else:
            payload = resolve_task(root)
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

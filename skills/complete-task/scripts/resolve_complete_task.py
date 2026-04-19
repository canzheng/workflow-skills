#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
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
    compute_completion_handoff,
    infer_selected_feature_id,
    is_primary_checkout,
    list_open_openspec_nested_items,
    list_git_worktree_roots,
    linked_openspec_implementation_plan_path,
    list_openspec_change_context_files,
    parse_feature_openspec_change,
    parse_feature_openspec_status,
    parse_tasks,
    collect_task_validation_evidence,
    required_validation_evidence_categories_for_plan,
    validate_implementation_plan_file,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed task resolution.")
    return parser.parse_args(argv)


def resolve_active_task(root: Path, *, selected_feature_id: str | None = None) -> dict[str, object]:
    backlog_path, _backlog_text, parsed_backlog = load_backlog(root)
    active_payloads: list[dict[str, object]] = []

    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_id = entry.feature_id
            if selected_feature_id is not None and feature_id != selected_feature_id:
                continue
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
            feature_label = str(feature_path.relative_to(root))
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
                try:
                    plan_summary = validate_implementation_plan_file(implementation_plan_path)
                except ValueError as exc:
                    raise WorkflowError(f"task implementation plan is invalid: {exc}") from exc
                evidence_summary = collect_task_validation_evidence(feature_text, task.task_id)
                if not evidence_summary.evidence_categories:
                    raise WorkflowError(
                        "task completion evidence is missing categorized proof: "
                        f"{feature_label} task {task.task_id} must record categorized evidence in Validation Log"
                    )
                required_evidence_categories = required_validation_evidence_categories_for_plan(plan_summary)
                if not set(evidence_summary.evidence_categories).intersection(required_evidence_categories):
                    raise WorkflowError(
                        "task completion evidence does not satisfy declared proof obligations: "
                        f"{feature_label} task {task.task_id} needs one of "
                        f"{', '.join(required_evidence_categories)}, got "
                        f"{', '.join(evidence_summary.evidence_categories)}"
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


def resolve_active_task_across_worktrees(root: Path) -> dict[str, object]:
    current_payload: dict[str, object] | None = None
    current_error: WorkflowError | None = None
    current_selected_feature_id = None if is_primary_checkout(root) else infer_selected_feature_id(root)

    try:
        current_payload = resolve_active_task(root, selected_feature_id=current_selected_feature_id)
    except WorkflowError as exc:
        current_error = exc

    candidate_payloads: list[dict[str, object]] = []
    for worktree_root in list_git_worktree_roots(root):
        if worktree_root == root:
            continue
        try:
            selected_feature_id = None if is_primary_checkout(worktree_root) else infer_selected_feature_id(worktree_root)
            candidate_payload = resolve_active_task(worktree_root, selected_feature_id=selected_feature_id)
        except WorkflowError:
            continue
        candidate_payloads.append(
            {
                **candidate_payload,
                "selected_repo_root": str(worktree_root.resolve()),
            }
        )

    feature_worktree_candidates = [
        payload for payload in candidate_payloads if not is_primary_checkout(Path(payload["selected_repo_root"]))
    ]
    if len(feature_worktree_candidates) == 1:
        return feature_worktree_candidates[0]
    if len(feature_worktree_candidates) > 1:
        raise WorkflowError("multiple feature worktrees report active tasks; re-run from the intended checkout")

    if current_payload is not None:
        return {
            **current_payload,
            "selected_repo_root": str(root.resolve()),
        }
    if len(candidate_payloads) == 1:
        return candidate_payloads[0]
    if len(candidate_payloads) > 1:
        raise WorkflowError("multiple worktrees report active tasks; re-run from the intended checkout")
    if current_error is not None:
        raise current_error
    raise WorkflowError("repository has no task with status `in_progress`")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = resolve_active_task_across_worktrees(repo_root(args.repo_root))
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

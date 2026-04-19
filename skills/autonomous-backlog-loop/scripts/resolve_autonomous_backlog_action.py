#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, load_backlog, repo_root
from _workflow.workflow_state import (
    WORKFLOW_SECTIONS,
    ensure_clean_feature_worktree_for_handoff,
    parse_tasks,
    resolve_feature_repo_root,
    validate_active_feature_execution,
    WorkflowStateError,
)


@dataclass(frozen=True)
class FeatureRecord:
    feature_id: str
    feature_path: Path
    feature_section: str
    feature_text: str
    tasks: list[object]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed workflow checks.")
    parser.add_argument("--feature-id", help="Resolve the next ready task for only this feature.")
    parser.add_argument(
        "--design-mode",
        action="store_true",
        help="Ignore READY and IN_PROGRESS features and resolve only shaping/backlog design work.",
    )
    parser.add_argument("--completed-count", type=int, default=0, help="Completed-feature count for this run.")
    parser.add_argument("--completion-limit", type=int, help="Stop once completed-count reaches this limit.")
    return parser.parse_args(argv)


def read_backlog(root: Path) -> tuple[Path, dict[str, list[FeatureRecord]], list[dict[str, object]]]:
    backlog_path, _backlog_text, parsed_backlog = load_backlog(root)
    feature_sections: dict[str, list[FeatureRecord]] = {name: [] for name in WORKFLOW_SECTIONS}

    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections[section_name]:
            feature_id = entry.feature_id
            link = entry.link
            feature_path = (backlog_path.parent / link).resolve()
            if not feature_path.exists():
                raise WorkflowError(
                    f"{backlog_path.relative_to(root)} section [{section_name}] links missing feature file {link}"
                )
            feature_text = feature_path.read_text(encoding="utf-8")
            feature_sections[section_name].append(
                FeatureRecord(
                    feature_id=feature_id,
                    feature_path=feature_path,
                    feature_section=section_name,
                    feature_text=feature_text,
                    tasks=parse_tasks(
                        feature_text,
                        feature_file=feature_path,
                        repo_root=root,
                    ),
                )
            )

    backlog_items = [
        {
            "backlog_id": item.backlog_id,
            "backlog_index": item.backlog_index,
            "backlog_title": item.title,
        }
        for item in parsed_backlog.backlog_items
    ]
    return backlog_path, feature_sections, backlog_items


def first_ready_task(tasks: list[object]):
    for task in tasks:
        if task.status == "ready":
            return task
    return None


def validated_first_ready_task(root: Path, feature: FeatureRecord):
    try:
        validate_active_feature_execution(
            feature.feature_text,
            feature_file=feature.feature_path,
            repo_root=root,
        )
        task = first_ready_task(feature.tasks)
        if task is not None and feature.feature_section == "IN_PROGRESS":
            ensure_clean_feature_worktree_for_handoff(root, feature.feature_id)
    except WorkflowStateError as exc:
        raise WorkflowError(str(exc)) from exc
    return task


def build_task_payload(root: Path, feature: FeatureRecord, task) -> dict[str, str]:
    return {
        "action": "run_task_loop",
        "feature_id": feature.feature_id,
        "feature_path": str(feature.feature_path.relative_to(root)),
        "feature_section": feature.feature_section,
        "task_id": task.task_id,
        "task_title": task.task_title,
    }


def build_feature_payload(root: Path, action: str, feature: FeatureRecord) -> dict[str, str]:
    return {
        "action": action,
        "feature_id": feature.feature_id,
        "feature_path": str(feature.feature_path.relative_to(root)),
        "feature_section": feature.feature_section,
    }


def resolve_action(
    root: Path,
    *,
    feature_id: str | None,
    design_mode: bool,
    completed_count: int,
    completion_limit: int | None,
) -> dict[str, object]:
    if completed_count < 0:
        raise WorkflowError("--completed-count must be >= 0")
    if completion_limit is not None and completion_limit < 0:
        raise WorkflowError("--completion-limit must be >= 0")
    if completion_limit is not None and completed_count >= completion_limit:
        return {
            "action": "stop",
            "reason": "completion_limit_reached",
        }

    _backlog_path, feature_sections, backlog_items = read_backlog(root)
    all_features = [feature for section_name in WORKFLOW_SECTIONS[1:] for feature in feature_sections[section_name]]
    active_tasks = sum(task.status == "in_progress" for feature in all_features for task in feature.tasks)
    if active_tasks:
        raise WorkflowError("repository already has a task with status `in_progress`")

    for section_name in ("IN_PROGRESS", "READY"):
        for feature in feature_sections[section_name]:
            validated_first_ready_task(root, feature)

    if feature_id is not None:
        for feature in all_features:
            if feature.feature_id != feature_id:
                continue
            task = first_ready_task(feature.tasks)
            if task is None:
                return build_feature_payload(root, "feature_exhausted", feature)
            return build_task_payload(root, feature, task)
        raise WorkflowError(f"feature {feature_id} not found in active backlog")

    if not design_mode:
        for section_name in ("IN_PROGRESS", "READY"):
            for feature in feature_sections[section_name]:
                task = validated_first_ready_task(root, feature)
                if task is not None:
                    return build_task_payload(root, feature, task)

    for feature in feature_sections["SHAPING"]:
        return build_feature_payload(root, "ready_feature", feature)

    if backlog_items:
        return {
            "action": "shape_backlog_item",
            "backlog_index": backlog_items[0]["backlog_index"],
            "backlog_title": backlog_items[0]["backlog_title"],
        }

    if design_mode:
        return {
            "action": "feature_exhausted",
            "reason": "design_mode_no_design_work",
        }

    return {
        "action": "stop",
        "reason": "no_eligible_work",
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        root = repo_root(args.repo_root)
        if args.feature_id is not None:
            try:
                root = resolve_feature_repo_root(root, args.feature_id)
            except WorkflowStateError as exc:
                raise WorkflowError(str(exc)) from exc
        payload = resolve_action(
            root,
            feature_id=args.feature_id,
            design_mode=args.design_mode,
            completed_count=args.completed_count,
            completion_limit=args.completion_limit,
        )
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

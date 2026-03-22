#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.workflow_state import WORKFLOW_SECTIONS, parse_backlog_document, parse_tasks


class WorkflowError(RuntimeError):
    pass


@dataclass(frozen=True)
class FeatureRecord:
    feature_id: str
    feature_path: Path
    feature_section: str
    tasks: list[object]


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
            feature_sections[section_name].append(
                FeatureRecord(
                    feature_id=feature_id,
                    feature_path=feature_path,
                    feature_section=section_name,
                    tasks=parse_tasks(feature_path.read_text(encoding="utf-8")),
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
                task = first_ready_task(feature.tasks)
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
        payload = resolve_action(
            repo_root(args.repo_root),
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

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.workflow_state import (
    WORKFLOW_SECTIONS,
    collect_openspec_change_linkage,
    compute_task_readiness_drift,
    find_backlog_section_order_errors,
    find_legacy_inline_planning_sections,
    parse_backlog_document,
    parse_current_task,
    parse_feature_openspec_change,
    parse_feature_openspec_status,
    parse_tasks,
    validate_promoted_feature_openspec_specs,
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
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed diagnosis.")
    return parser.parse_args(argv)


def add_finding(
    findings: list[dict[str, object]],
    *,
    severity: str,
    code: str,
    message: str,
    path: str | None = None,
    feature_id: str | None = None,
    section: str | None = None,
    details: dict[str, object] | None = None,
) -> None:
    finding: dict[str, object] = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if path is not None:
        finding["path"] = path
    if feature_id is not None:
        finding["feature_id"] = feature_id
    if section is not None:
        finding["section"] = section
    if details:
        finding["details"] = details
    findings.append(finding)


def _feature_summary(
    root: Path,
    section_name: str,
    feature_id: str,
    feature_path: Path,
    feature_text: str,
    findings: list[dict[str, object]],
) -> dict[str, object]:
    relative_path = str(feature_path.relative_to(root))
    change_id = parse_feature_openspec_change(feature_text)
    openspec_status = parse_feature_openspec_status(feature_text)
    current_task = None
    task_records = []
    invalid_current_task_error: str | None = None
    try:
        current_task = parse_current_task(feature_text)
        task_records = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
    except ValueError as exc:
        invalid_current_task_error = str(exc)
        add_finding(
            findings,
            severity="error",
            code="invalid_current_task_metadata",
            message=invalid_current_task_error,
            path=relative_path,
            feature_id=feature_id,
            section=section_name,
        )
    task_counts = dict(sorted(Counter(task.status for task in task_records).items()))
    active_task_ids = [task.task_id for task in task_records if task.status == "in_progress"]

    legacy_inline_sections = find_legacy_inline_planning_sections(feature_text)
    if legacy_inline_sections and openspec_status != "legacy-exempt":
        add_finding(
            findings,
            severity="error",
            code="legacy_inline_planning_sections",
            message="feature uses legacy inline planning sections",
            path=relative_path,
            feature_id=feature_id,
            section=section_name,
            details={"sections": legacy_inline_sections},
        )

    for specs_error in validate_promoted_feature_openspec_specs(feature_text, section_name=section_name):
        add_finding(
            findings,
            severity="error",
            code="missing_openspec_specs",
            message=specs_error,
            path=relative_path,
            feature_id=feature_id,
            section=section_name,
        )

    if section_name in {"SHAPING", "READY", "IN_PROGRESS", "DEFER"}:
        if change_id is None:
            add_finding(
                findings,
                severity="error",
                code="missing_openspec_change",
                message="feature is missing OpenSpec Change metadata",
                path=relative_path,
                feature_id=feature_id,
                section=section_name,
            )
        else:
            change_dir = root / "openspec" / "changes" / change_id
            if not change_dir.exists():
                add_finding(
                    findings,
                    severity="error",
                    code="linked_openspec_change_missing",
                    message=f"linked OpenSpec change openspec/changes/{change_id} is missing",
                    path=relative_path,
                    feature_id=feature_id,
                    section=section_name,
                )
            if section_name in {"SHAPING", "READY"}:
                for required_name in ("proposal.md", "design.md", "tasks.md"):
                    if not (change_dir / required_name).exists():
                        add_finding(
                            findings,
                            severity="error",
                            code="missing_shaping_artifact" if section_name == "SHAPING" else "missing_ready_artifact",
                            message=f"linked OpenSpec change is missing {required_name}",
                            path=relative_path,
                            feature_id=feature_id,
                            section=section_name,
                            details={"required_file": required_name},
                        )
    elif section_name == "DONE":
        if openspec_status == "legacy-exempt":
            if change_id is not None:
                add_finding(
                    findings,
                    severity="error",
                    code="legacy_exempt_with_change",
                    message="legacy-exempt completed feature should not still record an OpenSpec Change",
                    path=relative_path,
                    feature_id=feature_id,
                    section=section_name,
                )
        elif change_id is None:
            add_finding(
                findings,
                severity="error",
                code="missing_openspec_change",
                message="completed feature has neither archived OpenSpec change metadata nor OpenSpec Status legacy-exempt",
                path=relative_path,
                feature_id=feature_id,
                section=section_name,
            )
        else:
            active_change_dir = root / "openspec" / "changes" / change_id
            archive_matches = sorted((root / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))
            if active_change_dir.exists():
                add_finding(
                    findings,
                    severity="error",
                    code="done_feature_change_still_active",
                    message=f"completed feature still has active OpenSpec change openspec/changes/{change_id}",
                    path=relative_path,
                    feature_id=feature_id,
                    section=section_name,
                )
            if len(archive_matches) != 1:
                add_finding(
                    findings,
                    severity="error",
                    code="done_feature_archive_missing_or_ambiguous",
                    message="completed feature does not resolve to exactly one archived OpenSpec change",
                    path=relative_path,
                    feature_id=feature_id,
                    section=section_name,
                    details={"change_id": change_id, "archive_matches": [str(path.relative_to(root)) for path in archive_matches]},
                )

    if section_name == "READY" and "ready" not in task_counts:
        add_finding(
            findings,
            severity="error",
            code="no_ready_task",
            message="feature is in [READY] but has no task with status ready",
            path=relative_path,
            feature_id=feature_id,
            section=section_name,
        )

    if invalid_current_task_error is None:
        readiness_drift = compute_task_readiness_drift(feature_text, feature_file=feature_path, repo_root=root)
        if readiness_drift.promotable_task_ids or readiness_drift.invalid_ready_task_ids or readiness_drift.unknown_dependency_errors:
            add_finding(
                findings,
                severity="error",
                code="task_readiness_drift",
                message="feature has workflow-derived task readiness drift",
                path=relative_path,
                feature_id=feature_id,
                section=section_name,
                details={
                    "promotable_task_ids": readiness_drift.promotable_task_ids,
                    "invalid_ready_task_ids": readiness_drift.invalid_ready_task_ids,
                    "unknown_dependency_errors": readiness_drift.unknown_dependency_errors,
                },
            )

    return {
        "feature_id": feature_id,
        "section": section_name,
        "feature_path": relative_path,
        "openspec_change_id": change_id,
        "openspec_status": openspec_status,
        "current_task": current_task,
        "active_task_ids": active_task_ids,
        "task_counts": task_counts,
    }


def diagnose(root: Path) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    features: list[dict[str, object]] = []
    section_counts = {name: 0 for name in WORKFLOW_SECTIONS}

    current_version = root / "docs" / "planning" / "current_version"
    active_version_name: str | None = None
    backlog_relative: str | None = None
    planning_scaffold_ready_for_linkage = False

    if not current_version.exists():
        add_finding(
            findings,
            severity="error",
            code="missing_current_version",
            message="docs/planning/current_version is missing",
            path="docs/planning/current_version",
        )
    elif not current_version.is_symlink():
        add_finding(
            findings,
            severity="error",
            code="current_version_not_symlink",
            message="docs/planning/current_version is not a symlink",
            path="docs/planning/current_version",
        )
    else:
        active_version_name = current_version.resolve().name
        backlog_path = current_version.resolve() / "BACKLOG.md"
        backlog_relative = str(backlog_path.relative_to(root))
        if not backlog_path.exists():
            add_finding(
                findings,
                severity="error",
                code="missing_backlog",
                message=f"{backlog_relative} is missing",
                path=backlog_relative,
            )
        else:
            planning_scaffold_ready_for_linkage = True
            backlog_text = backlog_path.read_text(encoding="utf-8")
            parsed_backlog = parse_backlog_document(backlog_text)
            for section_error in find_backlog_section_order_errors(backlog_text):
                add_finding(
                    findings,
                    severity="error",
                    code="invalid_backlog_section_order",
                    message=section_error,
                    path=backlog_relative,
                )
            for malformed_entry in parsed_backlog.malformed_entries:
                add_finding(
                    findings,
                    severity="error",
                    code="malformed_backlog_entry",
                    message=malformed_entry,
                    path=backlog_relative,
                )
            section_counts["BACKLOG"] = len(parsed_backlog.backlog_items)
            for section_name in WORKFLOW_SECTIONS[1:]:
                entries = parsed_backlog.feature_sections.get(section_name, [])
                section_counts[section_name] = len(entries)
                for entry in entries:
                    feature_path = (backlog_path.parent / entry.link).resolve()
                    if not feature_path.exists():
                        add_finding(
                            findings,
                            severity="error",
                            code="missing_feature_file",
                            message=f"backlog entry links missing feature file {entry.link}",
                            path=backlog_relative,
                            feature_id=entry.feature_id,
                            section=section_name,
                        )
                        continue
                    features.append(
                        _feature_summary(
                            root,
                            section_name,
                            entry.feature_id,
                            feature_path,
                            feature_path.read_text(encoding="utf-8"),
                            findings,
                        )
                    )

    openspec_root = root / "openspec"
    if not openspec_root.exists():
        add_finding(
            findings,
            severity="error",
            code="missing_openspec_root",
            message="openspec is missing",
            path="openspec",
        )
    else:
        if not (openspec_root / "specs").is_dir():
            add_finding(
                findings,
                severity="error",
                code="missing_openspec_specs",
                message="openspec/specs is missing",
                path="openspec/specs",
            )
        if not (openspec_root / "changes").is_dir():
            add_finding(
                findings,
                severity="error",
                code="missing_openspec_changes",
                message="openspec/changes is missing",
                path="openspec/changes",
            )
        elif planning_scaffold_ready_for_linkage:
            linkage = collect_openspec_change_linkage(root)
            for change_id in linkage.orphan_active_change_ids:
                add_finding(
                    findings,
                    severity="error",
                    code="orphan_active_change",
                    message=f"active OpenSpec change {change_id} is not linked from any promoted feature",
                    path=f"openspec/changes/{change_id}",
                    details={"change_id": change_id},
                )

    active_tasks: list[dict[str, object]] = []
    for feature in features:
        for task_id in feature["active_task_ids"]:
            active_tasks.append(
                {
                    "feature_id": feature["feature_id"],
                    "feature_path": feature["feature_path"],
                    "task_id": task_id,
                }
            )

    if len(active_tasks) > 1:
        add_finding(
            findings,
            severity="error",
            code="multiple_in_progress_tasks",
            message="repository has multiple tasks with status in_progress",
            details={"active_tasks": active_tasks},
        )
        finding_counts = dict(sorted(Counter(finding["severity"] for finding in findings).items()))
        for severity in ("error", "warning", "info"):
            finding_counts.setdefault(severity, 0)
        status = "issues_found"
    else:
        finding_counts = dict(sorted(Counter(finding["severity"] for finding in findings).items()))
        for severity in ("error", "warning", "info"):
            finding_counts.setdefault(severity, 0)
        status = "ok" if not findings else "issues_found"

    return {
        "status": status,
        "repo_root": str(root),
        "active_version": active_version_name,
        "backlog_path": backlog_relative,
        "section_counts": section_counts,
        "feature_count": len(features),
        "active_task_count": len(active_tasks),
        "active_tasks": active_tasks,
        "features": features,
        "finding_counts": finding_counts,
        "findings": findings,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = diagnose(repo_root(args.repo_root))
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

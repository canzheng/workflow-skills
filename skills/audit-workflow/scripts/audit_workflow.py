#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, repo_root
from _workflow.workflow_state import (
    FEATURE_ID_RE,
    WORKFLOW_SECTIONS,
    collect_openspec_change_linkage,
    compute_task_readiness_drift,
    current_task_reference_error,
    find_backlog_section_order_errors,
    find_openspec_task_structure_errors,
    find_legacy_inline_planning_sections,
    format_task_readiness_drift_messages,
    list_git_worktree_roots,
    parse_backlog_document,
    validate_promoted_feature_openspec_specs,
    parse_current_task,
    parse_feature_openspec_status,
    parse_tasks,
    parse_feature_openspec_change,
)

BACKLOG_REF_RE = re.compile(r"^- Backlog Reference: `([^`]+)`$", re.MULTILINE)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed workflow checks.")
    parser.add_argument(
        "--gate",
        choices=("start", "complete"),
        help=(
            "Gate-aware in_progress check. start: assert 0 in_progress tasks. "
            "complete: assert exactly 1 in_progress task; print its feature_id and task_id on success."
        ),
    )
    parser.add_argument(
        "--include-worktrees",
        action="store_true",
        help=(
            "Walk all git worktrees and aggregate the in_progress count across them. "
            "Detects cross-worktree drift where two worktrees claim different in_progress tasks."
        ),
    )
    return parser.parse_args(argv)


def _audit_single_root(root: Path) -> tuple[list[str], list[tuple[str, str]]]:
    """Audit one checkout. Returns (errors, in_progress_records).

    in_progress_records is a list of (feature_id, task_id) tuples for tasks
    whose status is `in_progress` in this checkout's planning state.
    """
    errors: list[str] = []
    in_progress_records: list[tuple[str, str]] = []

    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        errors.append("docs/planning/current_version is missing")
        current_path = None
    else:
        if not current_version.is_symlink():
            errors.append("docs/planning/current_version is not a symlink")
        current_path = current_version.resolve()

    if current_path is None:
        return errors, in_progress_records

    openspec_root = root / "openspec"
    if not openspec_root.exists():
        errors.append("openspec is missing")
    else:
        if not (openspec_root / "specs").is_dir():
            errors.append("openspec/specs is missing")
        if not (openspec_root / "changes").is_dir():
            errors.append("openspec/changes is missing")

    backlog = current_path / "BACKLOG.md"
    if not backlog.exists():
        errors.append(f"{backlog.relative_to(root)} is missing")
        return errors, in_progress_records

    backlog_text = backlog.read_text(encoding="utf-8")
    for section_error in find_backlog_section_order_errors(backlog_text):
        errors.append(f"{backlog.relative_to(root)} {section_error}")

    version = current_path.name
    parsed_backlog = parse_backlog_document(backlog_text)
    for malformed_entry in parsed_backlog.malformed_entries:
        errors.append(f"{backlog.relative_to(root)} {malformed_entry}")

    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_id = entry.feature_id
            link = entry.link
            feature_path = (backlog.parent / link).resolve()
            if not feature_path.exists():
                errors.append(
                    f"{backlog.relative_to(root)} section [{section_name}] links missing feature file {link}"
                )
                continue

            feature_text = feature_path.read_text(encoding="utf-8")

            feature_id_match = FEATURE_ID_RE.search(feature_text)
            if not feature_id_match:
                errors.append(f"{feature_path.relative_to(root)} is missing Feature ID metadata")
            elif feature_id_match.group(1) != feature_id:
                errors.append(
                    f"{feature_path.relative_to(root)} has Feature ID {feature_id_match.group(1)}, expected {feature_id}"
                )

            backlog_ref_match = BACKLOG_REF_RE.search(feature_text)
            expected_anchor = f"docs/planning/versions/{version}/BACKLOG.md#{section_name.lower()}"
            if not backlog_ref_match:
                errors.append(f"{feature_path.relative_to(root)} is missing Backlog Reference metadata")
            elif backlog_ref_match.group(1) != expected_anchor:
                errors.append(
                    f"{feature_path.relative_to(root)} has Backlog Reference {backlog_ref_match.group(1)}, expected {expected_anchor}"
                )

            change_id = parse_feature_openspec_change(feature_text)
            openspec_status = parse_feature_openspec_status(feature_text)
            legacy_inline_sections = find_legacy_inline_planning_sections(feature_text)

            if legacy_inline_sections and openspec_status != "legacy-exempt":
                errors.append(
                    f"{feature_path.relative_to(root)} uses legacy inline planning sections: "
                    + ", ".join(legacy_inline_sections)
                )

            for specs_error in validate_promoted_feature_openspec_specs(feature_text, section_name=section_name):
                if specs_error == "feature is missing OpenSpec Specs metadata":
                    errors.append(f"{feature_path.relative_to(root)} is missing OpenSpec Specs metadata")
                else:
                    errors.append(f"{feature_path.relative_to(root)} {specs_error}")

            if section_name in {"SHAPING", "READY", "IN_PROGRESS"}:
                if openspec_status == "legacy-exempt":
                    errors.append(
                        f"{feature_path.relative_to(root)} uses OpenSpec Status `legacy-exempt` outside [DONE]"
                    )
                if change_id is None:
                    errors.append(f"{feature_path.relative_to(root)} is missing OpenSpec Change metadata")
                else:
                    change_dir = root / "openspec" / "changes" / change_id
                    if not change_dir.exists():
                        errors.append(
                            f"{feature_path.relative_to(root)} links missing OpenSpec change openspec/changes/{change_id}"
                        )
                    if section_name in {"SHAPING", "READY"}:
                        for required_name in ("proposal.md", "design.md", "tasks.md"):
                            if not (change_dir / required_name).exists():
                                errors.append(
                                    f"{feature_path.relative_to(root)} is in [{section_name}] but linked OpenSpec change is missing {required_name}"
                                )
                    tasks_file = change_dir / "tasks.md"
                    if tasks_file.exists():
                        structure_errors = find_openspec_task_structure_errors(
                            tasks_file.read_text(encoding="utf-8")
                        )
                        for structure_error in structure_errors:
                            errors.append(f"{feature_path.relative_to(root)} {structure_error}")
            elif section_name == "DONE":
                if openspec_status == "legacy-exempt":
                    if change_id is not None:
                        errors.append(
                            f"{feature_path.relative_to(root)} is marked `legacy-exempt` but still records OpenSpec Change {change_id}"
                        )
                else:
                    if change_id is None:
                        errors.append(
                            f"{feature_path.relative_to(root)} is in [DONE] but has neither archived OpenSpec change metadata nor OpenSpec Status `legacy-exempt`"
                        )
                    else:
                        active_change_dir = root / "openspec" / "changes" / change_id
                        archive_matches = sorted((root / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))
                        if active_change_dir.exists():
                            errors.append(
                                f"{feature_path.relative_to(root)} is in [DONE] but linked OpenSpec change is still active at openspec/changes/{change_id}"
                            )
                        if len(archive_matches) != 1:
                            errors.append(
                                f"{feature_path.relative_to(root)} is in [DONE] but expected exactly one archived OpenSpec change for {change_id}"
                            )
            else:
                if change_id is None:
                    errors.append(f"{feature_path.relative_to(root)} is missing OpenSpec Change metadata")
                else:
                    change_dir = root / "openspec" / "changes" / change_id
                    if not change_dir.exists():
                        errors.append(
                            f"{feature_path.relative_to(root)} links missing OpenSpec change openspec/changes/{change_id}"
                        )

            try:
                tasks = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
            except ValueError as exc:
                errors.append(f"{feature_path.relative_to(root)} {exc}")
                continue
            task_statuses = [task.status for task in tasks]
            for task in tasks:
                if task.status == "in_progress":
                    in_progress_records.append((feature_id, task.task_id))

            try:
                current_task = parse_current_task(feature_text)
            except ValueError as exc:
                errors.append(f"{feature_path.relative_to(root)} {exc}")
                current_task = None
            reference_error = current_task_reference_error(current_task, tasks)
            if reference_error is not None:
                errors.append(f"{feature_path.relative_to(root)} {reference_error}")

            if section_name == "READY" and "ready" not in task_statuses:
                errors.append(
                    f"{feature_path.relative_to(root)} is in [READY] but has no task with status `ready`"
                )

            readiness_drift = compute_task_readiness_drift(feature_text, feature_file=feature_path, repo_root=root)
            for drift_message in format_task_readiness_drift_messages(
                readiness_drift,
                feature_label=str(feature_path.relative_to(root)),
            ):
                errors.append(drift_message)

    if len(in_progress_records) > 1:
        errors.append(
            f"repository has {len(in_progress_records)} tasks with status `in_progress`, expected at most 1"
        )

    if current_path is not None and (openspec_root / "changes").is_dir():
        linkage = collect_openspec_change_linkage(root)
        for change_id in linkage.orphan_active_change_ids:
            errors.append(f"orphan active OpenSpec change {change_id} is not linked from any promoted feature")

    return errors, in_progress_records


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        root = repo_root(args.repo_root)
    except WorkflowError as exc:
        print(f"ERROR: {exc}")
        return 1

    errors, in_progress_records = _audit_single_root(root)
    aggregated_records: list[tuple[Path, str, str]] = [
        (root, feature_id, task_id) for feature_id, task_id in in_progress_records
    ]

    if args.include_worktrees:
        for worktree_root in list_git_worktree_roots(root):
            if worktree_root == root.resolve():
                continue
            wt_errors, wt_records = _audit_single_root(worktree_root)
            for wt_error in wt_errors:
                errors.append(f"[worktree {worktree_root}] {wt_error}")
            for feature_id, task_id in wt_records:
                aggregated_records.append((worktree_root, feature_id, task_id))

        distinct_pairs = {(feature_id, task_id) for _, feature_id, task_id in aggregated_records}
        if len(distinct_pairs) > 1:
            errors.append(
                "cross-worktree drift: multiple distinct in_progress tasks across worktrees: "
                + ", ".join(
                    f"{feature_id}/{task_id} in {worktree_root}"
                    for worktree_root, feature_id, task_id in aggregated_records
                )
            )

    if args.gate == "start":
        if aggregated_records:
            scope = "across worktrees" if args.include_worktrees else "in this checkout"
            errors.append(
                f"--gate=start requires 0 in_progress tasks {scope}; found "
                + ", ".join(f"{feature_id}/{task_id}" for _, feature_id, task_id in aggregated_records)
            )
    elif args.gate == "complete":
        distinct_pairs = {(feature_id, task_id) for _, feature_id, task_id in aggregated_records}
        if len(distinct_pairs) != 1:
            scope = "across worktrees" if args.include_worktrees else "in this checkout"
            errors.append(
                f"--gate=complete requires exactly 1 in_progress task {scope}; found {len(distinct_pairs)}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.gate == "complete" and aggregated_records:
        feature_id, task_id = aggregated_records[0][1], aggregated_records[0][2]
        print(f"OK: gate=complete feature_id={feature_id} task_id={task_id}")
    else:
        current_version = root / "docs" / "planning" / "current_version"
        label = current_version.resolve().relative_to(root) if current_version.exists() else current_version
        print(f"OK: workflow audit passed for {label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

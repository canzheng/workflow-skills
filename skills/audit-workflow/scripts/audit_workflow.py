#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.workflow_state import (
    WORKFLOW_SECTIONS,
    compute_task_readiness_drift,
    format_task_readiness_drift_messages,
    parse_backlog_document,
    parse_tasks,
    parse_feature_openspec_change,
)

SECTION_RE = re.compile(r"^## \[(?P<name>[A-Z_]+)\]$", re.MULTILINE)
FEATURE_ID_RE = re.compile(r"^- Feature ID: `([^`]+)`$", re.MULTILINE)
BACKLOG_REF_RE = re.compile(r"^- Backlog Reference: `([^`]+)`$", re.MULTILINE)
TASK_STATUS_RE = re.compile(r"^- Status: `([^`]+)`$", re.MULTILINE)


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
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed workflow checks.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        root = repo_root(args.repo_root)
    except WorkflowError as exc:
        print(f"ERROR: {exc}")
        return 1

    errors: list[str] = []

    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        errors.append("docs/planning/current_version is missing")
        current_path = None
    else:
        if not current_version.is_symlink():
            errors.append("docs/planning/current_version is not a symlink")
        current_path = current_version.resolve()

    if current_path is None:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

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
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    backlog_text = backlog.read_text(encoding="utf-8")
    found_sections = [match.group("name") for match in SECTION_RE.finditer(backlog_text)]
    if found_sections[: len(WORKFLOW_SECTIONS)] != WORKFLOW_SECTIONS:
        errors.append(
            f"{backlog.relative_to(root)} has section order {found_sections[:len(WORKFLOW_SECTIONS)]}, expected {WORKFLOW_SECTIONS}"
        )

    version = current_path.name
    parsed_backlog = parse_backlog_document(backlog_text)
    for malformed_entry in parsed_backlog.malformed_entries:
        errors.append(f"{backlog.relative_to(root)} {malformed_entry}")
    in_progress_tasks = 0

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
            if change_id is None:
                errors.append(f"{feature_path.relative_to(root)} is missing OpenSpec Change metadata")
            else:
                change_dir = root / "openspec" / "changes" / change_id
                if not change_dir.exists():
                    errors.append(
                        f"{feature_path.relative_to(root)} links missing OpenSpec change openspec/changes/{change_id}"
                    )
                if section_name == "READY":
                    for required_name in ("proposal.md", "design.md", "tasks.md"):
                        if not (change_dir / required_name).exists():
                            errors.append(
                                f"{feature_path.relative_to(root)} is in [READY] but linked OpenSpec change is missing {required_name}"
                            )

            task_statuses = [
                task.status
                for task in parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
            ]
            in_progress_tasks += sum(1 for status in task_statuses if status == "in_progress")

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

    if in_progress_tasks > 1:
        errors.append(f"repository has {in_progress_tasks} tasks with status `in_progress`, expected at most 1")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: workflow audit passed for {current_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

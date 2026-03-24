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

from _workflow.workflow_state import parse_backlog_document, parse_feature_openspec_change


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
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed finish checks.")
    parser.add_argument("--feature-id", help="Explicit feature ID to finish.")
    return parser.parse_args(argv)


def _read_done_features(root: Path) -> tuple[Path, list[tuple[str, Path]]]:
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

    done_features: list[tuple[str, Path]] = []
    for entry in parsed_backlog.feature_sections["DONE"]:
        feature_path = (backlog_path.parent / entry.link).resolve()
        done_features.append((entry.feature_id, feature_path))
    return backlog_path, done_features


def resolve_finish_feature(root: Path, feature_id: str | None = None) -> dict[str, object]:
    backlog_path, done_features = _read_done_features(root)

    if feature_id is None:
        if len(done_features) != 1:
            raise WorkflowError("expected exactly one feature in [DONE]; pass --feature-id to disambiguate")
        resolved_feature_id, feature_path = done_features[0]
    else:
        matches = [(candidate_id, path) for candidate_id, path in done_features if candidate_id == feature_id]
        if not matches:
            raise WorkflowError(f"feature {feature_id} is not in [DONE]")
        resolved_feature_id, feature_path = matches[0]

    if not feature_path.exists():
        raise WorkflowError(f"{backlog_path.relative_to(root)} links missing feature file {feature_path.relative_to(root)}")

    feature_text = feature_path.read_text(encoding="utf-8")
    change_id = parse_feature_openspec_change(feature_text)
    if change_id is None:
        raise WorkflowError(f"{feature_path.relative_to(root)} is missing OpenSpec Change metadata")

    active_change_dir = root / "openspec" / "changes" / change_id
    archive_matches = sorted((root / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))

    if active_change_dir.exists() and archive_matches:
        raise WorkflowError(
            f"{feature_path.relative_to(root)} has both an active change and archived change for {change_id}"
        )
    if len(archive_matches) > 1:
        raise WorkflowError(
            f"{feature_path.relative_to(root)} has multiple archived changes for {change_id}: "
            + ", ".join(str(path.relative_to(root)) for path in archive_matches)
        )
    if not active_change_dir.exists() and not archive_matches:
        raise WorkflowError(
            f"{feature_path.relative_to(root)} links OpenSpec change {change_id}, but no active or archived change exists"
        )

    archive_path = archive_matches[0] if archive_matches else None
    requires_archive = active_change_dir.exists()
    return {
        "feature_id": resolved_feature_id,
        "feature_path": str(feature_path.relative_to(root)),
        "change_id": change_id,
        "requires_archive": requires_archive,
        "active_change_path": str(active_change_dir.relative_to(root)) if active_change_dir.exists() else None,
        "archive_path": str(archive_path.relative_to(root)) if archive_path else None,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        payload = resolve_finish_feature(repo_root(args.repo_root), feature_id=args.feature_id)
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

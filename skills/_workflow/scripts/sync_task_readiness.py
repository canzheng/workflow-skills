#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.workflow_state import (  # noqa: E402
    compute_task_readiness_drift,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature-file", required=True, help="Absolute or repo-relative path to the feature file.")
    parser.add_argument("--repo-root", help="Optional repo root override for cross-feature dependency resolution.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Deprecated no-op. The script now always reports readiness without modifying the feature file.",
    )
    return parser.parse_args(argv)


def resolve_repo_root(feature_file: Path, explicit_repo_root: str | None) -> Path | None:
    if explicit_repo_root:
        return Path(explicit_repo_root).resolve()
    for parent in [feature_file.parent, *feature_file.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    feature_file = Path(args.feature_file).resolve()
    if not feature_file.exists():
        print(f"ERROR: feature file not found: {feature_file}", file=sys.stderr)
        return 1

    feature_text = feature_file.read_text(encoding="utf-8")
    repo_root = resolve_repo_root(feature_file, args.repo_root)
    drift = compute_task_readiness_drift(feature_text, feature_file=feature_file, repo_root=repo_root)

    print(
        json.dumps(
            {
                "feature_file": str(feature_file),
                "promotable_task_ids": drift.promotable_task_ids,
                "invalid_ready_task_ids": drift.invalid_ready_task_ids,
                "unknown_dependency_errors": drift.unknown_dependency_errors,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if drift.has_errors() else 0


if __name__ == "__main__":
    sys.exit(main())

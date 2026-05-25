#!/usr/bin/env python3
"""Deterministic openspec-archive readiness check for ready-feature.

Flags delta `## MODIFIED` requirements whose `### Requirement:` header differs
from the main spec without a `## RENAMED` bridge mapping the old main-spec header
to the new one. Without the bridge, OpenSpec archive cannot locate the
requirement to modify, so the change fails only at archive time. Running this at
readiness surfaces the gap while the feature is still being shaped.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, repo_root
from _workflow.workflow_state import openspec_archive_modified_without_rename_bridge


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root.")
    parser.add_argument("--change-id", required=True, help="The linked OpenSpec change id to check.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        root = repo_root(args.repo_root)
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    change_dir = root / "openspec" / "changes" / args.change_id
    if not change_dir.is_dir():
        print(f"ERROR: OpenSpec change not found: openspec/changes/{args.change_id}", file=sys.stderr)
        return 1

    issues = openspec_archive_modified_without_rename_bridge(change_dir, root)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1

    print(f"OK: openspec/changes/{args.change_id} has no MODIFIED-without-RENAMED archive-readiness issues")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Lint OpenSpec planning claims that need adjacent grep/Read evidence."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.workflow_state import lint_openspec_claim_evidence


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("change_dir", help="Path to the OpenSpec change directory to lint.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    change_dir = Path(args.change_dir)
    if not change_dir.is_dir():
        print(f"ERROR: OpenSpec change directory not found: {change_dir}", file=sys.stderr)
        return 1

    issues = lint_openspec_claim_evidence(change_dir)
    if issues:
        for issue in issues:
            print(
                f"ERROR: {issue.relative_path}:{issue.line_number}: "
                f"{issue.reason}: {issue.line}",
                file=sys.stderr,
            )
        return 1

    print(f"OK: {change_dir} has no unsupported pinned plan/design claims")
    return 0


if __name__ == "__main__":
    sys.exit(main())

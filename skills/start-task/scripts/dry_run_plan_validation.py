#!/usr/bin/env python3
"""Deterministic dry-run of the complete-task implementation-plan validator.

Runs the same `validate_implementation_plan_file` and
`required_validation_evidence_categories_for_plan` checks that `complete-task`
enforces at task closure, over the plan `start-task` just authored, so
plan-contract violations surface before the round-1 semantic-consistency review
instead of being deferred to completion time.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.workflow_state import (
    required_validation_evidence_categories_for_plan,
    validate_implementation_plan_file,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan_path", help="Path to the authored implementation plan to validate.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    plan_path = Path(args.plan_path)
    if not plan_path.exists():
        print(f"ERROR: implementation plan not found: {plan_path}", file=sys.stderr)
        return 1
    try:
        summary = validate_implementation_plan_file(plan_path)
    except ValueError as exc:
        print(f"ERROR: implementation plan is invalid: {exc}", file=sys.stderr)
        return 1

    payload = {
        "plan_path": str(plan_path),
        "required_validation_classes": list(summary.required_validation_classes),
        "required_evidence_categories": list(
            required_validation_evidence_categories_for_plan(summary)
        ),
        "unit_only_justification": summary.unit_only_justification,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

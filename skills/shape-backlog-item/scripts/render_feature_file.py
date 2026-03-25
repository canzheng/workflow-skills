#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from _workflow.feature_file import render_feature_file


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
    parser.add_argument("--repo-root", help="Override the repository root.")
    parser.add_argument("--feature-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--backlog-reference", required=True)
    parser.add_argument("--openspec-change", required=True)
    parser.add_argument("--openspec-spec", action="append", dest="openspec_specs", required=True)
    parser.add_argument("--created", required=True)
    parser.add_argument("--last-updated", required=True)
    parser.add_argument("--output", required=True, help="Feature file path relative to the repo root.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        root = repo_root(args.repo_root)
        output_path = (root / args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            render_feature_file(
                title=args.title,
                feature_id=args.feature_id,
                version=args.version,
                backlog_reference=args.backlog_reference,
                openspec_change=args.openspec_change,
                openspec_specs=args.openspec_specs,
                created=args.created,
                last_updated=args.last_updated,
            ),
            encoding="utf-8",
        )
    except (WorkflowError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(output_path.relative_to(root))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

SKILL_DIR = Path(__file__).resolve().parents[1]
WORKFLOW_REFERENCE_TEMPLATE_PATH = SKILL_DIR / "templates" / "WORKFLOW_REFERENCE.md"

from _workflow.cli_helpers import WorkflowError, repo_root as _repo_root
from _workflow.feature_file import FEATURE_TEMPLATE


def repo_root(explicit_root: str | None = None) -> Path:
    """Init-specific wrapper: falls back to cwd when git resolution fails
    because this skill may run against a directory that is not yet a git repo."""
    return _repo_root(explicit_root, fallback_to_cwd=True)


ROADMAP_TEMPLATE = """# Roadmap

Use `docs/planning/versions/` for active version planning artifacts.
"""


VERSION_SCOPE_TEMPLATE = """# {version_upper} Scope

## Goal
- Define the version goal.

## Exit Criteria
- Define the bar for completing this version.

## Explicit Deferrals
- None yet.

## Cross-Feature Decisions
- None yet.
"""


BACKLOG_TEMPLATE = """# {version_upper} Backlog

This file tracks feature-board status only.

- `[BACKLOG]` entries must use ``### `v1-b001` [TAG] TITLE``.
- `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` entries must use ``### `v1-f001` [TAG] [Title](features/v1-f001-title.md)``.
- `[TAG]` is optional in both formats.
- Promoted entries are heading-only. Do not write summaries, rationale, defer reasons, or evidence under them. Records go in the feature file; intent and design go in the linked OpenSpec change.
- `[BACKLOG]` items may carry body notes under the heading until they are promoted to `[SHAPING]`.

## [BACKLOG]

None yet.

## [SHAPING]

None yet.

## [READY]

None yet.

## [IN_PROGRESS]

None yet.

## [DONE]

None yet.

## [DEFER]

None yet.
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Target repository root. Defaults to git root or the current directory.")
    parser.add_argument("--version", default="v1", help="Active version directory to initialize. Defaults to v1.")
    return parser.parse_args(argv)


def ensure_text_file(path: Path, contents: str) -> str:
    if path.exists():
        return f"SKIP {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")
    return f"CREATE {path}"


def ensure_symlink(path: Path, target: Path) -> str:
    if path.exists() or path.is_symlink():
        if not path.is_symlink():
            raise WorkflowError(f"{path} exists and is not a symlink")
        if path.readlink() != target:
            raise WorkflowError(f"{path} points to {path.readlink()}, expected {target}")
        return f"SKIP {path}"
    path.symlink_to(target)
    return f"CREATE {path} -> {target}"


def workflow_reference_template() -> str:
    return WORKFLOW_REFERENCE_TEMPLATE_PATH.read_text(encoding="utf-8")


def run_openspec_init(root: Path) -> str:
    command = ["openspec", "init", "--tools", "claude"]
    try:
        subprocess.run(command, cwd=root, check=True)
    except subprocess.CalledProcessError as exc:
        raise WorkflowError(f"openspec init failed with exit code {exc.returncode}") from exc
    return f"RUN {' '.join(command)}"


def run_lessons_init(root: Path) -> str:
    command = ["lessons", "init", "--tools", "claude"]
    try:
        subprocess.run(command, cwd=root, check=True)
    except subprocess.CalledProcessError as exc:
        raise WorkflowError(f"lessons init failed with exit code {exc.returncode}") from exc
    return f"RUN {' '.join(command)}"


def initialize(root: Path, version: str) -> list[str]:
    root.mkdir(parents=True, exist_ok=True)
    planning_root = root / "docs" / "planning"
    version_root = planning_root / "versions" / version
    feature_root = version_root / "features"
    openspec_root = root / "openspec"
    results = []

    results.append(run_openspec_init(root))
    results.append(run_lessons_init(root))
    feature_root.mkdir(parents=True, exist_ok=True)
    results.append(f"ENSURE {feature_root}")
    (openspec_root / "specs").mkdir(parents=True, exist_ok=True)
    results.append(f"ENSURE {openspec_root / 'specs'}")
    (openspec_root / "changes" / "archive").mkdir(parents=True, exist_ok=True)
    results.append(f"ENSURE {openspec_root / 'changes' / 'archive'}")
    results.append(ensure_text_file(planning_root / "ROADMAP.md", ROADMAP_TEMPLATE))
    results.append(ensure_text_file(planning_root / "WORKFLOW_REFERENCE.md", workflow_reference_template()))
    results.append(ensure_text_file(planning_root / "template" / "feature-template.md", FEATURE_TEMPLATE))
    results.append(
        ensure_text_file(
            version_root / "VERSION_SCOPE.md",
            VERSION_SCOPE_TEMPLATE.format(version_upper=version.upper()),
        )
    )
    results.append(
        ensure_text_file(
            version_root / "BACKLOG.md",
            BACKLOG_TEMPLATE.format(version_upper=version.upper()),
        )
    )
    results.append(ensure_symlink(planning_root / "current_version", Path("versions") / version))

    return results


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        results = initialize(repo_root(args.repo_root), args.version)
    except WorkflowError as exc:
        print(f"ERROR: {exc}")
        return 1

    for line in results:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())

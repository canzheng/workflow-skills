#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


FEATURE_TEMPLATE = """# Feature: <title>

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f001`
- Version: `v1`
- Backlog Reference: `<link or anchor>`
- OpenSpec Change: `<change-id>`
- OpenSpec Specs:
  - `openspec/specs/<capability>/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
- Created: `YYYY-MM-DD`
- Last Updated: `YYYY-MM-DD`

## 1. Execution Scope
- Objective:
  - <execution target linked to the OpenSpec change>
- In Scope Files:
  - `<path/to/file>`
- Out of Scope:
  - <out-of-scope item>
- Constraints:
  - <constraint>
- Shaping Source:
  - `openspec/changes/<change-id>/proposal.md`
  - `openspec/changes/<change-id>/design.md`
  - `openspec/changes/<change-id>/tasks.md`

## 2. Tasks

Task status lives here. OpenSpec owns shaping artifacts; this file owns execution status, readiness, and evidence.

### T01: <title>
- Status: `todo`
- OpenSpec Task Reference:
  - `openspec/changes/<change-id>/tasks.md#task-group`
- Objective:
  - <what this task changes>
- Depends On:
  - none
- Scope:
  - `<path/to/file>`
- Constraints:
  - <constraint>
- Acceptance Criteria:
  - [ ] <observable outcome>
- Validation:
  - Run: `<command or inspection step>`
  - Expect: `<expected result>`
- Evidence:
  - Not run yet

---

### T02: <title>
- Status: `todo`
- OpenSpec Task Reference:
  - `openspec/changes/<change-id>/tasks.md#task-group`
- Objective:
  - <what this task changes>
- Depends On:
  - `T01`
- Scope:
  - `<path/to/file>`
- Constraints:
  - <constraint>
- Acceptance Criteria:
  - [ ] <observable outcome>
- Validation:
  - Run: `<command or inspection step>`
  - Expect: `<expected result>`
- Evidence:
  - Not run yet

## 3. Validation Log
- `<YYYY-MM-DD>` Task `<task-id>`:
  - Run: `<command or inspection step>`
  - Result: `<pass/fail and notable details>`

## 4. Change Log
- `<YYYY-MM-DD>`:
  - <summary of workflow state, task sync, or evidence update>
"""


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
- Detailed evidence, raw diagnostics, and task-level progress belong in feature files or source notes, not here.

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


class WorkflowError(RuntimeError):
    pass


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Target repository root. Defaults to git root or the current directory.")
    parser.add_argument("--version", default="v1", help="Active version directory to initialize. Defaults to v1.")
    return parser.parse_args(argv)


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

    return Path.cwd().resolve()


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


def initialize(root: Path, version: str) -> list[str]:
    planning_root = root / "docs" / "planning"
    version_root = planning_root / "versions" / version
    feature_root = version_root / "features"
    results = []

    feature_root.mkdir(parents=True, exist_ok=True)
    results.append(f"ENSURE {feature_root}")
    results.append(ensure_text_file(planning_root / "ROADMAP.md", ROADMAP_TEMPLATE))
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

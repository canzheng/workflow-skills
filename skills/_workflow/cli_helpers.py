"""Shared CLI preamble for skill entry scripts.

Every Python script under `skills/<skill>/scripts/` imports the workflow-level
error type, the repo-root resolver, and (when applicable) the backlog loader
from this module instead of redefining them locally. An anchor-based
`resolve_skills_root()` is also exported for callers that already have
`_workflow` importable.

Scripts themselves still carry a tiny inline bootstrap to put the `skills/`
directory on `sys.path` before they can import this module; that bootstrap
walks upward from `__file__` for the first directory with a `_workflow/`
child, so it is resilient to relocation.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from _workflow.workflow_state import ParsedBacklogDocument, parse_backlog_document


class WorkflowError(RuntimeError):
    """Canonical error type for workflow script-level failures."""


def repo_root(
    explicit_root: str | None = None,
    *,
    fallback_to_cwd: bool = False,
) -> Path:
    """Resolve the repository root.

    Precedence: explicit `--repo-root` value, then `WORKFLOW_REPO_ROOT` env var,
    then `git rev-parse --show-toplevel` in the current working directory. When
    `fallback_to_cwd=True` and git resolution fails, returns the current working
    directory (used by `initialize-workflow-artifacts`, which runs against a
    directory that may not yet be a git repo). Otherwise raises `WorkflowError`.
    """
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

    if fallback_to_cwd:
        return Path.cwd().resolve()

    raise WorkflowError(
        "could not determine repo root; run inside the target repo or pass --repo-root"
    )


def load_backlog(root: Path) -> tuple[Path, str, ParsedBacklogDocument]:
    """Load and parse the active-version `BACKLOG.md`.

    Returns `(backlog_path, backlog_text, parsed_backlog)`. Callers that only
    need the path and parsed document can discard `backlog_text`. Raises
    `WorkflowError` if the `current_version` symlink is missing or invalid,
    `BACKLOG.md` is missing, or the backlog has malformed entries.
    """
    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        raise WorkflowError("docs/planning/current_version is missing")
    if not current_version.is_symlink():
        raise WorkflowError("docs/planning/current_version is not a symlink")

    version_root = current_version.resolve()
    backlog_path = version_root / "BACKLOG.md"
    if not backlog_path.exists():
        raise WorkflowError(f"{backlog_path.relative_to(root)} is missing")

    backlog_text = backlog_path.read_text(encoding="utf-8")
    parsed_backlog = parse_backlog_document(backlog_text)
    if parsed_backlog.malformed_entries:
        raise WorkflowError(
            "; ".join(
                f"{backlog_path.relative_to(root)} {message}"
                for message in parsed_backlog.malformed_entries
            )
        )
    return backlog_path, backlog_text, parsed_backlog


def resolve_skills_root(start: Path | None = None) -> Path:
    """Locate the `skills/` root by walking upward for a `_workflow/` sibling.

    Intended for callers that already have `_workflow` importable (e.g. tests
    or helpers that want the shared path without re-implementing the walk).
    Scripts themselves do the equivalent walk inline before importing from
    this module, so they cannot rely on this function for their own bootstrap.
    Raises `WorkflowError` when no ancestor contains a `_workflow/` child.
    """
    here = (start or Path(__file__)).resolve()
    for candidate in (here.parent, *here.parents):
        if (candidate / "_workflow").is_dir():
            return candidate
    raise WorkflowError(
        f"could not locate a skills root containing _workflow/ above {here}"
    )

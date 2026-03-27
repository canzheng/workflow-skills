from __future__ import annotations

from pathlib import Path


_TRACKED_FEATURE_TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "docs" / "planning" / "template" / "feature-template.md"
_INSTALLED_FEATURE_TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "feature-template.md"
_REPO_FEATURE_TEMPLATE_RELATIVE_PATH = Path("docs") / "planning" / "template" / "feature-template.md"

_FALLBACK_FEATURE_TEMPLATE = """# Feature: <title>

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
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
  - This field is the active execution marker for the implemented workflow; OpenSpec `tasks.md` remains the checked/unchecked task ledger.
- Created: `YYYY-MM-DD`
- Last Updated: `YYYY-MM-DD`

## 1. Validation Log
- `<YYYY-MM-DD>` Task `<task-id>`:
  - Run: `<command or inspection step>`
  - Result: `<pass/fail and notable details>`

## 2. Handoff Notes
- `<YYYY-MM-DD>`:
  - Current Task: `<task-id like 1 or none>`
  - Worktree State: `<clean/dirty>`
  - Notes: <handoff summary>
"""


def _load_feature_template(repo_root: Path | None = None) -> str:
    candidate_paths: list[Path] = []
    if repo_root is not None:
        candidate_paths.append(repo_root / _REPO_FEATURE_TEMPLATE_RELATIVE_PATH)
    candidate_paths.extend((_TRACKED_FEATURE_TEMPLATE_PATH, _INSTALLED_FEATURE_TEMPLATE_PATH))

    for template_path in candidate_paths:
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")
    return _FALLBACK_FEATURE_TEMPLATE


FEATURE_TEMPLATE = _load_feature_template()


def render_feature_file(
    *,
    title: str,
    feature_id: str,
    version: str,
    backlog_reference: str,
    openspec_change: str,
    openspec_specs: list[str],
    created: str,
    last_updated: str,
    repo_root: Path | None = None,
) -> str:
    if not openspec_specs:
        raise ValueError("openspec_specs must not be empty")

    spec_lines = "\n".join(f"  - `{path}`" for path in openspec_specs)
    rendered = _load_feature_template(repo_root)
    replacements = (
        ("# Feature: <title>", f"# Feature: {title}"),
        ("- Feature ID: `v1-f001`", f"- Feature ID: `{feature_id}`"),
        ("- Version: `v1`", f"- Version: `{version}`"),
        ("- Backlog Reference: `<link or anchor>`", f"- Backlog Reference: `{backlog_reference}`"),
        ("- OpenSpec Change: `<change-id>`", f"- OpenSpec Change: `{openspec_change}`"),
        ("  - `openspec/specs/<capability>/spec.md`", spec_lines),
        ("- Created: `YYYY-MM-DD`", f"- Created: `{created}`"),
        ("- Last Updated: `YYYY-MM-DD`", f"- Last Updated: `{last_updated}`"),
    )
    for old, new in replacements:
        rendered = rendered.replace(old, new, 1)
    return rendered if rendered.endswith("\n") else f"{rendered}\n"

from __future__ import annotations

from textwrap import dedent


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

## 1. Validation Log
- `<YYYY-MM-DD>` Task `<task-id>`:
  - Run: `<command or inspection step>`
  - Result: `<pass/fail and notable details>`

## 2. Handoff Notes
- `<YYYY-MM-DD>`:
  - Current Task: `<task-id or none>`
  - Worktree State: `<clean/dirty>`
  - Notes: <handoff summary>
"""


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
) -> str:
    if not openspec_specs:
        raise ValueError("openspec_specs must not be empty")

    spec_lines = "\n".join(f"- `{path}`" for path in openspec_specs)
    return dedent(
        f"""\
        # Feature: {title}

        Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

        ## 0. Meta
        - Feature ID: `{feature_id}`
        - Version: `{version}`
        - Backlog Reference: `{backlog_reference}`
        - OpenSpec Change: `{openspec_change}`
        - OpenSpec Specs:
        {spec_lines}
        - Current Task: `none`
          - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
        - Created: `{created}`
        - Last Updated: `{last_updated}`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )

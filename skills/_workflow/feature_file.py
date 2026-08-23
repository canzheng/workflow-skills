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
- Treat this section as the running execution evidence ledger for the active task. Add entries as planned validation steps complete; do not wait until task closure to write all evidence at once.
- `<YYYY-MM-DD>` Task `<task-id>`:
  - Run: `<command or inspection step>`
  - Result: `<pass/fail and notable details>`
  - Evidence: `<comma-separated validation categories such as schema, runtime_path, artifact_repair, prompt_contract, orchestration, negative_case>`

## 2. Handoff Notes
- `<YYYY-MM-DD>`:
  - Current Task: `<task-id like 1 or none>`
  - Worktree State: `<clean/dirty>`
  - Review Scope: `<ready | task_readiness | task_execution | task_completion | feature_finish | remediation_code | record_integrity>`
  - Review Target: `<feature-id | top-level-task-id>`
  - Review Verdict: `<approved | changes_requested | blocked>`  # exactly these; `_remediation_gap` branches on the spelling
  - Blocking Findings: `<none or comma-separated stable finding ids or labels>`
  - Review Terminal: `<true | false>`
  - Notes: <handoff summary>
  - Proof Obligations: `<short note about the active task's proof-obligation surface when relevant>`

## 3. Task Completion Ledger
- `complete-task` appends one line here when it closes a task, as its final act. This is the
  workflow's only UNCONDITIONAL provenance record: `done` is derived from a checkbox in `tasks.md`,
  so without a line here a hand-checked box is indistinguishable from a fully gated close.
  `audit-workflow` requires one line per done task on every open feature.
- The line is written by `complete-task/scripts/write_completion_ledger.py` and by nothing else. It
  carries a `plan-sha256` and a `head` commit that `audit-workflow` RE-VERIFIES, so a hand-typed line
  is reported rather than accepted. Do not edit these lines; do not write one for a task that is not
  yet `done`, which would pre-approve a close that has not happened.
- Shape (produced by the script, not typed):
  `- Task `4` completed `2026-08-06` plan-sha256 `fe324224cd13e0be` head `1c6318818fbf``
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


def _format_validation_entry(*, entry_date: str, task_id: str, run: str, result: str, evidence: str) -> str:
    return (
        f"- `{entry_date}` Task `{task_id}`:\n"
        f"  - Run: `{run}`\n"
        f"  - Result: `{result}`\n"
        f"  - Evidence: `{evidence}`\n"
    )


def append_task_validation_entry(
    feature_file: Path,
    *,
    entry_date: str,
    task_id: str,
    run: str,
    result: str,
    evidence: str,
) -> None:
    feature_text = feature_file.read_text(encoding="utf-8")
    validation_log_header = "## 1. Validation Log\n"
    handoff_notes_header = "## 2. Handoff Notes\n"

    validation_log_start = feature_text.index(validation_log_header)
    handoff_notes_start = feature_text.index(handoff_notes_header)
    validation_body = feature_text[
        validation_log_start + len(validation_log_header):handoff_notes_start
    ]

    if validation_body.strip() == "- None yet.":
        new_validation_body = _format_validation_entry(
            entry_date=entry_date,
            task_id=task_id,
            run=run,
            result=result,
            evidence=evidence,
        )
    else:
        new_validation_body = validation_body.rstrip() + "\n" + _format_validation_entry(
            entry_date=entry_date,
            task_id=task_id,
            run=run,
            result=result,
            evidence=evidence,
        )

    updated = (
        feature_text[: validation_log_start + len(validation_log_header)]
        + new_validation_body
        + "\n"
        + feature_text[handoff_notes_start:]
    )
    feature_file.write_text(updated, encoding="utf-8")

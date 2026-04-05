from __future__ import annotations

import textwrap
from pathlib import Path

from _workflow.feature_file import append_task_validation_entry


def _feature_text() -> str:
    return textwrap.dedent(
        """\
        # Feature: Example

        ## 0. Meta
        - Feature ID: `v1-f015`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - OpenSpec Change: `v1-f015-record-execution-evidence`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `1`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - `2026-04-06`:
          - Current Task: `1`
          - Worktree State: `clean`
          - Notes: Test fixture
        """
    )


def test_append_task_validation_entry_replaces_none_yet_and_preserves_handoff_notes(tmp_path: Path) -> None:
    feature_file = tmp_path / "feature.md"
    feature_file.write_text(_feature_text(), encoding="utf-8")

    append_task_validation_entry(
        feature_file,
        entry_date="2026-04-06",
        task_id="1",
        run="rtk pytest tests/test_example.py -q",
        result="pass",
        evidence="runtime_path",
    )

    updated = feature_file.read_text(encoding="utf-8")
    assert "- None yet." not in updated
    assert "- `2026-04-06` Task `1`:" in updated
    assert "  - Run: `rtk pytest tests/test_example.py -q`" in updated
    assert "  - Result: `pass`" in updated
    assert "  - Evidence: `runtime_path`" in updated
    assert "## 2. Handoff Notes" in updated
    assert "Notes: Test fixture" in updated


def test_append_task_validation_entry_appends_without_overwriting_existing_entries(tmp_path: Path) -> None:
    feature_file = tmp_path / "feature.md"
    feature_file.write_text(_feature_text(), encoding="utf-8")

    append_task_validation_entry(
        feature_file,
        entry_date="2026-04-06",
        task_id="1",
        run="rtk pytest tests/test_example.py -q",
        result="pass",
        evidence="runtime_path",
    )
    append_task_validation_entry(
        feature_file,
        entry_date="2026-04-06",
        task_id="1",
        run="inspect generated artifact",
        result="pass",
        evidence="manual_inspection",
    )

    updated = feature_file.read_text(encoding="utf-8")
    assert updated.count("- `2026-04-06` Task `1`:") == 2
    assert "  - Run: `inspect generated artifact`" in updated
    assert "  - Evidence: `manual_inspection`" in updated

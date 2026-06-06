from __future__ import annotations

import textwrap
from pathlib import Path

from _workflow.workflow_state import (
    TaskRecord,
    WorkflowStateError,
    collect_openspec_change_linkage,
    collect_task_validation_evidence,
    compute_task_readiness_drift,
    current_task_reference_error,
    find_backlog_section_order_errors,
    find_openspec_task_structure_errors,
    latest_review_verdict,
    openspec_archive_modified_without_rename_bridge,
    parse_handoff_review_verdicts,
    parse_feature_openspec_specs,
    required_validation_evidence_categories_for_plan,
    validate_promoted_feature_openspec_specs,
    list_open_openspec_nested_items,
    lint_openspec_claim_evidence,
    parse_backlog_document,
    parse_current_task,
    parse_tasks,
    validate_implementation_plan_file,
    validate_active_feature_execution,
)


def _feature_text() -> str:
    return textwrap.dedent(
        """\
        # Feature: Example

        ## 0. Meta
        - Feature ID: `v1-f999`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `none`

        ## 6. Tasks

        ### T01: First task
        - Status: `done`
        - Depends On:
          - none

        ### T02: Second task
        - Status: `todo`
        - Depends On:
          - `T01`

        ### T03: Third task
        - Status: `todo`
        - Depends On:
          - `T02`

        ### T04: Parallel task
        - Status: `todo`
        - Depends On:
          - none

        ### T05: Invalid ready task
        - Status: `ready`
        - Depends On:
          - `T03`
        """
    )


def test_compute_task_readiness_drift_reports_all_eligible_todo_and_invalid_ready_tasks() -> None:
    drift = compute_task_readiness_drift(_feature_text())

    assert drift.promotable_task_ids == ["T02", "T04"]
    assert drift.invalid_ready_task_ids == ["T05"]
    assert drift.unknown_dependency_errors == []


def test_compute_task_readiness_drift_accepts_done_cross_feature_dependencies(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))

    external_feature = textwrap.dedent(
        """\
        # Feature: External

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
        - Current Task: `none`

        ## 6. Tasks

        ### T03: External task
        - Status: `done`
        - Depends On:
          - none
        """
    )
    (feature_dir / "v1-f001-external.md").write_text(external_feature, encoding="utf-8")

    local_feature = textwrap.dedent(
        """\
        # Feature: Local

        ## 0. Meta
        - Feature ID: `v1-f002`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - Current Task: `none`

        ## 6. Tasks

        ### T01: First task
        - Status: `done`
        - Depends On:
          - none

        ### T02: Second task
        - Status: `todo`
        - Depends On:
          - `T01`
          - `v1-f001/T03`
        """
    )
    local_feature_path = feature_dir / "v1-f002-local.md"
    local_feature_path.write_text(local_feature, encoding="utf-8")

    drift = compute_task_readiness_drift(local_feature, feature_file=local_feature_path, repo_root=repo)

    assert drift.promotable_task_ids == ["T02"]
    assert drift.invalid_ready_task_ids == []
    assert drift.unknown_dependency_errors == []


def test_compute_task_readiness_drift_uses_openspec_tasks_with_feature_context(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes" / "sample-change").mkdir(parents=True, exist_ok=True)

    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `sample-change`
        - OpenSpec Specs:
          - `openspec/specs/workflow-board-lifecycle/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    feature_path = feature_dir / "v1-f001-sample.md"
    feature_path.write_text(feature_text, encoding="utf-8")
    (repo / "openspec" / "changes" / "sample-change" / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Work

            - [x] 1 Baseline
              - [x] 1.1 Capture current behavior
            - [ ] 2 Next step
              - [ ] 2.1 Update helper code
              - Depends On:
                - `1`
            """
        ),
        encoding="utf-8",
    )

    drift = compute_task_readiness_drift(feature_text, feature_file=feature_path, repo_root=repo)

    assert drift.promotable_task_ids == []
    assert drift.invalid_ready_task_ids == []
    assert drift.unknown_dependency_errors == []


def test_validate_implementation_plan_file_accepts_structured_proof_sections(tmp_path: Path) -> None:
    plan_path = tmp_path / "1.md"
    plan_path.write_text(
        textwrap.dedent(
            """\
            # Task 1 Implementation Plan

            ## Objective

            Exercise workflow validation.

            ## Contract Surface

            - Change Type: `behavioral`
            - Workflow Surface: `resolver path`

            ## Proof Obligations

            - The plan must declare proof obligations explicitly.

            ## Validation Plan

            ### Required Validation Classes

            - `unit`
            - `integration`

            ### Unit-Only Justification

            None.
            """
        ),
        encoding="utf-8",
    )

    summary = validate_implementation_plan_file(plan_path)

    assert summary.required_validation_classes == ("unit", "integration")
    assert summary.unit_only_justification == "None."
    assert required_validation_evidence_categories_for_plan(summary) == ("runtime_path",)


def test_collect_task_validation_evidence_normalizes_categorized_validation_log_entries() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Example

        ## 0. Meta
        - Feature ID: `v1-f999`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `none`

        ## 1. Validation Log
        - `2026-04-05` Task `3` Completion:
          - Run: `python -m pytest`
          - Result: `pass`
          - Evidence: `runtime path`, helper proof, negative-case
        - `2026-04-05` Task `2` Completion:
          - Run: `python -m pytest`
          - Result: `pass`
          - Evidence: `schema`

        ## 2. Handoff Notes
        - None yet.
        """
    )

    evidence = collect_task_validation_evidence(feature_text, "3")

    assert evidence.task_id == "3"
    assert evidence.evidence_lines == ("`runtime path`, helper proof, negative-case",)
    assert evidence.evidence_categories == ("runtime_path", "negative_case")


def test_validate_implementation_plan_file_rejects_behavioral_plan_without_runtime_validation_or_justification(
    tmp_path: Path,
) -> None:
    plan_path = tmp_path / "1.md"
    plan_path.write_text(
        textwrap.dedent(
            """\
            # Task 1 Implementation Plan

            ## Objective

            Exercise workflow validation.

            ## Contract Surface

            - Change Type: `behavioral`
            - Workflow Surface: `resolver path`

            ## Proof Obligations

            - The plan must declare proof obligations explicitly.

            ## Validation Plan

            ### Required Validation Classes

            - `unit`

            ### Unit-Only Justification

            None.
            """
        ),
        encoding="utf-8",
    )

    try:
        validate_implementation_plan_file(plan_path)
    except ValueError as exc:
        assert "runtime-facing validation class or an explicit unit-only justification" in str(exc)
    else:
        raise AssertionError("expected behavioral plan without runtime validation to be rejected")


def test_lint_openspec_claim_evidence_rejects_unsupported_file_line_and_numeric_claims(
    tmp_path: Path,
) -> None:
    change_dir = tmp_path / "example-change"
    change_dir.mkdir()
    (change_dir / "design.md").write_text(
        textwrap.dedent(
            """\
            ## Decision

            - `calibration_run.py:636` is the only embargo arithmetic path.
            - The matched evaluation reproduces canonical 0.0782.
            """
        ),
        encoding="utf-8",
    )

    issues = lint_openspec_claim_evidence(change_dir)

    assert [(issue.relative_path, issue.line_number, issue.reason) for issue in issues] == [
        ("design.md", 3, "file-line citation lacks adjacent grep/Read evidence block"),
        ("design.md", 4, "numeric claim lacks adjacent grep/Read evidence block"),
    ]


def test_lint_openspec_claim_evidence_accepts_adjacent_grep_evidence_blocks(
    tmp_path: Path,
) -> None:
    change_dir = tmp_path / "example-change"
    change_dir.mkdir()
    (change_dir / "design.md").write_text(
        textwrap.dedent(
            """\
            ## Decision

            Evidence:
            ```text
            rtk rg -n "embargo" calibration_run.py panel.py
            calibration_run.py:636:existing embargo arithmetic
            panel.py:147:duplicated embargo arithmetic
            ```
            - `calibration_run.py:636` and `panel.py:147` show the duplicated paths.

            Evidence:
            ```text
            Read output: matched evaluation returned 0.0782.
            ```
            - The matched evaluation reproduces canonical 0.0782.
            """
        ),
        encoding="utf-8",
    )

    assert lint_openspec_claim_evidence(change_dir) == []


def test_validate_active_feature_execution_rejects_missing_openspec_change_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    feature_path = feature_dir / "v1-f001-sample.md"
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - Current Task: `none`
        """
    )
    feature_path.write_text(feature_text, encoding="utf-8")

    try:
        validate_active_feature_execution(feature_text, feature_file=feature_path, repo_root=repo)
    except WorkflowStateError as exc:
        assert str(exc) == "docs/planning/versions/v1/features/v1-f001-sample.md is missing OpenSpec Change metadata"
    else:
        raise AssertionError("expected missing OpenSpec Change metadata to be rejected")


def test_validate_active_feature_execution_rejects_missing_active_change_dir(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    feature_path = feature_dir / "v1-f001-sample.md"
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `sample-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`
        """
    )
    feature_path.write_text(feature_text, encoding="utf-8")

    try:
        validate_active_feature_execution(feature_text, feature_file=feature_path, repo_root=repo)
    except WorkflowStateError as exc:
        assert (
            str(exc)
            == "docs/planning/versions/v1/features/v1-f001-sample.md links missing active OpenSpec change directory "
            "openspec/changes/sample-change"
        )
    else:
        raise AssertionError("expected missing active change directory to be rejected")


def test_validate_active_feature_execution_rejects_missing_openspec_specs_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "openspec" / "changes" / "sample-change").mkdir(parents=True, exist_ok=True)
    feature_path = feature_dir / "v1-f001-sample.md"
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `sample-change`
        - Current Task: `none`
        """
    )
    feature_path.write_text(feature_text, encoding="utf-8")

    try:
        validate_active_feature_execution(feature_text, feature_file=feature_path, repo_root=repo)
    except WorkflowStateError as exc:
        assert (
            str(exc)
            == "docs/planning/versions/v1/features/v1-f001-sample.md is missing OpenSpec Specs metadata"
        )
    else:
        raise AssertionError("expected missing OpenSpec Specs metadata to be rejected")


def test_validate_active_feature_execution_rejects_readiness_drift(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    feature_path = feature_dir / "v1-f001-sample.md"
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `sample-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 6. Tasks

        ### T01: Baseline
        - Status: `done`
        - Depends On:
          - none

        ### T02: Should be ready
        - Status: `todo`
        - Depends On:
          - `T01`
        """
    )
    feature_path.write_text(feature_text, encoding="utf-8")

    change_dir = repo / "openspec" / "changes" / "sample-change"
    change_dir.mkdir(parents=True, exist_ok=True)

    try:
        validate_active_feature_execution(feature_text, feature_file=feature_path, repo_root=repo)
    except WorkflowStateError as exc:
        assert (
            str(exc)
            == "workflow-derived task readiness drift detected: "
            "docs/planning/versions/v1/features/v1-f001-sample.md T02 could be `ready` but is still `todo`"
        )
    else:
        raise AssertionError("expected readiness drift to be rejected")


def test_parse_current_task_rejects_nested_subtask_identifier() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Invalid Current Task

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `1.1`
        """
    )

    try:
        parse_current_task(feature_text)
    except ValueError as exc:
        assert str(exc) == "Current Task must be `none` or a top-level OpenSpec task ID, got `1.1`"
    else:
        raise AssertionError("expected nested Current Task identifier to be rejected")


def test_parse_current_task_accepts_top_level_task_identifier() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Active Current Task

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `1`
        """
    )

    assert parse_current_task(feature_text) == "1"


def test_parse_current_task_maps_none_to_no_active_task() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Idle Current Task

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `none`
        """
    )

    assert parse_current_task(feature_text) is None


def test_parse_tasks_marks_openspec_cross_feature_dependency_ready_from_active_change(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))

    upstream_feature_text = textwrap.dedent(
        """\
        # Feature: Active upstream

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - OpenSpec Change: `active-upstream`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    upstream_feature_path = feature_dir / "v1-f001-active-upstream.md"
    upstream_feature_path.write_text(upstream_feature_text, encoding="utf-8")

    upstream_change_dir = repo / "openspec" / "changes" / "active-upstream"
    upstream_change_dir.mkdir(parents=True, exist_ok=True)
    (upstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Upstream work

            - [x] 1 Completed upstream task
            """
        ),
        encoding="utf-8",
    )

    downstream_feature_text = textwrap.dedent(
        """\
        # Feature: Downstream

        ## 0. Meta
        - Feature ID: `v1-f002`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `downstream-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    downstream_feature_path = feature_dir / "v1-f002-downstream.md"
    downstream_feature_path.write_text(downstream_feature_text, encoding="utf-8")

    downstream_change_dir = repo / "openspec" / "changes" / "downstream-change"
    downstream_change_dir.mkdir(parents=True, exist_ok=True)
    (downstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Downstream work

            - [ ] 1 Start after upstream
              - Depends On:
                - `v1-f001/1`
            """
        ),
        encoding="utf-8",
    )

    tasks = parse_tasks(downstream_feature_text, feature_file=downstream_feature_path, repo_root=repo)

    assert [(task.task_id, task.status) for task in tasks] == [("1", "ready")]


def test_parse_tasks_marks_openspec_cross_feature_dependency_ready_from_archived_change(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes" / "downstream-change").mkdir(parents=True, exist_ok=True)

    archived_feature_text = textwrap.dedent(
        """\
        # Feature: Archived upstream

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
        - OpenSpec Change: `archived-upstream`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - Archived after completion.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    archived_feature_path = feature_dir / "v1-f001-archived-upstream.md"
    archived_feature_path.write_text(archived_feature_text, encoding="utf-8")

    archive_change_dir = repo / "openspec" / "changes" / "archive" / "2026-03-25-archived-upstream"
    archive_change_dir.mkdir(parents=True, exist_ok=True)
    (archive_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Upstream work

            - [x] 1 Completed upstream task
            """
        ),
        encoding="utf-8",
    )

    downstream_feature_text = textwrap.dedent(
        """\
        # Feature: Downstream

        ## 0. Meta
        - Feature ID: `v1-f002`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `downstream-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    downstream_feature_path = feature_dir / "v1-f002-downstream.md"
    downstream_feature_path.write_text(downstream_feature_text, encoding="utf-8")
    (repo / "openspec" / "changes" / "downstream-change" / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Downstream work

            - [ ] 1 Start after upstream
              - Depends On:
                - `v1-f001/1`
            """
        ),
        encoding="utf-8",
    )

    tasks = parse_tasks(downstream_feature_text, feature_file=downstream_feature_path, repo_root=repo)

    assert [(task.task_id, task.status) for task in tasks] == [("1", "ready")]


def test_compute_task_readiness_drift_accepts_openspec_cross_feature_dependency_from_active_change(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))

    upstream_feature_text = textwrap.dedent(
        """\
        # Feature: Upstream

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - OpenSpec Change: `upstream-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / "v1-f001-upstream.md").write_text(upstream_feature_text, encoding="utf-8")

    upstream_change_dir = repo / "openspec" / "changes" / "upstream-change"
    upstream_change_dir.mkdir(parents=True, exist_ok=True)
    (upstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Upstream work

            - [x] 1 Completed upstream task
            """
        ),
        encoding="utf-8",
    )

    downstream_feature_text = textwrap.dedent(
        """\
        # Feature: Downstream

        ## 0. Meta
        - Feature ID: `v1-f002`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `downstream-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    downstream_feature_path = feature_dir / "v1-f002-downstream.md"
    downstream_feature_path.write_text(downstream_feature_text, encoding="utf-8")

    downstream_change_dir = repo / "openspec" / "changes" / "downstream-change"
    downstream_change_dir.mkdir(parents=True, exist_ok=True)
    (downstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Downstream work

            - [ ] 1 Resolve downstream task
              - Depends On:
                - `v1-f001/1`
            """
        ),
        encoding="utf-8",
    )

    drift = compute_task_readiness_drift(
        downstream_feature_text,
        feature_file=downstream_feature_path,
        repo_root=repo,
    )

    assert drift.promotable_task_ids == []
    assert drift.invalid_ready_task_ids == []
    assert drift.unknown_dependency_errors == []


def test_compute_task_readiness_drift_accepts_openspec_cross_feature_dependency_from_archived_change(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))

    upstream_feature_text = textwrap.dedent(
        """\
        # Feature: Upstream

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
        - OpenSpec Change: `upstream-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / "v1-f001-upstream.md").write_text(upstream_feature_text, encoding="utf-8")

    archive_dir = repo / "openspec" / "changes" / "archive" / "2026-03-27-upstream-change"
    archive_dir.mkdir(parents=True, exist_ok=True)
    (archive_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Upstream work

            - [x] 1 Completed upstream task
            """
        ),
        encoding="utf-8",
    )

    downstream_feature_text = textwrap.dedent(
        """\
        # Feature: Downstream

        ## 0. Meta
        - Feature ID: `v1-f002`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `downstream-change`
        - OpenSpec Specs:
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    downstream_feature_path = feature_dir / "v1-f002-downstream.md"
    downstream_feature_path.write_text(downstream_feature_text, encoding="utf-8")

    downstream_change_dir = repo / "openspec" / "changes" / "downstream-change"
    downstream_change_dir.mkdir(parents=True, exist_ok=True)
    (downstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Downstream work

            - [ ] 1 Resolve downstream task
              - Depends On:
                - `v1-f001/1`
            """
        ),
        encoding="utf-8",
    )

    drift = compute_task_readiness_drift(
        downstream_feature_text,
        feature_file=downstream_feature_path,
        repo_root=repo,
    )

    assert drift.promotable_task_ids == []
    assert drift.invalid_ready_task_ids == []
    assert drift.unknown_dependency_errors == []


def test_collect_openspec_change_linkage_reports_orphan_active_change(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes").mkdir(parents=True, exist_ok=True)

    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    backlog_path.write_text(
        textwrap.dedent(
            """\
            # V1 Backlog

            ## [BACKLOG]

            None yet.

            ## [SHAPING]

            ### `v1-f001` [Linked feature](features/v1-f001-linked-feature.md)

            ## [READY]

            None yet.

            ## [IN_PROGRESS]

            None yet.

            ## [DONE]

            None yet.

            ## [DEFER]

            None yet.
            """
        ),
        encoding="utf-8",
    )

    feature_text = textwrap.dedent(
        """\
        # Feature: Linked feature

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
        - OpenSpec Change: `linked-change`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / "v1-f001-linked-feature.md").write_text(feature_text, encoding="utf-8")

    (repo / "openspec" / "changes" / "linked-change").mkdir()
    (repo / "openspec" / "changes" / "orphan-change").mkdir()
    (repo / "openspec" / "changes" / "archive").mkdir()

    linkage = collect_openspec_change_linkage(repo)

    assert linkage.active_change_ids == ["linked-change", "orphan-change"]
    assert linkage.linked_promoted_change_ids == ["linked-change"]
    assert linkage.orphan_active_change_ids == ["orphan-change"]


def test_collect_openspec_change_linkage_excludes_archived_changes_from_active_set(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    version_dir = repo / "docs" / "planning" / "versions" / "v1"
    version_dir.mkdir(parents=True, exist_ok=True)
    (version_dir / "features").mkdir()
    (version_dir / "BACKLOG.md").write_text(
        textwrap.dedent(
            """\
            # V1 Backlog

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
        ),
        encoding="utf-8",
    )

    archive_dir = repo / "openspec" / "changes" / "archive" / "2026-03-27-archived-change"
    archive_dir.mkdir(parents=True, exist_ok=True)

    linkage = collect_openspec_change_linkage(repo)

    assert linkage.active_change_ids == []
    assert linkage.linked_promoted_change_ids == []
    assert linkage.orphan_active_change_ids == []


def test_collect_openspec_change_linkage_keeps_done_feature_linked_to_archived_change(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes" / "archive").mkdir(parents=True, exist_ok=True)

    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    backlog_path.write_text(
        textwrap.dedent(
            """\
            # V1 Backlog

            ## [BACKLOG]

            None yet.

            ## [SHAPING]

            None yet.

            ## [READY]

            None yet.

            ## [IN_PROGRESS]

            None yet.

            ## [DONE]

            ### `v1-f001` [Archived feature](features/v1-f001-archived-feature.md)

            ## [DEFER]

            None yet.
            """
        ),
        encoding="utf-8",
    )

    feature_text = textwrap.dedent(
        """\
        # Feature: Archived feature

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
        - OpenSpec Change: `archived-change`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / "v1-f001-archived-feature.md").write_text(feature_text, encoding="utf-8")
    (repo / "openspec" / "changes" / "archive" / "2026-03-27-archived-change").mkdir(parents=True, exist_ok=True)

    linkage = collect_openspec_change_linkage(repo)

    assert linkage.active_change_ids == []
    assert linkage.linked_promoted_change_ids == ["archived-change"]
    assert linkage.orphan_active_change_ids == []


def test_find_openspec_task_structure_errors_reports_nested_only_tasks() -> None:
    errors = find_openspec_task_structure_errors(
        textwrap.dedent(
            """\
            ## 1. Work

              - [ ] 1.1 Missing parent executable task
              - [ ] 1.2 Another nested item
            """
        )
    )

    assert errors == [
        "tasks.md has nested checklist items but no top-level executable tasks; add parent tasks like `- [ ] 1 ...` before nested items such as `1.1`",
        "nested checklist item `1.1` is missing parent top-level executable task `1`",
        "nested checklist item `1.2` is missing parent top-level executable task `1`",
    ]


def test_find_openspec_task_structure_errors_accepts_parent_task_structure() -> None:
    errors = find_openspec_task_structure_errors(
        textwrap.dedent(
            """\
            ## 1. Work

            - [ ] 1 Parent executable task
              - [ ] 1.1 Nested implementation detail
            - [ ] 2 Another task
              - [ ] 2.1 Another nested item
            """
        )
    )

    assert errors == []


def test_list_open_openspec_nested_items_returns_unchecked_nested_items_for_top_level_task(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes" / "sample-change").mkdir(parents=True, exist_ok=True)

    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - OpenSpec Change: `sample-change`
        - OpenSpec Specs:
          - `openspec/specs/workflow-board-lifecycle/spec.md`
        - Current Task: `1`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    feature_path = feature_dir / "v1-f001-sample.md"
    feature_path.write_text(feature_text, encoding="utf-8")
    (repo / "openspec" / "changes" / "sample-change" / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Work

            - [ ] 1 Parent task
              - [x] 1.1 Closed nested item
              - [ ] 1.2 Open nested item
            - [ ] 2 Next task
              - [ ] 2.1 Another open nested item
            """
        ),
        encoding="utf-8",
    )

    open_nested_items = list_open_openspec_nested_items(
        feature_text,
        "1",
        feature_file=feature_path,
        repo_root=repo,
    )

    assert open_nested_items == ["1.2"]


def test_parse_backlog_document_accepts_optional_tags_and_flexible_spacing() -> None:
    backlog_text = textwrap.dedent(
        """\
        # V1 Backlog

        ## [BACKLOG]

        ### `v1-b001`   [DISCOVERY]   First backlog item

        ## [SHAPING]

        ### `v1-f001`   [BOUNDARY]   [First feature](features/v1-f001-first-feature.md)

        ## [READY]

        None yet.

        ## [IN_PROGRESS]

        None yet.

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )

    parsed = parse_backlog_document(backlog_text)

    assert parsed.malformed_entries == []
    assert [(item.backlog_id, item.tag, item.title) for item in parsed.backlog_items] == [
        ("v1-b001", "DISCOVERY", "First backlog item")
    ]
    shaping_entries = parsed.feature_sections["SHAPING"]
    assert len(shaping_entries) == 1
    assert shaping_entries[0].feature_id == "v1-f001"
    assert shaping_entries[0].tag == "BOUNDARY"
    assert shaping_entries[0].title == "First feature"
    assert shaping_entries[0].link == "features/v1-f001-first-feature.md"


def test_parse_backlog_document_reports_malformed_structured_entries() -> None:
    backlog_text = textwrap.dedent(
        """\
        # V1 Backlog

        ## [BACKLOG]

        ### Missing backlog id

        ## [SHAPING]

        ### `v1-f001` Missing linked title

        ## [READY]

        None yet.

        ## [IN_PROGRESS]

        None yet.

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )

    parsed = parse_backlog_document(backlog_text)

    assert parsed.backlog_items == []
    assert parsed.feature_sections["SHAPING"] == []
    assert "malformed backlog entry" in parsed.malformed_entries[0]
    assert "malformed feature entry" in parsed.malformed_entries[1]


def test_find_backlog_section_order_errors_rejects_extra_section_after_defer() -> None:
    backlog_text = textwrap.dedent(
        """\
        # V1 Backlog

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

        ## [BLOCKED]

        None yet.
        """
    )

    assert find_backlog_section_order_errors(backlog_text) == [
        "has section order ['BACKLOG', 'SHAPING', 'READY', 'IN_PROGRESS', 'DONE', 'DEFER', 'BLOCKED'], "
        "expected ['BACKLOG', 'SHAPING', 'READY', 'IN_PROGRESS', 'DONE', 'DEFER']"
    ]


def test_find_backlog_section_order_errors_rejects_out_of_order_sections() -> None:
    backlog_text = textwrap.dedent(
        """\
        # V1 Backlog

        ## [BACKLOG]

        None yet.

        ## [READY]

        None yet.

        ## [SHAPING]

        None yet.

        ## [IN_PROGRESS]

        None yet.

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )

    assert find_backlog_section_order_errors(backlog_text) == [
        "has section order ['BACKLOG', 'READY', 'SHAPING', 'IN_PROGRESS', 'DONE', 'DEFER'], "
        "expected ['BACKLOG', 'SHAPING', 'READY', 'IN_PROGRESS', 'DONE', 'DEFER']"
    ]


def test_parse_feature_openspec_specs_returns_linked_spec_paths() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `sample-change`
        - OpenSpec Specs:
          - `openspec/specs/workflow-board-lifecycle/spec.md`
          - `openspec/specs/task-execution-handoff/spec.md`
        - Current Task: `none`
        """
    )

    assert parse_feature_openspec_specs(feature_text) == [
        "openspec/specs/workflow-board-lifecycle/spec.md",
        "openspec/specs/task-execution-handoff/spec.md",
    ]


def test_validate_promoted_feature_openspec_specs_rejects_missing_specs_for_active_feature() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `sample-change`
        - Current Task: `none`
        """
    )

    assert validate_promoted_feature_openspec_specs(feature_text, section_name="READY") == [
        "feature is missing OpenSpec Specs metadata"
    ]


def test_validate_promoted_feature_openspec_specs_allows_legacy_exempt_done_feature() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Sample

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
        - OpenSpec Status: `legacy-exempt`
        - Current Task: `none`
        """
    )

    assert validate_promoted_feature_openspec_specs(feature_text, section_name="DONE") == []


def test_parse_handoff_review_verdicts_reads_canonical_review_lines() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Example

        ## 0. Meta
        - Feature ID: `v1-f018`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - `2026-04-13`:
          - Current Task: `none`
          - Worktree State: `clean`
          - Review Scope: `task_execution`
          - Review Target: `2`
          - Review Verdict: `approved`
          - Blocking Findings: `none`
          - Review Terminal: `true`
          - Notes: Example
        """
    )

    verdicts = parse_handoff_review_verdicts(feature_text)

    assert len(verdicts) == 1
    verdict = verdicts[0]
    assert verdict.scope == "task_execution"
    assert verdict.target == "2"
    assert verdict.verdict == "approved"
    assert verdict.blocking_findings == ()
    assert verdict.terminal is True


def test_latest_review_verdict_returns_latest_matching_scope_and_target() -> None:
    feature_text = textwrap.dedent(
        """\
        # Feature: Example

        ## 0. Meta
        - Feature ID: `v1-f018`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - `2026-04-13`:
          - Current Task: `none`
          - Worktree State: `clean`
          - Review Scope: `ready`
          - Review Target: `v1-f018`
          - Review Verdict: `changes_requested`
          - Blocking Findings: `gap-1`
          - Review Terminal: `false`
          - Notes: Earlier review
        - `2026-04-14`:
          - Current Task: `none`
          - Worktree State: `clean`
          - Review Scope: `ready`
          - Review Target: `v1-f018`
          - Review Verdict: `approved`
          - Blocking Findings: `none`
          - Review Terminal: `true`
          - Notes: Latest review
        """
    )

    verdict = latest_review_verdict(feature_text, scope="ready", target="v1-f018")

    assert verdict is not None
    assert verdict.scope == "ready"
    assert verdict.target == "v1-f018"
    assert verdict.verdict == "approved"
    assert verdict.blocking_findings == ()
    assert verdict.terminal is True


def test_validate_implementation_plan_file_ignores_hash_comments_inside_fenced_blocks(tmp_path: Path) -> None:
    plan_path = tmp_path / "1.md"
    plan_path.write_text(
        textwrap.dedent(
            """\
            # Task 1 Implementation Plan

            ## Objective

            Exercise fenced-block handling.

            ## Contract Surface

            - Change Type: `behavioral`
            - Workflow Surface: `resolver path`

            ## Proof Obligations

            - The plan must declare proof obligations explicitly.

            ## Validation Plan

            ```bash
            # this comment must not terminate the Validation Plan section
            python -m pytest
            ```

            ### Required Validation Classes

            - `integration`

            ### Unit-Only Justification

            None.
            """
        ),
        encoding="utf-8",
    )

    summary = validate_implementation_plan_file(plan_path)

    assert summary.required_validation_classes == ("integration",)


def test_validate_implementation_plan_file_accepts_named_validation_class_with_description(tmp_path: Path) -> None:
    plan_path = tmp_path / "1.md"
    plan_path.write_text(
        textwrap.dedent(
            """\
            # Task 1 Implementation Plan

            ## Objective

            Exercise named-bullet handling.

            ## Contract Surface

            - Change Type: `behavioral`
            - Workflow Surface: `resolver path`

            ## Proof Obligations

            - The plan must declare proof obligations explicitly.

            ## Validation Plan

            ### Required Validation Classes

            - `integration` — runs the resolver end to end

            ### Unit-Only Justification

            None.
            """
        ),
        encoding="utf-8",
    )

    summary = validate_implementation_plan_file(plan_path)

    assert summary.required_validation_classes == ("integration",)


def _task_record(task_id: str, status: str) -> TaskRecord:
    return TaskRecord(
        task_id=task_id,
        task_title=f"Task {task_id}",
        status=status,
        depends_on=(),
        status_line_index=0,
    )


def test_current_task_reference_error_accepts_in_progress_reference() -> None:
    tasks = [_task_record("1", "in_progress")]

    assert current_task_reference_error("1", tasks) is None


def test_current_task_reference_error_allows_no_current_task() -> None:
    tasks = [_task_record("1", "done")]

    assert current_task_reference_error(None, tasks) is None


def test_current_task_reference_error_rejects_done_reference() -> None:
    tasks = [_task_record("1", "done")]

    assert (
        current_task_reference_error("1", tasks)
        == "Current Task `1` references a task with status `done`, expected `in_progress`"
    )


def test_current_task_reference_error_rejects_unknown_reference() -> None:
    tasks = [_task_record("1", "in_progress")]

    assert (
        current_task_reference_error("9", tasks)
        == "Current Task `9` does not reference any top-level OpenSpec task"
    )


def _write_archive_readiness_change(repo: Path, *, modified_header: str, with_rename_bridge: bool) -> Path:
    capability = "task-execution-handoff"
    main_spec = repo / "openspec" / "specs" / capability / "spec.md"
    main_spec.parent.mkdir(parents=True, exist_ok=True)
    main_spec.write_text(
        "## Purpose\n\n### Requirement: Original requirement name\nThe system SHALL do X.\n",
        encoding="utf-8",
    )
    change_dir = repo / "openspec" / "changes" / "example-change"
    delta_spec = change_dir / "specs" / capability / "spec.md"
    delta_spec.parent.mkdir(parents=True, exist_ok=True)
    body = ""
    if with_rename_bridge:
        body += (
            "## RENAMED Requirements\n\n"
            "- FROM: `### Requirement: Original requirement name`\n"
            f"- TO: `### Requirement: {modified_header}`\n\n"
        )
    body += (
        "## MODIFIED Requirements\n\n"
        f"### Requirement: {modified_header}\nThe system SHALL do X better.\n"
    )
    delta_spec.write_text(body, encoding="utf-8")
    return change_dir


def test_openspec_archive_modified_matching_main_spec_has_no_issue(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    change_dir = _write_archive_readiness_change(
        repo, modified_header="Original requirement name", with_rename_bridge=False
    )

    assert openspec_archive_modified_without_rename_bridge(change_dir, repo) == []


def test_openspec_archive_modified_renamed_header_requires_bridge(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    change_dir = _write_archive_readiness_change(
        repo, modified_header="Renamed requirement name", with_rename_bridge=False
    )

    issues = openspec_archive_modified_without_rename_bridge(change_dir, repo)

    assert len(issues) == 1
    assert "`## MODIFIED` requirement `Renamed requirement name` header differs from the main spec" in issues[0]
    assert "no `## RENAMED` bridge" in issues[0]


def test_openspec_archive_modified_renamed_header_accepts_rename_bridge(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    change_dir = _write_archive_readiness_change(
        repo, modified_header="Renamed requirement name", with_rename_bridge=True
    )

    assert openspec_archive_modified_without_rename_bridge(change_dir, repo) == []

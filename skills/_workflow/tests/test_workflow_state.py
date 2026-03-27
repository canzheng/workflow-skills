from __future__ import annotations

import textwrap
from pathlib import Path

from _workflow.workflow_state import (
    collect_openspec_change_linkage,
    compute_task_readiness_drift,
    find_openspec_task_structure_errors,
    list_open_openspec_nested_items,
    parse_backlog_document,
    parse_current_task,
    parse_tasks,
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

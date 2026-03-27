from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
AUDIT_SCRIPT = SKILLS_ROOT / "audit-workflow" / "scripts" / "audit_workflow.py"
DIAGNOSE_SCRIPT = SKILLS_ROOT / "diagnose-workflow" / "scripts" / "diagnose_workflow.py"
START_TASK_SCRIPT = SKILLS_ROOT / "start-task" / "scripts" / "resolve_start_task.py"
AUTONOMOUS_RESOLVER_SCRIPT = (
    SKILLS_ROOT / "autonomous-backlog-loop" / "scripts" / "resolve_autonomous_backlog_action.py"
)


def _write_repo_fixture(
    tmp_path: Path,
    *,
    feature_section: str = "IN_PROGRESS",
    task_statuses: dict[str, str],
    include_openspec_change: bool = True,
    create_change_dir: bool = True,
) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "openspec" / "changes").mkdir(parents=True, exist_ok=True)
    (repo / "openspec" / "specs").mkdir(parents=True, exist_ok=True)
    current_version = repo / "docs" / "planning" / "current_version"
    current_version.symlink_to(Path("versions/v1"))

    backlog = textwrap.dedent(
        f"""\
        # V1 Backlog

        ## [BACKLOG]

        None yet.

        ## [SHAPING]

        None yet.

        ## [READY]

        {"### `v1-f999` [Example](features/v1-f999-example.md)" if feature_section == "READY" else "None yet."}

        ## [IN_PROGRESS]

        {"### `v1-f999` [Example](features/v1-f999-example.md)" if feature_section == "IN_PROGRESS" else "None yet."}

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    feature_lines = [
        "# Feature: Example",
        "",
        "## 0. Meta",
        "- Feature ID: `v1-f999`",
        "- Version: `v1`",
        f"- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{feature_section.lower()}`",
    ]
    if include_openspec_change:
        feature_lines.extend(
            [
                "- OpenSpec Change: `example-change`",
                "- OpenSpec Specs:",
                "  - `openspec/specs/task-execution-handoff/spec.md`",
            ]
        )
    feature_lines.extend(
        [
            "- Current Task: `none`",
            "",
            "## 6. Tasks",
            "",
            "### T01: First task",
            f"- Status: `{task_statuses['T01']}`",
            "- Depends On:",
            "  - none",
            "",
            "### T02: Second task",
            f"- Status: `{task_statuses['T02']}`",
            "- Depends On:",
            "  - `T01`",
            "",
        ]
    )
    feature_text = "\n".join(feature_lines)
    (feature_dir / "v1-f999-example.md").write_text(feature_text, encoding="utf-8")
    if include_openspec_change and create_change_dir:
        change_dir = repo / "openspec" / "changes" / "example-change"
        change_dir.mkdir(parents=True, exist_ok=True)
        (change_dir / "proposal.md").write_text("## Why\n\nFixture.\n", encoding="utf-8")
        (change_dir / "design.md").write_text("## Context\n\nFixture.\n", encoding="utf-8")
        (change_dir / "tasks.md").write_text("- [ ] 1 Fixture task\n", encoding="utf-8")
    return repo


def _write_autonomous_repo_fixture(
    tmp_path: Path,
    *,
    backlog_items: list[str] | None = None,
    shaping_features: list[dict[str, object]] | None = None,
    ready_features: list[dict[str, object]] | None = None,
    in_progress_features: list[dict[str, object]] | None = None,
) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    current_version = repo / "docs" / "planning" / "current_version"
    current_version.symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes").mkdir(parents=True, exist_ok=True)

    backlog_items = backlog_items or []
    shaping_features = shaping_features or []
    ready_features = ready_features or []
    in_progress_features = in_progress_features or []

    def feature_entry(feature: dict[str, object]) -> str:
        tag = f" [{feature['tag']}]" if feature.get("tag") else ""
        return f"### `{feature['id']}`{tag} [{feature['title']}](features/{feature['id']}-{feature['slug']}.md)"

    def section_entries(lines: list[str]) -> list[str]:
        return lines if lines else ["None yet."]

    backlog = "\n".join(
        [
            "# V1 Backlog",
            "",
            "## [BACKLOG]",
            "",
            *section_entries([f"### `v1-b{index:03d}` {title}" for index, title in enumerate(backlog_items, start=1)]),
            "",
            "## [SHAPING]",
            "",
            *section_entries([feature_entry(feature) for feature in shaping_features]),
            "",
            "## [READY]",
            "",
            *section_entries([feature_entry(feature) for feature in ready_features]),
            "",
            "## [IN_PROGRESS]",
            "",
            *section_entries([feature_entry(feature) for feature in in_progress_features]),
            "",
            "## [DONE]",
            "",
            "None yet.",
            "",
            "## [DEFER]",
            "",
            "None yet.",
            "",
        ]
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    for section_name, features in (
        ("SHAPING", shaping_features),
        ("READY", ready_features),
        ("IN_PROGRESS", in_progress_features),
    ):
        for feature in features:
            change_id = feature.get("change_id")
            create_change_dir = feature.get("create_change_dir", True)
            task_lines = []
            for index, (task_id, status) in enumerate(feature["tasks"], start=1):
                depends_on = "none" if index == 1 else feature["tasks"][index - 2][0]
                task_lines.append(
                    textwrap.dedent(
                        f"""\
                        ### {task_id}: Task {index}
                        - Status: `{status}`
                        - Depends On:
                          - {depends_on}
                        """
                    ).rstrip()
                )

            feature_text = "\n".join(
                [
                    f"# Feature: {feature['title']}",
                    "",
                    "## 0. Meta",
                    f"- Feature ID: `{feature['id']}`",
                    "- Version: `v1`",
                    f"- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{section_name.lower()}`",
                    *((
                        f"- OpenSpec Change: `{change_id}`",
                        "- OpenSpec Specs:",
                        "  - `openspec/specs/task-execution-handoff/spec.md`",
                    ) if change_id else ()),
                    "- Current Task: `none`",
                    "",
                    "## 6. Tasks",
                    "",
                    *task_lines,
                    "",
                ]
            )
            (feature_dir / f"{feature['id']}-{feature['slug']}.md").write_text(feature_text, encoding="utf-8")
            if change_id and create_change_dir:
                change_dir = repo / "openspec" / "changes" / str(change_id)
                change_dir.mkdir(parents=True, exist_ok=True)
                (change_dir / "proposal.md").write_text("## Why\n\nFixture.\n", encoding="utf-8")
                (change_dir / "design.md").write_text("## Context\n\nFixture.\n", encoding="utf-8")
                (change_dir / "tasks.md").write_text("- [ ] 1 Fixture task\n", encoding="utf-8")

    return repo


def _write_cross_feature_openspec_repo_fixture(tmp_path: Path, *, archived_upstream: bool) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "specs").mkdir(parents=True, exist_ok=True)

    upstream_section = "DONE" if archived_upstream else "IN_PROGRESS"
    backlog = textwrap.dedent(
        f"""\
        # V1 Backlog

        ## [BACKLOG]

        None yet.

        ## [SHAPING]

        None yet.

        ## [READY]

        ### `v1-f002` [Downstream](features/v1-f002-downstream.md)
        {"### `v1-f001` [Upstream](features/v1-f001-upstream.md)" if upstream_section == "READY" else ""}

        ## [IN_PROGRESS]

        {"### `v1-f001` [Upstream](features/v1-f001-upstream.md)" if upstream_section == "IN_PROGRESS" else "None yet."}

        ## [DONE]

        {"### `v1-f001` [Upstream](features/v1-f001-upstream.md)" if upstream_section == "DONE" else "None yet."}

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    upstream_feature_text = textwrap.dedent(
        f"""\
        # Feature: Upstream

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{upstream_section.lower()}`
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
    (feature_dir / "v1-f002-downstream.md").write_text(downstream_feature_text, encoding="utf-8")

    downstream_change_dir = repo / "openspec" / "changes" / "downstream-change"
    downstream_change_dir.mkdir(parents=True, exist_ok=True)
    (downstream_change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
    (downstream_change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
    (downstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Downstream work

            - [ ] 1 Resolve downstream task
              - [ ] 1.1 Execute the downstream work
              - Depends On:
                - `v1-f001/1`
            - [ ] 2 Follow-up task
              - [ ] 2.1 Finish later work
              - Depends On:
                - `1`
            """
        ),
        encoding="utf-8",
    )

    upstream_tasks_text = textwrap.dedent(
        """\
        ## 1. Upstream work

        - [x] 1 Complete upstream task
          - [x] 1.1 Land prerequisite work
        """
    )
    if archived_upstream:
        archive_dir = repo / "openspec" / "changes" / "archive" / "20260327-upstream-change"
        archive_dir.mkdir(parents=True, exist_ok=True)
        (archive_dir / "proposal.md").write_text("## Why\n\nArchived\n", encoding="utf-8")
        (archive_dir / "tasks.md").write_text(upstream_tasks_text, encoding="utf-8")
    else:
        upstream_change_dir = repo / "openspec" / "changes" / "upstream-change"
        upstream_change_dir.mkdir(parents=True, exist_ok=True)
        (upstream_change_dir / "proposal.md").write_text("## Why\n\nUpstream\n", encoding="utf-8")
        (upstream_change_dir / "design.md").write_text("## Context\n\nUpstream\n", encoding="utf-8")
        (upstream_change_dir / "tasks.md").write_text(upstream_tasks_text, encoding="utf-8")

    return repo


def _write_invalid_current_task_openspec_repo_fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "specs").mkdir(parents=True, exist_ok=True)

    backlog = textwrap.dedent(
        """\
        # V1 Backlog

        ## [BACKLOG]

        None yet.

        ## [SHAPING]

        None yet.

        ## [READY]

        None yet.

        ## [IN_PROGRESS]

        ### `v1-f001` [Invalid Current Task](features/v1-f001-invalid-current-task.md)

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    feature_text = textwrap.dedent(
        """\
        # Feature: Invalid Current Task

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - OpenSpec Change: `invalid-current-task`
        - OpenSpec Specs:
          - `openspec/specs/feature-execution-tracking/spec.md`
          - `openspec/specs/workflow-audit-and-repair/spec.md`
        - Current Task: `1.1`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / "v1-f001-invalid-current-task.md").write_text(feature_text, encoding="utf-8")

    change_dir = repo / "openspec" / "changes" / "invalid-current-task"
    change_dir.mkdir(parents=True, exist_ok=True)
    (change_dir / "proposal.md").write_text("## Why\n\nInvalid current task fixture.\n", encoding="utf-8")
    (change_dir / "design.md").write_text("## Context\n\nInvalid current task fixture.\n", encoding="utf-8")
    (change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            - [ ] 1 Repair metadata
              - [ ] 1.1 Replace nested task id
            """
        ),
        encoding="utf-8",
    )

    return repo


def test_audit_workflow_reports_ready_drift_for_promotable_todo_tasks(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, task_statuses={"T01": "done", "T02": "todo"})

    result = subprocess.run(
        ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "could be `ready` but is still `todo`" in result.stdout


def test_resolve_start_task_fails_when_feature_has_task_readiness_drift(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, feature_section="READY", task_statuses={"T01": "done", "T02": "todo"})

    result = subprocess.run(
        ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "workflow-derived task readiness drift" in result.stderr.lower()


def test_resolve_start_task_fails_when_ready_feature_links_missing_active_change_dir(tmp_path: Path) -> None:
    repo = _write_repo_fixture(
        tmp_path,
        feature_section="READY",
        task_statuses={"T01": "ready", "T02": "todo"},
        create_change_dir=False,
    )

    result = subprocess.run(
        ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert (
        "docs/planning/versions/v1/features/v1-f999-example.md links missing active OpenSpec change directory "
        "openspec/changes/example-change" in result.stderr
    )


def test_autonomous_resolver_uses_openspec_backed_tasks_for_ready_features(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes" / "ready-feature-change").mkdir(parents=True, exist_ok=True)

    backlog = textwrap.dedent(
        """\
        # V1 Backlog

        ## [BACKLOG]

        None yet.

        ## [SHAPING]

        None yet.

        ## [READY]

        ### `v1-f001` [Ready Feature](features/v1-f001-ready-feature.md)

        ## [IN_PROGRESS]

        None yet.

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    feature_text = textwrap.dedent(
        """\
        # Feature: Ready Feature

        ## 0. Meta
        - Feature ID: `v1-f001`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
        - OpenSpec Change: `ready-feature-change`
        - OpenSpec Specs:
          - `openspec/specs/workflow-board-lifecycle/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / "v1-f001-ready-feature.md").write_text(feature_text, encoding="utf-8")
    (repo / "openspec" / "changes" / "ready-feature-change" / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Work

            - [x] 1 Baseline
              - [x] 1.1 Capture current behavior
            - [ ] 2 Execute task
              - [ ] 2.1 Run the workflow
              - Depends On:
                - `1`
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["action"] == "run_task_loop"
    assert payload["feature_id"] == "v1-f001"
    assert payload["task_id"] == "2"


def test_audit_workflow_accepts_resolvable_cross_feature_dependencies(tmp_path: Path) -> None:
    for fixture_name, archived_upstream in (("active", False), ("archived", True)):
        repo = _write_cross_feature_openspec_repo_fixture(tmp_path / fixture_name, archived_upstream=archived_upstream)

        result = subprocess.run(
            ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, result.stdout + result.stderr


def test_audit_workflow_reports_invalid_current_task_metadata(tmp_path: Path) -> None:
    repo = _write_invalid_current_task_openspec_repo_fixture(tmp_path)

    result = subprocess.run(
        ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "docs/planning/versions/v1/features/v1-f001-invalid-current-task.md" in result.stdout
    assert "Current Task must be `none` or a top-level OpenSpec task ID, got `1.1`" in result.stdout


def test_diagnose_workflow_reports_invalid_current_task_metadata(tmp_path: Path) -> None:
    repo = _write_invalid_current_task_openspec_repo_fixture(tmp_path)

    result = subprocess.run(
        ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["status"] == "issues_found"
    assert any(
        finding["code"] == "invalid_current_task_metadata"
        and finding["path"] == "docs/planning/versions/v1/features/v1-f001-invalid-current-task.md"
        and "Current Task must be `none` or a top-level OpenSpec task ID, got `1.1`" in finding["message"]
        for finding in payload["findings"]
    )


def test_resolve_start_task_selects_cross_feature_ready_task_with_active_upstream_change(tmp_path: Path) -> None:
    repo = _write_cross_feature_openspec_repo_fixture(tmp_path, archived_upstream=False)

    result = subprocess.run(
        ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["feature_id"] == "v1-f002"
    assert payload["feature_section"] == "READY"
    assert payload["task_id"] == "1"
    assert payload["task_title"] == "Resolve downstream task"


def test_resolve_start_task_selects_cross_feature_ready_task_with_archived_upstream_change(tmp_path: Path) -> None:
    repo = _write_cross_feature_openspec_repo_fixture(tmp_path, archived_upstream=True)

    result = subprocess.run(
        ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["feature_id"] == "v1-f002"
    assert payload["feature_section"] == "READY"
    assert payload["task_id"] == "1"
    assert payload["task_title"] == "Resolve downstream task"


def test_autonomous_resolver_selects_cross_feature_ready_task_with_active_upstream_change(tmp_path: Path) -> None:
    repo = _write_cross_feature_openspec_repo_fixture(tmp_path, archived_upstream=False)

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "action": "run_task_loop",
        "feature_id": "v1-f002",
        "feature_path": "docs/planning/versions/v1/features/v1-f002-downstream.md",
        "feature_section": "READY",
        "task_id": "1",
        "task_title": "Resolve downstream task",
    }


def test_autonomous_resolver_selects_cross_feature_ready_task_with_archived_upstream_change(tmp_path: Path) -> None:
    repo = _write_cross_feature_openspec_repo_fixture(tmp_path, archived_upstream=True)

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "action": "run_task_loop",
        "feature_id": "v1-f002",
        "feature_path": "docs/planning/versions/v1/features/v1-f002-downstream.md",
        "feature_section": "READY",
        "task_id": "1",
        "task_title": "Resolve downstream task",
    }


def test_resolve_autonomous_backlog_action_fails_when_feature_has_task_readiness_drift(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, feature_section="READY", task_statuses={"T01": "done", "T02": "todo"})

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "workflow-derived task readiness drift" in result.stderr.lower()


def test_resolve_autonomous_backlog_action_feature_id_path_fails_when_feature_has_task_readiness_drift(
    tmp_path: Path,
) -> None:
    repo = _write_repo_fixture(tmp_path, feature_section="READY", task_statuses={"T01": "done", "T02": "todo"})

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--feature-id", "v1-f999"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "workflow-derived task readiness drift" in result.stderr.lower()


def test_audit_workflow_reports_malformed_canonical_backlog_entries(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, task_statuses={"T01": "done", "T02": "done"})
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    backlog_path.write_text(
        textwrap.dedent(
            """\
            # V1 Backlog

            ## [BACKLOG]

            ### Missing backlog id

            ## [SHAPING]

            None yet.

            ## [READY]

            None yet.

            ## [IN_PROGRESS]

            ### `v1-f999` [Example](features/v1-f999-example.md)

            ## [DONE]

            None yet.

            ## [DEFER]

            None yet.
            """
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "malformed backlog entry" in result.stdout


def test_resolve_autonomous_backlog_action_preserves_normal_precedence(tmp_path: Path) -> None:
    repo = _write_autonomous_repo_fixture(
        tmp_path,
        backlog_items=["Backlog item"],
        shaping_features=[
            {"id": "v1-f010", "slug": "shape", "title": "Shape", "tasks": [("T01", "todo")]},
        ],
        ready_features=[
            {
                "id": "v1-f020",
                "slug": "ready",
                "title": "Ready",
                "tasks": [("T01", "ready")],
                "change_id": "ready-change",
            },
        ],
        in_progress_features=[
            {
                "id": "v1-f030",
                "slug": "active",
                "title": "Active",
                "tasks": [("T01", "done")],
                "change_id": "active-change",
            },
        ],
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "action": "run_task_loop",
        "feature_id": "v1-f020",
        "feature_path": "docs/planning/versions/v1/features/v1-f020-ready.md",
        "feature_section": "READY",
        "task_id": "T01",
        "task_title": "Task 1",
    }


def test_resolve_autonomous_backlog_action_design_mode_skips_ready_and_selects_shaping(tmp_path: Path) -> None:
    repo = _write_autonomous_repo_fixture(
        tmp_path,
        backlog_items=["Backlog item"],
        shaping_features=[
            {"id": "v1-f010", "slug": "shape", "title": "Shape", "tasks": [("T01", "todo")]},
        ],
        ready_features=[
            {
                "id": "v1-f020",
                "slug": "ready",
                "title": "Ready",
                "tasks": [("T01", "ready")],
                "change_id": "ready-change",
            },
        ],
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--design-mode"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "action": "ready_feature",
        "feature_id": "v1-f010",
        "feature_path": "docs/planning/versions/v1/features/v1-f010-shape.md",
        "feature_section": "SHAPING",
    }


def test_resolve_autonomous_backlog_action_design_mode_falls_back_to_backlog(tmp_path: Path) -> None:
    repo = _write_autonomous_repo_fixture(
        tmp_path,
        backlog_items=["First backlog item", "Second backlog item"],
        ready_features=[
            {
                "id": "v1-f020",
                "slug": "ready",
                "title": "Ready",
                "tasks": [("T01", "ready")],
                "change_id": "ready-change",
            },
        ],
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--design-mode"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "action": "shape_backlog_item",
        "backlog_index": 1,
        "backlog_title": "First backlog item",
    }


def test_resolve_autonomous_backlog_action_design_mode_reports_feature_exhausted_without_design_work(
    tmp_path: Path,
) -> None:
    repo = _write_autonomous_repo_fixture(
        tmp_path,
        ready_features=[
            {
                "id": "v1-f020",
                "slug": "ready",
                "title": "Ready",
                "tasks": [("T01", "ready")],
                "change_id": "ready-change",
            },
        ],
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--design-mode"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "action": "feature_exhausted",
        "reason": "design_mode_no_design_work",
    }


def test_resolve_autonomous_backlog_action_fails_when_ready_feature_is_missing_openspec_change_metadata(
    tmp_path: Path,
) -> None:
    repo = _write_repo_fixture(
        tmp_path,
        feature_section="READY",
        task_statuses={"T01": "ready", "T02": "todo"},
        include_openspec_change=False,
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "docs/planning/versions/v1/features/v1-f999-example.md is missing OpenSpec Change metadata" in result.stderr


def test_resolve_autonomous_backlog_action_does_not_route_around_malformed_active_feature(
    tmp_path: Path,
) -> None:
    repo = _write_autonomous_repo_fixture(
        tmp_path,
        ready_features=[
            {"id": "v1-f010", "slug": "broken", "title": "Broken", "tasks": [("T01", "ready")]},
            {
                "id": "v1-f020",
                "slug": "valid",
                "title": "Valid",
                "tasks": [("T01", "ready")],
                "change_id": "valid-change",
            },
        ],
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "docs/planning/versions/v1/features/v1-f010-broken.md is missing OpenSpec Change metadata" in result.stderr


def test_resolve_autonomous_backlog_action_fails_when_ready_feature_links_missing_active_change_dir(
    tmp_path: Path,
) -> None:
    repo = _write_autonomous_repo_fixture(
        tmp_path,
        ready_features=[
            {
                "id": "v1-f010",
                "slug": "broken",
                "title": "Broken",
                "tasks": [("T01", "ready")],
                "change_id": "missing-change",
                "create_change_dir": False,
            },
        ],
    )

    result = subprocess.run(
        ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert (
        "docs/planning/versions/v1/features/v1-f010-broken.md links missing active OpenSpec change directory "
        "openspec/changes/missing-change" in result.stderr
    )

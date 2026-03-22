from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path


SKILLS_ROOT = Path(__file__).resolve().parents[2]
AUDIT_SCRIPT = SKILLS_ROOT / "audit-workflow" / "scripts" / "audit_workflow.py"
START_TASK_SCRIPT = SKILLS_ROOT / "start-task" / "scripts" / "resolve_start_task.py"
SYNC_SCRIPT = SKILLS_ROOT / "_workflow" / "scripts" / "sync_task_readiness.py"
AUTONOMOUS_RESOLVER_SCRIPT = (
    SKILLS_ROOT / "autonomous-backlog-loop" / "scripts" / "resolve_autonomous_backlog_action.py"
)


def _write_repo_fixture(tmp_path: Path, *, feature_section: str = "IN_PROGRESS", task_statuses: dict[str, str]) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
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

    feature_text = textwrap.dedent(
        f"""\
        # Feature: Example

        ## 0. Meta
        - Feature ID: `v1-f999`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{feature_section.lower()}`
        - Current Task: `none`

        ## 6. Tasks

        ### T01: First task
        - Status: `{task_statuses["T01"]}`
        - Depends On:
          - none

        ### T02: Second task
        - Status: `{task_statuses["T02"]}`
        - Depends On:
          - `T01`
        """
    )
    (feature_dir / "v1-f999-example.md").write_text(feature_text, encoding="utf-8")
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
                    "- Current Task: `none`",
                    "",
                    "## 6. Tasks",
                    "",
                    *task_lines,
                    "",
                ]
            )
            (feature_dir / f"{feature['id']}-{feature['slug']}.md").write_text(feature_text, encoding="utf-8")

    return repo


def test_sync_task_readiness_promotes_eligible_tasks_in_place(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, task_statuses={"T01": "done", "T02": "todo"})
    feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f999-example.md"

    result = subprocess.run(
        ["python", str(SYNC_SCRIPT), "--feature-file", str(feature_file)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "- Status: `ready`" in feature_file.read_text(encoding="utf-8")


def test_audit_workflow_reports_ready_drift_for_promotable_todo_tasks(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, task_statuses={"T01": "done", "T02": "todo"})

    result = subprocess.run(
        ["python", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "could be `ready` but is still `todo`" in result.stdout


def test_resolve_start_task_fails_when_feature_has_task_readiness_drift(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, feature_section="READY", task_statuses={"T01": "done", "T02": "todo"})

    result = subprocess.run(
        ["python", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "task readiness drift" in result.stderr.lower()


def test_audit_workflow_accepts_resolvable_cross_feature_dependencies(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path, task_statuses={"T01": "done", "T02": "done"})
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"

    local_feature = textwrap.dedent(
        """\
        # Feature: Local

        ## 0. Meta
        - Feature ID: `v1-f002`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
        - Current Task: `none`

        ## 6. Tasks

        ### T01: First task
        - Status: `done`
        - Depends On:
          - none

        ### T02: Cross-feature dependent task
        - Status: `done`
        - Depends On:
          - `T01`
          - `v1-f001/T03`
        """
    )
    (feature_dir / "v1-f002-local.md").write_text(local_feature, encoding="utf-8")

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

        ### `v1-f002` [Local](features/v1-f002-local.md)

        ## [DONE]

        ### `v1-f001` [External](features/v1-f001-external.md)

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

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

    result = subprocess.run(
        ["python", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr


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
        ["python", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
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
            {"id": "v1-f020", "slug": "ready", "title": "Ready", "tasks": [("T01", "ready")]},
        ],
        in_progress_features=[
            {"id": "v1-f030", "slug": "active", "title": "Active", "tasks": [("T01", "done")]},
        ],
    )

    result = subprocess.run(
        ["python", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo)],
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
            {"id": "v1-f020", "slug": "ready", "title": "Ready", "tasks": [("T01", "ready")]},
        ],
    )

    result = subprocess.run(
        ["python", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--design-mode"],
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
            {"id": "v1-f020", "slug": "ready", "title": "Ready", "tasks": [("T01", "ready")]},
        ],
    )

    result = subprocess.run(
        ["python", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--design-mode"],
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
            {"id": "v1-f020", "slug": "ready", "title": "Ready", "tasks": [("T01", "ready")]},
        ],
    )

    result = subprocess.run(
        ["python", str(AUTONOMOUS_RESOLVER_SCRIPT), "--repo-root", str(repo), "--design-mode"],
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

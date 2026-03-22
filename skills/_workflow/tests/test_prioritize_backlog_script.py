from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

from _workflow.workflow_state import parse_backlog_document


SKILLS_ROOT = Path(__file__).resolve().parents[2]
PRIORITIZE_SCRIPT = SKILLS_ROOT / "prioritize-backlog" / "scripts" / "prioritize_backlog.py"


def _write_feature(
    feature_dir: Path,
    *,
    feature_id: str,
    slug: str,
    title: str,
    section_name: str,
    first_status: str = "ready",
    second_status: str = "todo",
) -> None:
    feature_text = textwrap.dedent(
        f"""\
        # Feature: {title}

        ## 0. Meta
        - Feature ID: `{feature_id}`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{section_name.lower()}`
        - Current Task: `none`

        ## 1. Problem
        Improve {title.lower()} handling.

        ## 2. Goal
        Make {title.lower()} easier to execute safely.

        ## 3. Scope
        Only update the workflow path for {title.lower()}.

        ## 6. Tasks

        ### T01: First task
        - Status: `{first_status}`
        - Depends On:
          - none

        ### T02: Second task
        - Status: `{second_status}`
        - Depends On:
          - `T01`
        """
    )
    (feature_dir / f"{feature_id}-{slug}.md").write_text(feature_text, encoding="utf-8")


def _write_repo_fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))

    backlog = textwrap.dedent(
        """\
        # V1 Backlog

        ## [BACKLOG]

        ### `v1-b001` Improve repo docs
        ### `v1-b002` Reduce onboarding friction

        ## [SHAPING]

        ### `v1-f001` [Clarify workflow](features/v1-f001-clarify-workflow.md)
        ### `v1-f002` [Stabilize templates](features/v1-f002-stabilize-templates.md)

        ## [READY]

        ### `v1-f003` [Tighten checks](features/v1-f003-tighten-checks.md)
        ### `v1-f004` [Simplify defaults](features/v1-f004-simplify-defaults.md)

        ## [IN_PROGRESS]

        ### `v1-f099` [Leave alone](features/v1-f099-leave-alone.md)

        ## [DONE]

        ### `v1-f050` [Already done](features/v1-f050-already-done.md)

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    _write_feature(
        feature_dir,
        feature_id="v1-f001",
        slug="clarify-workflow",
        title="Clarify workflow",
        section_name="SHAPING",
    )
    _write_feature(
        feature_dir,
        feature_id="v1-f002",
        slug="stabilize-templates",
        title="Stabilize templates",
        section_name="SHAPING",
        first_status="todo",
    )
    _write_feature(
        feature_dir,
        feature_id="v1-f003",
        slug="tighten-checks",
        title="Tighten checks",
        section_name="READY",
    )
    _write_feature(
        feature_dir,
        feature_id="v1-f004",
        slug="simplify-defaults",
        title="Simplify defaults",
        section_name="READY",
    )
    _write_feature(
        feature_dir,
        feature_id="v1-f099",
        slug="leave-alone",
        title="Leave alone",
        section_name="IN_PROGRESS",
        first_status="in_progress",
    )
    _write_feature(
        feature_dir,
        feature_id="v1-f050",
        slug="already-done",
        title="Already done",
        section_name="DONE",
        first_status="done",
        second_status="done",
    )

    return repo


def test_prioritize_backlog_list_returns_only_eligible_items_with_feature_context(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path)

    result = subprocess.run(
        ["python", str(PRIORITIZE_SCRIPT), "--repo-root", str(repo), "list"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    ids = [item["id"] for item in payload["items"]]
    assert ids == ["v1-b001", "v1-b002", "v1-f001", "v1-f002", "v1-f003", "v1-f004"]

    feature_item = next(item for item in payload["items"] if item["id"] == "v1-f001")
    assert feature_item["feature_path"] == "docs/planning/versions/v1/features/v1-f001-clarify-workflow.md"
    assert feature_item["problem"] == "Improve clarify workflow handling."
    assert feature_item["goal"] == "Make clarify workflow easier to execute safely."
    assert feature_item["task_counts"] == {"ready": 1, "todo": 1}


def test_prioritize_backlog_apply_reorders_each_eligible_section_from_global_order(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path)
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"

    result = subprocess.run(
        [
            "python",
            str(PRIORITIZE_SCRIPT),
            "--repo-root",
            str(repo),
            "apply",
            "--ordered-id",
            "v1-f002",
            "--ordered-id",
            "v1-b002",
            "--ordered-id",
            "v1-f004",
            "--ordered-id",
            "v1-f001",
            "--ordered-id",
            "v1-b001",
            "--ordered-id",
            "v1-f003",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["changed"] is True

    parsed = parse_backlog_document(backlog_path.read_text(encoding="utf-8"))
    assert [item.backlog_id for item in parsed.backlog_items] == ["v1-b002", "v1-b001"]
    assert [entry.feature_id for entry in parsed.feature_sections["SHAPING"]] == ["v1-f002", "v1-f001"]
    assert [entry.feature_id for entry in parsed.feature_sections["READY"]] == ["v1-f004", "v1-f003"]
    assert [entry.feature_id for entry in parsed.feature_sections["IN_PROGRESS"]] == ["v1-f099"]
    assert [entry.feature_id for entry in parsed.feature_sections["DONE"]] == ["v1-f050"]

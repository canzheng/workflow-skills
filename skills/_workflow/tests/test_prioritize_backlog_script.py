from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

from _workflow.workflow_state import parse_backlog_document


from _workflow.cli_helpers import resolve_skills_root

SKILLS_ROOT = resolve_skills_root(Path(__file__))
PRIORITIZE_SCRIPT = SKILLS_ROOT / "prioritize-backlog" / "scripts" / "prioritize_backlog.py"


def _write_feature(
    repo: Path,
    feature_dir: Path,
    *,
    feature_id: str,
    slug: str,
    title: str,
    section_name: str,
    change_id: str,
    first_done: bool = False,
) -> None:
    feature_text = textwrap.dedent(
        f"""\
        # Feature: {title}

        ## 0. Meta
        - Feature ID: `{feature_id}`
        - Version: `v1`
        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{section_name.lower()}`
        - OpenSpec Change: `{change_id}`
        - OpenSpec Specs:
          - `openspec/specs/workflow-board-lifecycle/spec.md`
        - Current Task: `none`

        ## 1. Validation Log
        - None yet.

        ## 2. Handoff Notes
        - None yet.
        """
    )
    (feature_dir / f"{feature_id}-{slug}.md").write_text(feature_text, encoding="utf-8")

    change_dir = repo / "openspec" / "changes" / change_id
    (change_dir / "specs" / "workflow-board-lifecycle").mkdir(parents=True, exist_ok=True)
    (change_dir / "proposal.md").write_text(
        f"# Proposal\n\nImprove {title.lower()} prioritization context.\n",
        encoding="utf-8",
    )
    (change_dir / "design.md").write_text(
        f"# Design\n\nUse OpenSpec context for {title.lower()}.\n",
        encoding="utf-8",
    )
    (change_dir / "tasks.md").write_text(
        textwrap.dedent(
            f"""\
            ## 1. Work

            - [{"x" if first_done else " "}] 1 First task
              - [{"x" if first_done else " "}] 1.1 Prepare context
            - [ ] 2 Second task
              - [ ] 2.1 Execute the change
              - Depends On:
                - `1`
            """
        ),
        encoding="utf-8",
    )
    (change_dir / "specs" / "workflow-board-lifecycle" / "spec.md").write_text(
        f"# Delta\n\nContext for {title.lower()}.\n",
        encoding="utf-8",
    )


def _write_repo_fixture(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"
    feature_dir.mkdir(parents=True)
    (repo / "docs" / "planning").mkdir(parents=True, exist_ok=True)
    (repo / "docs" / "planning" / "current_version").symlink_to(Path("versions/v1"))
    (repo / "openspec" / "changes" / "archive").mkdir(parents=True, exist_ok=True)

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

        None yet.

        ## [DONE]

        None yet.

        ## [DEFER]

        None yet.
        """
    )
    (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").write_text(backlog, encoding="utf-8")

    _write_feature(
        repo,
        feature_dir,
        feature_id="v1-f001",
        slug="clarify-workflow",
        title="Clarify workflow",
        section_name="SHAPING",
        change_id="clarify-workflow",
        first_done=False,
    )
    _write_feature(
        repo,
        feature_dir,
        feature_id="v1-f002",
        slug="stabilize-templates",
        title="Stabilize templates",
        section_name="SHAPING",
        change_id="stabilize-templates",
        first_done=True,
    )
    _write_feature(
        repo,
        feature_dir,
        feature_id="v1-f003",
        slug="tighten-checks",
        title="Tighten checks",
        section_name="READY",
        change_id="tighten-checks",
        first_done=False,
    )
    _write_feature(
        repo,
        feature_dir,
        feature_id="v1-f004",
        slug="simplify-defaults",
        title="Simplify defaults",
        section_name="READY",
        change_id="simplify-defaults",
        first_done=False,
    )

    return repo


def test_prioritize_backlog_list_returns_only_eligible_items_with_openspec_context(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path)

    result = subprocess.run(
        ["python3", str(PRIORITIZE_SCRIPT), "--repo-root", str(repo), "list"],
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
    assert feature_item["openspec_change_id"] == "clarify-workflow"
    assert feature_item["openspec_context_files"] == [
        "openspec/changes/clarify-workflow/proposal.md",
        "openspec/changes/clarify-workflow/design.md",
        "openspec/changes/clarify-workflow/tasks.md",
        "openspec/changes/clarify-workflow/specs/workflow-board-lifecycle/spec.md",
    ]
    assert feature_item["proposal"] == "Improve clarify workflow prioritization context."
    assert feature_item["design"] == "Use OpenSpec context for clarify workflow."
    assert feature_item["tasks_summary"] == "- [ ] 1 First task - [ ] 1.1 Prepare context - [ ] 2 Second task - [ ] 2.1 Execute the change - Depends On: - `1`"
    assert feature_item["task_counts"] == {"ready": 1, "todo": 1}


def test_prioritize_backlog_apply_reorders_each_eligible_section_from_global_order(tmp_path: Path) -> None:
    repo = _write_repo_fixture(tmp_path)
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"

    result = subprocess.run(
        [
            "python3",
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
    assert parsed.feature_sections["IN_PROGRESS"] == []
    assert parsed.feature_sections["DONE"] == []

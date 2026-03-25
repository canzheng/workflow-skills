from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = REPO_ROOT / "skills" / "initialize-workflow-artifacts" / "scripts" / "init_workflow_artifacts.py"
AUDIT_SCRIPT = REPO_ROOT / "skills" / "audit-workflow" / "scripts" / "audit_workflow.py"
START_TASK_SCRIPT = REPO_ROOT / "skills" / "start-task" / "scripts" / "resolve_start_task.py"
COMPLETE_TASK_SCRIPT = REPO_ROOT / "skills" / "complete-task" / "scripts" / "resolve_complete_task.py"
FINISH_FEATURE_SCRIPT = REPO_ROOT / "skills" / "finish-feature" / "scripts" / "resolve_finish_feature.py"

_SPEC = importlib.util.spec_from_file_location("init_workflow_artifacts", INIT_SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
initialize = _MODULE.initialize


def _write_implementation_plan(change_dir: Path, task_id: str) -> None:
    implementation_plan_dir = change_dir / "implementation-plans"
    implementation_plan_dir.mkdir(parents=True, exist_ok=True)
    (implementation_plan_dir / f"{task_id}.md").write_text(
        f"# Task {task_id} Implementation Plan\n\n- Objective: Execute task {task_id}.\n",
        encoding="utf-8",
    )


class WorkflowOpenSpecIntegrationTests(unittest.TestCase):
    def test_audit_workflow_fails_when_openspec_scaffold_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

            # Simulate a repo that has planning artifacts but not the required OpenSpec scaffold.
            openspec_root = repo / "openspec"
            if openspec_root.exists():
                for path in sorted(openspec_root.rglob("*"), reverse=True):
                    if path.is_file() or path.is_symlink():
                        path.unlink()
                    elif path.is_dir():
                        path.rmdir()
                openspec_root.rmdir()

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("openspec", result.stdout.lower())

    def test_start_task_resolves_next_ready_task_from_linked_openspec_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [IN_PROGRESS]

                    None yet.

                    ## [DONE]

                    ### `v1-f999` [Done feature](features/v1-f999-done-feature.md)

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )
            done_feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f999-done-feature.md"
            done_feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Done feature

                    ## 0. Meta
                    - Feature ID: `v1-f999`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
                    - OpenSpec Change: `done-change`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                      - [x] 1.1 Capture current behavior
                    - [ ] 2 Wire task parsing
                      - [ ] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    - [ ] 3 Start-task integration
                      - [ ] 3.1 Use shared task context
                      - Depends On:
                        - `2`
                    """
                ),
                encoding="utf-8",
            )
            (change_dir / "notes.md").write_text("# Notes\n\nExtra context\n", encoding="utf-8")
            _write_implementation_plan(change_dir, "2")
            done_change_dir = repo / "openspec" / "changes" / "done-change"
            done_change_dir.mkdir(parents=True, exist_ok=True)
            (done_change_dir / "proposal.md").write_text("## Why\n\nDone\n", encoding="utf-8")
            (done_change_dir / "design.md").write_text("## Context\n\nDone\n", encoding="utf-8")
            (done_change_dir / "tasks.md").write_text("- [x] 1 Wrapped up\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f001")
            self.assertEqual(payload["task_id"], "2")
            self.assertEqual(
                payload["openspec_change_path"],
                "openspec/changes/integrate-openspec-shaping-readiness",
            )
            self.assertEqual(
                payload["implementation_plan_path"],
                "openspec/changes/integrate-openspec-shaping-readiness/implementation-plans/2.md",
            )
            self.assertEqual(
                payload["openspec_context_files"],
                [
                    "openspec/changes/integrate-openspec-shaping-readiness/proposal.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/design.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/tasks.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/notes.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/implementation-plans/2.md",
                ],
            )
            self.assertIn("write or update the implementation plan", payload["execution_instruction"])

    def test_complete_task_resolves_active_task_with_linked_openspec_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `2`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                    - [ ] 2 Wire task parsing
                      - [x] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )
            (change_dir / "notes.md").write_text("# Notes\n\nExtra context\n", encoding="utf-8")
            _write_implementation_plan(change_dir, "2")

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f001")
            self.assertEqual(payload["task_id"], "2")
            self.assertEqual(
                payload["implementation_plan_path"],
                "openspec/changes/integrate-openspec-shaping-readiness/implementation-plans/2.md",
            )
            self.assertEqual(
                payload["openspec_context_files"],
                [
                    "openspec/changes/integrate-openspec-shaping-readiness/proposal.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/design.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/tasks.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/notes.md",
                    "openspec/changes/integrate-openspec-shaping-readiness/implementation-plans/2.md",
                ],
            )
            self.assertIn("Read the files listed as context", payload["execution_instruction"])

    def test_complete_task_rejects_active_top_level_task_with_open_nested_checklist_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `2`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                    - [ ] 2 Wire task parsing
                      - [ ] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )
            _write_implementation_plan(change_dir, "2")

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("nested checklist", result.stderr)

    def test_complete_task_reports_in_progress_handoff_when_more_work_remains(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `1`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [ ] 1 Seed baseline
                    - [ ] 2 Wire task parsing
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )
            _write_implementation_plan(change_dir, "1")

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(
                payload["completion_handoff"],
                {
                    "all_top_level_tasks_complete": False,
                    "decision": "stay_in_progress",
                    "next_ready_task_ids": ["2"],
                    "remaining_open_task_ids": ["2"],
                },
            )

    def test_complete_task_reports_explicit_done_handoff_when_final_task_completes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `1`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [ ] 1 Seed baseline
                    """
                ),
                encoding="utf-8",
            )
            _write_implementation_plan(change_dir, "1")

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(
                payload["completion_handoff"],
                {
                    "all_top_level_tasks_complete": True,
                    "decision": "confirm_feature_acceptance",
                    "next_ready_task_ids": [],
                    "remaining_open_task_ids": [],
                },
            )

    def test_final_task_handoff_does_not_make_finish_feature_startable_while_feature_stays_in_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `2`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                    - [ ] 2 Final integration
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )
            _write_implementation_plan(change_dir, "2")

            complete_result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(complete_result.returncode, 0, complete_result.stdout + complete_result.stderr)
            complete_payload = json.loads(complete_result.stdout)
            self.assertEqual(complete_payload["completion_handoff"]["decision"], "confirm_feature_acceptance")

            finish_result = subprocess.run(
                ["python3", str(FINISH_FEATURE_SCRIPT), "--repo-root", str(repo), "--feature-id", "v1-f001"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(finish_result.returncode, 0)
            self.assertIn("feature v1-f001 is not in [DONE]", finish_result.stderr)

    def test_final_task_handoff_becomes_finish_feature_startable_after_feature_moves_to_done(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [OpenSpec integration](features/v1-f001-openspec-integration.md)

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: OpenSpec integration

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
                    - OpenSpec Change: `integrate-openspec-shaping-readiness`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-board-lifecycle/spec.md`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - `2026-03-26` Task `2`: feature acceptance satisfied after the final task handoff.

                    ## 2. Handoff Notes
                    - `2026-03-26`: Ready for `finish-feature`.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                    - [x] 2 Final integration
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )

            finish_result = subprocess.run(
                ["python3", str(FINISH_FEATURE_SCRIPT), "--repo-root", str(repo), "--feature-id", "v1-f001"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(finish_result.returncode, 0, finish_result.stdout + finish_result.stderr)
            finish_payload = json.loads(finish_result.stdout)
            self.assertEqual(finish_payload["feature_id"], "v1-f001")
            self.assertTrue(finish_payload["requires_archive"])
            self.assertEqual(
                finish_payload["active_change_path"],
                "openspec/changes/integrate-openspec-shaping-readiness",
            )

    def test_audit_accepts_legacy_exempt_done_feature_without_openspec_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [Historical feature](features/v1-f001-historical-feature.md)

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-historical-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Historical feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
                    - OpenSpec Status: `legacy-exempt`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - Historical feature predates OpenSpec adoption.

                    ## 2. Handoff Notes
                    - None yet.
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

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_audit_accepts_done_feature_with_archived_openspec_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-archived-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Archived feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
                    - OpenSpec Change: `archived-feature`
                    - OpenSpec Specs:
                      - `openspec/specs/workflow-audit-and-repair/spec.md`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - Archived after completion.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            archive_dir = repo / "openspec" / "changes" / "archive" / "2026-03-25-archived-feature"
            archive_dir.mkdir(parents=True, exist_ok=True)
            (archive_dir / "proposal.md").write_text("proposal", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_audit_rejects_done_feature_without_archived_change_or_legacy_exemption(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [Broken migrated feature](features/v1-f001-broken-migrated-feature.md)

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-broken-migrated-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Broken migrated feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
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

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("legacy-exempt", result.stdout)

    def test_audit_rejects_old_format_active_feature_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

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

                    ### `v1-f001` [Legacy formatted feature](features/v1-f001-legacy-formatted-feature.md)

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-legacy-formatted-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Legacy formatted feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `legacy-formatted-feature`
                    - Current Task: `none`

                    ## 1. Problem
                    - Old feature layout still present.

                    ## 2. Goal
                    - Should be rejected by audit.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "legacy-formatted-feature"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [ ] 1 Do it\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("legacy inline planning sections", result.stdout)


if __name__ == "__main__":
    unittest.main()

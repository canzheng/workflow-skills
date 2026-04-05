from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

from skills._workflow.workflow_state import find_openspec_task_structure_errors


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = REPO_ROOT / "skills" / "initialize-workflow-artifacts" / "scripts" / "init_workflow_artifacts.py"
AUDIT_SCRIPT = REPO_ROOT / "skills" / "audit-workflow" / "scripts" / "audit_workflow.py"
START_TASK_SCRIPT = REPO_ROOT / "skills" / "start-task" / "scripts" / "resolve_start_task.py"
AUTONOMOUS_RESOLVER_SCRIPT = (
    REPO_ROOT / "skills" / "autonomous-backlog-loop" / "scripts" / "resolve_autonomous_backlog_action.py"
)
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
        textwrap.dedent(
            f"""\
            # Task {task_id} Implementation Plan

            ## Objective

            Execute task {task_id}.

            ## Contract Surface

            - Change Type: `behavioral`
            - Workflow Surface: `resolver fixture`

            ## Proof Obligations

            - Resolver fixtures must satisfy the workflow implementation-plan contract.

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


def _write_task_validation_log(feature_file: Path, *, task_id: str, evidence_categories: str) -> None:
    feature_text = feature_file.read_text(encoding="utf-8")
    validation_log_start = feature_text.index("## 1. Validation Log")
    handoff_notes_start = feature_text.index("## 2. Handoff Notes")
    feature_file.write_text(
        (
            feature_text[:validation_log_start]
            + textwrap.dedent(
                f"""\
                ## 1. Validation Log
                - `2026-04-05` Task `{task_id}` Completion:
                  - Run: `python -m pytest`
                  - Result: `pass`
                  - Evidence: `{evidence_categories}`

                """
            )
            + feature_text[handoff_notes_start:]
        ),
        encoding="utf-8",
    )


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _write_active_change_linkage_fixture(repo: Path, *, orphaned: bool) -> None:
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"

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

    linked_change_id = "linked-change" if orphaned else "orphan-change"
    feature_file = feature_dir / "v1-f001-linked-feature.md"
    feature_file.write_text(
        textwrap.dedent(
            f"""\
            # Feature: Linked feature

            ## 0. Meta
            - Feature ID: `v1-f001`
            - Version: `v1`
            - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
            - OpenSpec Change: `{linked_change_id}`
            - OpenSpec Specs:
              - `openspec/specs/workflow-audit-and-repair/spec.md`
            - Current Task: `none`

            ## 1. Validation Log
            - None yet.

            ## 2. Handoff Notes
            - None yet.
            """
        ),
        encoding="utf-8",
    )

    linked_change = repo / "openspec" / "changes" / linked_change_id
    linked_change.mkdir(parents=True, exist_ok=True)
    (linked_change / "proposal.md").write_text("proposal", encoding="utf-8")
    (linked_change / "design.md").write_text("design", encoding="utf-8")
    (linked_change / "tasks.md").write_text("- [ ] 1 Do linked work\n", encoding="utf-8")

    if orphaned:
        orphan_change = repo / "openspec" / "changes" / "orphan-change"
        orphan_change.mkdir(parents=True, exist_ok=True)
        (orphan_change / "proposal.md").write_text("proposal", encoding="utf-8")
        (orphan_change / "design.md").write_text("design", encoding="utf-8")
        (orphan_change / "tasks.md").write_text("- [ ] 1 Orphan work\n", encoding="utf-8")


def _write_cross_feature_start_task_fixture(repo: Path, *, archived_upstream: bool) -> None:
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"

    backlog_path.write_text(
        textwrap.dedent(
            f"""\
            # V1 Backlog

            ## [BACKLOG]

            None yet.

            ## [SHAPING]

            None yet.

            ## [READY]

            ### `v1-f002` [Downstream feature](features/v1-f002-downstream-feature.md)

            ## [IN_PROGRESS]

            {"### `v1-f001` [Upstream feature](features/v1-f001-upstream-feature.md)" if not archived_upstream else "None yet."}

            ## [DONE]

            {"### `v1-f001` [Upstream feature](features/v1-f001-upstream-feature.md)" if archived_upstream else "None yet."}

            ## [DEFER]

            None yet.
            """
        ),
        encoding="utf-8",
    )

    upstream_section = "done" if archived_upstream else "in_progress"
    upstream_feature_file = feature_dir / "v1-f001-upstream-feature.md"
    upstream_feature_file.write_text(
        textwrap.dedent(
            f"""\
            # Feature: Upstream feature

            ## 0. Meta
            - Feature ID: `v1-f001`
            - Version: `v1`
            - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#{upstream_section}`
            - OpenSpec Change: `upstream-feature-change`
            - OpenSpec Specs:
              - `openspec/specs/task-execution-handoff/spec.md`
            - Current Task: `none`

            ## 1. Validation Log
            - None yet.

            ## 2. Handoff Notes
            - None yet.
            """
        ),
        encoding="utf-8",
    )

    downstream_feature_file = feature_dir / "v1-f002-downstream-feature.md"
    downstream_feature_file.write_text(
        textwrap.dedent(
            """\
            # Feature: Downstream feature

            ## 0. Meta
            - Feature ID: `v1-f002`
            - Version: `v1`
            - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
            - OpenSpec Change: `downstream-feature-change`
            - OpenSpec Specs:
              - `openspec/specs/task-execution-handoff/spec.md`
            - Current Task: `none`

            ## 1. Validation Log
            - None yet.

            ## 2. Handoff Notes
            - None yet.
            """
        ),
        encoding="utf-8",
    )

    downstream_change_dir = repo / "openspec" / "changes" / "downstream-feature-change"
    downstream_change_dir.mkdir(parents=True, exist_ok=True)
    (downstream_change_dir / "proposal.md").write_text("## Why\n\nDownstream\n", encoding="utf-8")
    (downstream_change_dir / "design.md").write_text("## Context\n\nDownstream\n", encoding="utf-8")
    (downstream_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Downstream work

            - [ ] 1 Resolve downstream task
              - [ ] 1.1 Execute downstream work
              - Depends On:
                - `v1-f001/1`
            - [ ] 2 Follow-up work
              - [ ] 2.1 Finish later
              - Depends On:
                - `1`
            """
        ),
        encoding="utf-8",
    )
    _write_implementation_plan(downstream_change_dir, "1")

    upstream_tasks = textwrap.dedent(
        """\
        ## 1. Upstream work

        - [x] 1 Completed upstream task
          - [x] 1.1 Land prerequisite work
        """
    )
    if archived_upstream:
        archive_dir = repo / "openspec" / "changes" / "archive" / "2026-03-27-upstream-feature-change"
        archive_dir.mkdir(parents=True, exist_ok=True)
        (archive_dir / "proposal.md").write_text("## Why\n\nArchived upstream\n", encoding="utf-8")
        (archive_dir / "tasks.md").write_text(upstream_tasks, encoding="utf-8")
    else:
        upstream_change_dir = repo / "openspec" / "changes" / "upstream-feature-change"
        upstream_change_dir.mkdir(parents=True, exist_ok=True)
        (upstream_change_dir / "proposal.md").write_text("## Why\n\nUpstream\n", encoding="utf-8")
        (upstream_change_dir / "design.md").write_text("## Context\n\nUpstream\n", encoding="utf-8")
        (upstream_change_dir / "tasks.md").write_text(upstream_tasks, encoding="utf-8")


def _write_complete_task_legacy_exempt_fixture(repo: Path, *, missing_active_change: bool = False) -> None:
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    feature_dir = repo / "docs" / "planning" / "versions" / "v1" / "features"

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

            ### `v1-f002` [Active feature](features/v1-f002-active-feature.md)

            ## [DONE]

            ### `v1-f001` [Historical feature](features/v1-f001-historical-feature.md)

            ## [DEFER]

            None yet.
            """
        ),
        encoding="utf-8",
    )

    active_feature_file = feature_dir / "v1-f002-active-feature.md"
    active_feature_lines = [
        "# Feature: Active feature",
        "",
        "## 0. Meta",
        "- Feature ID: `v1-f002`",
        "- Version: `v1`",
        "- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`",
    ]
    if not missing_active_change:
        active_feature_lines.append("- OpenSpec Change: `active-feature-change`")
    active_feature_lines.extend(
        [
            "- OpenSpec Specs:",
            "  - `openspec/specs/task-execution-handoff/spec.md`",
            "- Current Task: `1`",
            "",
            "## 1. Validation Log",
            "- `2026-04-05` Task `1` Completion:",
            "  - Run: `python -m pytest`",
            "  - Result: `pass`",
            "  - Evidence: `runtime_path`",
            "",
            "## 2. Handoff Notes",
            "- None yet.",
            "",
        ]
    )
    active_feature_file.write_text("\n".join(active_feature_lines), encoding="utf-8")

    historical_feature_file = feature_dir / "v1-f001-historical-feature.md"
    historical_feature_file.write_text(
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

    if missing_active_change:
        return

    active_change_dir = repo / "openspec" / "changes" / "active-feature-change"
    active_change_dir.mkdir(parents=True, exist_ok=True)
    (active_change_dir / "proposal.md").write_text("## Why\n\nActive\n", encoding="utf-8")
    (active_change_dir / "design.md").write_text("## Context\n\nActive\n", encoding="utf-8")
    (active_change_dir / "tasks.md").write_text(
        textwrap.dedent(
            """\
            ## 1. Active task

            - [ ] 1 Finish active task
              - [x] 1.1 Existing task work is complete
            """
        ),
        encoding="utf-8",
    )
    _write_implementation_plan(active_change_dir, "1")


class WorkflowOpenSpecIntegrationTests(unittest.TestCase):
    def test_repo_sample_change_task_files_use_parent_top_level_structure(self) -> None:
        invalid_task_files: dict[str, list[str]] = {}
        archive_root = REPO_ROOT / "openspec" / "changes" / "archive"

        for tasks_path in sorted((REPO_ROOT / "openspec" / "changes").rglob("tasks.md")):
            if archive_root in tasks_path.parents:
                continue
            errors = find_openspec_task_structure_errors(tasks_path.read_text(encoding="utf-8"))
            if errors:
                invalid_task_files[str(tasks_path.relative_to(REPO_ROOT))] = errors

        self.assertEqual(invalid_task_files, {})

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

    def test_start_task_prefers_existing_feature_worktree_for_later_tasks(self) -> None:
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

            change_dir = repo / "openspec" / "changes" / "integrate-openspec-shaping-readiness"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("## Why\n\nTest\n", encoding="utf-8")
            (change_dir / "design.md").write_text("## Context\n\nTest\n", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [ ] 1 Seed baseline
                      - [ ] 1.1 Capture current behavior
                    - [ ] 2 Wire task parsing
                      - [ ] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )

            init_result = _git(repo, "init", "-b", "main")
            self.assertEqual(init_result.returncode, 0, init_result.stdout + init_result.stderr)
            self.assertEqual(_git(repo, "config", "user.name", "Test User").returncode, 0)
            self.assertEqual(_git(repo, "config", "user.email", "test@example.com").returncode, 0)
            self.assertEqual(_git(repo, "add", ".").returncode, 0)
            commit_result = _git(repo, "commit", "-m", "initial workflow state")
            self.assertEqual(commit_result.returncode, 0, commit_result.stdout + commit_result.stderr)

            worktree_root = Path(tmpdir) / "worktrees"
            worktree_root.mkdir()
            feature_worktree = worktree_root / "v1-f001-openspec-integration"
            add_worktree_result = _git(
                repo,
                "worktree",
                "add",
                "-b",
                "v1-f001-openspec-integration",
                str(feature_worktree),
            )
            self.assertEqual(add_worktree_result.returncode, 0, add_worktree_result.stdout + add_worktree_result.stderr)

            feature_backlog = feature_worktree / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
            feature_backlog.write_text(
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

            feature_worktree_file = (
                feature_worktree / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            )
            feature_worktree_file.write_text(
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
                    - Current Task: `none`

                    ## 1. Validation Log
                    - 2026-03-28: task 1 completed on the feature branch

                    ## 2. Handoff Notes
                    - Feature worktree is ready for the next task.
                    """
                ),
                encoding="utf-8",
            )
            (feature_worktree / "openspec" / "changes" / "integrate-openspec-shaping-readiness" / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                      - [x] 1.1 Capture current behavior
                    - [ ] 2 Wire task parsing
                      - [ ] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )
            _write_implementation_plan(
                feature_worktree / "openspec" / "changes" / "integrate-openspec-shaping-readiness",
                "2",
            )
            self.assertEqual(_git(feature_worktree, "add", ".").returncode, 0)
            worktree_commit_result = _git(feature_worktree, "commit", "-m", "progress task state on feature branch")
            self.assertEqual(
                worktree_commit_result.returncode,
                0,
                worktree_commit_result.stdout + worktree_commit_result.stderr,
            )

            result = subprocess.run(
                ["python3", str(START_TASK_SCRIPT)],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f001")
            self.assertEqual(payload["feature_section"], "IN_PROGRESS")
            self.assertEqual(payload["task_id"], "2")
            self.assertEqual(payload["selected_repo_root"], str(feature_worktree.resolve()))

    def test_autonomous_resolver_prefers_existing_feature_worktree_for_feature_continuation(self) -> None:
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

                    - [ ] 1 Seed baseline
                      - [ ] 1.1 Capture current behavior
                    - [ ] 2 Wire task parsing
                      - [ ] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )

            init_result = _git(repo, "init", "-b", "main")
            self.assertEqual(init_result.returncode, 0, init_result.stdout + init_result.stderr)
            self.assertEqual(_git(repo, "config", "user.name", "Test User").returncode, 0)
            self.assertEqual(_git(repo, "config", "user.email", "test@example.com").returncode, 0)
            self.assertEqual(_git(repo, "add", ".").returncode, 0)
            commit_result = _git(repo, "commit", "-m", "initial workflow state")
            self.assertEqual(commit_result.returncode, 0, commit_result.stdout + commit_result.stderr)

            worktree_root = Path(tmpdir) / "worktrees"
            worktree_root.mkdir()
            feature_worktree = worktree_root / "v1-f001-openspec-integration"
            add_worktree_result = _git(
                repo,
                "worktree",
                "add",
                "-b",
                "v1-f001-openspec-integration",
                str(feature_worktree),
            )
            self.assertEqual(add_worktree_result.returncode, 0, add_worktree_result.stdout + add_worktree_result.stderr)

            feature_worktree_file = (
                feature_worktree / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            )
            feature_worktree_file.write_text(
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
                    - Current Task: `none`

                    ## 1. Validation Log
                    - 2026-03-28: task 1 completed on the feature branch

                    ## 2. Handoff Notes
                    - Feature worktree is ready for the next task.
                    """
                ),
                encoding="utf-8",
            )
            (feature_worktree / "openspec" / "changes" / "integrate-openspec-shaping-readiness" / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Setup

                    - [x] 1 Seed baseline
                      - [x] 1.1 Capture current behavior
                    - [ ] 2 Wire task parsing
                      - [ ] 2.1 Update helper code
                      - Depends On:
                        - `1`
                    """
                ),
                encoding="utf-8",
            )
            self.assertEqual(_git(feature_worktree, "add", ".").returncode, 0)
            worktree_commit_result = _git(feature_worktree, "commit", "-m", "progress task state on feature branch")
            self.assertEqual(
                worktree_commit_result.returncode,
                0,
                worktree_commit_result.stdout + worktree_commit_result.stderr,
            )

            result = subprocess.run(
                ["python3", str(AUTONOMOUS_RESOLVER_SCRIPT), "--feature-id", "v1-f001"],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f001")
            self.assertEqual(payload["feature_section"], "IN_PROGRESS")
            self.assertEqual(payload["task_id"], "2")

    def test_start_task_rejects_missing_implementation_plan(self) -> None:
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
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "task implementation plan is missing: "
                "openspec/changes/integrate-openspec-shaping-readiness/implementation-plans/2.md",
                result.stderr,
            )

    def test_start_task_rejects_structurally_invalid_implementation_plan(self) -> None:
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
            implementation_plan_dir = change_dir / "implementation-plans"
            implementation_plan_dir.mkdir(parents=True, exist_ok=True)
            (implementation_plan_dir / "2.md").write_text(
                "# Task 2 Implementation Plan\n\n- Objective: weak plan fixture.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task implementation plan is invalid:", result.stderr)
            self.assertIn("## Contract Surface", result.stderr)

    def test_start_task_resolves_cross_feature_ready_task_with_active_upstream_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_cross_feature_start_task_fixture(repo, archived_upstream=False)

            result = subprocess.run(
                ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f002")
            self.assertEqual(payload["feature_section"], "READY")
            self.assertEqual(payload["task_id"], "1")
            self.assertEqual(
                payload["openspec_change_path"],
                "openspec/changes/downstream-feature-change",
            )
            self.assertEqual(
                payload["implementation_plan_path"],
                "openspec/changes/downstream-feature-change/implementation-plans/1.md",
            )
            self.assertEqual(
                payload["openspec_context_files"],
                [
                    "openspec/changes/downstream-feature-change/proposal.md",
                    "openspec/changes/downstream-feature-change/design.md",
                    "openspec/changes/downstream-feature-change/tasks.md",
                    "openspec/changes/downstream-feature-change/implementation-plans/1.md",
                ],
            )

    def test_start_task_resolves_cross_feature_ready_task_with_archived_upstream_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_cross_feature_start_task_fixture(repo, archived_upstream=True)

            result = subprocess.run(
                ["python3", str(START_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f002")
            self.assertEqual(payload["feature_section"], "READY")
            self.assertEqual(payload["task_id"], "1")
            self.assertEqual(
                payload["openspec_change_path"],
                "openspec/changes/downstream-feature-change",
            )
            self.assertEqual(
                payload["implementation_plan_path"],
                "openspec/changes/downstream-feature-change/implementation-plans/1.md",
            )
            self.assertEqual(
                payload["openspec_context_files"],
                [
                    "openspec/changes/downstream-feature-change/proposal.md",
                    "openspec/changes/downstream-feature-change/design.md",
                    "openspec/changes/downstream-feature-change/tasks.md",
                    "openspec/changes/downstream-feature-change/implementation-plans/1.md",
                ],
            )

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
            _write_task_validation_log(feature_file, task_id="2", evidence_categories="runtime_path")

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

    def test_complete_task_ignores_done_legacy_exempt_feature_during_active_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_complete_task_legacy_exempt_fixture(repo)

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f002")
            self.assertEqual(payload["feature_section"], "IN_PROGRESS")
            self.assertEqual(payload["task_id"], "1")
            self.assertEqual(payload["openspec_change_id"], "active-feature-change")
            self.assertEqual(
                payload["openspec_context_files"],
                [
                    "openspec/changes/active-feature-change/proposal.md",
                    "openspec/changes/active-feature-change/design.md",
                    "openspec/changes/active-feature-change/tasks.md",
                    "openspec/changes/active-feature-change/implementation-plans/1.md",
                ],
            )

    def test_complete_task_rejects_missing_implementation_plan(self) -> None:
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

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "task implementation plan is missing: "
                "openspec/changes/integrate-openspec-shaping-readiness/implementation-plans/2.md",
                result.stderr,
            )

    def test_complete_task_rejects_structurally_invalid_implementation_plan(self) -> None:
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
            implementation_plan_dir = change_dir / "implementation-plans"
            implementation_plan_dir.mkdir(parents=True, exist_ok=True)
            (implementation_plan_dir / "2.md").write_text(
                "# Task 2 Implementation Plan\n\n- Objective: weak plan fixture.\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task implementation plan is invalid:", result.stderr)
            self.assertIn("## Contract Surface", result.stderr)

    def test_complete_task_rejects_completion_evidence_with_wrong_category(self) -> None:
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
            _write_task_validation_log(feature_file, task_id="1", evidence_categories="schema")

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("task completion evidence does not satisfy declared proof obligations", result.stderr)

    def test_complete_task_still_rejects_active_feature_missing_change_with_done_legacy_exempt_feature(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_complete_task_legacy_exempt_fixture(repo, missing_active_change=True)

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("v1-f002-active-feature.md is missing OpenSpec Change metadata", result.stderr)

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
            _write_task_validation_log(feature_file, task_id="1", evidence_categories="runtime_path")

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

    def test_complete_task_prefers_existing_feature_worktree_for_active_task_resolution(self) -> None:
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
            _write_task_validation_log(feature_file, task_id="1", evidence_categories="runtime_path")

            init_result = _git(repo, "init", "-b", "main")
            self.assertEqual(init_result.returncode, 0, init_result.stdout + init_result.stderr)
            self.assertEqual(_git(repo, "config", "user.name", "Test User").returncode, 0)
            self.assertEqual(_git(repo, "config", "user.email", "test@example.com").returncode, 0)
            self.assertEqual(_git(repo, "add", ".").returncode, 0)
            commit_result = _git(repo, "commit", "-m", "initial workflow state")
            self.assertEqual(commit_result.returncode, 0, commit_result.stdout + commit_result.stderr)

            worktree_root = Path(tmpdir) / "worktrees"
            worktree_root.mkdir()
            feature_worktree = worktree_root / "v1-f001-openspec-integration"
            add_worktree_result = _git(
                repo,
                "worktree",
                "add",
                "-b",
                "v1-f001-openspec-integration",
                str(feature_worktree),
            )
            self.assertEqual(add_worktree_result.returncode, 0, add_worktree_result.stdout + add_worktree_result.stderr)

            feature_worktree_file = (
                feature_worktree / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-openspec-integration.md"
            )
            feature_worktree_file.write_text(
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
                    - 2026-03-28: task 1 completed on the feature branch

                    ## 2. Handoff Notes
                    - Feature worktree is ready to complete task 2.
                    """
                ),
                encoding="utf-8",
            )
            _write_task_validation_log(feature_worktree_file, task_id="2", evidence_categories="runtime_path")
            (feature_worktree / "openspec" / "changes" / "integrate-openspec-shaping-readiness" / "tasks.md").write_text(
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
            _write_implementation_plan(
                feature_worktree / "openspec" / "changes" / "integrate-openspec-shaping-readiness",
                "2",
            )
            self.assertEqual(_git(feature_worktree, "add", ".").returncode, 0)
            worktree_commit_result = _git(feature_worktree, "commit", "-m", "progress task state on feature branch")
            self.assertEqual(
                worktree_commit_result.returncode,
                0,
                worktree_commit_result.stdout + worktree_commit_result.stderr,
            )

            result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT)],
                cwd=repo,
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
            _write_task_validation_log(feature_file, task_id="1", evidence_categories="runtime_path")

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

    def test_final_task_handoff_makes_finish_feature_startable_while_feature_stays_in_progress(self) -> None:
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
            _write_task_validation_log(feature_file, task_id="2", evidence_categories="runtime_path")

            complete_result = subprocess.run(
                ["python3", str(COMPLETE_TASK_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(complete_result.returncode, 0, complete_result.stdout + complete_result.stderr)
            complete_payload = json.loads(complete_result.stdout)
            self.assertEqual(complete_payload["completion_handoff"]["decision"], "confirm_feature_acceptance")
            feature_file.write_text(
                feature_file.read_text(encoding="utf-8").replace("- Current Task: `2`", "- Current Task: `none`"),
                encoding="utf-8",
            )
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

    def test_finish_feature_rejects_in_progress_feature_when_current_task_is_not_none(self) -> None:
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
                    - `2026-03-26` Task `2`: final task closed but task handoff is still active.

                    ## 2. Handoff Notes
                    - `2026-03-26`: Final task closed, but the current task marker was not cleared.
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

            self.assertNotEqual(finish_result.returncode, 0)
            self.assertIn("Current Task must be `none`", finish_result.stderr)

    def test_audit_accepts_in_progress_feature_ready_for_finish_feature(self) -> None:
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
                    - Current Task: `none`

                    ## 1. Validation Log
                    - `2026-03-26` Task `2`: all top-level task work completed; feature is ready for `finish-feature`.

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

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

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

    def test_audit_rejects_shaping_feature_missing_baseline_artifact(self) -> None:
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

                    ### `v1-f001` [Shaping feature](features/v1-f001-shaping-feature.md)

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-shaping-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Shaping feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
                    - OpenSpec Change: `shaping-feature`
                    - OpenSpec Specs:
                      - `openspec/specs/openspec-change-integration/spec.md`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "shaping-feature"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [ ] 1 Draft work\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("is in [SHAPING] but linked OpenSpec change is missing design.md", result.stdout)

    def test_audit_rejects_ready_feature_missing_baseline_artifact_with_ready_error_code(self) -> None:
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

                    ### `v1-f001` [Ready feature](features/v1-f001-ready-feature.md)

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-ready-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Ready feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `ready-feature`
                    - OpenSpec Specs:
                      - `openspec/specs/openspec-change-integration/spec.md`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "ready-feature"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [ ] 1 Draft work\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("is in [READY] but linked OpenSpec change is missing design.md", result.stdout)

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

    def test_audit_rejects_done_feature_with_duplicate_archived_changes(self) -> None:
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

            first_archive = repo / "openspec" / "changes" / "archive" / "2026-03-25-archived-feature"
            first_archive.mkdir(parents=True, exist_ok=True)
            (first_archive / "proposal.md").write_text("proposal", encoding="utf-8")
            second_archive = repo / "openspec" / "changes" / "archive" / "2026-03-26-archived-feature"
            second_archive.mkdir(parents=True, exist_ok=True)
            (second_archive / "proposal.md").write_text("proposal", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "is in [DONE] but expected exactly one archived OpenSpec change for archived-feature",
                result.stdout,
            )

    def test_audit_rejects_extra_section_after_defer_in_initialized_repo(self) -> None:
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

                    None yet.

                    ## [DEFER]

                    None yet.

                    ## [BLOCKED]

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

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("docs/planning/versions/v1/BACKLOG.md has section order", result.stdout)
            self.assertIn("BLOCKED", result.stdout)

    def test_audit_rejects_promoted_feature_missing_openspec_specs_in_initialized_repo(self) -> None:
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

                    ### `v1-f001` [Spec-less feature](features/v1-f001-spec-less-feature.md)

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-spec-less-feature.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Spec-less feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `spec-less-feature`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "spec-less-feature"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    - [x] 1 Completed prerequisite
                    - [ ] 2 Ready fixture task
                      - Depends On:
                        - `1`
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
            self.assertIn(
                "docs/planning/versions/v1/features/v1-f001-spec-less-feature.md is missing OpenSpec Specs metadata",
                result.stdout,
            )

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

    def test_audit_rejects_shaping_feature_with_nested_only_openspec_tasks(self) -> None:
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

                    ### `v1-f001` [Malformed OpenSpec tasks](features/v1-f001-malformed-openspec-tasks.md)

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-malformed-openspec-tasks.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Malformed OpenSpec tasks

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
                    - OpenSpec Change: `malformed-openspec-tasks`
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

            change_dir = repo / "openspec" / "changes" / "malformed-openspec-tasks"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Work

                      - [ ] 1.1 Missing parent executable task
                      - [ ] 1.2 Another nested item
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
            self.assertIn("nested checklist item `1.1` is missing parent top-level executable task `1`", result.stdout)

    def test_audit_rejects_ready_feature_with_nested_only_openspec_tasks(self) -> None:
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

                    ### `v1-f001` [Malformed OpenSpec tasks](features/v1-f001-malformed-openspec-tasks.md)

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

            feature_file = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-malformed-openspec-tasks.md"
            feature_file.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Malformed OpenSpec tasks

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `malformed-openspec-tasks`
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

            change_dir = repo / "openspec" / "changes" / "malformed-openspec-tasks"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Work

                      - [ ] 1.1 Missing parent executable task
                      - [ ] 1.2 Another nested item
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
            self.assertIn("nested checklist item `1.1` is missing parent top-level executable task `1`", result.stdout)

    def test_audit_rejects_orphan_active_change_not_linked_from_promoted_feature(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_active_change_linkage_fixture(repo, orphaned=True)

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("orphan active OpenSpec change orphan-change is not linked from any promoted feature", result.stdout)

    def test_audit_accepts_repaired_active_change_linkage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_active_change_linkage_fixture(repo, orphaned=False)

            result = subprocess.run(
                ["python3", str(AUDIT_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("OK: workflow audit passed", result.stdout)


if __name__ == "__main__":
    unittest.main()

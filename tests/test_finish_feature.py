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
FINISH_RESOLVER = REPO_ROOT / "skills" / "finish-feature" / "scripts" / "resolve_finish_feature.py"

_SPEC = importlib.util.spec_from_file_location("init_workflow_artifacts", INIT_SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
initialize = _MODULE.initialize


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def _write_finishable_feature(
    repo: Path,
    *,
    feature_id: str = "v1-f001",
    change_id: str = "finish-feature-gate",
    current_task: str = "none",
) -> Path:
    backlog_path = repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md"
    feature_slug = "finish-feature-gate"
    backlog_path.write_text(
        textwrap.dedent(
            f"""\
            # V1 Backlog

            ## [BACKLOG]

            None yet.

            ## [SHAPING]

            None yet.

            ## [READY]

            None yet.

            ## [IN_PROGRESS]

            ### `{feature_id}` [Finish feature gate](features/{feature_id}-{feature_slug}.md)

            ## [DONE]

            None yet.

            ## [DEFER]

            None yet.
            """
        ),
        encoding="utf-8",
    )

    feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / f"{feature_id}-{feature_slug}.md"
    feature_path.write_text(
        textwrap.dedent(
            f"""\
            # Feature: Finish feature gate

            ## 0. Meta
            - Feature ID: `{feature_id}`
            - Version: `v1`
            - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
            - OpenSpec Change: `{change_id}`
            - OpenSpec Specs:
              - `openspec/specs/task-execution-handoff/spec.md`
            - Current Task: `{current_task}`

            ## 1. Validation Log
            - 2026-03-25: task evidence recorded

            ## 2. Handoff Notes
            - Ready for feature-finalization gate.
            """
        ),
        encoding="utf-8",
    )
    return feature_path


class FinishFeatureResolverTests(unittest.TestCase):
    def test_resolver_rejects_primary_checkout_and_requires_feature_worktree(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo)

            change_dir = repo / "openspec" / "changes" / "finish-feature-gate"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [x] 1 Done\n- [x] 2 Done\n", encoding="utf-8")

            init_result = _git(repo, "init", "-b", "main")
            self.assertEqual(init_result.returncode, 0, init_result.stdout + init_result.stderr)
            self.assertEqual(_git(repo, "config", "user.name", "Test User").returncode, 0)
            self.assertEqual(_git(repo, "config", "user.email", "test@example.com").returncode, 0)
            self.assertEqual(_git(repo, "add", ".").returncode, 0)
            commit_result = _git(repo, "commit", "-m", "initial workflow state")
            self.assertEqual(commit_result.returncode, 0, commit_result.stdout + commit_result.stderr)

            worktree_root = Path(tmpdir) / "worktrees"
            worktree_root.mkdir()
            feature_worktree = worktree_root / "v1-f001-finish-feature-gate"
            add_worktree_result = _git(
                repo,
                "worktree",
                "add",
                "-b",
                "v1-f001-finish-feature-gate",
                str(feature_worktree),
            )
            self.assertEqual(add_worktree_result.returncode, 0, add_worktree_result.stdout + add_worktree_result.stderr)

            primary_result = subprocess.run(
                ["python3", str(FINISH_RESOLVER)],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(primary_result.returncode, 0)
            self.assertIn("finish-feature must run from the feature worktree", primary_result.stderr)

            worktree_result = subprocess.run(
                ["python3", str(FINISH_RESOLVER)],
                cwd=feature_worktree,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(worktree_result.returncode, 0, worktree_result.stdout + worktree_result.stderr)
            payload = json.loads(worktree_result.stdout)
            self.assertTrue(payload["requires_archive"])
            self.assertEqual(payload["feature_id"], "v1-f001")

    def test_resolver_reports_active_change_that_still_requires_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo)

            change_dir = repo / "openspec" / "changes" / "finish-feature-gate"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "tasks.md").write_text(
                textwrap.dedent(
                    """\
                    ## 1. Work

                    - [x] 1 Complete task
                    - [x] 2 Final verification
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["requires_archive"])
            self.assertEqual(payload["change_id"], "finish-feature-gate")
            self.assertEqual(payload["active_change_path"], "openspec/changes/finish-feature-gate")
            self.assertIsNone(payload["archive_path"])

    def test_resolver_reports_archived_change_ready_for_branch_finish(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo)

            archive_dir = repo / "openspec" / "changes" / "archive" / "2026-03-25-finish-feature-gate"
            archive_dir.mkdir(parents=True, exist_ok=True)
            (archive_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (archive_dir / "tasks.md").write_text("- [x] 1 Wrapped up\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["requires_archive"])
            self.assertIsNone(payload["active_change_path"])
            self.assertEqual(payload["archive_path"], "openspec/changes/archive/2026-03-25-finish-feature-gate")

    def test_resolver_requires_explicit_feature_when_multiple_finishable_features_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo, feature_id="v1-f001", change_id="change-one")
            _write_finishable_feature(repo, feature_id="v1-f002", change_id="change-two")

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

                    ### `v1-f001` [Finish feature gate](features/v1-f001-finish-feature-gate.md)
                    ### `v1-f002` [Finish feature gate](features/v1-f002-finish-feature-gate.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_one_dir = repo / "openspec" / "changes" / "change-one"
            change_two_dir = repo / "openspec" / "changes" / "change-two"
            change_one_dir.mkdir(parents=True, exist_ok=True)
            change_two_dir.mkdir(parents=True, exist_ok=True)
            (change_one_dir / "tasks.md").write_text("- [x] 1 Done\n", encoding="utf-8")
            (change_two_dir / "tasks.md").write_text("- [x] 1 Done\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected exactly one finishable feature in [IN_PROGRESS]", result.stderr)

    def test_resolver_with_feature_id_ignores_unrelated_invalid_in_progress_feature(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo, feature_id="v1-f001", change_id="change-one")
            _write_finishable_feature(repo, feature_id="v1-f002", change_id="change-two")

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

                    ### `v1-f001` [Finish feature gate](features/v1-f001-finish-feature-gate.md)
                    ### `v1-f002` [Finish feature gate](features/v1-f002-finish-feature-gate.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_one_dir = repo / "openspec" / "changes" / "change-one"
            change_one_dir.mkdir(parents=True, exist_ok=True)
            (change_one_dir / "tasks.md").write_text("- [x] 1 Done\n", encoding="utf-8")
            # Intentionally leave change-two missing to make the sibling feature malformed.

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo), "--feature-id", "v1-f001"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f001")
            self.assertEqual(payload["change_id"], "change-one")

    def test_resolver_rejects_feature_when_current_task_is_still_active(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo, current_task="2")

            change_dir = repo / "openspec" / "changes" / "finish-feature-gate"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "tasks.md").write_text("- [x] 1 Done\n- [x] 2 Done\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo), "--feature-id", "v1-f001"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Current Task must be `none`", result.stderr)

    def test_resolver_rejects_feature_when_top_level_tasks_remain_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_finishable_feature(repo)

            change_dir = repo / "openspec" / "changes" / "finish-feature-gate"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "tasks.md").write_text("- [x] 1 Done\n- [ ] 2 Still open\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo), "--feature-id", "v1-f001"],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("top-level OpenSpec tasks are not all done", result.stderr)


if __name__ == "__main__":
    unittest.main()

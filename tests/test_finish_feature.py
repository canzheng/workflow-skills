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


def _write_done_feature(repo: Path, *, feature_id: str = "v1-f001", change_id: str = "finish-feature-gate") -> Path:
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

            None yet.

            ## [DONE]

            ### `{feature_id}` [Finish feature gate](features/{feature_id}-{feature_slug}.md)

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
            - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#done`
            - OpenSpec Change: `{change_id}`
            - OpenSpec Specs:
              - `openspec/specs/task-execution-handoff/spec.md`
            - Current Task: `none`

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
    def test_resolver_reports_active_change_that_still_requires_archive(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_done_feature(repo)

            change_dir = repo / "openspec" / "changes" / "finish-feature-gate"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")

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
            _write_done_feature(repo)

            archive_dir = repo / "openspec" / "changes" / "archive" / "2026-03-25-finish-feature-gate"
            archive_dir.mkdir(parents=True, exist_ok=True)
            (archive_dir / "proposal.md").write_text("proposal", encoding="utf-8")

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

    def test_resolver_requires_explicit_feature_when_multiple_done_features_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_done_feature(repo, feature_id="v1-f001", change_id="change-one")
            _write_done_feature(repo, feature_id="v1-f002", change_id="change-two")

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

                    ### `v1-f001` [Finish feature gate](features/v1-f001-finish-feature-gate.md)
                    ### `v1-f002` [Finish feature gate](features/v1-f002-finish-feature-gate.md)

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            (repo / "openspec" / "changes" / "change-one").mkdir(parents=True, exist_ok=True)
            (repo / "openspec" / "changes" / "change-two").mkdir(parents=True, exist_ok=True)

            result = subprocess.run(
                ["python3", str(FINISH_RESOLVER), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected exactly one feature in [DONE]", result.stderr)


if __name__ == "__main__":
    unittest.main()

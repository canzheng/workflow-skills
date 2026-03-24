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

_SPEC = importlib.util.spec_from_file_location("init_workflow_artifacts", INIT_SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
initialize = _MODULE.initialize


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

                    - [x] 1.1 Seed baseline
                    - [ ] 1.2 Wire task parsing
                      - Depends On:
                        - `1.1`
                    - [ ] 1.3 Start-task integration
                      - Depends On:
                        - `1.2`
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

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["feature_id"], "v1-f001")
            self.assertEqual(payload["task_id"], "1.2")


if __name__ == "__main__":
    unittest.main()

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
DIAGNOSE_SCRIPT = REPO_ROOT / "skills" / "diagnose-workflow" / "scripts" / "diagnose_workflow.py"

_SPEC = importlib.util.spec_from_file_location("init_workflow_artifacts", INIT_SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
initialize = _MODULE.initialize


class DiagnoseWorkflowTests(unittest.TestCase):
    def test_diagnose_workflow_reports_healthy_repo_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["active_version"], "v1")
            self.assertEqual(payload["section_counts"]["BACKLOG"], 0)
            self.assertEqual(payload["finding_counts"]["error"], 0)
            self.assertEqual(payload["finding_counts"]["warning"], 0)

    def test_diagnose_workflow_reports_findings_without_failing_for_repairable_state(self) -> None:
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

                    ### `v1-f001` [Legacy format feature](features/v1-f001-legacy-format-feature.md)

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

            feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-legacy-format-feature.md"
            feature_path.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Legacy format feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - Current Task: `none`

                    ## Problem
                    - Old inline planning content still exists.

                    ## 6. Tasks

                    ### T01: First task
                    - Status: `todo`
                    - Depends On:
                      - none
                    """
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            finding_codes = {finding["code"] for finding in payload["findings"]}
            self.assertIn("missing_openspec_change", finding_codes)
            self.assertIn("legacy_inline_planning_sections", finding_codes)
            self.assertIn("no_ready_task", finding_codes)


if __name__ == "__main__":
    unittest.main()

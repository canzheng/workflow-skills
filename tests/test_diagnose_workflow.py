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
    feature_path = feature_dir / "v1-f001-linked-feature.md"
    feature_path.write_text(
        textwrap.dedent(
            f"""\
            # Feature: Linked feature

            ## 0. Meta
            - Feature ID: `v1-f001`
            - Version: `v1`
            - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
            - OpenSpec Change: `{linked_change_id}`
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

    def test_diagnose_workflow_reports_missing_current_version_as_structured_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            (repo / "docs" / "planning" / "current_version").unlink()

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertTrue(
                any(
                    finding["code"] == "missing_current_version"
                    and finding["path"] == "docs/planning/current_version"
                    for finding in payload["findings"]
                )
            )

    def test_diagnose_workflow_reports_missing_active_backlog_as_structured_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            (repo / "docs" / "planning" / "versions" / "v1" / "BACKLOG.md").unlink()
            orphan_change = repo / "openspec" / "changes" / "orphan-change"
            orphan_change.mkdir(parents=True, exist_ok=True)
            (orphan_change / "proposal.md").write_text("proposal", encoding="utf-8")
            (orphan_change / "design.md").write_text("design", encoding="utf-8")
            (orphan_change / "tasks.md").write_text("- [ ] 1 Orphan work\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertTrue(
                any(
                    finding["code"] == "missing_backlog"
                    and finding["path"] == "docs/planning/versions/v1/BACKLOG.md"
                    for finding in payload["findings"]
                )
            )
            self.assertFalse(any(finding["code"] == "orphan_active_change" for finding in payload["findings"]))

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

    def test_diagnose_workflow_reports_extra_canonical_section_after_defer(self) -> None:
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
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertTrue(
                any(
                    finding["code"] == "invalid_backlog_section_order"
                    and finding["path"] == "docs/planning/versions/v1/BACKLOG.md"
                    and "BLOCKED" in finding["message"]
                    for finding in payload["findings"]
                )
            )

    def test_diagnose_workflow_reports_missing_promoted_feature_openspec_specs(self) -> None:
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

            feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-spec-less-feature.md"
            feature_path.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Spec-less feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `spec-less-change`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "spec-less-change"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [ ] 1 Fixture task\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertTrue(
                any(
                    finding["code"] == "missing_openspec_specs"
                    and finding["path"] == "docs/planning/versions/v1/features/v1-f001-spec-less-feature.md"
                    and finding["feature_id"] == "v1-f001"
                    for finding in payload["findings"]
                )
            )

    def test_diagnose_workflow_reports_missing_shaping_artifact(self) -> None:
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

            feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-shaping-feature.md"
            feature_path.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Shaping feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
                    - OpenSpec Change: `shaping-change`
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

            change_dir = repo / "openspec" / "changes" / "shaping-change"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [ ] 1 Fixture task\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertTrue(
                any(
                    finding["code"] == "missing_shaping_artifact"
                    and finding["path"] == "docs/planning/versions/v1/features/v1-f001-shaping-feature.md"
                    and finding["details"]["required_file"] == "design.md"
                    for finding in payload["findings"]
                )
            )

    def test_diagnose_workflow_reports_done_feature_with_active_change(self) -> None:
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

            feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-archived-feature.md"
            feature_path.write_text(
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

            change_dir = repo / "openspec" / "changes" / "archived-feature"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertTrue(
                any(
                    finding["code"] == "done_feature_change_still_active"
                    and finding["path"] == "docs/planning/versions/v1/features/v1-f001-archived-feature.md"
                    for finding in payload["findings"]
                )
            )

    def test_diagnose_workflow_reports_multiple_structural_findings_without_false_healthy_status(self) -> None:
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

                    ## [BLOCKED]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / "v1-f001-spec-less-feature.md"
            feature_path.write_text(
                textwrap.dedent(
                    """\
                    # Feature: Spec-less feature

                    ## 0. Meta
                    - Feature ID: `v1-f001`
                    - Version: `v1`
                    - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
                    - OpenSpec Change: `spec-less-change`
                    - Current Task: `none`

                    ## 1. Validation Log
                    - None yet.

                    ## 2. Handoff Notes
                    - None yet.
                    """
                ),
                encoding="utf-8",
            )

            change_dir = repo / "openspec" / "changes" / "spec-less-change"
            change_dir.mkdir(parents=True, exist_ok=True)
            (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
            (change_dir / "design.md").write_text("design", encoding="utf-8")
            (change_dir / "tasks.md").write_text("- [ ] 1 Fixture task\n", encoding="utf-8")

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
            self.assertIn("invalid_backlog_section_order", finding_codes)
            self.assertIn("missing_openspec_specs", finding_codes)

    def test_diagnose_workflow_reports_multiple_active_tasks_as_an_error(self) -> None:
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

                    ### `v1-f001` [One](features/v1-f001-one.md)
                    ### `v1-f002` [Two](features/v1-f002-two.md)

                    ## [DONE]

                    None yet.

                    ## [DEFER]

                    None yet.
                    """
                ),
                encoding="utf-8",
            )

            for feature_id, slug in (("v1-f001", "one"), ("v1-f002", "two")):
                feature_path = repo / "docs" / "planning" / "versions" / "v1" / "features" / f"{feature_id}-{slug}.md"
                feature_path.write_text(
                    textwrap.dedent(
                        f"""\
                        # Feature: {slug}

                        ## 0. Meta
                        - Feature ID: `{feature_id}`
                        - Version: `v1`
                        - Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
                        - OpenSpec Change: `{feature_id}-change`
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

                change_dir = repo / "openspec" / "changes" / f"{feature_id}-change"
                change_dir.mkdir(parents=True, exist_ok=True)
                (change_dir / "proposal.md").write_text("proposal", encoding="utf-8")
                (change_dir / "design.md").write_text("design", encoding="utf-8")
                (change_dir / "tasks.md").write_text("- [ ] 1 Execute work\n", encoding="utf-8")

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            self.assertEqual(payload["active_task_count"], 2)
            finding_codes = {finding["code"] for finding in payload["findings"]}
            self.assertIn("multiple_in_progress_tasks", finding_codes)

    def test_diagnose_workflow_reports_orphan_active_change_finding(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_active_change_linkage_fixture(repo, orphaned=True)

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "issues_found")
            orphan_findings = [finding for finding in payload["findings"] if finding["code"] == "orphan_active_change"]
            self.assertEqual(len(orphan_findings), 1)
            self.assertEqual(orphan_findings[0]["details"]["change_id"], "orphan-change")

    def test_diagnose_workflow_accepts_repaired_active_change_linkage(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            initialize(repo, "v1")
            _write_active_change_linkage_fixture(repo, orphaned=False)

            result = subprocess.run(
                ["python3", str(DIAGNOSE_SCRIPT), "--repo-root", str(repo)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            orphan_findings = [finding for finding in payload["findings"] if finding["code"] == "orphan_active_change"]
            self.assertEqual(orphan_findings, [])


if __name__ == "__main__":
    unittest.main()

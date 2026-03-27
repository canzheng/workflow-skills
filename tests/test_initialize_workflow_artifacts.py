from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = REPO_ROOT / "skills" / "initialize-workflow-artifacts" / "scripts" / "init_workflow_artifacts.py"

_SPEC = importlib.util.spec_from_file_location("init_workflow_artifacts", INIT_SCRIPT)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
initialize = _MODULE.initialize


class InitializeWorkflowArtifactsTests(unittest.TestCase):
    def test_initialize_creates_thin_feature_template_with_openspec_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"

            initialize(repo, "v1")

            template = (repo / "docs" / "planning" / "template" / "feature-template.md").read_text(encoding="utf-8")

            self.assertIn("- OpenSpec Change: `<change-id>`", template)
            self.assertIn("- OpenSpec Specs:", template)
            self.assertIn("- Current Task: `none`", template)
            self.assertIn("## 1. Validation Log", template)
            self.assertIn("## 2. Handoff Notes", template)
            self.assertNotIn("## 2. Tasks", template)
            self.assertNotIn("## 3. Validation Log", template)
            self.assertNotIn("## 4. Change Log", template)
            self.assertNotIn("## 4. Design Spec", template)
            self.assertNotIn("## 5. Implementation Plan", template)
            self.assertNotIn("## 6. Tasks", template)

    def test_initialize_creates_required_openspec_scaffold(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"

            initialize(repo, "v1")

            self.assertTrue((repo / "openspec" / "specs").is_dir())
            self.assertTrue((repo / "openspec" / "changes" / "archive").is_dir())

    def test_initialize_creates_workflow_reference_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"

            initialize(repo, "v1")

            reference_doc = (repo / "docs" / "planning" / "WORKFLOW_REFERENCE.md").read_text(encoding="utf-8")

            self.assertIn("# Workflow Reference", reference_doc)
            self.assertIn("## Feature Status Model", reference_doc)
            self.assertIn("## Task Status Model", reference_doc)


if __name__ == "__main__":
    unittest.main()

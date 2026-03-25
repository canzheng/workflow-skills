from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDER_SCRIPT = REPO_ROOT / "skills" / "shape-backlog-item" / "scripts" / "render_feature_file.py"


class ShapeBacklogItemRendererTests(unittest.TestCase):
    def test_renderer_outputs_thin_feature_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            (repo / ".git").mkdir(parents=True)

            output = "docs/planning/versions/v1/features/v1-f123-example.md"
            result = subprocess.run(
                [
                    "python3",
                    str(RENDER_SCRIPT),
                    "--repo-root",
                    str(repo),
                    "--feature-id",
                    "v1-f123",
                    "--title",
                    "Example",
                    "--version",
                    "v1",
                    "--backlog-reference",
                    "docs/planning/versions/v1/BACKLOG.md#shaping",
                    "--openspec-change",
                    "example-change",
                    "--openspec-spec",
                    "openspec/specs/workflow-board-lifecycle/spec.md",
                    "--openspec-spec",
                    "openspec/specs/workflow-audit-and-repair/spec.md",
                    "--created",
                    "2026-03-25",
                    "--last-updated",
                    "2026-03-25",
                    "--output",
                    output,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            feature_text = (repo / output).read_text(encoding="utf-8")
            self.assertIn("- OpenSpec Change: `example-change`", feature_text)
            self.assertIn("- `openspec/specs/workflow-board-lifecycle/spec.md`", feature_text)
            self.assertIn("- `openspec/specs/workflow-audit-and-repair/spec.md`", feature_text)
            self.assertNotIn("## 1. Problem", feature_text)
            self.assertNotIn("## 4. Design Spec", feature_text)
            self.assertNotIn("## 6. Tasks", feature_text)

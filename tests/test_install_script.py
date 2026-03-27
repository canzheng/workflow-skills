from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = REPO_ROOT / "install.sh"
MANAGED_WORKFLOW = REPO_ROOT / "AGENTS-global-workflow.md"
FEATURE_TEMPLATE = REPO_ROOT / "docs" / "planning" / "template" / "feature-template.md"


def _run_install(codex_home: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(INSTALL_SCRIPT)],
        cwd=REPO_ROOT,
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        capture_output=True,
        text=True,
        check=False,
    )


class InstallScriptTests(unittest.TestCase):
    def test_install_script_copies_workflow_skills_and_patches_agents(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            codex_home = Path(tmpdir) / "codex-home"
            agents_path = codex_home / "AGENTS.md"
            agents_path.parent.mkdir(parents=True, exist_ok=True)
            agents_path.write_text(
                "\n".join(
                    [
                        "# Global Instructions",
                        "",
                        "User-managed header",
                        "",
                        "<!-- Beginning of Workflow Section -->",
                        "OLD WORKFLOW CONTENT",
                        "<!-- End of Workflow Section -->",
                        "",
                        "User-managed footer",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = _run_install(codex_home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            skills_root = codex_home / "skills"
            self.assertTrue((skills_root / "audit-workflow" / "SKILL.md").is_file())
            self.assertTrue((skills_root / "diagnose-workflow" / "SKILL.md").is_file())
            self.assertTrue((skills_root / "finish-feature" / "SKILL.md").is_file())
            self.assertTrue((skills_root / "_workflow" / "workflow_state.py").is_file())
            self.assertFalse((skills_root / "_workflow" / "tests").exists())
            self.assertTrue((skills_root / "_workflow" / "templates" / "feature-template.md").is_file())
            self.assertFalse((codex_home / "bin" / "run-python.sh").exists())
            self.assertFalse((skills_root / "run-python.sh").exists())
            self.assertFalse((skills_root / "bin" / "run-python.sh").exists())

            installed_template = (skills_root / "_workflow" / "templates" / "feature-template.md").read_text(
                encoding="utf-8"
            )
            self.assertEqual(installed_template, FEATURE_TEMPLATE.read_text(encoding="utf-8"))

            installed_agents = agents_path.read_text(encoding="utf-8")
            managed_workflow = MANAGED_WORKFLOW.read_text(encoding="utf-8")
            self.assertIn(managed_workflow, installed_agents)
            self.assertNotIn("OLD WORKFLOW CONTENT", installed_agents)
            self.assertIn("User-managed header", installed_agents)
            self.assertIn("User-managed footer", installed_agents)

    def test_install_script_fails_when_agents_markers_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            codex_home = Path(tmpdir) / "codex-home"
            agents_path = codex_home / "AGENTS.md"
            agents_path.parent.mkdir(parents=True, exist_ok=True)
            agents_path.write_text(
                "\n".join(
                    [
                        "# Global Instructions",
                        "",
                        "No managed workflow markers here.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            result = _run_install(codex_home)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Workflow section markers", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

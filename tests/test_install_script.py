from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_SCRIPT = REPO_ROOT / "install.sh"


def test_install_script_copies_workflow_skills_to_codex_home(tmp_path: Path) -> None:
    codex_home = tmp_path / "codex-home"

    result = subprocess.run(
        ["bash", str(INSTALL_SCRIPT)],
        cwd=REPO_ROOT,
        env={**os.environ, "CODEX_HOME": str(codex_home)},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr

    skills_root = codex_home / "skills"
    assert (skills_root / "audit-workflow" / "SKILL.md").is_file()
    assert (skills_root / "_workflow" / "workflow_state.py").is_file()
    assert not (skills_root / "_workflow" / "tests").exists()

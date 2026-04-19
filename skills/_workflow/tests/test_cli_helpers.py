"""Unit tests for skills/_workflow/cli_helpers.py.

Covers the walk-up semantics of `resolve_skills_root()` so future script
relocations cannot silently resolve the wrong path. This is the regression
that replaces the `Path(__file__).resolve().parents[2]` idiom removed during
v1-f019 task 1.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from _workflow.cli_helpers import WorkflowError, resolve_skills_root


def test_resolve_skills_root_finds_the_real_skills_directory() -> None:
    here = Path(__file__).resolve()
    root = resolve_skills_root(here)
    assert (root / "_workflow").is_dir(), root


def test_resolve_skills_root_walks_up_from_a_deeper_relocation(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    (skills_root / "_workflow").mkdir(parents=True)
    deep_script = skills_root / "new-skill" / "scripts" / "extra" / "nested.py"
    deep_script.parent.mkdir(parents=True)
    deep_script.write_text("# script at an unconventional depth\n", encoding="utf-8")

    resolved = resolve_skills_root(deep_script)

    assert resolved == skills_root.resolve()


def test_resolve_skills_root_raises_when_no_workflow_sibling_is_found(tmp_path: Path) -> None:
    orphan = tmp_path / "somewhere" / "file.py"
    orphan.parent.mkdir(parents=True)
    orphan.write_text("# no _workflow ancestor here\n", encoding="utf-8")

    with pytest.raises(WorkflowError):
        resolve_skills_root(orphan)

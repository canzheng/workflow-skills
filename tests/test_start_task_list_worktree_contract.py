"""Regression test for the `_list_git_worktree_roots` convergence landed in
v1-f019 task 1. Before the migration, `skills/start-task/scripts/resolve_start_task.py`
carried a private `_list_git_worktree_roots` whose failure contract returned
`[]` while the public `list_git_worktree_roots` in `skills/_workflow/workflow_state.py`
returned `[root.resolve()]`. Retrieved lesson L-002 required a missing-worktree
negative-path test to keep fallback behavior from silently returning during
resolver runs. This test enforces that the private copy cannot come back.
"""
from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
START_TASK_SCRIPT = REPO_ROOT / "skills" / "start-task" / "scripts" / "resolve_start_task.py"


class StartTaskListWorktreeContractTests(unittest.TestCase):
    def test_start_task_script_does_not_redefine_list_git_worktree_roots(self) -> None:
        source = START_TASK_SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn(
            "_list_git_worktree_roots",
            source,
            "skills/start-task/scripts/resolve_start_task.py reintroduced "
            "_list_git_worktree_roots. Import list_git_worktree_roots from "
            "_workflow.workflow_state instead of redefining a private copy — its "
            "failure contract diverged from the public helper, which is the "
            "regression L-002 catches.",
        )

    def test_start_task_script_imports_the_public_list_git_worktree_roots(self) -> None:
        source = START_TASK_SCRIPT.read_text(encoding="utf-8")
        self.assertIn(
            "list_git_worktree_roots",
            source,
            "skills/start-task/scripts/resolve_start_task.py no longer references "
            "list_git_worktree_roots; something else must be enumerating worktrees "
            "now, and the migration contract needs a review.",
        )
        self.assertIn("from _workflow.workflow_state import", source)
        import_block_start = source.index("from _workflow.workflow_state import")
        import_block_end = source.index(")", import_block_start)
        import_block = source[import_block_start:import_block_end]
        self.assertIn(
            "list_git_worktree_roots",
            import_block,
            "list_git_worktree_roots is mentioned but not imported from "
            "_workflow.workflow_state; route enumeration through the public helper.",
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FINISH_FEATURE_SKILL = REPO_ROOT / "skills" / "finish-feature" / "SKILL.md"
AUTONOMOUS_BACKLOG_LOOP_SKILL = REPO_ROOT / "skills" / "autonomous-backlog-loop" / "SKILL.md"
TASK_EXECUTION_HANDOFF_SPEC = REPO_ROOT / "openspec" / "specs" / "task-execution-handoff" / "spec.md"


class WorkflowContractDocsTests(unittest.TestCase):
    def test_finish_feature_skill_describes_in_progress_completion_gate(self) -> None:
        finish_feature_skill = FINISH_FEATURE_SKILL.read_text(encoding="utf-8")

        self.assertIn(
            "Use when a feature in `[IN_PROGRESS]` has satisfied its feature-level acceptance bar",
            finish_feature_skill,
        )

    def test_autonomous_backlog_loop_routes_completion_through_finish_feature(self) -> None:
        autonomous_loop_skill = AUTONOMOUS_BACKLOG_LOOP_SKILL.read_text(encoding="utf-8")

        self.assertIn("if the task finishes cleanly, call `complete-task`", autonomous_loop_skill)
        self.assertIn(
            "if `complete-task` reports that `finish-feature` is startable, call `finish-feature` before any downstream cleanup",
            autonomous_loop_skill,
        )
        self.assertIn(
            "if `finish-feature` moves the feature to `[DONE]`, perform the default finishing behavior",
            autonomous_loop_skill,
        )

    def test_autonomous_backlog_loop_clarifies_continue_vs_stop_after_complete_task(self) -> None:
        autonomous_loop_skill = AUTONOMOUS_BACKLOG_LOOP_SKILL.read_text(encoding="utf-8")

        self.assertIn(
            "if the feature remains `IN_PROGRESS` and another task is `ready`, continue the feature loop",
            autonomous_loop_skill,
        )
        self.assertIn(
            "if the feature remains `IN_PROGRESS` but no next task is `ready`, stop the feature loop and return control",
            autonomous_loop_skill,
        )

    def test_autonomous_backlog_loop_design_mode_meaning_is_sanity_only(self) -> None:
        autonomous_loop_skill = AUTONOMOUS_BACKLOG_LOOP_SKILL.read_text(encoding="utf-8")

        self.assertIn("does not act on active execution work", autonomous_loop_skill)
        self.assertIn(
            "still sanity-checks `[READY]` and `[IN_PROGRESS]` features for invalid workflow state",
            autonomous_loop_skill,
        )

    def test_stable_handoff_spec_mentions_autonomous_finish_feature_gate(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("### Requirement: Autonomous orchestration routes completion through finish-feature", task_execution_handoff_spec)
        self.assertIn("#### Scenario: Autonomous loop completes the final task for a feature", task_execution_handoff_spec)


if __name__ == "__main__":
    unittest.main()

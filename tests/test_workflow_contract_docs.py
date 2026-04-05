from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
START_TASK_SKILL = REPO_ROOT / "skills" / "start-task" / "SKILL.md"
FINISH_FEATURE_SKILL = REPO_ROOT / "skills" / "finish-feature" / "SKILL.md"
AUTONOMOUS_BACKLOG_LOOP_SKILL = REPO_ROOT / "skills" / "autonomous-backlog-loop" / "SKILL.md"
TASK_EXECUTION_HANDOFF_SPEC = REPO_ROOT / "openspec" / "specs" / "task-execution-handoff" / "spec.md"
WORKFLOW_REFERENCE = REPO_ROOT / "docs" / "planning" / "WORKFLOW_REFERENCE.md"


class WorkflowContractDocsTests(unittest.TestCase):
    def test_start_task_skill_prefers_existing_feature_worktree_for_later_tasks(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("otherwise prefer the existing feature branch/worktree", start_task_skill)
        self.assertIn("require the resolver payload to include the selected repo root", start_task_skill)

    def test_start_task_skill_reads_change_context_before_updating_plan(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("Read the linked change context before updating the task implementation plan", start_task_skill)
        self.assertIn("read `proposal.md`, `design.md`, linked specs, `tasks.md`", start_task_skill)
        self.assertIn("use that context to update the task implementation plan", start_task_skill)

    def test_start_task_skill_requires_gpt_5_4_mini_plan_review_loop(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("spawn a `gpt-5.4-mini` reviewer subagent", start_task_skill)
        self.assertIn("fully cover the selected task's intended change and proof obligations", start_task_skill)
        self.assertIn("return to step 5 to update the implementation plan and rerun this review until it passes", start_task_skill)

    def test_start_task_skill_requires_validation_section_completion_before_handoff(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("every step in the implementation plan's validation section has been completed successfully", start_task_skill)
        self.assertIn("leaving only the fresh completion-time verification gate owned by `complete-task`", start_task_skill)

    def test_start_task_skill_requires_changed_tests_narrowed_contract_review_question(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("changed tests narrowed contract?", start_task_skill)
        self.assertIn("compare the new assertions to the task plan", start_task_skill)

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

    def test_autonomous_backlog_loop_reuses_feature_worktree_for_continuation(self) -> None:
        autonomous_loop_skill = AUTONOMOUS_BACKLOG_LOOP_SKILL.read_text(encoding="utf-8")

        self.assertIn("revalidate the effective repo root for `<feature-id>`", autonomous_loop_skill)
        self.assertIn("run feature-scoped `audit-workflow` from that selected repo root", autonomous_loop_skill)

    def test_workflow_reference_prefers_canonical_end_to_end_fixtures_for_contract_tests(self) -> None:
        workflow_reference = WORKFLOW_REFERENCE.read_text(encoding="utf-8")

        self.assertIn("prefer canonical end-to-end fixtures", workflow_reference)
        self.assertIn("workflow contract behavior is under test", workflow_reference)

    def test_stable_handoff_spec_mentions_autonomous_finish_feature_gate(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("### Requirement: Autonomous orchestration routes completion through finish-feature", task_execution_handoff_spec)
        self.assertIn("#### Scenario: Autonomous loop completes the final task for a feature", task_execution_handoff_spec)

    def test_stable_handoff_spec_requires_later_tasks_to_resolve_from_feature_worktree(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("Later execution task resumes on the same feature", task_execution_handoff_spec)
        self.assertIn("resolves that later task from the reusable feature worktree", task_execution_handoff_spec)
        self.assertIn("Autonomous continuation reuses the same feature worktree", task_execution_handoff_spec)


if __name__ == "__main__":
    unittest.main()

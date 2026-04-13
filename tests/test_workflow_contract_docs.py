from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
START_TASK_SKILL = REPO_ROOT / "skills" / "start-task" / "SKILL.md"
COMPLETE_TASK_SKILL = REPO_ROOT / "skills" / "complete-task" / "SKILL.md"
FINISH_FEATURE_SKILL = REPO_ROOT / "skills" / "finish-feature" / "SKILL.md"
AUTONOMOUS_BACKLOG_LOOP_SKILL = REPO_ROOT / "skills" / "autonomous-backlog-loop" / "SKILL.md"
TASK_EXECUTION_HANDOFF_SPEC = REPO_ROOT / "openspec" / "specs" / "task-execution-handoff" / "spec.md"
FEATURE_EXECUTION_TRACKING_SPEC = REPO_ROOT / "openspec" / "specs" / "feature-execution-tracking" / "spec.md"
WORKFLOW_AUDIT_AND_REPAIR_SPEC = REPO_ROOT / "openspec" / "specs" / "workflow-audit-and-repair" / "spec.md"
WORKFLOW_REFERENCE = REPO_ROOT / "docs" / "planning" / "WORKFLOW_REFERENCE.md"
FEATURE_TEMPLATE = REPO_ROOT / "docs" / "planning" / "template" / "feature-template.md"


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
        self.assertIn("leaving only the fresh completion-time reconciliation gate owned by `complete-task`", start_task_skill)

    def test_start_task_skill_forbids_task_agent_from_continuing_to_next_workflow_task(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("Execute only the selected top-level OpenSpec task", start_task_skill)
        self.assertIn("do not mark the selected OpenSpec task checkbox done", start_task_skill)
        self.assertIn("do not start implementation work for any downstream top-level OpenSpec task", start_task_skill)
        self.assertIn("do not commit task-closure state", start_task_skill)

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

    def test_complete_task_skill_forbids_starting_next_task(self) -> None:
        complete_task_skill = COMPLETE_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("does not start the next task", complete_task_skill)
        self.assertIn("clear `Current Task` to `none`", complete_task_skill)
        self.assertIn("do not start another task", complete_task_skill)
        self.assertIn("downstream task execution must go through a later explicit `start-task` invocation", complete_task_skill)

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
            "complete `complete-task` before resolving or starting any downstream top-level task",
            autonomous_loop_skill,
        )
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
        self.assertIn("canonical machine-readable payload", workflow_reference)
        self.assertIn("structured review verdicts", workflow_reference)

    def test_feature_template_includes_structured_review_verdict_fields(self) -> None:
        feature_template = FEATURE_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("Review Scope", feature_template)
        self.assertIn("Review Target", feature_template)
        self.assertIn("Review Verdict", feature_template)
        self.assertIn("Blocking Findings", feature_template)
        self.assertIn("Review Terminal", feature_template)

    def test_planning_stage_lesson_lifecycle_docs_expose_canonical_handoff_lines(self) -> None:
        shape_backlog_item_skill = (REPO_ROOT / "skills" / "shape-backlog-item" / "SKILL.md").read_text(encoding="utf-8")
        ready_feature_skill = (REPO_ROOT / "skills" / "ready-feature" / "SKILL.md").read_text(encoding="utf-8")
        finish_feature_skill = FINISH_FEATURE_SKILL.read_text(encoding="utf-8")
        workflow_reference = WORKFLOW_REFERENCE.read_text(encoding="utf-8")
        feature_template = FEATURE_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("call `retrieve-lessons`", shape_backlog_item_skill)
        self.assertIn("task-scoped canonical `Retrieved Lesson IDs: ...` line for `shaping`", shape_backlog_item_skill)
        self.assertIn("call `record-lesson-usage`", shape_backlog_item_skill)
        self.assertIn("record any warranted high-signal notes in `docs/lessons/notes.md`", shape_backlog_item_skill)
        self.assertIn("before the independent readiness review", ready_feature_skill)
        self.assertIn("call `retrieve-lessons`", ready_feature_skill)
        self.assertIn("task-scoped canonical `Retrieved Lesson IDs: ...` line for `ready`", ready_feature_skill)
        self.assertIn("call `record-lesson-usage`", ready_feature_skill)
        self.assertIn("record any warranted high-signal notes in `docs/lessons/notes.md`", ready_feature_skill)
        self.assertIn("Retrieved Lesson IDs", feature_template)
        self.assertIn("Lesson Usage", feature_template)
        self.assertIn("Lesson lifecycle integrates with shaping, readiness, task execution, and feature completion", workflow_reference)
        self.assertIn("Earlier workflow stages record lesson usage and high-signal notes only", finish_feature_skill)
        self.assertIn("only workflow stage that runs `distill-lessons`", finish_feature_skill)

    def test_stable_handoff_spec_mentions_autonomous_finish_feature_gate(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("### Requirement: Autonomous orchestration routes completion through finish-feature", task_execution_handoff_spec)
        self.assertIn("#### Scenario: Autonomous loop completes the final task for a feature", task_execution_handoff_spec)
        self.assertIn("Autonomous continuation stays inside one feature-scoped agent", task_execution_handoff_spec)

    def test_stable_handoff_spec_requires_later_tasks_to_resolve_from_feature_worktree(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("Later execution task resumes on the same feature", task_execution_handoff_spec)
        self.assertIn("resolves that later task from the reusable feature worktree", task_execution_handoff_spec)
        self.assertIn("Autonomous continuation reuses the same feature worktree", task_execution_handoff_spec)

    def test_stable_handoff_spec_defines_continuation_payload(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("fields `action`, `target_feature_id`, `target_task_id`, `reason`, and `requires_human_decision`", task_execution_handoff_spec)
        self.assertIn("action=finish_feature", task_execution_handoff_spec)
        self.assertIn("action=start_task", task_execution_handoff_spec)
        self.assertIn("requires_human_decision=true", task_execution_handoff_spec)

    def test_feature_execution_tracking_spec_defines_structured_review_verdict_fields(self) -> None:
        feature_execution_tracking_spec = FEATURE_EXECUTION_TRACKING_SPEC.read_text(encoding="utf-8")

        self.assertIn("### Requirement: Feature files carry structured review verdict state", feature_execution_tracking_spec)
        self.assertIn("Review Scope", feature_execution_tracking_spec)
        self.assertIn("Review Target", feature_execution_tracking_spec)
        self.assertIn("Review Verdict", feature_execution_tracking_spec)
        self.assertIn("Blocking Findings", feature_execution_tracking_spec)
        self.assertIn("Review Terminal", feature_execution_tracking_spec)

    def test_workflow_audit_and_repair_spec_allows_selected_feature_scoping_with_diagnostics(self) -> None:
        workflow_audit_and_repair_spec = WORKFLOW_AUDIT_AND_REPAIR_SPEC.read_text(encoding="utf-8")

        self.assertIn("Execution-scoped helpers block on selected-feature integrity", workflow_audit_and_repair_spec)
        self.assertIn("Execution-scoped helpers report unrelated active drift separately", workflow_audit_and_repair_spec)
        self.assertIn("direct `audit-workflow` remains the global pass/fail integrity gate", workflow_audit_and_repair_spec)


if __name__ == "__main__":
    unittest.main()

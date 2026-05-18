from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
START_TASK_SKILL = REPO_ROOT / "skills" / "start-task" / "SKILL.md"
COMPLETE_TASK_SKILL = REPO_ROOT / "skills" / "complete-task" / "SKILL.md"
READY_FEATURE_SKILL = REPO_ROOT / "skills" / "ready-feature" / "SKILL.md"
FINISH_FEATURE_SKILL = REPO_ROOT / "skills" / "finish-feature" / "SKILL.md"
AUTONOMOUS_BACKLOG_LOOP_SKILL = REPO_ROOT / "skills" / "autonomous-backlog-loop" / "SKILL.md"
TASK_EXECUTION_HANDOFF_SPEC = REPO_ROOT / "openspec" / "specs" / "task-execution-handoff" / "spec.md"
FEATURE_EXECUTION_TRACKING_SPEC = REPO_ROOT / "openspec" / "specs" / "feature-execution-tracking" / "spec.md"
WORKFLOW_AUDIT_AND_REPAIR_SPEC = REPO_ROOT / "openspec" / "specs" / "workflow-audit-and-repair" / "spec.md"
SHAPE_BACKLOG_ITEM_SKILL = REPO_ROOT / "skills" / "shape-backlog-item" / "SKILL.md"
PRIORITIZE_BACKLOG_SKILL = REPO_ROOT / "skills" / "prioritize-backlog" / "SKILL.md"
WORKFLOW_REFERENCE = REPO_ROOT / "docs" / "planning" / "WORKFLOW_REFERENCE.md"
WORKFLOW_REFERENCE_TEMPLATE = (
    REPO_ROOT
    / "skills"
    / "initialize-workflow-artifacts"
    / "templates"
    / "WORKFLOW_REFERENCE.md"
)
FEATURE_TEMPLATE = REPO_ROOT / "docs" / "planning" / "template" / "feature-template.md"


class WorkflowContractDocsTests(unittest.TestCase):
    def test_start_task_skill_prefers_existing_feature_worktree_for_later_tasks(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("otherwise prefer the existing feature branch/worktree", start_task_skill)
        self.assertIn("require the resolver payload to include the selected repo root", start_task_skill)

    def test_start_task_skill_reads_change_context_before_updating_plan(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn(
            "read the linked change context before drafting or updating the task implementation plan",
            start_task_skill,
        )
        self.assertIn("read `proposal.md`, `design.md`, linked specs, `tasks.md`", start_task_skill)
        self.assertIn(
            "the task implementation plan at `openspec/changes/<change-id>/implementation-plans/<task-id>.md`",
            start_task_skill,
        )

    def test_start_task_skill_requires_gpt_5_4_mini_plan_review_loop(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("spawn a lightweight independent reviewer subagent", start_task_skill)
        self.assertIn("fully cover the selected task's intended change and proof obligations", start_task_skill)
        self.assertIn("return to step 7 to update the implementation plan and rerun this review until it passes", start_task_skill)

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
        self.assertIn("canonical `completion_handoff` payload", complete_task_skill)
        self.assertIn("clear `Current Task` to `none`", complete_task_skill)
        self.assertIn("do not start another task", complete_task_skill)
        self.assertIn("downstream task execution must go through a later explicit `start-task` invocation", complete_task_skill)

    def test_complete_task_skill_requires_canonical_review_verdict_lines(self) -> None:
        complete_task_skill = COMPLETE_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("canonical `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal` lines", complete_task_skill)
        self.assertIn("downstream workflow can consume it without prose inference", complete_task_skill)

    def test_ready_feature_skill_requires_canonical_review_verdict_lines(self) -> None:
        ready_feature_skill = READY_FEATURE_SKILL.read_text(encoding="utf-8")

        self.assertIn("record the readiness review verdict", ready_feature_skill)
        self.assertIn("canonical `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal` lines", ready_feature_skill)
        self.assertIn("consumed without prose inference", ready_feature_skill)

    def test_autonomous_backlog_loop_routes_completion_through_finish_feature(self) -> None:
        autonomous_loop_skill = AUTONOMOUS_BACKLOG_LOOP_SKILL.read_text(encoding="utf-8")

        self.assertIn("if the task finishes cleanly, invoke `complete-task`", autonomous_loop_skill)
        self.assertIn(
            "if `completion_handoff.action` is `finish_feature`, invoke `finish-feature` before any downstream cleanup",
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
            "if `completion_handoff.action` is `start_task`, continue the feature loop",
            autonomous_loop_skill,
        )
        self.assertIn(
            "if `completion_handoff.action` is `stop`, exit the feature loop and return control",
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
        self.assertIn("stage-scoped canonical `Retrieved Lesson IDs: ...` line for `shaping`", shape_backlog_item_skill)
        self.assertIn("call `record-lesson-usage`", shape_backlog_item_skill)
        self.assertIn("record any warranted high-signal notes in `docs/lessons/notes.md`", shape_backlog_item_skill)
        self.assertIn("before the independent readiness review", ready_feature_skill)
        self.assertIn("call `retrieve-lessons`", ready_feature_skill)
        self.assertIn("stage-scoped canonical `Retrieved Lesson IDs: ...` line for `ready`", ready_feature_skill)
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

        self.assertIn("Selected-feature continuation fails when the intended worktree is missing", task_execution_handoff_spec)
        self.assertIn("later task execution or autonomous continuation targets a selected feature already in `[IN_PROGRESS]`", task_execution_handoff_spec)
        self.assertIn("it does not silently continue from the primary or current checkout", task_execution_handoff_spec)

    def test_stable_handoff_spec_defines_continuation_payload(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")

        self.assertIn("canonical `completion_handoff` payload", task_execution_handoff_spec)
        self.assertIn("action=start_task", task_execution_handoff_spec)
        self.assertIn("requires_human_decision=true", task_execution_handoff_spec)
        self.assertIn("the workflow reports that `finish-feature` is startable", task_execution_handoff_spec)

    def test_stable_handoff_spec_requires_task_completion_review_verdict_lines(self) -> None:
        feature_execution_tracking_spec = FEATURE_EXECUTION_TRACKING_SPEC.read_text(encoding="utf-8")

        self.assertIn("Workflow stages emit the canonical review-verdict lines they own", feature_execution_tracking_spec)
        self.assertIn("ready-feature` or `complete-task` passes through a required review gate", feature_execution_tracking_spec)
        self.assertIn("Review Scope", feature_execution_tracking_spec)
        self.assertIn("Review Target", feature_execution_tracking_spec)
        self.assertIn("Review Verdict", feature_execution_tracking_spec)
        self.assertIn("Blocking Findings", feature_execution_tracking_spec)
        self.assertIn("Review Terminal", feature_execution_tracking_spec)

    def test_feature_execution_tracking_spec_defines_structured_review_verdict_fields(self) -> None:
        feature_execution_tracking_spec = FEATURE_EXECUTION_TRACKING_SPEC.read_text(encoding="utf-8")

        self.assertIn("### Requirement: Feature files carry structured review verdict state", feature_execution_tracking_spec)
        self.assertIn("Review Scope", feature_execution_tracking_spec)
        self.assertIn("Review Target", feature_execution_tracking_spec)
        self.assertIn("Review Verdict", feature_execution_tracking_spec)
        self.assertIn("Blocking Findings", feature_execution_tracking_spec)
        self.assertIn("Review Terminal", feature_execution_tracking_spec)

    def test_feature_template_fallback_matches_tracked_template(self) -> None:
        import sys

        skills_root = REPO_ROOT / "skills"
        if str(skills_root) not in sys.path:
            sys.path.insert(0, str(skills_root))
        from _workflow.feature_file import _FALLBACK_FEATURE_TEMPLATE  # type: ignore[attr-defined]

        tracked = FEATURE_TEMPLATE.read_text(encoding="utf-8")
        self.assertEqual(
            _FALLBACK_FEATURE_TEMPLATE,
            tracked,
            "_FALLBACK_FEATURE_TEMPLATE in skills/_workflow/feature_file.py is out of sync "
            "with docs/planning/template/feature-template.md. Update the Python constant to "
            "match the tracked template so the fallback does not silently downgrade content.",
        )

    def test_workflow_reference_template_matches_live_reference(self) -> None:
        live = WORKFLOW_REFERENCE.read_text(encoding="utf-8")
        template = WORKFLOW_REFERENCE_TEMPLATE.read_text(encoding="utf-8")

        self.assertEqual(
            template,
            live,
            "skills/initialize-workflow-artifacts/templates/WORKFLOW_REFERENCE.md is out of sync "
            "with docs/planning/WORKFLOW_REFERENCE.md — run "
            "`cp docs/planning/WORKFLOW_REFERENCE.md "
            "skills/initialize-workflow-artifacts/templates/WORKFLOW_REFERENCE.md`.",
        )

    def test_stage_level_skills_describe_retrieved_lesson_ids_as_stage_scoped(self) -> None:
        shape_backlog_item_skill = SHAPE_BACKLOG_ITEM_SKILL.read_text(encoding="utf-8")
        ready_feature_skill = READY_FEATURE_SKILL.read_text(encoding="utf-8")

        self.assertIn(
            "stage-scoped canonical `Retrieved Lesson IDs: ...` line for `shaping`",
            shape_backlog_item_skill,
        )
        self.assertIn(
            "stage-scoped canonical `Retrieved Lesson IDs: ...` line for `ready`",
            ready_feature_skill,
        )
        self.assertNotIn(
            "task-scoped canonical `Retrieved Lesson IDs: ...` line for `shaping`",
            shape_backlog_item_skill,
        )
        self.assertNotIn(
            "task-scoped canonical `Retrieved Lesson IDs: ...` line for `ready`",
            ready_feature_skill,
        )

    def test_task_level_skills_describe_retrieved_lesson_ids_as_task_scoped(self) -> None:
        start_task_skill = START_TASK_SKILL.read_text(encoding="utf-8")
        complete_task_skill = COMPLETE_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("task-scoped canonical `Retrieved Lesson IDs: ...` line", start_task_skill)
        self.assertIn("task-scoped canonical `Retrieved Lesson IDs: ...` line", complete_task_skill)

    def test_complete_task_skill_documents_completion_handoff_output_contract(self) -> None:
        complete_task_skill = COMPLETE_TASK_SKILL.read_text(encoding="utf-8")

        self.assertIn("## Output Contract", complete_task_skill)
        self.assertIn("`completion_handoff`", complete_task_skill)
        for field in ("`action`", "`target_feature_id`", "`target_task_id`", "`reason`", "`requires_human_decision`"):
            self.assertIn(field, complete_task_skill, f"Output Contract is missing field {field}")
        for action in ("`start_task`", "`finish_feature`", "`stop`"):
            self.assertIn(action, complete_task_skill, f"Output Contract is missing action {action}")

    def test_workflow_wrapper_preamble_remains_in_owning_skills(self) -> None:
        """Pin the `It is a workflow wrapper around` fragment across every SKILL.md
        that currently uses it. v1-f019 accepted this repetition explicitly; any
        future one-sided removal should fail here instead of silently drifting.
        """
        fragment = "It is a workflow wrapper around"
        for path in (
            START_TASK_SKILL,
            READY_FEATURE_SKILL,
            SHAPE_BACKLOG_ITEM_SKILL,
            PRIORITIZE_BACKLOG_SKILL,
        ):
            self.assertIn(
                fragment,
                path.read_text(encoding="utf-8"),
                f"{path.relative_to(REPO_ROOT)} lost the shared preamble '{fragment}'. "
                "Either restore it here or remove it from every owning SKILL.md in the same change.",
            )

    def test_workflow_audit_and_repair_spec_allows_selected_feature_scoping_with_diagnostics(self) -> None:
        task_execution_handoff_spec = TASK_EXECUTION_HANDOFF_SPEC.read_text(encoding="utf-8")
        workflow_audit_and_repair_spec = WORKFLOW_AUDIT_AND_REPAIR_SPEC.read_text(encoding="utf-8")

        self.assertIn("Selected-feature helper fails closed on missing worktree", workflow_audit_and_repair_spec)
        self.assertIn("it does not silently reuse the current checkout as a substitute for the missing feature worktree", workflow_audit_and_repair_spec)
        self.assertIn("Selected-feature continuation reports unrelated drift without blocking", task_execution_handoff_spec)
        self.assertIn("the unrelated drift is surfaced as diagnostic workflow information rather than a selected-feature stop condition", task_execution_handoff_spec)


if __name__ == "__main__":
    unittest.main()

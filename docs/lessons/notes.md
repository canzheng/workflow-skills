- id: N-001
  status: open
  created_at: 2026-04-14
  updated_at: 2026-04-14
  feature_ref: v1-f018
  task_ref: ""
  kind: signal
  context: Review of shipped v1-f018 against its archived design and implementation-plan scope after local merge to main.
  observation: The change added stable docs, template fields, a review-verdict parser, and parser coverage, but the workflow skills that should emit and rely on canonical review verdict lines were not updated in the same way. ready-feature still describes the review gate without requiring Review Scope or Review Verdict output, complete-task still describes review expectations without canonical verdict emission, and there are no runtime consumers of parsed verdicts outside the parser test.
  why_notable: This is a review-triggered rework signal because the feature looked complete at the contract and helper layer while the operator-facing workflow and end-to-end behavior for structured review verdicts remained only partially implemented.
  current_hypothesis: The change validated the new verdict schema at the docs and parser layer but did not add an end-to-end proof obligation that the wrapped skills actually write and consume those canonical lines during readiness and task completion.
  artifacts:
    - openspec/changes/archive/2026-04-13-v1-f018-reduce-status-only-workflow-overhead/design.md
    - openspec/changes/archive/2026-04-13-v1-f018-reduce-status-only-workflow-overhead/specs/feature-execution-tracking/spec.md
    - openspec/changes/archive/2026-04-13-v1-f018-reduce-status-only-workflow-overhead/implementation-plans/2.md
    - skills/ready-feature/SKILL.md
    - skills/complete-task/SKILL.md
    - skills/_workflow/workflow_state.py
    - skills/_workflow/tests/test_workflow_state.py
  next_check: Update the emitting skills and their end-to-end tests so readiness and task-completion review actually record canonical verdict lines, then add at least one downstream consumer check that uses those emitted lines instead of prose-only notes.
  outcome: ""
  what_worked: ""
  what_did_not_work: ""
  reusable_insight: ""
  do_differently_next_time: ""
  catch_earlier_by: ""
  distilled_into: []

- id: N-002
  status: open
  created_at: 2026-04-14
  updated_at: 2026-04-14
  feature_ref: v1-f018
  task_ref: ""
  kind: signal
  context: Same post-implementation review of v1-f018 with attention on the selected-feature worktree continuation and finalization path.
  observation: The change did fix explicit selected-feature scoping in finish-feature and taught autonomous routing to prefer the feature worktree, but the shared helper still falls back to the current checkout when it cannot resolve a unique active feature worktree. That leaves the fail-closed behavior promised by the implementation plan and autonomous-loop contract only partially implemented.
  why_notable: The review concern is process-level rather than patch-level. The plan and skill contract promised a stronger guard than the helper now enforces, so a missing-worktree path can still silently drift back toward stale primary-checkout continuation unless callers add their own protection.
  current_hypothesis: Positive-path and dirty-worktree tests were added, but the missing-worktree negative path was not covered, so the older helper fallback survived while the surrounding design and skill text moved to the stricter contract.
  artifacts:
    - openspec/changes/archive/2026-04-13-v1-f018-reduce-status-only-workflow-overhead/implementation-plans/2.md
    - skills/autonomous-backlog-loop/SKILL.md
    - skills/_workflow/workflow_state.py
    - skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py
    - tests/test_workflow_openspec_integration.py
  next_check: Decide whether the helper should truly fail closed when the intended feature worktree is missing or ambiguous, then add a regression test for that exact missing-worktree path in autonomous continuation and any other resolver that depends on the shared helper.
  outcome: ""
  what_worked: ""
  what_did_not_work: ""
  reusable_insight: ""
  do_differently_next_time: ""
  catch_earlier_by: ""
  distilled_into: []

- id: N-001
  status: distilled
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
  outcome: The reopened remediation updated the owning skill guidance and added a real start-task resolver consumer for canonical readiness review verdict state.
  what_worked: Requiring both emission guidance and a runtime consumer path closed the parser-only gap cleanly.
  what_did_not_work: Treating schema text, template fields, and parser coverage as sufficient proof left the original feature incomplete.
  reusable_insight: Workflow metadata changes need an emitter path and a consumer path in the same feature.
  do_differently_next_time: Add a proof obligation that names the runtime consumer before closing the original implementation task.
  catch_earlier_by: Ask during review whether any runtime resolver or downstream workflow step reads the new metadata outside parser-only tests.
  distilled_into:
    - L-001

- id: N-002
  status: distilled
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
  outcome: The reopened remediation changed the shared worktree-resolution helper to fail closed and added the missing autonomous-resolver regression for the absent-worktree path.
  what_worked: Adding the exact negative-path test exposed and removed the stale checkout fallback.
  what_did_not_work: Happy-path and dirty-worktree coverage alone did not prove the helper enforced the stronger contract.
  reusable_insight: Resolver hardening for worktree targeting needs explicit missing-resource tests.
  do_differently_next_time: Add missing-worktree and ambiguous-worktree tests whenever a feature-scoped resolver is supposed to fail closed.
  catch_earlier_by: Review the shared helper and ask what happens when no unique active worktree exists.
  distilled_into:
    - L-002

- id: N-003
  status: open
  created_at: 2026-05-29
  updated_at: 2026-05-29
  feature_ref: ad-hoc-claim-evidence-lint
  task_ref: ""
  kind: signal
  context: User supplied review synthesis that repeated assertions from memory caused planning and review rework, including incorrect numeric pins and incorrect claims about centralized code structure.
  observation: The existing guidance requiring grep/Read evidence for correctness-critical pinned claims was prose-only; ready-feature and start-task had no deterministic gate that could reject unsupported file-line or numeric claims before review.
  why_notable: This is a review-loop signal because the same human correction recurred across tasks, and relying on agent memory let unsupported claims reach plan/design artifacts where reviewers had to catch them manually.
  current_hypothesis: A focused lint over OpenSpec proposal, design, and implementation-plan files should turn the soft norm into a cheap blocking check while avoiding task/spec numbering noise.
  artifacts:
    - skills/_workflow/workflow_state.py
    - skills/_workflow/scripts/lint_openspec_claim_evidence.py
    - skills/ready-feature/SKILL.md
    - skills/start-task/SKILL.md
    - skills/_workflow/tests/test_workflow_state.py
    - skills/_workflow/tests/test_workflow_scripts.py
  next_check: Watch the lint during the next ready-feature/start-task pass for noisy false positives around legitimate numeric planning language, then narrow or broaden the regex based on concrete cases.
  outcome: Implemented a shared pinned-claim evidence lint and wired ready-feature/start-task guidance to run it before promotion or execution review.
  what_worked: Testing the unsupported file-line and numeric cases first kept the implementation focused on the specific review failure.
  what_did_not_work: ""
  reusable_insight: Repeated memory-based claim corrections need executable gates, not only prose lessons.
  do_differently_next_time: Add lint-level enforcement when a lesson describes a recurring review failure that can be detected mechanically.
  catch_earlier_by: During shaping/readiness review, ask whether each file-line citation or numeric pin has adjacent grep/Read output before accepting the artifact.
  distilled_into: []

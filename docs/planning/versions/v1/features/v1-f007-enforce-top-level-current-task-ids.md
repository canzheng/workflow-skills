# Feature: Enforce Top-Level Current Task IDs

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f007`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `enforce-top-level-current-task-ids`
- OpenSpec Specs:
  - `openspec/specs/feature-execution-tracking/spec.md`
  - `openspec/specs/workflow-audit-and-repair/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-25`
- Last Updated: `2026-03-27`

## 1. Validation Log
- `2026-03-27` Task `2`:
  - Run: `PYTHONPATH=skills .local/venv/bin/pytest skills/_workflow/tests/test_workflow_scripts.py -q`
  - Result: `17 tests passed in the disposable local virtualenv used for workflow task execution because pytest is not installed on the base shell PATH in this environment.`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `Passed after closing nested checklist items 2.1 and 2.2; completion_handoff.decision = stay_in_progress and next_ready_task_ids = ['3'].`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `Passed before task-state updates and again after them.`
  - Run: `git diff --check`
  - Result: `Passed before task completion and again after task-state updates.`
  - Review: `Local spec-compliance review found the task-2 diff stayed within audit-and-diagnosis reporting scope after the dedicated gpt-5.4-mini review agents stalled.`
  - Review: `Local code-quality review found no correctness, fixture, or maintainability issues in the reporting and script-test changes.`
- `2026-03-27` Task `1`:
  - Run: `PYTHONPATH=skills .local/venv/bin/pytest skills/_workflow/tests/test_workflow_state.py -q`
  - Result: `16 tests passed in the disposable local virtualenv used for workflow task execution because pytest is not installed on the base shell PATH in this environment.`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `Passed after closing nested checklist items 1.1 and 1.2; completion_handoff.decision = stay_in_progress and next_ready_task_ids = ['2', '3'].`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `Passed before task-state updates and again after them.`
  - Run: `git diff --check`
  - Result: `Passed before task completion and again after task-state updates.`
  - Review: `Local spec-compliance review found the task-1 diff stayed within shared-validation scope after the dedicated gpt-5.4-mini review agents stalled.`
  - Review: `Local code-quality review found no correctness or maintainability issues in the helper, test, or workflow-bookkeeping changes.`
- `2026-03-27` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass before promoting the feature to [READY] and pass after moving the feature to [READY]`
  - Inspection: `openspec/changes/enforce-top-level-current-task-ids/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/feature-execution-tracking/spec.md`, and `openspec/specs/workflow-audit-and-repair/spec.md` are present; top-level OpenSpec tasks `1`, `2`, and `3` all resolve to workflow status `ready` because they are unchecked, `Current Task` is `none`, and no workflow dependency blocks are present.`
  - Run: `openspec validate enforce-top-level-current-task-ids --type change --json --no-interactive`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `2`. `skills/audit-workflow/scripts/audit_workflow.py` now reports invalid nested `Current Task` values as normal workflow errors, and `skills/diagnose-workflow/scripts/diagnose_workflow.py` now emits a structured `invalid_current_task_metadata` finding instead of crashing. `completion_handoff.next_ready_task_ids` is `['3']`; handoff should resume with task `3` (`Coverage`).
- `2026-03-27`:
  - Current Task: `2`
  - Worktree State: `dirty`
  - Notes: Started task `2` in the existing feature worktree `../worktrees/workflow-skills/v1-f007-enforce-top-level-current-task-ids` after writing `openspec/changes/enforce-top-level-current-task-ids/implementation-plans/2.md`. Execution is scoped to surfacing invalid `Current Task` metadata through `audit-workflow` and `diagnose-workflow`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `1`. `skills/_workflow/workflow_state.py` now rejects nested `Current Task` values such as `1.1` while preserving valid top-level task id parsing. `completion_handoff.next_ready_task_ids` is `['2', '3']`; handoff should resume with task `2` by top-to-bottom order, while task `3` remains separately ready because it has no workflow dependency block.
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `dirty`
  - Notes: Started task `1` in feature worktree `../worktrees/workflow-skills/v1-f007-enforce-top-level-current-task-ids` after writing `openspec/changes/enforce-top-level-current-task-ids/implementation-plans/1.md`. Execution is scoped to shared `Current Task` validation in `skills/_workflow/workflow_state.py`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `enforce-top-level-current-task-ids`. Top-level OpenSpec tasks `1`, `2`, and `3` are ready to execute, so the feature can move to `[READY]`.

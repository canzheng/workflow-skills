# Feature: Detect Orphan OpenSpec Changes

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f004`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `detect-orphan-openspec-changes`
- OpenSpec Specs:
  - `openspec/specs/workflow-audit-and-repair/spec.md`
  - `openspec/specs/workflow-board-lifecycle/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-25`
- Last Updated: `2026-03-27`

## 1. Validation Log
- `2026-03-27` Readiness Review:
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass before promoting the feature to [READY]`
  - Inspection: `openspec/changes/detect-orphan-openspec-changes/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/workflow-audit-and-repair/spec.md`, and `openspec/specs/workflow-board-lifecycle/spec.md` are present.`
  - Run: `python3` readiness inspection using `skills._workflow.workflow_state.parse_tasks()` and `compute_task_readiness_drift()`
  - Result: `top-level OpenSpec tasks 1, 2, and 3 all resolve to workflow status ready, with no task-readiness drift`
  - Run: `openspec validate detect-orphan-openspec-changes --type change --json --no-interactive`
  - Result: `pass; summary totals report 1 passed, 0 failed`
- `2026-03-27` Task `1`:
  - Run: `python3` direct `skills/_workflow/tests/test_workflow_state.py` harness covering all `test_*` functions
  - Result: `15 tests passed, including the new orphan active-change enumeration, archive exclusion, and done-feature archived-linkage coverage`
  - Run: `python3 skills/complete-task/scripts/resolve_complete_task.py`
  - Result: `pass after closing nested items 1.1 and 1.2; completion_handoff reports decision stay_in_progress with next_ready_task_ids ['2', '3']`
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass with the feature in [IN_PROGRESS] and task 1 active`
  - Inspection: `git diff -- skills/_workflow/workflow_state.py skills/_workflow/tests/test_workflow_state.py docs/planning/versions/v1/BACKLOG.md docs/planning/versions/v1/features/v1-f004-detect-orphan-openspec-changes.md openspec/changes/detect-orphan-openspec-changes/implementation-plans/1.md openspec/changes/detect-orphan-openspec-changes/tasks.md`
  - Result: `reviewed locally; task-scoped changes are limited to shared change-linkage enumeration, narrow tests, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `detect-orphan-openspec-changes`. Top-level OpenSpec tasks `1`, `2`, and `3` are ready to execute, so the feature can move to `[READY]`.
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `dirty`
  - Notes: Started task `1` in feature worktree `v1-f004-detect-orphan-openspec-changes` after writing `openspec/changes/detect-orphan-openspec-changes/implementation-plans/1.md`. Execution is scoped to shared active-change enumeration helpers.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `1`. Shared helper logic now enumerates active-versus-linked OpenSpec changes while excluding archived directories and preserving completed-feature archived-linkage behavior. The feature remains `[IN_PROGRESS]`; next ready tasks are `2` and `3`.

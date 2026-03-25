# Feature: Add Feature Completion Handoff Gate

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f006`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `add-feature-completion-handoff-gate`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/feature-execution-tracking/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-25`
- Last Updated: `2026-03-26`

## 1. Validation Log
- `2026-03-26` Task `1`:
  - Run: `python3 -m unittest tests.test_workflow_openspec_integration -v`
  - Result: `9 tests passed, including the new completion-handoff cases for the stay-in-progress and confirm-feature-acceptance branches.`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `Passed for docs/planning/versions/v1 before and after task-state updates.`
  - Run: `git diff --check`
  - Result: `Passed with no patch-format issues.`

## 2. Handoff Notes
- `2026-03-26`:
  - Current Task: `1`
  - Worktree State: `dirty`
  - Notes: Task `1` started in the feature worktree `../worktrees/workflow-skills/v1-f006-add-feature-completion-handoff-gate`. The execution focus is the `complete-task` handoff that decides whether the feature remains in `[IN_PROGRESS]` or becomes eligible for `[DONE]`.
- `2026-03-26`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Task `1` completed. The resolver now reports `completion_handoff.decision = stay_in_progress`, so the feature remains in `[IN_PROGRESS]` and top-level task `2` is ready next.

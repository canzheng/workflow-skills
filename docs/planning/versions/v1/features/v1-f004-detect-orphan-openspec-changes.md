# Feature: Detect Orphan OpenSpec Changes

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f004`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
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

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `detect-orphan-openspec-changes`. Top-level OpenSpec tasks `1`, `2`, and `3` are ready to execute, so the feature can move to `[READY]`.

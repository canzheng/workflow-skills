# Feature: Integrate Lessons With Workflow

## 0. Meta
- Feature ID: `v1-f016`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `integrate-lessons-with-workflow`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/feature-execution-tracking/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
  - This field is the active execution marker for the implemented workflow; OpenSpec `tasks.md` remains the checked/unchecked task ledger.
- Created: `2026-04-08`
- Last Updated: `2026-04-08`

## 1. Validation Log
- `2026-04-08` Task `shape`:
  - Run: `openspec status --change "integrate-lessons-with-workflow" --json`
  - Result: `pass; proposal, design, specs, and tasks are present for the change`
  - Evidence: `manual_inspection`
- `2026-04-08` Task `shape`:
  - Run: `rtk bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass`
  - Evidence: `manual_inspection`
- `2026-04-08` Task `1`:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/start-task/scripts/resolve_start_task.py" --repo-root /Users/canzheng/.config/superpowers/worktrees/workflow-skills/v1-f016-lesson-lifecycle-workflow`
  - Result: `pass; selected task 1 and implementation plan path openspec/changes/integrate-lessons-with-workflow/implementation-plans/1.md`
  - Evidence: `runtime_path`
- `2026-04-08` Task `1`:
  - Run: `rtk git diff --check`
  - Result: `pass`
  - Evidence: `manual_inspection`
- `2026-04-08` Task `1`:
  - Run: `rtk bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass`
  - Evidence: `schema`

## 2. Handoff Notes
- `2026-04-08`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `1`. The workflow now integrates lesson retrieval at task start, lesson usage reconciliation at task completion, and lesson promotion at feature finish. The next ready task is `2`.
  - Proof Obligations: `The workflow must carry retrieved lesson IDs through the feature file so complete-task can reconcile usage, then capture and promote lessons at the correct lifecycle points without automating refresh-lessons.`

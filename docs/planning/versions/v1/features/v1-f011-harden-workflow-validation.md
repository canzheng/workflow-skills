# Feature: Harden Workflow Validation

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f011`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `v1-f011-harden-workflow-validation`
- OpenSpec Specs:
  - `openspec/specs/workflow-audit-and-repair/spec.md`
  - `openspec/specs/openspec-change-integration/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-27`
- Last Updated: `2026-03-27`

## 1. Validation Log
- `2026-03-27` Readiness Review:
  - Run: `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass before promoting the feature to [READY] and pass after moving the feature to [READY]`
  - Inspection: `openspec/changes/v1-f011-harden-workflow-validation/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/workflow-audit-and-repair/spec.md`, and `openspec/specs/openspec-change-integration/spec.md` are present; top-level OpenSpec task \`1\` resolves to workflow status \`ready\`, while tasks \`2\` and \`3\` remain blocked by explicit \`Depends On\` references.`
  - Run: `openspec validate v1-f011-harden-workflow-validation --type change --json --no-interactive`
  - Result: `pass`
- `2026-03-27` Task `1`:
  - Run: `bin/run-python.sh -m pytest tests/test_diagnose_workflow.py -q -k 'missing_current_version or missing_active_backlog'`
  - Result: `failed before the fix with tracebacks from collect_openspec_change_linkage(...), then passed after the diagnose fallback guard was added`
  - Run: `bin/run-python.sh -m pytest tests/test_diagnose_workflow.py -q`
  - Result: `10 passed in 0.53s`
  - Run: `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass with the feature in [IN_PROGRESS] and task 1 active, then pass again after clearing Current Task and checking off OpenSpec task 1`
  - Run: `python3 skills/diagnose-workflow/scripts/diagnose_workflow.py --repo-root .`
  - Result: `pass; JSON status is ok with active_task_count=1 during task execution and no findings in the clean feature worktree`
  - Run: `bin/run-python.sh skills/complete-task/scripts/resolve_complete_task.py`
  - Result: `pass after closing nested checklist items 1.1 and 1.2 while task 1 remained active; completion_handoff.decision = stay_in_progress, next_ready_task_ids = ['2'], and remaining_open_task_ids = ['2', '3']`
  - Inspection: `git diff -- skills/diagnose-workflow/scripts/diagnose_workflow.py tests/test_diagnose_workflow.py openspec/changes/v1-f011-harden-workflow-validation/implementation-plans/1.md docs/planning/versions/v1/BACKLOG.md docs/planning/versions/v1/features/v1-f011-harden-workflow-validation.md`
  - Result: `reviewed locally; task-scoped changes are limited to diagnose fallback control flow, focused regression coverage, the task implementation plan, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`
  - Review: `Focused local task review found no correctness, regression, or scope-drift issues in the task-1 diff.`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `v1-f011-harden-workflow-validation`. Top-level OpenSpec task `1` is ready to execute, so the feature can move to `[READY]`.
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `resumed clean feature worktree at ../worktrees/workflow-skills/v1-f011-harden-workflow-validation on branch v1-f011-harden-workflow-validation`
  - Notes: Task `1` entered active execution after a passing workflow audit and resolver confirmation that it is the next ready task. The task implementation plan now lives at `openspec/changes/v1-f011-harden-workflow-validation/implementation-plans/1.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `task-1 changes ready to commit on branch v1-f011-harden-workflow-validation in ../worktrees/workflow-skills/v1-f011-harden-workflow-validation`
  - Notes: Completed task `1`. `skills/diagnose-workflow/scripts/diagnose_workflow.py` now preserves structured findings when `docs/planning/current_version` or the active `BACKLOG.md` is missing, and task `2` is the next ready execution unit while task `3` remains blocked by dependencies.

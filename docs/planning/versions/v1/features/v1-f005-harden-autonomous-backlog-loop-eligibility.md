# Feature: Harden Autonomous Backlog Loop Eligibility

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f005`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `harden-autonomous-backlog-loop-eligibility`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/workflow-audit-and-repair/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-25`
- Last Updated: `2026-03-27`

## 1. Validation Log
- `2026-03-27` Task `1`:
  - Run: `conda run -n workflow python -m pytest skills/_workflow/tests/test_workflow_scripts.py -k 'autonomous_backlog_action and (missing_openspec_change_metadata or malformed_active_feature or missing_active_change_dir or normal_precedence or design_mode_skips_ready_and_selects_shape or design_mode_falls_back_to_backlog or feature_exhausted_without_design_work)' -q`
  - Result: `6 passed, 14 deselected in 0.36s`
  - Run: `conda run -n workflow python -m pytest skills/_workflow/tests/test_workflow_scripts.py -k 'autonomous_backlog_action' -q`
  - Result: `9 passed, 11 deselected in 0.48s`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass with the feature in [IN_PROGRESS] and task 1 active, then pass again after clearing Current Task and checking off OpenSpec task 1`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `pass after closing nested checklist items 1.1 and 1.2 while task 1 remained active; completion_handoff.decision = stay_in_progress, next_ready_task_ids = ['2'], and remaining_open_task_ids = ['2', '3']`
  - Inspection: `git diff -- docs/planning/versions/v1/BACKLOG.md docs/planning/versions/v1/features/v1-f005-harden-autonomous-backlog-loop-eligibility.md openspec/changes/harden-autonomous-backlog-loop-eligibility/tasks.md skills/_workflow/tests/test_workflow_scripts.py skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py openspec/changes/harden-autonomous-backlog-loop-eligibility/implementation-plans/1.md`
  - Result: `reviewed locally; task-scoped changes are limited to active-feature eligibility validation, fixture support for linked OpenSpec metadata, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`
  - Run: `python skills/start-task/scripts/resolve_start_task.py --repo-root .`
  - Result: `pass after task closure; the next ready execution unit resolves to task 2 (Shared policy alignment)`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `pass after closing nested checklist items 1.1 and 1.2 while task 1 remained active; completion_handoff.decision = stay_in_progress, next_ready_task_ids = ['2'], and remaining_open_task_ids = ['2', '3']`
  - Run: `python3 - <<'PY' ...`
  - Result: `pass; direct harness re-ran 4 targeted task-1 checks covering preserved normal precedence, missing OpenSpec Change metadata rejection, do-not-route-around malformed active work, and missing active change directory rejection.`
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `OK: workflow audit passed for docs/planning/versions/v1`
  - Run: `git diff --check`
  - Result: `pass`
  - Review: `Focused local task review found no correctness, regression, or scope-drift issues in the task-1 diff.`
  - Inspection: `git diff -- skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py skills/_workflow/tests/test_workflow_scripts.py docs/planning/versions/v1/features/v1-f005-harden-autonomous-backlog-loop-eligibility.md openspec/changes/harden-autonomous-backlog-loop-eligibility/tasks.md openspec/changes/harden-autonomous-backlog-loop-eligibility/implementation-plans/1.md`
  - Result: `reviewed locally; task-scoped changes stay within eligibility validation, fixture support, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`
- `2026-03-27` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass before promoting the feature to [READY] and pass after moving the feature to [READY]`
  - Inspection: `openspec/changes/harden-autonomous-backlog-loop-eligibility/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/task-execution-handoff/spec.md`, and `openspec/specs/workflow-audit-and-repair/spec.md` are present; top-level OpenSpec task \`1\` resolves to workflow status \`ready\` because it is unchecked, \`Current Task\` is \`none\`, and tasks \`2\` and \`3\` are gated by workflow \`Depends On\` prerequisites.`
  - Run: `openspec validate harden-autonomous-backlog-loop-eligibility --type change --json --no-interactive`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `1`. `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py` now blocks active `[READY]` and `[IN_PROGRESS]` features that are missing `OpenSpec Change` metadata, link to a missing active change directory, or carry workflow-derived readiness drift before returning `run_task_loop`. The next start-task resolution now points to task `2` (`Shared policy alignment`), and task `3` remains `todo` until task `2` is done.
- `2026-03-27`: Shaping completed. Linked OpenSpec tasks now use top-level executable task IDs, and task `1` is ready for execution.
- `2026-03-27`: Started task `1` in the feature worktree using the linked implementation plan at `openspec/changes/harden-autonomous-backlog-loop-eligibility/implementation-plans/1.md`.

# Feature: Align Workflow Contract And Templates

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f012`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `v1-f012-align-workflow-contract-and-templates`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/feature-execution-tracking/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-27`
- Last Updated: `2026-03-27`

## 1. Validation Log
- `2026-03-27` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass before promoting the feature to [READY]`
  - Run: `openspec validate v1-f012-align-workflow-contract-and-templates --type change --json --no-interactive`
  - Result: `pass; summary totals report 1 passed and 0 failed`
  - Inspection: `openspec/changes/v1-f012-align-workflow-contract-and-templates/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/task-execution-handoff/spec.md`, and `openspec/specs/feature-execution-tracking/spec.md` are present`
  - Run: `python3` `skills._workflow.workflow_state.parse_tasks(...)` over `docs/planning/versions/v1/features/v1-f012-align-workflow-contract-and-templates.md`
  - Result: `top-level OpenSpec task 1 resolves to workflow status ready, while tasks 2 and 3 remain todo behind declared dependencies`
- `2026-03-27` Task `1`:
  - Run: `bin/run-python.sh -m unittest tests.test_workflow_contract_docs -v`
  - Result: `3 tests passed, covering the finish-feature entrypoint wording, autonomous-loop finish-feature routing, and the stable autonomous handoff requirement`
  - Run: `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass after the task-scoped wording/spec updates and task-state bookkeeping`
  - Run: `python` one-off using `skills._workflow.workflow_state.compute_completion_handoff(...)` for completed task `1`
  - Result: `pass; completion_handoff reports decision stay_in_progress with next_ready_task_ids ['2'] and all_top_level_tasks_complete=False`
  - Inspection: `git diff -- skills/finish-feature/SKILL.md skills/autonomous-backlog-loop/SKILL.md openspec/specs/task-execution-handoff/spec.md tests/test_workflow_contract_docs.py docs/planning/versions/v1/features/v1-f012-align-workflow-contract-and-templates.md openspec/changes/v1-f012-align-workflow-contract-and-templates/tasks.md openspec/changes/v1-f012-align-workflow-contract-and-templates/implementation-plans/1.md`
  - Result: `reviewed locally; task-scoped changes are limited to finish-feature/autonomous-loop wording alignment, the stable handoff contract update, focused contract coverage, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `dirty`
  - Notes: Started task `1` in feature worktree `v1-f012-align-workflow-contract-and-templates` after writing `openspec/changes/v1-f012-align-workflow-contract-and-templates/implementation-plans/1.md`. Execution is scoped to aligning `finish-feature` and autonomous-loop wording with the accepted `[IN_PROGRESS]` handoff gate before downstream cleanup.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `1`. `finish-feature` now advertises the accepted `[IN_PROGRESS]` entrypoint, autonomous orchestration now routes final-task completion through `finish-feature` before cleanup, and task `2` is the next ready execution target while the feature remains `[IN_PROGRESS]`.

# Feature: Align Workflow Contract And Templates

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f012`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
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

## 2. Handoff Notes
- None yet.

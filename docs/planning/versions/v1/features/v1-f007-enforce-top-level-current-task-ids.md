# Feature: Enforce Top-Level Current Task IDs

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f007`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
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
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `enforce-top-level-current-task-ids`. Top-level OpenSpec tasks `1`, `2`, and `3` are ready to execute, so the feature can move to `[READY]`.

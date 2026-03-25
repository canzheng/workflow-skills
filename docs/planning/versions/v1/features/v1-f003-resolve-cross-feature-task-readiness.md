# Feature: Resolve Cross-Feature Task Readiness

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f003`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
- OpenSpec Change: `fix-cross-feature-openspec-task-readiness`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/workflow-audit-and-repair/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-25`
- Last Updated: `2026-03-26`

## 1. Validation Log
- `2026-03-26` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass before and after promoting the feature to [READY]`
  - Inspection: `openspec/changes/fix-cross-feature-openspec-task-readiness/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/task-execution-handoff/spec.md`, and `openspec/specs/workflow-audit-and-repair/spec.md` all present; `tasks.md` now exposes executable top-level checklist entries, and top-level task `1` is `ready` because it is unchecked, `Current Task` is `none`, and no workflow dependency blocks are present.
  - Run: `openspec validate fix-cross-feature-openspec-task-readiness --type change --json --no-interactive`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-26`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `fix-cross-feature-openspec-task-readiness`. Top-level OpenSpec task `1` is ready to execute, so the feature can move to `[READY]`.

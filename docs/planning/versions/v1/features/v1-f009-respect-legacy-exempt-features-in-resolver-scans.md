# Feature: Respect Legacy-Exempt Features in Resolver Scans

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f009`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#ready`
- OpenSpec Change: `handle-legacy-exempt-resolver-scan`
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
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass before promoting the feature to [READY] and pass after moving the feature to [READY]`
  - Inspection: `openspec/changes/handle-legacy-exempt-resolver-scan/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/task-execution-handoff/spec.md`, and `openspec/specs/feature-execution-tracking/spec.md` are present; top-level OpenSpec tasks \`1\` and \`2\` both resolve to workflow status \`ready\` because they are unchecked, \`Current Task\` is \`none\`, and no workflow dependency blocks are present.`
  - Run: `openspec validate handle-legacy-exempt-resolver-scan --type change --json --no-interactive`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `handle-legacy-exempt-resolver-scan`. Top-level OpenSpec tasks `1` and `2` are ready to execute, so the feature can move to `[READY]`.

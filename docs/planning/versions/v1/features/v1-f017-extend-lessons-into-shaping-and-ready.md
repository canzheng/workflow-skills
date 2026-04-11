# Feature: Extend Lessons Into Shaping And Ready

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f017`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#shaping`
- OpenSpec Change: `extend-lessons-into-shaping-and-ready`
- OpenSpec Specs:
  - `openspec/specs/openspec-change-integration/spec.md`
  - `openspec/specs/feature-execution-tracking/spec.md`
  - `openspec/specs/task-execution-handoff/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
  - This field is the active execution marker for the implemented workflow; OpenSpec `tasks.md` remains the checked/unchecked task ledger.
- Created: `2026-04-11`
- Last Updated: `2026-04-11`

## 1. Validation Log
- `2026-04-11` Task `shape`:
  - Run: `rtk openspec validate extend-lessons-into-shaping-and-ready --type change --json --no-interactive`
  - Result: `pass`
  - Evidence: `schema`

## 2. Handoff Notes
- `2026-04-11`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are now present for `extend-lessons-into-shaping-and-ready`. The feature is linked to an active OpenSpec change and remains in `[SHAPING]` until readiness work decides whether the planning-stage lesson lifecycle is specified clearly enough for promotion.
  - Proof Obligations: `The workflow should retrieve, apply, record, and capture lessons during `shaping` and `ready` without introducing a separate planning-only lesson system or weakening the existing execution-stage lesson lifecycle.`

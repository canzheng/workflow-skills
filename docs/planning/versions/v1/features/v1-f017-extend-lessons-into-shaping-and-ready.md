# Feature: Extend Lessons Into Shaping And Ready

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f017`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
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
- `2026-04-11` Readiness review:
  - Run: independent `gpt-5.4-mini` review of `proposal.md`, `design.md`, `tasks.md`, linked specs, `WORKFLOW_REFERENCE.md`, and `skills/ready-feature/SKILL.md`
  - Result: `pass`
  - Evidence: `contract_surface`
- `2026-04-11` Task `1`:
  - Run: `rtk python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass`
  - Evidence: `artifact_inspection`
- `2026-04-11` Task `1`:
  - Run: `rtk git diff --check`
  - Result: `pass`
  - Evidence: `manual_inspection`
- `2026-04-11` Task `2`:
  - Run: `rtk python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass`
  - Evidence: `artifact_inspection`
- `2026-04-11` Task `2`:
  - Run: `rtk git diff --check`
  - Result: `pass`
  - Evidence: `manual_inspection`

## 2. Handoff Notes
- `2026-04-11` Task `2`:
  - Current Task: `none`
  - Worktree State: `dirty`
  - Retrieved Lesson IDs: `none`
  - Notes: Task `2` is complete in the feature worktree; the planning-stage workflow skills now describe the same lesson lifecycle as the planning docs.
  - Proof Obligations: `The planning-stage lesson lifecycle is now explicit in the workflow skills without splitting into a separate planning-only lesson system.`
- `2026-04-11` Task `2`:
  - Current Task: `2`
  - Worktree State: `dirty`
  - Retrieved Lesson IDs: `none`
  - Notes: Starting task `2` in the feature worktree; the planning-stage workflow skills will be updated to retrieve lessons before stage decisions and to keep finish-stage lesson handling coherent.
  - Proof Obligations: `The workflow skills must retrieve, apply, record, and capture lessons during shaping and readiness without creating a separate planning-only lesson system or weakening execution-stage lesson handling.`
- `2026-04-11` Task `1`:
  - Current Task: `none`
  - Worktree State: `dirty`
  - Retrieved Lesson IDs: `none`
  - Notes: Task `1` is complete in the feature worktree; the OpenSpec task ledger and workflow docs now reflect the canonical planning-stage lesson handoff lines.
  - Proof Obligations: `The workflow reference and feature template now make planning-stage lesson retrieval, usage reconciliation, and capture explicit without introducing a separate planning-only lesson system.`
- `2026-04-11` Task `1`:
  - Current Task: `1`
  - Worktree State: `dirty`
  - Retrieved Lesson IDs: `none`
  - Notes: Task `1` execution started in the feature worktree; updating the workflow reference and feature template to make planning-stage lesson handoffs canonical.
  - Proof Obligations: `Canonicalize planning-stage lesson retrieval, usage reconciliation, capture, and feature-file handoff lines without creating a separate planning-only lesson system.`
- `2026-04-11` Task `1`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Retrieved Lesson IDs: `none`
  - Notes: Preparing the implementation plan for task `1`; no active lessons were returned for this task boundary.
  - Proof Obligations: `Update the workflow reference and feature-template guidance so planning-stage lesson retrieval, usage reconciliation, and capture are canonicalized in the docs and feature-file handoff notes.`
- `2026-04-11`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are now present for `extend-lessons-into-shaping-and-ready`. The feature is linked to an active OpenSpec change and remains in `[SHAPING]` until readiness work decides whether the planning-stage lesson lifecycle is specified clearly enough for promotion.
  - Proof Obligations: `The workflow should retrieve, apply, record, and capture lessons during `shaping` and `ready` without introducing a separate planning-only lesson system or weakening the existing execution-stage lesson lifecycle.`
- `2026-04-11`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Readiness review passed. The shaping artifacts define enough contract surface for `start-task` to draft against safely, and the feature can move to `[READY]`.

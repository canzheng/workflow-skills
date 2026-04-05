# Feature: <title>

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f001`
- Version: `v1`
- Backlog Reference: `<link or anchor>`
- OpenSpec Change: `<change-id>`
- OpenSpec Specs:
  - `openspec/specs/<capability>/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
  - This field is the active execution marker for the implemented workflow; OpenSpec `tasks.md` remains the checked/unchecked task ledger.
- Created: `YYYY-MM-DD`
- Last Updated: `YYYY-MM-DD`

## 1. Validation Log
- Treat this section as the running execution evidence ledger for the active task. Add entries as planned validation steps complete; do not wait until task closure to write all evidence at once.
- `<YYYY-MM-DD>` Task `<task-id>`:
  - Run: `<command or inspection step>`
  - Result: `<pass/fail and notable details>`
  - Evidence: `<comma-separated validation categories such as schema, runtime_path, artifact_repair, prompt_contract, orchestration, negative_case>`

## 2. Handoff Notes
- `<YYYY-MM-DD>`:
  - Current Task: `<task-id like 1 or none>`
  - Worktree State: `<clean/dirty>`
  - Notes: <handoff summary>
  - Proof Obligations: `<short note about the active task's proof-obligation surface when relevant>`

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
  - Review Scope: `<ready | task_readiness | task_execution | task_completion | feature_finish | remediation_code | record_integrity>`
  - Review Target: `<feature-id | top-level-task-id>`
  - Review Verdict: `<approved | changes_requested | blocked>`  # exactly these; `_remediation_gap` branches on the spelling
  - Blocking Findings: `<none or comma-separated stable finding ids or labels>`
  - Review Terminal: `<true | false>`
  - Notes: <handoff summary>
  - Proof Obligations: `<short note about the active task's proof-obligation surface when relevant>`

## 3. Task Completion Ledger
- `complete-task` appends one line here when it closes a task, as its final act. This is the
  workflow's only UNCONDITIONAL provenance record: `done` is derived from a checkbox in `tasks.md`,
  so without a line here a hand-checked box is indistinguishable from a fully gated close.
  `audit-workflow` requires one line per done task on every open feature.
- The line is written by `complete-task/scripts/write_completion_ledger.py` and by nothing else. It
  carries a `plan-sha256` and a `head` commit that `audit-workflow` RE-VERIFIES, so a hand-typed line
  is reported rather than accepted. Do not edit these lines; do not write one for a task that is not
  yet `done`, which would pre-approve a close that has not happened.
- Shape (produced by the script, not typed):
  `- Task `4` completed `2026-08-06` plan-sha256 `fe324224cd13e0be` head `1c6318818fbf``

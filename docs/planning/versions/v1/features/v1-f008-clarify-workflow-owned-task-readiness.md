# Feature: Clarify Workflow-Owned Task Readiness

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f008`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `clarify-workflow-task-readiness-convention`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/workflow-audit-and-repair/spec.md`
  - `openspec/specs/openspec-change-integration/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-26`
- Last Updated: `2026-03-26`

## 1. Validation Log
- `2026-03-26` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass`
  - Run: `openspec validate clarify-workflow-task-readiness-convention --type change --json --no-interactive`
  - Result: `pass`
  - Inspection: `openspec/changes/clarify-workflow-task-readiness-convention/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, `openspec/specs/task-execution-handoff/spec.md`, `openspec/specs/workflow-audit-and-repair/spec.md`, and `openspec/specs/openspec-change-integration/spec.md` all present; top-level task \`1\` is \`ready\` because it is unchecked, \`Current Task\` is \`none\`, and no workflow dependency blocks are present.
- `2026-03-26` Task `1`:
  - Run: `python3 -m pytest skills/_workflow/tests/test_workflow_scripts.py -q`
  - Result: `Could not run in this environment because the pytest module is unavailable under python3.`
  - Run: `python3` one-off fixture that invokes `skills/start-task/scripts/resolve_start_task.py --repo-root <temp-repo>`
  - Result: `Passed; the resolver exits 1 and reports "workflow-derived task readiness drift detected" when a feature has a promotable task still left in \`todo\`.`
  - Run: `openspec validate clarify-workflow-task-readiness-convention --type change --json --no-interactive`
  - Result: `Passed with 1 change item, 1 passed, 0 failed.`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `Passed for docs/planning/versions/v1 before task-state closure and after task-state closure.`
  - Run: `git diff --check`
  - Result: `Passed with no patch-format issues.`
  - Inspection: `rg -n "/Users/canzheng|/Users/|/home/" ...`
  - Result: `No local absolute path leakage found in the tracked task changes.`

## 2. Handoff Notes
- `2026-03-26`:
  - Current Task: `1`
  - Worktree State: `feature branch v1-f008-clarify-workflow-owned-task-readiness created for task execution`
  - Notes: Started task `1` for `clarify-workflow-task-readiness-convention` and moved the feature into `[IN_PROGRESS]`.
- `2026-03-26`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Task `1` completed. The completion handoff resolves to `stay_in_progress`, and top-level tasks `2` and `3` are both ready for the next execution decision on this feature branch.

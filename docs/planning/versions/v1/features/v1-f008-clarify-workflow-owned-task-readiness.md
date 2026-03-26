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
- `2026-03-26` Task `2`:
  - Run: `python3` one-off assertions for `find_openspec_task_structure_errors(...)`
  - Result: `Passed; nested-only task structures report missing parent top-level task IDs, while valid parent-task structures produce no errors.`
  - Run: `python3 -m unittest tests.test_workflow_openspec_integration -v`
  - Result: `Passed; 15 integration tests green, including malformed nested-only task rejection for both [SHAPING] and [READY] features.`
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `Passed for docs/planning/versions/v1 after shared task-structure validation was added to the workflow audit.`
  - Run: `git diff --check`
  - Result: `Passed with no patch-format issues.`
- `2026-03-26` Task `3`:
  - Run: `python3` repo scan over active `openspec/changes/**/tasks.md` using `find_openspec_task_structure_errors(...)`
  - Result: `Passed; no active tracked OpenSpec change task file violates the parent top-level executable task structure contract.`
  - Run: `python3 -m unittest tests.test_workflow_openspec_integration -v`
  - Result: `Passed; 16 integration tests green, including malformed nested-only rejection coverage plus a regression that active tracked change task files keep the required parent-task structure.`
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `Passed for docs/planning/versions/v1 with task 3 in progress and after task-3 implementation verification.`
  - Run: `git diff --check`
  - Result: `Passed with no patch-format issues.`
  - Review: `gpt-5.4-mini` code-review subagent on the task-3 diff
  - Result: `One medium issue found: the new regression initially scanned archived changes too. Fixed by excluding \`openspec/changes/archive/\` from the active-change fixture sweep; no remaining findings after re-verification.`

## 2. Handoff Notes
- `2026-03-26`:
  - Current Task: `1`
  - Worktree State: `feature branch v1-f008-clarify-workflow-owned-task-readiness created for task execution`
  - Notes: Started task `1` for `clarify-workflow-task-readiness-convention` and moved the feature into `[IN_PROGRESS]`.
- `2026-03-26`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Task `1` completed. The completion handoff resolves to `stay_in_progress`, and top-level tasks `2` and `3` are both ready for the next execution decision on this feature branch.
- `2026-03-26`:
  - Current Task: `2`
  - Worktree State: `dirty`
  - Notes: Task `2` started in the existing feature worktree `../worktrees/workflow-skills/v1-f008-clarify-workflow-owned-task-readiness`. The execution focus is rejecting malformed linked `tasks.md` files that use nested checklist items without a parent top-level executable task and surfacing that validation through workflow readiness checks.
- `2026-03-26`:
  - Current Task: `none`
  - Worktree State: `dirty`
  - Notes: Task `2` completed. Shared workflow validation now rejects nested-only OpenSpec task structures, audit blocks malformed [SHAPING] and [READY] features, and the completion handoff resolves to `stay_in_progress` with task `3` as the next ready execution unit.
- `2026-03-26`:
  - Current Task: `3`
  - Worktree State: `dirty`
  - Notes: Task `3` started in the existing feature worktree `../worktrees/workflow-skills/v1-f008-clarify-workflow-owned-task-readiness`. The execution focus is repairing valid workflow fixtures and sample task files so they use explicit top-level executable tasks while preserving malformed nested-only cases only for rejection coverage.
- `2026-03-26`:
  - Current Task: `none`
  - Worktree State: `dirty`
  - Notes: Task `3` completed. Active tracked OpenSpec change task files now have explicit parent top-level executable tasks, malformed nested-only fixtures remain only as rejection coverage, and the completion handoff resolves to `confirm_feature_acceptance`, so `finish-feature` is the next workflow step.

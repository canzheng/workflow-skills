# Feature: Respect Legacy-Exempt Features in Resolver Scans

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f009`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
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
- `2026-03-27` Task `1`:
  - Run: `python3 -m unittest tests.test_workflow_openspec_integration.WorkflowOpenSpecIntegrationTests.test_complete_task_resolves_active_task_with_linked_openspec_context tests.test_workflow_openspec_integration.WorkflowOpenSpecIntegrationTests.test_complete_task_reports_in_progress_handoff_when_more_work_remains -v`
  - Result: `pass`
  - Run: `python3 skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass with the feature in [IN_PROGRESS] and task 1 active`
  - Run: `python3` one-off temp repo harness invoking `skills/complete-task/scripts/resolve_complete_task.py --repo-root <temp-repo>` with one active feature plus one `[DONE]` `legacy-exempt` historical feature missing `OpenSpec Change`
  - Result: `pass; resolver returns the active task payload instead of failing on the historical completed feature`
  - Run: `python3` one-off temp repo harness invoking `skills/complete-task/scripts/resolve_complete_task.py --repo-root <temp-repo>` with an active feature missing `OpenSpec Change`
  - Result: `pass; resolver still exits 1 with "...is missing OpenSpec Change metadata" for invalid active state`
  - Run: `python3 skills/complete-task/scripts/resolve_complete_task.py`
  - Result: `pass after closing nested items 1.1 and 1.2; completion handoff reports decision stay_in_progress with next_ready_task_ids ['2']`
  - Inspection: `git diff -- skills/complete-task/scripts/resolve_complete_task.py docs/planning/versions/v1/BACKLOG.md docs/planning/versions/v1/features/v1-f009-respect-legacy-exempt-features-in-resolver-scans.md openspec/changes/handle-legacy-exempt-resolver-scan/implementation-plans/1.md openspec/changes/handle-legacy-exempt-resolver-scan/tasks.md`
  - Result: `reviewed locally; no blocking issues found in the task-scoped diff`
  - Run: `git diff --check`
  - Result: `pass`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `handle-legacy-exempt-resolver-scan`. Top-level OpenSpec tasks `1` and `2` are ready to execute, so the feature can move to `[READY]`.
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `dirty`
  - Notes: Started task `1` in feature worktree `v1-f009-legacy-exempt-resolver-scan` after writing `openspec/changes/handle-legacy-exempt-resolver-scan/implementation-plans/1.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `clean`
  - Notes: Completed task `1`. `skills/complete-task/scripts/resolve_complete_task.py` now ignores unrelated `[DONE]` `legacy-exempt` features during active-task resolution while preserving strict active-state linkage failures. Feature remains `[IN_PROGRESS]`; next ready task is `2` (`Regression Coverage`).

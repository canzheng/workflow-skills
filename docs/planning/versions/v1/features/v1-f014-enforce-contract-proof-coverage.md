# Feature: Enforce Contract-Proof Coverage

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f014`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `v1-f014-enforce-contract-proof-coverage`
- OpenSpec Specs:
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/feature-execution-tracking/spec.md`
  - `openspec/specs/openspec-change-integration/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
  - This field is the active execution marker for the implemented workflow; OpenSpec `tasks.md` remains the checked/unchecked task ledger.
- Created: `2026-04-05`
- Last Updated: `2026-04-05`

## 1. Validation Log
- `2026-04-05` Readiness Review:
  - Run: `rtk openspec validate v1-f014-enforce-contract-proof-coverage --type change --json --no-interactive`
  - Result: `pass; summary.totals.passed = 1 and summary.totals.failed = 0`
  - Inspection: `openspec/changes/v1-f014-enforce-contract-proof-coverage/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, and the linked stable spec paths are present for the new feature.`
  - Inspection: `openspec/changes/v1-f014-enforce-contract-proof-coverage/tasks.md`
  - Result: `top-level task 1 is immediately startable; task 2 remains blocked on task 1.`
- `2026-04-05` Task `1`:
  - Run: `rtk bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_state.py skills/_workflow/tests/test_workflow_scripts.py tests/test_workflow_openspec_integration.py -q -k 'implementation_plan or start_task or complete_task or selects_cross_feature_ready_task'`
  - Result: `24 passed, 65 deselected in 2.37s`
  - Run: `rtk bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_state.py skills/_workflow/tests/test_workflow_scripts.py tests/test_workflow_openspec_integration.py -q`
  - Result: `89 passed in 5.37s`
  - Run: `rtk bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass with the feature in [IN_PROGRESS] and task 1 active, then pass again after task-1 completion bookkeeping`
  - Run: `rtk python3 skills/complete-task/scripts/resolve_complete_task.py --repo-root .`
  - Result: `pass; completion_handoff.decision = stay_in_progress, next_ready_task_ids = ['2'], and remaining_open_task_ids = ['2']`
  - Run: `rtk git diff --check`
  - Result: `pass`
  - Review: `Focused local review found the diff stayed within the task-1 scope: shared implementation-plan validation, resolver gate wiring, and fixture/test updates for the stronger contract.`
- `2026-04-05` Task `2`:
  - Run: `rtk bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
  - Result: `pass; workflow audit passed for docs/planning/versions/v1`
  - Run: `rtk git diff --check`
  - Result: `pass`
  - Run: `rtk rg -n "proof obligation|proof obligations|validation taxonomy|Current Task|Evidence:" skills docs/planning -g '*.md'`
  - Result: `pass; matched the updated guidance in shape-backlog-item, ready-feature, start-task, complete-task, docs/planning/WORKFLOW_REFERENCE.md, and docs/planning/template/feature-template.md`

## 2. Handoff Notes
- `2026-04-05`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Feature `v1-f014` was created to harden workflow validation against surrogate lower-level contracts. Task `1` is ready to execute once the feature worktree is created.
- `2026-04-05`:
  - Current Task: `1`
  - Worktree State: `clean feature worktree at ../worktrees/workflow-skills/v1-f014-enforce-contract-proof-coverage on branch v1-f014-enforce-contract-proof-coverage`
  - Notes: Started task `1` after writing `openspec/changes/v1-f014-enforce-contract-proof-coverage/implementation-plans/1.md` and confirming with `resolve_start_task.py` that the task is the next ready execution unit.
- `2026-04-05`:
  - Current Task: `none`
  - Worktree State: `task-1 changes ready to commit on branch v1-f014-enforce-contract-proof-coverage in ../worktrees/workflow-skills/v1-f014-enforce-contract-proof-coverage`
  - Notes: Completed task `1`. The workflow now validates implementation-plan proof structure through shared helpers used by both start and completion resolvers, stale cross-feature fixtures now carry compliant plans, and task `2` is the next ready execution unit while the feature remains `[IN_PROGRESS]`.
- `2026-04-05`:
  - Current Task: `2`
  - Worktree State: `dirty feature worktree on branch v1-f014-enforce-contract-proof-coverage in ../worktrees/workflow-skills/v1-f014-enforce-contract-proof-coverage`
  - Notes: Started task `2` after writing `openspec/changes/v1-f014-enforce-contract-proof-coverage/implementation-plans/2.md`. Execution is scoped to aligning shaping, readiness, task guidance, and the workflow reference around explicit proof obligations and the shared validation taxonomy.
- `2026-04-05`:
  - Current Task: `none`
  - Worktree State: `dirty feature worktree on branch v1-f014-enforce-contract-proof-coverage in ../worktrees/workflow-skills/v1-f014-enforce-contract-proof-coverage`
  - Notes: Completed task `2`. Shaping, readiness, task start, task completion, the feature template, and the workflow reference now describe the shared proof-obligation / validation-taxonomy contract; task `3` is the next ready execution unit while the feature remains `[IN_PROGRESS]`.

## Why

Workflow execution currently proves that a task has *some* implementation plan and *some* validation evidence, but it does not force those artifacts to describe the same contract surface that shaping approved. That gap lets helper-only tests, file-presence checks, and narrower local schemas become surrogate acceptance bars for broader shaped behavior.

## What Changes

- Require task-scoped implementation plans to declare contract surface, proof obligations, required validation classes, and any unit-only justification before execution starts.
- Tighten task start and completion workflow gates so they reject implementation plans that do not expose those proof obligations explicitly.
- Align workflow shaping and readiness guidance so promoted work captures proof obligations early enough to prevent lower-level tests from silently redefining acceptance.
- Add focused regression coverage for implementation-plan validation and update fixture plans that currently encode the older weaker contract.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `task-execution-handoff`: task start and completion now require implementation plans that make proof obligations and validation classes explicit.
- `feature-execution-tracking`: task evidence guidance now records validation against explicit proof obligations rather than treating any narrow validation log as sufficient by default.
- `openspec-change-integration`: shaping and readiness now require linked OpenSpec work to expose proof obligations and intended validation coverage for executable tasks.

## Impact

- Affected code: `skills/_workflow/workflow_state.py`, `skills/start-task/scripts/resolve_start_task.py`, `skills/complete-task/scripts/resolve_complete_task.py`, and workflow-skill documentation for shaping, readiness, task start, and task completion.
- Affected tests: workflow-state tests, resolver/integration tests, and any fixture helper that writes implementation plans.
- Affected process: new workflow-managed tasks must author richer implementation plans before execution can begin.

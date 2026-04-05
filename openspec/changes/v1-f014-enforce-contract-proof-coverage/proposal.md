## Why

Workflow execution currently proves that a task has *some* implementation plan and *some* validation evidence, but it does not force those artifacts to describe the same contract surface that shaping approved. That gap lets helper-only tests, file-presence checks, and narrower local schemas become surrogate acceptance bars for broader shaped behavior.

## What Changes

- Require task-scoped implementation plans to declare contract surface, proof obligations, required validation classes, and any unit-only justification before execution starts.
- Tighten task start workflow gates so they reject anti-surrogate validation plans such as helper-only proof for orchestration behavior, file-presence proof for structured assets, bookkeeping-only proof for repair behavior, and isolated helper proof without real execution-path coverage.
- Tighten readiness guidance so a feature cannot become `[READY]` unless at least one startable task has proof planning aligned to the shaped contract, not only dependency-derived readiness.
- Tighten completion workflow gates so task closure reconciles proof obligations to categorized evidence rather than accepting any narrow validation log as sufficient by default.
- Add a workflow review question for test changes that asks whether new or modified tests narrow the contract relative to the shaped task plan.
- Update workflow reference and skill guidance to define a validation taxonomy and prefer canonical end-to-end fixtures over minimized local fixtures when contract behavior is at stake.
- Add focused regression coverage for implementation-plan validation, evidence reconciliation, review guidance, and fixture strategy so stale tests do not normalize the weaker contract again.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `task-execution-handoff`: task start and completion now require implementation plans that make proof obligations and validation classes explicit, reject anti-surrogate proof patterns for behavioral work, and reconcile completion against categorized evidence.
- `feature-execution-tracking`: task evidence guidance now records categorized validation against explicit proof obligations rather than treating any narrow validation log as sufficient by default.
- `openspec-change-integration`: shaping and readiness now require linked OpenSpec work to expose proof obligations and intended validation coverage for executable tasks before those tasks become ready.

## Impact

- Affected code: `skills/_workflow/workflow_state.py`, `skills/start-task/scripts/resolve_start_task.py`, `skills/complete-task/scripts/resolve_complete_task.py`, workflow feature templates, and workflow-skill documentation for shaping, readiness, task start, and task completion.
- Affected tests: workflow-state tests, resolver/integration tests, fixture helpers that write implementation plans or evidence, and review/process coverage for test-contract narrowing.
- Affected process: new workflow-managed tasks must author richer proof plans before execution, record categorized evidence at completion, and review test changes against the shaped contract instead of only the implementation.

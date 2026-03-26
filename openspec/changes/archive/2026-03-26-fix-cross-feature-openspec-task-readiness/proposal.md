## Why

OpenSpec-backed task readiness currently disagrees across parser, drift, and task-selection paths when a task depends on another feature's task. That leaves valid work stuck as `todo` or unresolved, especially once upstream work has been archived.

## What Changes

- Make cross-feature task dependencies resolve consistently for OpenSpec-backed tasks.
- Teach dependency resolution to follow completed features through archived OpenSpec changes, not only active change directories.
- Align `parse_tasks()`, readiness drift checks, and task-selection callers so they all compute the same executable task state.
- Add regression coverage for cross-feature dependencies in both active and archived upstream-feature scenarios.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Task selection and execution readiness will support cross-feature task dependencies consistently.
- `workflow-audit-and-repair`: Readiness validation will treat resolvable cross-feature dependencies as valid instead of permanent drift.

## Impact

- Affected helpers: `skills/_workflow/workflow_state.py`
- Affected resolvers: `skills/start-task/scripts/resolve_start_task.py`
- Affected automation: `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py`
- Affected tests: `skills/_workflow/tests/test_workflow_state.py`, `skills/_workflow/tests/test_workflow_scripts.py`, `tests/test_workflow_openspec_integration.py`

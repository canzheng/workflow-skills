## Why

The autonomous backlog loop can currently propose work from malformed workflow states that the normal wrappers would reject. That weakens the repo's own execution guarantees by letting automation skip readiness drift and OpenSpec linkage checks.

## What Changes

- Make autonomous action resolution enforce the same basic eligibility rules used by the manual workflow wrappers.
- Reject or skip features that are missing required OpenSpec linkage, missing ready tasks, or carrying readiness drift.
- Preserve autonomous shaping behavior for clean `[BACKLOG]` and `[SHAPING]` items.
- Add fixture coverage for invalid ready features and repaired states.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Automated task selection will honor the same execution eligibility rules as manual task start.
- `workflow-audit-and-repair`: Autonomous orchestration will not bypass readiness drift and linkage validation.

## Impact

- Affected automation: `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py`
- Affected helpers: `skills/_workflow/workflow_state.py`
- Affected tests: `skills/_workflow/tests/test_workflow_scripts.py`

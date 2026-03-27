## Why

The workflow contract says `Current Task` must reference a top-level OpenSpec task ID, but the current parser accepts any backticked value. That leaves malformed values like `1.1` undocumentedly tolerated instead of being rejected as invalid workflow state.

## What Changes

- Enforce that `Current Task` is either `none` or a top-level OpenSpec task ID.
- Make audit and diagnosis report invalid `Current Task` values clearly.
- Add fixture coverage for valid top-level IDs and invalid subtask IDs.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `feature-execution-tracking`: `Current Task` metadata will be restricted to top-level task IDs.
- `workflow-audit-and-repair`: Audit and diagnosis will treat subtask-style `Current Task` values as invalid workflow state.

## Impact

- Affected helpers: `skills/_workflow/workflow_state.py`
- Affected scripts: `skills/audit-workflow/scripts/audit_workflow.py`, `skills/diagnose-workflow/scripts/diagnose_workflow.py`
- Affected tests: workflow state and diagnosis fixtures

## Why

`complete-task` currently scans promoted feature files broadly and hard-fails when a historical `[DONE]` feature is marked `legacy-exempt` and therefore omits `OpenSpec Change`. That makes valid migrated workflow state block task completion even though audit and diagnosis already accept the same historical record.

## What Changes

- Make repository-wide resolver scans treat `[DONE]` features marked `OpenSpec Status: `legacy-exempt`` as historical records that do not require `OpenSpec Change` metadata.
- Update `complete-task` so it only requires linked OpenSpec change metadata for feature states and tasks that actually need change context.
- Add regression coverage for a repo state with one active task and one historical `legacy-exempt` completed feature missing `OpenSpec Change`.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Task-completion resolver scans will not fail on historical `legacy-exempt` completed features that are not part of the active execution path.
- `feature-execution-tracking`: Historical completed-feature exemptions will remain valid when repository-wide resolvers inspect promoted feature files.

## Impact

- Affected scripts: `skills/complete-task/scripts/resolve_complete_task.py`
- Affected helpers: `skills/_workflow/workflow_state.py` if shared legacy-exemption parsing is centralized
- Affected tests: `tests/test_workflow_openspec_integration.py`

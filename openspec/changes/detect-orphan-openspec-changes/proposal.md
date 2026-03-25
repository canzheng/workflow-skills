## Why

The workflow health checks currently report a clean state even when active OpenSpec changes are not represented on the board. That leaves a real planning-to-OpenSpec drift mode invisible to the tools that are supposed to explain and gate workflow integrity.

## What Changes

- Detect active OpenSpec changes that are not linked from any promoted feature.
- Report those orphaned changes in `diagnose-workflow` and fail `audit-workflow` when they represent active unarchived work.
- Clarify the workflow contract so active changes must map to a promoted feature or be archived.
- Add fixture coverage for orphaned active changes and the repaired linked-feature state.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `workflow-audit-and-repair`: Audit and diagnosis will validate that active changes are linked into workflow state.
- `workflow-board-lifecycle`: Promoted feature tracking will explicitly include the active-change linkage expectation.

## Impact

- Affected scripts: `skills/audit-workflow/scripts/audit_workflow.py`, `skills/diagnose-workflow/scripts/diagnose_workflow.py`
- Affected docs/specs: workflow audit and board lifecycle contracts
- Affected tests: `tests/test_diagnose_workflow.py`, `tests/test_workflow_openspec_integration.py`

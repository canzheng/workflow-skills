## Why

The workflow review found a cluster of source-of-truth drift issues that are individually small but collectively make the repo teach contradictory behavior. The highest-value fix is to align the documented workflow boundary around `finish-feature`, keep `design-mode` wording precise without changing its defendable validation behavior, and remove template/path-hygiene drift from the feature-file lane.

## What Changes

- Update `finish-feature` metadata and autonomous-loop workflow guidance so they explicitly preserve the `finish-feature` gate from `[IN_PROGRESS]` before any final cleanup.
- Clarify `design-mode` wording so it states that design-mode does not act on `[READY]` or `[IN_PROGRESS]` work, but still validates it for sanity.
- Make the tracked feature template the single source of truth and have the renderer read from it instead of maintaining a second inline template literal.
- Remove the machine-local absolute-path leakage from the historical feature record.
- Add narrow validation coverage for the template/render alignment and any wording-sensitive workflow behavior touched by the change.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Autonomous workflow guidance will explicitly route feature completion through `finish-feature` before downstream cleanup.
- `feature-execution-tracking`: Workflow-maintained feature-file templates and records will stay aligned with the documented `Current Task` contract and remain teammate-safe.

## Impact

- Affected skills/docs: `skills/autonomous-backlog-loop/`, `skills/finish-feature/`, `README.md`, `AGENTS-global-workflow.md`
- Affected helpers/templates: `skills/_workflow/feature_file.py`, `docs/planning/template/feature-template.md`
- Affected planning/history artifacts: `docs/planning/versions/v1/features/v1-f008-clarify-workflow-owned-task-readiness.md`

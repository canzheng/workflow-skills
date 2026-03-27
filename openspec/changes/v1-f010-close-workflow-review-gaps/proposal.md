## Why

The review surfaced workflow contract gaps in the repo's own source of truth: `audit-workflow` misses required checks, `diagnose-workflow` can report malformed states as healthy, and several workflow docs/artifacts disagree with the implemented process.

## What Changes

- Tighten `audit-workflow` so it enforces promoted-feature `OpenSpec Specs` linkage and rejects non-canonical backlog sections, including extra sections appended after `[DEFER]`.
- Extend `diagnose-workflow` so it surfaces the same structural workflow issues as read-only findings instead of returning a false healthy status.
- Align workflow documentation around `finish-feature` ownership of the `[IN_PROGRESS] -> [DONE]` transition.
- Repair incomplete or contradictory workflow source-of-truth artifacts identified in the review.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `workflow-audit-and-repair`: Audit and diagnosis will enforce/report canonical board structure and promoted-feature OpenSpec spec linkage more strictly.

## Impact

- Affected skills: `skills/audit-workflow/`, `skills/diagnose-workflow/`
- Affected helpers/tests: `skills/_workflow/`, `skills/_workflow/tests/`, `tests/`
- Affected docs/planning artifacts: `AGENTS-global-workflow.md`, `README.md`, `docs/planning/versions/v1/`

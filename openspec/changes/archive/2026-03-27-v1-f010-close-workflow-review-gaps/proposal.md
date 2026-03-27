## Why

The review surfaced multiple mismatches between the documented workflow contract, the implemented enforcement, and the repo's own planning/spec artifacts. The current repo can pass audit while still missing required promoted-feature metadata, and diagnosis can still report malformed states as healthy.

## What Changes

- Tighten `audit-workflow` so it enforces every structural rule implicated by the review:
  - promoted-feature `OpenSpec Specs` linkage
  - canonical backlog section order
  - rejection of extra backlog sections, including sections appended after `[DEFER]`
- Extend `diagnose-workflow` so the same malformed states are surfaced as structured findings rather than being reported as healthy.
- Explicitly cover the review's source-of-truth findings in tracked artifacts:
  - `finish-feature` wording drift across workflow docs
  - incomplete `VERSION_SCOPE.md` placeholders despite a fully completed board
  - placeholder stable-spec purpose text in `openspec-change-integration`
  - historical feature records whose notes currently contradict the accepted workflow
- Add validations that map directly back to each review finding so readiness and later task completion can prove full finding coverage.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `workflow-audit-and-repair`: Audit and diagnosis will enforce/report canonical board structure and promoted-feature OpenSpec spec linkage more strictly.

## Impact

- Affected skills: `skills/audit-workflow/`, `skills/diagnose-workflow/`
- Affected helpers/tests: `skills/_workflow/`, `skills/_workflow/tests/`, `tests/`
- Affected docs/planning artifacts: `AGENTS-global-workflow.md`, `README.md`, `docs/planning/versions/v1/`
- Affected stable source-of-truth docs: `openspec/specs/openspec-change-integration/spec.md`

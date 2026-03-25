## Why

The current audit assumes every promoted feature has an active OpenSpec change directory. That is wrong in two important cases:

- historical completed features from a repo that adopts OpenSpec midstream may never have had OpenSpec changes
- completed post-adoption features should point to archived changes, not active change directories

Without a migration-aware rule, midstream adoption either forces fake retrospective changes for already-completed work or breaks the audit after valid feature archive steps.

## What Changes

- Add an explicit legacy-completed exemption marker for historical `[DONE]` features that predate OpenSpec adoption.
- Change audit expectations for `[DONE]` features so post-adoption completed work is validated against archived OpenSpec change state instead of active change state.
- Keep active OpenSpec change requirements for `[SHAPING]`, `[READY]`, and `[IN_PROGRESS]`.
- Document the migration rule that baseline specs should describe current main-checkout behavior while planned but unimplemented work remains in backlog and roadmap artifacts.

## Capabilities

### Modified Capabilities
- `workflow-audit-and-repair`: Teach audit to distinguish active, archived, and legacy-exempt completed features.
- `workflow-board-lifecycle`: Clarify that completed migrated features may remain valid without a linked change only when explicitly marked as historical pre-OpenSpec work.
- `feature-execution-tracking`: Add an optional legacy exemption marker for historical completed features during midstream adoption.

## Impact

- Affected skills: `audit-workflow`, `repair-drift`, `finish-feature`
- Affected helpers/tests: workflow metadata parsing, audit checks, and integration tests
- Affected migration docs: managed workflow contract, README, and future migration guidance

## Context

The workflow already documents that historical `[DONE]` features may omit `OpenSpec Change` when they record `OpenSpec Status: `legacy-exempt``. Audit and diagnosis implement that rule, but `complete-task` still loops over every promoted feature file and raises on any missing `OpenSpec Change` before it even knows whether the feature is relevant to the active task.

## Goals / Non-Goals

**Goals:**
- Remove the false hard-failure for historical `legacy-exempt` completed features during task-completion resolution.
- Keep strict OpenSpec linkage requirements for active shaping and execution states.
- Add fixture coverage that reproduces the migrated-repo failure mode.

**Non-Goals:**
- Relax OpenSpec linkage requirements for active features.
- Redesign the `legacy-exempt` migration contract.
- Broaden this change into unrelated resolver cleanup.

## Decisions

### Decision: Defer change-link validation until the resolver reaches relevant active work
`complete-task` only needs linked change context for the feature that actually owns the `in_progress` task. Historical completed features can still be parsed for task state without demanding change metadata up front.

### Decision: Keep legacy-exempt tolerance section-aware
The exemption remains valid only for completed historical features. Active sections such as `[SHAPING]`, `[READY]`, and `[IN_PROGRESS]` must still fail if they lack required OpenSpec linkage.

### Decision: Cover the bug with an end-to-end integration fixture
The failure depends on a specific repository shape: an active task plus an unrelated completed historical feature. The regression test should model that exact state instead of only unit-testing helper behavior.

## Risks / Trade-offs

- [Resolver validation could become too permissive] -> Keep the exemption narrow and tie it to completed `legacy-exempt` features only.
- [Future broad-scan resolvers could drift again] -> Encode the migrated historical-feature case in integration coverage and reuse shared parsing helpers where practical.

## Migration Plan

1. Update `complete-task` resolver logic to tolerate completed `legacy-exempt` feature records during repository scans.
2. Keep active-state linkage checks intact for the feature that owns the active task.
3. Add regression coverage for the mixed active-plus-historical repository state.
4. Re-run the narrow workflow integration tests.

## Open Questions

- None.

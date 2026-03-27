## Context

The accepted workflow already has the right lifecycle boundary: tasks finish while the feature remains `[IN_PROGRESS]`, then `finish-feature` validates and archives the linked change before the board moves to `[DONE]`. The drift is in the surrounding source-of-truth material. One skill header still says `finish-feature` is for work that "has reached done," the autonomous-loop instructions still describe going straight from `complete-task` to final cleanup, and the feature-file template exists in two places that no longer render identical content.

There is also one tracked historical feature entry with a machine-local absolute path pattern. That is not a runtime bug, but it violates the repo's own teammate-safe path hygiene rules and should be repaired in the same pass.

## Goals / Non-Goals

**Goals:**
- Align workflow skill/docs wording with the already-accepted `finish-feature` gate.
- Clarify `design-mode` wording without changing the current sanity-check behavior.
- Single-source the feature-file template from the tracked template file.
- Remove the local-path leak from tracked historical documentation.

**Non-Goals:**
- Change the actual `finish-feature` resolver semantics.
- Relax the validation of `[READY]` or `[IN_PROGRESS]` work in design mode.
- Rewrite historical feature records beyond the targeted hygiene fix.

## Decisions

### Decision: Treat the current design-mode behavior as correct and tighten the wording
The user's direction is explicit: design mode should not act on `[READY]` or `[IN_PROGRESS]` work, but validating that those states are sane is still defendable. The fix here is the language, not the control flow.

### Decision: Make the tracked template file authoritative
The renderer should load the checked-in template file rather than keep a second literal copy. That keeps the human-facing template and generated feature files aligned by construction.

### Decision: Keep the workflow-gate wording anchored in task-execution handoff
The `finish-feature` boundary is fundamentally a handoff rule: after final task completion, orchestration must route through `finish-feature` before any downstream cleanup. The stable spec change should live there.

## Risks / Trade-offs

- [Doc-only changes can drift again] -> Make the template single-sourced and keep lifecycle wording changes tied to the stable spec.
- [Historical record repair could accidentally rewrite chronology] -> Limit the feature-file edit to the local-path leak and preserve the underlying evidence.
- [Wording changes can overreach into behavior changes] -> Keep design-mode semantics unchanged and only make the language precise.

## Migration Plan

1. Align the workflow wording in skills and source-of-truth docs.
2. Update the stable handoff/tracking specs where the contract needs to be explicit.
3. Make the renderer consume the tracked template file.
4. Repair the local-path leak and add narrow coverage.

## Open Questions

- None.

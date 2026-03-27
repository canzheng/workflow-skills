## Context

The current audit and diagnosis logic starts from the active backlog and feature files. That is useful for linked workflow state, but it misses active change directories that no promoted feature points to. The review surfaced an actual repo example of that drift mode, so this is no longer theoretical.

## Goals / Non-Goals

**Goals:**
- Make active unarchived changes visible to workflow diagnosis.
- Make audit fail when active changes are not linked to promoted features.
- Keep archived completed changes and legacy-exempt completed features valid.

**Non-Goals:**
- Infer missing board entries automatically.
- Change how archived completed features are represented.

## Decisions

### Decision: Enumerate active changes directly from `openspec/changes/`
The health checks should compare the set of active change directories against the set of change IDs linked from promoted features.

### Decision: Keep diagnosis advisory and audit gating
`diagnose-workflow` should report orphaned active changes as structured findings, while `audit-workflow` should fail on them as an invalid workflow state.

### Decision: Ignore archived directories when computing orphan drift
Archived changes are already validated through the completed-feature rules and should not be re-flagged as active drift.

## Risks / Trade-offs

- [Generated or experimental change drafts may now fail audit] -> Require teams to either link the change to a promoted feature or remove/archive the draft before running the workflow gate.
- [Mismatch logic could double-report issues] -> Normalize to change IDs and emit one finding per orphaned change.

## Migration Plan

1. Add active-change enumeration helpers.
2. Thread orphan-change detection into diagnosis and audit.
3. Add fixtures for the orphaned and repaired states.
4. Re-run narrow workflow tests.

## Open Questions

- None.

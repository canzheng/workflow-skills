## Context

The repo's current active state is healthy, but the review exposed an important difference between "passes on the happy path" and "holds up when the scaffold is malformed." `diagnose-workflow` currently records missing planning findings and then still calls into a helper that raises. Separately, the workflow contract now expects shaping to be anchored by authored `proposal.md`, `design.md`, and `tasks.md`, but audit only requires those files once a feature reaches `[READY]`.

This change should harden the validation contract without changing the user's position on deferred work. Deferred items do not need new validation here; the desired tightening is for promoted work in `[SHAPING]`, plus clearer archived-change semantics for `[DONE]` features.

## Goals / Non-Goals

**Goals:**
- Keep `diagnose-workflow` advisory while making it resilient to missing planning scaffold.
- Make `[SHAPING]` enforce the baseline OpenSpec artifact set produced by `openspec-propose`.
- Clarify the stable audit contract for completed non-legacy features.
- Add narrow regression coverage for the new failure modes.

**Non-Goals:**
- Change how `[DEFER]` items are validated.
- Relax or redesign the existing `[READY]` gate.
- Introduce new workflow sections or new feature states.

## Decisions

### Decision: Gate linkage collection behind scaffold availability in diagnosis
Diagnosis should only call the change-linkage helper when the planning scaffold needed by that helper is present. That preserves structured findings and avoids a second control path that can still raise.

### Decision: Treat shaping-artifact presence as a workflow invariant, not a readiness-only check
Once a backlog item is promoted, the linked OpenSpec change should already contain `proposal.md`, `design.md`, and `tasks.md`. That is not the same as being `[READY]`; it is the baseline shaping authority created by `openspec-propose`.

### Decision: Make archived `[DONE]` expectations explicit in the stable audit spec
The implementation already distinguishes active changes for active work from archived state for completed work. The spec should state that directly so the audit contract is no longer internally ambiguous.

## Risks / Trade-offs

- [Broader shaping enforcement] -> Keep the new requirement limited to the authored baseline artifacts and do not import `[READY]`-only checks into `[SHAPING]`.
- [Diagnosis/control-flow drift] -> Reuse shared helpers where possible, but guard them with scaffold-aware checks in diagnosis.
- [Spec wording duplication] -> Keep `workflow-audit-and-repair` focused on validation behavior and `openspec-change-integration` focused on shaping/change-authority expectations.

## Migration Plan

1. Harden diagnosis control flow around missing planning scaffold.
2. Extend shared validation to report missing shaping artifacts.
3. Update audit and diagnosis to use the stricter shaping baseline.
4. Tighten the stable spec wording for completed archived-change expectations.
5. Add focused regression coverage.

## Open Questions

- None.

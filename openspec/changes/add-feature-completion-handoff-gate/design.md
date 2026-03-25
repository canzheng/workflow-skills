## Context

`complete-task` currently resolves only the active task and leaves feature acceptance as an operator decision described in skill text. `finish-feature` then requires the feature to already be in `[DONE]`. The gap is not that `finish-feature` is wrong; it is that the path from “final task completed” to “feature is now ready for finish-feature” is under-specified and weakly enforced.

## Goals / Non-Goals

**Goals:**
- Make the final task handoff into `[DONE]` explicit and testable.
- Keep feature acceptance distinct from task completion while making the transition operationally clear.
- Ensure `finish-feature` remains gated on `[DONE]` rather than guessing feature completion itself.

**Non-Goals:**
- Auto-archive or auto-finish the branch from `complete-task`.
- Replace feature-level acceptance with a naive “all tasks checked means done” rule unless the workflow explicitly says that is sufficient.

## Decisions

### Decision: Add an explicit feature-completion decision point to completion flow
The completion flow should return enough information to decide whether the feature stays `[IN_PROGRESS]` or moves to `[DONE]`, instead of leaving that as an entirely undocumented operator guess.

### Decision: Keep `finish-feature` strict
`finish-feature` should continue requiring `[DONE]`. The fix belongs in the handoff from `complete-task`, not in loosening the finish gate.

## Risks / Trade-offs

- [Feature acceptance is still repo-specific] -> Keep the workflow explicit about the decision point and required evidence rather than pretending it can infer all acceptance automatically.
- [Operators may expect “last task means done”] -> Document the exact handoff behavior and test both acceptance branches.

## Migration Plan

1. Define the feature-completion handoff requirement.
2. Update completion helpers/tests to expose the final-task decision path.
3. Keep finish-feature strict on `[DONE]`.
4. Add regression coverage for the handoff.

## Open Questions

- Should the workflow treat “all top-level tasks done” as sufficient by default, or should it require an explicit feature-acceptance confirmation?

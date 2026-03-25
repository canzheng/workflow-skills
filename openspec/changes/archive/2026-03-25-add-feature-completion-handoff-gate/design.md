## Context

`complete-task` currently resolves the active task and is documented as the place that may move a feature to `[DONE]`. `finish-feature` then assumes the feature has already crossed that boundary and focuses on OpenSpec validation/archive. That split creates a semantic mismatch: `DONE` no longer cleanly means “acceptance has passed,” and the workflow has no single owner for the transition from task completion into feature completion.

## Goals / Non-Goals

**Goals:**
- Make the final-task handoff explicit and testable without letting `complete-task` decide feature completion.
- Make `finish-feature` the single owner of the terminal feature transition from `[IN_PROGRESS]` to `[DONE]`.
- Keep `DONE` aligned with “acceptance passed,” not merely “all tasks are closed.”
- Ensure top-level OpenSpec task closure is blocked when any nested checklist item under that task is still open.

**Non-Goals:**
- Auto-archive or auto-finish the branch from `complete-task`.
- Infer feature acceptance from “all tasks checked” alone.
- Add a new intermediate backlog state such as `READY_TO_FINISH`.

## Decisions

### Decision: `complete-task` stops at task closure
`complete-task` should close tasks, verify evidence, and make the final-task handoff explicit, but it should never move a feature to `[DONE]`. If the completed task was the last top-level task, the result is “ready for finish-feature,” not “feature is done.”

### Decision: `finish-feature` owns `[IN_PROGRESS] -> [DONE]`
`finish-feature` should start from `[IN_PROGRESS]` and require:

- all top-level OpenSpec tasks are done
- `Current Task` is `none`
- the linked OpenSpec change is present

Only after feature acceptance is confirmed and OpenSpec validation/archive succeeds should `finish-feature` move the feature to `[DONE]`.

### Decision: Top-level task closure requires closed nested checklist items
Top-level OpenSpec tasks remain the workflow execution units, but nested checklist items are still meaningful implementation detail. `complete-task` should therefore refuse to close a top-level task while any nested checklist item under that task remains unchecked.

## Risks / Trade-offs

- [DONE becomes a near-terminal state] -> Accept this because it matches the semantic meaning the user wants: acceptance has passed.
- [Operators may expect “last task means done”] -> Document that the last task only makes `finish-feature` startable.
- [Nested checklist validation adds parser work] -> Keep the rule local to the selected top-level task rather than expanding checklist semantics globally.

## Migration Plan

1. Update the workflow contract and change specs so `finish-feature` owns the terminal feature transition.
2. Update `complete-task` to expose “ready for finish-feature” rather than moving the feature to `[DONE]`.
3. Update `finish-feature` to validate readiness from `[IN_PROGRESS]` and move the feature to `[DONE]` only after acceptance/archive passes.
4. Add task-closure validation for nested checklist items.
5. Add regression coverage for the new task/finalization boundary.

## Open Questions

- None. The approved contract is:
  - `finish-feature` owns `[IN_PROGRESS] -> [DONE]`
  - `DONE` means acceptance passed
  - `complete-task` must validate nested checklist closure before top-level closure

## Context

The workflow already allows cross-feature dependency references such as `v1-f001/2`, and the drift checker has logic to resolve them. The shared OpenSpec task parser does not: it treats any dependency containing `/` as automatically unsatisfied, and it only follows active change directories when loading another feature's tasks. The result is inconsistent task state depending on which helper is asked.

## Goals / Non-Goals

**Goals:**
- Make OpenSpec-backed task status derivation honor resolvable cross-feature dependencies.
- Allow dependency resolution to read archived upstream changes for completed features.
- Keep task selection, drift detection, and diagnostics aligned on one dependency model.

**Non-Goals:**
- Redesign the workflow dependency syntax.
- Introduce multi-change execution or parallel task execution.

## Decisions

### Decision: Centralize cross-feature readiness on the dependency resolver
Task status derivation should use the same dependency-resolution path already used by readiness drift instead of hard-coding `/` dependencies as unsatisfied.

### Decision: Treat archived changes as valid task history for completed features
When a dependency points to a completed feature, task lookup should be able to load `tasks.md` from the archived change directory recorded by that feature.

### Decision: Add regression fixtures for active and archived upstream dependencies
This bug is subtle because several helpers disagree while individual tests still pass. The fix should add end-to-end fixture coverage at the resolver level.

## Risks / Trade-offs

- [Archived task lookup adds more branches] -> Keep the lookup helper narrow and test both active and archived cases.
- [Status derivation could diverge from legacy inline task parsing] -> Limit the change to OpenSpec-backed task loading and leave legacy parsing untouched.

## Migration Plan

1. Refactor shared dependency/status derivation.
2. Update task-selection callers if their assumptions change.
3. Add fixture coverage for archived and active cross-feature dependencies.
4. Re-run narrow workflow tests and resolver checks.

## Open Questions

- None.

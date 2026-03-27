## Context

`autonomous-backlog-loop` is meant to advance eligible work, but its resolver currently treats feature/task presence as sufficient. The main workflow wrappers enforce more: linkage, readiness honesty, and drift-free state. The autonomous path should not be a weaker contract than the manual path.

## Goals / Non-Goals

**Goals:**
- Make autonomous task selection skip or reject invalid active features.
- Reuse shared readiness/linkage checks instead of inventing a second policy.
- Keep backlog shaping and ready-feature recommendations available for clean states.

**Non-Goals:**
- Rebuild the autonomous backlog loop around full wrapper execution.
- Add new autonomous actions beyond the current shape/ready/run-task decisions.

## Decisions

### Decision: Reuse shared readiness validation before returning `run_task_loop`
The autonomous resolver should validate the same invariants as `start-task` before it offers a task as executable.

### Decision: Treat malformed active features as blocking workflow issues
If the active board contains invalid `[READY]` or `[IN_PROGRESS]` features, the resolver should stop with a useful error rather than silently route around the problem.

## Risks / Trade-offs

- [Automation becomes stricter] -> That is intentional; strictness keeps autonomous runs aligned with the documented workflow.
- [Some existing fixtures may need repair] -> Update tests to make the new contract explicit.

## Migration Plan

1. Add shared validation into the autonomous resolver path.
2. Add fixtures covering invalid and repaired states.
3. Re-run the narrow script/helper tests.

## Open Questions

- None.

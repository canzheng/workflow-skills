## Why

The workflow benchmark shows that a meaningful share of overhead is administrative coordination rather than implementation work. The most common long status-only turns are explicit relays like "task complete, feature remains `IN_PROGRESS`, next handoff is ...", prose-only review verdict summaries, and autonomous-loop notifications that mostly move workflow state forward without changing code.

The current workflow keeps those relays explicit, but the implementation also adds avoidable overhead on top of that contract:

- final-task completion always forces a separate `finish-feature` handoff turn
- review outcomes are mostly persisted as prose instead of machine-checkable verdict state
- execution resolvers and finish checks can be blocked by unrelated malformed sibling features
- autonomous loop coordination still pays extra agent-lifecycle cost for relay-only transitions

## What Changes

- Add a deterministic continuation path so `complete-task` can hand off directly to the next ready workflow action when no unresolved decision remains, including the final-task path into `finish-feature`.
- Extend that continuation contract into `autonomous-backlog-loop` so autonomous execution does not stop on a status-only boundary after the last task or between sequential tasks on the same feature.
- Persist structured review verdict state for readiness and task/feature execution gates so approval outcomes do not have to travel only as prose summaries.
- Tighten execution resolvers and finish checks so they scope blocking validation to the selected feature/worktree, while still surfacing unrelated workflow drift as diagnostics instead of silently ignoring it.
- Reduce autonomous-loop relay overhead by keeping feature-local continuation inside the same feature-scoped agent rather than requiring extra outer-step status coordination when no human decision is needed.

## Capabilities

### Modified Capabilities

- `task-execution-handoff`: task completion, next-step continuation, worktree targeting, and autonomous continuation now support deterministic machine-readable handoff instead of status-only relay turns.
- `feature-execution-tracking`: feature files now carry structured review verdict state in addition to existing handoff notes and validation evidence.
- `workflow-audit-and-repair`: execution-scoped helpers now distinguish selected-feature blocking issues from unrelated workflow drift, while direct audit remains the global integrity gate.

## Impact

- `skills/start-task/SKILL.md`
- `skills/complete-task/SKILL.md`
- `skills/finish-feature/SKILL.md`
- `skills/autonomous-backlog-loop/SKILL.md`
- `skills/start-task/scripts/resolve_start_task.py`
- `skills/complete-task/scripts/resolve_complete_task.py`
- `skills/finish-feature/scripts/resolve_finish_feature.py`
- `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py`
- `skills/_workflow/workflow_state.py`
- `docs/planning/WORKFLOW_REFERENCE.md`
- `openspec/specs/task-execution-handoff/spec.md`
- `openspec/specs/feature-execution-tracking/spec.md`
- `openspec/specs/workflow-audit-and-repair/spec.md`
- `tests/test_workflow_contract_docs.py`
- `tests/test_workflow_openspec_integration.py`
- `tests/test_finish_feature.py`

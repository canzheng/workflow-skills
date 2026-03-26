## Why

The repository currently talks about "OpenSpec task readiness" in several places even though OpenSpec itself does not model execution readiness. In this workflow, OpenSpec owns task definitions and checkbox completion state, while readiness and dependency semantics are interpreted by the workflow layer.

## What Changes

- Clarify the contract, specs, skill docs, and user-facing wording so task readiness is described as workflow-derived rather than OpenSpec-native.
- Define the workflow task dependency convention precisely: only top-level checklist items are executable tasks, `Current Task` marks `in_progress`, checked top-level tasks are `done`, and unchecked top-level tasks become `ready` when workflow prerequisites are satisfied.
- Treat optional `Depends On` markdown blocks as a workflow parser convention rather than an OpenSpec feature.
- Require workflow-managed `openspec/changes/<change-id>/tasks.md` files to include explicit top-level checklist items for each executable task group, with nested checklist items remaining implementation detail.
- Make shaping and readiness validation fail clearly when `tasks.md` uses nested checklist items without the required parent top-level executable task entry.
- Recommend naming linked OpenSpec changes with a version/feature prefix when workflow shaping creates them, while keeping naming guidance non-gating for audit and readiness checks.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Clarify that readiness and dependency semantics are workflow-owned and that executable tasks must be represented by top-level checklist items.
- `workflow-audit-and-repair`: Audit and readiness checks will reject malformed `tasks.md` structures that do not expose required top-level executable tasks.
- `openspec-change-integration`: Workflow shaping and readiness rules will describe `tasks.md` as source material whose executable structure must satisfy workflow conventions.

## Impact

- Affected helpers/scripts: `skills/_workflow/workflow_state.py`, `skills/audit-workflow/scripts/audit_workflow.py`, and any shared validation used by `ready-feature`
- Affected skills/docs: `ready-feature`, `shape-backlog-item`, and repository workflow documentation such as `README.md` and `AGENTS-global-workflow.md`
- Affected tests: workflow-state, audit, and workflow integration fixtures that currently assume malformed nested-only task structures are acceptable

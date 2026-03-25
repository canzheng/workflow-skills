## MODIFIED Requirements

### Requirement: Task execution uses top-level OpenSpec task IDs and a task-scoped implementation plan
Executable workflow tasks SHALL be represented by top-level checklist items in the linked OpenSpec `tasks.md`, and each task SHALL be executed with a task-scoped implementation plan stored under the linked change.

#### Scenario: Starting a task prepares implementation context
- **WHEN** `start-task` selects the next executable task for a feature
- **THEN** the task is identified by its top-level OpenSpec task ID such as `1`, `2`, or `3`
- **AND** `start-task` provides the linked OpenSpec change context for that task
- **AND** it writes or updates `openspec/changes/<change-id>/implementation-plans/<task-id>.md` before code execution begins
- **AND** that implementation plan becomes part of the execution context for the task
- **AND** active execution is represented by `Current Task` in the feature file while OpenSpec `tasks.md` remains the checked/unchecked task ledger

#### Scenario: Nested checklist items remain implementation detail
- **WHEN** a linked OpenSpec `tasks.md` contains nested checklist items such as `1.1` or `1.2`
- **THEN** those nested items are treated as implementation detail under their parent top-level task
- **AND** they are not treated as standalone executable workflow tasks

### Requirement: Workflow task readiness is derived from checklist state plus the dependency convention
Workflow task readiness SHALL be derived by repository helpers from top-level OpenSpec checklist state, feature-file current-task metadata, and any optional `Depends On` markdown blocks interpreted by the workflow layer.

#### Scenario: Workflow derives a ready task from OpenSpec task markdown
- **WHEN** workflow skills evaluate whether a top-level OpenSpec task is executable
- **THEN** checked tasks are treated as `done`
- **AND** the task named by `Current Task` is treated as `in_progress`
- **AND** an unchecked task with satisfied workflow prerequisites and `Depends On` references is treated as `ready`
- **AND** those dependency references are interpreted by the workflow layer rather than by a native OpenSpec task dependency model

#### Scenario: Workflow derives a ready task without explicit dependencies
- **WHEN** workflow skills evaluate an unchecked top-level OpenSpec task that has no `Depends On` block
- **AND** no other workflow rule blocks execution
- **THEN** the workflow treats that task as `ready`

## ADDED Requirements

### Requirement: Workflow-managed task files expose executable parent checklist items
Workflow-managed OpenSpec `tasks.md` files SHALL include an explicit top-level checklist item for each executable task group.

#### Scenario: Shaped change defines executable tasks
- **WHEN** a workflow-managed OpenSpec change defines task work in `tasks.md`
- **THEN** each executable task group has a parent top-level checklist item such as `- [ ] 1 ...`
- **AND** any nested checklist items remain children of that parent task rather than standalone execution units

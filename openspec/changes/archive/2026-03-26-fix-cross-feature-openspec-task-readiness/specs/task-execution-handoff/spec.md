## MODIFIED Requirements

### Requirement: Task execution uses top-level OpenSpec task IDs and a task-scoped implementation plan
Executable workflow tasks SHALL be top-level OpenSpec task IDs, and each task SHALL be executed with a task-scoped implementation plan stored under the linked change.

#### Scenario: Starting a task prepares implementation context
- **WHEN** `start-task` selects the next executable task for a feature
- **THEN** the task is identified by its top-level OpenSpec task ID such as `1`, `2`, or `3`
- **AND** `start-task` provides the linked OpenSpec change context for that task
- **AND** the workflow writes or updates `openspec/changes/<change-id>/implementation-plans/<task-id>.md` before code execution begins
- **AND** that implementation plan becomes part of the execution context for the task

#### Scenario: Cross-feature dependency becomes executable after upstream completion
- **WHEN** an unchecked OpenSpec task depends on another feature's task using `<feature-id>/<task-id>`
- **AND** the referenced upstream task is complete in either the active feature state or the archived change for that completed feature
- **THEN** the workflow treats the local task as executable once its dependencies are otherwise satisfied
- **AND** task selection, diagnostics, and readiness reporting agree on that executable state

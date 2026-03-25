## MODIFIED Requirements

### Requirement: OpenSpec change artifacts justify readiness
Workflow-derived readiness SHALL be determined from the linked change artifacts rather than from long-form design and plan prose embedded in the feature file.

#### Scenario: Feature becomes ready from linked OpenSpec artifacts
- **WHEN** a shaped feature is evaluated for promotion to `[READY]`
- **THEN** the linked OpenSpec change has `proposal.md`, `design.md`, and `tasks.md`
- **AND** the feature file links to the affected OpenSpec capability specs
- **AND** at least one top-level execution task can be started without further shaping work

### Requirement: OpenSpec tasks are authoritative for workflow execution
The linked OpenSpec change SHALL be the task-definition authority and checkbox-completion ledger for workflow execution, while workflow readiness remains derived by repository workflow rules.

#### Scenario: Workflow execution reads task state from OpenSpec
- **WHEN** workflow skills determine task readiness, start a task, or complete a task
- **THEN** they read task definitions and checkbox status from `openspec/changes/<change-id>/tasks.md`
- **AND** they derive readiness from workflow rules such as top-level task structure, `Current Task`, and the workflow task dependency convention
- **AND** they do not require a second authored task ledger in the feature file

## ADDED Requirements

### Requirement: Workflow shaping authors workflow-compatible OpenSpec task structure
Promoting or reshaping workflow-managed OpenSpec changes SHALL produce `tasks.md` content that exposes executable work through top-level checklist items.

#### Scenario: Backlog shaping writes linked task structure
- **WHEN** `shape-backlog-item` creates or updates the linked OpenSpec change for a promoted feature
- **THEN** the resulting `tasks.md` includes a top-level checklist item for each executable task group
- **AND** nested checklist items are authored only as children of those top-level executable tasks

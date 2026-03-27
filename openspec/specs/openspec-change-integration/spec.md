# openspec-change-integration Specification

## Purpose
Define how promoted workflow features link to one OpenSpec change, which linked change artifacts are required for readiness, and how workflow execution derives task structure and readiness from that linked OpenSpec source of truth.
## Requirements
### Requirement: Promoted features link to one OpenSpec change
Each feature promoted out of `[BACKLOG]` SHALL record exactly one linked OpenSpec change as the authority for shaping and readiness artifacts.

#### Scenario: Feature enters shaping with an OpenSpec change
- **WHEN** a backlog item is promoted into a feature for shaping
- **THEN** the feature is assigned one OpenSpec change ID
- **AND** the linked change directory exists under `openspec/changes/`

### Requirement: OpenSpec change artifacts justify readiness
Workflow-derived readiness SHALL be determined from the linked change artifacts rather than from long-form design and plan prose embedded in the feature file.

#### Scenario: Feature becomes ready from linked OpenSpec artifacts
- **WHEN** a shaped feature is evaluated for promotion to `[READY]`
- **THEN** the linked OpenSpec change has `proposal.md`, `design.md`, and `tasks.md`
- **AND** the feature file links to the affected OpenSpec capability specs
- **AND** at least one execution task can be started without further shaping work

### Requirement: OpenSpec tasks are authoritative for workflow execution
The linked OpenSpec change SHALL be the task-definition authority and checkbox-completion ledger for workflow execution, while workflow readiness remains derived by repository workflow rules.

#### Scenario: Workflow execution reads task state from OpenSpec
- **WHEN** workflow skills determine task readiness, start a task, or complete a task
- **THEN** they read task definitions and checkbox status from `openspec/changes/<change-id>/tasks.md`
- **AND** they derive readiness from workflow rules such as top-level task structure, `Current Task`, and the workflow task dependency convention
- **AND** they do not require a second authored task ledger in the feature file

### Requirement: Workflow shaping authors workflow-compatible OpenSpec task structure
Promoting or reshaping workflow-managed OpenSpec changes SHALL produce `tasks.md` content that exposes executable work through top-level checklist items.

#### Scenario: Backlog shaping writes linked task structure
- **WHEN** `shape-backlog-item` creates or updates the linked OpenSpec change for a promoted feature
- **THEN** the resulting `tasks.md` includes a top-level checklist item for each executable task group
- **AND** nested checklist items are authored only as children of those top-level executable tasks

### Requirement: Workflow promotion owns the OpenSpec propose step
Promoting a backlog item into shaping SHALL create or update its linked OpenSpec change through the workflow wrapper rather than through an independent manual lane.

#### Scenario: Backlog shaping creates the linked change
- **WHEN** `shape-backlog-item` promotes work from `[BACKLOG]` into `[SHAPING]`
- **THEN** it creates or updates the linked OpenSpec change as part of that workflow
- **AND** the resulting feature file and backlog entry reference that same linked change

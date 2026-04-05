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

### Requirement: Shaping retains authored OpenSpec change artifacts
Promoted workflow-managed features in `[SHAPING]` SHALL keep the authored baseline artifacts created by `openspec-propose`.

#### Scenario: Feature enters shaping with authored change artifacts
- **WHEN** `shape-backlog-item` promotes a backlog item into `[SHAPING]`
- **THEN** the linked OpenSpec change contains `proposal.md`, `design.md`, and `tasks.md`
- **AND** those files remain part of the shaping authority for that feature until later workflow stages tighten additional gates

### Requirement: Shaped executable tasks expose proof obligations and validation intent
Workflow-managed OpenSpec shaping SHALL define proof obligations and planned validation coverage for executable tasks before those tasks enter execution.

#### Scenario: Ready task is justified by explicit shaping context
- **WHEN** workflow shaping prepares a feature for promotion to `[READY]`
- **THEN** the linked proposal, design, spec paths, and task structure describe the task's intended contract surface clearly enough for `start-task` to draft the task implementation plan without inventing or narrowing scope
- **AND** readiness guidance does not treat a task as execution-ready when proof intent is still implicit or only described through lower-level helper tests

### Requirement: Ready features require contract-aligned proof coverage
Workflow readiness SHALL require at least one execution task whose shaped contract surface is independently reviewed as clear enough for execution planning rather than relying only on dependency-derived status.

#### Scenario: Ready-feature rejects dependency-ready work without independent contract review
- **WHEN** a feature has a top-level task that is dependency-ready under the workflow task rules
- **AND** an independent readiness review finds that the shaping artifacts still leave the task's contract surface ambiguous, incomplete, or vulnerable to surrogate-proof narrowing
- **THEN** `ready-feature` does not promote the feature to `[READY]`
- **AND** the missing contract clarity is treated as unresolved shaping work rather than as execution-time cleanup

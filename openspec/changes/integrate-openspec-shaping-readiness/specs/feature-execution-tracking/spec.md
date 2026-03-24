## MODIFIED Requirements

### Requirement: Feature files own task-level execution state
Each promoted feature SHALL maintain a feature file that records task-level execution state and evidence.

#### Scenario: Feature file carries task execution state
- **WHEN** a backlog item has been promoted into a feature
- **THEN** the feature has a single feature file under `docs/planning/versions/<version>/features/`
- **AND** the feature file records the linked OpenSpec change and affected OpenSpec specs
- **AND** the feature file stores validation evidence and handoff notes for execution
- **AND** design prose, task definitions, task status, and implementation-planning prose live in the linked OpenSpec artifacts instead of the feature file

### Requirement: Board state and task state are separated
The backlog board SHALL track feature-level state without duplicating task-level execution details.

#### Scenario: Feature board remains high level
- **WHEN** feature progress is updated on the board
- **THEN** `BACKLOG.md` records only the feature’s board section and linked summary entry
- **AND** task definition and task status remain in OpenSpec

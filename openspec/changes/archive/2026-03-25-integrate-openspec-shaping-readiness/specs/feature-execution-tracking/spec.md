## MODIFIED Requirements

### Requirement: Feature files own task-level execution state
Each promoted feature SHALL maintain a feature file that records execution metadata and evidence.

#### Scenario: Feature file carries task execution state
- **WHEN** a backlog item has been promoted into a feature
- **THEN** the feature has a single feature file under `docs/planning/versions/<version>/features/`
- **AND** the feature file records the linked OpenSpec change and affected OpenSpec specs
- **AND** the feature file stores current-task tracking, validation evidence, and handoff notes
- **AND** task definitions and checkbox completion state remain in OpenSpec
- **AND** any optional `Depends On` references are interpreted through the workflow's markdown dependency convention rather than a native OpenSpec task model

### Requirement: Board state and task state are separated
The backlog board SHALL track feature-level state without duplicating task-level execution details.

#### Scenario: Feature board remains high level
- **WHEN** feature progress is updated on the board
- **THEN** `BACKLOG.md` records only the feature’s board section and linked summary entry
- **AND** task definition and task status remain in OpenSpec

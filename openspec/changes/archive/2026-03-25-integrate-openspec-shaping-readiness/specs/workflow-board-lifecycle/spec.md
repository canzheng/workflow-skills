## MODIFIED Requirements

### Requirement: Promotion from backlog creates a feature record
A backlog item SHALL become a feature when it leaves `[BACKLOG]` for active shaping.

#### Scenario: Backlog item enters shaping
- **WHEN** a backlog item is promoted from `[BACKLOG]` to `[SHAPING]`
- **THEN** a stable feature ID is assigned
- **AND** a linked feature file is created for that feature
- **AND** the feature file records one linked OpenSpec change as the shaping authority

### Requirement: Feature execution starts only from ready
Execution SHALL begin only after shaping has produced at least one executable task.

#### Scenario: Ready feature enters execution
- **WHEN** a feature in `[READY]` starts its first executing task
- **THEN** the feature moves to `[IN_PROGRESS]`
- **AND** the feature remains in `[IN_PROGRESS]` until it reaches `[DONE]` or `[DEFER]`

#### Scenario: Ready state requires linked OpenSpec shaping artifacts
- **WHEN** a feature is promoted into `[READY]`
- **THEN** its linked OpenSpec change includes `proposal.md`, `design.md`, and `tasks.md`
- **AND** the feature file links to the affected OpenSpec capability specs
- **AND** at least one execution task is ready to start

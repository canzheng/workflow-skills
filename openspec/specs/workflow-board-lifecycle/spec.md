## Purpose
Define the canonical feature-level workflow board, allowed lifecycle transitions, and the point at which a backlog item becomes an executable feature.
## Requirements
### Requirement: Backlog board owns feature workflow status
The active version backlog SHALL be the canonical board for feature-level workflow status.

#### Scenario: Active backlog provides the canonical feature board
- **WHEN** a repository adopts the workflow planning structure
- **THEN** the active board is `docs/planning/current_version/BACKLOG.md`
- **AND** feature-level status is represented only through the `[BACKLOG]`, `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` sections

### Requirement: Promotion from backlog creates a feature record
A backlog item SHALL become a feature when it leaves `[BACKLOG]` for active shaping.

#### Scenario: Backlog item enters shaping
- **WHEN** a backlog item is promoted from `[BACKLOG]` to `[SHAPING]`
- **THEN** a stable feature ID is assigned
- **AND** a linked feature file is created for that feature

### Requirement: Feature execution starts only from ready
Execution SHALL begin only after shaping has produced at least one executable task.

#### Scenario: Ready feature enters execution
- **WHEN** a feature in `[READY]` starts its first executing task
- **THEN** the feature moves to `[IN_PROGRESS]`
- **AND** the feature remains in `[IN_PROGRESS]` until it reaches `[DONE]` or `[DEFER]`

### Requirement: Deferral is available before completion
Deferred status SHALL be available for work that is not complete.

#### Scenario: Feature is deferred before completion
- **WHEN** a feature in `[BACKLOG]`, `[SHAPING]`, `[READY]`, or `[IN_PROGRESS]` is intentionally postponed or dropped
- **THEN** the feature may move to `[DEFER]`
- **AND** the reason for the deferral is recorded in the backlog entry or linked feature file

#### Scenario: Completed work is not reclassified as deferred
- **WHEN** a feature has already reached `[DONE]`
- **THEN** it is not reclassified into `[DEFER]`

### Requirement: Completed features support explicit historical migration exemptions
Completed-feature audit expectations SHALL distinguish historical pre-OpenSpec work from post-adoption archived work.

#### Scenario: Historical completed feature remains done after OpenSpec adoption
- **WHEN** a feature was completed before OpenSpec adoption and the repo later adopts OpenSpec
- **THEN** the feature may remain in `[DONE]`
- **AND** its feature file may mark `OpenSpec Status` as `legacy-exempt`

#### Scenario: Post-adoption completed feature uses archived OpenSpec state
- **WHEN** a feature reaches `[DONE]` after OpenSpec adoption
- **THEN** its linked OpenSpec change is expected to be archived rather than active

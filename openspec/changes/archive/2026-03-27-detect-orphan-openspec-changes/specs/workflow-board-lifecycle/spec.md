## MODIFIED Requirements

### Requirement: Promotion from backlog creates a feature record
A backlog item SHALL become a feature when it leaves `[BACKLOG]` for active shaping.

#### Scenario: Backlog item enters shaping
- **WHEN** a backlog item is promoted from `[BACKLOG]` to `[SHAPING]`
- **THEN** a stable feature ID is assigned
- **AND** a linked feature file is created for that feature
- **AND** the promoted feature links the active OpenSpec change that owns its shaping state

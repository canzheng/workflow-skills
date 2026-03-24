## ADDED Requirements

### Requirement: Promoted features link to one OpenSpec change
Each feature promoted out of `[BACKLOG]` SHALL record exactly one linked OpenSpec change as the authority for shaping and readiness artifacts.

#### Scenario: Feature enters shaping with an OpenSpec change
- **WHEN** a backlog item is promoted into a feature for shaping
- **THEN** the feature is assigned one OpenSpec change ID
- **AND** the linked change directory exists under `openspec/changes/`

### Requirement: OpenSpec change artifacts justify readiness
OpenSpec-backed readiness SHALL be determined from the linked change artifacts rather than from long-form design and plan prose embedded in the feature file.

#### Scenario: Feature becomes ready from linked OpenSpec artifacts
- **WHEN** a shaped feature is evaluated for promotion to `[READY]`
- **THEN** the linked OpenSpec change has `proposal.md`, `design.md`, and `tasks.md`
- **AND** the feature file links to the affected OpenSpec capability specs
- **AND** at least one execution task can be started without further shaping work

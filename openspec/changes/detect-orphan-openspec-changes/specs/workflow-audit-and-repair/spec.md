## MODIFIED Requirements

### Requirement: Workflow audit validates active OpenSpec change requirements
The workflow audit SHALL keep active OpenSpec change requirements for non-completed active work.

#### Scenario: Audit checks active change linkage for shaping and execution states
- **WHEN** the workflow audit inspects a feature in `[SHAPING]`, `[READY]`, or `[IN_PROGRESS]`
- **THEN** it verifies that the feature file records a linked OpenSpec change ID
- **AND** it verifies that `openspec/changes/<change-id>/` exists

#### Scenario: Audit rejects orphan active changes
- **WHEN** an active change exists under `openspec/changes/`
- **AND** no promoted feature links to that change ID
- **THEN** the workflow audit fails
- **AND** it reports the orphaned change ID so the board and feature state can be repaired

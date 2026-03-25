## MODIFIED Requirements

### Requirement: Workflow audit validates feature linkage consistency
The workflow audit SHALL confirm that backlog entries and feature files agree on identity, placement, and migration-era OpenSpec expectations.

#### Scenario: Audit checks feature linkage metadata
- **WHEN** the workflow audit inspects a promoted feature
- **THEN** it verifies that the feature file’s `Feature ID` matches the backlog entry
- **AND** it verifies that the feature file’s `Backlog Reference` matches the owning backlog section

#### Scenario: Audit accepts a historical completed feature during midstream adoption
- **WHEN** the workflow audit inspects a feature in `[DONE]` whose feature file records `OpenSpec Status` as `legacy-exempt`
- **THEN** it does not require a linked OpenSpec change for that historical completed feature

#### Scenario: Audit requires archive state for post-adoption completed features
- **WHEN** the workflow audit inspects a feature in `[DONE]` that records a linked OpenSpec change
- **THEN** it verifies that `openspec/changes/<change-id>/` does not exist
- **AND** it verifies that exactly one `openspec/changes/archive/*-<change-id>/` directory exists

#### Scenario: Audit rejects ambiguous completed features after adoption
- **WHEN** the workflow audit inspects a feature in `[DONE]` with neither a linked archived OpenSpec change nor `OpenSpec Status` set to `legacy-exempt`
- **THEN** the audit fails

## ADDED Requirements

### Requirement: Workflow audit validates active OpenSpec change requirements
The workflow audit SHALL keep active OpenSpec change requirements for non-completed active work.

#### Scenario: Audit checks active change linkage for shaping and execution states
- **WHEN** the workflow audit inspects a feature in `[SHAPING]`, `[READY]`, or `[IN_PROGRESS]`
- **THEN** it verifies that the feature file records a linked OpenSpec change ID
- **AND** it verifies that `openspec/changes/<change-id>/` exists

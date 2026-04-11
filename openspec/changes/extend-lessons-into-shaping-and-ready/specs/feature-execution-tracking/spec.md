## MODIFIED Requirements

### Requirement: Feature files carry lesson handoff state
Feature files SHALL preserve the lesson IDs returned by `retrieve-lessons` across workflow stages until the corresponding stage handoff is reconciled.

#### Scenario: Start-task records retrieved lesson IDs
- **WHEN** `start-task` retrieves lessons for an executing task
- **THEN** the feature file records the returned lesson IDs in handoff notes or equivalent task handoff state
- **AND** those IDs remain available to `complete-task`

#### Scenario: Shape-backlog-item records retrieved lesson IDs
- **WHEN** `shape-backlog-item` retrieves lessons for shaping work on a promoted feature
- **THEN** the feature file records the returned lesson IDs in stage-scoped handoff notes for `shaping`
- **AND** those IDs remain available until shaping lesson usage is reconciled

#### Scenario: Ready-feature records retrieved lesson IDs
- **WHEN** `ready-feature` retrieves lessons for readiness work on a shaped feature
- **THEN** the feature file records the returned lesson IDs in stage-scoped handoff notes for `ready`
- **AND** those IDs remain available until readiness lesson usage is reconciled

### Requirement: Complete-task records lesson usage in the feature file
Feature files SHALL record the usage outcome for each lesson ID that was retrieved during workflow-stage entry.

#### Scenario: Complete-task reconciles lesson usage
- **WHEN** `complete-task` closes the task
- **THEN** the feature file records whether each retrieved lesson was applied, partially applied, or not applied
- **AND** the feature file preserves that usage record as part of the completion handoff

#### Scenario: Shape-backlog-item reconciles lesson usage
- **WHEN** `shape-backlog-item` completes the shaping stage
- **THEN** the feature file records whether each retrieved lesson was applied, partially applied, or not applied during shaping
- **AND** the feature file preserves that usage record as part of the shaping handoff

#### Scenario: Ready-feature reconciles lesson usage
- **WHEN** `ready-feature` completes the readiness stage
- **THEN** the feature file records whether each retrieved lesson was applied, partially applied, or not applied during readiness
- **AND** the feature file preserves that usage record as part of the readiness handoff

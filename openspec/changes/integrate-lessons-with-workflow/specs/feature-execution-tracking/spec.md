## ADDED Requirements

### Requirement: Feature files carry lesson handoff state
Feature files SHALL preserve the lesson IDs returned by `retrieve-lessons` until the task is closed.

#### Scenario: Start-task records retrieved lesson IDs
- **WHEN** `start-task` retrieves lessons for an executing task
- **THEN** the feature file records the returned lesson IDs in handoff notes or equivalent task handoff state
- **AND** those IDs remain available to `complete-task`

### Requirement: Complete-task records lesson usage in the feature file
Feature files SHALL record the usage outcome for each lesson ID that was retrieved during task start.

#### Scenario: Complete-task reconciles lesson usage
- **WHEN** `complete-task` closes the task
- **THEN** the feature file records whether each retrieved lesson was applied, partially applied, or not applied
- **AND** the feature file preserves that usage record as part of the completion handoff

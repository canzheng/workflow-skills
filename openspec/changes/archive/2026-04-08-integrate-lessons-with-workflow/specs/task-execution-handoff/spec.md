## ADDED Requirements

### Requirement: Task execution integrates the lesson lifecycle
Task execution SHALL retrieve relevant lessons before implementation begins, carry the retrieved lesson IDs through the feature-file handoff state, record end-of-task usage for those lesson IDs during completion, capture new lesson candidates before completion is finalized, and promote durable lessons at feature finish.

#### Scenario: Start-task retrieves lessons for the active task
- **WHEN** `start-task` has read the linked change context and is preparing to begin execution
- **THEN** it retrieves relevant active lessons before drafting or updating the implementation plan
- **AND** it records the returned lesson IDs in the feature file handoff state

#### Scenario: Complete-task reconciles lesson usage before closure
- **WHEN** `complete-task` closes the active task
- **THEN** it reads the retrieved lesson IDs from the feature file handoff state
- **AND** it records whether each lesson was applied, partially applied, or not applied before completion is finalized
- **AND** it captures high-value lesson candidates after usage reconciliation and before the task is marked complete

#### Scenario: Finish-feature promotes durable lessons
- **WHEN** `finish-feature` validates and archives the linked OpenSpec change
- **THEN** it promotes only the small set of durable high-value lessons before branch finalization
- **AND** `refresh-lessons` remains explicitly user-triggered rather than part of the automated workflow

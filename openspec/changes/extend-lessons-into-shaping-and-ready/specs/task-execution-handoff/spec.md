## MODIFIED Requirements

### Requirement: Task execution integrates the lesson lifecycle
The workflow lesson lifecycle SHALL retrieve relevant lessons before shaping, readiness, and execution work begins, carry the retrieved lesson IDs through feature-file handoff state, record stage-exit usage for those lesson IDs, capture new lesson candidates before each stage is finalized, and promote durable lessons at feature finish.

#### Scenario: Shape-backlog-item retrieves lessons for shaping
- **WHEN** `shape-backlog-item` has gathered the initial context for a promoted backlog item
- **THEN** it retrieves relevant active lessons before finalizing the shaping output
- **AND** it records the returned lesson IDs in the feature file handoff state for `shaping`

#### Scenario: Ready-feature retrieves lessons for readiness
- **WHEN** `ready-feature` has read the feature file and linked change context and is preparing the independent readiness review
- **THEN** it retrieves relevant active lessons before readiness is judged
- **AND** it records the returned lesson IDs in the feature file handoff state for `ready`

#### Scenario: Start-task retrieves lessons for the active task
- **WHEN** `start-task` has read the linked change context and is preparing to begin execution
- **THEN** it retrieves relevant active lessons before drafting or updating the implementation plan
- **AND** it records the returned lesson IDs in the feature file handoff state

#### Scenario: Shape-backlog-item reconciles lesson usage before stage exit
- **WHEN** `shape-backlog-item` finishes shaping work for the promoted feature
- **THEN** it reads the retrieved lesson IDs from the `shaping` handoff state
- **AND** it records whether each lesson was applied, partially applied, or not applied before the stage exits
- **AND** it captures high-value lesson candidates after usage reconciliation and before the shaping stage is finalized

#### Scenario: Ready-feature reconciles lesson usage before stage exit
- **WHEN** `ready-feature` finishes readiness work for the shaped feature
- **THEN** it reads the retrieved lesson IDs from the `ready` handoff state
- **AND** it records whether each lesson was applied, partially applied, or not applied before the stage exits
- **AND** it captures high-value lesson candidates after usage reconciliation and before the feature is promoted to `[READY]`

#### Scenario: Complete-task reconciles lesson usage before closure
- **WHEN** `complete-task` closes the active task
- **THEN** it reads the retrieved lesson IDs from the feature file handoff state
- **AND** it records whether each lesson was applied, partially applied, or not applied before completion is finalized
- **AND** it captures high-value lesson candidates after usage reconciliation and before the task is marked complete

#### Scenario: Finish-feature promotes durable lessons
- **WHEN** `finish-feature` validates and archives the linked OpenSpec change
- **THEN** it promotes only the small set of durable high-value lessons before branch finalization
- **AND** `refresh-lessons` remains explicitly user-triggered rather than part of the automated workflow

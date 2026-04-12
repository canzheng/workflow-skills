## ADDED Requirements

### Requirement: Task execution integrates the lesson lifecycle
Task execution SHALL retrieve relevant lessons before implementation begins, carry the retrieved lesson IDs through the feature-file handoff state, record end-of-task usage for those lesson IDs during completion, record high-signal observations in `docs/lessons/notes.md` before completion is finalized when the work surfaces reusable lessons, near-misses, or fragile decisions, and run `distill-lessons` only at feature finish.

#### Scenario: Start-task retrieves lessons for the active task
- **WHEN** `start-task` has read the linked change context and is preparing to begin execution
- **THEN** it retrieves relevant active lessons before drafting or updating the implementation plan
- **AND** it records the returned lesson IDs in the feature file handoff state

#### Scenario: Complete-task reconciles lesson usage before closure
- **WHEN** `complete-task` closes the active task
- **THEN** it reads the retrieved lesson IDs from the feature file handoff state
- **AND** it records whether each lesson was applied, partially applied, or not applied before completion is finalized
- **AND** it records any high-signal observations in `docs/lessons/notes.md` after usage reconciliation and before the task is marked complete when the work surfaced reusable lessons, near-misses, or fragile decisions

#### Scenario: Finish-feature distills durable lessons only at feature completion
- **WHEN** `finish-feature` validates and archives the linked OpenSpec change
- **THEN** it runs `distill-lessons` to review `docs/lessons/notes.md` and distill only the small set of durable reusable lessons before branch finalization
- **AND** `refresh-lessons` remains explicitly user-triggered rather than part of the automated workflow

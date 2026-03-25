## ADDED Requirements

### Requirement: Task completion makes the finish-feature handoff explicit
Completing the active task SHALL make it explicit whether the feature still has more task work remaining or is now ready for `finish-feature`.

#### Scenario: Final accepted task completes but feature still remains in progress
- **WHEN** `complete-task` finishes the active task
- **AND** feature-level acceptance is not yet satisfied
- **THEN** the feature remains in `[IN_PROGRESS]`
- **AND** the workflow reports that `finish-feature` is not yet startable

#### Scenario: Final task completion makes finish-feature startable
- **WHEN** `complete-task` finishes the active task
- **AND** all top-level OpenSpec tasks are done
- **THEN** the feature remains in `[IN_PROGRESS]`
- **AND** the workflow reports that `finish-feature` is startable

### Requirement: Top-level task closure requires closed nested checklist items
`complete-task` SHALL refuse to close a top-level OpenSpec task while any nested checklist item under that task remains unchecked.

#### Scenario: Nested implementation detail remains open
- **WHEN** `complete-task` is asked to close a top-level OpenSpec task
- **AND** at least one nested checklist item under that task is still unchecked
- **THEN** the top-level task is not marked done
- **AND** the workflow reports that the task closure preconditions are not yet satisfied

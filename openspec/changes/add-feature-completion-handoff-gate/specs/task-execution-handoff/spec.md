## ADDED Requirements

### Requirement: Task completion makes the feature-completion handoff explicit
Completing the active task SHALL make it explicit whether the feature remains in execution or is now ready to move to `[DONE]`.

#### Scenario: Final accepted task completes but feature still remains in progress
- **WHEN** `complete-task` finishes the active task
- **AND** feature-level acceptance is not yet satisfied
- **THEN** the feature remains in `[IN_PROGRESS]`
- **AND** the workflow reports that `finish-feature` is not yet startable

#### Scenario: Feature becomes done after task completion
- **WHEN** `complete-task` finishes the active task
- **AND** feature-level acceptance is satisfied
- **THEN** the feature moves to `[DONE]`
- **AND** the resulting state makes the feature eligible for `finish-feature`

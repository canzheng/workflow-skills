## MODIFIED Requirements

### Requirement: Current task reflects active execution
Feature metadata SHALL identify whether a task is currently executing.

#### Scenario: No task is actively executing
- **WHEN** a feature has not started execution or is between tasks
- **THEN** the feature file records `Current Task` as `none`

#### Scenario: A task is actively executing
- **WHEN** execution starts on a task for a feature
- **THEN** the feature file records that task's top-level OpenSpec task ID as the current task
- **AND** the executing task is marked `in_progress`

#### Scenario: Invalid subtask identifier is rejected
- **WHEN** a feature file records `Current Task` as a nested subtask identifier such as `1.1`
- **THEN** workflow validation rejects that value as invalid metadata
- **AND** the repository must repair the feature file before execution continues

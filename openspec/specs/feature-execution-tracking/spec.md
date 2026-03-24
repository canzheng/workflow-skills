## Purpose
Define how promoted features are tracked during execution, including where task state, current-task metadata, and validation evidence live.

## Requirements

### Requirement: Feature files own task-level execution state
Each promoted feature SHALL maintain a feature file that records task-level execution state and evidence.

#### Scenario: Feature file carries task execution state
- **WHEN** a backlog item has been promoted into a feature
- **THEN** the feature has a single feature file under `docs/planning/versions/<version>/features/`
- **AND** the feature file owns task statuses, task dependencies, current-task tracking, and validation evidence

### Requirement: Board state and task state are separated
The backlog board SHALL track feature-level state without duplicating task-level execution details.

#### Scenario: Feature board remains high level
- **WHEN** feature progress is updated on the board
- **THEN** `BACKLOG.md` records only the feature’s board section and linked summary entry
- **AND** task-by-task detail remains in the feature file

### Requirement: Current task reflects active execution
Feature metadata SHALL identify whether a task is currently executing.

#### Scenario: No task is actively executing
- **WHEN** a feature has not started execution or is between tasks
- **THEN** the feature file records `Current Task` as `none`

#### Scenario: A task is actively executing
- **WHEN** execution starts on a task for a feature
- **THEN** the feature file records that task as the current task
- **AND** the executing task is marked `in_progress`

### Requirement: Completed tasks include evidence
Task completion SHALL be supported by recorded validation evidence.

#### Scenario: Task moves to done
- **WHEN** a task is marked `done`
- **THEN** the feature file includes the exact validation command or inspection step and its result
- **AND** the recorded evidence explains why the task is considered complete

## Purpose
Define how promoted features are tracked during execution, including where task state, current-task metadata, and validation evidence live.
## Requirements
### Requirement: Feature files own task-level execution state
Each promoted feature SHALL maintain a feature file that records execution metadata and evidence.

#### Scenario: Feature file carries task execution state
- **WHEN** a backlog item has been promoted into a feature
- **THEN** the feature has a single feature file under `docs/planning/versions/<version>/features/`
- **AND** the feature file records the linked OpenSpec change and affected OpenSpec specs
- **AND** the feature file stores current-task tracking, validation evidence, and handoff notes
- **AND** task definitions, task dependencies, and task completion state remain in OpenSpec

### Requirement: Board state and task state are separated
The backlog board SHALL track feature-level state without duplicating task-level execution details.

#### Scenario: Feature board remains high level
- **WHEN** feature progress is updated on the board
- **THEN** `BACKLOG.md` records only the feature’s board section and linked summary entry
- **AND** task definition and task status remain in OpenSpec

### Requirement: Current task reflects active execution
Feature metadata SHALL identify whether a task is currently executing.

#### Scenario: No task is actively executing
- **WHEN** a feature has not started execution or is between tasks
- **THEN** the feature file records `Current Task` as `none`

#### Scenario: A task is actively executing
- **WHEN** execution starts on a task for a feature
- **THEN** the feature file records that task's top-level OpenSpec task ID as the current task
- **AND** the executing task is marked `in_progress`

#### Scenario: Final task is closed before feature completion
- **WHEN** the final top-level task is closed for a feature
- **THEN** the feature may still remain `[IN_PROGRESS]`
- **AND** the feature file records `Current Task` as `none`
- **AND** the handoff notes state whether the feature is ready for `finish-feature`

### Requirement: Completed tasks include evidence
Task completion SHALL be supported by recorded validation evidence.

#### Scenario: Task moves to done
- **WHEN** a task is marked `done`
- **THEN** the feature file includes the exact validation command or inspection step and its result
- **AND** the recorded evidence explains why the task is considered complete

### Requirement: Feature completion is a finish-feature outcome
Feature metadata SHALL treat the `[IN_PROGRESS] -> [DONE]` transition as a feature-completion action, not a task-completion side effect.

#### Scenario: Finish-feature completes the feature
- **WHEN** `finish-feature` verifies acceptance and archives the linked OpenSpec change
- **THEN** the feature file records evidence for the feature-level completion decision
- **AND** the feature is moved to `[DONE]`

### Requirement: Feature files support historical completed-feature exemptions
Feature metadata SHALL support an explicit exemption marker for historical completed features that predate OpenSpec adoption.

#### Scenario: Historical completed feature is exempt from OpenSpec change linkage
- **WHEN** a repository adopts OpenSpec after a feature already reached `[DONE]`
- **THEN** the feature file may record `OpenSpec Status` as `legacy-exempt`
- **AND** the feature is not required to record a linked OpenSpec change
- **AND** the exemption does not apply to active shaping or execution states

### Requirement: Feature completion evidence supports the move to done
Feature metadata SHALL make the transition from `[IN_PROGRESS]` to `[DONE]` evidence-based rather than implicit.

#### Scenario: Finish-feature moves a feature to done after acceptance passes
- **WHEN** `finish-feature` moves a feature from `[IN_PROGRESS]` to `[DONE]`
- **THEN** the feature file records completion evidence consistent with the accepted task work
- **AND** the handoff state makes it clear that branch finalization is still a downstream `finish-feature` action

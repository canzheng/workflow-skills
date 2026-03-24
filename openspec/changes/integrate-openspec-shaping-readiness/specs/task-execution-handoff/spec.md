## MODIFIED Requirements

### Requirement: Only one repository task executes at a time
Task execution SHALL remain globally serialized at the repository level.

#### Scenario: Starting a task while another task is active
- **WHEN** one task in the repository is already `in_progress`
- **THEN** no second task is started until the active task is resolved

### Requirement: Feature execution uses a dedicated reusable worktree
Executing features SHALL use one feature-scoped worktree reused across sequential tasks.

#### Scenario: First execution task for a feature starts
- **WHEN** a feature starts its first executing task
- **THEN** a dedicated feature branch and worktree are created from a clean primary checkout

#### Scenario: Later execution task resumes on the same feature
- **WHEN** a later task starts for a feature already in execution
- **THEN** execution resumes in the same feature worktree
- **AND** that worktree is clean before the next task begins

### Requirement: Workflow execution uses OpenSpec task status
The workflow SHALL read and update task status in the linked OpenSpec change during execution.

#### Scenario: Start task marks OpenSpec task in progress
- **WHEN** `start-task` selects the next executable task for a feature
- **THEN** it selects that task from the linked OpenSpec `tasks.md`
- **AND** it records the task as `in_progress` in OpenSpec

#### Scenario: Complete task marks OpenSpec task done
- **WHEN** `complete-task` finishes a task successfully
- **THEN** it records validation evidence in the feature file
- **AND** it marks the corresponding task `done` in OpenSpec

### Requirement: Workflow execution provides explicit linked-change context
Execution wrappers SHALL provide explicit linked-change context to the executor.

#### Scenario: Start task surfaces authoritative change context
- **WHEN** `start-task` selects the next executable task for a feature
- **THEN** it provides the linked OpenSpec change directory
- **AND** it provides the Markdown files under that change as context, including `proposal.md`, `design.md`, and `tasks.md`
- **AND** it instructs the executor to read the files listed as context before starting work

#### Scenario: Complete task reuses authoritative change context
- **WHEN** `complete-task` resolves the active task for completion
- **THEN** it provides the linked OpenSpec change directory
- **AND** it provides the Markdown files under that change as context
- **AND** it instructs the executor to read the files listed as context before closing the task

### Requirement: Feature completion is distinct from branch finalization
Finishing a task or feature SHALL remain separate from final branch/worktree cleanup decisions.

#### Scenario: Feature reaches acceptance before branch finalization
- **WHEN** a feature satisfies its feature-level acceptance bar
- **THEN** the feature may move to `[DONE]`
- **AND** branch/worktree finalization remains a separate downstream action

### Requirement: Branch finalization requires archived OpenSpec change state
Feature branch finalization SHALL be gated on linked OpenSpec validation and archive state.

#### Scenario: Workflow finishes a done feature
- **WHEN** a feature in `[DONE]` is handed off for branch finalization
- **THEN** the workflow first validates the linked OpenSpec change
- **AND** it archives that change
- **AND** `openspec/changes/<change-id>/` no longer exists
- **AND** exactly one `openspec/changes/archive/*-<change-id>/` directory exists before branch finalization continues

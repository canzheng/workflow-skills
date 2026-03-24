## Purpose
Define how task execution starts, how feature worktrees are reused across tasks, what a clean completion handoff requires, and how task completion differs from branch finalization.

## Requirements

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

### Requirement: Task completion leaves a clean handoff
Completing a task SHALL leave the feature ready for the next handoff.

#### Scenario: Task is completed successfully
- **WHEN** `complete-task` finishes a task
- **THEN** verification is run and evidence is recorded before completion is claimed
- **AND** intended task changes are committed when needed to leave the feature worktree clean
- **AND** downstream task readiness is synchronized after completion

### Requirement: Feature completion is distinct from branch finalization
Finishing a task or feature SHALL remain separate from final branch/worktree cleanup decisions.

#### Scenario: Feature reaches acceptance before branch finalization
- **WHEN** a feature satisfies its feature-level acceptance bar
- **THEN** the feature may move to `[DONE]`
- **AND** branch/worktree finalization remains a separate downstream action

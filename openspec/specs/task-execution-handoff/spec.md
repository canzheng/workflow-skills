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

### Requirement: Task execution uses top-level OpenSpec task IDs and a task-scoped implementation plan
Executable workflow tasks SHALL be top-level OpenSpec task IDs, and each task SHALL be executed with a task-scoped implementation plan stored under the linked change.

#### Scenario: Starting a task prepares implementation context
- **WHEN** `start-task` selects the next executable task for a feature
- **THEN** the task is identified by its top-level OpenSpec task ID such as `1`, `2`, or `3`
- **AND** `start-task` provides the linked OpenSpec change context for that task
- **AND** the workflow writes or updates `openspec/changes/<change-id>/implementation-plans/<task-id>.md` before code execution begins
- **AND** that implementation plan becomes part of the execution context for the task
- **AND** active execution is represented by `Current Task` in the feature file while OpenSpec `tasks.md` remains the checked/unchecked task ledger

### Requirement: Workflow task readiness is derived from checklist state plus the dependency convention
Workflow task readiness SHALL be derived by repository helpers from top-level OpenSpec checklist state, feature-file current-task metadata, and any optional `Depends On` markdown blocks.

#### Scenario: Workflow derives a ready task from OpenSpec task markdown
- **WHEN** workflow skills evaluate whether a top-level OpenSpec task is executable
- **THEN** checked tasks are treated as `done`
- **AND** the task named by `Current Task` is treated as `in_progress`
- **AND** an unchecked task with satisfied workflow prerequisites and `Depends On` references is treated as `ready`
- **AND** those dependency references are interpreted by the workflow layer rather than by a native OpenSpec task dependency model

### Requirement: Task completion leaves a clean handoff
Completing a task SHALL leave the feature ready for the next handoff.

#### Scenario: Task is completed successfully
- **WHEN** `complete-task` finishes a task
- **THEN** verification is run and evidence is recorded before completion is claimed
- **AND** intended task changes are committed when needed to leave the feature worktree clean
- **AND** downstream task readiness is synchronized from checkbox completion state plus any workflow `Depends On` references

### Requirement: Feature completion is distinct from branch finalization
Finishing a task or feature SHALL remain separate from final branch/worktree cleanup decisions.

#### Scenario: Feature reaches acceptance before branch finalization
- **WHEN** a feature satisfies its feature-level acceptance bar
- **THEN** the feature may move to `[DONE]`
- **AND** branch/worktree finalization remains a separate downstream action

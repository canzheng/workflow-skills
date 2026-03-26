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

#### Scenario: Cross-feature dependency becomes executable after upstream completion
- **WHEN** an unchecked OpenSpec task depends on another feature's task using `<feature-id>/<task-id>`
- **AND** the referenced upstream task is complete in either the active feature state or the archived change for that completed feature
- **THEN** the workflow treats the local task as executable once its dependencies are otherwise satisfied
- **AND** task selection, diagnostics, and readiness reporting agree on that executable state

### Requirement: Workflow task readiness is derived from checklist state plus the dependency convention
Workflow task readiness SHALL be derived by repository helpers from top-level OpenSpec checklist state, feature-file current-task metadata, and any optional `Depends On` markdown blocks interpreted by the workflow layer.

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
- **AND** downstream workflow-derived task readiness is synchronized from checkbox completion state plus any workflow `Depends On` references

#### Scenario: Final task completes but feature completion remains downstream
- **WHEN** `complete-task` closes the final top-level task for a feature
- **THEN** the feature remains `[IN_PROGRESS]`
- **AND** `Current Task` is `none`
- **AND** the workflow reports whether `finish-feature` is now startable

#### Scenario: Top-level task closure is blocked by open nested checklist items
- **WHEN** `complete-task` attempts to close a top-level OpenSpec task
- **AND** any nested checklist item under that task is still unchecked
- **THEN** the top-level task is not closed
- **AND** the workflow reports that nested checklist closure is required first

### Requirement: Feature completion is distinct from branch finalization
Finishing a task or feature SHALL remain separate from final branch/worktree cleanup decisions.

#### Scenario: Finish-feature owns the transition into done
- **WHEN** a feature satisfies its feature-level acceptance bar
- **AND** `finish-feature` verifies the linked OpenSpec change and archive requirements
- **THEN** `finish-feature` moves the feature to `[DONE]`
- **AND** branch/worktree finalization remains a separate downstream action

### Requirement: Branch finalization requires archived OpenSpec change state
Feature branch finalization SHALL be gated on linked OpenSpec validation and archive state.

#### Scenario: Workflow finishes a done feature
- **WHEN** a feature in `[DONE]` is handed off for branch finalization
- **THEN** the workflow first validates the linked OpenSpec change
- **AND** it archives that change
- **AND** `openspec/changes/<change-id>/` no longer exists
- **AND** exactly one `openspec/changes/archive/*-<change-id>/` directory exists before branch finalization continues

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

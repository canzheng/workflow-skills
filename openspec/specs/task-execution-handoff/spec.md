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
- **AND** `start-task` resolves that later task from the reusable feature worktree rather than a stale primary checkout
- **AND** that worktree is clean before the next task begins

#### Scenario: Autonomous continuation reuses the same feature worktree
- **WHEN** autonomous orchestration continues execution for an already-active feature
- **THEN** it resolves the feature-scoped audit and task selection from the reusable feature worktree
- **AND** it does not silently fall back to a stale primary checkout while that feature worktree still exists

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

### Requirement: Autonomous orchestration routes completion through finish-feature
Autonomous workflow guidance SHALL preserve the same feature-completion gate used by the manual workflow.

#### Scenario: Autonomous loop completes the final task for a feature
- **WHEN** autonomous orchestration finishes the final top-level task for a feature
- **THEN** the feature remains `[IN_PROGRESS]`
- **AND** the next workflow handoff is `finish-feature`
- **AND** downstream branch or worktree cleanup does not occur until `finish-feature` has satisfied its validate-and-archive gate

### Requirement: Top-level task closure requires closed nested checklist items
`complete-task` SHALL refuse to close a top-level OpenSpec task while any nested checklist item under that task remains unchecked.

#### Scenario: Nested implementation detail remains open
- **WHEN** `complete-task` is asked to close a top-level OpenSpec task
- **AND** at least one nested checklist item under that task is still unchecked
- **THEN** the top-level task is not marked done
- **AND** the workflow reports that the task closure preconditions are not yet satisfied

### Requirement: Task-completion resolver ignores unrelated legacy-exempt completed features
Repository-wide task-completion resolution SHALL tolerate historical completed features that are explicitly marked `legacy-exempt`.

#### Scenario: Complete-task scans a migrated repository
- **WHEN** `complete-task` scans promoted feature files to find the active `in_progress` task
- **AND** a different feature is already in `[DONE]`
- **AND** that completed feature records `OpenSpec Status` as `legacy-exempt`
- **THEN** the completed feature is treated as historical metadata during the scan
- **AND** `complete-task` does not require that feature to record `OpenSpec Change`
- **AND** the resolver continues to locate and validate the actual active task normally

### Requirement: Automated task selection honors manual execution gates
Automated workflow task selection SHALL honor the same task eligibility rules used by manual execution entrypoints.

#### Scenario: Autonomous loop selects executable work
- **WHEN** autonomous orchestration proposes a task from an active feature
- **THEN** the feature has valid OpenSpec linkage
- **AND** the selected task is honestly executable under the shared readiness rules
- **AND** the active feature does not carry unresolved readiness drift

#### Scenario: Autonomous loop encounters malformed active work
- **WHEN** an active `[READY]` or `[IN_PROGRESS]` feature is missing linkage or carries readiness drift
- **THEN** autonomous orchestration stops with a workflow error
- **AND** it does not return `run_task_loop` for that malformed state

### Requirement: Task execution plans expose proof obligations before code execution
Workflow task execution SHALL require each task-scoped implementation plan to expose the contract surface and proof obligations that execution is expected to satisfy.

#### Scenario: Start-task validates implementation-plan proof structure
- **WHEN** `start-task` selects a top-level OpenSpec task for execution
- **THEN** the linked implementation plan records the task's contract surface and proof obligations
- **AND** the plan records the required validation classes for that task before code execution begins
- **AND** `start-task` refuses to continue when those sections are missing or empty

### Requirement: Task execution plans declare when unit-only proof is acceptable
Workflow task execution SHALL not silently treat narrow helper-level checks as sufficient proof for broader behavioral work.

#### Scenario: Behavioral task requires runtime-facing validation coverage
- **WHEN** a task implementation plan declares behavioral, orchestration, persistence, repair, or prompt-interface change surface
- **THEN** the plan records at least one runtime-facing validation class such as integration, runtime-path, or manual artifact inspection
- **AND** the workflow rejects a unit-only validation plan unless the plan includes an explicit unit-only justification

#### Scenario: Start-task rejects known anti-surrogate proof patterns
- **WHEN** a task implementation plan proposes helper-only proof for orchestration behavior, file-presence proof for structured assets, bookkeeping-only proof for repair behavior, or isolated helper proof without execution-path coverage
- **THEN** `start-task` does not treat that plan as sufficient execution proof
- **AND** the workflow requires the plan to add a matching runtime-facing validation class or an explicit narrowed-scope justification

### Requirement: Completion gates reuse the same proof-plan contract
Task completion SHALL require the active task's implementation plan to remain valid under the same proof-structure rules enforced at task start.

#### Scenario: Complete-task validates the active plan before closure
- **WHEN** `complete-task` resolves the active top-level task
- **THEN** it verifies that the linked implementation plan still exposes contract surface, proof obligations, and validation classes
- **AND** it refuses task closure when the active plan no longer satisfies that structure

### Requirement: Completion reconciles proof obligations to categorized evidence
Task completion SHALL reconcile declared proof obligations to categorized validation evidence before closure is accepted.

#### Scenario: Complete-task checks obligation-aware evidence
- **WHEN** `complete-task` closes an active top-level task
- **THEN** the recorded evidence covers each declared proof obligation with one or more evidence categories such as `schema`, `runtime_path`, `artifact_repair`, `prompt_contract`, `orchestration`, or `negative_case`
- **AND** completion does not treat uncategorized or unrelated passing checks as sufficient proof for uncovered obligations

### Requirement: Test changes are reviewed for contract narrowing
Workflow execution review SHALL treat test changes as potential contract-surface changes rather than as neutral implementation detail by default.

#### Scenario: Task modifies tests alongside implementation
- **WHEN** a task adds or modifies tests
- **THEN** the execution review asks whether those assertions narrow the contract relative to the task plan
- **AND** the review compares the changed tests to the declared proof obligations, not only to the current implementation

### Requirement: Task execution records validation evidence as it is produced
Workflow task execution SHALL record validation evidence while the task is being worked, rather than leaving evidence capture to task closure alone.

#### Scenario: Execution records a completed validation step
- **WHEN** task execution finishes a planned validation step such as a test run, inspection, or runtime-path check
- **THEN** the workflow appends the step's command or inspection, result, and evidence categories to the active feature file's validation log before execution moves on
- **AND** that recorded evidence becomes part of the task handoff into `complete-task`

#### Scenario: Complete-task reconciles previously recorded execution evidence
- **WHEN** `complete-task` closes the active task
- **THEN** it consumes the evidence already recorded during execution
- **AND** it treats reconciliation as a closure gate rather than as the primary moment when evidence is first authored


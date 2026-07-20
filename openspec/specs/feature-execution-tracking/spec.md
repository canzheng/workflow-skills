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
- **AND** task definitions and checkbox completion state remain in OpenSpec
- **AND** any optional `Depends On` references are interpreted through the workflow's markdown dependency convention rather than a native OpenSpec task model

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

#### Scenario: Invalid subtask identifier is rejected
- **WHEN** a feature file records `Current Task` as a nested subtask identifier such as `1.1`
- **THEN** workflow validation rejects that value as invalid metadata
- **AND** the repository must repair the feature file before execution continues

### Requirement: Feature files carry structured review verdict state
Feature execution records SHALL preserve machine-readable review verdicts for workflow gates that currently depend on approval outcomes.

#### Scenario: Workflow stages emit the canonical review-verdict lines they own
- **WHEN** `ready-feature` or `complete-task` passes through a required review gate
- **THEN** that stage writes the canonical `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal` lines into the relevant handoff-note entry
- **AND** downstream workflow behavior does not depend on operators reconstructing approval state from prose-only summary notes

#### Scenario: Downstream workflow consumes emitted structured verdict state
- **WHEN** downstream workflow logic needs the result of a readiness or task-completion review gate
- **THEN** it can read the emitted canonical review-verdict lines as structured state
- **AND** the runtime path is covered by at least one regression test

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

### Requirement: Historical legacy-exempt metadata remains valid during resolver scans
Historical completed-feature exemptions SHALL remain valid when repository-wide workflow resolvers inspect promoted feature files.

#### Scenario: Resolver inspects completed migrated feature metadata
- **WHEN** a workflow resolver reads a promoted feature in `[DONE]`
- **AND** that feature records `OpenSpec Status` as `legacy-exempt`
- **THEN** the resolver treats the feature as a valid historical completed record
- **AND** it does not require `OpenSpec Change` metadata unless the feature is being processed under an active-state rule

### Requirement: Task evidence guidance follows explicit proof obligations
Feature execution records SHALL treat validation evidence as proof against explicit obligations rather than as an unstructured collection of passing checks.

#### Scenario: Completion guidance records obligation-aware evidence
- **WHEN** workflow guidance records task validation evidence in a feature file
- **THEN** that guidance ties the evidence back to the active task's declared proof obligations
- **AND** it distinguishes between helper-level checks and broader runtime-facing validation classes when both exist

### Requirement: Workflow records evidence using a shared validation taxonomy
Feature execution records SHALL use a shared validation taxonomy so proof categories remain comparable across tasks and reviews.

#### Scenario: Task evidence names validation categories
- **WHEN** workflow guidance records task evidence
- **THEN** the evidence categories distinguish helper proof, schema proof, composed runtime proof, persistence proof, negative-path proof, and manual inspection proof
- **AND** the recorded evidence makes it clear which category each proof item satisfies

### Requirement: Feature files act as the running evidence ledger for task execution
Feature execution records SHALL be updated during execution so the validation log reflects completed proof steps as they occur.

#### Scenario: Validation log is updated during execution
- **WHEN** a task execution step produces proof such as a passing command, an inspection result, or a categorized negative-path check
- **THEN** the feature file records that proof in the validation log under the active task
- **AND** the record includes the exact run or inspection step, the result, and the relevant evidence categories

#### Scenario: Completion reuses the execution-time evidence ledger
- **WHEN** the workflow later evaluates task closure
- **THEN** the feature file already contains the evidence ledger built during execution
- **AND** completion guidance does not depend on reconstructing the task's proof surface from memory at the end

### Requirement: The completion_handoff payload schema is discoverable from the owning skill contract

The `complete-task` SKILL.md contract SHALL name the canonical `completion_handoff` payload fields directly, so operators can understand the downstream continuation contract without cross-referencing the workflow reference.

#### Scenario: Operator reads complete-task contract

- **WHEN** an operator reads `skills/complete-task/SKILL.md`
- **THEN** the contract lists the canonical payload fields — `action`, `target_feature_id`, `target_task_id`, `reason`, and `requires_human_decision` — and their permitted `action` values (`start_task`, `finish_feature`, `stop`)
- **AND** the contract cross-references the authoritative schema in `docs/planning/WORKFLOW_REFERENCE.md` without requiring the operator to jump there to learn the field names


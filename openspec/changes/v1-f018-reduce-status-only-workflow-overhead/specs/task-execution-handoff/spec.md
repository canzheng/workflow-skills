## MODIFIED Requirements

### Requirement: Task completion leaves a clean handoff
Completing a task SHALL leave the feature ready for the next handoff.

#### Scenario: Final task completion can continue without a status-only relay turn
- **WHEN** `complete-task` finishes the final top-level task for a feature
- **AND** all required task-level gates have passed
- **THEN** the workflow produces a deterministic machine-readable next-step result for `finish-feature`
- **AND** wrappers such as `autonomous-backlog-loop` may continue directly to that step without requiring a separate status-only relay turn

### Requirement: Task completion makes the finish-feature handoff explicit
Completing the active task SHALL make it explicit whether the feature still has more task work remaining or is now ready for `finish-feature`.

#### Scenario: Non-final task completion can continue directly to the next ready task
- **WHEN** `complete-task` finishes the active task
- **AND** another top-level task is already `ready`
- **THEN** the workflow produces a deterministic machine-readable next-step result for that ready task
- **AND** wrappers may continue directly to that task on the same feature worktree when no unresolved decision remains

### Requirement: Automated task selection honors manual execution gates
Automated workflow task selection SHALL honor the same task eligibility rules used by manual execution entrypoints.

#### Scenario: Selected-feature continuation reports unrelated drift without blocking
- **WHEN** execution is already continuing a selected feature on its intended worktree
- **AND** a different active feature has malformed linkage or readiness drift
- **THEN** the selected feature still blocks on its own workflow integrity rules
- **AND** the unrelated drift is surfaced as diagnostic workflow information rather than a selected-feature stop condition

#### Scenario: Autonomous continuation stays inside one feature-scoped agent for relay-only transitions
- **WHEN** `autonomous-backlog-loop` finishes a task and the next workflow step is already determined
- **THEN** it may keep the continuation inside the same feature-scoped agent
- **AND** it does not require a new outer-step relay turn solely to restate the deterministic next workflow action

## MODIFIED Requirements

### Requirement: Task completion leaves a clean handoff
Completing a task SHALL leave the feature ready for the next handoff.

#### Scenario: Completion exposes a canonical continuation payload
- **WHEN** `complete-task` finishes evaluating the active task handoff
- **THEN** it emits one canonical continuation object with fields `action`, `target_feature_id`, `target_task_id`, `reason`, and `requires_human_decision`
- **AND** `action` is one of `start_task`, `finish_feature`, or `stop`
- **AND** `target_task_id` is null unless `action` is `start_task`
- **AND** wrappers rely on that object instead of inferring continuation from prose-only handoff notes

#### Scenario: Final task completion can continue without a status-only relay turn
- **WHEN** `complete-task` finishes the final top-level task for a feature
- **AND** all required task-level gates have passed
- **THEN** the workflow produces a continuation object with `action=finish_feature`, `target_feature_id=<feature-id>`, `target_task_id=null`, `reason=all_tasks_complete`, and `requires_human_decision=false`
- **AND** wrappers such as `autonomous-backlog-loop` may continue directly to that step without requiring a separate status-only relay turn

### Requirement: Task completion makes the finish-feature handoff explicit
Completing the active task SHALL make it explicit whether the feature still has more task work remaining or is now ready for `finish-feature`.

#### Scenario: Non-final task completion can continue directly to the next ready task
- **WHEN** `complete-task` finishes the active task
- **AND** another top-level task is already `ready`
- **THEN** the workflow produces a continuation object with `action=start_task`, `target_feature_id=<feature-id>`, `target_task_id=<ready-task-id>`, `reason=next_ready_task`, and `requires_human_decision=false`
- **AND** wrappers may continue directly to that task on the same feature worktree when no unresolved decision remains

#### Scenario: Completion stops when continuation is not yet determined
- **WHEN** `complete-task` finishes the active task
- **AND** downstream continuation depends on unresolved human or workflow judgment
- **THEN** the workflow produces a continuation object with `action=stop`
- **AND** it sets `requires_human_decision=true`
- **AND** `reason` explains why direct continuation is not yet safe

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

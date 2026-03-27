## ADDED Requirements

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

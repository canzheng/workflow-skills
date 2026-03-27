## ADDED Requirements

### Requirement: Workflow audit validates current-task metadata shape
The workflow audit SHALL validate that `Current Task` metadata matches the documented task-ID contract.

#### Scenario: Audit checks current-task metadata
- **WHEN** the workflow audit inspects a feature file with `Current Task` set
- **THEN** it accepts `none` and top-level OpenSpec task IDs
- **AND** it rejects nested subtask identifiers such as `1.1`

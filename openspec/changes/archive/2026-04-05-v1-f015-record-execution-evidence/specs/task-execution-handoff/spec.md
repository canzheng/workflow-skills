## ADDED Requirements

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

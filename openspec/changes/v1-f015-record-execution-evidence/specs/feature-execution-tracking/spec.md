## ADDED Requirements

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

## ADDED Requirements

### Requirement: Task-completion resolver ignores unrelated legacy-exempt completed features
Repository-wide task-completion resolution SHALL tolerate historical completed features that are explicitly marked `legacy-exempt`.

#### Scenario: Complete-task scans a migrated repository
- **WHEN** `complete-task` scans promoted feature files to find the active `in_progress` task
- **AND** a different feature is already in `[DONE]`
- **AND** that completed feature records `OpenSpec Status` as `legacy-exempt`
- **THEN** the completed feature is treated as historical metadata during the scan
- **AND** `complete-task` does not require that feature to record `OpenSpec Change`
- **AND** the resolver continues to locate and validate the actual active task normally

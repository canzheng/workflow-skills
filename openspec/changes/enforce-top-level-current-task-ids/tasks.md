- [ ] 1 Shared Validation
  - [ ] 1.1 Enforce that `Current Task` is either `none` or a top-level OpenSpec task ID
  - [ ] 1.2 Keep task-state parsing and resolver behavior unchanged for valid top-level IDs

- [ ] 2 Workflow Reporting
  - [ ] 2.1 Make audit-workflow reject invalid subtask-style `Current Task` values
  - [ ] 2.2 Make diagnose-workflow report invalid `Current Task` values clearly

- [ ] 3 Coverage
  - [ ] 3.1 Add helper-level tests for valid and invalid `Current Task` values
  - [ ] 3.2 Add workflow-fixture tests proving `1.1`-style values are rejected

## 1. Enforce implementation-plan proof structure

- [x] 1 Enforce implementation-plan proof structure in execution helpers
  - [x] 1.1 Add shared workflow-state helpers to parse and validate task implementation plans
  - [x] 1.2 Fail `start-task` and `complete-task` resolution when the linked implementation plan lacks required proof-coverage sections
  - [x] 1.3 Update workflow tests and fixture plan writers to use the stronger implementation-plan contract

## 2. Align shaping and readiness guidance

- [ ] 2 Align shaping and readiness guidance around explicit proof obligations
  - [ ] 2.1 Update `shape-backlog-item` and `ready-feature` to require explicit proof-obligation capture for executable tasks
  - [ ] 2.2 Update `start-task`, `complete-task`, and the workflow reference so execution and evidence guidance match the new proof-coverage contract

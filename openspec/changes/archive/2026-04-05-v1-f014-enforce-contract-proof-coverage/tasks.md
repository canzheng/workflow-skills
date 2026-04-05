## 1. Enforce implementation-plan proof structure

- [x] 1 Enforce implementation-plan proof structure in execution helpers
  - [x] 1.1 Add shared workflow-state helpers to parse and validate task implementation plans
  - [x] 1.2 Fail `start-task` and `complete-task` resolution when the linked implementation plan lacks required proof-coverage sections
  - [x] 1.3 Update workflow tests and fixture plan writers to use the stronger implementation-plan contract

## 2. Align shaping, readiness, and reference guidance

- [x] 2 Align shaping, readiness, and workflow-reference guidance around explicit proof obligations
  - [x] 2.1 Update `shape-backlog-item` and `ready-feature` to require explicit proof-obligation capture and contract-ready proof coverage for executable tasks
  - [x] 2.2 Update `start-task`, `complete-task`, the feature template, and `docs/planning/WORKFLOW_REFERENCE.md` so execution and evidence guidance use the same proof-obligation contract and validation taxonomy

## 3. Reconcile completion evidence to obligations

- [x] 3 Make completion reconcile obligations to categorized evidence
  - [x] 3.1 Extend workflow evidence guidance and supporting helpers/templates to record evidence categories such as `schema`, `runtime_path`, `artifact_repair`, `prompt_contract`, `orchestration`, and `negative_case`
  - [x] 3.2 Update `complete-task` and focused tests so task closure checks obligation-aware evidence instead of accepting unrelated narrow proof

## 4. Harden review and fixture strategy against contract narrowing

- [x] 4 Prevent review and test fixtures from normalizing weaker local contracts
  - [x] 4.1 Add the mandatory “changed tests narrowed contract?” review question to the task-execution workflow guidance
  - [x] 4.2 Update fixture guidance and targeted tests to prefer canonical end-to-end fixtures when workflow contract behavior is under test

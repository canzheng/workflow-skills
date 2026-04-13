## 1. Contract And Metadata

- [x] 1 Update the workflow docs and stable specs so status-only continuation, structured review verdicts, and selected-feature execution scoping are part of the accepted workflow contract
  - [x] 1.1 Update `docs/planning/WORKFLOW_REFERENCE.md` and any affected feature-file guidance so deterministic next-step continuation and structured review verdict state are documented canonically
  - [x] 1.2 Update the stable specs for `task-execution-handoff`, `feature-execution-tracking`, and `workflow-audit-and-repair` to reflect the new continuation and scoping behavior

## 2. Resolver And Workflow-State Changes

- [x] 2 Update the workflow helpers and resolver scripts so selected-feature execution can continue deterministically without status-only relay turns
  - [x] 2.1 Extend `complete-task` handoff data so callers can deterministically continue to the next ready task or `finish-feature`
  - [x] 2.2 Persist structured review verdict state in the feature-file execution metadata and expose it through workflow helpers where needed
  - [x] 2.3 Tighten `start-task`, `complete-task`, and `finish-feature` resolver behavior so selected-feature continuation uses the intended worktree and is not blocked by unrelated malformed sibling features

## 3. Autonomous Loop Integration

- [x] 3 Update `autonomous-backlog-loop` so it consumes the new continuation contract and keeps feature-local relay-only transitions inside the same feature-scoped agent
  - [x] 3.1 Add `autonomous-backlog-loop` to the change surface for final-task continuation so autonomous execution does not stop at a status-only `finish-feature` handoff
  - [x] 3.2 Reduce outer-step or subagent lifecycle churn for feature-local continuation when no human decision is needed

## 4. Validation

- [ ] 4 Add the narrowest relevant tests and workflow checks for deterministic continuation, structured review verdicts, selected-feature scoping, and autonomous-loop reuse
  - [ ] 4.1 Add or update integration coverage for final-task continuation into `finish-feature` and non-final continuation into the next ready task
  - [ ] 4.2 Add or update contract coverage for structured review verdict state and feature-scoped resolver behavior
  - [ ] 4.3 Run the narrow workflow validation needed for the shaped change, including `audit-workflow`, `git diff --check`, and any affected repo tests

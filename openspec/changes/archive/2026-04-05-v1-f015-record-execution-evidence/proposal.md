## Why

The workflow now requires explicit proof obligations and categorized completion evidence, but the execution path still tends to produce that evidence first and record it later. That keeps `complete-task` doing some retroactive evidence capture instead of only reconciling an evidence ledger that was already built during execution.

## What Changes

- Require task execution guidance to record validation evidence in the feature file as each planned validation step completes, rather than waiting until task closure.
- Add a small shared helper for appending task-scoped validation entries in the expected feature-file format so execution can record evidence consistently.
- Clarify in workflow docs and templates that `start-task` / execution owns evidence capture while `complete-task` owns reconciliation against the task plan.
- Add focused tests for the evidence-recording helper and for the updated execution guidance where appropriate.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `task-execution-handoff`: execution now records validation evidence while the task is being worked, not only at closure time.
- `feature-execution-tracking`: feature files now act as the running evidence ledger for task execution, with `complete-task` consuming that ledger rather than inventing it at the end.

## Impact

- Affected code: shared workflow helpers for feature-file evidence updates, plus workflow guidance for `start-task`.
- Affected docs: feature template and workflow reference wording about when evidence is recorded.
- Affected tests: focused helper and workflow integration coverage for execution-time evidence recording.

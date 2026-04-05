## Context

`start-task` already requires an implementation plan with proof obligations and validation classes, and `complete-task` now checks that recorded evidence matches that plan. The remaining weakness is ownership timing: execution produces validation results, but the workflow does not clearly require those results to be recorded as they happen. That encourages retroactive summary instead of contemporaneous evidence capture.

## Goals / Non-Goals

**Goals:**

- Make execution-time evidence recording an explicit part of task execution.
- Keep the evidence format aligned with the existing feature-file validation log structure.
- Keep `complete-task` focused on reconciliation and closure, not on reconstructing missing evidence from memory.
- Provide a minimal helper so evidence recording is easy and consistent during execution.

**Non-Goals:**

- Build a fully automatic runtime logger for all task work.
- Add a new standalone evidence file format outside the feature file.
- Infer exact timestamps for when each validation step originally happened from outside the workflow.

## Decisions

### Decision: execution owns evidence recording, completion owns reconciliation

The workflow will explicitly state that validation evidence should be appended to the feature file as execution completes each planned validation step. `complete-task` remains responsible for checking that the evidence ledger is sufficient for closure.

### Decision: add a small shared helper for appending validation log entries

Rather than relying on every caller to rewrite Markdown blocks safely, the workflow will expose a helper that appends a task-scoped `Run` / `Result` / `Evidence` entry to the feature file's validation log.

### Decision: keep the feature-file format stable

The evidence helper will write entries that match the existing feature template, so no new storage model is needed. This keeps the change small and avoids churning the current completion parser more than necessary.

## Risks / Trade-offs

- Execution guidance may still rely on discipline rather than a fully automatic recorder. Mitigation: make the helper easy to call and make the ownership boundary explicit in docs and tests.
- Feature-file validation logs can grow quickly during larger tasks. Mitigation: keep entries concise and task-scoped.

## Migration Plan

1. Add a shared helper for appending validation entries to a feature file.
2. Update `start-task` guidance and workflow docs so execution records evidence as planned validation steps complete.
3. Add focused tests for the helper and any updated integration expectations.

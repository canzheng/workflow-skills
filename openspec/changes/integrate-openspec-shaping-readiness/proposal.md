## Why

The current workflow has strong structural audit coverage for board state, task state, and handoff cleanliness, but it does not provide a canonical behavior-spec layer or any systematic check that shaping outputs are semantically consistent. Making OpenSpec mandatory for this workflow gives the system a durable spec/change authority without replacing the existing release board and execution controls.

## What Changes

- Make OpenSpec a required part of workflow initialization and an assumed dependency of the workflow skills.
- Add an OpenSpec integration contract that maps one promoted feature to one OpenSpec change during shaping, readiness, execution, and archive work.
- Modify shaping and readiness expectations so `[SHAPING]` and `[READY]` are justified by linked OpenSpec artifacts rather than long-form design and plan prose in the feature file.
- Reduce feature files to execution metadata, validation evidence, and links to the authoritative OpenSpec change and affected specs.
- Make OpenSpec `tasks.md` the authoritative task definition and task-status ledger for execution.
- Extend workflow audit and task resolution to validate required OpenSpec links, readiness prerequisites, and OpenSpec task-state invariants structurally.

## Capabilities

### New Capabilities
- `openspec-change-integration`: Defines how promoted workflow features link to OpenSpec changes and how those linked artifacts justify shaping and readiness transitions.

### Modified Capabilities
- `workflow-board-lifecycle`: Change `[SHAPING]` and `[READY]` gates to depend on a linked OpenSpec change and its artifacts.
- `feature-execution-tracking`: Change feature files from mixed planning-plus-execution documents into thin execution records with OpenSpec links and validation evidence only.
- `workflow-audit-and-repair`: Extend audit and repair expectations to cover OpenSpec linkage and readiness prerequisites.
- `task-execution-handoff`: Move task selection and task-status updates to linked OpenSpec tasks instead of feature-file task sections.

## Impact

- Affected skills: `shape-backlog-item`, `ready-feature`, `start-task`, `complete-task`, `audit-workflow`, `repair-drift`, and `initialize-workflow-artifacts`
- Affected helpers/tests: workflow audit/task parsing helpers, task resolution scripts, and tests under `skills/_workflow/tests/`
- Affected planning artifacts: feature-file template and workflow contract language

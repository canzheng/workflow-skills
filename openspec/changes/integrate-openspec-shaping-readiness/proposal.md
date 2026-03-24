## Why

The current workflow has strong structural audit coverage for board state, task state, and handoff cleanliness, but it does not provide a canonical behavior-spec layer or any systematic check that shaping outputs are semantically consistent. Introducing OpenSpec for shaping and readiness gives the workflow a durable spec/change authority without replacing the existing release board and execution controls.

## What Changes

- Add an OpenSpec integration contract that maps one promoted feature to one OpenSpec change during shaping and readiness work.
- Modify shaping and readiness expectations so `[SHAPING]` and `[READY]` are justified by linked OpenSpec artifacts rather than long-form design and plan prose in the feature file.
- Reduce feature files to execution metadata, task progress, validation evidence, and links to the authoritative OpenSpec change and affected specs.
- Extend workflow audit to verify the required OpenSpec links and readiness prerequisites for features that depend on OpenSpec-backed shaping.

## Capabilities

### New Capabilities
- `openspec-change-integration`: Defines how promoted workflow features link to OpenSpec changes and how those linked artifacts justify shaping and readiness transitions.

### Modified Capabilities
- `workflow-board-lifecycle`: Change `[SHAPING]` and `[READY]` gates to depend on a linked OpenSpec change and its artifacts.
- `feature-execution-tracking`: Change feature files from mixed planning-plus-execution documents into thin execution records with OpenSpec links.
- `workflow-audit-and-repair`: Extend audit and repair expectations to cover OpenSpec linkage and readiness prerequisites.

## Impact

- Affected skills: `shape-backlog-item`, `ready-feature`, `audit-workflow`, `repair-drift`, and likely `initialize-workflow-artifacts`
- Affected helpers/tests: workflow audit parser and tests under `skills/_workflow/tests/`
- Affected planning artifacts: feature-file template and workflow contract language

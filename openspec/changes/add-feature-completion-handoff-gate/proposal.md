## Why

The workflow says `complete-task` may move a feature to `[DONE]` once feature acceptance is satisfied, but there is no explicit enforcement or helper support for that last-task handoff. That leaves teams with a documented path to `finish-feature` that is easy to miss or handle inconsistently.

## What Changes

- Add explicit workflow support for deciding when a feature can move from `[IN_PROGRESS]` to `[DONE]` at task completion time.
- Define and document the feature-completion handoff that makes `finish-feature` startable after the final accepted task.
- Add resolver and test coverage for the “last task done but feature not yet completed” versus “feature ready for `[DONE]`” paths.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Task completion will explicitly cover the feature-completion handoff into `[DONE]`.
- `feature-execution-tracking`: Feature metadata and evidence rules will clarify what must be true before a feature leaves `[IN_PROGRESS]`.

## Impact

- Affected skills: `complete-task`, `finish-feature`
- Affected helpers/tests: task-completion and finish-feature resolvers, workflow integration tests
- Affected docs/specs: feature completion and handoff requirements

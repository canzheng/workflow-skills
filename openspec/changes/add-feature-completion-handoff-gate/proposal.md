## Why

The current workflow splits feature completion across two skills in a way that creates an awkward and error-prone state boundary. `complete-task` is documented as the place that may move a feature to `[DONE]`, but `finish-feature` owns OpenSpec validation and archive. That forces the workflow to choose between two bad states:

- leave the feature in `[IN_PROGRESS]`, which makes `finish-feature` reject it
- move the feature to `[DONE]` before OpenSpec validation/archive, which weakens the meaning of `[DONE]`

The workflow contract should instead make `finish-feature` the single owner of the terminal feature transition after acceptance has actually been proven.

## What Changes

- Keep `complete-task` responsible for closing tasks, recording evidence, and making the final-task handoff explicit, but not for moving a feature to `[DONE]`.
- Make `finish-feature` start from `[IN_PROGRESS]` and require that all top-level OpenSpec tasks are done and `Current Task` is `none`.
- Move the `[IN_PROGRESS] -> [DONE]` transition into `finish-feature`, after feature acceptance and OpenSpec validation/archive succeed.
- Require `complete-task` to verify that all nested checklist items under a top-level OpenSpec task are already closed before it marks that top-level task done.
- Add regression coverage for the new readiness boundary between `complete-task`, `audit-workflow`, and `finish-feature`.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: Task completion will explicitly hand off to `finish-feature` after the final task without moving the feature to `[DONE]`.
- `feature-execution-tracking`: Feature metadata and evidence rules will clarify what must be true before `finish-feature` may move a feature to `[DONE]`.

## Impact

- Affected skills: `complete-task`, `finish-feature`
- Affected helpers/tests: task-completion and finish-feature resolvers, workflow audit, workflow integration tests
- Affected docs/specs: feature completion and handoff requirements

## Why

The workflow already has lesson capture, promotion, retrieval, and usage-recording skills, but the task lifecycle does not name them as part of the canonical execution flow. That leaves lesson reuse optional and fragmented instead of being a consistent part of task start, task completion, and feature finalization.

## What Changes

- `start-task` retrieves relevant active lessons before implementation begins and records the returned lesson IDs in the feature file handoff state.
- `complete-task` reads the retrieved lesson IDs from the feature file, records whether each lesson was applied, partially applied, or not applied, and then captures any new high-value lesson candidates before the task closes.
- `finish-feature` promotes durable lessons after the linked OpenSpec change is validated and archived, before branch finalization.
- `refresh-lessons` remains explicitly user-triggered.
- The workflow reference and task lifecycle skills will name the lesson lifecycle canonically so the behavior is not only implied by the lesson skills themselves.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: task start, task completion, and feature handoff behavior now include lesson retrieval, usage reconciliation, and post-task lesson capture
- `feature-execution-tracking`: feature files now carry lesson handoff state between `start-task` and `complete-task`

## Impact

- `skills/start-task/SKILL.md`
- `skills/complete-task/SKILL.md`
- `skills/finish-feature/SKILL.md`
- `docs/planning/WORKFLOW_REFERENCE.md`
- `docs/planning/versions/v1/features/`
- `docs/lessons/lesson-candidates.md`
- `docs/lessons/lessons.md`

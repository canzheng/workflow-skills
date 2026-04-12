## Why

The workflow already has lesson retrieval, usage-recording, note-recording, and feature-final distillation behavior, but the task lifecycle does not name them as part of the canonical execution flow. That leaves lesson reuse optional and fragmented instead of being a consistent part of task start, task completion, and feature finalization.

## What Changes

- `start-task` retrieves relevant active lessons before implementation begins and records the returned lesson IDs in the feature file handoff state.
- `complete-task` reads the retrieved lesson IDs from the feature file, records whether each lesson was applied, partially applied, or not applied, and then records any high-signal observations in `docs/lessons/notes.md` before the task closes.
- `finish-feature` runs `distill-lessons` after the linked OpenSpec change is validated and archived, before branch finalization.
- `refresh-lessons` remains explicitly user-triggered.
- The workflow reference and task lifecycle skills will name the lesson lifecycle canonically so the behavior is not only implied by the lesson skills themselves.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `task-execution-handoff`: task start, task completion, and feature handoff behavior now include lesson retrieval, usage reconciliation, post-task note recording, and feature-final distillation
- `feature-execution-tracking`: feature files now carry lesson handoff state between `start-task` and `complete-task`

## Impact

- `skills/start-task/SKILL.md`
- `skills/complete-task/SKILL.md`
- `skills/finish-feature/SKILL.md`
- `docs/planning/WORKFLOW_REFERENCE.md`
- `docs/planning/versions/v1/features/`
- `docs/lessons/notes.md`
- `docs/lessons/lessons.md`

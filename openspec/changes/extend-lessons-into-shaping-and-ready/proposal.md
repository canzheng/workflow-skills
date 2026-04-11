## Why

Lessons already influence execution through `start-task`, `complete-task`, and `finish-feature`, but the workflow does not reuse that same learning earlier when shaping and readiness decisions are being made. That leaves avoidable design mistakes, weak proof obligations, and readiness ambiguity undiscovered until execution.

## What Changes

- Extend the lesson lifecycle so `shape-backlog-item` retrieves relevant active lessons before shaping is finalized, applies them to shaping decisions, records whether they materially influenced the stage, and captures new high-value planning lessons before exit.
- Extend the lesson lifecycle so `ready-feature` retrieves relevant active lessons before the independent readiness review, applies them to readiness judgment and contract-clarity checks, records whether they materially influenced the stage, and captures new high-value readiness lessons before exit.
- Reuse the existing feature-file handoff surface to persist planning-stage lesson retrieval and usage state instead of creating a separate planning-only lessons ledger.
- Keep `promote-lessons` at feature finalization and keep `refresh-lessons` explicitly user-triggered.
- Update the canonical workflow reference so lessons are part of shaping and readiness, not only task execution and feature completion.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `openspec-change-integration`: shaping and readiness contracts now include lesson-aware retrieval, usage recording, and post-stage lesson capture as part of the planning workflow around linked OpenSpec artifacts.
- `feature-execution-tracking`: feature files now preserve lesson retrieval and usage outcomes for planning stages in addition to execution-stage handoff state.
- `task-execution-handoff`: the end-to-end lesson lifecycle description now spans shaping, readiness, execution, and feature finish so the workflow names one canonical lesson flow instead of an execution-only subset.

## Impact

- `skills/shape-backlog-item/SKILL.md`
- `skills/ready-feature/SKILL.md`
- `docs/planning/WORKFLOW_REFERENCE.md`
- `openspec/specs/openspec-change-integration/spec.md`
- `openspec/specs/feature-execution-tracking/spec.md`
- `openspec/specs/task-execution-handoff/spec.md`
- No additional corresponding existing docs required content changes beyond the workflow metadata already updated in the feature file and backlog entry.

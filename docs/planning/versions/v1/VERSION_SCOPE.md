# V1 Scope

## Goal
- Finish adopting the workflow-owned planning and OpenSpec execution model for this repository so backlog state, task execution, validation evidence, OpenSpec archive flow, and branch handoff all follow one consistent contract.

## Exit Criteria
- All v1 workflow features are either `[DONE]` or explicitly moved to `[DEFER]`.
- The remaining review-gap cleanup in `v1-f010` is complete, leaving no placeholder or contradictory source-of-truth artifacts in the active workflow docs, planning files, or stable OpenSpec specs.
- `audit-workflow` passes for the active version and every `[DONE]` feature has exactly one archived linked OpenSpec change or an explicit `legacy-exempt` historical exemption.

## Explicit Deferrals
- None currently recorded.

## Cross-Feature Decisions
- OpenSpec is required for active shaped, ready, and in-progress features; `legacy-exempt` applies only to historical completed features from before OpenSpec adoption.
- Execution remains one top-level OpenSpec task at a time, with `Current Task` in the feature file as the active-task marker and `tasks.md` as the checkbox ledger.
- `finish-feature` owns the `[IN_PROGRESS] -> [DONE]` transition by validating and archiving the linked OpenSpec change before downstream branch finalization.
- Feature execution uses one reusable feature branch/worktree per active feature, kept outside the main repository directory.

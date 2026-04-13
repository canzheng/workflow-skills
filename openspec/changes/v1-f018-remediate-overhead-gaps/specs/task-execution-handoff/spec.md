## MODIFIED Requirements

### Requirement: Feature execution uses a dedicated reusable worktree

#### Scenario: Selected-feature continuation fails when the intended worktree is missing
- **WHEN** later task execution or autonomous continuation targets a selected feature already in `[IN_PROGRESS]`
- **AND** no unique active non-primary feature worktree can be resolved for that feature
- **THEN** the workflow stops with a worktree-resolution error
- **AND** it does not silently continue from the primary or current checkout

### Requirement: Task completion leaves a clean handoff

#### Scenario: Complete-task guidance follows the canonical continuation payload
- **WHEN** operator-facing workflow guidance describes the result of `complete-task`
- **THEN** it describes the canonical `completion_handoff` payload rather than a prose-only terminal handoff model
- **AND** it still makes clear that `complete-task` itself does not launch downstream task execution

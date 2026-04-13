## MODIFIED Requirements

### Requirement: Autonomous orchestration does not bypass workflow integrity checks

#### Scenario: Selected-feature helper fails closed on missing worktree
- **WHEN** an execution helper continues a selected feature by feature ID
- **AND** the helper cannot resolve a unique active feature worktree for that feature
- **THEN** it reports a workflow error
- **AND** it does not silently reuse the current checkout as a substitute for the missing feature worktree

## ADDED Requirements

### Requirement: Autonomous orchestration routes completion through finish-feature
Autonomous workflow guidance SHALL preserve the same feature-completion gate used by the manual workflow.

#### Scenario: Autonomous loop completes the final task for a feature
- **WHEN** autonomous orchestration finishes the final top-level task for a feature
- **THEN** the feature remains `[IN_PROGRESS]`
- **AND** the next workflow handoff is `finish-feature`
- **AND** downstream branch or worktree cleanup does not occur until `finish-feature` has satisfied its validate-and-archive gate

## MODIFIED Requirements

### Requirement: Autonomous orchestration does not bypass workflow integrity checks
Automation helpers SHALL not route around workflow integrity rules that manual wrappers enforce.

#### Scenario: Execution-scoped helpers block on selected-feature integrity
- **WHEN** an execution helper continues an already-selected feature
- **THEN** it enforces the same linkage, readiness, and worktree integrity rules for that selected feature as the manual workflow gate
- **AND** it does not silently continue malformed selected-feature work

#### Scenario: Execution-scoped helpers report unrelated active drift separately
- **WHEN** an execution helper continues a selected feature
- **AND** a different active feature has unrelated workflow drift
- **THEN** the helper surfaces that unrelated drift as diagnostic information
- **AND** direct `audit-workflow` remains the global pass/fail integrity gate for repo-wide repair or planning-state edits

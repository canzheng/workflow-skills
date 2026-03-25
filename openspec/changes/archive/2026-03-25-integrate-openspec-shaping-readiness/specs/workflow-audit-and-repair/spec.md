## MODIFIED Requirements

### Requirement: Workflow audit validates structural planning invariants
The workflow audit SHALL verify the structural integrity of the active planning artifacts.

#### Scenario: Audit checks active planning structure
- **WHEN** the workflow audit runs
- **THEN** it verifies that `docs/planning/current_version` exists and is a symlink
- **AND** it verifies that the active `BACKLOG.md` uses the required workflow sections in canonical order
- **AND** it verifies that non-backlog feature entries link to existing feature files

#### Scenario: Audit checks OpenSpec links for promoted features
- **WHEN** the workflow audit inspects a feature outside `[BACKLOG]`
- **THEN** it verifies that the feature file records a linked OpenSpec change ID
- **AND** it verifies that the linked change directory exists

### Requirement: Workflow audit validates feature linkage consistency
The workflow audit SHALL confirm that backlog entries and feature files agree on identity and placement.

#### Scenario: Audit checks feature linkage metadata
- **WHEN** the workflow audit inspects a promoted feature
- **THEN** it verifies that the feature file’s `Feature ID` matches the backlog entry
- **AND** it verifies that the feature file’s `Backlog Reference` matches the owning backlog section
- **AND** it verifies that the feature file records linked OpenSpec capability specs for OpenSpec-backed shaping states

### Requirement: Workflow audit validates task readiness invariants
The workflow audit SHALL detect illegal task-readiness states.

#### Scenario: Audit checks task readiness and dependency integrity
- **WHEN** the workflow audit inspects workflow-derived task state for a promoted feature
- **THEN** it validates the optional `Depends On` references interpreted by the workflow dependency convention
- **AND** it detects tasks that are marked `ready` without satisfied workflow prerequisites
- **AND** it detects tasks that could be promoted to `ready` but remain stale
- **AND** it detects references to unknown dependency IDs
- **AND** it enforces that at most one repository task is `in_progress`

#### Scenario: Audit checks OpenSpec-backed ready prerequisites
- **WHEN** the workflow audit inspects a feature in `[READY]`
- **THEN** it verifies that the linked OpenSpec change includes `proposal.md`, `design.md`, and `tasks.md`

#### Scenario: Audit fails when mandatory OpenSpec structure is missing
- **WHEN** a repository adopts the workflow without the required `openspec/` structure
- **THEN** the workflow audit fails
- **AND** the failure identifies the missing OpenSpec prerequisite

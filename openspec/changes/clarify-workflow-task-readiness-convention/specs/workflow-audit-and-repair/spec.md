## MODIFIED Requirements

### Requirement: Workflow audit validates task readiness invariants
The workflow audit SHALL detect illegal workflow-derived task-readiness states.

#### Scenario: Audit checks task readiness and dependency integrity
- **WHEN** the workflow audit inspects workflow-derived task state for a promoted feature
- **THEN** it validates the optional `Depends On` references interpreted by the workflow task dependency convention
- **AND** it detects tasks that are marked `ready` without satisfied workflow prerequisites
- **AND** it detects tasks that could be promoted to `ready` but remain stale
- **AND** it detects references to unknown dependency IDs
- **AND** it enforces that at most one repository task is `in_progress`

#### Scenario: Audit rejects nested-only OpenSpec task structures
- **WHEN** a linked OpenSpec `tasks.md` contains nested checklist items for a task group
- **AND** the corresponding parent top-level checklist item is missing
- **THEN** the workflow audit fails
- **AND** it reports that the linked change does not expose a valid top-level executable task structure

#### Scenario: Audit checks OpenSpec-backed ready prerequisites
- **WHEN** the workflow audit inspects a feature in `[READY]`
- **THEN** it verifies that the linked OpenSpec change includes `proposal.md`, `design.md`, and `tasks.md`
- **AND** it verifies that the linked change exposes at least one valid top-level task that resolves to workflow status `ready`

#### Scenario: Audit fails when mandatory OpenSpec structure is missing
- **WHEN** a repository adopts the workflow without the required `openspec/` structure
- **THEN** the workflow audit fails
- **AND** the failure identifies the missing OpenSpec prerequisite

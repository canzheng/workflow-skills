## MODIFIED Requirements

### Requirement: Workflow audit validates task readiness invariants
The workflow audit SHALL detect illegal task-readiness states.

#### Scenario: Audit checks task readiness and dependency integrity
- **WHEN** the workflow audit inspects tasks in a feature file
- **THEN** it detects tasks that are marked `ready` without satisfied dependencies
- **AND** it detects tasks that could be promoted to `ready` but remain stale
- **AND** it detects references to unknown dependency IDs
- **AND** it enforces that at most one repository task is `in_progress`

#### Scenario: Audit accepts resolvable cross-feature dependencies
- **WHEN** a task depends on another feature's task by feature-qualified ID
- **AND** the referenced task can be resolved from the active feature state or the archived change for that completed feature
- **THEN** the dependency is treated as valid input to readiness evaluation
- **AND** the audit does not report that dependency as unknown drift

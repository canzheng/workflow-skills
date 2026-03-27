## Purpose
Define what workflow audit and repair guarantee for the planning system, and clearly separate workflow integrity checks from semantic behavior validation.
## Requirements
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

### Requirement: Workflow repair is minimal and truth-preserving
Drift repair SHALL restore workflow consistency without silently redefining intended product behavior.

#### Scenario: Repair addresses a concrete structural inconsistency
- **WHEN** workflow drift is repaired
- **THEN** the repair changes only the minimum artifact content needed to restore consistency
- **AND** it stops if the intended source of truth is ambiguous

### Requirement: Workflow audit does not substitute for semantic spec validation
Workflow audit scope SHALL remain distinct from semantic behavior validation.

#### Scenario: Audit passes while semantic contradictions remain possible
- **WHEN** workflow audit completes successfully
- **THEN** the result guarantees workflow-state consistency
- **AND** it does not, by itself, prove that design intent, product behavior, or separate behavior specifications are semantically consistent

### Requirement: Workflow audit validates active OpenSpec change requirements
The workflow audit SHALL keep active OpenSpec change requirements for non-completed active work.

#### Scenario: Audit checks active change linkage for shaping and execution states
- **WHEN** the workflow audit inspects a feature in `[SHAPING]`, `[READY]`, or `[IN_PROGRESS]`
- **THEN** it verifies that the feature file records a linked OpenSpec change ID
- **AND** it verifies that `openspec/changes/<change-id>/` exists

#### Scenario: Audit rejects orphan active changes
- **WHEN** an active change exists under `openspec/changes/`
- **AND** no promoted feature links to that change ID
- **THEN** the workflow audit fails
- **AND** it reports the orphaned change ID so the board and feature state can be repaired

### Requirement: Workflow audit validates current-task metadata shape
The workflow audit SHALL validate that `Current Task` metadata matches the documented task-ID contract.

#### Scenario: Audit checks current-task metadata
- **WHEN** the workflow audit inspects a feature file with `Current Task` set
- **THEN** it accepts `none` and top-level OpenSpec task IDs
- **AND** it rejects nested subtask identifiers such as `1.1`

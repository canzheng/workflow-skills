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

#### Scenario: Automation evaluates active work
- **WHEN** an automation helper decides whether active work is eligible to continue
- **THEN** it uses the same linkage and readiness integrity rules as the manual workflow gate
- **AND** malformed active work remains a blocking workflow issue rather than an eligible action

### Requirement: Workflow audit validates canonical board sections without extras
The workflow audit SHALL enforce the canonical workflow board shape rather than accepting extra sections outside the documented lifecycle.

#### Scenario: Audit rejects extra backlog sections
- **WHEN** the workflow audit runs on an active `BACKLOG.md`
- **THEN** it requires exactly the canonical workflow sections in order
- **AND** it rejects extra sections such as `[BLOCKED]`, even when they appear after `[DEFER]`

### Requirement: Workflow audit validates promoted-feature OpenSpec spec linkage
The workflow audit SHALL verify that promoted OpenSpec-backed features record linked stable spec paths as part of their workflow metadata.

#### Scenario: Audit rejects promoted feature missing linked stable specs
- **WHEN** the workflow audit inspects a promoted feature that is not `legacy-exempt`
- **THEN** it requires the feature file to record at least one linked path under `openspec/specs/`
- **AND** it reports a workflow error when that metadata is missing

### Requirement: Workflow diagnosis surfaces structural workflow defects
The read-only workflow diagnosis SHALL report structural workflow issues even when it does not act as a hard gate.

#### Scenario: Diagnose reports malformed canonical board structure
- **WHEN** diagnosis inspects an active backlog with missing, out-of-order, or extra canonical sections
- **THEN** it emits a structured finding describing the board-shape defect
- **AND** it does not report the malformed repository as healthy

#### Scenario: Diagnose reports missing promoted-feature spec linkage
- **WHEN** diagnosis inspects a promoted feature that is missing linked stable OpenSpec spec paths
- **THEN** it emits a structured finding for the missing metadata
- **AND** the finding is visible in the per-repository health report

### Requirement: Workflow diagnosis reports missing planning scaffold as findings
The read-only workflow diagnosis SHALL report missing planning scaffold as structured findings instead of terminating with an uncaught exception.

#### Scenario: Diagnose handles missing current version
- **WHEN** diagnosis runs and `docs/planning/current_version` is missing
- **THEN** it emits a structured finding describing the missing scaffold
- **AND** it returns JSON output rather than a Python traceback

#### Scenario: Diagnose handles missing active backlog
- **WHEN** diagnosis resolves the active version but the linked `BACKLOG.md` is missing
- **THEN** it emits a structured finding describing the missing backlog
- **AND** it continues producing an operator-facing report

### Requirement: Workflow audit validates shaping artifact baseline
The workflow audit SHALL require shaped promoted work to retain the baseline authored OpenSpec artifacts created by `openspec-propose`.

#### Scenario: Audit rejects shaping feature missing baseline artifacts
- **WHEN** the workflow audit inspects a feature in `[SHAPING]`
- **THEN** it requires the linked OpenSpec change to contain `proposal.md`, `design.md`, and `tasks.md`
- **AND** it reports a workflow error when any of those files are missing

### Requirement: Workflow audit validates archived change state for completed features
The workflow audit SHALL treat archived linked-change state as the expected source of truth for completed post-adoption features.

#### Scenario: Audit checks completed feature archive resolution
- **WHEN** the workflow audit inspects a feature in `[DONE]` that is not marked `legacy-exempt`
- **THEN** it requires the linked OpenSpec change to be absent from `openspec/changes/<change-id>/`
- **AND** it requires exactly one matching directory under `openspec/changes/archive/*-<change-id>/`

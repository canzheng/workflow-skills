## ADDED Requirements

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

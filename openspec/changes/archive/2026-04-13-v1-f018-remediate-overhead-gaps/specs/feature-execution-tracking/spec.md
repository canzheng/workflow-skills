## MODIFIED Requirements

### Requirement: Feature files carry structured review verdict state
Feature execution records SHALL preserve machine-readable review verdicts for workflow gates that currently depend on approval outcomes.

#### Scenario: Workflow stages emit the canonical review-verdict lines they own
- **WHEN** `ready-feature` or `complete-task` passes through a required review gate
- **THEN** that stage writes the canonical `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal` lines into the relevant handoff-note entry
- **AND** downstream workflow behavior does not depend on operators reconstructing approval state from prose-only summary notes

#### Scenario: Downstream workflow consumes emitted structured verdict state
- **WHEN** downstream workflow logic needs the result of a readiness or task-completion review gate
- **THEN** it can read the emitted canonical review-verdict lines as structured state
- **AND** the runtime path is covered by at least one regression test

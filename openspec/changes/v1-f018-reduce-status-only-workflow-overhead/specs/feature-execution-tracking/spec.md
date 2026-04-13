## ADDED Requirements

### Requirement: Feature files carry structured review verdict state
Feature execution records SHALL preserve machine-readable review verdicts for workflow gates that currently depend on approval outcomes.

#### Scenario: Readiness review records a structured verdict
- **WHEN** `ready-feature` completes its independent readiness review
- **THEN** the feature file records the review scope, verdict state, and whether blocking findings remain
- **AND** that verdict can be consumed without parsing prose-only handoff notes

#### Scenario: Task-completion review records a structured verdict
- **WHEN** task execution or completion passes through a required review gate
- **THEN** the feature file records a structured verdict for that boundary
- **AND** downstream workflow steps can distinguish `approved`, `changes_requested`, and `blocked` outcomes without inferring them from summary text

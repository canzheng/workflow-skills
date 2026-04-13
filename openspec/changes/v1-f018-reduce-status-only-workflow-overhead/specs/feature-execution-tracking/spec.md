## ADDED Requirements

### Requirement: Feature files carry structured review verdict state
Feature execution records SHALL preserve machine-readable review verdicts for workflow gates that currently depend on approval outcomes.

#### Scenario: Feature file stores the verdict in canonical handoff-note fields
- **WHEN** a workflow stage or task emits a structured review verdict
- **THEN** the verdict is stored in the feature file `Handoff Notes` entry for that stage or task
- **AND** it uses canonical lines `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal`
- **AND** downstream tooling does not need to infer the verdict from prose-only summary notes

#### Scenario: Readiness review records a structured verdict
- **WHEN** `ready-feature` completes its independent readiness review
- **THEN** the feature file records `Review Scope: ready`
- **AND** it records `Review Target: <feature-id>`
- **AND** it records `Review Verdict: approved | changes_requested | blocked`
- **AND** it records `Blocking Findings: none | <comma-separated stable finding ids or labels>`
- **AND** it records `Review Terminal: true | false`
- **AND** that verdict can be consumed without parsing prose-only handoff notes

#### Scenario: Task-completion review records a structured verdict
- **WHEN** task execution or completion passes through a required review gate
- **THEN** the feature file records `Review Scope: task_execution` or `Review Scope: task_completion`
- **AND** it records `Review Target: <top-level-task-id>`
- **AND** it records `Review Verdict: approved | changes_requested | blocked`
- **AND** it records `Blocking Findings: none | <comma-separated stable finding ids or labels>`
- **AND** it records `Review Terminal: true | false`
- **AND** downstream workflow steps can distinguish `approved`, `changes_requested`, and `blocked` outcomes without inferring them from summary text

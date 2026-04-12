## ADDED Requirements

### Requirement: Shaping retrieves lessons before finalizing OpenSpec artifacts
Workflow-managed shaping SHALL retrieve relevant active lessons before finalizing the linked OpenSpec change for a promoted feature.

#### Scenario: Shape-backlog-item uses lessons to inform shaping output
- **WHEN** `shape-backlog-item` has read the selected backlog item and gathered the initial repository context
- **THEN** it retrieves relevant active lessons before finalizing feature splitting, linked documentation/spec surfaces, proof obligations, or validation intent
- **AND** the shaping output incorporates those lessons only when they materially improve the shaped contract

### Requirement: Ready-feature uses lessons before independent readiness review
Workflow-managed readiness SHALL retrieve relevant active lessons before the independent readiness review evaluates whether shaping is execution-ready.

#### Scenario: Ready-feature retrieves lessons before readiness judgment
- **WHEN** `ready-feature` has read the feature file and linked OpenSpec change and is preparing the independent readiness review
- **THEN** it retrieves relevant active lessons before the review decides whether the shaped contract is sufficiently clear
- **AND** those lessons may influence documentation consistency checks, acceptance-boundary review, proof-obligation clarity, and surrogate-proof risk judgment

### Requirement: Planning stages record lesson outcomes before exit
Workflow-managed shaping and readiness SHALL record lesson usage and record high-signal observations in `docs/lessons/notes.md` before the stage exits.

#### Scenario: Shape-backlog-item closes with lesson reconciliation
- **WHEN** `shape-backlog-item` completes its shaping work for a promoted feature
- **THEN** it records whether each retrieved lesson materially influenced the shaping decisions
- **AND** it records any reusable planning observations in `docs/lessons/notes.md` before the stage exits when shaping surfaced near-misses or fragile decisions worth distilling later

#### Scenario: Ready-feature closes with lesson reconciliation
- **WHEN** `ready-feature` finishes its readiness work for a shaped feature
- **THEN** it records whether each retrieved lesson materially influenced the readiness decision
- **AND** it records any reusable readiness observations in `docs/lessons/notes.md` before the stage exits when readiness surfaced near-misses or fragile decisions worth distilling later

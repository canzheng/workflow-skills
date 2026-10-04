# Workflow v2 delivery

## Purpose
Issue-level authorization, documentation and honest evidence obligations.

## Requirements
### Requirement: Native delivery ownership
GitHub Issues SHALL own shared delivery state and PRs SHALL index evidence. An open
workflow Issue SHALL have one phase plus supported modifiers; partial work SHALL use
non-closing references and SHALL NOT complete a parent from one child.

#### Scenario: Ambiguous source identity
- **WHEN** multiple open/closed Issues have the same source marker
- **THEN** creation stops for reconciliation rather than creating another Issue

### Requirement: Proportional execution and documentation
Authorized delivery SHALL inspect existing code/contracts, verify meaningful failure
paths, reassess documentation at start and final diff, and preserve discriminating
assertions. Ordinary work SHALL NOT require a task ledger, per-task plan or reviewer.

#### Scenario: New configuration with stale guidance
- **WHEN** configuration behavior changes and current setup guidance omits it
- **THEN** delivery remains unfinished until accurate defaults/errors/examples are maintained

#### Scenario: Repair preserves current explanation
- **WHEN** an internal repair restores the accurately documented contract
- **THEN** a reasoned no-document-change statement is permitted

### Requirement: Evidence and proportional change planning
Evidence SHALL identify tested revision/content/environment and distinguish unavailable
checks from passes. Significant change planning SHALL use one OpenSpec change-owned
plan; partial PRs SHALL NOT archive pending scope. Delivered SHALL require acceptance,
required verification/docs/archive/review and intended merge/release obligations.

#### Scenario: Local pass and open PR
- **WHEN** local tests pass but required Ubuntu verification or merge is absent
- **THEN** progress reports locally verified and integration pending, not delivered

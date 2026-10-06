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

### Requirement: Canonical PR review boundary
When PR publication is available, delivery SHALL keep the Issue in progress while
the canonical PR is draft and transition to review after that PR is Ready for Review.
Formal independent semantic review SHALL use the PR boundary rather than a mandatory
independent pre-PR Issue-stage pipeline. Branch-only review SHALL remain available
when publication is unavailable; approved cumulative rewrite bootstrap is an exception.

#### Scenario: Ready and draft transitions
- **WHEN** self-verification and documentation reassessment prepare a published result
- **THEN** the canonical PR becomes Ready for Review before the linked Issue enters review
- **AND** returning that PR to draft restores in progress without asserting completion

#### Scenario: Publication unavailable
- **WHEN** authorized implementation finishes but PR publication is unavailable
- **THEN** a committed reviewable branch and precise evidence can use the review fallback
- **AND** required integration, review and merge remain pending

### Requirement: One-shot initial design backlog
Design shaping SHALL treat one or more supplied existing design documents as the
durable intent source and produce the smallest coherent initial or MVP delivery-outcome
Issue batch in one run. Intermediate decomposition SHALL NOT require persistence.
Detailed scope/acceptance/dependencies SHALL be translated faithfully; high-level
intent SHALL receive proportional shaping with product choices surfaced explicitly.

#### Scenario: Fresh project batch and approval
- **WHEN** a fresh repository design includes MVP scope, later capabilities, direct dependencies and an unresolved decision
- **THEN** one shaping run prepares outcome Issues with design-section references and explicit prerequisites
- **AND** one batch approval enables specified dependency-ready work while affected unknown/dependent work stays backlog or blocked
- **AND** later scope stays unmaterialized or deliberately backlog, without coding-task Issues
- **AND** application implementation does not start unless separately requested

#### Scenario: Evolved design and human acceptance
- **WHEN** backlog generation is rerun after design changes
- **THEN** stable logical identities reuse open or closed matches without silent reopening
- **AND** human edits and contradictory acceptance are preserved for reconciliation
- **AND** genuinely new scope gets new candidates without a second editable backlog

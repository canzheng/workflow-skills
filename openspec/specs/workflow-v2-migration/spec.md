# Workflow v2 migration

## Purpose
Known-format read-only inventory and deliberate one-time authority cutover with provenance.

## Requirements
### Requirement: Read-only known-format inventory
Migration inspection SHALL read known v1 backlog/feature/OpenSpec records, retain
original acceptance/evidence/blockers and paths, distinguish historical Done from
remaining work, and propose dispositions without performing remote or local mutations.

#### Scenario: Empty active backlog
- **WHEN** all known records are Done and active sections are empty
- **THEN** inspection reports historical counts and zero active work without creating Issues

#### Scenario: Ambiguous or inconsistent record
- **WHEN** IDs duplicate, feature/change targets are missing or states are inconsistent
- **THEN** inspection returns actionable findings rather than guessed migration state

### Requirement: Single authority and bounded rollback
Authorized consumer cutover SHALL assign one explicit disposition per active item,
reconcile remote source identities before retry, preserve human edits and freeze the
old ledger for migrated items. Rollback SHALL preserve published remote history.

#### Scenario: Partial remote creation
- **WHEN** remote creation may have succeeded before an interruption
- **THEN** the next operation re-reads open/closed identities before continuing
- **AND** neither Done history nor confirmed migrated items are recreated

## MODIFIED Requirements

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

#### Scenario: Legacy read target changes after validation
- **WHEN** a ledger or feature is replaced with a symlink, FIFO or unsafe parent after path validation
- **THEN** inventory reads only a bound regular-file descriptor or reports a finding without blocking or disclosing external records
- **AND** original/replacement/index bytes and remote state are not modified


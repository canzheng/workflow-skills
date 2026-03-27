## ADDED Requirements

### Requirement: Shaping retains authored OpenSpec change artifacts
Promoted workflow-managed features in `[SHAPING]` SHALL keep the authored baseline artifacts created by `openspec-propose`.

#### Scenario: Feature enters shaping with authored change artifacts
- **WHEN** `shape-backlog-item` promotes a backlog item into `[SHAPING]`
- **THEN** the linked OpenSpec change contains `proposal.md`, `design.md`, and `tasks.md`
- **AND** those files remain part of the shaping authority for that feature until later workflow stages tighten additional gates

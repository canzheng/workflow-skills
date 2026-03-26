## ADDED Requirements

### Requirement: Historical legacy-exempt metadata remains valid during resolver scans
Historical completed-feature exemptions SHALL remain valid when repository-wide workflow resolvers inspect promoted feature files.

#### Scenario: Resolver inspects completed migrated feature metadata
- **WHEN** a workflow resolver reads a promoted feature in `[DONE]`
- **AND** that feature records `OpenSpec Status` as `legacy-exempt`
- **THEN** the resolver treats the feature as a valid historical completed record
- **AND** it does not require `OpenSpec Change` metadata unless the feature is being processed under an active-state rule

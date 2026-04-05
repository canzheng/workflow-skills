## ADDED Requirements

### Requirement: Shaped executable tasks expose proof obligations and validation intent
Workflow-managed OpenSpec shaping SHALL define proof obligations and planned validation coverage for executable tasks before those tasks enter execution.

#### Scenario: Ready task is justified by explicit proof planning
- **WHEN** workflow shaping prepares a feature for promotion to `[READY]`
- **THEN** each startable top-level OpenSpec task has an associated implementation-plan shape that names the contract surface, proof obligations, and required validation classes
- **AND** readiness guidance does not treat a task as execution-ready when proof intent is still implicit or only described through lower-level helper tests

### Requirement: Ready features require contract-aligned proof coverage
Workflow readiness SHALL require at least one execution task whose proof planning is aligned to the shaped contract rather than only to dependency-derived status.

#### Scenario: Ready-feature rejects dependency-ready work without contract-ready proof
- **WHEN** a feature has a top-level task that is dependency-ready under the workflow task rules
- **AND** that task still lacks proof planning aligned to the shaped contract surface
- **THEN** `ready-feature` does not promote the feature to `[READY]`
- **AND** the missing proof coverage is treated as unresolved shaping work rather than as execution-time cleanup

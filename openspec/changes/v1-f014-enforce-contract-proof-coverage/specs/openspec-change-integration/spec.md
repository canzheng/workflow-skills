## ADDED Requirements

### Requirement: Shaped executable tasks expose proof obligations and validation intent
Workflow-managed OpenSpec shaping SHALL define proof obligations and planned validation coverage for executable tasks before those tasks enter execution.

#### Scenario: Ready task is justified by explicit proof planning
- **WHEN** workflow shaping prepares a feature for promotion to `[READY]`
- **THEN** each startable top-level OpenSpec task has an associated implementation-plan shape that names the contract surface, proof obligations, and required validation classes
- **AND** readiness guidance does not treat a task as execution-ready when proof intent is still implicit or only described through lower-level helper tests

## ADDED Requirements

### Requirement: Autonomous orchestration does not bypass workflow integrity checks
Automation helpers SHALL not route around workflow integrity rules that manual wrappers enforce.

#### Scenario: Automation evaluates active work
- **WHEN** an automation helper decides whether active work is eligible to continue
- **THEN** it uses the same linkage and readiness integrity rules as the manual workflow gate
- **AND** malformed active work remains a blocking workflow issue rather than an eligible action

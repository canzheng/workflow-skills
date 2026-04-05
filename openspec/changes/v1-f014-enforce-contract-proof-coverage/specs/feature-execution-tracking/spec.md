## ADDED Requirements

### Requirement: Task evidence guidance follows explicit proof obligations
Feature execution records SHALL treat validation evidence as proof against explicit obligations rather than as an unstructured collection of passing checks.

#### Scenario: Completion guidance records obligation-aware evidence
- **WHEN** workflow guidance records task validation evidence in a feature file
- **THEN** that guidance ties the evidence back to the active task's declared proof obligations
- **AND** it distinguishes between helper-level checks and broader runtime-facing validation classes when both exist

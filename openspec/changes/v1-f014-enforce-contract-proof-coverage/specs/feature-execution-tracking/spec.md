## ADDED Requirements

### Requirement: Task evidence guidance follows explicit proof obligations
Feature execution records SHALL treat validation evidence as proof against explicit obligations rather than as an unstructured collection of passing checks.

#### Scenario: Completion guidance records obligation-aware evidence
- **WHEN** workflow guidance records task validation evidence in a feature file
- **THEN** that guidance ties the evidence back to the active task's declared proof obligations
- **AND** it distinguishes between helper-level checks and broader runtime-facing validation classes when both exist

### Requirement: Workflow records evidence using a shared validation taxonomy
Feature execution records SHALL use a shared validation taxonomy so proof categories remain comparable across tasks and reviews.

#### Scenario: Task evidence names validation categories
- **WHEN** workflow guidance records task evidence
- **THEN** the evidence categories distinguish helper proof, schema proof, composed runtime proof, persistence proof, negative-path proof, and manual inspection proof
- **AND** the recorded evidence makes it clear which category each proof item satisfies

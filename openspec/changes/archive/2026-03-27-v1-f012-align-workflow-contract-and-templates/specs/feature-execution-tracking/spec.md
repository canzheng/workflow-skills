## ADDED Requirements

### Requirement: Workflow-maintained feature-file templates stay contract-aligned
Workflow-managed feature-file templates and rendered feature files SHALL describe the same execution-tracking contract.

#### Scenario: Renderer output matches tracked template guidance
- **WHEN** workflow tooling renders a new feature file
- **THEN** the generated `Current Task` guidance matches the tracked feature template
- **AND** the template remains the single source of truth for that guidance

### Requirement: Tracked feature records remain teammate-safe
Workflow-maintained feature records SHALL avoid machine-local absolute paths in tracked validation and handoff notes.

#### Scenario: Recorded validation evidence is portable
- **WHEN** a workflow-maintained feature file records a validation command or inspection pattern
- **THEN** it avoids embedding machine-local absolute paths or usernames in tracked documentation

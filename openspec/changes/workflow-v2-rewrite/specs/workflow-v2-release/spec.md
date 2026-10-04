## ADDED Requirements

### Requirement: Revision-bound environment acceptance
The rewrite SHALL provide actual fresh Cloud skill discovery/execution, same-content
Ubuntu portability, native GitHub operations and Actions evidence, and separately
observed merge enforcement before reporting full release validation. Missing access
SHALL remain explicit pending acceptance and SHALL prevent early rewrite archive.

#### Scenario: Required environment is unavailable
- **WHEN** local checks pass but fresh Cloud or Ubuntu evidence is unavailable
- **THEN** implementation is reviewable and environmental acceptance remains pending
- **AND** the rewrite change remains active with an exact same-revision next action

#### Scenario: Required acceptance is satisfied
- **WHEN** all required acceptance and review evidence exists for the delivering content
- **THEN** the closing branch synchronizes final specs, archives the rewrite and reruns checks
- **AND** archive alone does not claim merge or release publication

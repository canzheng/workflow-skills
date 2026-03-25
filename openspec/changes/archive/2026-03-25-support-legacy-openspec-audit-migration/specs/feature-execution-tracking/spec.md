## ADDED Requirements

### Requirement: Feature files support historical completed-feature exemptions
Feature metadata SHALL support an explicit exemption marker for historical completed features that predate OpenSpec adoption.

#### Scenario: Historical completed feature is exempt from OpenSpec change linkage
- **WHEN** a repository adopts OpenSpec after a feature already reached `[DONE]`
- **THEN** the feature file may record `OpenSpec Status` as `legacy-exempt`
- **AND** the feature is not required to record a linked OpenSpec change
- **AND** the exemption does not apply to active shaping or execution states

## ADDED Requirements

### Requirement: Completed features support explicit historical migration exemptions
Completed-feature audit expectations SHALL distinguish historical pre-OpenSpec work from post-adoption archived work.

#### Scenario: Historical completed feature remains done after OpenSpec adoption
- **WHEN** a feature was completed before OpenSpec adoption and the repo later adopts OpenSpec
- **THEN** the feature may remain in `[DONE]`
- **AND** its feature file may mark `OpenSpec Status` as `legacy-exempt`

#### Scenario: Post-adoption completed feature uses archived OpenSpec state
- **WHEN** a feature reaches `[DONE]` after OpenSpec adoption
- **THEN** its linked OpenSpec change is expected to be archived rather than active

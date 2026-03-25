## ADDED Requirements

### Requirement: Feature completion evidence supports the move to done
Feature metadata SHALL make the transition from `[IN_PROGRESS]` to `[DONE]` evidence-based rather than implicit.

#### Scenario: Finish-feature moves a feature to done after acceptance passes
- **WHEN** `finish-feature` moves a feature from `[IN_PROGRESS]` to `[DONE]`
- **THEN** the feature file records completion evidence consistent with the accepted task work
- **AND** the handoff state makes it clear that branch finalization is still a downstream `finish-feature` action

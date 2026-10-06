## Purpose
Define revision-bound Ubuntu, GitHub, review and enforcement acceptance for the v2 release, preserving explicit authorization gates and deferred Cloud evidence.

## ADDED Requirements

### Requirement: Revision-bound environment acceptance
The rewrite SHALL provide actual fresh Ubuntu Codex repository-local skill
discovery/execution, exact-revision Ubuntu portability and continuation, native
GitHub operations and Actions evidence, and separately
observed merge enforcement before reporting full release validation. Missing access
to required premerge acceptance SHALL remain explicit pending and SHALL prevent
early rewrite archive. Unavailable post-merge or administrative access SHALL remain
a separate authorization/deployment gate and SHALL NOT by itself prevent premerge
acceptance or archive.
Cloud setup/discovery SHALL be deferred for this first release under the user-approved
2026-10-05 scope change; unsuccessful Cloud checks SHALL NOT be reported as passed.

#### Scenario: Required environment is unavailable
- **WHEN** local checks or a catalog query pass but required Ubuntu agent-use evidence is unavailable
- **THEN** implementation is reviewable and environmental acceptance remains pending
- **AND** the rewrite change remains active with an exact same-revision next action

#### Scenario: Required acceptance is satisfied
- **WHEN** all required acceptance and review evidence exists for the delivering content
- **THEN** the closing branch synchronizes final specs, archives the rewrite and reruns checks
- **AND** archive alone does not claim merge or release publication

#### Scenario: Cloud is deferred
- **WHEN** Ubuntu adoption/use and all other required release acceptance are satisfied but Cloud discovery is unverified
- **THEN** Cloud is reported deferred and does not prevent acceptance or final archive
- **AND** required semantic review, GitHub checks, documentation and merge authorization remain unchanged

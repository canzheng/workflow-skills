# Workflow v2 quality and checks

## Purpose
Executable mechanical obligations and risk proof with explicit semantic and enforcement limits.

## Requirements
### Requirement: Actual verification consumer
Reviewed config commands SHALL be argv arrays executed without shell interpretation
only when requested in the intended environment. A missing required checker/runtime
SHALL fail rather than silently fall back or count skipped work as passed.

#### Scenario: Configured local command fails
- **WHEN** a selected local verification command exits nonzero
- **THEN** the checker reports the actual failed exit and does not certify completion

### Requirement: Trusted metadata and bounded enforcement claims
PR checks SHALL require the declared nonempty evidence/documentation sections and
valid local references; trusted-base metadata SHALL treat body/head content as data,
not execute head code or interpolated shell fragments. Required merge enforcement
SHALL be reported only after actual configuration/readback/observation.

#### Scenario: Metadata contains executable text
- **WHEN** a PR body contains shell commands or links to a malicious head script
- **THEN** mechanical validation reads data without executing those commands/scripts

#### Scenario: Edited documentation is false
- **WHEN** structure/link checks pass but docs contradict code defaults
- **THEN** semantic review still reports unfinished documentation

### Requirement: Discriminating risk proof
Material risks SHALL select independent numerical expectations, actual downstream
consumers and missing/denied/interrupted paths where pertinent. Repairs SHALL retain
original fixture/assertion strength unless an approved behavior change requires otherwise.

#### Scenario: Parsed currency has no effective consumer
- **WHEN** a consumer always formats USD despite valid emitted EUR metadata
- **THEN** an independent EUR output expectation fails the consumer proof

### Requirement: Native Issue audit input
Issue audits SHALL validate native state and optional state_reason values before
classifying snapshots, without treating mechanical validity as semantic delivery.

#### Scenario: Malformed closure reason
- **WHEN** state_reason is an unknown string or a non-string/non-null value
- **THEN** public check returns structured invalid-input JSON without changing the snapshot or index

#### Scenario: Case-normalized completion
- **WHEN** a closed Issue supplies COMPLETED without delivery evidence
- **THEN** the same missing-evidence finding applies as for completed
- **AND** null, not_planned, duplicate and reopened reasons remain supported without asserting completed delivery

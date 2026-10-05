## MODIFIED Requirements

### Requirement: Actual verification consumer
Reviewed config commands SHALL be argv arrays executed without shell interpretation
only when requested in the intended environment. A missing required checker/runtime
SHALL fail rather than silently fall back or count skipped work as passed.

#### Scenario: Configured local command fails
- **WHEN** a selected local verification command exits nonzero
- **THEN** the checker reports the actual failed exit and does not certify completion

#### Scenario: Required OpenSpec subprocess hangs
- **WHEN** selected OpenSpec version or validation execution times out or cannot launch
- **THEN** the checker returns a structured required-check error with no pass or captured partial timeout output
- **AND** version/validation deadlines are 10/120 seconds and the repository/index remain unchanged

### Requirement: Trusted metadata and bounded enforcement claims
PR checks SHALL require the declared nonempty evidence/documentation sections and
valid local references; trusted-base metadata SHALL treat body/head content as data,
not execute head code or interpolated shell fragments. Required merge enforcement
SHALL be reported only after actual configuration/readback/observation.

#### Scenario: Metadata contains executable text
- **WHEN** a PR body contains shell commands or links to a malicious head script
- **THEN** mechanical validation reads data without executing those commands/scripts

#### Scenario: Malformed PR event adapter input
- **WHEN** event object fields, head SHA or body have malformed shapes, or repository identities differ
- **THEN** public metadata check returns structured invalid-input JSON before any head fetch
- **AND** snapshot and index remain unchanged, without a traceback
- **AND** native null/absent bodies still receive missing-section findings rather than certifying a PR contract

#### Scenario: PR-body fragment links
- **WHEN** a saved or native PR snapshot links to a heading in its own body
- **THEN** validation uses body anchors without requiring a synthetic PR.md in the head
- **AND** missing body anchors fail even if an actual head PR.md contains the heading

#### Scenario: Edited documentation is false
- **WHEN** structure/link checks pass but docs contradict code defaults
- **THEN** semantic review still reports unfinished documentation

#### Scenario: Enumerated Markdown is a symlink
- **WHEN** a document selected for local link checking is a symlink, including a dangling or cyclic link
- **THEN** check reports an unsafe repository-relative document path before reading the target
- **AND** external content is not disclosed, document/link/index bytes remain unchanged, and regular local link diagnostics still run
- **AND** no-follow/nonblocking directory/file descriptors reject substitutions and non-regular entries, and reads remain bound after opening

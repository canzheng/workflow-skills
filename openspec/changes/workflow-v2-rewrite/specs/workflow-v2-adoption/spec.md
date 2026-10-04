## ADDED Requirements

### Requirement: Tracked policy and pinned local skill dependencies
Consumer adoption SHALL track project-owned configuration, policy, utilities,
CI/templates, docs/specs, project-specific skills and a dependency manifest containing
an exact source commit, credential-free source URL and asset hashes. Only the three
shared canonical skill directories SHALL be gitignored. Source authoring SHALL keep
its authored shared skills tracked. Setup SHALL NOT modify the Git index.

#### Scenario: Fresh clone and repeatable bootstrap
- **WHEN** a fresh consumer clone lacks ignored shared skills
- **THEN** bootstrap fetches only the tracked full source commit and verifies pinned hashes
- **AND** materializes only those ignored namespaces without rewriting project files or index
- **AND** a second bootstrap with matching bytes returns no changes without network access

#### Scenario: Dependency conflict or failed fetch
- **WHEN** shared assets are modified, extra, symlinked or tracked, or the pin/fetch is invalid
- **THEN** bootstrap fails without silently overwriting user changes or choosing latest
- **AND** interrupted writes restore originals or report recoverable residuals

#### Scenario: Preparation and enforcement are separate evidence
- **WHEN** Cloud, Ubuntu or consumer CI prepares an adopted repository
- **THEN** bootstrap consumes the same tracked source pin before discovery or verification
- **AND** local files or workflow YAML alone do not establish actual host discovery or enforcement

#### Scenario: Effective ignore policy conflicts
- **WHEN** broader or nested excludes hide project skills, or negations expose shared dependencies
- **THEN** setup detects the effective policy conflict before destination writes
- **AND** bootstrap/check/doctor report the conflict without rewriting unrelated rules

#### Scenario: Source-owned environment entrypoint
- **WHEN** Cloud install-script or local setup fetches an explicit workflow-skills commit
- **THEN** its source-owned entrypoint adopts a fresh Git root and verifies the dependency
- **AND** an adopted consumer retains its tracked pin and project files on repeated runs
- **AND** no setup entrypoint is copied into the consumer or installed globally
- **AND** before the first commit diagnostics report revision:null and dirty:true

#### Scenario: Adopted configuration and provenance preflight
- **WHEN** repeat environment setup finds an adopted repo with missing config or wrong explicit identity
- **THEN** it fails before materializing missing shared dependencies or rewriting project files
- **AND** malformed installed bundle versions fail check, doctor and bootstrap before writes
- **AND** setup, source checks and installed provenance use the same v2 version format

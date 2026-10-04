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

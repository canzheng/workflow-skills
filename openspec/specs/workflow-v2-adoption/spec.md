# Workflow v2 adoption

## Purpose
Explicit repository adoption and safe pinned setup without global installation.

## Requirements
### Requirement: Explicit repository routing
Repositories using v2 SHALL select it explicitly through config and AGENTS guidance;
historical planning directories SHALL NOT select obsolete execution wrappers.

#### Scenario: History remains beside v2
- **WHEN** historical planning files remain after instruction cutover
- **THEN** current guidance selects the v2 contract and preserves unrelated rules

### Requirement: Pinned bounded repository setup
Setup SHALL require an explicit Git root and full source commit, preview by default,
preflight all assets/ownership/markers, and preserve user-owned configuration.
Source bytes SHALL match the pinned commit. The manifest SHALL describe installation
provenance, not task state or its own content hash.

#### Scenario: Modified file or unsafe target
- **WHEN** a managed file has local changes or the target uses a symlink or missing Git root
- **THEN** update fails without silently overwriting files or selecting another checkout

#### Scenario: Apply is interrupted
- **WHEN** a replacement fails during apply
- **THEN** original bytes/modes are restored or exact recoverable residuals reported

### Requirement: Bounded uninstall and diagnostics
Uninstall SHALL remove only unmodified managed assets/block, retain configuration
and user modifications, and report residuals. Doctor SHALL be read-only and distinguish
source authoring from installed consumers and authentication from unprobed writes.

#### Scenario: Duplicate active skill name
- **WHEN** a canonical v2 skill is discoverable in two inspected locations
- **THEN** doctor reports a conflict without deleting global skills

### Requirement: Consumer CI adoption
The pinned consumer bundle SHALL include read-only generic verification and
trusted-base PR metadata workflows. Verification SHALL bootstrap the tracked skill dependency before checks and consume reviewed local argv
commands and mechanical checks without assuming source development dependencies or
executing environment-specific integration commands. Setup SHALL NOT configure
repository protections or overwrite unmanaged or modified workflows.

#### Scenario: Consumer commands and ownership
- **WHEN** a consumer installs the pinned bundle with declared application verification
- **THEN** the installed verification workflow runs those commands and mechanical checks
- **AND** missing prerequisites or a failed command fail verification
- **AND** existing workflow collisions fail preflight without unrelated writes

#### Scenario: Adoption is not enforcement
- **WHEN** setup installs workflow files
- **THEN** trusted-base metadata still requires base adoption
- **AND** required check enforcement remains pending until separately configured and observed

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

#### Scenario: Canonical objects despite local replacement refs
- **WHEN** a source checkout has local Git replacement refs for a pinned revision
- **THEN** setup and bootstrap validate the canonical commit and asset objects
- **AND** substituted worktree bytes conflict before consumer writes
- **AND** canonical bytes remain reproducible from a separate checkout without those refs
- **AND** validation does not delete replacement refs or change Git configuration

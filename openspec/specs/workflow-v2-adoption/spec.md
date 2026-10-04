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
trusted-base PR metadata workflows. Verification SHALL consume reviewed local argv
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

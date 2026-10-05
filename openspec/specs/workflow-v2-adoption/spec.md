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
trusted-base PR metadata workflows. Verification SHALL verify the checked-out tracked assets directly and consume reviewed local argv
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
Consumer adoption SHALL commit project-owned configuration, policy, utilities,
CI/templates, docs/specs, project-specific skills and the three shared skill
namespaces with risk references. Schema-3 provenance SHALL record tracked skill
storage, an exact source commit, credential-free URL and managed asset hashes.
Setup SHALL NOT change the index or add shared-skill ignores. Adoption SHALL be
reviewed and committed before host discovery acceptance.

#### Scenario: Fresh clone and repeat verification
- **WHEN** a fresh consumer clone checks out a reviewed adoption
- **THEN** all shared skills and references are present as committed Git files
- **AND** startup/CI verifies the same pin without downloads, repairs or index writes
- **AND** repeated verification remains a no-op without source network access

#### Scenario: Tracked snapshot conflict
- **WHEN** an adopted shared asset is missing, modified, extra, symlinked, ignored or untracked
- **THEN** bootstrap/check/doctor fail without recreating files or overwriting edits
- **AND** recovery requires restoring Git or an explicit reviewed setup/update

#### Scenario: Complete tracked adoption and initial review
- **WHEN** any managed asset is indexed or present in HEAD
- **THEN** every manifest asset, provenance manifest, project config and managed AGENTS file must remain indexed
- **AND** removing provenance or a runtime/documentation/CI asset from the index fails verification even if working files remain intact
- **WHEN** initial adoption is completely unstaged with no managed assets in HEAD
- **THEN** it may be verified as reviewable, but all required assets must be trackable
- **AND** ignoring provenance/policy/runtime/docs/CI fails setup preflight before writes and later verification without repair
- **AND** partially staging adoption cannot bypass the complete tracked-file obligation

#### Scenario: Staged adoption is independently valid
- **WHEN** intact working files coexist with invalid staged installation bytes or modes
- **THEN** bootstrap/check/doctor reject the staged commit candidate without changing files or index
- **AND** staged provenance/config schemas, configured document paths, managed hashes and AGENTS block must be coherent regular files without merge stages
- **AND** valid project-owned policy differences between index and working tree remain permitted

#### Scenario: Explicit ignored-to-tracked migration
- **WHEN** setup updates schema-2 adoption to tracked storage
- **THEN** it verifies and removes only its owned ignore block, preserving other rules
- **AND** modified assets/blocks or effective excludes conflict before writes
- **AND** failed writes restore originals or report recoverable residuals
- **AND** the caller stages/commits the resulting complete adoption, not setup

#### Scenario: Checkout and host discovery are separate
- **WHEN** Cloud or Ubuntu starts from the committed consumer revision
- **THEN** skill files already exist without environment injection
- **AND** initial host catalog/use evidence is recorded before explicit skill reads
- **AND** local files or green CI do not establish host discovery or enforcement

#### Scenario: Effective ignore conflicts
- **WHEN** root, nested, global or info excludes hide required installed assets, policy/provenance or project-specific skills
- **THEN** setup detects the policy conflict before writes
- **AND** startup checks report the conflict without altering unrelated rules

#### Scenario: Source-owned first adoption and repeat setup
- **WHEN** first adoption fetches an explicit workflow-skills source commit
- **THEN** its source-owned entrypoint installs commit-ready files in a fresh Git root
- **AND** repeat setup retains an adopted schema-3 pin/files/index and only verifies
- **AND** old schema-1/2 adoption requires explicit reviewed update, not automatic migration
- **AND** no source entrypoint is copied into the consumer or installed globally
- **AND** before the first commit diagnostics report revision:null and dirty:true

#### Scenario: Adopted configuration and provenance preflight
- **WHEN** repeat setup finds missing config or a wrong explicit repository identity
- **THEN** it fails before writes
- **AND** malformed provenance or bundle versions fail verification without repairs

#### Scenario: Canonical objects despite replacement refs
- **WHEN** the pinned source has local Git replacement refs
- **THEN** setup and explicit offline source verification read canonical commit/asset objects
- **AND** substituted worktree bytes conflict before writes
- **AND** committed canonical consumer bytes are reproducible in a fresh clone
- **AND** no replacement refs or Git configuration are changed

## ADDED Requirements

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

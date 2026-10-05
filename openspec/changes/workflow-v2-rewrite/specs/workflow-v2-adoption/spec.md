## ADDED Requirements

### Requirement: Tracked policy and pinned local skill dependencies
Consumer adoption SHALL track project policy/configuration, utilities, CI/templates,
docs/specs, project-specific skills and schema-4 provenance. The three shared skill
namespaces/references SHALL be ignored repo-local dependencies, with an exact source
commit, credential-free URL, managed hashes and a narrow owned ignore-block hash.
Setup SHALL NOT stage/untrack/commit or ignore all of .agents. Source canonical
skills SHALL remain tracked. Required Ubuntu discovery/use SHALL be tested separately.

#### Scenario: Fresh clone and repeat bootstrap
- **WHEN** a fresh consumer clone contains committed project adoption but lacks shared dependency files
- **THEN** bootstrap previews missing shared files and --apply fetches only the recorded commit or uses an explicitly matching source
- **AND** canonical source bytes/hashes are validated before writing only missing shared files
- **AND** complete matching reruns are offline no-ops preserving project files, pin and raw index
- **AND** consumer CI bootstraps the same pin before configured local/mechanical checks

#### Scenario: Dependency conflict or missing revision
- **WHEN** a shared dependency is modified, extra or symlinked, or the exact pin is unavailable or mismatched
- **THEN** bootstrap fails without overwriting edits or falling back to main/latest
- **AND** project assets and index remain unchanged

#### Scenario: Complete project adoption and initial review
- **WHEN** any managed project asset or provenance is staged or committed
- **THEN** every non-shared manifest asset, provenance/config, AGENTS and .gitignore remains indexed
- **AND** shared dependency paths must be ignored and absent from the index
- **AND** untracking provenance cannot reset adoption or hide incomplete project files
- **WHEN** initial adoption is completely unstaged
- **THEN** it is reviewable only with trackable project files and valid narrow shared ignores

#### Scenario: Staged adoption is independently valid
- **WHEN** intact working files coexist with invalid staged project bytes or modes
- **THEN** bootstrap/check/doctor reject the staged commit candidate without changing files or index
- **AND** staged schemas, configured docs, managed project hashes and AGENTS/ignore blocks must form a coherent regular-file snapshot without merge stages
- **AND** valid project-owned policy differences remain permitted

#### Scenario: Explicit tracked-to-ignored migration
- **WHEN** setup explicitly updates tracked schema-1/3 adoption to schema 4
- **THEN** it preserves the index and adds only its owned shared-directory ignore block
- **AND** the caller reviews/untracks only shared directories without deleting their working files, stages project changes and commits
- **AND** modified assets/blocks and unsafe destinations conflict before writes
- **AND** failed writes restore originals or report recoverable residuals

#### Scenario: Tracked compatibility
- **WHEN** an existing schema-3 consumer has not explicitly migrated
- **THEN** full tracked-asset and canonical staged validation remain supported
- **AND** bootstrap never recreates missing tracked skills or changes storage/index

#### Scenario: Bootstrap and host discovery are separate
- **WHEN** Ubuntu starts a fresh Codex session from the committed consumer root after bootstrap
- **THEN** capture its initial native catalog before explicit skill reads and separately prove actual skill use
- **AND** disk presence, catalog-only queries and green CI do not establish semantic use or merge enforcement
- **AND** Cloud discovery is deferred for the first release, not claimed as passed

#### Scenario: Effective ignore conflicts
- **WHEN** root/nested/global/info excludes hide project/provenance assets or project-specific skills, or shared dependency paths are not ignored
- **THEN** setup detects the policy conflict before writes and checks preserve unrelated rules

#### Scenario: Source-owned first adoption and repeat setup
- **WHEN** first adoption fetches an explicit source commit into a new consumer Git root
- **THEN** its source-owned entrypoint installs project assets and ignored shared skills without pre-existing tools or first commit
- **AND** repeat startup retains the installed pin and materializes only missing ignored dependencies
- **AND** old schema-1/2 adoption requires reviewed update rather than automatic migration
- **AND** no entrypoint/global project policy is copied into the consumer or installed globally
- **AND** before the first commit diagnostics report revision:null and dirty:true

#### Scenario: Adopted configuration and provenance preflight
- **WHEN** repeat setup finds missing config, wrong repository identity, malformed provenance or bundle version
- **THEN** it fails before dependency writes and preserves existing files/index

#### Scenario: Canonical objects despite replacement refs
- **WHEN** pinned source has local Git replacement refs
- **THEN** setup/bootstrap read canonical commit/assets and reject substituted worktree bytes before writes
- **AND** a replacement-free source clone reproduces the same shared bytes without altering local refs/configuration

### Requirement: Explicit optional global shared skills
An explicit install-skills command SHALL preview by default and install only the
three shared skills/references plus provenance at ~/.agents/skills or an explicit
absolute target. It SHALL pin canonical source bytes and preserve unrelated names,
modified assets, project policy and authentication. Repository setup SHALL NOT
install globally as a side effect; global installation SHALL NOT claim project adoption.

#### Scenario: Global install, rerun and conflicts
- **WHEN** the user explicitly applies a pinned shared-only installation
- **THEN** only owned shared files/provenance are installed and identical reruns are no-ops
- **AND** unmanaged collisions, modified assets, symlinks and bad pins fail without overwrite
- **AND** interrupted writes restore originals or report precise residuals
- **AND** uninstall retains modifications/unrelated names and reports residuals

#### Scenario: One discovery source and project routing
- **WHEN** repo-local and global shared names are both visible
- **THEN** report duplicate discovery and choose one active location explicitly
- **AND** global skill instructions resolve contract/docs from the selected project rather than a global docs tree

# Workflow v2 adoption

## Purpose
Explicit repository adoption and exact-pin skill dependencies with bounded optional global installation.

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

#### Scenario: Initial adoption preserves indexed deletions
- **WHEN** a project asset or policy destination is owned by the index or HEAD but absent from the worktree
- **THEN** preview and apply reject before writing and preserve all files and the raw index
- **AND** removing the cached path alone does not authorize replacing a committed deletion

#### Scenario: Indexed ancestor is deleted
- **WHEN** a destination ancestor is an index/HEAD-owned file or gitlink absent from the working tree, including a staged deletion
- **THEN** preview/apply preserve its deletion without recreating a directory or modifying files/index

#### Scenario: Apply is interrupted
- **WHEN** a replacement fails during apply
- **THEN** original bytes/modes are restored or exact recoverable residuals reported

#### Scenario: Concurrent edit during rollback
- **WHEN** another process changes an applied file or recreates a deleted destination before rollback
- **THEN** rollback preserves that changed content, including mode changes and symlink replacements
- **AND** reports the exact residual path and recoverable original bytes/mode without following unsafe paths
- **AND** newly created directories are removed only if their inode/mode is unchanged and they are empty; changed directories are retained/reported with creation metadata
- **AND** unchanged installer writes can still be restored; no multi-process lock or atomic multi-file transaction is promised

#### Scenario: Deleted file parent is replaced
- **WHEN** an owned file is deleted and its existing parent or ancestor is concurrently replaced before a later apply failure
- **THEN** rollback leaves the replacement directory and missing destination unchanged
- **AND** reports recoverable original bytes/mode and the expected parent identity chain
- **AND** a replaced parent discovered before another write prevents that write rather than repurposing the new directory

#### Scenario: Parent swap inside a mutation
- **WHEN** an existing parent or ancestor is replaced after validation but inside deletion, staging, replacement, restoration or cleanup
- **THEN** the operation remains bound to its verified parent directory descriptor without following the replacement pathname
- **AND** replacement-directory human files and staging names remain unchanged, the raw Git index is preserved and original bytes/mode stay recoverable
- **AND** the namespace change is reported as a residual rather than successful restoration

#### Scenario: Staging entry changes before successful replacement
- **WHEN** a staging entry is changed after validation but the replacement syscall succeeds, or the destination changes during that call
- **THEN** destination bytes/mode/device/inode are compared with the owned staged identity before setup can succeed
- **AND** mismatches preserve foreign/changed destination content or absence, original backups and the raw Git index with a recoverable conflict

#### Scenario: Destination changes at replacement boundary
- **WHEN** an existing destination changes or a previously absent destination is created immediately before replacement
- **THEN** atomic exchange/no-replace preserves the actual competing entry and reports a recoverable conflict
- **AND** original backups/modes and the raw Git index remain unchanged

#### Scenario: Installed inode changes before rollback writes
- **WHEN** applied content changes after rollback validation but before restoration
- **THEN** restoration stages the original rather than truncating a live file and preserves the changed entry as a residual

#### Scenario: Destination changes at deletion boundary
- **WHEN** an owned entry changes immediately before removal
- **THEN** removal captures and validates the actual entry before discarding it, restoring a mismatch when the path remains absent
- **AND** concurrent content and original backups remain recoverable without changing the index

#### Scenario: Atomic primitive is unavailable
- **WHEN** libc/kernel/filesystem atomic exchange or no-replace is unavailable
- **THEN** apply fails without falling back to an unchecked overwrite

#### Scenario: Displaced inode changes during cleanup
- **WHEN** in-place content changes while cleanup holds the displaced inode open through removal
- **THEN** changed bytes and mode are retained in recovery metadata and a residual is reported

#### Scenario: Staging basename changes at cleanup boundary
- **WHEN** a shared staging, restoration or removal basename is replaced immediately before cleanup capture
- **THEN** cleanup validates the actual captured entry in private same-filesystem storage before deleting anything
- **AND** the concurrent entry and original backups/index remain preserved as a recoverable conflict

#### Scenario: Created directory changes at removal boundary
- **WHEN** another process replaces a newly created directory after validation but before cleanup capture
- **THEN** cleanup preserves the actual competing directory and reports a residual instead of removing it

#### Scenario: Quarantine restoration collides with recreated public name
- **WHEN** a public entry is recreated after private capture and prevents no-replace restoration
- **THEN** both public and captured entries remain intact, with the quarantine path in recovery metadata

#### Scenario: Private directory cleanup has no conditional removal primitive
- **WHEN** a transaction finishes using private capture storage
- **THEN** private storage and captured empty directories are retained rather than removed by a checked basename
- **AND** repository storage resides under Git-private storage without project/index/ignore changes
- **AND** identical no-op reruns create no additional storage

#### Scenario: Directory creation is privately bound before publication
- **WHEN** a new directory must be published but a concurrent directory already occupies its public path
- **THEN** no-replace publication preserves the competing directory and reports recoverable ownership metadata
- **AND** installer ownership derives from the privately opened staged inode instead of a public post-mkdir lookup

#### Scenario: Private directory birth is observed before ownership
- **WHEN** a private storage or staged-directory basename changes between mkdir and open
- **THEN** kernel observation begun before creation rejects replacement, including a same-mode inode, before writes or publication
- **AND** missing observation support, permission/owner mismatch, watch invalidation and event overflow fail closed without changing project files or index

#### Scenario: Capture storage has another filesystem
- **WHEN** Git-private storage or explicit shared-only TMPDIR differs from the destination filesystem
- **THEN** apply fails before project writes without an unsafe copy/delete fallback

#### Scenario: Captured file changes during finalization
- **WHEN** an actual captured file is edited or replaced during finalization
- **THEN** no path-based unlink discards either entry and observed changes receive recovery metadata
- **AND** successful replacement retains displaced bytes/mode in private storage without changing the index
- **AND** uninstall removes the managed project namespace but retains captured recovery copies

### Requirement: Bounded uninstall and diagnostics
Uninstall SHALL remove only unmodified managed assets/block, retain configuration
and user modifications, and report residuals. Doctor SHALL be read-only and distinguish
source authoring from installed consumers and authentication from unprobed writes.

#### Scenario: Duplicate active skill name
- **WHEN** a canonical v2 skill is discoverable in two inspected locations
- **THEN** doctor reports a conflict without deleting global skills

#### Scenario: Undecodable unrelated discovery file
- **WHEN** a discovery root contains an unrelated skill file that is not valid UTF-8
- **THEN** doctor reports a per-file warning and continues inspecting other entries
- **AND** valid duplicates are still detected and the invalid file remains unchanged

### Requirement: Consumer CI adoption
The pinned consumer bundle SHALL include read-only generic verification and
trusted-base PR metadata workflows. Verification SHALL bootstrap the exact shared dependency pin, verify tracked project assets and consume reviewed local argv
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
Consumer adoption SHALL track project policy/configuration, CI/templates,
docs/specs, project-specific skills and schema-5 provenance. The three shared skill
namespaces/references and .agents/tools/workflow runtime SHALL be ignored repo-local dependencies, with an exact source
commit, credential-free URL, managed hashes and a narrow owned ignore-block hash.
Setup SHALL NOT stage/untrack/commit or ignore all of .agents. Source canonical
skills SHALL remain tracked. Required Ubuntu discovery/use SHALL be tested separately.

#### Scenario: Fresh clone and repeat bootstrap
- **WHEN** a fresh consumer clone contains committed project adoption but lacks shared dependency files
- **THEN** bootstrap previews missing shared skill/runtime files and --apply fetches only the recorded commit or uses an explicitly matching source
- **AND** canonical source bytes/hashes are validated before writing only missing shared skill/runtime files
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

#### Scenario: Ignored update refuses tracked dependencies
- **WHEN** an existing schema-4 consumer has a shared dependency in the index and requests a newer pinned setup update
- **THEN** preview and apply reject the index conflict before changing shared bytes, project assets or provenance
- **AND** files and raw index remain unchanged until the caller explicitly resolves the conflict

#### Scenario: Fresh ignored adoption refuses indexed shared paths
- **WHEN** initial ignored adoption encounters a shared namespace path in the index, including a deleted working copy
- **THEN** preview and apply reject before writing shared or project assets and preserve the raw index
- **AND** explicit reviewed tracked-to-ignored migration remains a separate operation

#### Scenario: Nested staged ignore policy
- **WHEN** a nested ignore policy or new project-specific skill exists in the index with a different or absent working copy
- **THEN** staged validation uses indexed policies and indexed project paths from one canonical snapshot
- **AND** blocking or nonregular indexed policies fail without mutation while valid project-owned policy differences remain allowed

#### Scenario: Explicit tracked-to-ignored migration
- **WHEN** setup explicitly updates tracked schema-1/3 adoption to schema 5
- **THEN** it preserves the index and adds only its owned shared-directory ignore block
- **AND** the caller reviews/untracks only shared dependency namespaces without deleting their working files, stages project changes and commits
- **AND** modified assets/blocks and unsafe destinations conflict before writes
- **AND** failed writes restore originals or report recoverable residuals

#### Scenario: Runtime relocation is completely staged
- **WHEN** a reviewed legacy runtime relocation introduces the new dependency pin but leaves an old shared Python file indexed
- **THEN** setup/check/doctor/bootstrap reject the incomplete new-layout candidate without mutation
- **AND** the documented untrack command tolerates paths absent from old layouts
- **AND** the caller stages all owned legacy runtime deletions and project changes before verification succeeds
- **AND** unrelated project tools in the old directory remain tracked and unchanged
- **AND** mixed old/new canonical runtime inventories are invalid before installer writes

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

#### Scenario: Runtime and skills use one dependency policy
- **WHEN** a fresh consumer adopts the default schema-5 bundle
- **THEN** shared skills and runtime are ignored/untracked at the same exact pin
- **AND** the runtime resides under .agents/tools/workflow while project tools/skills remain trackable
- **AND** source-owned bootstrap and CI fetch the tracked pin before running the consumer CLI
- **AND** metadata review fetches only the trusted base pin and never executes head code

#### Scenario: Partial initial policy staging
- **WHEN** the caller stages only newly adopted policy/configuration or introduces managed routing into a previously committed human policy
- **THEN** verification rejects the incomplete commit candidate while preserving working files and raw index
- **AND** pre-existing human policy alone does not turn entirely unstaged adoption into a completed commit


#### Scenario: Indexed dependency ancestor is a file
- **WHEN** a staged snapshot contains a file or gitlink at an ancestor of a managed dependency destination
- **THEN** check, doctor and bootstrap reject the candidate even when working directories remain intact
- **AND** they preserve dependency bytes, project files and the raw index
- **AND** an explicitly staged coherent migration remains valid without requiring the old HEAD to be merged


#### Scenario: Schema-five layout and consumer provenance win
- **WHEN** ignored setup is requested from a legacy runtime-layout bundle or schema-five provenance names that old layout
- **THEN** setup and installed diagnostics reject before dependency writes
- **AND** existing schema-three/four installations remain verifiable without automatic migration
- **WHEN** an adopted consumer also contains an unrelated workflow bundle marker
- **THEN** CI chooses its installation provenance and exact source pin before the marker
- **AND** verification invokes the manifest runtime and PR metadata chooses only the trusted base pin

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

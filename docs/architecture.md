# Current architecture

The active entrypoint selects explicit github-v2 configuration and the short
contract; historical planning does not select execution. Three canonical authored
skills live only in .agents/skills: design-to-backlog, deliver-issue and risk-review.
Native Codex execution handles internal work; GitHub owns shared delivery identity
and state. There is no task-state service, feature ledger or synchronizer.

The source Python standard-library utility entrypoint is tools/workflow/workflow.py;
consumers materialize the same pinned runtime at .agents/tools/workflow/workflow.py.
Both shared skills and runtime are dependencies with one storage policy and exact pin.
Fresh clones/CI fetch the source-owned entrypoint before bootstrap; trusted-base PR
metadata selects the base pin and reads head content only as data.
core.py validates configuration/paths/provenance and computes actual content identity.
setup.py preflights pinned source assets/target ownership, stages backups and restores
on apply failure; installation provenance is generated only for consumers.
bootstrap.py materializes only missing ignored shared skills/runtime from the exact source
pin. Schema-5 provenance records ignored storage/URL/full SHA/asset and ignore hashes.
Setup preserves project policy/config and index; caller handles explicit untracking
when migrating schema 3. Complete bootstrap reruns are offline/no-op; tracked schema-3
compatibility verifies only. Optional explicit install-skills installs shared bytes
at a chosen global/custom root without project/global policy. No cache/database or
mutable environment version selector is introduced.
records.py renders approved source bodies and provides pure snapshot checks/edits
for native operations, with no GitHub client or durable remote state.
checks.py validates mechanical bundle/schema/link/PR obligations; metadata is data,
and trusted code reads PR head Git blobs without executing them.
verify.py is source development tooling, not part of the consumer runtime.

.workflow/bundle.json is the explicit source-to-consumer asset map and version;
setup consumes every entry and verifies actual bytes against the full source SHA.
Consumer config remains user-owned. templates/consumer contains rendered consumer
guidance rather than a duplicate skill source. GitHub forms/PR templates ship;
consumer verification, trusted-base PR metadata and Issue completion label workflows
ship as owned assets. The Issue Action runs inline trusted github-script with only
issues:write and no checkout, projects fresh native state/reason into exact owned
labels and offers on-demand reconciliation. GitHub closing keywords own Issue closure;
automation never decides delivery or executes Issue/PR bodies. Bundle 2.1 requires
this asset while 2.0 inventories remain valid.
The generic verification job invokes configured local argv commands plus mechanical
checks; source development CI/dependencies are not copied into applications.

OpenSpec 1.14.0 is an optional pinned local development dependency. Current v2 specs
cover implemented adoption, delivery, migration and quality; the active rewrite delta retains required F14
environment acceptance. Legacy wrappers/state engine/global installer and six obsolete stable contracts
are removed. Original v1 records/archives remain reachable through the recorded baseline in Git,
not a duplicate in-tree legacy directory. migration.py performs read-only known-format v1 inventory; it preserves original
acceptance/evidence/blockers and proposes explicit dispositions without mutation.

Tests execute public CLIs and installed fixture consumers, injected apply failures,
metadata/head-data handling, content invalidation and numerical/consumer negative
controls. Skill exercises are primary-author artifact/evidence records, not proof
of fresh Cloud discovery or independent review. Actual Ubuntu portability evidence
is recorded separately in docs/validation/v2-acceptance.md.

Tracking validation covers every installed manifest asset and provenance/config/AGENTS,
excluding ignored shared dependencies, which must remain absent from the index. Indexed or committed managed assets identify adoption even
when the manifest is removed from the index. Initial unstaged review remains separate;
all required files must be trackable. Ignore previews preserve ancestor, global and
repository-info rules for every required destination before writes.
core.py also validates the staged installation independently using canonical index
blobs and modes: staged provenance/config, configured documents, every managed hash
and the AGENTS block must form a coherent regular-file snapshot. A good working tree
does not mask broken staged content. This is read-only commit-candidate validation,
not a requirement for unrelated project edits to match HEAD or the working tree.

## Approved Ubuntu distribution refinement — 2026-10-05

Canonical source skills remain tracked; consumer skills are ignored dependencies.
Setup owns four anchored dependency ignore entries and schema-5 pin/hash provenance.
Bootstrap uses canonical exact Git objects, never latest, and writes only missing
skills after policy/project preflight. Consumer CI performs the same bootstrap.
Optional explicit install-skills installs shared bytes/provenance at a chosen root
(default ~/.agents/skills), without project policy/helpers or authentication changes.
Both installer paths reuse preflight/rollback and preserve edits and unrelated files.
Ubuntu initial catalog plus actual use is the first-release host gate; Cloud is deferred.


Schema-5 ignored dependencies require the runtime at `.agents/tools/workflow/`.
Ignored setup from an old runtime-layout bundle fails before writes; existing
schema-3/4 pins remain supported and tracked legacy setup stays explicit. CI
selects consumer provenance before any unrelated `.workflow/bundle.json`, fetches
that exact pin, and verification chooses the runtime recorded in its manifest.
PR metadata makes the same selection from the trusted base checkout only.

Transaction recovery binds file restoration to the recorded parent/ancestor inode
chain, not only destination bytes or absence. Replaced parent directories are
preserved with recovery metadata. Issue audit entry/label/state shapes are checked
inside the shared snapshot helper before dereferencing or phase classification.

Transaction mutations use directory-relative descriptors opened component by
component with no-follow and recorded inode checks. Parent-path checks detect
namespace changes; descriptor binding preserves replacement-directory human files
even when a swap occurs inside unlink/open/replace/restore/cleanup. Recovery remains
best-effort, without a multi-process lock or atomic multi-file promise.

After rename, destination identity/content must match the owned staged inode; a
foreign or changed destination remains a recoverable conflict. Snapshot helpers
validate and normalize optional native closure reasons before completion audits.

New private/staged directories use a short-lived inotify parent watch begun before
mkdir. A single creation event, matching path/descriptor identity and owner, and
mode0700 for private storage are required before use. Replacement, attribute/move/
delete events, queue overflow or missing support fail closed. The watch closes after
binding; it is not a task monitor, lock or workflow state engine.

Single-entry writes use Linux renameat2 exchange/no-replace to retain the actual
displaced destination for validation; rollback stages original content and deletion
captures an entry before validating/removing it. This does not make multi-file apply
atomic or provide a process lock. Unsupported primitives fail safely. PR-body
fragment links resolve against the supplied body; explicit file links still read
trusted head Git blobs in metadata checks.

Cleanup first captures public staging entries and created directory names in
exclusive private same-filesystem storage, then validates the actual captured inode
before removal. Restore collisions preserve both entries and record the quarantine
location; this is transient recovery storage, not workflow or task state.

Directory creation binds an opened privately staged inode before no-replace
publication. Private capture storage and empty captured directories remain retained:
there is no Linux conditional rmdir-by-opened-inode primitive. Repository storage
lives under .git; explicit shared-only installation uses a same-filesystem TMPDIR.
No project ignore rules, task state or index writes are introduced.

File finalization also retains captured entries instead of path-based unlink. This
preserves actual displaced/deleted bytes even if a private basename changes at the
finalization boundary. Recovery storage is intentionally retained, including after
successful replacement/uninstall, and is excluded from project/index/ignore state.

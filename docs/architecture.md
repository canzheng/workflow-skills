# Current architecture

The active entrypoint selects explicit github-v2 configuration and the short
contract; historical planning does not select execution. Three canonical authored
skills live only in .agents/skills: design-to-backlog, deliver-issue and risk-review.
Native Codex execution handles internal work; GitHub owns shared delivery identity
and state. There is no task-state service, feature ledger or synchronizer.

The Python standard-library utility entrypoint is tools/workflow/workflow.py.
core.py validates configuration/paths/provenance and computes actual content identity.
setup.py preflights pinned source assets/target ownership, stages backups and restores
on apply failure; installation provenance is generated only for consumers.
bootstrap.py is a read-only compatibility verifier for tracked skills; it no longer
fetches or materializes dependencies. Schema-3 provenance records tracked storage,
source URL/full SHA/hashes. Setup produces commit-ready skills; explicit migration
removes only a verified old schema-2 ignore block. All shared and project skills are
trackable. Fresh Git checkouts supply skills; repeat environment verification never
repairs missing files or rewrites policy/index. No cache/distribution database or
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
consumer verification and trusted-base PR metadata workflows ship as owned assets.
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

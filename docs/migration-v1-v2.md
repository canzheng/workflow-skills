# v1 to v2 migration

## Actual source baseline
Starting branch: `work`. Starting commit:
`d2aaf1904b2ccbe7fbab9733627e9c82fcf12f53`. Working tree was clean.
Rewrite branch: `rewrite/workflow-skills-v2`. No reset to the design reference
`27f86db43ad895a78e214a453df2069868118cb7` occurred; baseline remains reachable in Git.

## Inspected assets and dispositions
| Actual asset | Disposition |
| --- | --- |
| AGENTS.md / CLAUDE.md | Select v2 early; retain Python style, focused testing, relative paths, reversible edits, scoped commits and review obligations |
| skills/ (13 wrappers plus _workflow) | Inspect useful safety behavior; retire runtime at F13 |
| install.sh / AGENTS-global-workflow.md | Unsafe global default; retain baseline in Git, retire from distribution at F13 |
| environment.yml / bin/run-python.sh / unpinned requirements.txt | Replace required launcher with portable pinned development at F02 |
| tests/ and skills/_workflow/tests/ | Inspect by protected behavior; port safety regressions, retire ceremony assertions at F13 |
| docs/planning/versions/v1/BACKLOG.md | 19 DONE entries; BACKLOG/SHAPING/READY/IN_PROGRESS/DEFER empty; no active work to import |
| docs/planning, docs/lessons | Preserve historical evidence; never select v1 from directory presence |
| openspec/specs (six v1 contracts) | Reconcile current meanings at F07/F13 |
| openspec/changes/archive | Preserve historical contracts and decisions |

This is a bounded repository instruction cutover, not a global policy override.
Host policies remain applicable. Git history preserves all original assets.
Consumer migration and rollback procedures are implemented in F12.

## Consumer inventory and one-time cutover

```sh
python3 tools/workflow/workflow.py migrate inspect --repo /exact/repository --json
```

This command reads the known `docs/planning/versions/*/BACKLOG.md` sections and
linked feature metadata/OpenSpec records. It returns original record content,
old ID, paths, phase and proposed disposition. Missing/ambiguous/duplicated IDs,
changes, inconsistent Done/task metadata and unsafe paths produce findings; resolve
manually rather than guessing. Unknown formats require manual mapping. The starting source
had zero active and 19 historical Done. The final source has no v1 records; inspect
the recorded baseline to reproduce the historical inventory. Do not create fake
migration Issues.

For each active item, explicitly choose one disposition with the authorized owner:
finish v1, migrate once, defer, or cancel. A proposed inspector choice is not approval.
Freeze writes to each migrating ledger item before remote creation; preserve relevant
remaining acceptance/specs/evidence/blockers and the pre-cutover Git revision. Search
open and closed Issues by stable old source ID; reuse one match, stop on multiple.
After timeout/partial success re-read confirmed remote IDs before continuing. Keep a
link-only old-ID/Issue mapping, preserving human edits and unrelated labels.

Only after confirming the remote item, mark the old item read-only with its Issue
link or move the old ledger to labeled history. Enable v2 ownership once, then apply
the pinned repository bundle and remove conflicting active v1 instruction routing
with a reviewed bounded edit. Retaining history never selects v1. Items finishing
under v1 remain explicitly assigned there; do not make the same work writable in
both systems. Deferred/cancelled outcomes retain reasons and evidence; Done history
is not recreated. Missing write permission leaves authorized code work possible,
but cutover/remote confirmation stays pending.

## Rollback limits
Restore bundle/config/instruction ownership through a reviewed revert to the actual
pre-cutover revision; no hard reset discards newer work. Uninstall removes only
unmodified owned files/block and preserves config/modifications. Identify exact
residuals. Published Issues/PRs/history remain intact. If reverting live work to v1,
explicitly assign each open item's authority and leave rollback links. Never revive
two-way synchronization or delete remote history. Application data rollback is
outside this workflow. No user-global installation/configuration is changed here.

## Final source asset/test disposition

| Retired asset/test contract | Current proof / reason |
| --- | --- |
| Global installer tests / initialize scaffold | test_setup public pinned repo installation, preflight, modified assets, rollback and uninstall |
| Missing-worktree / duplicated resolver helpers | test_setup explicit Git-root/symlink failures and test_handoff missing/stale target rejection; no resolver engine retained |
| Structured review metadata/parser fields | test_risk emitted currency has real consumer; broken consumer fails L-001 proof, without a lifecycle engine |
| v1 shaping / backlog promotion | design-to-backlog skill exercise and test_records stable identity/dependencies; native Issues own state |
| v1 task wrappers / ledger / audit / repair / autonomous loop | Retired ceremony-specific contracts; no v2 task pointer, lifecycle wrappers or forced reviewer topology |
| v1 OpenSpec integration | test_openspec actual pinned validation/archive and partial-owner obligation; no blanket apply prohibition |
| v1 audit/remediation mutation corpora | Retired old linter/state APIs; current wrong-formula/consumer/assertion/target negative controls remain |
| Conda launcher and environment tests | Portable verify/clean-venv/missing-suite proof; Conda is not required |
| six old current OpenSpec specs | Replaced by implemented adoption/delivery/migration contracts and later checks/risk spec; original meanings retained in baseline Git history |
| docs/superpowers | Removed from final source; original remains in Git |
| docs/planning / docs/lessons / v1 archived changes | Removed from final source; original acceptance/evidence remains inspectable at baseline; zero active work |

The removed tests required APIs/ceremony intentionally replaced by v2; passing them
would falsely require the old system. Their safety meanings are covered by current
outcome tests, not just renamed assertions. No global files or historical Git commits
were removed. The final source has no v1-only history directory. The rewrite stays active for unperformed F14 environmental acceptance.

## Updated approved cleanup and exhaustive disposition

Human design clarifications on main at `e5747944a7e0520cf766db263834c8485fe63012`
were incorporated into the rewrite branch without resetting its actual baseline.
F13 now removes all v1-only planning/lesson/Superpowers/current/archive artifacts
from the final tree rather than retaining labeled copies. Intermediate labeled
history was removed to satisfy that updated contract. The source inventory is now
empty; inspect a temporary checkout of the baseline to reproduce the 19 Done result.

[Per-path disposition manifest](validation/v1-asset-disposition.json) accounts for
all 321 tracked baseline paths as delete, translate or current-v2, with destinations
and rationale. Primary-author review checked category meaning and final paths;
independent PR review remains pending. test_retirement validates coverage and a
clean clone; the manifest is fixed asset provenance, never a backlog/status ledger.
No active old-ID migration mapping is needed because there was no remaining work.

For prior global v1 installations, manually inspect the known global skill/policy
locations and remove/disable conflicting routing only with the user's authorization.
Doctor reports discoverable legacy/duplicate names but does not edit globals.
Keeping v1 for another repository requires explicit repository guidance preventing
its use here. This rewrite does not uninstall the user's global configuration.

Inspection validates OpenSpec archive roots and matching archive directories with
repository-relative symlink-safe checks. A symlinked archive cannot supply external
change evidence; report an unsafe/ambiguous change finding and resolve it deliberately.
Legacy BACKLOG.md files are also validated before reads; a ledger symlink is a finding
and cannot import unrelated external acceptance into migration candidates.

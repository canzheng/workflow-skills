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
manually rather than guessing. Unknown formats require manual mapping. This source
has zero active and 19 historical Done; do not create fake migration Issues.

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

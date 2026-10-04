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

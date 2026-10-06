# v2 candidate release and migration notes

This rewrite branch implements the approved v2 system and is available for review.
It has not merged or released. Required Ubuntu discovery/actual-use acceptance is verified in the independent
workstation session; final current-head source/consumer reviews passed and the rewrite
change is archived with post-archive checks recorded in the acceptance evidence.
Cloud is deferred by the user-approved 2026-10-05 scope change; see [actual evidence](validation/v2-acceptance.md).

V2 selects one short repository contract and three repository-scoped skills:
workflow-design-to-backlog, workflow-deliver-issue and workflow-risk-review.
GitHub Issues/PRs own shared work identity; ordinary fixes need no per-task ledger,
mandatory plan, wrapper lifecycle or forced reviewer. OpenSpec is proportional.

For a new project with an existing design, create the initial/MVP backlog in one
design-to-backlog run: delivery outcomes, design references, direct prerequisite
metadata and isolated unresolved decisions. One batch readiness approval does not
start execution. Reruns reuse identities and preserve human edits. The
[actual consumer pilot](validation/f14-consumer-pilot.md) exercises this entry point,
installed generic CI, the Ready-PR boundary and independently reviewed fixes;
verified Ubuntu host use and pending final merge obligations remain explicit. Consumer
required-check enforcement has actual configured/observed evidence.

Use the pinned source setup/doctor/check utilities in [operations](operations.md).
Setup defaults to dry-run, preserves unrelated instructions and user configuration,
rejects collisions/modified managed files and records provenance. Review changes
before explicit apply. Uninstall preserves modified assets and reports residuals.
Do not run the old global installer or old task wrappers.

For existing projects, follow [inventory/cutover/rollback](migration-v1-v2.md).
Known v1 formats have read-only inspection; ambiguous records need manual resolution.
No Done history is recreated, no two-way state synchronization is introduced, and
rollback preserves GitHub history. All 321 original source assets have explicit
[dispositions](validation/v1-asset-disposition.json); v1-only files are absent from
this source head, with original code and evidence available at the actual baseline.
Global skills/configuration are never changed automatically.

Runtime requires Python >=3.10 and Git. Full source verification uses pinned
OpenSpec 1.14.0 with Node >=20.19.0. Tested versions and commands are in
[development](development.md). GitHub access and native host skill discovery are
separate capabilities. Deterministic checks cannot certify semantic documentation,
Issue closure or merge protection; adoption of trusted-base checks and protection
configuration need their own observed evidence and authorization.

The default consumer setup tracks project policy/config, CI/templates,
docs/specs, project skills and schema-5 exact-source provenance. Shared skills and Python runtime in .agents/tools/workflow are
repo-local ignored dependencies, materialized before Ubuntu Codex starts. Only those
four dependency namespaces are ignored. Complete matching bootstrap repeats offline and does
not change tracked files/index; modified dependencies fail without overwrite.
Tracked schema-3 and mixed schema-4 consumers migrate explicitly; setup never untracks or stages.
Optional explicit global skills-only installation into ~/.agents/skills is supported,
without installing global project policy or changing authentication. No real global
installation was performed by this rewrite task; tests use isolated targets.
Ubuntu discovery/use and final review/archive are verified; authorized merge remains pending;
Cloud is deferred. This is not a published release.

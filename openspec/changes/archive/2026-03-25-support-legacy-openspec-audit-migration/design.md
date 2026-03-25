## Context

OpenSpec is now mandatory for the active workflow, but that assumption is too strict for repositories that adopt it after they already have a history of completed features. In a midstream migration, the canonical baseline specs should be created from the current behavior of the main checkout. Planned or partially implemented work should not be backfilled into the baseline; it should remain in roadmap/backlog planning artifacts or become active OpenSpec changes for the remaining work.

The current audit does not support that model. It requires every promoted feature to link to an active change directory, which makes historical `[DONE]` features invalid and also conflicts with the archive step for newly completed features.

## Goals / Non-Goals

**Goals:**
- Allow repositories to adopt OpenSpec midstream without fabricating retrospective changes for already-completed work.
- Preserve strict OpenSpec requirements for active shaping/execution work.
- Make `[DONE]` audit semantics compatible with archived OpenSpec changes.
- Keep migration behavior explicit rather than inferred from missing metadata.

**Non-Goals:**
- Reconstruct historical design intent for already-completed features.
- Relax OpenSpec requirements for current `[SHAPING]`, `[READY]`, or `[IN_PROGRESS]` work.
- Add a full migration automation skill in this change.

## Decisions

### Decision: Use an explicit legacy exemption marker for historical completed work
Historical completed features from before OpenSpec adoption should be explicitly marked rather than silently inferred from a missing change ID. This prevents the audit from accepting accidentally incomplete post-adoption features.

Chosen metadata:
- `- OpenSpec Status: `legacy-exempt``

This marker is valid only for historical `[DONE]` features created before OpenSpec adoption.

### Decision: Audit `[DONE]` features against archive state when they are OpenSpec-backed
If a completed feature records an OpenSpec change, audit should require archive state rather than active-change state:
- `openspec/changes/<change-id>/` must not exist
- exactly one `openspec/changes/archive/*-<change-id>/` directory must exist

This aligns audit with `finish-feature` and `openspec-archive-change`.

### Decision: Keep active-change requirements for non-completed active work
Features in `[SHAPING]`, `[READY]`, and `[IN_PROGRESS]` still require one active linked change. Midstream adoption should create change items for remaining work in those states.

## Risks / Trade-offs

- [Historical metadata churn] → Requiring an explicit exemption marker means some migrated feature files need a one-time edit, but the audit remains trustworthy.
- [False acceptance of incomplete post-adoption features] → Avoided by refusing to treat missing change metadata as implicitly legacy.
- [Deferred legacy work still ambiguous] → Leave `[DEFER]` behavior unchanged in this change and revisit separately if real repos need it.

## Migration Rule

For a legacy repo adopting OpenSpec:

1. Create baseline specs from the current behavior of the main checkout.
2. Leave planned-but-unimplemented work in `ROADMAP.md` and `BACKLOG.md`.
3. For historical completed features, mark the feature file `OpenSpec Status: legacy-exempt`.
4. For features currently in `[SHAPING]`, `[READY]`, or `[IN_PROGRESS]`, create OpenSpec changes that describe the remaining work to be done.
5. For newly completed post-adoption features, use the normal archive path rather than the legacy exemption.

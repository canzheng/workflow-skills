## Context

This repository already has a stable release-board and execution workflow centered on `docs/planning/current_version/BACKLOG.md`, per-feature files, audit checks, and feature worktrees. The missing piece is a canonical behavior-spec layer for shaping: today the feature file mixes workflow state, design prose, implementation planning, and task execution evidence in one place.

The agreed target is narrower than a full workflow replacement. `BACKLOG.md` remains the authority for queue order and feature status transitions. Execution still uses the current workflow wrappers, worktree rules, and validation evidence. OpenSpec becomes the authority for shaping artifacts and readiness inputs. Feature files become thin records that track execution state and link to the relevant OpenSpec change and specs.

## Goals / Non-Goals

**Goals:**
- Make one linked OpenSpec change the shaping/readiness authority for a promoted feature.
- Keep backlog ordering, feature-board state, and execution handoff under the existing workflow system.
- Reduce feature-file content to execution-oriented metadata, task progress, evidence, and OpenSpec links.
- Extend audit so OpenSpec-backed workflow states can be checked structurally rather than informally.

**Non-Goals:**
- Replace `BACKLOG.md` with OpenSpec as the release-planning board.
- Move task execution, worktree lifecycle, or final branch handling into OpenSpec.
- Require global workflow skills to depend on repo-local slash commands or generated `.codex/` instructions.
- Redesign `start-task` and `complete-task` in the same change beyond the metadata they depend on.

## Decisions

### Decision: Keep `BACKLOG.md` as the release-board authority
The version backlog already provides ordering, status sections, and release scope. OpenSpec does not currently offer an equivalent version-scoped backlog board. Keeping the existing board avoids duplicating release planning in OpenSpec.

Alternative considered:
- Let OpenSpec become the backlog authority. Rejected because the repo would need a custom release/queue layer that does not exist today and would blur OpenSpec’s change-centric model.

### Decision: Use one linked OpenSpec change per promoted feature
Each promoted feature will record one OpenSpec change ID as the shaping/readiness authority. This keeps the mapping deterministic for audit, repair, and wrappers.

Alternatives considered:
- Allow many changes per feature. Rejected because it complicates readiness checks and ownership.
- Allow one change to cover many promoted features. Rejected because it weakens feature-level state transitions and worktree ownership.

### Decision: Make feature files thin execution records
Feature files will keep feature identity, backlog reference, linked OpenSpec change/specs, execution task state, current task, and validation evidence. Design spec and implementation plan prose move out of the feature file and into OpenSpec artifacts.

Alternative considered:
- Continue dual-writing design and plan content into both OpenSpec and feature files. Rejected because it creates exactly the split-source drift this change is meant to remove.

### Decision: Extend audit with structural OpenSpec checks only
The audit should verify that required OpenSpec links and shaping/readiness artifacts exist, but it should not attempt deep semantic analysis of spec quality. OpenSpec validation remains the semantic/spec-focused tool.

Alternative considered:
- Parse OpenSpec semantics deeply inside `audit-workflow`. Rejected for the first integration because it would create a large, brittle validator instead of a narrow workflow guard.

### Decision: Keep global workflow skills dependent on artifact contracts, not repo-local slash commands
Global skills will read and validate `openspec/changes/<change-id>/` artifacts directly, and may use the OpenSpec CLI when available. They will not depend on generated `.codex/` skills or local `/opsx:*` commands.

Alternative considered:
- Have global skills wrap repo-local OpenSpec skills directly. Rejected because that couples reusable workflow automation to generated, repo-local agent scaffolding.

## Risks / Trade-offs

- [Feature-file template churn] → Update initializer/template and wrapper expectations together so planning artifacts do not drift.
- [Audit misses a meaningful readiness gap] → Limit the first integration to deterministic existence/linkage checks and add tests for expected failure modes.
- [Execution wrappers become inconsistent with new thin feature files] → Scope this change so shaping/readiness wrappers and audit are updated first, and explicitly defer deeper `start-task`/`complete-task` changes unless needed.
- [OpenSpec and workflow state diverge during adoption] → Treat the linked OpenSpec change as the shaping/readiness authority and avoid dual-writing planning prose into feature files.

## Migration Plan

1. Add OpenSpec-backed workflow requirements and the new integration capability.
2. Update the workflow contract, feature template, and wrapper skill docs to reflect thin feature files plus OpenSpec links.
3. Extend audit and repair helpers to validate linked change IDs and readiness prerequisites.
4. Update tests to cover OpenSpec-linked shaping/readiness cases.
5. Adopt the new model for future promoted features; migrate existing feature files only when they are touched next.

## Open Questions

- Should feature files contain a synchronized execution task ledger derived from OpenSpec `tasks.md`, or should `start-task` read OpenSpec tasks directly?
- Should `[DONE]` require an OpenSpec archive step, or remain independent from archive/final-branch handling?

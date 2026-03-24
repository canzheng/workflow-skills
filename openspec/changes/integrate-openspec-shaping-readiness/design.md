## Context

This repository already has a stable release-board and execution workflow centered on `docs/planning/current_version/BACKLOG.md`, per-feature files, audit checks, and feature worktrees. The missing piece is a canonical behavior-spec layer for shaping: today the feature file mixes workflow state, design prose, implementation planning, and task execution evidence in one place.

The agreed target is narrower than a full workflow replacement. `BACKLOG.md` remains the authority for queue order and feature status transitions. Execution still uses the current workflow wrappers, worktree rules, and validation evidence. OpenSpec becomes the authority for shaping artifacts, readiness inputs, and task status. Feature files become thin records that track workflow identity, links to the relevant OpenSpec change and specs, validation evidence, and any minimal execution context still required by the workflow engine.

## Goals / Non-Goals

**Goals:**
- Make OpenSpec a mandatory dependency of the workflow rather than an optional integration.
- Make one linked OpenSpec change the shaping/readiness authority for a promoted feature.
- Keep backlog ordering, feature-board state, and execution handoff under the existing workflow system.
- Reduce feature-file content to execution-oriented metadata, evidence, and OpenSpec links.
- Make OpenSpec `tasks.md` the authoritative task ledger used by `ready-feature`, `start-task`, and `complete-task`.
- Extend audit so OpenSpec-backed workflow states and OpenSpec task invariants can be checked structurally rather than informally.
- Require feature completion to pass through a workflow-owned OpenSpec validate/archive gate before generic branch finalization.

**Non-Goals:**
- Replace `BACKLOG.md` with OpenSpec as the release-planning board.
- Move worktree lifecycle or final branch handling into OpenSpec.
- Require global workflow skills to depend on repo-local slash commands or generated `.codex/` instructions.

## Decisions

### Decision: Make OpenSpec mandatory for the workflow
The workflow will require `openspec/` to exist and will assume OpenSpec artifacts are available in every adopting repository. This avoids carrying a fallback behavior for legacy planning-only repos inside the active workflow engine.

Alternative considered:
- Keep dual classic/hybrid behaviors. Rejected because it doubles the state model and prolongs migration complexity.

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
Feature files will keep feature identity, backlog reference, linked OpenSpec change/specs, current-task context if needed, and validation evidence. Design spec, implementation planning, task definitions, and task status move out of the feature file and into OpenSpec artifacts.

Alternative considered:
- Continue dual-writing design and plan content into both OpenSpec and feature files. Rejected because it creates exactly the split-source drift this change is meant to remove.

### Decision: Make OpenSpec tasks authoritative for execution
`openspec/changes/<change-id>/tasks.md` will define the execution tasks and carry their checkbox status. Workflow skills will read and update OpenSpec task status directly instead of maintaining a second authored task ledger in the feature file.

Alternative considered:
- Keep a synchronized execution task ledger in the feature file. Rejected as the steady state because it recreates a second mutable task source of truth.

### Decision: Extend audit with structural OpenSpec checks only
The audit should verify that required OpenSpec links and shaping/readiness artifacts exist, and that OpenSpec task status satisfies workflow invariants, but it should not attempt deep semantic analysis of spec quality. OpenSpec validation remains the semantic/spec-focused tool.

Alternative considered:
- Parse OpenSpec semantics deeply inside `audit-workflow`. Rejected for the first integration because it would create a large, brittle validator instead of a narrow workflow guard.

### Decision: Keep global workflow skills dependent on artifact contracts, not repo-local slash commands
Global skills will read and validate `openspec/changes/<change-id>/` artifacts directly, and may use the OpenSpec CLI when available. They will not depend on generated `.codex/` skills or local `/opsx:*` commands.

Alternative considered:
- Have global skills wrap repo-local OpenSpec skills directly. Rejected because that couples reusable workflow automation to generated, repo-local agent scaffolding.

### Decision: Add a workflow-owned feature completion gate before branch finishing
The generic branch-finishing skill should remain repo-agnostic. The workflow will therefore add its own `finish-feature` gate that validates the linked OpenSpec change, archives it, confirms filesystem-visible archive state, and only then hands off to branch finalization.

Alternative considered:
- Call `finishing-a-development-branch` directly and rely on operator discipline to archive first. Rejected because the archive gate is workflow-specific and should be enforced mechanically.

## Risks / Trade-offs

- [Feature-file template churn] → Update initializer/template and wrapper expectations together so planning artifacts do not drift.
- [Audit misses a meaningful readiness gap] → Limit the first integration to deterministic existence/linkage and task-status checks and add tests for expected failure modes.
- [OpenSpec task parsing becomes brittle] → Keep task syntax constrained to OpenSpec checkbox conventions and add parser coverage for representative task files.
- [OpenSpec and workflow state diverge during adoption] → Treat the linked OpenSpec change as the shaping and task authority and avoid dual-writing task sections into feature files.

## Migration Plan

1. Add mandatory-OpenSpec workflow requirements and the new integration capability.
2. Update the workflow contract, feature template, and wrapper skill docs to reflect links-plus-evidence feature files.
3. Extend audit, repair, and task-resolution helpers to validate linked change IDs, readiness prerequisites, and OpenSpec task status.
4. Update tests to cover OpenSpec-linked shaping/readiness and OpenSpec task parsing/execution.
5. Add a workflow-owned feature completion gate that proves archive state before branch finalization.
6. Adopt the new model for future promoted features; migrate existing feature files only when they are touched next.

## Open Questions

- Should feature files retain `Current Task`, or should current-task discovery be computed entirely from OpenSpec task state?

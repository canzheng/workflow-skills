---
name: ready-feature
description: Use when finishing shaping and promoting a feature into READY with at least one ready task
---

# Ready Feature

## Overview

This skill completes shaping for one feature and promotes it from `[SHAPING]` to `[READY]`.

It is a workflow wrapper around linked OpenSpec shaping artifacts, with optional `brainstorming` if the change still needs design clarification before the OpenSpec artifacts can justify readiness.

## Defaults

- If the user names a feature, use it.
- Otherwise select the first feature under `[SHAPING]` in the active version backlog.
- "First" means top-to-bottom document order.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target feature.
3. Confirm the feature is in `[SHAPING]`.
4. Review the feature file and linked OpenSpec change.
   - before the independent readiness review, retrieve relevant active lessons and record the returned lesson IDs in the feature file handoff notes under a task-scoped canonical `Retrieved Lesson IDs: ...` line for `ready`; use `none` when no lessons are returned
5. If the linked OpenSpec change is too weak to justify readiness, wrap `brainstorming` only long enough to strengthen the shaping output.
   - if `brainstorming` is used here, do not continue until its required review gates have passed
6. Confirm the linked OpenSpec change has the required shaping artifacts:
   - `proposal.md`
   - `design.md`
   - `tasks.md`
   - relevant linked spec paths
7. Review corresponding existing documentation for consistency with the shaped change, update any documentation that must change before the feature can honestly be considered ready, and otherwise make the no-update-needed conclusion explicit in the linked OpenSpec change.
8. Confirm at least one linked top-level OpenSpec task resolves to workflow status `ready` under the workflow task dependency convention.
9. Perform an independent readiness review before promotion:
   - spawn a `gpt-5.4-mini` subagent to review the selected `ready` task against `proposal.md`, `design.md`, linked specs, `tasks.md`, and corresponding existing docs
   - require that review to answer whether the shaping artifacts define the contract surface clearly enough that `start-task` can draft the task implementation plan without inventing or narrowing the acceptance contract
   - require that review to check for unresolved ambiguity, missing acceptance boundaries, or surrogate-proof risk that would force `start-task` to decide scope instead of inheriting it
   - do not promote the feature to `[READY]` unless the independent review passes
   - if the review finds gaps, return to shaping and strengthen the linked OpenSpec artifacts before retrying readiness
   - after the review and before promotion, reconcile whether the retrieved lessons materially influenced the readiness judgment and capture any strong new lesson candidates that would improve future readiness reviews
10. Update the feature file first, then move the backlog entry from `[SHAPING]` to the bottom of `[READY]`.
11. Re-run `audit-workflow`.
12. Commit the intentional planning-state changes when needed to leave the primary checkout clean before exiting.
13. Confirm the primary checkout is clean before exit.

## Rules

- Do not create `docs/superpowers/plans/` artifacts.
- This skill is planning-only. Run it from a clean primary checkout and do not create or reuse a feature worktree here.
- Leave the primary checkout clean before exiting this skill.
- A clean planning exit usually means committing the intentional readiness changes, but the invariant is a clean primary checkout.
- `brainstorming` owns any design-review gates used to strengthen the feature before planning.
- Preserve inherited validation and review gates. OpenSpec shaping does not relax audit, review, or verification requirements.
- Do not promote a feature to `[READY]` while known documentation drift remains in corresponding existing docs that should already reflect the shaped change.
- Do not promote the feature to `[READY]` unless at least one linked top-level OpenSpec task resolves to workflow status `ready`.
- Do not treat dependency-derived `ready` status as sufficient on its own; the independent readiness review must conclude that shaping already defines enough contract surface for `start-task` to draft against it safely.
- Preserve the existing feature file and update only relevant sections.
- Treat proof obligations and the validation taxonomy as part of the readiness contract, but gate them through the independent readiness review rather than through a shaping-owned execution artifact.

## Stop Conditions

- The target feature is not in `[SHAPING]`
- The feature file does not exist
- The linked OpenSpec change is too incomplete to justify readiness safely
- No task can honestly be marked `ready`
- The primary checkout cannot be left clean before exit
- `audit-workflow` reports an invalid workflow state

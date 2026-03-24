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
5. If the linked OpenSpec change is too weak to justify readiness, wrap `brainstorming` only long enough to strengthen the shaping output.
   - if `brainstorming` is used here, do not continue until its required review gates have passed
6. Confirm the linked OpenSpec change has the required shaping artifacts:
   - `proposal.md`
   - `design.md`
   - `tasks.md`
   - relevant linked spec paths
7. Confirm at least one linked OpenSpec task is ready to execute under the workflow dependency rules.
8. Update the feature file first, then move the backlog entry from `[SHAPING]` to the bottom of `[READY]`.
9. Re-run `audit-workflow`.
10. Commit the intentional planning-state changes when needed to leave the primary checkout clean before exiting.
11. Confirm the primary checkout is clean before exit.

## Rules

- Do not create `docs/superpowers/plans/` artifacts.
- This skill is planning-only. Run it from a clean primary checkout and do not create or reuse a feature worktree here.
- Leave the primary checkout clean before exiting this skill.
- A clean planning exit usually means committing the intentional readiness changes, but the invariant is a clean primary checkout.
- `brainstorming` owns any design-review gates used to strengthen the feature before planning.
- Preserve inherited validation and review gates. OpenSpec shaping does not relax audit, review, or verification requirements.
- Do not promote the feature to `[READY]` unless at least one linked OpenSpec task is `ready`.
- Preserve the existing feature file and update only relevant sections.

## Stop Conditions

- The target feature is not in `[SHAPING]`
- The feature file does not exist
- The linked OpenSpec change is too incomplete to justify readiness safely
- No task can honestly be marked `ready`
- The primary checkout cannot be left clean before exit
- `audit-workflow` reports an invalid workflow state

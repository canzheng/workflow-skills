---
name: ready-feature
description: Use when finishing shaping and promoting a feature into READY with at least one ready task
---

# Ready Feature

## Overview

This skill completes shaping for one feature and promotes it from `[SHAPING]` to `[READY]`.

It is a workflow wrapper around `writing-plans`, with optional `brainstorming` if the design is still too weak to plan from.

## Defaults

- If the user names a feature, use it.
- Otherwise select the first feature under `[SHAPING]` in the active version backlog.
- "First" means top-to-bottom document order.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target feature.
3. Confirm the feature is in `[SHAPING]`.
4. Review the feature file.
5. If the design section is too weak to plan from, wrap `brainstorming` only long enough to strengthen the design.
   - if `brainstorming` is used here, do not continue until its required review gates have passed
6. Wrap `writing-plans` and write the output into:
   - `## 5. Implementation Plan`
   - `## 6. Tasks`
   - do not promote the feature until the wrapped `writing-plans` review loop has approved the plan
7. Run `python "${CODEX_HOME:-$HOME/.codex}/skills/_workflow/scripts/sync_task_readiness.py" --feature-file <feature-file>` and ensure at least one task has status `ready`.
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
- `writing-plans` owns the mandatory plan-review loop for this skill. Do not move a feature to `[READY]` before that review has passed.
- Do not promote the feature to `[READY]` unless at least one task is `ready`.
- Preserve the existing feature file and update only relevant sections.

## Stop Conditions

- The target feature is not in `[SHAPING]`
- The feature file does not exist
- The design is too incomplete to plan from safely
- No task can honestly be marked `ready`
- The primary checkout cannot be left clean before exit
- `audit-workflow` reports an invalid workflow state

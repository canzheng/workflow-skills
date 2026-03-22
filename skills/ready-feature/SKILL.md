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
6. Wrap `writing-plans` and write the output into:
   - `## 5. Implementation Plan`
   - `## 6. Tasks`
7. Run `python "${CODEX_HOME:-$HOME/.codex}/skills/_workflow/scripts/sync_task_readiness.py" --feature-file <feature-file>` and ensure at least one task has status `ready`.
8. Update the feature file first, then move the backlog entry from `[SHAPING]` to the bottom of `[READY]`.
9. Re-run `audit-workflow`.

## Rules

- Do not create `docs/superpowers/plans/` artifacts.
- Do not promote the feature to `[READY]` unless at least one task is `ready`.
- Preserve the existing feature file and update only relevant sections.

## Stop Conditions

- The target feature is not in `[SHAPING]`
- The feature file does not exist
- The design is too incomplete to plan from safely
- No task can honestly be marked `ready`
- `audit-workflow` reports an invalid workflow state

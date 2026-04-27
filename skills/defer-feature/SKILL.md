---
name: defer-feature
description: Use when a shaping, ready, or in-progress feature should be moved to deferred with an explicit reason
---

# Defer Feature

## Overview

This skill moves one feature to `[DEFER]` and records why the work is being postponed or dropped.

## Defaults

- If the user names a feature, use it.
- Otherwise select the first feature in `[SHAPING]`, then `[READY]`, then `[IN_PROGRESS]`.
- "First" means top-to-bottom document order.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target feature.
3. Require an explicit deferral reason.
4. If a task is active, stop and ask how that task should be closed before deferring.
5. Record the reason in the feature file.
6. Move the backlog entry to `[DEFER]`. The entry remains heading-only; do not write the deferral reason under it.
7. Re-run `audit-workflow`.

## Rules

- Do not silently cancel an active task.
- Do not defer a feature without a reason.
- Keep edits minimal and local to the deferral change.

## Stop Conditions

- Missing deferral reason
- Active task state is ambiguous
- The target is already `[DONE]` or `[DEFER]`
- `audit-workflow` reports an invalid workflow state

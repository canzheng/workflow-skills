---
name: finish-feature
description: Use when a feature in `[IN_PROGRESS]` has satisfied its feature-level acceptance bar and branch finalization must be gated on linked OpenSpec validation and archive state
---

# Finish Feature

## Overview

This skill is the workflow-owned preflight for moving a feature from `[IN_PROGRESS]` to `[DONE]`.

It enforces the acceptance-plus-OpenSpec validate/archive gate for the linked change after task execution is complete, before handing off to the generic `finishing-a-development-branch` skill.

`finish-feature` is intentionally strict: completing the final task is not enough on its own. The expected handoff is that `complete-task` leaves the feature in `[IN_PROGRESS]`, and only a feature whose top-level OpenSpec tasks are all done and whose `Current Task` is `none` is startable here.

## Defaults

- If the user names a feature ID, use it.
- Otherwise select the only finishable feature in `[IN_PROGRESS]`.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target feature in `[IN_PROGRESS]`.
   - require all top-level OpenSpec tasks to be done and `Current Task` to be `none`
3. Read the linked feature file and confirm it records exactly one OpenSpec change.
4. Run the finish-feature resolver script to inspect active-vs-archived state for that change.
5. If the linked change is still active:
   - run the relevant OpenSpec validation command for the linked change
   - run `openspec-archive-change` for that exact change
   - rerun the resolver script and confirm the active change directory is gone and exactly one archive directory now exists
   - move the feature from `[IN_PROGRESS]` to `[DONE]` only after acceptance plus archive succeed
6. If the linked change is already archived:
   - confirm no active change directory still exists
   - confirm exactly one matching archive directory exists
   - move the feature from `[IN_PROGRESS]` to `[DONE]` only after acceptance is confirmed
7. Record the archive result and feature-completion evidence in the feature file when that evidence is not already present.
8. Re-run `audit-workflow` if the feature file changed.
9. Only after the linked change is validated and archived, invoke `finishing-a-development-branch`.

## Rules

- Do not call `finishing-a-development-branch` before the linked OpenSpec change is archived.
- This skill must run `openspec-archive-change` when the linked change is still active.
- Archive proof is filesystem state, not memory:
  - `openspec/changes/<change-id>/` must not exist
  - exactly one `openspec/changes/archive/*-<change-id>/` directory must exist
- If the feature is not in `[IN_PROGRESS]`, stop instead of trying to finish the branch early.
- A feature is not startable here unless all top-level OpenSpec tasks are done and `Current Task` is `none`.
- OpenSpec archive is additive. It does not replace task-level verification or feature-level acceptance.
- Keep the generic branch-finishing workflow generic; this skill owns the OpenSpec-specific gate.

## Stop Conditions

- Zero or multiple candidate finishable `[IN_PROGRESS]` features exist and no feature was named
- The target feature is not in `[IN_PROGRESS]`
- The feature file is missing `OpenSpec Change` metadata
- Top-level OpenSpec tasks are not all done
- `Current Task` is not `none`
- OpenSpec validation fails
- The archive result is ambiguous or missing
- `audit-workflow` reports an invalid workflow state

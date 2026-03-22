---
name: complete-task
description: Use when closing the active task, writing verification evidence, and updating task and feature state without finishing the feature branch
---

# Complete Task

## Overview

This skill verifies one active task, records evidence, and updates task and feature state.

It does not merge or clean up the feature branch/worktree. Branch finalization is separate and should use the existing finishing skill when the feature is complete.

## Defaults

- If the user names a task, use it.
- Otherwise select the only task in the repository with status `in_progress`.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target task.
3. Confirm it is the only task in the repository with status `in_progress`.
4. Wrap `verification-before-completion` and run the narrowest relevant verification.
5. Optionally wrap `requesting-code-review` if review tooling is available and the task changed code materially.
6. Update the feature file:
   - write exact validation evidence
   - mark the task `done`
   - run `python "${CODEX_HOME:-$HOME/.codex}/skills/_workflow/scripts/sync_task_readiness.py" --feature-file <feature-file>` to update downstream task readiness if dependencies are now satisfied
   - clear or update `Current Task`
7. If feature acceptance is satisfied, move the feature to the bottom of `[DONE]`. Otherwise keep it in `[IN_PROGRESS]`.
8. Re-run `audit-workflow`.
9. Report explicitly that the feature branch/worktree still exists and is not finalized unless downstream automation is closing a feature that just reached `[DONE]`.

## Rules

- No completion claim without fresh verification evidence.
- Do not finish the feature branch/worktree in this skill.
- A task may be `done` while the feature remains `[IN_PROGRESS]`, including contract-or-test tasks whose broader feature suite is still intentionally red.
- Use the repo feature file as the place to record evidence and downstream task changes.

## Stop Conditions

- Zero or multiple tasks are `in_progress`
- Verification fails
- Evidence cannot be recorded cleanly
- The target task is not `in_progress`
- `audit-workflow` reports an invalid workflow state

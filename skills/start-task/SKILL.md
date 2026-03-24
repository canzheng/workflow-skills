---
name: start-task
description: Use when starting the next ready task, ensuring the feature worktree exists, and executing task work under the repository workflow
---

# Start Task

## Overview

This skill starts one task, ensures the feature worktree is ready, and immediately executes that task.

It is a workflow wrapper around `using-git-worktrees` for feature-scoped isolation, followed by a task-scoped execution mode and the appropriate work method inside that mode. Task selection and task-status updates come from the linked OpenSpec change rather than a feature-file task ledger.

## Defaults

- If the user names a task, use it.
- Otherwise select:
  - the first feature under `[IN_PROGRESS]` in the active version backlog that still has a task with status `ready`
  - otherwise the first feature under `[READY]` in the active version backlog
  - then the first linked OpenSpec task in that feature with status `ready`
- "First" means top-to-bottom document order.
- For the default path, use `python "${CODEX_HOME:-$HOME/.codex}/skills/start-task/scripts/resolve_start_task.py"`.

## Workflow

1. Run `audit-workflow`.
2. Confirm there is no repository task already marked `in_progress`.
3. Resolve the target feature and task.
4. Confirm the feature is `[IN_PROGRESS]` or `[READY]`, the linked OpenSpec task is `ready`, and the feature has no task-readiness drift against the shared dependency model.
5. If this is the first executing task for the feature, confirm the primary checkout is clean so the worktree will be created from a clean commit. If the primary checkout is dirty, stop and resolve the changes explicitly instead of auto-committing them.
6. Wrap `using-git-worktrees`:
   - use the repo's preferred worktree root
   - if this is the first executing task for the feature, create one feature branch/worktree
   - otherwise re-enter or reuse the existing feature branch/worktree for that feature only
   - if reusing an existing feature worktree, stop unless that worktree is already clean and ready for the next task
7. Update the feature file:
   - set `Current Task`
8. Update the linked OpenSpec change:
   - mark the selected task `in_progress`
9. If the feature is currently `[READY]`, move the backlog entry to the bottom of `[IN_PROGRESS]`. If the feature is already `[IN_PROGRESS]`, leave the backlog entry there.
10. Re-run `audit-workflow`.
11. Choose execution mode:
   - prefer `subagent-driven-development` when available and still scoped to this one task
   - otherwise use `executing-plans`
12. Within the chosen execution mode, choose the work method:
   - use `systematic-debugging` when the task is primarily a debug task
   - use `test-driven-development` when the task is implementation or bugfix work with tests in scope
13. Execute the task work inside the selected feature worktree:
   - keep execution scoped to this one task
   - apply the chosen work method inside the chosen execution mode
   - stop only when the task is ready for `complete-task`, or when the task must be marked `blocked` or `cancelled`

## Rules

- Only one repository task may be `in_progress`.
- One task means one task ID and one bounded acceptance target.
- A feature in execution owns one feature branch/worktree reused across its sequential tasks.
- OpenSpec is the task-definition and task-status authority for this skill.
- Do not auto-commit dirty primary-checkout changes just to create a feature worktree.
- For later tasks on the same feature, resume in that existing feature worktree only; never switch the task back to the primary checkout or a different feature worktree.
- Do not start a second task while another is active.
- Keep any `subagent-driven-development` execution scoped to the one active task only.
- Treat `systematic-debugging` and `test-driven-development` as task methods inside the chosen execution mode, not as peer replacements for that mode.
- Do not finish the feature branch/worktree in this skill.

## Stop Conditions

- Another repository task is already `in_progress`
- The target feature is neither `[READY]` nor `[IN_PROGRESS]`
- The task is not `ready`
- Task scope is missing or invalid
- The primary checkout is dirty when the first feature worktree must be created
- The existing feature worktree is dirty when resuming a later task
- Worktree creation fails
- `audit-workflow` reports an invalid workflow state

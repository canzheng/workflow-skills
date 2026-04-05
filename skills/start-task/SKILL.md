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
- When naming a task explicitly, use the raw top-level OpenSpec task ID like `1`, not a synthetic label like `T1`.
- "First" means top-to-bottom document order.
- For the default path, use `python "${CODEX_HOME:-$HOME/.codex}/skills/start-task/scripts/resolve_start_task.py"`.

## Workflow

1. Run `audit-workflow`.
2. Confirm there is no repository task already marked `in_progress`.
3. Resolve the target feature and task from the correct checkout.
   - if this is the first executing task for the feature, resolve from the primary checkout before creating the feature branch/worktree
   - otherwise prefer the existing feature branch/worktree for that feature and require it instead of the primary checkout
   - do not continue later-task execution from the primary checkout
   - if a later task belongs to an existing `[IN_PROGRESS]` feature but no feature worktree is found, stop and ask the user to choose between:
     1. create a new feature worktree and continue there (recommended)
     2. stop
   - require the resolver payload to include the selected repo root, the linked OpenSpec change directory, the Markdown context file list under that change, and the task implementation-plan path
4. Confirm the feature is `[IN_PROGRESS]` or `[READY]`, the linked top-level OpenSpec task resolves to workflow status `ready`, and the feature has no workflow-derived task-readiness drift against the shared dependency model.
5. Read the linked change context before updating the task implementation plan.
   - read `proposal.md`, `design.md`, linked specs, `tasks.md`, and any other Markdown files under the linked change directory before drafting or updating the task implementation plan
   - use that context to update the task implementation plan at `openspec/changes/<change-id>/implementation-plans/<task-id>.md` before code execution starts
   - keep the implementation plan's validation section aligned with the selected task, the linked change intent, and the proof-obligation / validation-taxonomy language used by shaping and readiness guidance
6. Perform a semantic consistency and coverage review across the selected change context before code execution starts.
   - read the task implementation plan after updating it
   - spawn a `gpt-5.4-mini` reviewer subagent to review whether the task implementation plan and its validation section are semantically consistent with the selected task, the change proposal, the design, and the linked spec intent
   - require that review to confirm the plan and its validation section fully cover the selected task's intended change and proof obligations before execution continues, using the same validation taxonomy that the workflow reference and feature template describe
   - if the review finds semantic inconsistency, ambiguity, uncovered change intent, or missing validation coverage, return to step 5 to update the implementation plan and rerun this review until it passes
7. If this is the first executing task for the feature, confirm the primary checkout is clean so the worktree will be created from a clean commit. If the primary checkout is dirty, stop and resolve the changes explicitly instead of auto-committing them.
8. Wrap `using-git-worktrees`:
   - use the repo's preferred worktree root
   - if this is the first executing task for the feature, create one feature branch/worktree
   - otherwise re-enter or reuse the existing feature branch/worktree for that feature only; never fall back to the primary checkout for a later task
   - if no feature worktree exists for a later task, ask the user whether to create one now or stop; recommend creating the worktree
   - if reusing an existing feature worktree, stop unless that worktree is already clean and ready for the next task
9. Update the feature file to record active execution:
   - set `Current Task` to the selected top-level task ID
   - keep OpenSpec `tasks.md` as the checked/unchecked task ledger rather than inventing a separate native `in_progress` syntax
10. If the feature is currently `[READY]`, move the backlog entry to the bottom of `[IN_PROGRESS]`. If the feature is already `[IN_PROGRESS]`, leave the backlog entry there.
11. Re-run `audit-workflow`.
12. Choose execution mode:
   - prefer `subagent-driven-development` when available and still scoped to this one task
   - otherwise use `executing-plans`
13. Within the chosen execution mode, choose the work method:
   - use `systematic-debugging` when the task is primarily a debug task
   - use `test-driven-development` when the task is implementation or bugfix work with tests in scope
14. Execute the task work inside the selected feature worktree:
   - if the resolver selected an existing feature worktree, re-enter that repo root before reading change context, updating the implementation plan, or editing code
   - keep execution scoped to this one task
   - use the already-reviewed change context as the execution baseline, and if later edits introduce new semantic inconsistency between the task plan and the linked change artifacts, stop and reconcile before continuing
   - apply the chosen work method inside the chosen execution mode
   - stop only when the selected task's implementation work is complete and every step in the implementation plan's validation section has been completed successfully, leaving only the fresh completion-time verification gate owned by `complete-task`, or when the task must be marked `blocked` or `cancelled`

## Rules

- Keep any `subagent-driven-development` execution scoped to the one active task only.
- Treat `systematic-debugging` and `test-driven-development` as task methods inside the chosen execution mode, not as peer replacements for that mode.
- Do not finish the feature branch/worktree in this skill.

## Stop Conditions

- Another repository task is already `in_progress`
- The target feature is neither `[READY]` nor `[IN_PROGRESS]`
- The task is not `ready`
- Task scope is missing or invalid
- The task implementation plan cannot be written or updated before execution begins
- The `gpt-5.4-mini` semantic consistency and coverage review finds inconsistency, ambiguity, unresolved drift, or missing validation coverage between the task implementation plan and the linked proposal, design, specs, or selected task
- The primary checkout is dirty when the first feature worktree must be created
- A later task for an existing `[IN_PROGRESS]` feature has no feature worktree and the user chooses to stop instead of creating one
- The existing feature worktree is dirty when resuming a later task
- Worktree creation fails
- `audit-workflow` reports an invalid workflow state

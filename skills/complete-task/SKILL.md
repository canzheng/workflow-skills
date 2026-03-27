---
name: complete-task
description: Use when closing the active task, writing verification evidence, and updating task and feature state without finishing the feature branch
---

# Complete Task

## Overview

This skill verifies one active task, records evidence, and updates task and feature state.

It does not merge or clean up the feature branch/worktree. Branch finalization is separate and should use `finish-feature` once the feature is complete.

## Defaults

- If the user names a task, use it.
- Otherwise select the only task in the repository with status `in_progress`.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target task.
   - require the resolver payload to include the linked OpenSpec change directory, the Markdown context file list under that change, and the task implementation-plan path
3. Confirm it is the only task in the repository with status `in_progress`.
4. Wrap `verification-before-completion` and run the narrowest relevant verification.
   - do not mark the task `done` until this verification gate has passed with fresh evidence
5. Confirm the execution-path review expectation has been satisfied:
   - if the task ran through `subagent-driven-development`, confirm its required per-task reviews already passed before completion
   - if the task ran through `executing-plans`, wrap `requesting-code-review` whenever this task closes a review batch, materially completes a feature, or otherwise reaches a review checkpoint
6. Confirm the active feature worktree contains only intended task changes and will be left clean after completion. Use repo-appropriate checks such as `git status --short` and `git diff --check`.
   - read the files listed as context before completing the task so validation and task closure are checked against the authoritative change artifacts
7. Update the feature file:
   - write exact validation evidence
   - clear or update `Current Task`
   - record any handoff notes needed for the next task
8. Update the linked OpenSpec change:
   - mark the completed task `done`
   - rely on the workflow `Depends On` convention parsed from the linked OpenSpec task file to expose downstream ready work
9. Commit the intended task changes, including the task-state updates that live on the feature branch, whenever needed to leave the feature worktree clean for the next handoff.
10. Confirm the feature worktree is clean and ready for reuse on the next task.
11. Keep the feature in `[IN_PROGRESS]` after task closure.
   - treat the final-task handoff as an explicit decision point:
     - if the completed task was not the last top-level OpenSpec task, the feature stays `[IN_PROGRESS]` and the next ready task becomes the handoff target
     - if the completed task was the last top-level OpenSpec task, the feature still remains `[IN_PROGRESS]` and `finish-feature` becomes the handoff target once `Current Task` is cleared
12. Re-run `audit-workflow`.
13. Report explicitly that the feature branch/worktree still exists and is not finalized.

## Rules

- Verification and review are separate requirements: verification proves the completion claim, while review satisfies the execution-path quality gate.
- Do not bypass review requirements inherited from the execution method that produced the task changes.

## Stop Conditions

- Zero or multiple tasks are `in_progress`
- Verification fails
- Evidence cannot be recorded cleanly
- The required execution-path review has not been satisfied
- The feature worktree cannot be left clean for the next handoff
- The target task is not `in_progress`
- `audit-workflow` reports an invalid workflow state

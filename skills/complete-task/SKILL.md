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
   - rely on OpenSpec task dependencies to expose downstream ready work
9. Commit the intended task changes, including the task-state updates that live on the feature branch, whenever needed to leave the feature worktree clean for the next handoff.
10. Confirm the feature worktree is clean and ready for reuse on the next task.
11. If feature acceptance is satisfied, move the feature to the bottom of `[DONE]`. Otherwise keep it in `[IN_PROGRESS]`.
12. Re-run `audit-workflow`.
13. Report explicitly that the feature branch/worktree still exists and is not finalized unless downstream automation is closing a feature that just reached `[DONE]` and is about to hand off to `finish-feature`.

## Rules

- `verification-before-completion` is a mandatory gate for this skill, not an optional check.
- No completion claim without fresh verification evidence.
- Verification and review are separate requirements: verification proves the completion claim, while review satisfies the execution-path quality gate.
- Do not bypass review requirements inherited from the execution method that produced the task changes.
- Leave the feature worktree clean before handing off to the next task.
- A clean handoff usually means committing the task's intended changes, but the invariant is a clean feature worktree, not a fixed number of commits.
- Do not finish, repurpose, or clean up the feature branch/worktree in this skill.
- A task may be `done` while the feature remains `[IN_PROGRESS]`, including contract-or-test tasks whose broader feature suite is still intentionally red.
- Use the repo feature file as the place to record evidence and handoff notes. Use OpenSpec as the task-definition and task-status authority.
- Execution context must be explicit. Provide the linked OpenSpec change directory plus the Markdown context file list to the executor instead of relying on implied context.

## Stop Conditions

- Zero or multiple tasks are `in_progress`
- Verification fails
- Evidence cannot be recorded cleanly
- The required execution-path review has not been satisfied
- The feature worktree cannot be left clean for the next handoff
- The target task is not `in_progress`
- `audit-workflow` reports an invalid workflow state

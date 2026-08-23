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
- For the default path, use `python "${AGENTS_HOME:-$HOME/.agents}/skills/start-task/scripts/resolve_start_task.py"`.
- When the caller already knows the feature and task IDs (for example, from the autonomous-backlog-loop resolver, or when the user named a task explicitly), pass `--feature-id <feature-id> --task-id <task-id>` to take the explicit-ID fast path. The fast path skips BACKLOG-wide scanning and the cross-worktree fanout, and runs only the per-task validation. The two flags must be supplied together.

## Workflow

Create or re-enter the feature worktree early, before any heavy planning or review work, so the primary checkout is freed for concurrent `shape-backlog-item`, `ready-feature`, or other features' `start-task` work. Steps 1–4 are read-only against the primary checkout; steps 5–6 create the worktree; every step from 7 onward runs inside the feature worktree.

**Hard ordering rule.** Do not read change context or draft/update the task implementation plan in the primary checkout. These belong to step 7 inside the feature worktree. If the resolver reports `implementation_plan_status: missing`, that is expected — proceed to steps 5–6 to create the worktree, then draft the plan inside the worktree at step 7. Never write the plan or do context-reading in the primary checkout and then roll back.

1. Run `audit-workflow`.
2. Confirm there is no repository task already marked `in_progress`.
3. Resolve the target feature and task from the correct checkout.
   - if this is the first executing task for the feature, resolve from the primary checkout before creating the feature branch/worktree
   - otherwise prefer the existing feature branch/worktree for that feature and require it instead of the primary checkout
   - do not continue later-task execution from the primary checkout
   - if a later task belongs to an existing `[IN_PROGRESS]` feature but no feature worktree is found, stop and ask the user to choose between:
     1. create a new feature worktree and continue there (recommended)
     2. stop
   - require the resolver payload to include the selected repo root, the linked OpenSpec change directory, the Markdown context file list under that change, the task implementation-plan path, and the implementation-plan status (`present` or `missing`)
   - if the resolver returns `implementation_plan_status: missing`, do NOT draft the plan here. Proceed to steps 5–6; the plan is drafted inside the worktree at step 7.
4. Confirm the feature is `[IN_PROGRESS]` or `[READY]`, the linked top-level OpenSpec task resolves to workflow status `ready`, and the feature has no workflow-derived task-readiness drift against the shared dependency model.
5. If this is the first executing task for the feature, confirm the primary checkout is clean so the worktree will be created from a clean commit. If the primary checkout is dirty, stop and resolve the changes explicitly instead of auto-committing them.
6. Wrap `using-git-worktrees` to create or re-enter the feature worktree before any heavy planning or review work:
   - use the repo's preferred worktree root
   - if this is the first executing task for the feature, create one feature branch/worktree
   - otherwise re-enter or reuse the existing feature branch/worktree for that feature only; never fall back to the primary checkout for a later task
   - if no feature worktree exists for a later task, ask the user whether to create one now or stop; recommend creating the worktree
   - if reusing an existing feature worktree, stop unless that worktree is already clean and ready for the next task
   - all subsequent steps run inside this feature worktree so the primary checkout stays free for other features
7. From inside the feature worktree, read the linked change context before drafting or updating the task implementation plan. All substeps here must run inside the worktree; do not read context or write the plan in the primary checkout.
   - read `proposal.md`, `design.md`, linked specs, `tasks.md`, and any other Markdown files under the linked change directory before drafting or updating the task implementation plan
7.1. PER-TASK CONTRACT READINESS — ask this BEFORE drafting the plan, because it is a question about the CONTRACT, not about the plan.
   - spawn a lightweight independent reviewer over `proposal.md`, `design.md`, the linked specs, and this task's entry in `tasks.md`, asking one question: do the shaping artifacts define THIS task's contract surface clearly enough to draft against without inventing or narrowing the acceptance contract?
   - require it to name any unresolved ambiguity, missing acceptance boundary, or surrogate-proof risk that would force this step to decide scope instead of inheriting it
   - if it finds gaps, STOP and strengthen the linked OpenSpec artifacts before drafting the plan. A gap found here is cheap; the same gap found at `finish-feature` is not.
   - record the verdict in the feature file handoff notes using canonical `Review Scope: task_readiness`, `Review Target: <feature-id>/<task-id>`, `Review Verdict`, `Blocking Findings`, and `Review Terminal` lines
   - MEASURE A DATA-DEPENDENT CRITERION BEFORE APPROVING IT, when and only when the contract names a threshold, cut-off, ranking or selection rule that ranges over data the repository can already query. In that situation the reviewer cannot settle it: a read-only reviewer can see that a rule is UNSPECIFIED but not that a specified one is WRONG, and the artifacts read equally well either way. Run the rule against the data and record what it selects before the verdict, not after.
     - measured on `v1-f006` task 3: design D3b named a floor criterion, passed round 1, and was found degenerate at round 2 only because the objection prompted someone to run it -- no candidate value in the range punched a hole in any slice, so the rule had no upper bound and would have erased nearly all of one slice's history, which is the exact failure the decision existed to prevent
     - the situational test is whether the data exists to run it against. A criterion over data not yet collected, or over a system not yet built, is approved on its reasoning as before; this clause adds nothing there.
     - when a reviewer raises a theoretical objection about such a rule, the answer is a measurement rather than another round of prose. Rounds 2 and 3 above would have been one round.
   - this replaces the feature-level readiness review that `ready-feature` used to run. That one reviewed the first task and promoted all of them: on `v1-f010` task `1` was reviewed, tasks `2`-`6` were not, and every contract-surface defect its nine feature gates found lived in tasks 2-6. Asking per task is also better than asking once, because shaping is often amended between tasks.
7.2. Draft or update the task implementation plan, now that the contract has been confirmed draftable.
   - draft (when the resolver returned `implementation_plan_status: missing`) or update (when `present`) the plan at `openspec/changes/<change-id>/implementation-plans/<task-id>.md` before code execution starts
   - keep the implementation plan's validation section aligned with the selected task, the linked change intent, and the proof-obligation / validation-taxonomy language used by shaping and readiness guidance
   - EVERY executable task gets a plan. There is no path that skips it: all three deterministic gates below key on the plan file, so a task executed without one silently receives none of them. On `v1-f010` task 6 had no plan, never had one, and carried the longest defect tail of any task — blocking findings at four separate gates.
7.4. Run a deterministic pinned-claim evidence lint over the linked change after the task implementation plan is drafted or updated:
   - from inside the feature worktree, run `python "${AGENTS_HOME:-$HOME/.agents}/skills/_workflow/scripts/lint_openspec_claim_evidence.py" "openspec/changes/<linked-change-id>"`
   - it flags any plan/design line containing a file:line citation or numeric pin without an adjacent grep/Read evidence block, including the task implementation plan
   - if the lint fails, return to step 7, add the adjacent evidence block or remove the unsupported pinned claim, and re-run the lint before invoking the reviewer
7.5. Run a deterministic dry-run of the `complete-task` implementation-plan validator over the authored plan, before spawning the round-1 reviewer:
   - from inside the feature worktree, run `python "${AGENTS_HOME:-$HOME/.agents}/skills/start-task/scripts/dry_run_plan_validation.py" <implementation-plan-path>`
   - this runs the same `validate_implementation_plan_file` and `required_validation_evidence_categories_for_plan` checks `complete-task` enforces at closure, so plan-contract violations surface now instead of at completion: missing `## Contract Surface` / `## Proof Obligations` / `## Validation Plan`, missing or non-bare-name `### Required Validation Classes` bullets, or a runtime-facing contract surface with neither a runtime-facing validation class nor an explicit unit-only justification
   - if the dry-run fails, return to step 7, fix the implementation plan, and re-run the dry-run until it passes before invoking the reviewer
8. Perform a semantic consistency and coverage review across the selected change context before code execution starts.
   - read the task implementation plan after updating it
   - spawn a lightweight independent reviewer subagent to review whether the task implementation plan and its validation section are semantically consistent with the selected task, the change proposal, the design, and the linked spec intent
   - require that review to confirm the plan and its validation section fully cover the selected task's intended change and proof obligations before execution continues, using the same validation taxonomy that the workflow reference and feature template describe
   - if tests are being added or modified, ask the mandatory review question "changed tests narrowed contract?" and compare the new assertions to the task plan, not just the implementation
   - if the review finds semantic inconsistency, ambiguity, uncovered change intent, or missing validation coverage, return to step 7 to update the implementation plan and rerun this review until it passes
   - **record `Plan Review Round: <n>` in the feature file handoff notes on every invocation of this review**, incrementing it each time, so the loop can see its own length. `finish-feature`'s gate loop carries `Gate Iteration` for the same reason; this loop had no equivalent, so a plan review that ran five times looked identical in the record to one that ran once.
     - this is a COUNTER, not a cap. Nothing here stops at a round number, because a plan that is still wrong on round four should still be fixed.
     - what it is for: this loop reviews a DOCUMENT and fixes it by rewriting the document, so each round produces new prose for the next round to read. That shape is self-sustaining when it goes wrong, and the only cheap way to notice is to be able to count. Measured across the features recorded so far, `task_readiness` verdicts have gone non-terminal 0 times out of 10 and this review has never iterated in the record — so the counter is there to show a change from that, not because a cost has been observed.
     - if the round number reaches 3, say so plainly in the handoff note and state what each round changed. A loop that has rewritten the same plan three times is more likely to be reporting an unclear CONTRACT than an unclear plan, and the fix for that is step 7.1's stop-and-strengthen, not a fourth rewrite.
9. Update the feature file to record active execution:
   - set `Current Task` to the selected top-level task ID
   - keep OpenSpec `tasks.md` as the checked/unchecked task ledger rather than inventing a separate native `in_progress` syntax
10. If the feature is currently `[READY]`, move the backlog entry to the bottom of `[IN_PROGRESS]`. If the feature is already `[IN_PROGRESS]`, leave the backlog entry there.
11. Re-run `audit-workflow`.
12. Choose execution mode:
   - prefer `subagent-driven-development` when available and still scoped to this one task
   - otherwise use `executing-plans`
   - when wrapping either execution mode, explicitly override its generic "execute all tasks" or "commit" guidance with this workflow boundary: Execute only the selected top-level OpenSpec task from `openspec/changes/<change-id>/implementation-plans/<task-id>.md`; do not mark the selected OpenSpec task checkbox done, do not clear `Current Task`, do not commit task-closure state, and do not start implementation work for any downstream top-level OpenSpec task
13. Within the chosen execution mode, choose the work method:
   - use `systematic-debugging` when the task is primarily a debug task
   - use `test-driven-development` when the task is implementation or bugfix work with tests in scope
14. Execute the task work inside the selected feature worktree:
   - if the resolver selected an existing feature worktree, re-enter that repo root before reading change context, updating the implementation plan, or editing code
   - keep execution scoped to this one task
   - use the already-reviewed change context as the execution baseline, and if later edits introduce new semantic inconsistency between the task plan and the linked change artifacts, stop and reconcile before continuing
   - as each planned validation step completes, record its `Run`, `Result`, and `Evidence` entry in the feature file's validation log instead of deferring evidence capture to `complete-task`
   - apply the chosen work method inside the chosen execution mode
   - stop only when the selected task's implementation work is complete, every step in the implementation plan's validation section has been completed successfully, and the corresponding execution-time evidence has been recorded, leaving only the fresh completion-time reconciliation gate owned by `complete-task`, or when the task must be marked `blocked` or `cancelled`

## Rules

- Keep any `subagent-driven-development` execution scoped to the one active task only.
- `start-task` owns task execution, not task closure: the selected OpenSpec task checkbox, `Current Task: none`, and closure commit belong to `complete-task`.
- Treat `systematic-debugging` and `test-driven-development` as task methods inside the chosen execution mode, not as peer replacements for that mode.
- Do not finish the feature branch/worktree in this skill.

## Stop Conditions

- Another repository task is already `in_progress`
- The target feature is neither `[READY]` nor `[IN_PROGRESS]`
- The task is not `ready`
- Task scope is missing or invalid
- The task implementation plan cannot be written or updated before execution begins
- The per-task contract-readiness review (step 7.1) finds the shaping artifacts inadequate for this task
- The linked change has a plan/design file:line citation or numeric pin without adjacent grep/Read evidence
- The deterministic `complete-task` plan-validator dry-run cannot be made to pass before the reviewer is spawned
- The independent reviewer subagent's semantic consistency and coverage review finds inconsistency, ambiguity, unresolved drift, or missing validation coverage between the task implementation plan and the linked proposal, design, specs, or selected task
- The primary checkout is dirty when the first feature worktree must be created
- A later task for an existing `[IN_PROGRESS]` feature has no feature worktree and the user chooses to stop instead of creating one
- The existing feature worktree is dirty when resuming a later task
- The execution flow attempts to mark the selected task done, commit task-closure state, or start another top-level OpenSpec task before `complete-task`
- Worktree creation fails
- `audit-workflow` reports an invalid workflow state

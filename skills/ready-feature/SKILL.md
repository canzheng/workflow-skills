---
name: ready-feature
description: Use when finishing shaping and promoting a feature into READY with at least one ready task
---

# Ready Feature

## Overview

This skill completes shaping for one feature and promotes it from `[SHAPING]` to `[READY]`.

It is a workflow wrapper around linked OpenSpec shaping artifacts, with optional `brainstorming` if the change still needs design clarification before the OpenSpec artifacts can justify readiness.

## Defaults

- If the user names a feature, use it.
- Otherwise select the first feature under `[SHAPING]` in the active version backlog.
- "First" means top-to-bottom document order.

## Workflow

1. Run `audit-workflow`.
2. Resolve the target feature.
3. Confirm the feature is in `[SHAPING]`.
4. Review the feature file and linked OpenSpec change.
5. If the linked OpenSpec change is too weak to justify readiness, wrap `brainstorming` only long enough to strengthen the shaping output.
   - if `brainstorming` is used here, do not continue until its required review gates have passed
6. Confirm the linked OpenSpec change has the required shaping artifacts:
   - `proposal.md`
   - `design.md`
   - `tasks.md`
   - relevant linked spec paths
6.5. Run a deterministic openspec-archive readiness check on the linked change:
   - run `python "${AGENTS_HOME:-$HOME/.agents}/skills/ready-feature/scripts/check_archive_readiness.py" --change-id <linked-change-id>`
   - it flags any delta `## MODIFIED` requirement whose `### Requirement:` header differs from the main spec without a `## RENAMED Requirements` bridge mapping the old main-spec header to the new one
   - if it reports issues, return to shaping and add the required `## RENAMED` bridge (or correct the MODIFIED header) before promotion, so the change does not fail only at archive time
6.6. Run a deterministic pinned-claim evidence lint on the linked change:
   - run `python "${AGENTS_HOME:-$HOME/.agents}/skills/_workflow/scripts/lint_openspec_claim_evidence.py" "openspec/changes/<linked-change-id>"`
   - it flags any plan/design line containing a file:line citation or numeric pin without an adjacent grep/Read evidence block
   - if it reports issues, return to shaping and add the adjacent evidence block or remove the unsupported pinned claim before promotion
7. Review corresponding existing documentation for consistency with the shaped change, update any documentation that must change before the feature can honestly be considered ready, and otherwise make the no-update-needed conclusion explicit in the linked OpenSpec change.
8. Confirm at least one linked top-level OpenSpec task resolves to workflow status `ready` under the workflow task dependency convention.
9. Do NOT perform a feature-level readiness review. Readiness is judged PER TASK, in `start-task`, immediately before that task runs.
   - This step used to spawn a reviewer against the one selected `ready` task and then promote the whole feature. That is not a small version of the right check — it licenses every task on the evidence of one, and it reads as though the feature's contract has been reviewed when only a single task's has.
   - Measured on `v1-f010`: the recorded readiness verdict covered task `1`; tasks `2`-`6` were never contract-reviewed; and **every contract-surface defect its nine feature gates found lived in tasks 2-6** — the units seam, the sigma-vs-E|move| basis, and an audit whose scope was wrong by 4x.
   - Judging readiness per task is also strictly better than judging it once up front, because shaping is frequently amended between tasks, so a task-5 contract is best assessed when task 5 is about to run.
   - The deterministic checks in steps 6.5 and 6.6 remain gating here: they are cheap, they are feature-wide, and they catch archive-time and evidence failures that no per-task review would look for.
10. Update the feature file first, then move the backlog entry from `[SHAPING]` to the bottom of `[READY]`.
11. Re-run `audit-workflow`.
12. Commit the intentional planning-state changes when needed to leave the primary checkout clean before exiting.
13. Confirm the primary checkout is clean before exit.

## Rules

- Do not create `docs/superpowers/plans/` artifacts.
- This skill is planning-only. Run it from a clean primary checkout and do not create or reuse a feature worktree here.
- Leave the primary checkout clean before exiting this skill.
- A clean planning exit usually means committing the intentional readiness changes, but the invariant is a clean primary checkout.
- `brainstorming` owns any design-review gates used to strengthen the feature before planning.
- Preserve inherited validation and review gates. OpenSpec shaping does not relax audit, review, or verification requirements.
- Do not promote a feature to `[READY]` while known documentation drift remains in corresponding existing docs that should already reflect the shaped change.
- Do not promote the feature to `[READY]` unless at least one linked top-level OpenSpec task resolves to workflow status `ready`.
- Do not treat dependency-derived `ready` status as a statement about contract quality. It is a dependency fact only; the contract question is asked per task in `start-task`.
- Preserve the existing feature file and update only relevant sections.
- Treat proof obligations and the validation taxonomy as part of the readiness contract, but gate them per task in `start-task` rather than through a shaping-owned execution artifact or a feature-wide review.

## Stop Conditions

- The target feature is not in `[SHAPING]`
- The feature file does not exist
- The linked OpenSpec change is too incomplete to justify readiness safely
- The linked OpenSpec change has a delta `## MODIFIED` requirement whose header differs from the main spec without a `## RENAMED` bridge
- The linked OpenSpec change has a plan/design file:line citation or numeric pin without adjacent grep/Read evidence
- No task can honestly be marked `ready`
- The primary checkout cannot be left clean before exit
- `audit-workflow` reports an invalid workflow state

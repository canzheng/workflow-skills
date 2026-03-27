<!-- Beginning of Workflow Section -->

<!-- DO NOT EDIT BELOW SECTION MANUALLY. It is maintained by automated script -->

## Workflow Applicability
- Apply the workflow rules below to repositories that adopt the planning artifact structure under `docs/planning/`.
- This workflow requires `openspec/` and assumes OpenSpec artifacts are available once the workflow is adopted.
- Treat any repo-local `AGENTS.md` as an overlay for project-specific constraints, not a second source of truth for the full workflow contract unless the repo explicitly says otherwise.
- The canonical workflow definitions, status models, artifact ownership, and shared structural rules live in `docs/planning/WORKFLOW_REFERENCE.md`.
- Individual `SKILL.md` files own skill-specific execution steps, gates, and stop conditions.

## Workflow Core Principle
- One feature = one feature file for workflow identity/evidence + one linked OpenSpec change for shaping and task truth.
- Always prefer updating existing workflow artifacts in place over creating parallel files or duplicate summaries.
- Do not mix levels.

## Workflow Skill Routing
- Use `initialize-workflow-artifacts` when a repository wants to adopt this workflow but does not yet have the required scaffold.
- Use `diagnose-workflow` for a non-blocking workflow health snapshot before deciding whether to audit, repair, defer, or continue.
- Use `audit-workflow` before and after planning-state edits, and whenever a workflow action needs a deterministic validity gate.
- Use `shape-backlog-item` instead of raw `brainstorming` when promoting backlog work into shaped features.
- Use `ready-feature` instead of raw `writing-plans` when finishing shaping and promoting a feature into `[READY]`.
- Use `start-task` to begin execution, `complete-task` to close the active task, and `repair-drift` to fix minimal workflow-state inconsistencies.
- Use `finish-feature` when an accepted feature in `[IN_PROGRESS]` is ready to move to `[DONE]` before any generic branch-finalization workflow.
- Use `autonomous-backlog-loop` only when the goal is to keep advancing eligible workflow items autonomously.

## Workflow Execution Policy
- Do not skip lifecycle stages. Follow the feature and task definitions in `docs/planning/WORKFLOW_REFERENCE.md`.
- Execute through the workflow skills instead of making ad hoc planning-state or task-state edits.
- Only one repository task may be `in_progress` at a time.
- One task means one top-level OpenSpec task ID and one bounded acceptance target.
- One executing feature owns one feature branch/worktree reused across its sequential tasks.
- A feature must be in `[READY]` before its first task execution starts.
- When the first task execution starts, move the backlog entry to `[IN_PROGRESS]` and keep it there until the feature reaches `[DONE]` or `[DEFER]`.
- Do not expand scope beyond the task.
- Only modify files listed in scope.
- If the listed scope is wrong or incomplete, update the linked OpenSpec change before proceeding.
- Verify against acceptance criteria before completion.
- Do not add a feature-level `BLOCKED` section. If work stalls during shaping, keep the feature in `[SHAPING]` and record the reason in the feature file. If work stalls during execution, keep the feature in `[IN_PROGRESS]` and mark the active task as `blocked` in the feature file.
- Planning-only workflow state edits may stay in the primary checkout only when that checkout starts clean and can be left clean again before exit.
- Non-trivial execution or code-changing task work must use a feature worktree.
- Wrappers and orchestration must respect, not bypass, review and verification gates inherited from the wrapped execution skills.

## Workflow Update Policy
- Only update the relevant feature-file section.
- Do not rewrite the whole file.
- Do not duplicate content.
- Preserve existing content unless explicitly required.
- Update the feature file first, then update `BACKLOG.md` if the board section or linked summary also changed.

## Workflow Worktree Policy
- Always create feature worktrees outside the main repository directory.
- Preferred worktree root relative to `<repo_root>` is `../worktrees/<repo_name>/`.
- Use one worktree per active feature branch.
- Create the feature branch/worktree when the first task for that feature enters execution.
- Name feature branches and worktrees with the feature ID and a short feature slug when execution starts, for example `v1-f001-acceptance-assessment`.
- Create the worktree from a clean commit, not from a dirty primary checkout.
- If the primary checkout has relevant uncommitted changes, inspect them and port them intentionally. Never overwrite or ignore them.
- Do not reuse the same worktree for unrelated features.

## Workflow Validation Policy
- Verification, review, audit, and OpenSpec archive checks are additive gates. They do not substitute for one another.
- Midstream OpenSpec adoption should create baseline specs from current main-checkout behavior and keep planned-but-unimplemented work in roadmap/backlog artifacts rather than backfilling it into the baseline specs.
- Record evidence and status updates in the workflow artifacts defined in `docs/planning/WORKFLOW_REFERENCE.md`, and follow the owning `SKILL.md` plus that reference for detailed acceptance, archive, and evidence rules.
- Record the exact validation command or inspection step and the result in the task's `Validation` or `Evidence` section.
- Distinguish clearly between implemented, validated locally, and not verified.
- Prefer task-scoped verification first and only escalate to broader suites when the risk justifies it.
- For docs or process-only changes, validate structure, links, symlinks, and relevant git status instead of pretending runtime tests prove the change.

## Workflow Git Hygiene
- Do not modify lockfiles unless dependency changes are intentional.
- Keep unrelated changes out of the same task.

<!-- End of Workflow Section -->

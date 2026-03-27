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
- Always prefer updating existing artifacts over creating new ones.
- Keep changes minimal, scoped, and verifiable.

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
- One executing feature owns one feature branch/worktree reused across its sequential tasks.
- Planning-only workflow state edits may stay in the primary checkout only when that checkout starts clean and can be left clean again before exit.
- Non-trivial execution or code-changing task work must use a feature worktree.
- Wrappers and orchestration must respect, not bypass, review and verification gates inherited from the wrapped execution skills.

## Workflow Validation Policy
- Verification, review, audit, and OpenSpec archive checks are additive gates. They do not substitute for one another.
- Record evidence and status updates in the workflow artifacts defined in `docs/planning/WORKFLOW_REFERENCE.md`.
- For detailed acceptance, status, archive, and evidence rules, follow the owning `SKILL.md` plus `docs/planning/WORKFLOW_REFERENCE.md`.

## Workflow Git Hygiene
- Do not commit caches, editor artifacts, temp files, or local exports.
- Do not modify lockfiles unless dependency changes are intentional.
- Keep unrelated changes out of the same task.

<!-- End of Workflow Section -->

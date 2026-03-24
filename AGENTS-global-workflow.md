<!-- Beginning of Workflow Section -->

<!-- DO NOT EDIT BELOW SECTION MANUALLY. It is maintained by automated script -->

## Workflow applicability
- Apply the workflow rules below to repositories that adopt the planning artifact structure under `docs/planning/`.
- Use `initialize-workflow-artifacts` when a repository wants to adopt this workflow but does not yet have the required scaffold.
- Treat any repo-local `AGENTS.md` as an overlay for project-specific constraints, not a second source of truth for the full workflow contract unless the repo explicitly says otherwise.

## Workflow core principle
- One feature = one feature file for execution state + one linked OpenSpec change for shaping truth
- Always prefer updating existing artifacts over creating new ones
- Keep changes minimal, scoped, and verifiable

## Workflow skill routing
- Use `audit-workflow` before and after planning-state edits.
- Use `shape-backlog-item` instead of raw `brainstorming` when promoting backlog work into shaped features.
- `shape-backlog-item` inherits the mandatory review gates from `brainstorming`.
- Use `ready-feature` instead of raw `writing-plans` when finishing shaping and promoting a feature into `[READY]`.
- `ready-feature` inherits the mandatory plan-review gate from `writing-plans`.
- Use `start-task` to begin execution, `complete-task` to close the active task, and `repair-drift` to fix workflow-state inconsistencies.
- Use `autonomous-backlog-loop` only when the goal is to keep advancing eligible workflow items autonomously.
- Within the workflow wrappers, prefer `subagent-driven-development` for approved execution work and run a review pass before declaring completion.
- Wrappers and orchestration must respect, not bypass, review and verification gates inherited from wrapped execution skills.

## Workflow lifecycle
- Feature lifecycle must follow `BACKLOG -> SHAPING -> READY -> IN_PROGRESS -> DONE` or `DEFER`.
- Work inside a feature must follow `Feature -> OpenSpec proposal/specs/design/tasks -> Execution`.
- Do not skip steps.
- Do not mix levels.
- Tasks are the only execution units.

## Workflow artifact ownership
- `docs/planning/ROADMAP.md` owns high-level major-version planning only.
- `docs/planning/current_version` is a symlink to the active version directory. It is a convenience pointer, not a second source of truth.
- `docs/planning/versions/<version>/VERSION_SCOPE.md` owns the version goal, exit criteria, explicit deferrals, and cross-feature decisions for that version.
- `docs/planning/versions/<version>/BACKLOG.md` owns the ordered work items for that version and tracks feature-level status only through the `[BACKLOG]`, `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` sections.
- `openspec/specs/` owns the current behavior specification for stable capabilities.
- `openspec/changes/<change-id>/proposal.md`, `design.md`, `tasks.md`, and delta specs own shaping and readiness intent for one linked feature change.
- `[BACKLOG]` entries must use lowercase backlog IDs like `v1-b001` and follow ``### `v1-b001` [TAG] TITLE``, where `[TAG]` is optional.
- `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` entries must follow ``### `v1-f001` [TAG] [Title](features/v1-f001-title.md)``, where `[TAG]` is optional.
- `docs/planning/versions/<version>/features/<feature-id>-<slug>.md` owns one feature's execution metadata, synchronized execution tasks, task status, validation evidence, and links to the authoritative OpenSpec change and specs.
- Keep feature-board status in `BACKLOG.md`. Keep task-level tracking and validation evidence in the feature file.

## Workflow directory convention
- Keep `ROADMAP.md` at `docs/planning/ROADMAP.md`.
- Keep version planning artifacts under `docs/planning/versions/<version>/`.
- Use `docs/planning/versions/<version>/features/`, never `feature/`.
- Treat `docs/superpowers/specs/` and `docs/superpowers/plans/` as historical records only. Do not create new current feature-workflow artifacts there.
- If a planning artifact already exists, update it in place instead of creating a parallel file.

## Workflow feature file contract
- Each feature must be maintained in one file named `docs/planning/versions/<version>/features/<feature-id>-<slug>.md`.
- Feature IDs must be stable and unique within the repository. Use lowercase IDs like `v1-f001`.
- Assign the feature ID when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.
- Once created, a feature ID must never be reused for a different feature.
- The feature file contains `Meta`, `Execution Scope`, `Tasks`, `Validation Log`, and `Change Log`.
- The feature file must record one linked OpenSpec change plus the affected OpenSpec spec paths.
- Do not duplicate OpenSpec proposal, design, or spec prose inside the feature file.
- Always update the existing feature file in-place before updating any derived summary elsewhere.

## Workflow feature status model
- `BACKLOG`: an idea-level work item that is still unclear or not yet shaped into a ready feature. No feature ID or feature file is required yet.
- `SHAPING`: a real feature exists, its feature ID is assigned, its feature file exists, and one linked OpenSpec change owns active proposal/spec/design/task shaping work before execution begins.
- `READY`: shaping is complete, the linked OpenSpec change has the required shaping artifacts, the execution task breakdown has been synchronized into the feature file, and at least one task has status `ready`.
- `IN_PROGRESS`: execution has started on at least one task for the feature, and the feature is not yet complete or deferred. Once a feature enters `IN_PROGRESS`, keep it there until the feature reaches `DONE` or `DEFER`, even if there is a handoff gap where no task is currently `in_progress`.
- `DONE`: feature-level acceptance is satisfied.
- `DEFER`: the work is intentionally postponed or dropped from the current version.
- Every `BACKLOG.md` file must use the sections `[BACKLOG]`, `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` in that order.
- Moving an item from `[BACKLOG]` to `[SHAPING]` is the moment the feature ID is assigned and the feature file is created.
- One `[BACKLOG]` item may split into multiple `[SHAPING]` features, but keep a single split below 5 features. If the work appears to need 5 or more, first split it into multiple backlog items.
- Move a feature from `[SHAPING]` to `[READY]` when shaping is complete and tasks are ready to execute.
- Move a feature from `[READY]` to `[IN_PROGRESS]` as soon as task execution starts.
- A feature may move to `[DONE]` only when its required tasks are complete and its feature-level acceptance bar is satisfied.
- A feature may move to `[DEFER]` from any section, but the reason should be captured in the backlog entry or linked feature file.
- Do not add a feature-level `BLOCKED` section. If work stalls during shaping, keep the feature in `[SHAPING]` and record the reason in the feature file. If work stalls during execution, keep the feature in `[IN_PROGRESS]` and mark the active task as `blocked` in the feature file.

## Workflow task status model
- Task statuses are `todo`, `ready`, `in_progress`, `blocked`, `done`, and `cancelled`.
- A task may move from `todo` to `ready` only when its dependencies and prerequisites are satisfied.
- At most one task in the repository may be `in_progress` at a time.
- A task may move to `done` only after validation evidence is recorded in the feature file.
- If new work is discovered during execution, add or revise tasks first. Do not silently expand the current task.

## Workflow update discipline
- Only update the relevant feature-file section.
- Do not rewrite the whole file.
- Do not duplicate content.
- Preserve existing content unless explicitly required.
- Update the feature file first, then update `BACKLOG.md` if the board section or linked summary also changed.

## Workflow task execution rules
- Only execute one task at a time across the entire repository.
- One task means one task ID and one bounded acceptance target.
- A feature in execution owns one feature branch/worktree reused across its sequential tasks.
- After the first task starts, later tasks on that feature must resume in that same feature worktree until the feature reaches `[DONE]` or `[DEFER]`.
- A feature must be in `[READY]` before its first task execution starts.
- When the first task execution starts, move the backlog entry to `[IN_PROGRESS]` and keep it there until the feature reaches `[DONE]` or `[DEFER]`.
- Do not expand scope beyond the task.
- Only modify files listed in scope.
- If the listed scope is wrong or incomplete, update the feature file before proceeding.
- Verify against acceptance criteria before completion.
- If something is unclear, stop and ask instead of guessing.

## Workflow worktree policy
- Always use a git worktree for non-trivial execution or code-changing task work.
- Always create the worktree outside the main repository directory.
- Preferred worktree root relative to `<repo_root>` is `../worktrees/<repo_name>/`.
- Use one worktree per active feature branch.
- Create the feature branch/worktree when the first task for that feature enters execution.
- Reuse the same feature branch/worktree for later tasks on that feature until the feature reaches `[DONE]` or `[DEFER]`.
- Name feature branches and worktrees with the feature ID and a short feature slug when execution starts, for example `v1-f001-acceptance-assessment`.
- Create the worktree from a clean commit, not from a dirty primary checkout.
- Do not auto-commit dirty primary-checkout changes just to create the worktree.
- If the primary checkout has relevant uncommitted changes, inspect them and port them intentionally. Never overwrite or ignore them.
- Do not reuse the same worktree for unrelated features.
- Do not work directly in the primary checkout unless explicitly instructed.
- If a later task resumes on an existing feature worktree, that worktree must already be clean before the task starts.
- Planning-only workflow state edits may stay in the primary checkout only when that checkout is clean before the edit begins and can be left clean again before the skill exits, unless a repo-local overlay requires worktrees for them too.

## Workflow validation
- `complete-task` requires `verification-before-completion` as a mandatory gate distinct from review.
- Record the exact validation command or inspection step and the result in the task's `Validation` or `Evidence` section.
- A task is not `done` until validation evidence is recorded, or the feature file explicitly says why validation could not be run.
- A task is not `done` until the active feature worktree is left clean for the next handoff.
- When a feature-file task uses checklist-style acceptance criteria, mark each satisfied item as `[x]` before declaring the task `done`.
- Prefer task-scoped verification first and only escalate to broader suites when the risk justifies it.
- For docs or process-only changes, validate structure, links, symlinks, and relevant git status instead of pretending runtime tests prove the change.
- If validation cannot be run, say so explicitly.
- Distinguish clearly between implemented, validated locally, and not verified.
- OpenSpec shaping and archive checks are additive gates. They do not replace workflow audit, task readiness checks, code review, or `verification-before-completion`.
- Before archiving a linked OpenSpec change, run the relevant OpenSpec validation command for that change and record or report the result.

## Workflow git hygiene
- Do not commit caches, editor artifacts, temp files, or local exports.
- Do not modify lockfiles unless dependency changes are intentional.
- Keep unrelated changes out of the same task.
- Before marking a task `done`, leave the active feature worktree clean for the next handoff, usually by committing the task's intended changes.

<!-- End of Workflow Section -->

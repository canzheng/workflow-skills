# Workflow Skills + OpenSpec

This repository defines the official workflow:

- `docs/planning/` owns release planning, queue order, and feature-board state
- `openspec/specs/` owns stable behavior specifications
- `openspec/changes/<change-id>/` owns shaping artifacts for one feature change
- feature files under `docs/planning/versions/<version>/features/` own workflow metadata, validation evidence, and handoff notes

The goal is to keep one source of truth per concern:

- release planning truth in `BACKLOG.md`
- shaping truth in OpenSpec
- task-definition truth in OpenSpec `tasks.md`
- execution evidence truth in the feature file
- execution verification truth in task evidence and workflow validation logs

## Lifecycle

Feature lifecycle:

`BACKLOG -> SHAPING -> READY -> IN_PROGRESS -> DONE | DEFER`

Work lifecycle inside a feature:

`Backlog Item -> OpenSpec proposal/specs/design/tasks -> Execution -> OpenSpec archive -> Branch finish`

`DEFER` is allowed from any non-`DONE` state when the deferral reason is recorded.

## Artifact Ownership

### `docs/planning/versions/<version>/BACKLOG.md`

Owns:
- version-scoped queue order
- feature-board state
- feature-level transitions between `[BACKLOG]`, `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]`

Does not own:
- task-by-task execution details
- shaping/design prose
- validation evidence

### `openspec/specs/`

Owns:
- current behavior specifications for stable capabilities

Does not own:
- release order
- feature-board state
- worktree lifecycle

### `openspec/changes/<change-id>/`

Owns:
- `proposal.md`
- `design.md`
- `tasks.md`
- spec deltas for the change

This is the shaping and readiness authority for one promoted feature.

### `docs/planning/versions/<version>/features/<feature-id>-<slug>.md`

Owns:
- feature metadata
- linked OpenSpec change and spec paths
- current task pointer
- validation evidence
- execution handoff notes

Does not own:
- duplicated proposal, design, spec, or task prose from OpenSpec

## Official Phase Workflow

### 1. Backlog

The feature starts as a backlog item in `BACKLOG.md`.

Use:
- `prioritize-backlog` to reorder eligible work when needed

OpenSpec is required by this workflow, but no change is required yet.

### 2. Shaping

Use:
- `shape-backlog-item`

`shape-backlog-item` is the official wrapper for promotion from `[BACKLOG]` to `[SHAPING]`.

Responsibilities:
- run `audit-workflow` before and after
- select the backlog item
- use exploration/brainstorming as needed
- use the OpenSpec propose flow to create or update one OpenSpec change for the feature
- ensure shaping happens in OpenSpec artifacts
- create the thin feature file with workflow metadata and OpenSpec links
- move the board item to `[SHAPING]`
- leave the primary checkout clean

OpenSpec tools used during shaping:
- `openspec-explore` for requirements/thinking
- `openspec-propose` through the wrapper for creating the change artifacts

OpenSpec `apply` is not part of this workflow.

### 3. Ready

Use:
- `ready-feature`

`ready-feature` is the official wrapper for promotion from `[SHAPING]` to `[READY]`.

Responsibilities:
- run `audit-workflow` before and after
- inspect the feature file and linked OpenSpec change
- require the linked OpenSpec change to have:
  - `proposal.md`
  - `design.md`
  - `tasks.md`
  - relevant linked spec paths
- ensure the linked OpenSpec change has at least one task that is honestly `ready`
- move the board item to `[READY]`
- leave the primary checkout clean

### 4. Execution

Use:
- `start-task`
- `complete-task`

`start-task` is the official entry into execution.

Responsibilities:
- run `audit-workflow`
- enforce one repository task `in_progress`
- create or reuse the feature worktree
- set `Current Task`
- mark the selected OpenSpec task `in_progress`
- move the feature to `[IN_PROGRESS]` if needed
- provide the linked OpenSpec change directory and Markdown context file list to the executor, then require the executor to read the listed context files before work begins

`complete-task` is the official exit for one execution task.

Responsibilities:
- run `verification-before-completion`
- record exact evidence
- optionally request code review
- update OpenSpec task status and rely on OpenSpec dependencies for downstream readiness
- leave the feature worktree clean
- keep the feature in `[IN_PROGRESS]` until feature acceptance is satisfied
- provide the linked OpenSpec change directory and Markdown context file list to the executor, then require the executor to read the listed context files before task closure

OpenSpec `apply` is intentionally not used here. Execution stays under workflow task control so the repo keeps:
- one-task-at-a-time enforcement
- worktree reuse rules
- explicit validation evidence
- clean handoff rules

### 5. Feature Completion

When the feature-level acceptance bar is met:
- the feature can move to `[DONE]`
- the linked OpenSpec change must be validated before archive

Official sequence:
1. Finish the last execution task with `complete-task`
2. Run `finish-feature`
3. Let `finish-feature` validate and archive the linked OpenSpec change
4. Let `finish-feature` hand off to `finishing-a-development-branch`

Current OpenSpec CLI note:
- this workflow uses `openspec validate ...` as the verification step before archive
- if a future wrapper introduces an `openspec verify` command, it should remain additive rather than replacing workflow validation gates

### 6. Deferral

Use:
- `defer-feature`

This moves a feature to `[DEFER]` and records why it was postponed or dropped.

## Skill Mapping

Official skill usage by phase:

- Backlog ordering: `prioritize-backlog`
- Backlog to shaping: `shape-backlog-item`
- Shaping exploration: `openspec-explore`
- Shaping proposal creation: `openspec-propose`
- Shaping to ready: `ready-feature`
- Execution start: `start-task`
- Execution completion: `complete-task`
- Drift repair: `repair-drift`
- Feature deferral: `defer-feature`
- Feature completion gate: `finish-feature`
- OpenSpec change archive: `openspec-archive-change`
- Final branch handling: `finishing-a-development-branch`

Not used for execution in this workflow:

- `openspec-apply-change`

## Gates That Must Remain

This workflow does not weaken existing gates.

Always preserve:
- `audit-workflow` before and after planning-state edits
- at most one repository task `in_progress`
- task-scoped verification before completion claims
- review where the wrapper or execution flow requires it
- clean primary checkout for planning-only changes
- clean feature worktree handoff between execution tasks
- exact validation evidence in the feature file

OpenSpec validation is additive:
- it validates shaping/change artifacts
- it does not replace workflow audit
- it does not replace task-level evidence
- it does not replace review or branch-finish checks
- branch finishing must be preceded by the workflow-owned archive gate

## Minimal Operating Rules

- Do not let users or agents independently update both OpenSpec shaping prose and feature-file shaping prose. Shaping belongs in OpenSpec.
- Do not let feature files become a second task ledger. Task definitions and task status belong in OpenSpec.
- Do not move a feature to `[READY]` without linked OpenSpec shaping artifacts and at least one `ready` OpenSpec task.
- Do not use OpenSpec archive as a substitute for `complete-task` evidence or `DONE` acceptance.
- Do not finish the branch before the linked OpenSpec change is validated and archived.
- Do not run `openspec-propose` as a separate manual lane for promoted work; `shape-backlog-item` owns that step.

## Repository State

This repository is both:
- the development source of truth for the workflow skills
- the reference implementation of the hybrid workflow itself

That means workflow changes in this repo should follow the same official lifecycle documented above.

## Migration Expectation

This workflow assumes OpenSpec is present and authoritative for shaping and task state.

- New workflow adopters should initialize `docs/planning/` and `openspec/` together.
- Repositories using the older planning-only workflow must migrate to the OpenSpec-backed model before relying on the current global workflow skills.

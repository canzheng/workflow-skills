# Workflow Skills + OpenSpec

This repository defines the official workflow:

- `docs/planning/` owns release planning, queue order, and feature-board state
- `openspec/specs/` owns stable behavior specifications
- `openspec/changes/<change-id>/` owns shaping artifacts for one feature change
- feature files under `docs/planning/versions/<version>/features/` own workflow metadata, validation evidence, and handoff notes

## Contributor Setup

Use the tracked environment definition to manage local development:

- `conda env create -f environment.yml`
- `conda env update -f environment.yml --prune`

The environment name comes from `environment.yml`. Keep environment changes limited to `environment.yml` and `requirements.txt`.

Use `bin/run-python.sh` for repository Python scripts and module entrypoints while working in this repo. The wrapper is dev-repo-only and is not shipped with installed skills.

Examples:

- `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
- `bin/run-python.sh -m unittest tests.test_install_script -v`
- `bin/run-python.sh -m pytest skills/_workflow/tests -q`

`install.sh` also depends on `rsync` to copy the tracked skill directories into `${AGENTS_HOME:-$HOME/.agents}/skills`.

The goal is to keep one source of truth per concern:

- release planning truth in `BACKLOG.md`
- shaping truth in OpenSpec
- task-definition truth in OpenSpec `tasks.md`
- workflow-derived task-readiness truth in the workflow parser over top-level OpenSpec tasks, checkbox state, `Current Task`, and the optional `Depends On` markdown convention
- execution evidence truth in the feature file
- execution verification truth in task evidence and workflow validation logs

## Lifecycle

Feature lifecycle:

`BACKLOG -> SHAPING -> READY -> IN_PROGRESS -> DONE | DEFER`

Work lifecycle inside a feature:

`Backlog Item -> OpenSpec proposal/specs/design/tasks -> Execution -> finish-feature archive/completion gate -> Branch finish`

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
- `implementation-plans/<task-id>.md`
- spec deltas for the change

This is the shaping authority for one promoted feature, and the source material from which workflow-derived task readiness is computed.

Prefer linked change ids that reuse the feature-style prefix when practical, for example `v1-f008-clarify-workflow-owned-task-readiness`. This convention is guidance only; audit and readiness checks must not fail solely because a valid change uses a different name.

### `docs/planning/versions/<version>/features/<feature-id>-<slug>.md`

Owns:
- feature metadata
- linked OpenSpec change and spec paths
- current task pointer
- validation evidence
- execution handoff notes

Does not own:
- duplicated proposal, design, spec, or task prose from OpenSpec

Migration note:
- historical `[DONE]` features from before OpenSpec adoption may instead record `OpenSpec Status: legacy-exempt`
- active workflow feature files must use the thin execution-record format rather than legacy inline planning sections

## Official Phase Workflow

### 1. Backlog

The feature starts as a backlog item in `BACKLOG.md`.

Use:
- `prioritize-backlog` to reorder eligible work when needed

OpenSpec is required by this workflow, but no change is required yet.

For a legacy repo adopting OpenSpec midstream:
- baseline specs should describe current main-checkout behavior
- planned but unimplemented work stays in backlog and roadmap artifacts
- historical completed features may be marked `OpenSpec Status: legacy-exempt`
- current `[SHAPING]`, `[READY]`, and `[IN_PROGRESS]` work should get active OpenSpec changes for the remaining work

### 2. Workflow Diagnosis

Use:
- `diagnose-workflow`

`diagnose-workflow` is the operator-facing health report for this workflow.

Use it when you want:
- a read-only summary of workflow state
- structured findings without failing fast
- a quick distinction between healthy, repairable, and ambiguous workflow states

It complements, but does not replace:
- `audit-workflow` for pass/fail gating
- `repair-drift` for minimal structural fixes

### 3. Shaping

Use:
- `shape-backlog-item`

`shape-backlog-item` is the official wrapper for promotion from `[BACKLOG]` to `[SHAPING]`.

Responsibilities:
- run `audit-workflow` before and after
- select the backlog item
- use exploration/brainstorming as needed
- run `openspec-propose` through the wrapper to create or update one OpenSpec change for the feature
- prefer linked change ids that reuse the feature-style prefix when practical, while treating that naming convention as non-gating guidance
- ensure shaping happens in OpenSpec artifacts
- create the thin feature file with workflow metadata and OpenSpec links
- move the board item to `[SHAPING]`
- leave the primary checkout clean

OpenSpec tools used during shaping:
- `openspec-explore` for requirements/thinking
- `openspec-propose`, which `shape-backlog-item` must run through the wrapper for creating the change artifacts

OpenSpec `apply` is not part of this workflow.

### 4. Ready

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
- ensure the linked OpenSpec change has at least one top-level task that resolves honestly to workflow-`ready`
- move the board item to `[READY]`
- leave the primary checkout clean

### 5. Execution

Use:
- `start-task`
- `complete-task`

`start-task` is the official entry into execution.

Responsibilities:
- run `audit-workflow`
- enforce one repository task `in_progress`
- create or reuse the feature worktree
- set `Current Task` to the selected top-level task ID
- treat that feature-file field as the active `in_progress` marker while `tasks.md` remains the checked/unchecked task ledger
- write or update the selected task's implementation plan at `openspec/changes/<change-id>/implementation-plans/<task-id>.md` before code execution begins
- move the feature to `[IN_PROGRESS]` if needed
- provide the linked OpenSpec change directory and Markdown context file list to the executor, then require the executor to read the listed context files before work begins

`complete-task` is the official exit for one execution task.

Responsibilities:
- run `verification-before-completion`
- record exact evidence
- optionally request code review
- update OpenSpec checkbox status and rely on the workflow `Depends On` convention for downstream readiness
- leave the feature worktree clean
- keep the feature in `[IN_PROGRESS]` until feature acceptance is satisfied
- provide the linked OpenSpec change directory and Markdown context file list to the executor, then require the executor to read the listed context files before task closure

OpenSpec `apply` is intentionally not used here. Execution stays under workflow task control so the repo keeps:
- one-task-at-a-time enforcement
- worktree reuse rules
- explicit validation evidence
- clean handoff rules

### 6. Feature Completion

When the feature-level acceptance bar is met:
- the feature remains `[IN_PROGRESS]` until `finish-feature` runs
- `finish-feature` validates and archives the linked OpenSpec change
- `finish-feature` moves the feature to `[DONE]` before any downstream branch/worktree finalization

Official sequence:
1. Finish the last execution task with `complete-task`
2. Run `finish-feature` while the feature is still `[IN_PROGRESS]` and `Current Task` is `none`
3. Let `finish-feature` validate the linked OpenSpec change and run `openspec-archive-change` if the change is still active
4. Let `finish-feature` move the feature to `[DONE]`
5. Let `finish-feature` hand off to `finishing-a-development-branch`

Current OpenSpec CLI note:
- this workflow uses `openspec validate ...` as the verification step before archive
- if a future wrapper introduces an `openspec verify` command, it should remain additive rather than replacing workflow validation gates

### 7. Deferral

Use:
- `defer-feature`

This moves a feature to `[DEFER]` and records why it was postponed or dropped.

## Skill Mapping

Official skill usage by phase:

- Workflow diagnosis: `diagnose-workflow`
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
- `diagnose-workflow` as read-only diagnosis only
- `audit-workflow` before and after planning-state edits
- at most one repository task `in_progress`
- task-scoped verification before completion claims
- review where the wrapper or execution flow requires it
- clean primary checkout for planning-only changes
- clean feature worktree handoff between execution tasks
- exact validation evidence in the feature file

OpenSpec validation is additive:
- `diagnose-workflow` helps explain workflow health, but it is not a gate
- it validates shaping/change artifacts
- it does not replace workflow audit
- it does not replace task-level evidence
- it does not replace review or branch-finish checks
- branch finishing must be preceded by the workflow-owned archive gate

## Minimal Operating Rules

- Do not let users or agents independently update both OpenSpec shaping prose and feature-file shaping prose. Shaping belongs in OpenSpec.
- Do not let feature files become a second task ledger. Task definitions and task status belong in OpenSpec.
- Use top-level OpenSpec task IDs like `1`, `2`, and `3` as execution units. Nested checklist items like `1.1` and `1.2` are supporting detail, not separate workflow tasks.
- Do not move a feature to `[READY]` without linked OpenSpec shaping artifacts and at least one top-level OpenSpec task that resolves to workflow status `ready`.
- Before executing a task, write or update its implementation plan under the linked OpenSpec change and feed that plan back into execution context.
- Do not use OpenSpec archive as a substitute for `complete-task` evidence or `DONE` acceptance.
- Do not finish the branch before the linked OpenSpec change is validated and archived.
- `shape-backlog-item` must run `openspec-propose` for promoted work; do not run `openspec-propose` as a separate manual lane.
- `shape-backlog-item` must create feature files through the renderer script rather than freehand authoring.
- `finish-feature` must run `openspec-archive-change` before handing off to `finishing-a-development-branch`.
- Historical `[DONE]` features are exempt from OpenSpec change checks only when explicitly marked `OpenSpec Status: legacy-exempt`.

## Repository State

This repository is both:
- the development source of truth for the workflow skills
- the reference implementation of the hybrid workflow itself

That means workflow changes in this repo should follow the same official lifecycle documented above.

## Migration Expectation

This workflow assumes OpenSpec is present and authoritative for shaping and task state.

- New workflow adopters should initialize `docs/planning/` and `openspec/` together.
- Repositories using the older planning-only workflow must migrate to the OpenSpec-backed model before relying on the current global workflow skills.

# Workflow Reference

## Purpose

This document is the canonical reference for workflow definitions, status models, artifact ownership, and shared structural rules.

## Workflow Lifecycle

- Feature lifecycle must follow `BACKLOG -> SHAPING -> READY -> IN_PROGRESS -> DONE` or `DEFER`.
- Work inside a feature must follow `Feature -> OpenSpec proposal/specs/design/tasks -> Execution`.
- Tasks are the only execution units.

## Artifact Ownership and Source of Truth

- `docs/planning/ROADMAP.md` owns high-level major-version planning only.
- `docs/planning/current_version` is a symlink to the active version directory. It is a convenience pointer, not a second source of truth.
- `docs/planning/versions/<version>/VERSION_SCOPE.md` owns the version goal, exit criteria, explicit deferrals, and cross-feature decisions for that version.
- `docs/planning/versions/<version>/BACKLOG.md` owns the ordered work items for that version and tracks feature-level status only through the `[BACKLOG]`, `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` sections.
- `openspec/specs/` owns the current behavior specification for stable capabilities.
- `openspec/changes/<change-id>/proposal.md`, `design.md`, `tasks.md`, and delta specs own shaping, readiness intent, task definitions, checkbox completion state, and any workflow dependency-convention references for one linked feature change.
- `openspec/changes/<change-id>/implementation-plans/<task-id>.md` owns the task-scoped implementation plan for one executable OpenSpec task.
- `openspec/changes/archive/` owns archived completed changes after feature completion has satisfied the archive gate.
- `docs/planning/versions/<version>/features/<feature-id>-<slug>.md` owns one feature's workflow metadata, validation evidence, handoff notes, and links to the authoritative OpenSpec change and specs.
- Keep feature-board status in `BACKLOG.md`. Keep task-level tracking and validation evidence in the feature file.

## Identifier and Entry Formats

- Prefer linked change IDs that reuse the feature-style prefix when practical, for example `v1-f008-...`; this naming convention is guidance only and must not be used as an audit or readiness gate.
- `[BACKLOG]` entries must use lowercase backlog IDs like `v1-b001` and follow ``### `v1-b001` [TAG] TITLE``, where `[TAG]` is optional.
- `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` entries must follow ``### `v1-f001` [TAG] [Title](features/v1-f001-title.md)``, where `[TAG]` is optional.
- Promoted entries are heading-only. Do not add body content, summaries, rationale, or defer reasons under the heading. Records belong in the feature file; intent and design belong in the linked OpenSpec change.
- `[BACKLOG]` items may carry body notes (rationale, dependency hints, sketch ideas) under the heading until they are promoted to `[SHAPING]`, since no feature file or OpenSpec change exists yet.

## Directory and Path Conventions

- Keep `ROADMAP.md` at `docs/planning/ROADMAP.md`.
- Keep version planning artifacts under `docs/planning/versions/<version>/`.
- Use `docs/planning/versions/<version>/features/`, never `feature/`.
- Treat `docs/superpowers/specs/` and `docs/superpowers/plans/` as historical records only. Do not create new current feature-workflow artifacts there.

## Feature Record Contract

- Each feature must be maintained in one file named `docs/planning/versions/<version>/features/<feature-id>-<slug>.md`.
- Feature IDs must be stable and unique within the repository. Use lowercase IDs like `v1-f001`.
- Assign the feature ID when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.
- Once created, a feature ID must never be reused for a different feature.
- The feature file contains `Meta`, `Validation Log`, and `Handoff Notes`.
- The feature file should record proof obligations and validation evidence using the same contract language that shaping, readiness, task start, and task completion guidance use.
- The feature file must record one linked OpenSpec change plus the affected OpenSpec spec paths, except for historical `[DONE]` features explicitly marked `OpenSpec Status: legacy-exempt` during midstream adoption.
- Active workflow feature files must use the thin execution-record format. Legacy inline planning sections such as `Problem`, `Goal`, `Design Spec`, `Implementation Plan`, or embedded `Tasks` are invalid unless the feature is an explicitly marked `legacy-exempt` historical completed feature.
- Do not duplicate OpenSpec proposal, design, spec, or task prose inside the feature file.
- Semantic readiness judgment belongs to `ready-feature` through an explicit independent review of the linked shaping artifacts; `audit-workflow` remains a structural workflow-state gate.

## Feature Status Model

- `BACKLOG`: an idea-level work item that is still unclear or not yet shaped into a ready feature. No feature ID or feature file is required yet.
- `SHAPING`: a real feature exists, its feature ID is assigned, its feature file exists, and one linked OpenSpec change owns active proposal/spec/design/task shaping work before execution begins.
- During `SHAPING`, identify the corresponding existing documentation and spec surfaces likely affected by the feature and capture the relevant paths in the linked OpenSpec change.
- `READY`: shaping is complete, the linked OpenSpec change has the required shaping artifacts, corresponding existing documentation has been reviewed for consistency with the shaped change, any documentation that must change for readiness has been updated, at least one linked top-level OpenSpec task resolves to workflow status `ready` under the workflow task-status rules, and `ready-feature` has passed an independent semantic review that the shaping artifacts define enough contract surface for `start-task` to draft against safely.
- `IN_PROGRESS`: execution has started on at least one task for the feature, and the feature is not yet complete or deferred. Once a feature enters `IN_PROGRESS`, keep it there until the feature reaches `DONE` or `DEFER`, even if there is a handoff gap where no task is currently `in_progress`.
- `DONE`: feature-level acceptance is satisfied.
- Historical `[DONE]` features that predate OpenSpec adoption may remain valid when explicitly marked `OpenSpec Status: legacy-exempt`.
- `DEFER`: the work is intentionally postponed or dropped from the current version.
- Every `BACKLOG.md` file must use the sections `[BACKLOG]`, `[SHAPING]`, `[READY]`, `[IN_PROGRESS]`, `[DONE]`, and `[DEFER]` in that order.
- Moving an item from `[BACKLOG]` to `[SHAPING]` is the moment the feature ID is assigned and the feature file is created.
- One `[BACKLOG]` item may split into multiple `[SHAPING]` features, but keep a single split below 5 features. If the work appears to need 5 or more, first split it into multiple backlog items.
- Move a feature from `[SHAPING]` to `[READY]` when shaping is complete and tasks are ready to execute.
- Move a feature from `[READY]` to `[IN_PROGRESS]` as soon as task execution starts.
- A feature may move to `[DONE]` only when its required tasks are complete and its feature-level acceptance bar is satisfied.
- A feature may move to `[DEFER]` from any section, but the reason must be captured in the linked feature file.

## Task Status Model

- OpenSpec `tasks.md` is the task-definition authority and checkbox completion ledger.
- Executable OpenSpec tasks use top-level task IDs like `1`, `2`, and `3`. Nested checklist items like `1.1` and `1.2` may exist as implementation detail, but they are not separate execution units.
- Optional `Depends On` blocks under top-level tasks are a workflow-layer markdown convention interpreted by this repository's helpers; they are not native OpenSpec task semantics.
- Unchecked top-level OpenSpec tasks are treated as workflow-`ready` work only when their workflow prerequisites and any `Depends On` references are satisfied. Otherwise they remain `todo`. This is a DEPENDENCY fact and says nothing about whether the task's contract is adequately specified — that question is asked per task in `start-task` 7.1, not feature-wide at promotion time.
- Every executable task has an implementation plan at `openspec/changes/<change-id>/implementation-plans/<task-id>.md`. The deterministic gates in `start-task` all key on that file, so a task executed without one silently receives none of them.
- `Current Task` in the feature file identifies the one top-level OpenSpec task currently `in_progress`; this feature-file field is the active execution marker in the implemented workflow.
- Workflow continuation after `complete-task` uses one canonical machine-readable payload with fields `action`, `target_feature_id`, `target_task_id`, `reason`, and `requires_human_decision`; wrappers should rely on that payload instead of inferring the next step from prose-only handoff notes.
- Canonical continuation actions are `start_task`, `finish_feature`, and `stop`. `target_task_id` must be `null` unless `action` is `start_task`.
- A REMEDIATION ROUND is the work done in response to a `feature_finish` gate's blocking findings. It is a first-class unit with its own lifecycle (`finish-feature` 3.5.1) and is NOT task execution: no task is reopened, `Current Task` stays `none`, and there is deliberately no `done -> ready` transition in the Task Status Model. Earlier guidance said to resolve findings "through normal task execution", which named a transition that does not exist; in practice remediation therefore ran ungated, and on one feature roughly half of all blocking findings were introduced by a previous gate's own remediation.
- Each round writes `openspec/changes/<change-id>/remediation/gate-<n>.md` enumerating every finding from that gate with its attribution, intended fix, proof obligation and disposition. This file is the round's audit trail and the only place a later reviewer can check whether a prescribed fix was implemented.
- `Gate Iteration: <n>` in the feature file counts `feature_finish` invocations. It exists so the loop can observe its own length: a feature that has failed the same gate repeatedly is a signal about scope or method, not only about defects.
- During task execution, record validation evidence in the feature file as planned proof steps complete; `complete-task` reconciles that ledger instead of acting as the primary place where evidence is first authored.
- Feature validation evidence should be written against the declared proof obligations and validation taxonomy, using explicit evidence categories such as `schema`, `runtime_path`, `artifact_repair`, `prompt_contract`, `orchestration`, and `negative_case` instead of only naming a successful command.
- Feature-file handoff notes may also carry structured review verdicts using canonical lines `Review Scope`, `Review Target`, `Review Verdict`, `Blocking Findings`, and `Review Terminal`; downstream tooling should consume those lines without parsing prose-only summaries.
- `Review Scope` values in use: `task_readiness` (per-task contract review, `start-task` 7.1), `task_completion` (`complete-task`), `feature_finish` (`finish-feature` 3.5), `remediation_code` (a remediation round's own diff review), `record_integrity` (a correction to earlier notes).
- `Review Terminal` means: `true` asserts that no further review round is warranted AT THIS SCOPE. It is a claim by the reviewer, not by the author, and it does not assert the feature is defect-free — only that continuing to review the same surface has stopped paying. `false` means another round at this scope is expected.
- `Blocking Findings` is a slug list and is authoritative for BLOCKING findings only. It is not a finding ledger: on one feature it listed 37 slugs against 47 blocking findings, enumerated none of the ~37 non-blocking ones, and two gates recorded no entry at all. A round's full ledger belongs in its remediation catalogue (below), not in this field.
- Execution-scoped helpers may continue a selected feature when its own linkage, readiness, and worktree state are valid even if unrelated active features have drift; surface that unrelated drift as diagnostics and keep direct `audit-workflow` as the repo-wide pass/fail gate.
- When workflow contract behavior is under test, prefer canonical end-to-end fixtures over hand-minimized local fixtures.
- Checked OpenSpec tasks are treated as `done`.
- The shared validation taxonomy should stay readable in Markdown and may distinguish helper proof, schema proof, composed runtime proof, persistence proof, negative-path proof, and manual inspection proof where that distinction matters.

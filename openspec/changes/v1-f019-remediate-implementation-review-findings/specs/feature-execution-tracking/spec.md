## ADDED Requirements

### Requirement: Stage-level lesson retrieval lines are referred to as stage-scoped in the owning skill contract

SKILL.md files that own a stage-level retrieval gate — `shape-backlog-item` for `shaping` and `ready-feature` for `ready` — SHALL describe the `Retrieved Lesson IDs: ...` line they write into the feature file handoff notes as "stage-scoped," matching the authoritative phrasing in `docs/planning/WORKFLOW_REFERENCE.md`. The equivalent line owned by task-level skills (`start-task`, `complete-task`) remains referred to as "task-scoped."

#### Scenario: Stage-level skill contract uses stage-scoped terminology

- **WHEN** an operator reads the `shape-backlog-item` or `ready-feature` SKILL.md contract describing the retrieved-lessons recording step
- **THEN** the contract describes the emitted line as "stage-scoped"
- **AND** the phrasing matches the `docs/planning/WORKFLOW_REFERENCE.md` lesson-lifecycle bullet that names stage-scoped emissions from `shape-backlog-item` and `ready-feature`

#### Scenario: Task-level skill contract retains task-scoped terminology

- **WHEN** an operator reads the `start-task` or `complete-task` SKILL.md contract describing the retrieved-lessons line
- **THEN** the contract describes the emitted line as "task-scoped"
- **AND** the phrasing is consistent with the per-task lesson recording responsibility those skills already carry

### Requirement: The completion_handoff payload schema is discoverable from the owning skill contract

The `complete-task` SKILL.md contract SHALL name the canonical `completion_handoff` payload fields directly, so operators can understand the downstream continuation contract without cross-referencing the workflow reference.

#### Scenario: Operator reads complete-task contract

- **WHEN** an operator reads `skills/complete-task/SKILL.md`
- **THEN** the contract lists the canonical payload fields — `action`, `target_feature_id`, `target_task_id`, `reason`, and `requires_human_decision` — and their permitted `action` values (`start_task`, `finish_feature`, `stop`)
- **AND** the contract cross-references the authoritative schema in `docs/planning/WORKFLOW_REFERENCE.md` without requiring the operator to jump there to learn the field names

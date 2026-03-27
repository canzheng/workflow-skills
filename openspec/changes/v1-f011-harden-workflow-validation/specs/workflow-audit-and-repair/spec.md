## ADDED Requirements

### Requirement: Workflow diagnosis reports missing planning scaffold as findings
The read-only workflow diagnosis SHALL report missing planning scaffold as structured findings instead of terminating with an uncaught exception.

#### Scenario: Diagnose handles missing current version
- **WHEN** diagnosis runs and `docs/planning/current_version` is missing
- **THEN** it emits a structured finding describing the missing scaffold
- **AND** it returns JSON output rather than a Python traceback

#### Scenario: Diagnose handles missing active backlog
- **WHEN** diagnosis resolves the active version but the linked `BACKLOG.md` is missing
- **THEN** it emits a structured finding describing the missing backlog
- **AND** it continues producing an operator-facing report

### Requirement: Workflow audit validates shaping artifact baseline
The workflow audit SHALL require shaped promoted work to retain the baseline authored OpenSpec artifacts created by `openspec-propose`.

#### Scenario: Audit rejects shaping feature missing baseline artifacts
- **WHEN** the workflow audit inspects a feature in `[SHAPING]`
- **THEN** it requires the linked OpenSpec change to contain `proposal.md`, `design.md`, and `tasks.md`
- **AND** it reports a workflow error when any of those files are missing

### Requirement: Workflow audit validates archived change state for completed features
The workflow audit SHALL treat archived linked-change state as the expected source of truth for completed post-adoption features.

#### Scenario: Audit checks completed feature archive resolution
- **WHEN** the workflow audit inspects a feature in `[DONE]` that is not marked `legacy-exempt`
- **THEN** it requires the linked OpenSpec change to be absent from `openspec/changes/<change-id>/`
- **AND** it requires exactly one matching directory under `openspec/changes/archive/*-<change-id>/`

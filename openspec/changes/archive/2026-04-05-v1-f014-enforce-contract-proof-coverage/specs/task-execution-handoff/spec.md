## ADDED Requirements

### Requirement: Task execution plans expose proof obligations before code execution
Workflow task execution SHALL require each task-scoped implementation plan to expose the contract surface and proof obligations that execution is expected to satisfy.

#### Scenario: Start-task validates implementation-plan proof structure
- **WHEN** `start-task` selects a top-level OpenSpec task for execution
- **THEN** the linked implementation plan records the task's contract surface and proof obligations
- **AND** the plan records the required validation classes for that task before code execution begins
- **AND** `start-task` refuses to continue when those sections are missing or empty

### Requirement: Task execution plans declare when unit-only proof is acceptable
Workflow task execution SHALL not silently treat narrow helper-level checks as sufficient proof for broader behavioral work.

#### Scenario: Behavioral task requires runtime-facing validation coverage
- **WHEN** a task implementation plan declares behavioral, orchestration, persistence, repair, or prompt-interface change surface
- **THEN** the plan records at least one runtime-facing validation class such as integration, runtime-path, or manual artifact inspection
- **AND** the workflow rejects a unit-only validation plan unless the plan includes an explicit unit-only justification

#### Scenario: Start-task rejects known anti-surrogate proof patterns
- **WHEN** a task implementation plan proposes helper-only proof for orchestration behavior, file-presence proof for structured assets, bookkeeping-only proof for repair behavior, or isolated helper proof without execution-path coverage
- **THEN** `start-task` does not treat that plan as sufficient execution proof
- **AND** the workflow requires the plan to add a matching runtime-facing validation class or an explicit narrowed-scope justification

### Requirement: Completion gates reuse the same proof-plan contract
Task completion SHALL require the active task's implementation plan to remain valid under the same proof-structure rules enforced at task start.

#### Scenario: Complete-task validates the active plan before closure
- **WHEN** `complete-task` resolves the active top-level task
- **THEN** it verifies that the linked implementation plan still exposes contract surface, proof obligations, and validation classes
- **AND** it refuses task closure when the active plan no longer satisfies that structure

### Requirement: Completion reconciles proof obligations to categorized evidence
Task completion SHALL reconcile declared proof obligations to categorized validation evidence before closure is accepted.

#### Scenario: Complete-task checks obligation-aware evidence
- **WHEN** `complete-task` closes an active top-level task
- **THEN** the recorded evidence covers each declared proof obligation with one or more evidence categories such as `schema`, `runtime_path`, `artifact_repair`, `prompt_contract`, `orchestration`, or `negative_case`
- **AND** completion does not treat uncategorized or unrelated passing checks as sufficient proof for uncovered obligations

### Requirement: Test changes are reviewed for contract narrowing
Workflow execution review SHALL treat test changes as potential contract-surface changes rather than as neutral implementation detail by default.

#### Scenario: Task modifies tests alongside implementation
- **WHEN** a task adds or modifies tests
- **THEN** the execution review asks whether those assertions narrow the contract relative to the task plan
- **AND** the review compares the changed tests to the declared proof obligations, not only to the current implementation

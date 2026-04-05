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

### Requirement: Completion gates reuse the same proof-plan contract
Task completion SHALL require the active task's implementation plan to remain valid under the same proof-structure rules enforced at task start.

#### Scenario: Complete-task validates the active plan before closure
- **WHEN** `complete-task` resolves the active top-level task
- **THEN** it verifies that the linked implementation plan still exposes contract surface, proof obligations, and validation classes
- **AND** it refuses task closure when the active plan no longer satisfies that structure

## ADDED Requirements

### Requirement: Skill entry scripts import a shared CLI preamble module

Every Python script under `skills/<skill>/scripts/` that serves as a skill entry point SHALL import its common CLI preamble — the `WorkflowError` exception type, the `repo_root()` resolver, the `read_backlog()` helper (when used), and the skills-root path resolver — from a shared module inside `skills/_workflow/` rather than redefining any of those names locally.

#### Scenario: New skill entry script inherits the shared preamble

- **WHEN** a contributor adds a new script under `skills/<skill>/scripts/` that needs to resolve the repository root, read the active backlog, or raise a workflow-level error
- **THEN** the script imports those names from the shared `skills/_workflow/` CLI helpers module
- **AND** the script does not redeclare `class WorkflowError`, `def repo_root`, or `def read_backlog` locally

#### Scenario: Existing script is audited against the shared preamble

- **WHEN** a reviewer inspects any existing `skills/*/scripts/*.py` entry script
- **THEN** the script imports `WorkflowError`, `repo_root`, and (where applicable) `read_backlog` from the shared module
- **AND** the script contains no local redefinition of those names

### Requirement: Skill entry scripts use an anchor-based skills-root resolver

The path used by skill entry scripts to locate the `skills/` root when inserting it on `sys.path` SHALL be computed by walking upward from `__file__` for the `_workflow/` sibling marker directory, rather than by a fixed `parents[N]` index.

#### Scenario: Script continues to resolve skills root after a directory move

- **WHEN** a skill's entry script is moved to a different directory depth within the repository
- **THEN** the anchor-based resolver still locates the correct `skills/` directory
- **AND** the script does not silently resolve to a wrong path or fail to import `_workflow` modules

### Requirement: Integration-test runtime is justified by coverage that cannot be expressed at unit level

Tests under `tests/` that execute real subprocess calls against skill resolver scripts SHALL be justified by coverage that materially differs from what unit tests calling the Python entry points directly would provide, and that justification SHALL be documented in the test file or an adjacent module docstring.

#### Scenario: Subprocess-driven test exists alongside an equivalent direct-call test

- **WHEN** an integration test runs a skill resolver script via `subprocess.run`
- **THEN** the test asserts on something that unit-level direct-call coverage cannot express — subprocess argv handling, exit codes, stdout byte-formatting, or an end-to-end path through `git`, `openspec`, or `lessons`
- **AND** the intent is either explicit in the test file's docstring or obvious from the assertions

# Feature: Harden Installer And Dev Environment

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f013`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `v1-f013-harden-installer-and-dev-environment`
- OpenSpec Specs:
  - `openspec/specs/repo-development-tooling/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-27`
- Last Updated: `2026-03-28`

## 1. Validation Log
- `2026-03-27` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass before promoting the feature to [READY] and pass after moving the feature to [READY]`
  - Inspection: `openspec/changes/v1-f013-harden-installer-and-dev-environment/{proposal,design,tasks}.md` and `openspec/changes/v1-f013-harden-installer-and-dev-environment/specs/repo-development-tooling/spec.md`
  - Result: `proposal.md`, `design.md`, `tasks.md`, and the linked change delta spec are present; top-level OpenSpec task \`1\` resolves to workflow status \`ready\`, while tasks \`2\` and \`3\` remain blocked by explicit \`Depends On\` references.`
  - Run: `openspec validate v1-f013-harden-installer-and-dev-environment --type change --json --no-interactive`
  - Result: `pass`
- `2026-03-28` Task `1`:
  - Run: `bin/run-python.sh -m unittest tests.test_install_script -v`
  - Result: `the new missing-marker initialization expectation failed before the fix because install.sh still rejected an existing AGENTS.md without workflow markers, then the full installer test module passed after the task-1 changes; 3 tests ran and all passed`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass with the feature in [IN_PROGRESS] and task 1 active, then pass again after clearing Current Task and checking off OpenSpec task 1`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `pass after closing nested checklist items 1.1, 1.2, and 1.3 while task 1 remained active; completion_handoff.decision = stay_in_progress, next_ready_task_ids = ['2'], and remaining_open_task_ids = ['2', '3']`
  - Inspection: `git diff -- install.sh tests/test_install_script.py README.md openspec/changes/v1-f013-harden-installer-and-dev-environment/tasks.md openspec/changes/v1-f013-harden-installer-and-dev-environment/implementation-plans/1.md docs/planning/versions/v1/BACKLOG.md docs/planning/versions/v1/features/v1-f013-harden-installer-and-dev-environment.md`
  - Result: `reviewed locally; task-scoped changes are limited to installer control flow, focused installer coverage, rsync documentation, the task implementation plan, OpenSpec task state, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`
  - Review: `Focused local spec-compliance and code-quality review found no correctness, regression, or scope-drift issues in the task-1 diff.`
  - Review Follow-up: `A late spec-compliance pass identified that the installer-behavior TDD coverage overlapped the original task 3 wording, so the remaining task-3 scope was narrowed to the managed-environment regression work that still depends on task 2.`
- `2026-03-28` Task `2`:
  - Run: `python3 - <<'PY' ...`
  - Result: `pass: environment.yml declares python>=3.10 and channels [conda-forge, defaults]`
  - Run: `bin/run-python.sh -m unittest tests.test_run_python_wrapper -v`
  - Result: `19 tests ran and all passed after the environment contract change`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass with the feature in [IN_PROGRESS] and task 2 active, then pass again after clearing Current Task and checking off OpenSpec task 2`
  - Inspection: `git diff -- environment.yml openspec/changes/v1-f013-harden-installer-and-dev-environment/implementation-plans/2.md docs/planning/versions/v1/features/v1-f013-harden-installer-and-dev-environment.md`
  - Result: `reviewed locally; task-scoped changes are limited to the Conda environment contract, the task implementation plan, and workflow bookkeeping`
  - Run: `git diff --check`
  - Result: `pass`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `pass after closing nested checklist items 2.1 and 2.2 while task 2 remained active; completion_handoff.decision = stay_in_progress, next_ready_task_ids = ['3'], and remaining_open_task_ids = ['3']`
  - Review: `Focused local spec-compliance and code-quality review found no correctness, reproducibility, or scope-drift issues in the task-2 diff.`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `n/a`
  - Notes: Shaping artifacts are complete for `v1-f013-harden-installer-and-dev-environment`. Top-level OpenSpec task `1` is ready to execute, so the feature can move to `[READY]`.
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `clean feature worktree at ../worktrees/workflow-skills/v1-f013-harden-installer-and-dev-environment on branch v1-f013-harden-installer-and-dev-environment`
  - Notes: Task `1` entered active execution after a passing workflow audit, resolver confirmation that it is the next ready task, and a passing baseline run of `bin/run-python.sh -m unittest tests.test_install_script -v`. The task implementation plan now lives at `openspec/changes/v1-f013-harden-installer-and-dev-environment/implementation-plans/1.md`.
- `2026-03-28`:
  - Current Task: `none`
  - Worktree State: `task-1 changes ready to commit on branch v1-f013-harden-installer-and-dev-environment in ../worktrees/workflow-skills/v1-f013-harden-installer-and-dev-environment`
  - Notes: Completed task `1`. `install.sh` now initializes an existing unmarked AGENTS.md while keeping the missing-file path strict, `README.md` now documents the installer's `rsync` dependency, and task `2` is the next ready execution unit while the remaining task-3 regression scope is limited to the managed-environment coverage that still depends on task `2`.
- `2026-03-28`:
  - Current Task: `2`
  - Worktree State: `clean feature worktree at ../worktrees/workflow-skills/v1-f013-harden-installer-and-dev-environment on branch v1-f013-harden-installer-and-dev-environment`
  - Notes: Task `2` entered active execution after `resolve_start_task.py --repo-root .` confirmed it as the next ready top-level OpenSpec task, task `1` was already checked off in `tasks.md`, and the task implementation plan was updated at `openspec/changes/v1-f013-harden-installer-and-dev-environment/implementation-plans/2.md`.
- `2026-03-28`:
  - Current Task: `none`
  - Worktree State: `task-2 changes ready to commit on branch v1-f013-harden-installer-and-dev-environment in ../worktrees/workflow-skills/v1-f013-harden-installer-and-dev-environment`
  - Notes: Completed task `2`. `environment.yml` now declares `python>=3.10` and the explicit Conda channels `conda-forge` and `defaults`, and task `3` is the next ready execution unit for the remaining managed-environment regression coverage.

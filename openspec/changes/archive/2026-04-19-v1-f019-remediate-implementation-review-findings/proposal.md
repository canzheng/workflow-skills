## Why

A targeted implementation review of the `skills/_workflow/` library, the nine skill entry scripts, the SKILL.md contract docs, and the test suites surfaced 11 concrete issues spanning code duplication, a dead conditional branch, terminology drift between SKILL.md files and the authoritative `WORKFLOW_REFERENCE.md`, test-suite runtime imbalance, and missing shared fixtures. Each finding is small on its own, but together they erode the consistency guarantees this workflow is supposed to enforce: scripts silently diverge when helpers are copy-pasted, docs say "task-scoped" where the stable spec says "stage-scoped," and a 100s integration test file crowds out faster unit coverage. Fixing them as a single coordinated remediation is cheaper than compounding the drift across future features.

## What Changes

- Extract shared CLI preamble — `WorkflowError`, `repo_root()`, `read_backlog()`, and the `SKILLS_ROOT` resolution pattern — into a new `skills/_workflow/cli_helpers.py` module; migrate all nine skill entry scripts (`audit-workflow`, `diagnose-workflow`, `shape-backlog-item`, `start-task`, `complete-task`, `finish-feature`, `prioritize-backlog`, `autonomous-backlog-loop`, `initialize-workflow-artifacts`) to import the shared helpers.
- Remove duplicate behavior implementations: delete the private `_list_git_worktree_roots` copy in `skills/start-task/scripts/resolve_start_task.py` in favor of the public helper in `skills/_workflow/workflow_state.py`; drop the redundant regex redefinitions in `skills/audit-workflow/scripts/audit_workflow.py`.
- Fix the dead conditional branch in `parse_feature_id` at `skills/_workflow/workflow_state.py:1225` and the double-split inefficiency on the same line.
- Align SKILL.md terminology with the authoritative `docs/planning/WORKFLOW_REFERENCE.md`: the `shape-backlog-item` and `ready-feature` skills must use "stage-scoped" for the `Retrieved Lesson IDs` line they own (the stage-level skills), matching the stable contract.
- Cross-reference the `completion_handoff` payload schema in `skills/complete-task/SKILL.md` so operators see the field list without having to jump to `WORKFLOW_REFERENCE.md`.
- Normalize `--feature-id` CLI surface across skill scripts: either required/optional everywhere or documented per-skill in the script argparse help.
- Introduce a shared `tests/conftest.py` carrying the repo-scaffold factories that `tests/test_diagnose_workflow.py` and `skills/_workflow/tests/test_workflow_scripts.py` currently reimplement.
- Rebalance `tests/test_workflow_openspec_integration.py`: convert a representative subset of subprocess-driven tests into direct Python-entry calls so unit-level coverage grows and the full-suite runtime drops meaningfully; keep a small subprocess smoke set for end-to-end confidence.

## Capabilities

### Modified Capabilities

- `repo-development-tooling`: scripts SHALL import the shared CLI preamble module rather than redefining error classes, repo-root resolution, or `read_backlog()` locally; SKILLS_ROOT-style path resolution SHALL use an anchor-based pattern resilient to script relocation; the integration-test runtime budget SHALL be justified by coverage that cannot be expressed at unit level.
- `feature-execution-tracking`: the canonical `Retrieved Lesson IDs: ...` line emitted by a stage-level skill (shaping, readiness) SHALL be referred to as "stage-scoped" in that skill's contract doc; the equivalent line emitted by task-level skills (`start-task`, `complete-task`) remains "task-scoped." The `completion_handoff` payload schema SHALL be discoverable directly from `skills/complete-task/SKILL.md` without requiring a cross-document lookup.

## Impact

- `skills/_workflow/cli_helpers.py` (new)
- `skills/_workflow/workflow_state.py`
- `skills/audit-workflow/scripts/audit_workflow.py`
- `skills/diagnose-workflow/scripts/diagnose_workflow.py`
- `skills/shape-backlog-item/scripts/render_feature_file.py`
- `skills/start-task/scripts/resolve_start_task.py`
- `skills/complete-task/scripts/resolve_complete_task.py`
- `skills/finish-feature/scripts/resolve_finish_feature.py`
- `skills/prioritize-backlog/scripts/prioritize_backlog.py`
- `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py`
- `skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py`
- `skills/shape-backlog-item/SKILL.md`
- `skills/ready-feature/SKILL.md`
- `skills/complete-task/SKILL.md`
- `tests/conftest.py` (new)
- `tests/test_workflow_openspec_integration.py`
- `tests/test_workflow_contract_docs.py` (to cover the new stage-scoped terminology assertions)
- `skills/_workflow/tests/test_workflow_scripts.py`
- `openspec/specs/repo-development-tooling/spec.md`
- `openspec/specs/feature-execution-tracking/spec.md`

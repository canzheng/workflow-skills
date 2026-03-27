# Feature: Close Workflow Review Gaps

Create this file only when a backlog item moves from `[BACKLOG]` to `[SHAPING]`.

## 0. Meta
- Feature ID: `v1-f010`
- Version: `v1`
- Backlog Reference: `docs/planning/versions/v1/BACKLOG.md#in_progress`
- OpenSpec Change: `v1-f010-close-workflow-review-gaps`
- OpenSpec Specs:
  - `openspec/specs/workflow-audit-and-repair/spec.md`
  - `openspec/specs/task-execution-handoff/spec.md`
  - `openspec/specs/feature-execution-tracking/spec.md`
  - `openspec/specs/openspec-change-integration/spec.md`
- Current Task: `none`
  - Use `none` when no task is actively executing, including handoff gaps inside an `[IN_PROGRESS]` feature.
  - Otherwise use the raw top-level OpenSpec task ID, for example `1`.
- Created: `2026-03-27`
- Last Updated: `2026-03-27`

## 1. Validation Log
- `2026-03-27` Readiness Review:
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass before promoting the feature to [READY]`
  - Run: `openspec validate v1-f010-close-workflow-review-gaps --type change --json --no-interactive`
  - Result: `pass; summary totals report 1 passed and 0 failed`
  - Inspection: `openspec/changes/v1-f010-close-workflow-review-gaps/{proposal,design,tasks}.md` and linked stable specs
  - Result: `proposal.md`, `design.md`, `tasks.md`, and the linked stable spec paths are present; the shaping artifacts now explicitly enumerate every review-finding bucket and the planned validation coverage for those findings`
  - Run: `python3` `skills._workflow.workflow_state.parse_tasks(...)` over `docs/planning/versions/v1/features/v1-f010-close-workflow-review-gaps.md`
  - Result: `top-level OpenSpec tasks 1 and 4 resolve to workflow status ready, while tasks 2, 3, and 5 remain todo behind declared dependencies`
- `2026-03-27` Task `1` Completion:
  - Run: `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_state.py -q`
  - Result: `pass; 27 passed in 0.04s`
  - Run: `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_scripts.py -q`
  - Result: `pass; 22 passed in 1.29s`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass after task-1 implementation`
  - Run: `git diff --check && git status --short`
  - Result: `no patch-format errors; only task-1 implementation files, workflow-state files, and the task implementation plan were pending before closure`
  - Run: `python - <<'PY' ... compute_completion_handoff(...) ... PY`
  - Result: `stay_in_progress; next ready tasks are 2 and 4, with remaining open tasks 2, 3, 4, and 5`
  - Review: `task-level code review completed with no findings before completion`
  - Result: `shared workflow helpers now detect malformed board section order and promoted features missing OpenSpec Specs metadata`
- `2026-03-27` Task `2` Completion:
  - Run: `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_scripts.py -q`
  - Result: `pass; 24 passed in 1.43s`
  - Run: `bin/run-python.sh -m pytest tests/test_diagnose_workflow.py -q`
  - Result: `pass; 7 passed in 0.40s`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass after task-2 implementation`
  - Run: `python skills/diagnose-workflow/scripts/diagnose_workflow.py --repo-root .`
  - Result: `status ok; no findings; active task count 1 for task 2 before closure`
  - Run: `git diff --check && git status --short`
  - Result: `no patch-format errors; only task-2 implementation files, feature workflow state, and the task implementation plan were pending before closure`
  - Run: `python - <<'PY' ... compute_completion_handoff(...) ... PY`
  - Result: `stay_in_progress; next ready tasks are 3 and 4, with remaining open tasks 3, 4, and 5`
  - Review: `task-level code review completed with no findings before completion`
  - Result: `audit and diagnose now consume the stricter structural checks for malformed canonical backlog sections and missing promoted-feature OpenSpec Specs metadata`
- `2026-03-27` Task `3` Completion:
  - Run: `bin/run-python.sh -m pytest tests/test_workflow_openspec_integration.py -q`
  - Result: `pass; 24 passed in 1.40s`
  - Run: `bin/run-python.sh -m pytest tests/test_diagnose_workflow.py -q`
  - Result: `pass; 8 passed in 0.47s`
  - Run: `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_scripts.py -q`
  - Result: `pass; 24 passed in 1.44s`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass after task-3 implementation`
  - Run: `git diff --check && git status --short`
  - Result: `no patch-format errors; only task-3 validation coverage files, feature workflow state, and the task implementation plan were pending before closure`
  - Run: `python - <<'PY' ... compute_completion_handoff(...) ... PY`
  - Result: `stay_in_progress; next ready task is 4, with remaining open tasks 4 and 5`
  - Review: `task-level code review completed with no findings before completion`
  - Result: `broader audit integration coverage and combined diagnose false-healthy regression now explicitly cover implementation findings F1 through F3`
- `2026-03-27` Task `4` Completion:
  - Run: `git diff --check`
  - Result: `pass; no patch-format errors in the task-4 doc, spec, workflow-state, or implementation-plan changes`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass after task-4 source-of-truth cleanup`
  - Run: `git status --short`
  - Result: `only the intended task-4 files were pending before closure: AGENTS-global-workflow.md, README.md, docs/planning/versions/v1/VERSION_SCOPE.md, docs/planning/versions/v1/features/{v1-f001,v1-f002,v1-f006,v1-f008,v1-f010}*.md, openspec/specs/openspec-change-integration/spec.md, openspec/changes/v1-f010-close-workflow-review-gaps/tasks.md, and openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/4.md`
  - Inspection: `rg -n "Define the version goal|Define the bar for completing this version|TBD - created by archiving change|Manual \`\[DONE\]\` transition was applied|Feature completion accepted\\. The linked OpenSpec change is archived|Feature reached \`\[DONE\]\` after" AGENTS-global-workflow.md README.md docs/planning/versions/v1/VERSION_SCOPE.md openspec/specs/openspec-change-integration/spec.md docs/planning/versions/v1/features/v1-f001-legacy-openspec-audit-migration.md docs/planning/versions/v1/features/v1-f002-integrate-openspec-shaping-readiness.md docs/planning/versions/v1/features/v1-f006-add-feature-completion-handoff-gate.md docs/planning/versions/v1/features/v1-f008-clarify-workflow-owned-task-readiness.md`
  - Result: `pass; the touched source-of-truth files no longer contain the placeholder text or superseded contradictory handoff phrases called out by findings F4 through F7`
  - Review: `manual task-scope diff review against implementation-plans/4.md`
  - Result: `no out-of-scope changes found; task-4 edits stay limited to source-of-truth artifact cleanup`
- `2026-03-27` Finding Coverage Matrix:

  | Finding | Fix Scope | Validation / Inspection Path | Feature-File Evidence |
  | --- | --- | --- | --- |
  | `F1` | Audit rejects promoted features missing `OpenSpec Specs` metadata | Task `1` helper/script validation plus task `3` integration coverage | `2026-03-27` Finding Coverage Evidence `F1` |
  | `F2` | Audit rejects extra canonical sections after `[DEFER]` | Task `1` helper validation plus task `3` integration coverage | `2026-03-27` Finding Coverage Evidence `F2` |
  | `F3` | Diagnose reports malformed workflow state as findings instead of healthy | Task `2` diagnose-focused coverage plus task `3` broader regression coverage | `2026-03-27` Finding Coverage Evidence `F3` |
  | `F4` | `finish-feature` wording aligned across workflow source-of-truth docs | Task `4` targeted source-of-truth inspection | `2026-03-27` Finding Coverage Evidence `F4` |
  | `F5` | `VERSION_SCOPE.md` placeholder text replaced with concrete version scope | Task `4` targeted source-of-truth inspection | `2026-03-27` Finding Coverage Evidence `F5` |
  | `F6` | `openspec-change-integration` purpose text replaced with concrete stable-spec purpose | Task `4` targeted source-of-truth inspection | `2026-03-27` Finding Coverage Evidence `F6` |
  | `F7` | Historical feature notes repaired so they preserve chronology without contradicting the accepted workflow | Task `4` targeted source-of-truth inspection | `2026-03-27` Finding Coverage Evidence `F7` |
- `2026-03-27` Finding Coverage Evidence:
  - `F1`:
    - Evidence Source: `2026-03-27` Task `1` Completion and Task `3` Completion
    - Validation: `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_state.py -q`, `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_scripts.py -q`, and `bin/run-python.sh -m pytest tests/test_workflow_openspec_integration.py -q`
    - Result: `shared helper, script, and integration coverage now explicitly reject promoted features missing linked OpenSpec spec metadata without regressing repository audit health`
  - `F2`:
    - Evidence Source: `2026-03-27` Task `1` Completion and Task `3` Completion
    - Validation: `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_state.py -q` and `bin/run-python.sh -m pytest tests/test_workflow_openspec_integration.py -q`
    - Result: `canonical backlog validation and the broader audit integration suite now reject extra sections appended after [DEFER]`
  - `F3`:
    - Evidence Source: `2026-03-27` Task `2` Completion and Task `3` Completion
    - Validation: `bin/run-python.sh -m pytest tests/test_diagnose_workflow.py -q` and `bin/run-python.sh -m pytest skills/_workflow/tests/test_workflow_scripts.py -q`
    - Result: `diagnose coverage now reports malformed board shape and missing promoted-feature spec linkage as findings instead of returning a false healthy status`
  - `F4`:
    - Evidence Source: `2026-03-27` Task `4` Completion
    - Inspection: `rg -n "finish-feature" AGENTS-global-workflow.md README.md openspec/specs/task-execution-handoff/spec.md openspec/specs/feature-execution-tracking/spec.md`
    - Result: `workflow routing, lifecycle wording, and stable spec behavior now agree that finish-feature runs from [IN_PROGRESS], owns validate/archive, and moves the feature to [DONE] before downstream branch finalization`
  - `F5`:
    - Evidence Source: `2026-03-27` Task `4` Completion
    - Inspection: `docs/planning/versions/v1/VERSION_SCOPE.md`
    - Result: `the version goal, exit criteria, deferral state, and cross-feature decisions are now concrete and no longer placeholder text`
  - `F6`:
    - Evidence Source: `2026-03-27` Task `4` Completion
    - Inspection: `openspec/specs/openspec-change-integration/spec.md`
    - Result: `the stable spec purpose now concretely describes feature-to-change linkage, readiness artifacts, and workflow-derived task structure/readiness`
  - `F7`:
    - Evidence Source: `2026-03-27` Task `4` Completion
    - Inspection: `docs/planning/versions/v1/features/v1-f001-legacy-openspec-audit-migration.md`, `docs/planning/versions/v1/features/v1-f002-integrate-openspec-shaping-readiness.md`, `docs/planning/versions/v1/features/v1-f006-add-feature-completion-handoff-gate.md`, and `docs/planning/versions/v1/features/v1-f008-clarify-workflow-owned-task-readiness.md`
    - Result: `historical notes now preserve migration and pre-contract chronology without implying that manual [DONE] transitions or superseded completion flows are the accepted workflow`
- `2026-03-27` Finding Coverage Completeness Check:
  - Run: `python - <<'PY' ... feature-file scan for F1 through F7 ... PY`
  - Result: `all_findings_present=F1,F2,F3,F4,F5,F6,F7; every finding named in the matrix has a matching evidence entry in this feature file before feature completion`
- `2026-03-27` Task `5` Completion:
  - Run: `git diff --check`
  - Result: `pass; no patch-format errors in the task-5 feature-file, task-ledger, or implementation-plan updates`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"`
  - Result: `pass after task-5 evidence mapping updates`
  - Run: `git status --short`
  - Result: `only the intended task-5 files were pending before closure: docs/planning/versions/v1/features/v1-f010-close-workflow-review-gaps.md, openspec/changes/v1-f010-close-workflow-review-gaps/tasks.md, and openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/5.md`
  - Run: `python "${CODEX_HOME:-$HOME/.codex}/skills/complete-task/scripts/resolve_complete_task.py"`
  - Result: `pass; completion_handoff.decision=confirm_feature_acceptance, all_top_level_tasks_complete=true, and remaining_open_task_ids=[] before task-state closure`
  - Review: `manual task-scope diff review against implementation-plans/5.md`
  - Result: `no out-of-scope changes found; task-5 work stays limited to explicit finding-to-validation evidence in the feature file plus matching task-ledger updates`

## 2. Handoff Notes
- `2026-03-27`:
  - Current Task: `1`
  - Worktree State: `feature worktree created at ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps on branch v1-f010-close-workflow-review-gaps`
  - Notes: Task `1` entered active execution after a passing workflow audit in the clean feature worktree. The task implementation plan now lives at `openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/1.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `task-1 changes committed on branch v1-f010-close-workflow-review-gaps in ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps`
  - Notes: Task `1` is complete. The feature remains `[IN_PROGRESS]`; next ready tasks are `2` and `4`, with `2` as the next ordered task.
- `2026-03-27`:
  - Current Task: `2`
  - Worktree State: `resumed clean feature worktree at ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps on branch v1-f010-close-workflow-review-gaps`
  - Notes: Task `2` entered active execution after a passing workflow audit and resolver confirmation that it is the next ready task. The task implementation plan now lives at `openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/2.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `task-2 changes committed on branch v1-f010-close-workflow-review-gaps in ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps`
  - Notes: Task `2` is complete. The feature remains `[IN_PROGRESS]`; next ready tasks are `3` and `4`, with `3` as the next ordered task.
- `2026-03-27`:
  - Current Task: `3`
  - Worktree State: `resumed clean feature worktree at ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps on branch v1-f010-close-workflow-review-gaps`
  - Notes: Task `3` entered active execution after a passing workflow audit and resolver confirmation that it is the next ready task. The task implementation plan now lives at `openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/3.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `task-3 changes committed on branch v1-f010-close-workflow-review-gaps in ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps`
  - Notes: Task `3` is complete. The feature remains `[IN_PROGRESS]`; task `4` is now the next ready task.
- `2026-03-27`:
  - Current Task: `4`
  - Worktree State: `resumed clean feature worktree at ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps on branch v1-f010-close-workflow-review-gaps`
  - Notes: Task `4` entered active execution after a passing workflow audit and confirmation that the remaining scope is limited to source-of-truth artifact cleanup. The task implementation plan now lives at `openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/4.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `task-4 changes committed on branch v1-f010-close-workflow-review-gaps in ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps`
  - Notes: Task `4` is complete. The feature remains `[IN_PROGRESS]`; task `5` is now the next ready task because tasks `2`, `3`, and `4` are all done.
- `2026-03-27`:
  - Current Task: `5`
  - Worktree State: `resumed clean feature worktree at ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps on branch v1-f010-close-workflow-review-gaps`
  - Notes: Task `5` entered active execution after a passing workflow audit and resolver confirmation that it is the next ready task. The task implementation plan now lives at `openspec/changes/v1-f010-close-workflow-review-gaps/implementation-plans/5.md`.
- `2026-03-27`:
  - Current Task: `none`
  - Worktree State: `task-5 changes committed on branch v1-f010-close-workflow-review-gaps in ../worktrees/workflow-skills/v1-f010-close-workflow-review-gaps`
  - Notes: Task `5` is complete. All top-level OpenSpec tasks are now done, the feature remains `[IN_PROGRESS]`, and the next handoff target is `finish-feature`.

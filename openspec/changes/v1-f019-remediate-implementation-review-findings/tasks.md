## 1. Shared CLI Helpers And Script Deduplication

- [x] 1 Land `skills/_workflow/cli_helpers.py` and migrate all nine skill entry scripts to it, removing the duplicate helpers and divergent worktree-root fallback
  - [x] 1.1 Create `skills/_workflow/cli_helpers.py` exporting `WorkflowError`, `repo_root()`, `read_backlog()`, and an anchor-based `resolve_skills_root()` that walks upward for the `_workflow/` sibling directory
  - [x] 1.2 Migrate all nine script entry files — `skills/audit-workflow/scripts/audit_workflow.py`, `skills/diagnose-workflow/scripts/diagnose_workflow.py`, `skills/shape-backlog-item/scripts/render_feature_file.py`, `skills/start-task/scripts/resolve_start_task.py`, `skills/complete-task/scripts/resolve_complete_task.py`, `skills/finish-feature/scripts/resolve_finish_feature.py`, `skills/prioritize-backlog/scripts/prioritize_backlog.py`, `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py`, `skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py` — to import the shared preamble and remove their local copies of `WorkflowError`, `repo_root`, and `read_backlog`
  - [x] 1.3 Delete the private `_list_git_worktree_roots` in `skills/start-task/scripts/resolve_start_task.py` and replace callers with the public helper exported by `skills/_workflow/workflow_state.py`; converge on a single failure contract
  - [x] 1.4 Drop the redundant `FEATURE_ID_RE` and `TASK_STATUS_RE` redefinitions in `skills/audit-workflow/scripts/audit_workflow.py` and import them from `_workflow.workflow_state`; leave `BACKLOG_REF_RE` in place since it is unique to `audit-workflow`
  - [x] 1.5 Replace the `SKILLS_ROOT = Path(__file__).resolve().parents[2]` idiom with the new anchor-based resolver in every migrated script

## 2. Code Quality And Contract-Doc Alignment

- [x] 2 Fix the narrow code defects and bring operator-facing docs into agreement with the stable spec
  - [x] 2.1 Rewrite `parse_feature_id` in `skills/_workflow/workflow_state.py:1225` to remove the unreachable conditional branch and the double `stem.split("-", 2)` call
  - [x] 2.2 Update `skills/shape-backlog-item/SKILL.md:30` and `skills/ready-feature/SKILL.md:26` to say "stage-scoped canonical `Retrieved Lesson IDs: ...`" matching `docs/planning/WORKFLOW_REFERENCE.md:85`; update `tests/test_workflow_contract_docs.py` assertions to match
  - [x] 2.3 Add a short `Output Contract` block to `skills/complete-task/SKILL.md` that lists the `completion_handoff` payload fields (`action`, `target_feature_id`, `target_task_id`, `reason`, `requires_human_decision`) and cross-references `docs/planning/WORKFLOW_REFERENCE.md:77-78`
  - [x] 2.4 Apply the canonical `--feature-id` contract defined in `design.md` under "Decision: canonical `--feature-id` treatment is ambiguity-driven, not uniform" to the nine skill entry scripts and their argparse help text, and land the matching delta requirement in `openspec/changes/v1-f019-remediate-implementation-review-findings/specs/repo-development-tooling/spec.md`
  - [x] 2.5 Leave the `start-task`/`complete-task`/`ready-feature` SKILL.md preamble repetition in place per `design.md` under "Decision: keep SKILL.md preamble repetition explicit"; add a `test_workflow_contract_docs.py` assertion guarding the preamble wording so future drift is caught by tests rather than review

## 3. Test Suite Ergonomics

- [x] 3 Cut integration-test runtime and remove repo-scaffold helper duplication
  - [x] 3.1 Introduce `tests/conftest.py` with shared repo-scaffold factories currently reimplemented in `tests/test_diagnose_workflow.py` and `skills/_workflow/tests/test_workflow_scripts.py`
  - [x] 3.2 Audit `tests/test_workflow_openspec_integration.py` and classify every test method as `keep-as-subprocess` or `convert-to-direct-call` using the criterion that only tests asserting on subprocess argv, exit codes, or stdout byte-formatting keep their subprocess harness
  - [x] 3.3 Convert the direct-call subset to use the resolver Python entry points directly and assert on return values; keep the subprocess smoke set short and explicit
  - [x] 3.4 Record the before/after full-suite runtime in this task's implementation plan; target a ≥30% reduction as the success metric, and stop there rather than chasing lower numbers
  - [x] 3.5 Update `openspec/specs/repo-development-tooling/spec.md` with the integration-test runtime-justification requirement documented in the spec delta under `openspec/changes/v1-f019-remediate-implementation-review-findings/specs/repo-development-tooling/spec.md`

## 4. Validation And Handoff

- [x] 4 Run the narrowest combined validation slice for the remediation scope and record evidence in the feature file
  - [x] 4.1 Re-run `audit-workflow` in the feature worktree after every task-closure bookkeeping edit and at feature completion
  - [x] 4.2 Run `bin/run-python.sh -m unittest discover -s tests` and `bin/run-python.sh -m pytest skills/_workflow/tests -q`; record both before/after results
  - [x] 4.3 Record the remediation evidence in the feature file Validation Log so `finish-feature` can close `v1-f019` cleanly
  - Depends On:
    - `1`
    - `2`
    - `3`

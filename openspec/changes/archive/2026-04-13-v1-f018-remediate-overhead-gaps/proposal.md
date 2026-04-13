## Why

`v1-f018` reduced status-only workflow coordination overhead, but a post-merge implementation review found three shipped inconsistencies against the accepted design and implementation-plan scope:

- structured review verdicts were documented and parsed, but not wired into the readiness/task-completion workflow steps that should emit and use them
- selected-feature worktree continuation was tightened for the happy path, but the shared helper still falls back to the current checkout instead of failing closed when the intended feature worktree is missing
- the `complete-task` helper now exposes a canonical continuation payload, while the shipped `complete-task` skill contract and contract-doc assertions still describe the older status-only terminal handoff model

The feature should be reopened and remediated rather than leaving those gaps as known debt, because they undermine the same workflow-overhead reduction that `v1-f018` was meant to deliver.

## What Changes

- Reopen `v1-f018` under a new active remediation change instead of reusing the archived implementation change.
- Make `ready-feature` and `complete-task` emit the canonical structured review-verdict lines in feature handoff notes, and add at least one downstream consumer path that relies on that structured data rather than prose-only notes.
- Fail closed when selected-feature continuation cannot resolve the intended active feature worktree uniquely, instead of silently falling back to the current checkout.
- Align the `complete-task` skill guidance and contract-doc tests with the canonical `completion_handoff` continuation model that `v1-f018` already implemented in helper code.

## Capabilities

### Modified Capabilities

- `task-execution-handoff`: selected-feature continuation and `complete-task` guidance must consistently follow the canonical `completion_handoff` contract, including fail-closed worktree targeting for later execution continuation.
- `feature-execution-tracking`: structured review verdicts must be emitted by the workflow stages that own readiness and task-completion review, not only parsed after the fact.
- `workflow-audit-and-repair`: execution-scoped helpers must fail closed when the selected feature's intended worktree cannot be resolved, while still keeping unrelated drift separate from selected-feature blocking checks.

## Impact

- `skills/ready-feature/SKILL.md`
- `skills/complete-task/SKILL.md`
- `skills/_workflow/workflow_state.py`
- `skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py`
- `tests/test_workflow_contract_docs.py`
- `tests/test_workflow_openspec_integration.py`
- `skills/_workflow/tests/test_workflow_state.py`
- `skills/_workflow/tests/test_workflow_scripts.py`
- `openspec/specs/task-execution-handoff/spec.md`
- `openspec/specs/feature-execution-tracking/spec.md`
- `openspec/specs/workflow-audit-and-repair/spec.md`

- id: L-001
  status: active
  domain: workflow
  task_type:
    - feature_remediation
    - review_followup
  scope:
    - workflow_skills
    - resolver_contracts
  tags:
    - review-verdicts
    - contract-drift
    - runtime-consumers
  situation: A workflow change adds canonical structured metadata and parser support for a new handoff state such as review verdicts.
  signal: Contract docs, templates, and parser tests are green, but no runtime resolver or downstream workflow step reads the emitted metadata.
  what_worked: Updating the owning skill guidance and adding a real resolver consumer path turned the schema from parser-only support into executable workflow state.
  what_did_not_work: Treating docs, templates, and parser coverage as sufficient let the original feature ship without any runtime consumer of the new verdict state.
  lesson: When a workflow change introduces canonical handoff metadata, require both emitter guidance and at least one runtime consumer path in the same feature.
  applies_when: You are adding or changing machine-readable workflow metadata, handoff fields, or review state that downstream automation is expected to trust.
  rationale: Metadata that is only documented and parsed can still drift from real workflow behavior. A runtime consumer test proves the data actually matters to execution instead of existing only as dormant schema text.
  source_evidence: N-001 from v1-f018, plus the reopened remediation that added start-task consumption of canonical readiness review verdict state.
  do_differently_next_time: Add a task-level proof obligation that names the emitter path, the consumer path, and the runtime regression test before closing the feature.
  catch_earlier_by: During review, ask whether the new structured state is emitted by the owning workflow stage and consumed anywhere outside parser-only tests.
  confidence: high
  retrieved_count: 0
  applied_count: 0.0
  last_retrieved_at: ""
  last_applied_at: ""
  optional_example: In reopened v1-f018, canonical review-verdict lines were documented and parsed, but the gap remained until start-task surfaced the latest readiness verdict in resolver output and tests covered that runtime path.
  updated_at: 2026-04-14

- id: L-002
  status: active
  domain: reliability
  task_type:
    - feature_remediation
    - negative_path_testing
  scope:
    - workflow_skills
    - worktree_resolution
  tags:
    - worktrees
    - fail-closed
    - negative-path
  situation: A workflow hardening change is meant to stop automation from silently continuing when the intended feature worktree cannot be resolved.
  signal: Happy-path and dirty-worktree tests pass, but the shared helper still falls back to the current checkout when the active feature worktree is missing.
  what_worked: Adding an explicit missing-worktree regression test forced the helper to fail closed instead of preserving the old fallback.
  what_did_not_work: Positive-path coverage alone did not expose that the resolver still reused the current checkout when no unique active feature worktree existed.
  lesson: For worktree-targeting or continuation hardening, always add the missing-resource negative path, not just the preferred-path and dirty-state tests.
  applies_when: You are tightening resolver behavior around selected feature worktrees, branch/worktree reuse, or continuation targeting.
  rationale: Fallback behavior usually survives unless a test proves the exact absence case. Negative-path coverage is what turns a policy like fail-closed into real behavior.
  source_evidence: N-002 from v1-f018, plus the reopened remediation that changed resolve_feature_repo_root and added the missing-worktree autonomous-resolver regression.
  do_differently_next_time: Pair any \"prefer existing worktree\" change with explicit tests for missing worktree, multiple worktrees, and dirty worktree outcomes.
  catch_earlier_by: Review the shared helper itself and ask which exact test fails if the intended feature worktree is absent.
  confidence: high
  retrieved_count: 1
  applied_count: 1.0
  last_retrieved_at: "2026-04-19"
  last_applied_at: "2026-04-19"
  optional_example: In reopened v1-f018, autonomous continuation looked hardened because existing-worktree and dirty-worktree tests passed, but the helper still needed a dedicated missing-worktree regression to remove the stale checkout fallback. In v1-f019 task 1, L-002 drove the addition of tests/test_start_task_list_worktree_contract.py to guard the convergence of start-task onto the public list_git_worktree_roots against reintroducing a private copy with a diverging failure contract.
  updated_at: 2026-04-14

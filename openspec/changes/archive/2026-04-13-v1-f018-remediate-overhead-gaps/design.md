## Context

The reopened `v1-f018` scope is not a fresh redesign. It is a remediation pass over inconsistencies between the accepted `v1-f018` design and the shipped implementation:

- the canonical `completion_handoff` payload landed in helper code and autonomous-loop guidance
- `finish-feature --feature-id` scoping landed
- stable docs and templates gained structured review-verdict fields

But the shipped feature still diverges from its own design in ways that matter operationally:

- structured review verdicts are parser-only because the workflow stages that own those review gates do not yet emit the canonical verdict lines
- the shared feature-root resolver still falls back to the current checkout when the intended feature worktree is missing, despite the remediation scope promising fail-closed continuation
- `complete-task` operator guidance and contract-doc assertions still describe the old terminal handoff model instead of the canonical continuation payload

## Goals / Non-Goals

**Goals**

- Make structured review verdicts real workflow state, not only schema text plus parser support.
- Make selected-feature continuation fail closed when the intended active feature worktree is missing or ambiguous.
- Remove the remaining contract drift between helper behavior and operator-facing `complete-task` guidance.

**Non-Goals**

- Rework the overall `v1-f018` continuation payload shape.
- Reopen the archived `v1-f018-reduce-status-only-workflow-overhead` change directory.
- Expand the remediation scope into unrelated workflow ergonomics or new lifecycle stages.

## Decisions

### Decision: Emit canonical structured review verdict lines at the workflow stages that own review gates

`ready-feature` and `complete-task` must stop treating structured review verdicts as documentation-only metadata. Each stage that already owns a review gate should write the canonical handoff-note lines required by the stable spec:

- `Review Scope`
- `Review Target`
- `Review Verdict`
- `Blocking Findings`
- `Review Terminal`

At minimum:

- `ready-feature` writes the readiness verdict on the stage-scoped handoff entry
- `complete-task` writes the task review verdict on the task-completion handoff entry when its execution-path review expectation is satisfied or fails

Downstream consumption must not remain parser-only. At least one runtime path should read those canonical lines as structured verdict state rather than relying on prose summary text.

### Decision: Selected-feature continuation fails closed when the intended worktree is missing

The shared selected-feature repo-root resolver should continue to:

- return the unique active non-primary feature worktree when it exists
- fail when multiple candidate active feature worktrees exist

But it should stop silently returning the current root when the selected feature is active and no unique feature worktree can be found. Later-task execution and autonomous continuation should treat that as a workflow error requiring operator repair, not as permission to reuse a stale primary checkout.

This stricter behavior applies only to selected-feature continuation paths. It does not change the repo-wide planning audit model.

### Decision: `complete-task` guidance follows the canonical continuation model without letting the skill start work implicitly

The `complete-task` skill should remain terminal for the active task in the sense that it does not itself launch `start-task` or mutate a downstream task into `in_progress`.

But the operator-facing contract should no longer describe the old status-only handoff model. Instead it should explain that `complete-task` returns a canonical continuation payload that downstream wrappers may use to continue automatically when `requires_human_decision=false`.

This keeps the separation of responsibilities intact while removing the doc-level contradiction that currently freezes the old relay model into contract-doc tests.

## Risks / Trade-offs

- [Structured verdict emission could make handoff notes noisier] -> Keep the canonical lines minimal and scoped only to the review-owning stages.
- [Fail-closed worktree resolution could stop workflows that previously limped forward] -> That is acceptable because the older fallback hid resolver ambiguity and contradicted the intended continuation contract.
- [Updating `complete-task` docs could be misread as letting the skill launch downstream work itself] -> Keep the explicit rule that `complete-task` never starts the next task; only its returned payload may authorize wrappers to continue.

## Validation Strategy

- Add or update tests proving `ready-feature` and `complete-task` guidance explicitly require canonical review-verdict emission.
- Add runtime coverage for structured review-verdict parsing plus at least one downstream use of the emitted verdict state.
- Add negative-path coverage showing selected-feature continuation fails when the intended feature worktree is missing or ambiguous.
- Update contract-doc tests so `complete-task` guidance matches the canonical continuation payload model without allowing the skill itself to start downstream work.

## Context

The repository has already moved execution onto OpenSpec-backed `tasks.md`, but some wording still implies that OpenSpec itself owns task readiness. In reality, this workflow derives readiness from top-level checklist state, `Current Task`, and the optional `Depends On` markdown convention layered on top of OpenSpec task files.

The current gap is both semantic and structural. Semantically, user-facing docs and specs still blur the line between OpenSpec task definition and workflow-derived readiness. Structurally, malformed `tasks.md` files can use nested checklist items such as `1.1` without the parent top-level executable task line, which leaves the workflow with no valid execution unit to select.

## Goals / Non-Goals

**Goals:**
- Make the contract explicit that OpenSpec owns task definitions and checkbox completion state, while the workflow owns readiness and dependency interpretation.
- Define the required top-level executable task structure in workflow-managed `tasks.md` files.
- Surface malformed nested-only task structures through shared validation used by readiness promotion and audit.
- Update workflow docs and user-facing skill language so they describe readiness consistently.
- Document a preferred version/feature-prefixed change naming convention without turning naming into an audit gate.

**Non-Goals:**
- Change the underlying execution model for valid task files.
- Introduce native dependency semantics into OpenSpec.
- Redesign feature-file task tracking beyond the existing `Current Task` field.
- Make linked change naming conventions a blocking workflow validation rule in this change.

## Decisions

### Decision: Keep readiness semantics entirely in the workflow layer
The workflow already interprets `Current Task` and optional `Depends On` blocks outside of native OpenSpec semantics. The cleanest contract is to say that OpenSpec provides task markdown and checkbox state, and the workflow computes readiness from that source material.

Alternative considered:
- Continue calling the result "OpenSpec readiness." Rejected because it misstates ownership and makes future bugs harder to reason about.

### Decision: Require explicit top-level checklist items for executable tasks
Every executable task group in workflow-managed `tasks.md` must have a parent top-level checklist item such as `- [ ] 1 Shared Validation`. Nested items like `1.1` remain implementation detail and cannot stand alone as execution units.

Alternative considered:
- Infer missing top-level tasks from nested `1.1` items. Rejected because inference would hide malformed source artifacts and produce unstable task titles.

### Decision: Enforce structure through shared validation surfaced by audit and readiness promotion
The rule should be enforced once in shared workflow parsing/validation and then surfaced through `ready-feature` and `audit-workflow`. That keeps shaping, readiness promotion, and diagnostics aligned on one structural contract.

Alternative considered:
- Add a `ready-feature`-only check. Rejected because malformed active changes should remain a repository workflow problem, not just a wrapper-local issue.

### Decision: Fix authoring guidance as well as validation
Validation alone is too late. The shaping path should describe and, where possible, generate the required top-level checklist structure so new changes start in a valid form.

Alternative considered:
- Rely on docs updates only. Rejected because the repo already showed that wording alone is not enough to prevent malformed task files.

### Decision: Treat change naming as guidance rather than a gate
The workflow docs can recommend naming linked OpenSpec changes with a version/feature prefix so the relationship is easier to scan, but audit and readiness validation should not fail solely because an existing change name does not match that convention.

Alternative considered:
- Make the naming convention mandatory in audit immediately. Rejected because that would create unrelated workflow failures for existing valid changes and is separable from the readiness contract itself.

## Risks / Trade-offs

- [Stricter validation may fail existing malformed shaped changes] -> Keep the rule narrow, provide clear workflow errors, and repair any affected fixtures or active changes as part of the work.
- [Docs and skill wording updates may become repetitive] -> Centralize on a small set of canonical phrases such as "workflow-derived readiness" and "workflow task dependency convention."
- [Recommended naming guidance may be mistaken for a hard requirement] -> State explicitly in docs and skill text that the convention is preferred but non-gating.
- [Shaping guidance may depend on external OpenSpec scaffolding behavior] -> Keep the repository-side requirement focused on the resulting `tasks.md` structure rather than on undocumented OpenSpec internals.

## Migration Plan

1. Update stable specs to separate OpenSpec checkbox authority from workflow-derived readiness and to require top-level executable task entries.
2. Update shared workflow validation so malformed nested-only task structures fail readiness checks clearly.
3. Update shaping/readiness workflow docs and skill text to use the new wording consistently and to recommend the non-gating change naming convention.
4. Repair affected fixtures and sample task files, then re-run the narrow workflow tests.

## Open Questions

- None.

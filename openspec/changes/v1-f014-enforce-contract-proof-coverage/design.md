## Context

The current workflow already derives task readiness from OpenSpec tasks, dependency rules, and `Current Task`, but implementation-plan handling is intentionally thin. `start-task` and `complete-task` only require that a task plan file exists, which means the strongest human-readable contract often lives in the proposal/design while the executable gate reduces to “a plan file is present.” That reduction is the same failure mode the user described in production: narrow unit tests or helper contracts can become de facto acceptance because the workflow never asks the plan to expose the broader proof surface explicitly.

## Goals / Non-Goals

**Goals:**

- Define a machine-checkable implementation-plan structure for workflow-managed execution tasks.
- Make `start-task` and `complete-task` reject plans that lack explicit contract surface and validation-class coverage.
- Document the same contract earlier in shaping/readiness guidance so proof obligations are authored before execution begins.
- Keep the implementation lightweight and Markdown-native so it fits the current workflow style.

**Non-Goals:**

- Infer semantic correctness of a task plan from source code or design prose with an LLM inside the Python helpers.
- Add a full schema parser for arbitrary Markdown tables or YAML front matter.
- Expand workflow audit into a semantic product-spec validator.

## Decisions

### Decision: validate a small required implementation-plan schema in shared workflow helpers

Implementation-plan validation will live in `skills/_workflow/workflow_state.py` so both `start-task` and `complete-task` use the same parsing rules. The required plan sections will be heading-based and list-based so existing Markdown workflow artifacts remain easy to read and edit.

Alternatives considered:
- Keep validation in each resolver script. Rejected because it would duplicate parsing logic and drift again.
- Require YAML front matter. Rejected because it adds a new authoring style to plans and is brittle in handwritten workflow docs.

### Decision: require explicit validation classes instead of trying to infer proof adequacy

Plans will declare `Required Validation Classes` and `Unit-Only Justification` directly. The helper will enforce that behavioral work names at least one runtime-facing validation class unless the plan explicitly justifies a unit-only exception.

Alternatives considered:
- Infer required validation from file paths or task titles. Rejected because the signal is too weak and would create false confidence.
- Only update prose guidance. Rejected because the user’s reported problem is specifically that prose-only intent drifted under weaker executable tests.

### Decision: keep completion evidence guidance structured in docs, but enforce plan structure first

This feature will harden execution entry and completion preconditions by validating plan structure. Skill docs and workflow reference text will also require evidence to reconcile against those plan obligations, but the code change will stop short of parsing every feature-file evidence line in this pass.

Alternatives considered:
- Parse feature validation logs immediately and block completion on full obligation-by-obligation evidence. Deferred because the existing feature-log format is still free-form and would turn this into a larger migration.

## Risks / Trade-offs

- [Risk] New plan requirements can break existing resolver tests and any in-flight local workflow usage. -> Mitigation: update fixture plan writers in the test suite and keep the required schema compact.
- [Risk] Authors may satisfy the schema mechanically without improving proof quality. -> Mitigation: make the required fields specifically about contract surface, proof obligations, and validation classes, not generic prose sections.
- [Risk] Partial enforcement could create asymmetry between start-time and completion-time gates. -> Mitigation: enforce the same plan validation in both resolvers and align the skill docs around the same structure.

## Migration Plan

1. Add shared implementation-plan parsing and validation helpers.
2. Update resolver scripts to fail when plans do not satisfy the new structure.
3. Update workflow tests and fixture plan writers to produce compliant plans.
4. Update shaping/readiness/start/completion skill docs and workflow reference so future changes author proof obligations consistently.

## Open Questions

- Whether a later feature should promote the structured validation evidence format from guidance into a strict feature-file parser.

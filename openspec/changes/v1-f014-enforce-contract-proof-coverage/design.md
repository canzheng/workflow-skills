## Context

The current workflow already derives task readiness from OpenSpec tasks, dependency rules, and `Current Task`, but implementation-plan handling is intentionally thin. `start-task` and `complete-task` only require that a task plan file exists, which means the strongest human-readable contract often lives in the proposal/design while the executable gate reduces to “a plan file is present.” That reduction is the same failure mode the user described in production: narrow unit tests or helper contracts can become de facto acceptance because the workflow never asks the plan to expose the broader proof surface explicitly.

## Goals / Non-Goals

**Goals:**

- Define a machine-checkable implementation-plan structure for workflow-managed execution tasks.
- Make `start-task` reject anti-surrogate proof plans that reduce behavioral work to narrower local contracts.
- Make `ready-feature` require at least one executable task whose proof plan is aligned to the shaped contract surface.
- Make `complete-task` reconcile proof obligations to categorized evidence instead of treating any passing check as sufficient.
- Document the same contract earlier in shaping/readiness guidance and in the workflow reference so proof obligations and validation taxonomy are authored before execution begins.
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

### Decision: require explicit validation classes and anti-surrogate review signals instead of trying to infer proof adequacy from code alone

Plans will declare `Required Validation Classes` and `Unit-Only Justification` directly. The helper will enforce that behavioral work names at least one runtime-facing validation class unless the plan explicitly justifies a unit-only exception.

Alternatives considered:
- Infer required validation from file paths or task titles. Rejected because the signal is too weak and would create false confidence.
- Only update prose guidance. Rejected because the user’s reported problem is specifically that prose-only intent drifted under weaker executable tests.

### Decision: add categorized evidence reconciliation for completion rather than leaving evidence fully free-form

Completion needs stronger structure than “run/result” prose if it is going to prevent narrower local proof from masquerading as full task acceptance. The workflow will therefore define evidence categories such as helper, schema, runtime_path, persistence, negative_path, and manual_inspection, and `complete-task` guidance will reconcile obligations to those evidence categories.

Alternatives considered:
- Leave evidence reconciliation as prose only. Rejected because that repeats the current failure mode where a weaker local contract can pass as sufficient proof.

### Decision: prefer canonical fixtures and explicit review questions for test-contract drift

The workflow cannot rely only on resolver logic; it also has to keep the tests from redefining the contract. The design therefore includes a mandatory review question for test changes and a preference for canonical end-to-end fixtures when execution-path behavior is being asserted.

Alternatives considered:
- Trust engineers to spot test narrowing during review. Rejected because the reported failure mode shows that this is not reliable enough.
- Replace all local fixtures with only large end-to-end suites. Rejected because narrow fixtures are still useful; the rule is to avoid them becoming the only contract proof for execution behavior.

## Risks / Trade-offs

- [Risk] New plan requirements can break existing resolver tests and any in-flight local workflow usage. -> Mitigation: update fixture plan writers in the test suite and keep the required schema compact.
- [Risk] Authors may satisfy the schema mechanically without improving proof quality. -> Mitigation: make the required fields specifically about contract surface, anti-surrogate proof risks, proof obligations, validation taxonomy, and evidence categories, not generic prose sections.
- [Risk] Evidence reconciliation will require updates to feature-file guidance and possibly template wording. -> Mitigation: treat the feature template and workflow reference as part of the same change rather than a follow-on cleanup.
- [Risk] Anti-surrogate checks can become too heuristic or brittle. -> Mitigation: keep the executable checks narrow, explicit, and task-plan-driven, and use review questions for the more semantic cases that code should not guess.

## Migration Plan

1. Add shared implementation-plan parsing and validation helpers.
2. Update `start-task` to reject anti-surrogate proof plans for execution work.
3. Update `ready-feature` guidance and supporting docs so execution-ready tasks require proof planning aligned to shaped contract surfaces.
4. Update `complete-task`, the feature template, and evidence guidance to reconcile categorized evidence to declared proof obligations.
5. Update workflow tests, fixture strategy, and review guidance so test changes are checked for contract narrowing.
6. Update workflow reference and skill docs to define the validation taxonomy and when each validation class is required.

## Open Questions

- Whether the first pass of evidence reconciliation should be guidance-plus-spot-check validation or a strict parser for every feature-file evidence block.

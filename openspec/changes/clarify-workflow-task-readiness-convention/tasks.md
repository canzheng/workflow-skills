## 1. Contract and Docs Clarification

- [ ] 1 Clarify workflow-owned readiness contract
  - [ ] 1.1 Update stable specs and repository docs to state that OpenSpec owns task definitions and checkbox completion state while workflow readiness is derived by repository rules
  - [ ] 1.2 Update workflow skill text and user-facing messages to use precise terms such as `workflow-derived readiness` and `workflow task dependency convention`
  - [ ] 1.3 Document the preferred version/feature-prefixed linked change naming convention while keeping it non-gating for audit and readiness checks

## 2. Top-Level Task Structure Enforcement

- [ ] 2 Enforce top-level executable task structure
  - [ ] 2.1 Add shared validation that rejects linked `tasks.md` files that use nested checklist items without the required parent top-level executable task entry
  - [ ] 2.2 Surface that validation through `audit-workflow`, `ready-feature`, and the shaping path so malformed task structure is blocked before execution

## 3. Coverage and Fixture Repair

- [ ] 3 Add coverage and repair malformed task fixtures
  - [ ] 3.1 Update affected fixtures and sample change/task files to include required top-level checklist items where appropriate
  - [ ] 3.2 Add regression coverage for both malformed nested-only task structures and valid workflow-compatible parent-task structures

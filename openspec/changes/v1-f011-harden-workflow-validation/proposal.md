## Why

The review identified two workflow-validation gaps that should be fixed at the contract and implementation level: `diagnose-workflow` can fail with a traceback instead of structured findings, and the workflow currently does not require the baseline `openspec-propose` artifacts to still exist once a feature is in `[SHAPING]`. The audit spec is also still ambiguous about how completed post-adoption features should resolve their linked change state.

## What Changes

- Make `diagnose-workflow` return structured findings when planning scaffold is missing instead of terminating with an uncaught exception.
- Require `[SHAPING]` features to retain `proposal.md`, `design.md`, and `tasks.md` under the linked OpenSpec change.
- Keep the stronger `[READY]` gate unchanged: valid `OpenSpec Specs` metadata, honest top-level task structure, and at least one workflow-ready task.
- Tighten the stable audit contract so completed non-legacy features are validated against archived change state rather than ambiguous "linked change directory exists" wording.
- Add focused regression coverage for diagnosis fallback and shaping-artifact enforcement.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `workflow-audit-and-repair`: Diagnosis and audit requirements will cover missing planning scaffold handling, shaping-artifact baseline enforcement, and archived change expectations for completed features.
- `openspec-change-integration`: Shaping will explicitly require the authored baseline OpenSpec artifacts produced by `openspec-propose`.

## Impact

- Affected skills: `skills/audit-workflow/`, `skills/diagnose-workflow/`, `skills/shape-backlog-item/`
- Affected helpers/tests: `skills/_workflow/`, `skills/_workflow/tests/`, `tests/`
- Affected stable specs: `openspec/specs/workflow-audit-and-repair/spec.md`, `openspec/specs/openspec-change-integration/spec.md`

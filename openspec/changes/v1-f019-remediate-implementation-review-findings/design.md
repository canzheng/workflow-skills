## Context

Eleven issues surfaced in a focused review of the implementation on `main`. None are individually critical; the cost of fixing them together is lower than letting them accumulate. The findings group cleanly into three remediation axes:

- **Duplication and drift in script entry points.** All nine skill scripts redefine `WorkflowError`, `repo_root()`, and (in four of them) `read_backlog()`. Two of the three regex constants in `audit_workflow.py` shadow names already exported by `_workflow.workflow_state`. `_list_git_worktree_roots` in `start-task` diverges from its public twin on the failure contract (`[]` vs `[root.resolve()]`). The `SKILLS_ROOT = Path(__file__).resolve().parents[2]` idiom relies on every script living at exactly two directory levels below `skills/`; any future reorganization breaks it silently.
- **Contract drift in operator-facing docs.** `shape-backlog-item/SKILL.md:30` and `ready-feature/SKILL.md:26` describe the stage-level `Retrieved Lesson IDs` line as "task-scoped," while the authoritative `WORKFLOW_REFERENCE.md:85` names it "stage-scoped." A single `parse_feature_id` branch in `workflow_state.py:1225` is unreachable (guarded by a condition that cannot be false at that point). `complete-task/SKILL.md:13` refers to the `completion_handoff` payload without listing its fields.
- **Test-suite ergonomics.** One file (`tests/test_workflow_openspec_integration.py`) is ~128 subprocess-heavy tests and eats ~70% of the ~100s full-suite runtime. There is no shared `conftest.py`; repo-scaffold helpers are reimplemented across test files.

## Goals / Non-Goals

**Goals**

- Land a shared CLI preamble module and migrate every skill script to import from it. One definition of `WorkflowError`, `repo_root()`, `read_backlog()`, and an anchor-based repo/skills-root resolver.
- Bring the two stage-side SKILL.md files into terminology agreement with `WORKFLOW_REFERENCE.md`.
- Cut the integration-test runtime materially by converting a representative subset of subprocess-driven tests to direct Python-entry calls, and introduce a shared `conftest.py` that both test roots can consume.
- Fix the narrow code quality defects — dead branch, duplicate regexes, divergent worktree-root helper — without expanding scope.
- Update the two affected stable specs (`repo-development-tooling`, `feature-execution-tracking`) so this discipline is contract, not convention.

**Non-Goals**

- Redesigning any skill's external contract, script CLI surface beyond normalizing the `--feature-id` treatment, or the OpenSpec workflow lifecycle.
- Touching archived feature files, archived OpenSpec changes, or `docs/superpowers/**`.
- Rewriting the full `tests/test_workflow_openspec_integration.py` file into a new layout — only migrate the tests that are clean wins.
- Backfilling unrelated tests or adding lifecycle stages.

## Decisions

### Decision: Extract a single `cli_helpers` module rather than per-script mixins or class inheritance

Introduce `skills/_workflow/cli_helpers.py` exporting:

- `class WorkflowError(RuntimeError)` — the single canonical error type for script-level failures
- `def repo_root(explicit_root: str | None = None) -> Path` — the current logic, unchanged in behavior, lifted from the nine copies
- `def read_backlog(root: Path)` — lifted from the current four-way duplication (signatures converge on whatever the existing callers already consume)
- `def resolve_skills_root() -> Path` — anchor-based resolver that searches upward from `__file__` for the `_workflow/` sibling, replacing the fragile `parents[2]` pattern

Each script keeps its own `parse_args`, `main`, and resolver logic — only the cross-cutting preamble is shared. This keeps the per-skill CLI surface explicit and avoids forcing a `BaseCommand` abstraction that would over-couple unrelated scripts.

### Decision: Preserve behavior during migration; refactor-only commits

Every helper extraction is behavior-preserving. If a script's current `read_backlog` signature differs from a sibling's, the shared helper exposes the superset and each caller adapts. No script gains or loses a CLI flag during Task 1. Contract changes (e.g., `--feature-id` normalization) happen in Task 2 so they can be reviewed separately from the refactor.

### Decision: "stage-scoped" applies only to stage-level skills

`shape-backlog-item` and `ready-feature` write the lesson line once per stage (one shaping gate, one readiness gate). `start-task` and `complete-task` write it once per top-level task. The stable spec already names the stage-level case "stage-scoped"; the task-level case stays "task-scoped." This change affects only the two stage-side SKILL.md files plus the `test_workflow_contract_docs.py` assertions that pin the wording.

### Decision: Migrate subprocess tests to direct-call on a per-test risk basis, not wholesale

The integration test file mixes genuine end-to-end scenarios (those that exercise `git worktree`, `openspec init`, or subprocess argv propagation) with tests that could be rewritten to call the resolver Python entry point directly and assert on return values. Task 3 converts only the direct-call-appropriate subset and documents the keep/convert criterion in a short module docstring. Full-suite runtime is the success metric; a ≥30% reduction is the target.

### Decision: No retroactive changes to archived evidence or historical features

All changes apply to the currently-shipped main-checkout implementation and the stable specs. Feature files under `docs/planning/versions/v1/features/` remain frozen evidence even if they contain outdated phrasing; that is the convention of this workflow.

## Risks / Trade-offs

- **Cross-script refactor risk.** Touching all nine scripts in one task has blast radius. Mitigated by: behavior-preserving migration, exhaustive test coverage of each script's existing contract, and a full-suite pass before handoff.
- **Test-migration risk.** Converting subprocess tests to direct-call can over-couple tests to internal function signatures. Mitigated by the keep/convert criterion: any test that asserts on subprocess argv, exit codes, or stdout byte-formatting stays as subprocess; only tests that assert on logical outcomes convert.
- **Terminology churn.** Flipping "task-scoped" → "stage-scoped" in the two SKILL.md files forces an update to the contract-doc assertions. The `test_workflow_contract_docs.py` file already uses `assertIn` on these exact strings; the churn is narrow and the test failure will be actionable.

## Migration Plan

1. Task 1 lands the shared module + script migration + the three code-quality fixes (#1, #2, #4, #5, #10). All existing tests must continue to pass with no assertion changes.
2. Task 2 lands the docs/contract alignment (#3, #8, #9, #11) plus the matching test adjustments in `test_workflow_contract_docs.py`. Spec delta for `feature-execution-tracking` lands here.
3. Task 3 lands the test ergonomics improvements (#6, #7) — shared `conftest.py`, migration of the direct-call-appropriate subset, and runtime-budget documentation. Spec delta for `repo-development-tooling` lands here (integration-test runtime justification).

Each task can close independently. No ordering hazard beyond the per-task scope.

## Open Questions

- Should `cli_helpers.read_backlog` return the exact tuple shape that each current caller consumes, or should callers migrate to a single canonical return type? The per-caller inspection happens at Task 1 start; default is the superset shape with explicit per-caller destructuring.
- How aggressive should the Task 3 runtime target be? ≥30% is the baseline; stop there rather than chasing lower numbers if it forces fragile mocks.

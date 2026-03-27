## Context

The repo's current workflow state is clean enough to pass the existing gates, but the review found several places where the documented contract is stricter than the implemented enforcement. The highest-risk gaps are structural false negatives:
- audit currently allows missing promoted-feature `OpenSpec Specs` metadata
- audit allows extra backlog sections appended after `[DEFER]`
- diagnosis can still report malformed repositories as healthy when those conditions exist

The review also found source-of-truth drift in tracked docs and planning artifacts:
- `finish-feature` wording differs between workflow docs and stable workflow specs
- `VERSION_SCOPE.md` still contains placeholders even though all tracked v1 work is in `[DONE]`
- `openspec-change-integration/spec.md` still contains archive-placeholder purpose text
- historical feature records include notes that conflict with the accepted workflow contract

## Goals / Non-Goals

**Goals:**
- Make audit enforce the structural workflow rules the specs already claim.
- Make diagnosis report those same structural issues without becoming a hard gate.
- Keep audit and diagnosis aligned by reusing shared validation logic where practical.
- Repair the repo's own workflow docs and planning artifacts so they match the accepted workflow contract.
- Define explicit validation coverage so every review finding has a named proof path.

**Non-Goals:**
- Redesign the overall workflow lifecycle.
- Add new workflow phases or new orchestration actions.
- Change feature-execution semantics beyond documentation/source-of-truth repair.

## Decisions

### Decision: Centralize the missing structural checks in shared workflow helpers
The missing checks should live in `skills/_workflow/` rather than being duplicated across audit and diagnosis. That keeps the hard gate and the read-only report aligned and reduces the risk that one tool silently drifts from the other again.

### Decision: Diagnose should surface the same structural defects as findings, not silently downgrade them
`diagnose-workflow` remains read-only and advisory, but it should still report malformed canonical sections and missing promoted-feature spec links as structured findings. The difference from audit is exit behavior, not whether the issue is visible.

### Decision: Treat source-of-truth cleanup as part of the same change
The review findings are not only implementation gaps; several tracked docs and planning artifacts are themselves inconsistent with the workflow contract. This change should repair those artifacts in the same pass so the repo stops teaching contradictory behavior.

### Decision: Make finding coverage explicit in both tasks and validation
The change should not rely on an implied "cleanup everything" task. Each review finding should map to a concrete task or subtask, and the validation plan should state how that finding will be proven resolved.

## Validation Strategy

- For audit false negatives:
  - add fixture coverage for missing promoted-feature `OpenSpec Specs`
  - add fixture coverage for extra backlog sections after `[DEFER]`
- For diagnosis false healthy states:
  - add fixture coverage that malformed backlog structure produces findings
  - add fixture coverage that missing promoted-feature `OpenSpec Specs` produces findings
- For source-of-truth cleanup findings:
  - use targeted file inspections and git-visible diffs to prove the affected tracked docs/artifacts were repaired
  - record explicit validation steps that map each repaired artifact back to the original review finding

## Risks / Trade-offs

- [Shared validation becomes broader] -> Keep the new helper scope limited to structural checks that both tools already conceptually own.
- [Historical feature evidence may need careful wording updates] -> Preserve factual history while removing claims that contradict the live workflow contract.
- [Audit will start failing on states that currently pass] -> That is intentional, but add focused fixture coverage so the stricter gate is explicit and stable.
- [Validation scope sprawls across docs and tests] -> Keep a direct finding-to-validation mapping so the final evidence stays reviewable rather than ad hoc.

## Migration Plan

1. Add shared structural validation for canonical board sections and promoted-feature spec links.
2. Wire audit to fail on those conditions and diagnosis to report them.
3. Add focused regression tests for the current false-negative cases.
4. Repair the repo's workflow docs and planning/spec artifacts to match the accepted contract.
5. Record explicit validation steps that prove all review findings are covered.

## Open Questions

- None.

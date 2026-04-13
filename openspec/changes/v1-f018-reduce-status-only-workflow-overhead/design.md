## Context

The workflow already separates shaping, readiness, execution, completion, and finish for good reasons, but the current implementation turns many of those boundaries into explicit status relay turns. Benchmark evidence shows the main cost is not failed work. It is repeated administrative coordination:

- last-task completion stops at "finish-feature is startable"
- review outcomes come back as notification text instead of deterministic state
- active-feature continuation can stop because unrelated sibling features are malformed
- autonomous execution still pays agent-lifecycle overhead for relay-only transitions

The requested scope is intentionally narrower than a lifecycle redesign. The workflow should keep its existing gates, but make the common transitions deterministic enough that humans and autonomous execution do not need to re-state the same status boundary as a separate turn.

## Goals / Non-Goals

**Goals:**
- Remove status-only relay turns when the next workflow action is already determined.
- Keep review and archive gates intact while making their outcomes machine-readable.
- Scope execution-time blocking checks to the selected feature/worktree instead of unrelated active work.
- Ensure `autonomous-backlog-loop` participates in the same reduced-overhead path rather than being stranded by the old relay boundary.
- Reduce avoidable subagent lifecycle churn for feature-local continuation.

**Non-Goals:**
- Add new lifecycle sections such as `[BLOCKED]`.
- Collapse shaping, readiness, execution, and finish into one generic command.
- Remove audit, verification, review, or archive gates.
- Change OpenSpec task semantics beyond the workflow wrapper behavior.

## Decisions

### Decision: Add deterministic continuation without inventing a new lifecycle phase

`complete-task` should continue to return a structured handoff payload, but that payload should be actionable enough for callers to continue immediately when no unresolved decision remains. The key behavior change is that the workflow may coalesce status-only transitions:

- non-final task completion may flow directly into the next ready task
- final task completion may flow directly into `finish-feature`
- callers may still choose to stop after the payload is produced, but they should not be forced into a separate relay turn just to restate the next deterministic step

Rationale:
- This preserves the same gates while cutting the admin-only baton pass.
- It gives `autonomous-backlog-loop` and future wrappers a stable machine interface instead of prose-only handoff notes.

### Decision: Store review outcomes as structured verdict state

Readiness review and execution/closure review should stop relying on free-form "approved / not approved / issues found" summaries as their only durable output. The workflow should add a minimal structured verdict model that can be persisted in the feature file and resolver payloads, with fields such as:

- review scope
- target task or feature boundary
- verdict state such as `approved`, `changes_requested`, or `blocked`
- blocking finding count or identifiers
- whether the verdict is terminal for the current boundary

Rationale:
- This preserves the existing human-readable notes while giving automation deterministic state.
- It reduces the need for notification turns whose only content is relaying a verdict.

### Decision: Execution resolvers should block on selected-feature integrity, not unrelated active drift

Once the workflow is continuing an already-selected feature, resolvers should treat that feature/worktree as the primary blocking scope. Unrelated malformed active features should be surfaced as diagnostics, but should not block continuation of the selected feature unless the direct audit gate is being invoked for repo-wide repair or planning-state edits.

Rationale:
- This keeps execution moving on valid selected work.
- It reduces administrative repair turns caused by sibling feature drift.
- It still preserves a global audit path for deterministic repo-wide repair.

### Decision: Autonomous continuation stays inside one feature-scoped agent

`autonomous-backlog-loop` should consume the deterministic continuation payload and keep status-only progression within the same feature-scoped agent whenever the next step is already determined. It should not require a new outer-step relay or extra agent lifecycle just to say "continue to the next task" or "run finish-feature now."

Rationale:
- This directly addresses the benchmark finding that many status-only turns are tied to agent lifecycle.
- It complements the continuation contract instead of fighting it.
- It keeps human intervention reserved for actual decisions or failures.

## Risks / Trade-offs

- [Atomic continuation could hide meaningful decision boundaries] -> Only allow coalescing when the next action is fully determined and no review/archive gate remains unresolved.
- [Structured verdicts could bloat feature files] -> Keep the schema minimal and stage-scoped, and continue using notes for rich context.
- [Feature-scoped continuation could let unrelated drift linger] -> Surface unrelated drift as diagnostics and keep direct `audit-workflow` as the repo-wide gate.
- [Autonomous loop reuse could make failures harder to inspect] -> Preserve explicit payload logging for each continued step inside the feature-scoped agent.

## Validation Strategy

- Add integration coverage for final-task completion producing a continuation payload that can immediately route to `finish-feature`.
- Add integration coverage for non-final task completion producing a deterministic next-task continuation payload.
- Add contract and parser coverage for structured review verdict state in feature files and workflow payloads.
- Add resolver coverage proving that selected-feature continuation is not blocked by unrelated malformed active work, while direct `audit-workflow` still reports that drift.
- Add autonomous-loop coverage proving that relay-only continuation stays inside the same feature-scoped agent path and includes `finish-feature` in the change surface.

## Open Questions

- The continuation contract should expose enough state for wrappers to decide whether to auto-continue. The main remaining design choice is whether that should be a single `next_workflow_action` enum or a slightly richer object with explicit `action`, `target_feature_id`, `target_task_id`, and `reason` fields. Implementation can finalize that detail as long as the result is deterministic and testable.

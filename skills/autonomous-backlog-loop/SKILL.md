---
name: autonomous-backlog-loop
description: Use when the repository should keep advancing eligible backlog work across READY, SHAPING, and BACKLOG states, with the main agent directly orchestrating each step
---

# Autonomous Backlog Loop

## Overview

Advance the active version backlog by repeatedly resolving one next workflow action and executing that action directly from the main agent.

Use the installed workflow skills as the source of truth for state transitions. This skill only orchestrates selection, sequencing, and stop conditions.

The main agent owns orchestration and invokes each wrapped workflow skill (`shape-backlog-item`, `ready-feature`, `start-task`, `complete-task`, `finish-feature`) directly. Do not delegate the outer loop or the per-feature task loop to a sub-agent. Several wrapped skills (notably `start-task` and `ready-feature`) themselves require spawning lightweight reviewer sub-agents, and in Claude Code a sub-agent cannot spawn further sub-agents. Running the orchestration from the main agent is what keeps those required review and verification gates honest.

Sub-agents may still be spawned from the main agent for scoped jobs that the wrapped skills define, for example the lightweight independent reviewer required by `start-task` and `ready-feature`. They are not used to wrap the backlog loop itself.

## Inputs

- Optional `number of backlog items`
  - Count completed features, not original backlog bullets.
  - If one backlog item splits into multiple features, each resulting feature counts separately.
  - Count a feature only when it reaches `DONE` or `DEFER`.
- Optional `--solo`
  - In solo mode, the main agent may auto-accept a wrapped skill's recommendation without pausing for user confirmation, unless it conflicts with direct user instructions.
  - If `--solo` is omitted, infer solo mode only when the user request clearly asks for unattended execution, no confirmation prompts, or equivalent "decide for me and keep going" behavior. Do not infer solo mode from the word "autonomous" alone.
  - Examples of cues that may justify inferred solo mode: "run unattended", "don't ask me", "keep going and decide for me", "no confirmation prompts".
  - Otherwise default to interactive mode and surface design choices back to the user.

## Run Log

Create one human-readable run log per autonomous-loop invocation at `<repo_root>/.local/autonomous-backlog-loop/<timestamp>-<run-id>.md`.

- Create the directory if it does not exist.
- Keep the file local-only. Do not add it to git.
- Reuse the same file for the full outer loop run, across every wrapped skill invocation.
- Start the file with run metadata: run id, started-at timestamp, scope, and completion limit if one was given.
- Finalize the file with ended-at timestamp and stop reason.
- If the run encounters no design choices, say so explicitly before finishing.

Whenever any wrapped skill or reviewer sub-agent presents a design choice, append an entry that captures:

- timestamp
- phase: `shape_backlog_item`, `ready_feature`, or `task_loop`
- feature id and task id if known
- source agent or workflow step
- the choice that was presented
- the recommendation that was offered, if any
- the resulting decision: `recommendation accepted`, `recommendation rejected`, `deferred due to user instruction conflict`, or `no clear recommendation`
- the basis for that decision
- succinct but informative context so the record is understandable later

## Resolver

Run `audit-workflow`, then resolve the next action:

```bash
python "${AGENTS_HOME:-$HOME/.agents}/skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py"
```

Optional resolver flags:

- `--completed-count <n>`
- `--completion-limit <n>`
- `--design-mode` to run only design-stage work from `[SHAPING]` and `[BACKLOG]`; it does not act on active execution work in `[READY]` or `[IN_PROGRESS]`, and the resolver still sanity-checks `[READY]` and `[IN_PROGRESS]` features for invalid workflow state before continuing
- `--feature-id <feature-id>` for continuing a selected feature's task loop

When `--feature-id` is used for a feature already in execution, first resolve the effective repo root for that feature and prefer the reusable feature worktree over a stale primary checkout. Run both `audit-workflow` and the resolver from that selected root.

Resolver precedence:

1. first `[IN_PROGRESS]` feature with a `ready` task
2. otherwise first `[READY]` feature with a `ready` task
3. otherwise first `[SHAPING]` feature
4. otherwise first `[BACKLOG]` item
5. otherwise stop

Blocked-only features are skipped. They do not prevent termination.

Design-mode precedence:

1. first `[SHAPING]` feature
2. otherwise first `[BACKLOG]` item
3. otherwise return `feature_exhausted`

Use design mode when the user request is clearly design-only, explicitly asks to avoid acting on active execution work, or asks to exhaust only shaping/backlog design work. Pass `--design-mode` explicitly in those cases. Design mode still sanity-checks `[READY]` and `[IN_PROGRESS]` features for invalid workflow state before it selects design work.

## Workflow

The main agent performs every step below. Do not wrap the outer selection loop or the per-feature task loop in a sub-agent; wrapped skills that require reviewer sub-agents must be invoked from the main agent so those reviewers can be spawned.

1. Create the run log file for this autonomous-loop invocation.
2. Run `audit-workflow`.
3. Decide whether the run is in normal mode or design mode from the user request.
4. Decide whether recommendation handling is `solo` or `interactive`, using explicit `--solo` first, then clear user-request inference, else interactive by default. Keep the selected mode in effect across every wrapped skill invocation in this run.
5. Run the resolver without `--feature-id`, adding `--design-mode` whenever the request is clearly design-only or explicitly asks to avoid acting on active execution work.
6. Dispatch on the resolver result:
   - `run_task_loop` → enter the feature loop (step 7) for that feature.
   - `ready_feature` → invoke `ready-feature` directly on the selected feature, then return to step 2.
   - `shape_backlog_item` → invoke `shape-backlog-item` directly on the selected first backlog item, then return to step 2.
   - `stop` or `feature_exhausted` → go to step 10 and terminate under the stop conditions.
7. Feature loop (runs in the main agent, never in a sub-agent):
   - before each feature-scoped `audit-workflow` or resolver call, revalidate the effective repo root for `<feature-id>` and prefer the existing feature worktree whenever it exists
   - if the active feature worktree no longer exists, stop with a workflow error instead of silently falling back to the primary checkout
   - run feature-scoped `audit-workflow` from that selected repo root
   - run the resolver with `--feature-id <feature-id>` from that same repo root
   - if the resolver returns `feature_exhausted`, exit the feature loop and return to step 2
   - otherwise:
     - invoke `start-task` for the named feature/task so execution stays on the selected feature and feature worktree. Pass the resolver-provided `feature_id` and `task_id` to `start-task`'s resolver script via `--feature-id` and `--task-id` so it takes the explicit-ID fast path and skips redundant BACKLOG and worktree scanning. `start-task` will spawn its required independent reviewer sub-agent from the main agent; do not bypass or reimplement that review
     - if the task finishes cleanly, invoke `complete-task`. Pass the same `feature_id` and `task_id` to `complete-task`'s resolver script via `--feature-id` and `--task-id` for the same fast path
     - complete `complete-task` before resolving or starting any downstream top-level task
     - after `complete-task`, confirm `git status --short` is clean from the selected feature worktree before continuing the feature loop
     - read the canonical `completion_handoff` payload returned by `complete-task`
     - if `completion_handoff.requires_human_decision` is `true`, exit the feature loop and return control instead of inferring the next step
     - if `completion_handoff.action` is `finish_feature`, invoke `finish-feature` before any downstream cleanup
     - do not bypass any review or verification gates owned by the wrapped execution skill, `complete-task`, or `finish-feature`
     - if `finish-feature` moves the feature to `[DONE]`, perform the default finishing behavior
     - if `finish-feature` completes successfully, exit the feature loop and return to step 2
     - if `completion_handoff.action` is `start_task`, continue the feature loop on the same feature branch/worktree
     - if `completion_handoff.action` is `stop`, exit the feature loop and return control
     - if the task ends `blocked` or `cancelled`, leave the feature branch/worktree in place and the feature in `[IN_PROGRESS]`, then exit the feature loop and return to step 2 so the outer resolver can pick the next eligible feature
8. When a wrapped skill or its reviewer sub-agent raises a design choice:
   - in `solo` mode, auto-accept the recommendation only if one was offered and it does not conflict with direct user instructions already given
   - in `interactive` mode, pause and surface the choice to the user with concise context, the recommendation if any, and the concrete options that need a decision
   - in `interactive` mode, wait for the user's answer before proceeding
   - after the decision, append the choice, recommendation, resulting decision, and basis to the shared run log immediately
9. After each completed step, re-run `audit-workflow` and resolve again. If the next step continues the same active feature, resolve the effective repo root again first and keep the audit/resolver pair on that feature worktree rather than the primary checkout.
10. Stop when the resolver returns:
    - `stop` with `reason == completion_limit_reached`
    - `stop` with `reason == no_eligible_work`
    - `feature_exhausted` in design mode because no `[SHAPING]` or `[BACKLOG]` work remains
11. Before returning, finalize the run log and include its path in the final report.

## Rules

- Do not pause, ask the user to confirm continuation, or hand back control between successful steps. Continue running until one of the Stop Conditions fires, you need to surface a design choice, or encountered a real blocker prevents progress.
- The main agent drives every outer step directly. Do not wrap the outer loop or the feature loop in a sub-agent.
- Never begin a new outer step before the current step's wrapped skill has returned.
- Keep the active feature's task loop on a single feature branch/worktree, and never switch branches while a task is `in_progress`. Multiple features may live in `[IN_PROGRESS]` simultaneously; when the active feature has no executable task (its task ended `blocked` or `cancelled`, or the resolver returned `feature_exhausted`), return to the outer resolver to pick the next eligible feature. The global "at most one `in_progress` task" invariant still holds.
- Reuse one feature branch/worktree across the sequential tasks of the same feature.
- Respect review and verification gates inherited from wrapped skills instead of short-circuiting them in the loop controller. In particular, let `start-task` and `ready-feature` spawn their required reviewer sub-agents from the main agent.
- Do not duplicate branch-finalization behavior owned by `finish-feature`.
- Do not auto-defer blocked work.

## Stop Conditions

- `audit-workflow` fails
- the resolver reports an existing `in_progress` task
- the resolver reports a feature with `Current Task` set but no active in-progress task backing it
- the resolver reports `completion_limit_reached`
- the resolver reports `no_eligible_work`
- the resolver reports `feature_exhausted` in design mode because only non-design work remains
- the selected feature or task no longer exists in the active backlog state

---
name: autonomous-backlog-loop
description: Use when the repository should keep advancing eligible backlog work across READY, SHAPING, and BACKLOG states with sequential sub-agents
---

# Autonomous Backlog Loop

## Overview

Advance the active version backlog by repeatedly resolving one next workflow action and delegating that action through fresh feature-scoped sub-agents.

Use the installed workflow skills as the source of truth for state transitions. This skill only orchestrates selection, sequencing, and stop conditions.

## Inputs

- Optional `number of backlog items`
  - Count completed features, not original backlog bullets.
  - If one backlog item splits into multiple features, each resulting feature counts separately.
  - Count a feature only when it reaches `DONE` or `DEFER`.
- Optional `--solo`
  - In solo mode, the loop may auto-accept a feature-scoped sub-agent's recommendation without pausing for user confirmation, unless it conflicts with direct user instructions.
  - If `--solo` is omitted, infer solo mode only when the user request clearly asks for unattended execution, no confirmation prompts, or equivalent "decide for me and keep going" behavior.
  - Otherwise default to interactive mode and surface design choices back to the user.

## Run Log

Create one human-readable run log per autonomous-loop invocation at `<repo_root>/.local/autonomous-backlog-loop/<timestamp>-<run-id>.md`.

- Create the directory if it does not exist.
- Keep the file local-only. Do not add it to git.
- Reuse the same file for the full outer loop run, including any spawned backlog-process sub-agents.
- Start the file with run metadata: run id, started-at timestamp, scope, and completion limit if one was given.
- Finalize the file with ended-at timestamp and stop reason.
- If the run encounters no design choices, say so explicitly before finishing.

Whenever any spawned agent presents a design choice, append an entry that captures:

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
python "${CODEX_HOME:-$HOME/.codex}/skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py"
```

Optional resolver flags:

- `--completed-count <n>`
- `--completion-limit <n>`
- `--design-mode` to run only design-stage work from `[SHAPING]` and `[BACKLOG]`
- `--feature-id <feature-id>` for continuing a selected feature's task loop

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

Use design mode when the user request is clearly design-only, explicitly says to ignore `[READY]` work, or asks to exhaust only shaping/backlog design work. Pass `--design-mode` explicitly in those cases.

## Recommendation Mode

Decide recommendation handling once near the start of the run and keep it consistent for the full outer loop invocation.

- `solo` mode:
  - enabled explicitly by `--solo`
  - or inferred only when the user's request clearly authorizes unattended execution without confirmation prompts
- `interactive` mode:
  - the default when `--solo` is absent and the request does not clearly authorize unattended execution

Examples of cues that may justify inferred solo mode:

- "run unattended"
- "don't ask me"
- "keep going and decide for me"
- "no confirmation prompts"

Do not infer solo mode from the word "autonomous" alone. When the user asks to run the loop but does not clearly authorize unattended design decisions, default to interactive mode.

## Workflow

1. Create the run log file for this autonomous-loop invocation.
2. Run `audit-workflow`.
3. Decide whether the run is in normal mode or design mode from the user request.
4. Decide whether recommendation handling is `solo` or `interactive`, using explicit `--solo` first, then clear user-request inference, else interactive by default.
5. Pass the selected recommendation-handling mode into every spawned backlog-process sub-agent instruction.
6. Run the resolver without `--feature-id`, adding `--design-mode` whenever the request is clearly design-only or explicitly excludes `[READY]` work.
7. If the resolver returns `run_task_loop`, spawn one backlog-process sub-agent for that feature.
8. The backlog-process sub-agent owns only that one feature and must not start another feature.
9. Inside that backlog-process agent, loop:
   - run the resolver with `--feature-id <feature-id>`
   - if the resolver returns `feature_exhausted`, stop the feature loop and return control
   - otherwise, inside the same backlog-process sub-agent:
     - call `start-task` for the named feature/task so execution stays on the selected feature and feature worktree
     - if the task finishes cleanly, call `complete-task`
     - if the feature reaches `DONE`, perform the default finishing behavior equivalent to local merge plus branch/worktree cleanup, then stop the feature loop and return control
     - if the feature remains `IN_PROGRESS`, continue the feature loop on the same feature branch/worktree
     - if the task ends `blocked` or `cancelled`, leave the feature branch/worktree in place, then stop the feature loop and return control
10. When a feature-scoped sub-agent raises a design choice:
   - in `solo` mode, auto-accept the recommendation only if one was offered and it does not conflict with direct user instructions already given
   - in `interactive` mode, pause and surface the choice to the user with concise context, the recommendation if any, and the concrete options that need a decision
   - in `interactive` mode, wait for the user's answer before proceeding
   - after the decision, append the choice, recommendation, resulting decision, and basis to the shared run log immediately
11. Wait for the backlog-process sub-agent to finish before starting the next outer step.
12. If the resolver returns `ready_feature`, spawn one backlog-process sub-agent that runs `ready-feature` on the selected feature, then return.
13. If the resolver returns `shape_backlog_item`, spawn one backlog-process sub-agent that runs `shape-backlog-item` on the selected first backlog item, then return.
14. After each completed step agent, re-run `audit-workflow` and resolve again.
15. Stop when the resolver returns:
   - `stop` with `reason == completion_limit_reached`
   - `stop` with `reason == no_eligible_work`
   - `feature_exhausted` in design mode because no `[SHAPING]` or `[BACKLOG]` work remains
16. Before returning, finalize the run log and include its path in the final report.

## Rules

- Always use one fresh backlog-process sub-agent per outer step.
- Never start a new step before the previous step agent finishes.
- Let the selected feature's backlog-process sub-agent own all sequential tasks for that feature.
- Reuse one feature branch/worktree across the sequential tasks of the same feature.
- Do not auto-defer blocked work.
- Pass the run-log path into every spawned backlog-process sub-agent and require it to append to the same file.
- Record every design choice presented during autonomous execution, not only the ones whose recommendations are accepted.
- Auto-accept recommendations only in `solo` mode, and only when they do not conflict with direct user instructions already given.
- In `interactive` mode, do not auto-accept recommendations. Surface the choice to the user and wait for their decision.
- When a recommendation is accepted, rejected, deferred, or absent, record that outcome in the run log immediately with the recommendation and context that led to the decision.
- Keep branch cleanup non-interactive only when the feature reaches `DONE`: local merge plus branch/worktree cleanup is the default policy.
- Keep using the installed workflow skills instead of re-implementing their state transitions here.

## Stop Conditions

- `audit-workflow` fails
- the resolver reports an existing `in_progress` task
- the resolver reports `completion_limit_reached`
- the resolver reports `no_eligible_work`
- the resolver reports `feature_exhausted` in design mode because only non-design work remains
- the selected feature or task no longer exists in the active backlog state

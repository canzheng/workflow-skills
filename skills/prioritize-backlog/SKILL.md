---
name: prioritize-backlog
description: Use when a repository with docs/planning needs BACKLOG, SHAPING, and READY items prioritized, reviewed with the user, and then reordered within BACKLOG.md
---

# Prioritize Backlog

## Overview

This skill ranks all eligible items in the active version backlog, proposes an order for user review, and only after approval rewrites the top-to-bottom order inside `[BACKLOG]`, `[SHAPING]`, and `[READY]`.

It is a workflow wrapper around `audit-workflow` plus the helper script at `python "${CODEX_HOME:-$HOME/.codex}/skills/prioritize-backlog/scripts/prioritize_backlog.py"`.

## Defaults

- Operate on the current repository root.
- Fail if `docs/planning/current_version` or the active `BACKLOG.md` is missing.
- Scope is only `[BACKLOG]`, `[SHAPING]`, and `[READY]`.
- Do not change section membership or feature/task status.

## Workflow

1. Run `audit-workflow`.
2. Understand the repository before ranking:
   - read the active version `VERSION_SCOPE.md`
   - read the active `BACKLOG.md`
   - inspect the repo's obvious product context such as `README.md`, top-level docs, and main source directories
   - use `gpt-5.4-mini` explorer subagents for exploration work when available
3. Run:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/prioritize-backlog/scripts/prioritize_backlog.py" list
```

4. Review the returned eligible items and linked OpenSpec context:
   - for `[SHAPING]` and `[READY]`, read the linked OpenSpec change context as needed
   - prefer `proposal.md`, `design.md`, `tasks.md`, and linked change spec markdown over old feature-file sections
   - for `[BACKLOG]`, inspect any surrounding notes in `BACKLOG.md`
5. Rank all eligible items using these heuristics in this exact order:
   - items that do not depend on other items
   - items with higher importance to the repository
   - items with clearer scope and more deterministic execution
   - items with lower estimated complexity
6. Present a ranked list before any edit. Each item must include:
   - section, ID, and title
   - short rationale
   - dependency note
   - risk note
7. Ask for user feedback. Do not rewrite `BACKLOG.md` yet.
8. After explicit approval, finalize one global ID order and run:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/prioritize-backlog/scripts/prioritize_backlog.py" apply \
  --ordered-id <id-1> \
  --ordered-id <id-2>
```

9. Re-run `audit-workflow`.
10. Show the resulting order or diff, calling out any remaining uncertainty.

## Rules

- Treat the heuristics as lexicographic. Do not average away a likely dependency blocker because an item looks important.
- Prefer evidence from the repository over generic product intuition.
- If dependencies, impact, or complexity are uncertain, say so explicitly and reflect that in the risk note.
- Preserve exact backlog entry text. Only reorder existing entry lines inside `[BACKLOG]`, `[SHAPING]`, and `[READY]`.
- Keep the final approved order global, but remember that file edits only reorder items within their existing section.

## Stop Conditions

- `audit-workflow` reports an invalid workflow state
- `docs/planning/current_version` is missing or not a symlink
- the active `BACKLOG.md` has malformed structured entries
- a linked feature file in `[SHAPING]` or `[READY]` is missing
- the user has not approved the final order yet

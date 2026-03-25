---
name: audit-workflow
description: Use when validating the repository workflow state before or after any planning-state edit, or when a workflow skill needs a guard check
---

# Audit Workflow

## Overview

Run the deterministic workflow audit before and after any state-changing workflow action.

The audit checks the active version under `<repo_root>/docs/planning/current_version` and the required `openspec/` scaffold against the global workflow contract, plus any repo-local `AGENTS.md` overlay.

## Run

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/audit-workflow/scripts/audit_workflow.py"
```

## What It Checks

- `current_version` exists and is a symlink
- `openspec/` exists with the required `specs/` and `changes/` directories
- the active backlog has the required section order
- every non-`[BACKLOG]` feature entry links to an existing feature file
- feature IDs match between backlog and feature files
- feature backlog anchors match the owning backlog section
- every promoted feature links to an existing OpenSpec change
- every `[READY]` feature links to an OpenSpec change with `proposal.md`, `design.md`, and `tasks.md`
- every `[READY]` feature has at least one top-level OpenSpec task that resolves to workflow status `ready`
- no feature has task-readiness drift such as:
  - a workflow `Depends On` reference that points at an unknown dependency id
  - inconsistent OpenSpec-backed task readiness
  - a task that references an unknown dependency id through the workflow dependency convention
- at most one repository task is `in_progress`

## How To Use It

1. Run the audit.
2. If it passes, proceed with the workflow action.
3. If it fails, stop and fix the reported issue or use `repair-drift`.
4. Re-run the audit after the repair or workflow action.

## Stop Conditions

- Any reported error
- Ambiguity about the intended source of truth
- Missing active-version files or broken links

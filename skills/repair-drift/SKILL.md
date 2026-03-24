---
name: repair-drift
description: Use when the backlog and feature files disagree or the workflow audit reports a planning-state inconsistency that needs minimal repair
---

# Repair Drift

## Overview

This skill repairs minimal workflow-state mismatches between the active backlog, feature files, and required OpenSpec links.

It is a workflow repair wrapper around `audit-workflow`.

## Defaults

- If the user names a specific issue, repair that issue.
- Otherwise run `audit-workflow` and repair the first reported inconsistency.

## Workflow

1. Run `audit-workflow`.
2. Identify the concrete inconsistency to repair.
3. Determine the intended source of truth from:
   - current backlog section
   - feature-file metadata
   - linked OpenSpec change metadata
   - explicit user instruction
4. Apply the smallest repair that restores consistency.
5. Re-run `audit-workflow`.

## Typical Repairs

- wrong backlog anchor in a feature file
- feature entry in the wrong backlog section
- stale `Current Task`
- missing or stale OpenSpec change link metadata
- illegal task-status combination
- missing required feature sections

## Rules

- Repair structure, not domain intent.
- If the intended source of truth is ambiguous, stop and ask.
- Do not silently rewrite large sections when a local fix is enough.

## Stop Conditions

- No concrete inconsistency is available
- The intended source of truth is ambiguous
- Repair would require guessing feature scope or product intent
- `audit-workflow` still fails after the attempted repair

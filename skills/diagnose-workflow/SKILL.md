---
name: diagnose-workflow
description: Use when you need a non-blocking sanity report of workflow health, active feature state, and OpenSpec linkage without enforcing the audit gate
---

# Diagnose Workflow

## Overview

Run a read-only workflow diagnosis to understand the current workflow state without treating findings as a hard gate.

This skill complements `audit-workflow`:
- `audit-workflow` is the deterministic pass/fail gate
- `diagnose-workflow` is the operator-facing health report

## Run

```bash
python "${AGENTS_HOME:-$HOME/.agents}/skills/diagnose-workflow/scripts/diagnose_workflow.py"
```

## What It Reports

- active version and backlog path
- feature counts by workflow section
- per-feature workflow and OpenSpec linkage summary
- active task count and current-task pointers
- legacy-exempt completed features
- readiness drift, missing links, archive mismatches, and other findings grouped as structured diagnostics

## How To Use It

1. Run the diagnosis script.
2. Review the JSON report for `errors`, `warnings`, and per-feature findings.
3. If the repo should be in a valid gated state, follow with `audit-workflow`.
4. If the report surfaces repairable structure issues, use `repair-drift` or make the minimal intended fix.

## Rules

- This skill never mutates workflow artifacts.
- This skill does not replace `audit-workflow`.
- Prefer this skill when you need a workflow health snapshot before deciding whether to repair, defer, or continue work.

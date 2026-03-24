---
name: initialize-workflow-artifacts
description: Use when a repository wants to adopt the docs/planning workflow but does not yet have the required scaffold, or when an existing scaffold is partially missing and needs conservative repair.
---

# Initialize Workflow Artifacts

## Overview

Create the minimum valid `docs/planning/` plus `openspec/` scaffold for the workflow contract without overwriting existing user content.

Use this before `audit-workflow` if the repo does not yet have `docs/planning/current_version`, `ROADMAP.md`, the active version directories, or the required OpenSpec scaffold.

## Run

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py" --version v1
```

## What It Creates

- `docs/planning/ROADMAP.md`
- `docs/planning/template/feature-template.md`
- `docs/planning/versions/<version>/VERSION_SCOPE.md`
- `docs/planning/versions/<version>/BACKLOG.md`
- `docs/planning/versions/<version>/features/`
- `docs/planning/current_version` symlink
- `openspec/specs/`
- `openspec/changes/archive/`

## Rules

- Create missing files and directories only.
- Preserve existing files.
- Stop on conflicting `current_version` links or non-symlink path collisions.
- Prefer project-relative contents and placeholders only.

## Typical Flow

1. Run the initializer in the target repo.
2. Confirm the scaffold exists.
3. Run `audit-workflow`.
4. Start shaping backlog items.

---
name: shape-backlog-item
description: Use when taking a backlog item and turning it into one or more shaped feature files under the repository workflow
---

# Shape Backlog Item

## Overview

This skill promotes one backlog item into one or more features in `[SHAPING]`, or rewrites it into smaller backlog items first.

It is a workflow wrapper around `brainstorming` plus linked OpenSpec change creation. It owns target selection, feature ID assignment, required OpenSpec linkage, feature-file creation, and backlog updates.

## Defaults

- If the user names a backlog item, use it.
- Otherwise select the first item under `[BACKLOG]` in `<repo_root>/docs/planning/current_version/BACKLOG.md`.
- "First" means top-to-bottom document order.

## Workflow

1. Run `audit-workflow`.
2. Resolve the active version through `<repo_root>/docs/planning/current_version`.
3. Read the selected backlog item.
4. Wrap `brainstorming` to decide whether the item becomes:
   - one feature
   - multiple features below the 5-feature split limit
   - or smaller backlog items first
   - do not continue until the wrapped `brainstorming` flow has completed its required review gates for the chosen shaping output
   - once the shaping output is clear, call `retrieve-lessons` to retrieve relevant active lessons and record the returned lesson IDs in the feature file handoff notes under a stage-scoped canonical `Retrieved Lesson IDs: ...` line for `shaping`; use `none` when no lessons are returned
5. For each promoted feature:
   - assign the next feature ID
   - run `openspec-propose` to create or update exactly one linked OpenSpec change for the feature's shaping authority
   - prefer linked change ids that reuse the feature-style prefix when practical, while keeping that naming convention non-gating
   - identify the corresponding existing documentation and spec surfaces likely affected by the feature, ensure the linked OpenSpec change captures the relevant paths, and note any documentation follow-up that shaping is not ready to reconcile yet
   - capture the proof obligations and validation surfaces that the shaped feature expects executable tasks to carry forward so later readiness review can confirm the contract is clear without forcing `start-task` to invent or narrow it
   - create the feature file under `features/` by running `python "${AGENTS_HOME:-$HOME/.agents}/skills/shape-backlog-item/scripts/render_feature_file.py"`
   - pass the authoritative OpenSpec change and affected spec paths as explicit inputs to the renderer
   - do not duplicate proposal, design, spec, or task prose from OpenSpec inside the feature file
   - before the stage exits, call `record-lesson-usage` for the retrieved lesson IDs to reconcile whether they materially influenced the shaped output
   - then record any warranted high-signal notes in `docs/lessons/notes.md`
6. Update feature files first, then update `BACKLOG.md` by editing only the entry headings; do not carry the backlog item's body notes into the promoted entry.
7. Place promoted features at the bottom of `[SHAPING]` as heading-only entries, preserving the existing top-to-bottom order of earlier items.
8. Re-run `audit-workflow`.
9. Commit the intentional planning-state changes when needed to leave the primary checkout clean before exiting.
10. Confirm the primary checkout is clean before exit.

## Rules

- Follow the global workflow contract plus any repo-local `AGENTS.md` overrides.
- This skill is planning-only. Run it from a clean primary checkout and do not create or reuse a feature worktree here.
- Leave the primary checkout clean before exiting this skill.
- A clean planning exit usually means committing the intentional shaping changes, but the invariant is a clean primary checkout.
- `brainstorming` owns the design-review gates for this skill. Do not treat shaping as complete until its required approvals and review loops have passed.
- This workflow requires OpenSpec. Do not promote a feature without a linked OpenSpec change.
- This skill must run `openspec-propose` for promoted work. Do not rely on a separate manual `openspec-propose` run followed by hand-edited workflow state.
- This skill must create feature files through the renderer script, not by freehand authoring.
- Preserve inherited validation and review gates. OpenSpec shaping does not relax audit, review, or verification requirements.
- Keep a single backlog-item split below 5 features.
- If the work appears to need 5 or more features, split it into multiple `[BACKLOG]` items first.
- Do not mark any feature `[READY]` in this skill.
- When shaping an executable task, make the proof-obligation and validation-coverage expectations explicit enough that `ready-feature` can pass its independent readiness review without forcing `start-task` to infer the contract surface from scratch.

## Stop Conditions

- The selected item is not in `[BACKLOG]`
- The split is still unclear after shaping
- The item appears to need 5 or more features before a smaller backlog split
- A feature ID collision or link-path conflict appears
- The primary checkout cannot be left clean before exit
- `audit-workflow` reports an invalid workflow state

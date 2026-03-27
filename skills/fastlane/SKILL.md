---
name: fastlane
description: Use only for very small, low-risk edits such as wording fixes, typo fixes, comments, docs copy edits, or tiny non-behavioral renames. Do not use when behavior, API, schema, config semantics, tests, or cross-file logic may change. Reject oversized or ambiguous tasks and route them back to the normal repository workflow.
---

# Fastlane

## Purpose

Handle tiny, low-risk edits quickly without entering heavyweight workflow.

## Eligibility

Use this skill only if all of the following are true:

- the requested change is small and localized
- no behavior change is intended
- no public API or interface change
- no schema, migration, or data-model change
- no config semantic change
- no test contract change
- no new dependency
- no more than 2 files
- no more than ~30 changed lines
- no architectural judgment is required
- no broader cleanup or opportunistic refactor is needed

Typical eligible tasks:

- fix wording in UI copy
- fix typo in docs or comments
- improve an error/help message without changing meaning
- small markdown cleanup
- rename a purely local variable for clarity with no behavior change

## Hard reject conditions

Reject fastlane immediately if any of the following is true:

- behavior may change
- public API/interface may change
- schema/data model/config semantics may change
- tests need to be added or changed for correctness
- the task touches multiple logical areas or subsystems
- more than 2 files are needed unless the edits are trivially identical
- the request is ambiguous and a “small edit” is not obviously safe
- the task asks for refactor, cleanup, optimization, or restructuring beyond the minimal fix

## What to do when rejected

When the task is out of scope:

1. Say it is **rejected by fastlane**.
2. State the concrete reason in one sentence.
3. Route it back to the normal repository workflow.
4. Do not perform partial risky edits.

## Execution rules

For eligible tasks:

1. Make the smallest possible edit.
2. Touch only the necessary file(s).
3. Preserve existing style, formatting, and intent.
4. Once fastlane accepts the task, do not invoke another workflow skill or load `docs/planning/WORKFLOW_REFERENCE.md`, OpenSpec artifacts, or workflow feature/task files while executing the edit.
5. Only load those workflow materials if fastlane rejects the task and routes it back to the normal repository workflow.
6. Do not invoke Superpower.
7. Do not spawn subagents.
8. Do not scan unrelated files.
9. Do not perform unrelated cleanup.
10. Run only the narrowest relevant validation, if any.
11. Stop once the requested tiny fix is complete.

## Validation policy

Validation should be minimal:

- docs/comment/wording only: usually no validation needed
- tiny UI/static text change: only the most local sanity check if cheap
- local rename with zero behavior change: only lightweight syntax or type check if already very cheap

Do not run broad test suites unless explicitly requested.

## Response format

Always respond in this structure:

- `eligibility`: eligible | rejected
- `reason`: one sentence
- `files_touched`: list
- `validation`: none | exact command(s)
- `summary`: one or two lines

If eligible, include a focused diff summary.
If rejected, explicitly say: `Route to normal repository workflow.`

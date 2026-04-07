---
name: record-lesson-usage
description: Record how previously retrieved lessons were used after a task completes, using `docs/lessons/lessons.md` and the target repo's `docs/lessons/lessons-schema.md`.
---

# Record Lesson Usage

## Overview

Record whether each lesson_id was applied, partially applied, or not applied.

## Workflow

1. Read the target repo's `docs/lessons/lessons-schema.md` and `docs/lessons/lessons.md`.
2. For each lesson_id you need to record at the end of the task, choose exactly one status: `applied`, `partially_applied`, or `not_applied`.
3. Record the matching `lesson_id` together with the chosen status.
4. If a lesson was partially applied, also record the chosen `applied_level` between `0.1` and `0.9`.
5. If a lesson was applied, add `1.0` to `applied_count` and set `last_applied_at` to today.
6. If a lesson was partially applied, add the recorded `applied_level` to `applied_count` and set `last_applied_at` to today.
7. If a lesson was not applied, add `0.0` to `applied_count` and leave `last_applied_at` unchanged.
8. Do not change `retrieved_count`.
9. Update only the referenced lessons and preserve unrelated entries, structure, and formatting.

## Judgment Rules

- Mark `applied` when the lesson materially changed execution, decision-making, debugging, validation, documentation, optimization, or implementation behavior.
- Mark `partially_applied` when the lesson influenced the task in a limited or incomplete way and you can assign a meaningful `applied_level`.
- Mark `not_applied` when the lesson did not materially affect the task.
- Keep judgments concise and practical.

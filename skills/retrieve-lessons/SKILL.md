---
name: retrieve-lessons
description: Retrieve up to three relevant active lessons for the current task from `docs/lessons/lessons.md`, using the embedded retrieval index, then update only the returned lessons' retrieval metadata.
---

# Retrieve Lessons

## Overview

Use this skill when a task should be guided by existing promoted lessons in `docs/lessons/lessons.md`. It only selects and returns relevant lessons; end-of-task usage is recorded separately.

## Workflow

1. Read the target repo's `docs/lessons/lessons-schema.md` and follow it exactly.
2. Consider only lessons with `status: active`.
3. Use the embedded retrieval index fields to rank relevance: `status`, `domain`, `task_type`, `scope`, `tags`, `applies_when`, `confidence`, `retrieved_count`, `applied_count`.
4. Select at most 3 lessons that best match the current task.
5. Return only `id`, `domain`, `lesson`, `applies_when`, and `rationale` for the final set.
6. After finalizing the returned set, update only those lessons in `docs/lessons/lessons.md`: increment `retrieved_count` by 1 and set `last_retrieved_at` to today.

## Selection Rules

- Prefer lessons that match the current domain, task type, or scope.
- Prefer specific trigger conditions in `applies_when`.
- Prefer evidence-supported or high-confidence lessons.
- Prefer lessons likely to reduce rework, mistakes, debugging time, performance waste, documentation gaps, validation misses, or workflow friction.
- If no lesson is relevant enough, return an empty set and do not update the file.
- Count a lesson as retrieved only if it is included in the final returned set.
- Leave unrelated entries untouched and do not change `applied_count`.

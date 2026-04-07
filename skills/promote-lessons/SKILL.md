---
name: promote-lessons
description: Promote the small set of reusable, evidence-backed lesson candidates from `docs/lessons/lesson-candidates.md` into `docs/lessons/lessons.md` using the exact schema in the target repo's `docs/lessons/lessons-schema.md`, with a default promotion threshold based on repeated occurrence.
---

# Promote Lessons

## Overview

Promote only the few lesson candidates that should become persistent reusable lessons.

## Workflow

1. Read `docs/lessons/lesson-candidates.md`, `docs/lessons/lessons.md`, and the target repo's `docs/lessons/lessons-schema.md`.
2. Review candidates against the current task context and the existing active lessons.
3. Treat `occurrence_count` as the number of matching candidate records with `status: candidate` for the same lesson idea in `docs/lessons/lesson-candidates.md`.
4. For each candidate, decide explicitly to promote, merge, or discard.
5. Promote at most a small, high-signal set.
6. When promoting, write to `docs/lessons/lessons.md` and use the existing lesson structure exactly.
7. Archive the source candidate record after it is processed.
8. Keep `AGENTS.md` out of the promotion path.

## Promotion Rules

- Promote by default when `occurrence_count >= 2` and the lesson is actionable, reusable, and not weakly evidenced.
- Promote immediately when a candidate is already strong enough that waiting for a second occurrence would add no value.
- Promote only lessons that are reusable, actionable, evidence-supported, and clear enough to change future default behavior.
- Skip one-off feature observations, vague preferences, emotional reactions, low-confidence conclusions, and process that adds more cost than value.
- Do not promote merely because `occurrence_count >= 2` if the lesson is still too feature-specific, fuzzy, noisy, or not clearly reusable.
- Merge overlapping lessons into the existing active lesson instead of creating duplicates.
- Keep the promoted set small, clear, and high-signal.
- Set `updated_at` to today for any lesson that is promoted in place or merged.

## Entry Rules

- Use `L-###` IDs with the next available global sequence in `docs/lessons/lessons.md`.
- Initialize promoted lessons with `status: active`.
- Initialize `retrieved_count` and `applied_count` to `0`.
- Initialize `last_retrieved_at` and `last_applied_at` to `""`.
- Set `updated_at` to today for any newly promoted lesson.
- Preserve file structure and formatting.
- Do not modify unrelated entries.

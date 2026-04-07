---
name: refresh-lessons
description: Refresh active lessons in `docs/lessons/lessons.md` by reviewing each lesson for keep, merge, archive, or AGENTS.md promotion decisions using the target repo's `docs/lessons/lessons-schema.md`.
---

# Refresh Lessons

## Overview

Keep the active lesson set small, current, and high-signal.

## Workflow

1. Read `docs/lessons/lessons.md` and the target repo's `docs/lessons/lessons-schema.md`.
2. Review each existing lesson against relevance, clarity, usefulness, redundancy, and whether it is stable enough to become a standing default.
3. Decide explicitly for each lesson: `keep`, `merge`, `archive`, or `copy_to_agents`.
4. Use `domain`, `retrieved_count`, `applied_count`, `last_retrieved_at`, `last_applied_at`, `applies_when`, and overlap with other lessons as signals.
5. Merge lessons when they substantially overlap in behavior, trigger condition, or intent, or when a stronger lesson can absorb a weaker near-duplicate.
6. Archive lessons when they are stale, superseded, rarely useful, noisy, or no longer worth keeping active.
7. Treat a lesson as stale when it has not been applied for 30 days.
8. Keep the resulting set small, clear, and high-signal.
9. Only `refresh-lessons` may copy a lesson into `AGENTS.md`.

## Decision Rules

- Keep a lesson only if it remains relevant, clear, and useful for improving future execution quality.
- Update only the lesson text and `applies_when` when a lesson is being kept in place.
- For merges, update `lesson`, `applies_when`, `confidence`, `source_evidence`, `applied_count`, `retrieved_count`, `last_retrieved_at`, `last_applied_at`, and `updated_at`.
- When merging, set `last_applied_at` to the later timestamp among the merged lessons.
- Set `updated_at` to today for any lesson that is merged or archived.
- Preserve the strongest evidence when updating or merging.
- Prefer the stronger or more established lesson id when merging.
- Do not duplicate overlapping active lessons.
- Set `status: archived` when archiving.
- Copy a lesson into `AGENTS.md` only if it is highly stable, broadly applicable, and important enough to become a standing default instruction.
- Preserve schema, structure, formatting, and unrelated entries.

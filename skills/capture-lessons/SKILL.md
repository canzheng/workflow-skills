---
name: capture-lessons
description: Capture concise retrospective lesson candidates after task completion, or immediately promote a lesson when it is already strong enough to skip the candidate queue. Use when you need to create, append, update, or directly promote lessons into `docs/lessons/lessons.md` using the target repo's `docs/lessons/lesson-candidates-schema.md` and `docs/lessons/lessons-schema.md`.
---

# Capture Lessons

## Overview

Capture only high-value lesson candidates that are likely to recur and can change future default behavior.
Capture lessons across any relevant domain, including but not limited to:
- workflow
- debugging
- performance
- documentation
- testing
- review
- architecture
- tooling
- data
- reliability


## Workflow

1. Read the target repo's `docs/lessons/lesson-candidates-schema.md`. If the immediate-promotion gate may apply, also read `docs/lessons/lessons-schema.md`.
2. Apply the immediate-promotion gate first. If any of these are true, promote the lesson using the same rules as `promote-lessons` instead of leaving it only as a candidate:
   - high severity or high-cost mistake
   - very strong evidence
   - clearly reusable
3. If the lesson is not strong enough for immediate promotion, capture it in `docs/lessons/lesson-candidates.md`.
4. If `docs/lessons/lesson-candidates.md` does not exist, create it with the exact schema and no extra prose.
5. If `docs/lessons/lesson-candidates.md` exists, check it for the existing entry structure and the next sequence for today.
6. Keep only 0-2 candidates per task unless the task clearly yielded more reusable lessons.
7. If a lesson is promoted directly, archive the source candidate record after processing.
8. Write concise, operational entries only.
9. Append new entries without modifying unrelated ones or changing file formatting.

## Selection Rules

- Capture only lessons that could improve future default behavior or repeated execution quality.
- Promote immediately when the lesson already meets the strong-case gate, even if this is the first occurrence.
- Skip summaries, emotions, one-off feature details, and implementation trivia.
- Prefer lessons that would change a future default step, check, or safeguard.
- If nothing meets that bar, leave the file unchanged.

## Entry Rules

- Use `LC-YYYY-MM-DD-###` IDs with the next available 3-digit sequence for the current date.
- Preserve the schema exactly, including field names, enums, date format, and empty value rules.
- Keep each field short and specific.
- Do not promote candidates during capture unless the strong-case gate is met or the user explicitly asks for promotion.

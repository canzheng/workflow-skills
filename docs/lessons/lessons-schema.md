Use the following schema contract exactly.

Files:
- docs/lessons/lessons.md

General rules:
- Preserve existing file structure and formatting.
- Do not invent new fields unless explicitly instructed.
- Do not rename existing fields.
- Dates must use format YYYY-MM-DD.
- Empty lists must be written as [].
- Empty optional strings must be written as "".
- Use lowercase enum values exactly as specified.

Allowed domain values:
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
- other


Promoted lesson ID format:
- L-###
- ### is a 3-digit global sequence within docs/lessons/lessons.md
- Example: L-001, L-012

Promoted lesson schema:
- id: string, required
- status: active|archived, required
- domain: string, required
- task_type: list[string], required
- scope: list[string], required
- tags: list[string], required
- lesson: string, required
- applies_when: string, required
- rationale: string, required
- source_evidence: string, required
- confidence: low|medium|high, required
- retrieved_count: integer >= 0, required
- applied_count: float >= 0, required
- last_retrieved_at: string, required, use "" if never retrieved
- last_applied_at: string, required, use "" if never applied
- optional_example: string, optional, use "" if empty
- updated_at: YYYY-MM-DD, required

Embedded retrieval index:
- The retrieval index is embedded in each lesson entry in docs/lessons/lessons.md.
- Indexed fields are:
  - status
  - domain
  - task_type
  - scope
  - tags
  - applies_when
  - confidence
  - retrieved_count
  - applied_count

Counting rules:
- A lesson counts as retrieved only if it is included in the final returned set for the current task.
- Do not count lessons that were only scanned, matched, or considered internally.
- A lesson counts as applied only if post-task review determines it materially changed task execution, decision-making, debugging, validation, documentation, optimization, or implementation behavior.
- applied should add 1.0 to applied_count.
- partially_applied should add the model-provided applied level between 0.1 and 0.9 to applied_count.
- not_applied should add 0.0 to applied_count.
- Do not change retrieved_count outside retrieval.
- Do not change applied_count outside post-task usage recording.

Update behavior:
- Append new entries when creating new candidates or lessons.
- Update in place when revising an existing lesson.
- Merge overlapping lessons instead of duplicating them.
- Do not modify unrelated entries.

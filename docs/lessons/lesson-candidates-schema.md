Use the following schema contract exactly.

Files:
- docs/lessons/lesson-candidates.md

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

Lesson candidate ID format:
- LC-YYYY-MM-DD-###
- ### is a 3-digit sequence starting from 001 for each date
- Example: LC-2026-04-08-001

Lesson candidate schema:
- id: string, required
- status: candidate|archived, required
- domain: string, required
- task_type: list[string], required
- scope: list[string], required
- tags: list[string], required
- problem: string, required
- proposed_lesson: string, required
- applies_when: string, required
- evidence: string, required
- confidence: low|medium|high, required
- optional_example: string, optional, use "" if empty
- created_at: YYYY-MM-DD, required

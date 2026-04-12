Use the following schema contract exactly.

Files:
- `docs/lessons/notes.md`

General rules:
- Preserve existing file structure and formatting.
- Do not invent new fields unless explicitly instructed.
- Do not rename existing fields.
- Dates must use format YYYY-MM-DD.
- Empty lists must be written as [].
- Empty optional strings must be written as "".
- Use lowercase enum values exactly as specified.
- Notes are execution-time observations. They are not lessons and do not need complete retrospective answers at creation time.

Allowed kind values:
- signal
- friction
- hypothesis
- failed_attempt
- near_miss
- decision
- pattern
- other

Allowed status values:
- open
- resolved
- invalidated
- distilled
- discarded

Note ID format:
- N-###
- ### is a 3-digit sequence within `docs/lessons/notes.md`
- Example: N-001, N-014

Note schema:
- id: string, required
- status: open|resolved|invalidated|distilled|discarded, required
- created_at: YYYY-MM-DD, required
- updated_at: YYYY-MM-DD, required
- feature_ref: string, required
- task_ref: string, optional, use "" if empty
- kind: string, required
- context: string, required
- observation: string, required
- why_notable: string, required
- current_hypothesis: string, optional, use "" if empty
- artifacts: list[string], required, use [] if empty
- next_check: string, optional, use "" if empty
- outcome: string, optional, use "" if empty
- what_worked: string, optional, use "" if empty
- what_did_not_work: string, optional, use "" if empty
- reusable_insight: string, optional, use "" if empty
- do_differently_next_time: string, optional, use "" if empty
- catch_earlier_by: string, optional, use "" if empty
- distilled_into: list[string], required, use [] if empty

Capture rules:
- At note creation time, require `context`, `observation`, and `why_notable`.
- Prefer adding `current_hypothesis`, `artifacts`, and `next_check` when they would help later distillation.
- Do not require `what_worked`, `what_did_not_work`, `reusable_insight`, `do_differently_next_time`, or `catch_earlier_by` at note creation time.
- If a note later proves wrong or incomplete, update it in place and use `status: invalidated` instead of deleting it automatically.

Distillation rules:
- Review notes at feature close and decide whether each note should be distilled into lessons, resolved locally, invalidated, or discarded.
- A note may produce a positive lesson, a negative lesson, a guardrail lesson, or no lesson.
- When a note contributes to one or more lessons, record those lesson IDs in `distilled_into`.

Update behavior:
- Append new notes when capturing new observations.
- Update an existing note in place when understanding changes later.
- Preserve the original `observation` unless it is factually wrong; later understanding should usually be recorded in `outcome` and the retrospective fields instead of rewriting the note history.
- Do not modify unrelated notes.

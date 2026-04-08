## Context

The repository already has separate skills for lesson retrieval, lesson capture, lesson promotion, lesson usage recording, and manual lesson refresh. What is missing is a canonical workflow contract that explains where those skills sit in the task lifecycle and how lesson IDs move from task start to task completion.

## Goals / Non-Goals

**Goals:**
- Make lesson retrieval part of task start.
- Make lesson usage recording part of task completion.
- Make lesson capture part of task closure.
- Make lesson promotion part of feature finalization.
- Preserve the existing manual `refresh-lessons` workflow.
- Use the feature file as the handoff location for retrieved lesson IDs.

**Non-Goals:**
- Changing the lesson candidate or lesson schemas.
- Adding new lesson metadata fields.
- Automating `refresh-lessons`.
- Changing feature-board lifecycle rules outside the lesson integration itself.

## Decisions

- Use the feature file handoff notes as the transport for retrieved lesson IDs.
  - Rationale: the feature file already owns active execution metadata and handoff notes, so this adds no new storage surface.
  - Alternatives considered: a new lesson-specific metadata block or a separate sidecar file. Rejected because they add unnecessary workflow surface and duplication.
- Record lesson usage in `complete-task`, not `start-task`.
  - Rationale: usage can only be judged after the task body and its verification work are complete.
  - Alternatives considered: recording usage at retrieval time or during `finish-feature`. Rejected because they do not reflect actual task impact.
- Keep `refresh-lessons` explicitly user-triggered.
  - Rationale: refresh is a broader curation action, not a routine lifecycle step.
  - Alternatives considered: auto-refresh during task completion or feature finalization. Rejected because they would add noise and hidden churn.
- Update the workflow reference at a high level and keep the detailed step ordering in the skill docs.
  - Rationale: the canonical workflow reference should describe the lifecycle, while the skill docs should preserve the execution choreography.

## Risks / Trade-offs

- If the retrieved lesson IDs are not recorded consistently, `complete-task` will not be able to reconcile usage cleanly.
  - Mitigation: make the handoff requirement explicit in `start-task` and `complete-task`, and surface it in the feature file.
- Keeping the lesson lifecycle in both the workflow reference and the skills can create duplication.
  - Mitigation: keep the reference short and leave the operational details in the skills.
- Lesson capture at task completion may produce noisy candidates if the threshold is too permissive.
  - Mitigation: keep the strong-case gate narrow and let `promote-lessons` remain conservative.

## Open Questions

- Should retrieved lesson IDs live only in handoff notes, or should the feature file eventually get a dedicated lesson-reuse field?
- Do we want any additional audit checks for malformed lesson handoff state, or is this sufficiently covered by the existing feature-file structure?

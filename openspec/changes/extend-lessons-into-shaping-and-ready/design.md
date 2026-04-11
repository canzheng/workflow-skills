## Context

The repository already has a complete lesson toolchain: `retrieve-lessons`, `record-lesson-usage`, `capture-lessons`, `promote-lessons`, and `refresh-lessons`. The current workflow wires those skills into execution and feature finish, but not into the planning stages where shaping decisions and readiness judgment are made.

That gap matters because shaping and readiness already own high-leverage decisions: feature splitting, affected spec/doc surfaces, proof obligations, validation intent, and readiness contract clarity. If lessons are only applied once execution starts, the workflow misses a chance to prevent weak shaping output earlier.

## Goals / Non-Goals

**Goals:**
- Make relevant active lessons available during `shape-backlog-item` before shaping output is finalized.
- Make relevant active lessons available during `ready-feature` before the independent readiness review runs.
- Record whether retrieved lessons materially influenced shaping or readiness decisions.
- Capture reusable new lessons discovered during shaping or readiness without waiting for execution.
- Reuse existing lesson skills, lesson schemas, and feature-file storage surfaces.

**Non-Goals:**
- Creating a separate planning-only lesson database or schema.
- Changing lesson ranking fields or lesson/candidate schemas.
- Automating `refresh-lessons`.
- Expanding shaping or readiness into broad curation passes over all active lessons.

## Decisions

### Decision: Reuse the existing lesson lifecycle skills at planning stages

`shape-backlog-item` and `ready-feature` will call the same lesson skills already used later in the workflow:
- `retrieve-lessons` at stage entry
- `record-lesson-usage` before stage exit
- `capture-lessons` before stage exit when the stage produces reusable insight

Rationale:
- This preserves one lesson system instead of creating a second planning-specific mechanism.
- The lesson schemas already support planning-stage retrieval because they index on `domain`, `task_type`, `scope`, `tags`, and `applies_when`.
- The same usage accounting model works for planning stages if "applied" is interpreted as materially influencing shaping or readiness decisions.

Alternatives considered:
- Create planning-specific lesson skills. Rejected because they would duplicate existing selection, usage, and capture behavior.
- Restrict lessons to execution only and copy a few stable lessons into `AGENTS.md`. Rejected because that only helps with very broad defaults and misses stage-specific retrieval.

### Decision: Persist planning-stage lesson state in the feature file handoff notes

Planning stages will reuse the feature file's `Handoff Notes` section as the canonical transport for retrieved lesson IDs and usage outcomes. Each planning-stage entry will use stage-scoped canonical lines so later workflow tooling can inspect them deterministically if needed.

Expected canonical lines:
- `Workflow Stage: shaping` or `Workflow Stage: ready`
- `Retrieved Lesson IDs: none` or `Retrieved Lesson IDs: L-001, L-014`
- `Lesson Usage: <concise status summary keyed to the retrieved IDs>`

Rationale:
- The feature file already owns workflow metadata, handoff state, and execution evidence.
- Reusing the feature file avoids adding another tracked planning artifact.
- Stage labels prevent collisions with execution-stage task handoff entries.

Alternatives considered:
- Add new top-level feature-file sections for planning lessons. Rejected because it expands the feature-file contract for a narrow need.
- Store planning-stage lesson state only in `docs/lessons/lessons.md`. Rejected because retrieval metadata alone is not enough to reconstruct feature-local usage.

### Decision: Retrieve lessons early enough to shape the stage outcome, but record usage only at stage exit

`shape-backlog-item` should retrieve lessons after reading the backlog item and initial repo context, but before finalizing the shaping output. `ready-feature` should retrieve lessons after reading the feature file and linked OpenSpec change, but before the independent readiness review. In both cases, usage is recorded only after the stage decisions are complete.

Rationale:
- Retrieval has value only if it can influence the stage outcome.
- Usage cannot be judged until the stage has actually produced or revised artifacts.

Alternatives considered:
- Retrieve lessons after shaping/readiness decisions. Rejected because this turns retrieval into documentation rather than guidance.
- Record usage immediately at retrieval time. Rejected because it would inflate applied counts without evidence that the stage was materially changed.

### Decision: Keep planning-stage capture conservative

`capture-lessons` should run at the end of shaping and readiness only for lessons that would change future planning defaults, such as how shaping defines proof obligations, how readiness checks for ambiguity, or how affected doc/spec surfaces are identified.

Rationale:
- Planning produces lots of observations, but most are feature-specific and should not become reusable lessons.
- A strict capture bar keeps the lesson pool high-signal.

Alternatives considered:
- Capture every notable shaping/readiness observation. Rejected because it would create noisy candidates with low reuse value.

## Risks / Trade-offs

- [Planning-stage retrieval adds ceremony] -> Keep retrieval capped at three lessons and use it only at the boundary of `shape-backlog-item` and `ready-feature`, not throughout every intermediate shaping conversation.
- [Usage judgments during planning are less obvious than execution usage] -> Define "applied" as materially changing shaping output, readiness judgment, proof obligations, or validation expectations, and keep the recorded usage summary concise.
- [Feature-file handoff notes could become inconsistent across stages] -> Standardize stage-scoped canonical lines in the workflow docs and skill text so both stages record the same shape.
- [Planning lessons could drift into duplicate execution lessons] -> Keep `capture-lessons` conservative and let `promote-lessons` continue to merge overlapping ideas before activation.

## Open Questions

- Should the workflow audit eventually validate the presence and formatting of planning-stage canonical lesson lines, or should that remain a softer convention until the lifecycle proves stable?
- Should `ready-feature` treat missing planning-stage lesson state from shaping as informational only, or eventually as a drift signal once the new lifecycle is established?

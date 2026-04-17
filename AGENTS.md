# Repository Guidelines

## Project Structure & Module Organization
This repository is the source-controlled home for global workflow skills. Keep shipped skills under `skills/`, one directory per skill, plus the shared `skills/_workflow/` package. Keep development-only verification in `skills/_workflow/tests/` and root `tests/`; those test files stay in the repo and are not installed into the live global skills directory.

## Build, Test, and Development Commands
Use narrow verification first.

- `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py` runs the repo audit script through the managed Python environment.
- `bin/run-python.sh -m unittest tests.test_install_script -v` verifies `install.sh` syncs the skills and patches only the managed workflow section in global `AGENTS.md`.
- `bin/run-python.sh -m pytest skills/_workflow/tests -q` runs the shared workflow helper and script tests.
- `conda env create -f environment.yml` creates the managed environment named in `environment.yml`.
- `conda env update -f environment.yml --prune` updates the managed environment from the tracked environment definition.
- `bash install.sh` syncs the workflow skills from this repo into `${AGENTS_HOME:-$HOME/.agents}/skills`, patches the managed workflow section in `${AGENTS_HOME:-$HOME/.agents}/AGENTS.md`, and does not install repo-only tests.
- `git status --short` and `git diff --check` confirm you only changed intended files and did not introduce patch-format issues.

## Coding Style & Naming Conventions
Keep mirrored skill directories layout-compatible with the global agent `skills/` root; many scripts resolve sibling paths relative to `skills/`. Prefer small, reversible edits. Use ASCII unless a file already requires Unicode. For Python helpers and tests, follow existing style: 4-space indentation, standard-library-first imports, and focused pytest cases.

## Testing Guidelines
When changing workflow Python code or mirrored tests, run the smallest relevant target first, then broaden only if needed. Tests under `skills/_workflow/tests/` only need to run from this repo, but they must use relative path discovery so contributors can clone the repo anywhere. If you add install behavior, cover it in `tests/test_install_script.py`.

## Commit & Pull Request Guidelines
Use short imperative commit subjects scoped to one change, for example `test: make workflow script tests path-relative`. In pull requests, summarize which skill directories changed, note whether the change must also be installed with `bash install.sh`, and list the exact verification commands you ran.

## Installation Notes
The repo is the development source of truth. Keep the managed workflow policy block in [AGENTS-global-workflow.md](AGENTS-global-workflow.md) and the canonical workflow definitions in [docs/planning/WORKFLOW_REFERENCE.md](docs/planning/WORKFLOW_REFERENCE.md). The installer patches only the marked section from `AGENTS-global-workflow.md` into `${AGENTS_HOME:-$HOME/.agents}/AGENTS.md`. The workflow reference doc for adopting repos is created by `initialize-workflow-artifacts` from its tracked template. After editing `skills/` or the managed workflow block, run `bash install.sh` to copy the tracked workflow skills into the global agent skills directory and update the managed workflow section. The installer fails hard if the target `AGENTS.md` is missing the expected workflow markers, and it excludes repo-only tests and generated Python cache files from the installed skills.

Environment changes happen only through `environment.yml` and `requirements.txt`.
`bin/run-python.sh` is dev-repo-only and is not part of installed skills.


<!-- BEGIN LESSONS NOTES POLICY -->
## Execution Notes

During execution, preserve high-signal observations in `docs/lessons/notes.md`. Notes are the in-flight capture layer. They are not lessons.

### Purpose

- Use notes to preserve context that may be hard to reconstruct later from the repo alone.
- Prefer notes for observations, fragile decisions, near-misses, repeated uncertainty, surprising evidence, and failed paths.
- Distill notes into reusable lessons at feature close.
- Keep notes selective. Do not use them as a changelog or diary.

### When To Write A Note

Write a note when at least one of these is true:

- unexpected friction: The work involves back-and-forth changes, reversions, or repeated rethinking before the path becomes clear.
- misleading path: A plausible direction seems right, but there is risk it may later prove wrong.
- near-miss: Something almost caused a bug, bad edit, broken contract, or wasted effort.
- repeated uncertainty: The agent has to re-evaluate the same question multiple times.
- repeated user correction: The user has to correct or restate the same guidance more than once.
- surprising evidence: A test, error, diff, or behavior changes the current understanding.
- review-loop signal: review feedback triggers rework, or task completion confirms what mattered after review-driven rework.
- possible reusable pattern: Something starts to look like it may generalize beyond this feature.
- a fragile or under-evidenced decision whose rationale may matter later, especially when the decision depends on an assumption, incomplete evidence, or a non-obvious tradeoff

Do not write a note for:

- routine successful execution
- obvious mechanics visible from the final diff
- ordinary command output
- low-value local details with no likely reuse

### Fragile Decisions

Do not try to predict every decision that may later prove wrong.

Instead, write a note when a decision is fragile or under-evidenced, especially when:

- it depends on an assumption not directly validated
- evidence is incomplete or indirect
- multiple plausible options remain
- the downside of being wrong is meaningful
- the rationale will likely be hard to reconstruct later

### What A Note Should Contain

A note should preserve the moment, not force a finished lesson.

At note-taking time, prefer capturing:

- `context`: what we were doing
- `observation`: what happened
- `why_notable`: why this is worth preserving
- `current_hypothesis`: what this may mean right now, if useful
- `artifacts`: relevant files, tests, diffs, commits, logs, or docs
- `next_check`: what would confirm or disprove the current interpretation

Do not require a finished lesson at note time.

### Review-Loop Notes

- When review feedback triggers rework, append a note for that rejection signal.
- At task completion, if review-driven rework occurred, append a follow-up note. This is also warranted when later review implicitly stopped raising the earlier issue even without an explicit acceptance event.
- Answer briefly in process terms. Prefer workflow, review, validation, and decision-making causes over low-level patch detail unless implementation detail is necessary for clarity.

For review-rejection notes, capture:

- What specific concern or deficiency did the review raise?
- What underlying gap in the work caused that concern?
- Why was that gap not caught before review?
- What kind of rework is now required to address it?
- What is the current best guess for preventing or catching this earlier next time?

For task-completion follow-up notes, capture:

- What changed during rework?
- Which part of the rework actually addressed the earlier review concern?
- What turned out to be unnecessary or misdirected?
- What lesson seems reusable now that the task is complete?

### Later Resolution

Notes may later be updated with retrospective understanding. At feature close, review each note and classify it as one of:

- `distilled`: produced one or more reusable lessons
- `invalidated`: later evidence showed the original interpretation was wrong or incomplete
- `discarded`: not useful enough to keep
- `resolved`: understood locally but not worth promoting to a lesson

Invalidated notes may still produce valuable negative lessons or guardrail lessons.

### Relationship To Lessons

- Notes are execution memory recorded in `docs/lessons/notes.md`.
- Lessons are distilled reusable guidance.
- Notes may depend on repo context, diffs, tests, and implementation history for interpretation.
- The repo remains the source of truth for implementation reality.
- Notes remain the source of truth for what was noticed during execution.

### Cleanup

At feature close:

- review all open notes
- distill reusable lessons from the notes
- update note statuses
- remove or archive noise
- preserve invalidated notes when they teach a reusable negative or diagnostic lesson
<!-- END LESSONS NOTES POLICY -->

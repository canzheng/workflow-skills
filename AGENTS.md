# Repository Guidelines

This repository explicitly uses the workflow-skills v2 rewrite. Read
[the contract](docs/workflow/contract.md) and [document index](docs/README.md).
The approved scope is WF2-F01–WF2-F14 in docs/v2/. Historical planning
records do not select a workflow. Repository-local v1 wrappers, global
installation, and Superpowers are obsolete for this rewrite.

## Project structure
Author v2 skills only in `.agents/skills/`; utilities in `tools/workflow/`;
consumer assets in `templates/`; outcome tests in `tests/`.
Run `python3 tools/workflow/verify.py`; use the public setup/doctor/check/migrate
utilities documented in docs/development.md and docs/operations.md.

## Coding and testing
Prefer small reversible changes, ASCII unless Unicode is needed, 4-space
Python indentation, standard-library-first imports, focused tests and relative
path discovery. Start with relevant verification, broaden for integration risk.
Preserve discriminating fixtures and assertions. Check `git diff --check` and
`git status --short`. See docs/development.md for portable verification.

## Commits and review
Use short imperative scoped subjects. Explain behavior, documentation impact,
exact verification and limitations. Preserve unrelated work and instructions.
Never modify global skills/configuration or merge/publish without authorization.

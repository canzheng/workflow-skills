# Repository Guidelines

## Project Structure & Module Organization
This repository is the source-controlled home for global workflow skills. Keep shipped skills under `skills/`, one directory per skill, plus the shared `skills/_workflow/` package. Keep development-only verification in `skills/_workflow/tests/` and root `tests/`; those test files stay in the repo and are not installed into the live global skills directory.

## Build, Test, and Development Commands
Use narrow verification first.

- `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py` runs the repo audit script through the managed Python environment.
- `bin/run-python.sh -m unittest tests.test_install_script -v` verifies `install.sh` syncs the skills and patches only the managed workflow section in global `AGENTS.md`.
- `bin/run-python.sh -m pytest skills/_workflow/tests -q` runs the shared workflow helper and script tests.
- `bin/run-python.sh skills/_workflow/tests/test_audit_checks.py` runs the audit-check self-tests. This file and `mutate_audit_checks.py` are self-running scripts, not pytest modules, so `conftest.py` excludes them from collection; run them directly.
- `bin/run-python.sh skills/_workflow/tests/mutate_audit_checks.py` mutation-tests the audit's own checks and must report zero SURVIVED and zero SKIPPED.
- `bin/run-python.sh skills/_workflow/tests/test_workflow_state_fixes.py` runs the shared-library self-tests; it is a self-running script too.
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

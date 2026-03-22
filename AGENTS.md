# Repository Guidelines

## Project Structure & Module Organization
This repository is the source-controlled home for global workflow skills. Keep shipped skills under `skills/`, one directory per skill, plus the shared `skills/_workflow/` package. Keep development-only verification in `skills/_workflow/tests/` and root `tests/`; those test files stay in the repo and are not installed into the live Codex skills directory.

## Build, Test, and Development Commands
Use narrow verification first.

- `pytest skills/_workflow/tests -q` runs the shared workflow helper and script tests.
- `pytest tests/test_install_script.py -q` verifies `install.sh` can install this repo into a target `CODEX_HOME`.
- `bash install.sh` syncs the workflow skills from this repo into `${CODEX_HOME:-$HOME/.codex}/skills` without installing repo-only tests.
- `git status --short` and `git diff --check` confirm you only changed intended files and did not introduce patch-format issues.

## Coding Style & Naming Conventions
Keep mirrored skill directories layout-compatible with Codex’s `skills/` root; many scripts resolve sibling paths relative to `skills/`. Prefer small, reversible edits. Use ASCII unless a file already requires Unicode. For Python helpers and tests, follow existing style: 4-space indentation, standard-library-first imports, and focused pytest cases.

## Testing Guidelines
When changing workflow Python code or mirrored tests, run the smallest relevant pytest target first, then broaden only if needed. Tests under `skills/_workflow/tests/` only need to run from this repo, but they must use relative path discovery so contributors can clone the repo anywhere. If you add install behavior, cover it in `tests/test_install_script.py`.

## Commit & Pull Request Guidelines
This repo started without inherited git history, so use short imperative commit subjects scoped to one change, for example `test: make workflow script tests path-relative`. In pull requests, summarize which skill directories changed, note whether the change must also be installed with `bash install.sh`, and list the exact verification commands you ran.

## Installation Notes
The repo is the development source of truth. After editing `skills/`, run `bash install.sh` to copy the tracked workflow skills back into the global Codex skills directory. The installer performs a one-way sync for the mirrored workflow skills and `_workflow/`, excluding repo-only tests and generated Python cache files.

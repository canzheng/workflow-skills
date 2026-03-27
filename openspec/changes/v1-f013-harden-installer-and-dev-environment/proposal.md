## Why

The repo's development tooling currently works only in a narrow happy path. First-time installation is not well initialized when an existing `AGENTS.md` lacks workflow markers, and the tracked Python environment is not constrained enough to guarantee a compatible interpreter or repeatable Conda resolution across machines.

## What Changes

- Keep `install.sh` strict when the target `AGENTS.md` file is missing.
- Initialize the managed workflow section when `AGENTS.md` exists but the workflow markers are absent.
- Document the installer's external `rsync` dependency.
- Constrain the tracked Conda environment with an explicit Python floor and declared channels consistent with repo code.
- Add or update regression coverage for installer marker behavior and managed-environment assumptions.

## Capabilities

### New Capabilities
- `repo-development-tooling`: Development installer and managed Python environment behavior for this repository.

### Modified Capabilities
- None.

## Impact

- Affected scripts/docs: `install.sh`, `README.md`, `AGENTS.md`, `bin/run-python.sh`, `environment.yml`, `requirements.txt`
- Affected tests: `tests/test_install_script.py`, `tests/test_run_python_wrapper.py`
- Affected stable spec path: `openspec/specs/repo-development-tooling/spec.md`

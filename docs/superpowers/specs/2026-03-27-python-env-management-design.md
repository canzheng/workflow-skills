# Python Env Management Design

## Summary

Add a repo-local Python environment convention so contributors can run Python scripts and tests through the existing Conda environment named `workflow` without relying on ad hoc shell activation.

This change is for the development repository only. It does not change shipped skill contents, and `bin/run-python.sh` is not part of the installed skills payload.

## Goals

- Make Python execution consistent across repo scripts and tests.
- Keep environment changes declarative through tracked env-management files.
- Avoid depending on interactive shell activation for normal repo commands.
- Keep the change small and reversible.

## Non-Goals

- Ship the wrapper into the installed Codex skills directory.
- Replace Conda with another environment manager.
- Add a general shell-command wrapper.
- Invent a second dependency source beyond the tracked env files.

## Files

### New

- `environment.yml`
  - Declares the Conda environment `workflow`.
  - Installs base interpreter tooling with Conda.
  - Installs Python packages through `pip` using `requirements.txt`.
- `requirements.txt`
  - Owns Python package dependencies for the repo.
  - Starts with `pytest` so the existing test commands work in the managed env.
- `bin/run-python.sh`
  - Repo-local entrypoint for running Python scripts inside the managed Conda env declared by `environment.yml`.
  - Not shipped by `install.sh`.

### Modified

- `AGENTS.md`
  - Documents the environment convention.
  - Replaces bare `python3` and `pytest` examples with `bin/run-python.sh ...`.
- `README.md`
  - Adds contributor-facing setup and usage notes for the managed Python env.

## Command Convention

Use `bin/run-python.sh` for repo Python script entrypoints in this repo.

Examples:

- `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
- `bin/run-python.sh skills/start-task/scripts/resolve_start_task.py`
- `bin/run-python.sh skills/autonomous-backlog-loop/scripts/resolve_autonomous_backlog_action.py --feature-id v1-f005`

Manage environment contents only through the tracked env files:

- `conda env create -f environment.yml`
- `conda env update -f environment.yml --prune`

## Wrapper Behavior

`bin/run-python.sh` will:

- resolve the repo root from its own path
- read `environment.yml` and extract the managed env name from the top-level `name:` field
- require Conda to be available
- require the declared Conda env to exist
- accept only a repo-relative `.py` path plus optional script arguments
- reject:
  - absolute script paths
  - script paths outside the repo
  - module-mode flags such as `-m`
  - non-Python entrypoints
- execute through `conda run -n <env-name-from-environment.yml> ...`

## Error Handling

The wrapper should fail with clear messages when:

- `conda` is not installed or not on `PATH`
- `environment.yml` is missing or does not declare a `name:`
- the declared env does not exist yet
- no entrypoint is provided
- the script path is absolute or resolves outside the repo
- the script path does not end in `.py`
- the target script does not exist

## Testing

Use narrow verification first:

- `bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py`
- `bin/run-python.sh skills/start-task/scripts/resolve_start_task.py`
- direct wrapper checks for:
  - repo-relative script mode
  - environment-name lookup from `environment.yml`
  - clear failure on invalid paths

## Risks

- Contributors without Conda installed will still need one-time setup.
- `conda run` can be slightly slower than a pre-activated shell, but it is more reliable for scripted usage.
- If docs and commands drift, contributors may fall back to raw `python3`; documenting the wrapper in both `AGENTS.md` and `README.md` reduces that risk.

## Open Questions

- None for the initial change. If the repo later needs non-Python tooling wrappers, that should be a separate change rather than broadening `bin/run-python.sh`.

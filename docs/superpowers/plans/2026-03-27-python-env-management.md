# Python Env Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add tracked Conda-based Python environment management plus a repo-local `bin/run-python.sh` wrapper so repo Python scripts and test entrypoints run consistently through the managed env.

**Architecture:** Keep environment state declarative in `environment.yml` and `requirements.txt`, and keep execution policy in one small shell wrapper under `bin/`. Update contributor docs to point at the wrapper, and add regression coverage so the wrapper behavior and the dev-only boundary stay explicit.

**Tech Stack:** Bash, Conda, Python, `unittest`, `pytest`

---

## File Structure

- Create: `environment.yml`
  - Declares the managed Conda env name and base interpreter tooling.
- Create: `requirements.txt`
  - Owns Python package dependencies for the repo, starting with `pytest`.
- Create: `bin/run-python.sh`
  - Runs repo Python scripts and Python module entrypoints through `conda run` using the env name declared in `environment.yml`.
- Create: `tests/test_run_python_wrapper.py`
  - Verifies wrapper behavior, including env-name lookup, module mode, repo-relative script mode, and clear failures on invalid inputs.
- Modify: `AGENTS.md`
  - Documents the new environment convention and replaces raw Python command examples with wrapper-based commands.
- Modify: `README.md`
  - Adds contributor setup and usage instructions for the Conda env and wrapper.
- Modify: `tests/test_install_script.py`
  - Locks in the dev-only boundary by asserting the wrapper is not installed into the Codex skills destination.

### Task 1: Add Managed Env Files And Wrapper

**Files:**
- Create: `environment.yml`
- Create: `requirements.txt`
- Create: `bin/run-python.sh`
- Test: `tests/test_run_python_wrapper.py`

- [ ] **Step 1: Write the failing wrapper tests**

```python
class RunPythonWrapperTests(unittest.TestCase):
    def test_reads_env_name_from_environment_yml(self) -> None:
        ...

    def test_runs_repo_script_via_conda_run(self) -> None:
        ...

    def test_runs_module_entrypoint_via_conda_run(self) -> None:
        ...

    def test_rejects_absolute_script_path(self) -> None:
        ...
```

- [ ] **Step 2: Run the new test target and verify it fails for the expected reason**

Run: `python3 -m unittest tests.test_run_python_wrapper -v`
Expected: FAIL because `bin/run-python.sh` and/or the env files do not exist yet.

- [ ] **Step 3: Add the tracked env-management files**

```yaml
# environment.yml
name: workflow
dependencies:
  - python
  - pip
  - pip:
      - -r requirements.txt
```

```text
# requirements.txt
pytest
```

- [ ] **Step 4: Implement the minimal wrapper**

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=...
ENV_NAME="$(awk '/^name:/ {print $2; exit}' "${REPO_ROOT}/environment.yml")"
cd "${REPO_ROOT}"
exec conda run -n "${ENV_NAME}" python "$@"
```

Implementation details to include:
- repo-root resolution from the wrapper path
- normalization of repo-relative script paths against the repo root before execution, or an equivalent `cd "${REPO_ROOT}"` strategy
- support for either `repo/path/script.py [args...]` or `-m <module> [args...]`
- rejection of absolute paths and non-`.py` script paths
- clear failures for missing `conda`, missing `environment.yml`, missing `name:`, missing env, and missing entrypoint
- a wrapper test proving repo-relative script execution still works when invoked from outside `<repo_root>`

- [ ] **Step 5: Create or update the managed Conda env from the tracked files**

Run: `conda env update -f environment.yml --prune`
Expected: the `workflow` env reflects `environment.yml` and `requirements.txt`, including `pytest`

- [ ] **Step 6: Re-run the wrapper tests and verify they pass**

Run: `python3 -m unittest tests.test_run_python_wrapper -v`
Expected: PASS

- [ ] **Step 7: Commit the task-1 implementation**

```bash
git add environment.yml requirements.txt bin/run-python.sh tests/test_run_python_wrapper.py
git commit -m "feat: add managed python wrapper"
```

### Task 2: Update Repo Command Conventions

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`

- [ ] **Step 1: Write the doc expectation changes**

Document these exact conventions:

```text
bin/run-python.sh skills/audit-workflow/scripts/audit_workflow.py
bin/run-python.sh -m unittest tests.test_install_script -v
bin/run-python.sh -m pytest skills/_workflow/tests -q
conda env create -f environment.yml
conda env update -f environment.yml --prune
```

- [ ] **Step 2: Run a focused diff check on the docs before editing behavior elsewhere**

Run: `git diff -- AGENTS.md README.md`
Expected: no output before the edits

- [ ] **Step 3: Update `AGENTS.md` with the new environment convention**

Required content:
- env changes happen only through `environment.yml` and `requirements.txt`
- Python commands in this repo should use `bin/run-python.sh`
- `bin/run-python.sh` is dev-repo-only and is not part of installed skills

- [ ] **Step 4: Update `README.md` with contributor setup and usage**

Required content:
- one-time Conda env creation/update commands
- wrapper usage for script and module entrypoints
- note that the wrapper derives the env name from `environment.yml`

- [ ] **Step 5: Verify the updated command examples are internally consistent**

Run: `git diff -- AGENTS.md README.md`
Expected: only the intended command and convention updates appear

- [ ] **Step 6: Commit the doc updates**

```bash
git add AGENTS.md README.md
git commit -m "docs: document python env workflow"
```

### Task 3: Lock The Dev-Only Boundary And Validate End-To-End

**Files:**
- Modify: `tests/test_install_script.py`
- Test: `tests/test_install_script.py`
- Test: `tests/test_run_python_wrapper.py`

- [ ] **Step 1: Add an install regression that proves the wrapper is not shipped**

```python
self.assertFalse((codex_home / "bin" / "run-python.sh").exists())
self.assertFalse((skills_root / "run-python.sh").exists())
```

- [ ] **Step 2: Run the install-script tests with the new assertion and verify the existing installer still satisfies the contract**

Run: `python3 -m unittest tests.test_install_script -v`
Expected: PASS, proving the dev-only wrapper stays outside the installed skills payload without changing `install.sh`.

- [ ] **Step 3: Keep `install.sh` unchanged unless the test disproves the current contract**

The intended outcome is that no production installer change is required because `install.sh` already syncs only the tracked skill directories.

- [ ] **Step 4: Run the narrow validation targets through the wrapper**

Run: `bin/run-python.sh -m unittest tests.test_install_script -v`
Expected: PASS

Run: `bin/run-python.sh -m pytest skills/_workflow/tests -q`
Expected: PASS

- [ ] **Step 5: Run patch hygiene checks**

Run: `git diff --check`
Expected: PASS

Run: `git status --short`
Expected: only the intended env, wrapper, docs, and test files are changed

- [ ] **Step 6: Commit the final validation and boundary lock**

```bash
git add tests/test_install_script.py
git commit -m "test: keep python wrapper repo-local"
```

## Notes

- Keep `install.sh` focused on shipping skill directories and patching the managed workflow section. Do not broaden it to install dev-only repo helpers.
- Prefer `conda run` in the wrapper instead of shell activation so commands behave the same in non-interactive automation.
- If wrapper tests need to avoid depending on a real Conda installation, stub `conda` with a temporary executable earlier on `PATH` and assert the invocation contract directly.

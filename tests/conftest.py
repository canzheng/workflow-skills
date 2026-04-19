"""Shared test helpers for workflow-skill integration tests.

This module centralizes three concerns that were duplicated across
`tests/test_workflow_openspec_integration.py`, `tests/test_diagnose_workflow.py`,
and `skills/_workflow/tests/test_workflow_scripts.py`:

1. Loading a resolver script as a Python module via `importlib.util` — each
   skill entry script lives under a hyphenated `skills/<skill>/scripts/`
   directory that cannot be imported with ordinary `import` syntax.
2. Running a resolver's `main(argv)` in-process with captured stdout/stderr —
   so integration tests can assert on the same `.returncode`, `.stdout`,
   `.stderr` surface without paying the ~1.5s Python-fork cost per test.
3. Reusing the ``initialize`` function from
   `skills/initialize-workflow-artifacts/scripts/init_workflow_artifacts.py`
   rather than reloading it in every test file.

## Keep subprocess vs. convert to direct call

An integration test **keeps its subprocess harness** when its coverage
materially differs from what a direct `main(argv)` call provides:

- It asserts on subprocess argv parsing, process exit semantics that are
  distinct from the function's return value, or stdout byte-formatting that a
  Python-level capture cannot faithfully reproduce.
- It exercises an installed-CLI fork path end-to-end (for example, a smoke
  test that proves `python3 <script> --help` still works after a migration).

An integration test **converts to ``run_resolver``** when it asserts on the
logical outcome of the resolver — a JSON payload on stdout, a
``WorkflowError`` message on stderr, or an exit-code distinction between
``0`` and ``1``. Those are all preserved by the in-process runner.

Subprocess calls to the ``git`` binary (via the per-file ``_git`` helper or
similar) are external tooling, not a Python resolver fork. They remain
subprocess.
"""

from __future__ import annotations

import atexit
import contextlib
import importlib.util
import io
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
INIT_SCRIPT = SKILLS_ROOT / "initialize-workflow-artifacts" / "scripts" / "init_workflow_artifacts.py"


_MODULE_CACHE: Dict[str, "object"] = {}


def load_script_module(script_path: Path):
    """Load a skill entry script as a Python module and cache it by path.

    Hyphenated script directories cannot be imported with bare ``import`` syntax,
    so we use ``importlib.util`` and cache the result so repeated calls do not
    re-execute the module body.
    """

    key = str(script_path.resolve())
    cached = _MODULE_CACHE.get(key)
    if cached is not None:
        return cached

    module_name = f"_test_script_{script_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None and spec.loader is not None, script_path
    module = importlib.util.module_from_spec(spec)
    # Register before ``exec_module`` so dataclasses/typing machinery that
    # looks the module up in ``sys.modules`` during class body execution can
    # resolve it.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    _MODULE_CACHE[key] = module
    return module


@dataclass(frozen=True)
class ResolverResult:
    """Stand-in for ``subprocess.CompletedProcess`` when running in-process."""

    returncode: int
    stdout: str
    stderr: str


def run_resolver(
    script_path: Path,
    argv: Sequence[str],
    *,
    cwd: Optional[Path] = None,
) -> ResolverResult:
    """Invoke a resolver's ``main(argv)`` in-process and capture its IO.

    Mirrors the observable contract of::

        subprocess.run(
            ["python3", str(script_path), *argv],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )

    for resolver scripts that expose a ``main(argv)`` entry point and use
    ``argparse`` + ``print`` / ``print(..., file=sys.stderr)`` for output.

    Behavior:
      - Normal return from ``main`` maps directly to ``ResolverResult.returncode``.
      - ``SystemExit`` (raised by ``argparse`` on parse errors) is caught and its
        code forwarded to ``returncode`` (``None`` is coerced to ``0``).
      - Any uncaught exception is re-raised so the test sees it as a hard failure.
      - ``stdout`` / ``stderr`` are captured via :func:`contextlib.redirect_stdout`
        and :func:`contextlib.redirect_stderr`.
      - When ``cwd`` is supplied the process working directory is temporarily
        changed with :func:`os.chdir` and restored after the call, so resolver
        scripts that compute ``repo_root`` via ``git rev-parse`` inherit the
        expected cwd just as ``subprocess.run(..., cwd=cwd)`` would.
    """

    module = load_script_module(script_path)
    main: Callable[[list[str]], int] = getattr(module, "main")

    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    argv_list = list(argv)
    original_cwd = Path(os.getcwd()) if cwd is not None else None
    saved_sys_argv = sys.argv
    # Resolver scripts default to ``sys.argv[1:]`` when their ``main`` receives
    # an empty list or ``None``. Override ``sys.argv`` so the fallback path still
    # sees ``argv_list`` rather than the outer test runner's argv.
    sys.argv = [str(script_path), *argv_list]
    try:
        if cwd is not None:
            os.chdir(cwd)
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            returncode = main(argv_list)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            returncode = 0
        elif isinstance(code, int):
            returncode = code
        else:
            stderr_buf.write(str(code) + "\n")
            returncode = 1
    finally:
        sys.argv = saved_sys_argv
        if original_cwd is not None:
            os.chdir(original_cwd)

    if returncode is None:
        returncode = 0

    return ResolverResult(
        returncode=int(returncode),
        stdout=stdout_buf.getvalue(),
        stderr=stderr_buf.getvalue(),
    )


def _load_real_initialize() -> Callable[[Path, str], None]:
    module = load_script_module(INIT_SCRIPT)
    return getattr(module, "initialize")


_real_initialize: Callable[[Path, str], None] = _load_real_initialize()
"""Unwrapped ``initialize`` from ``init_workflow_artifacts.py``.

Exposed for tests that need the real subprocess-backed behavior; most tests
should use the cached :func:`initialize` wrapper below.
"""


def initialize_repo_scaffold(repo: Path, version: str = "v1") -> Path:
    """Shared factory: materialize a freshly-initialized scaffold at ``repo``.

    Consumed by both ``tests/test_workflow_openspec_integration.py`` and
    ``tests/test_diagnose_workflow.py`` so the scaffold step is written once.
    Results are identical to calling :func:`_real_initialize` directly, but a
    per-version cache copies a pre-built tree instead of re-forking
    ``openspec init`` and ``lessons init`` for every test.
    """

    template = _ensure_scaffold_cache(version)
    if repo.exists():
        shutil.rmtree(repo)
    # ``symlinks=True`` preserves ``docs/planning/current_version`` as a symlink
    # rather than dereferencing it into a regular directory copy.
    shutil.copytree(template, repo, symlinks=True)
    return repo


def initialize(repo: Path, version: str = "v1") -> Path:
    """Backwards-compatible drop-in for ``init_workflow_artifacts.initialize``.

    Uses the cached scaffold copy for speed. Falls back to the real
    subprocess-backed initializer when the cache cannot be populated (for
    example, when ``openspec`` or ``lessons`` is unavailable).
    """

    try:
        return initialize_repo_scaffold(repo, version)
    except Exception:  # pragma: no cover - defensive fallback
        _real_initialize(repo, version)
        return repo


_SCAFFOLD_CACHE: Dict[str, Path] = {}
_SCAFFOLD_CACHE_ROOT: Optional[Path] = None


def _ensure_scaffold_cache(version: str) -> Path:
    global _SCAFFOLD_CACHE_ROOT
    cached = _SCAFFOLD_CACHE.get(version)
    if cached is not None and cached.exists():
        return cached

    if _SCAFFOLD_CACHE_ROOT is None:
        _SCAFFOLD_CACHE_ROOT = Path(tempfile.mkdtemp(prefix="workflow-scaffold-cache-"))
        atexit.register(shutil.rmtree, _SCAFFOLD_CACHE_ROOT, True)

    template = _SCAFFOLD_CACHE_ROOT / f"scaffold-{version}"
    if template.exists():
        shutil.rmtree(template)
    _real_initialize(template, version)
    _SCAFFOLD_CACHE[version] = template
    return template


if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER_SOURCE = REPO_ROOT / "bin" / "run-python.sh"


def _write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def _create_toolchain(
    tmpdir: Path,
    *,
    include_conda: bool = True,
    env_names: list[str] | None = None,
) -> Path:
    toolchain = tmpdir / "toolchain"
    toolchain.mkdir()

    bash = shutil.which("bash") or "/bin/bash"
    awk = shutil.which("awk") or "/usr/bin/awk"
    python3 = shutil.which("python3") or os.fspath(Path(os.sys.executable))

    for name, source in {"bash": bash, "awk": awk, "python3": python3}.items():
        source_path = Path(source)
        if source_path.exists():
            (toolchain / name).symlink_to(source_path)

    if include_conda:
        available_envs = env_names or ["workflow"]
        env_listing_lines = "".join(
            f"                                printf '%s /fake/prefix\\n' '{name}'\n" for name in available_envs
        )
        conda_script = (
            textwrap.dedent(
                """\
                #!/usr/bin/env bash
                set -euo pipefail

                log_path="${CONDA_STUB_LOG:?CONDA_STUB_LOG is required}"
                printf '%s\n' "$*" >> "${log_path}"

                case "${1-}" in
                    env)
                        shift
                        case "${1-}" in
                            list)
                                printf '# conda environments:\n'
                """
            )
            + env_listing_lines
            + textwrap.dedent(
                """\
                                exit 0
                                ;;
                        esac
                        ;;
                    run)
                        shift
                        if [[ "${1-}" != "-n" ]]; then
                            printf 'stub conda expected -n but got: %s\n' "${1-}" >&2
                            exit 2
                        fi
                        env_name="${2-}"
                        shift 2
                        if [[ "${1-}" != "python" ]]; then
                            printf 'stub conda expected python but got: %s\n' "${1-}" >&2
                            exit 2
                        fi
                        shift
                        if [[ -z "${env_name}" ]]; then
                            printf 'stub conda received empty env name\n' >&2
                            exit 2
                        fi
                        exec python3 "$@"
                        ;;
                esac

                printf 'stub conda received unexpected args: %s\n' "$*" >&2
                exit 2
                """
            )
        )
        _write_executable(
            toolchain / "conda",
            conda_script,
        )

    return toolchain


def _write_fixture_repo(tmpdir: Path, *, env_name: str = "workflow") -> Path:
    repo = tmpdir / "repo"
    repo.mkdir()
    (repo / "bin").mkdir()
    shutil.copy2(WRAPPER_SOURCE, repo / "bin" / "run-python.sh")
    (repo / "environment.yml").write_text(
        textwrap.dedent(
            f"""\
            name: {env_name}
            dependencies:
              - python
              - pip
              - pip:
                  - -r requirements.txt
            """
        ),
        encoding="utf-8",
    )
    (repo / "requirements.txt").write_text("pytest\n", encoding="utf-8")

    (repo / "scripts").mkdir()
    (repo / "scripts" / "echo_args.py").write_text(
        textwrap.dedent(
            """\
            from __future__ import annotations

            import json
            import sys
            from pathlib import Path


            print(json.dumps({"cwd": str(Path.cwd()), "argv": sys.argv[1:]}))
            """
        ),
        encoding="utf-8",
    )

    (repo / "samplepkg").mkdir()
    (repo / "samplepkg" / "__init__.py").write_text("", encoding="utf-8")
    (repo / "samplepkg" / "__main__.py").write_text(
        textwrap.dedent(
            """\
            from __future__ import annotations

            import json
            import sys
            from pathlib import Path


            print(json.dumps({"cwd": str(Path.cwd()), "argv": sys.argv[1:]}))
            """
        ),
        encoding="utf-8",
    )

    return repo


def _run_wrapper(
    repo: Path,
    args: list[str],
    *,
    cwd: Path,
    include_conda: bool = True,
    conda_env_names: list[str] | None = None,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    toolchain = _create_toolchain(cwd.parent, include_conda=include_conda, env_names=conda_env_names)
    env = os.environ.copy()
    env.update(
        {
            "PATH": os.fspath(toolchain),
            "CONDA_STUB_LOG": os.fspath(cwd / "conda.log"),
        }
    )
    if extra_env:
        env.update(extra_env)

    return subprocess.run(
        [os.fspath(repo / "bin" / "run-python.sh"), *args],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


class RunPythonWrapperTests(unittest.TestCase):
    def test_script_mode_runs_repo_relative_scripts_from_outside_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp, env_name="alt-workflow")
            outside_cwd = tmp / "outside"
            outside_cwd.mkdir()

            result = _run_wrapper(
                repo,
                ["scripts/echo_args.py", "one", "two"],
                cwd=outside_cwd,
                conda_env_names=["alt-workflow"],
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout.strip())
            self.assertEqual(Path(payload["cwd"]).resolve(), repo.resolve())
            self.assertEqual(payload["argv"], ["one", "two"])

            log = (outside_cwd / "conda.log").read_text(encoding="utf-8")
            self.assertIn("run -n alt-workflow python scripts/echo_args.py one two", log)

    def test_module_mode_uses_the_env_name_declared_in_environment_yml(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp, env_name="module-env")

            result = _run_wrapper(
                repo,
                ["-m", "samplepkg", "alpha"],
                cwd=repo,
                conda_env_names=["module-env"],
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout.strip())
            self.assertEqual(Path(payload["cwd"]).resolve(), repo.resolve())
            self.assertEqual(payload["argv"], ["alpha"])

            log = (repo / "conda.log").read_text(encoding="utf-8")
            self.assertIn("run -n module-env python -m samplepkg alpha", log)

    def test_rejects_absolute_script_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)
            outside_script = tmp / "outside.py"
            outside_script.write_text("print('outside')\n", encoding="utf-8")

            result = _run_wrapper(repo, [os.fspath(outside_script)], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("absolute script paths are not allowed", result.stderr)

    def test_rejects_paths_outside_the_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)
            outside_script = tmp / "outside.py"
            outside_script.write_text("print('outside')\n", encoding="utf-8")

            result = _run_wrapper(repo, ["../outside.py"], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("script path must stay inside the repository", result.stderr)

    def test_rejects_non_python_script_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)
            (repo / "scripts" / "not_python.txt").write_text("hello\n", encoding="utf-8")

            result = _run_wrapper(repo, ["scripts/not_python.txt"], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("script entrypoints must end with .py", result.stderr)

    def test_rejects_missing_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)

            result = _run_wrapper(repo, [], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing entrypoint", result.stderr)

    def test_rejects_missing_module_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)

            result = _run_wrapper(repo, ["-m"], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing python module name", result.stderr)

    def test_rejects_missing_conda(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)

            result = _run_wrapper(repo, ["scripts/echo_args.py"], cwd=repo, include_conda=False)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("conda is required but was not found on PATH", result.stderr)

    def test_rejects_missing_environment_yml(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)
            (repo / "environment.yml").unlink()

            result = _run_wrapper(repo, ["scripts/echo_args.py"], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("environment.yml is missing", result.stderr)

    def test_rejects_environment_yml_without_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp)
            (repo / "environment.yml").write_text(
                textwrap.dedent(
                    """\
                    dependencies:
                      - python
                    """
                ),
                encoding="utf-8",
            )

            result = _run_wrapper(repo, ["scripts/echo_args.py"], cwd=repo)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("environment.yml must declare a top-level name:", result.stderr)

    def test_rejects_missing_conda_environment(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            repo = _write_fixture_repo(tmp, env_name="missing-env")

            result = _run_wrapper(
                repo,
                ["scripts/echo_args.py"],
                cwd=repo,
                conda_env_names=["workflow"],
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("conda environment 'missing-env' is not installed", result.stderr)


if __name__ == "__main__":
    unittest.main()

"""Portable, offline v2 verification; never launches legacy tests."""
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    if sys.version_info < (3, 10):
        print('Python >=3.10 is required', file=sys.stderr)
        return 2
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests/v2'))
    if not suite.countTestCases():
        print('Required v2 tests are missing; refusing an empty pass', file=sys.stderr)
        return 1
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    cli = ROOT / 'tools/workflow/workflow.py'
    if cli.exists() and (cli.parent / 'checks.py').exists():
        return subprocess.run([sys.executable, str(cli), 'check', '--repo', str(ROOT)], check=False).returncode
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

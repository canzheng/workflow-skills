import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class BootstrapTests(unittest.TestCase):
    def test_routing_preserves_rules_without_legacy_activation(self):
        text = (ROOT / 'AGENTS.md').read_text()
        self.assertIn('explicitly uses the workflow-skills v2', text)
        self.assertIn('4-space', text)
        self.assertNotIn('bash install.sh', text)
        self.assertNotIn('bin/run-python.sh', text)
        self.assertIn('Historical planning', text)
        self.assertEqual((ROOT / 'CLAUDE.md').read_text(), '@AGENTS.md\n')

    def test_baseline_is_actual_not_reference(self):
        self.assertIn('d2aaf1904b2ccbe7fbab9733627e9c82fcf12f53',
                      (ROOT / 'docs/migration-v1-v2.md').read_text())

    def test_verifier_rejects_missing_suite(self):
        import subprocess
        import tempfile
        import shutil
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / 'tools/workflow').mkdir(parents=True)
            (root / 'tests/v2').mkdir(parents=True)
            shutil.copy(ROOT / 'tools/workflow/verify.py', root / 'tools/workflow/verify.py')
            result = subprocess.run(['python3', str(root / 'tools/workflow/verify.py')], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('refusing an empty pass', result.stderr)

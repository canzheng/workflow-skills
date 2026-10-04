import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CLI = ROOT / 'node_modules/.bin/openspec'


@unittest.skipUnless(CLI.exists(), 'Optional OpenSpec runtime absent; spec integration pending until npm ci')
class OpenSpecTests(unittest.TestCase):
    def test_actual_validate_and_archive_completed_disposable_change(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            change = root / 'openspec/changes/receipt-protocol'
            (change / 'specs/receipt').mkdir(parents=True)
            (root / 'openspec/specs').mkdir(parents=True)
            (change / 'proposal.md').write_text('# Receipt protocol\n\n## Why\nA receipt consumes quantity totals.\n\n## What Changes\nAdd receipt protocol.\n\n## Impact\nProducer and consumer.\n')
            (change / 'tasks.md').write_text('- [ ] 1. Implement producer and consumer.\n')
            (change / 'specs/receipt/spec.md').write_text('## Purpose\nReceipt producer and consumer preserve integer-cent quantity totals across the module boundary.\n\n## ADDED Requirements\n\n### Requirement: Quantity receipt\nThe receipt SHALL consume actual quantity totals.\n\n#### Scenario: Quantity two\n- **WHEN** price 199 has quantity 2\n- **THEN** receipt shows 398 cents\n')
            r = subprocess.run([str(CLI), 'validate', 'receipt-protocol', '--strict', '--no-interactive'], cwd=root, env={**os.environ, 'OPENSPEC_TELEMETRY': '0', 'DO_NOT_TRACK': '1'}, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            # Partial delivery cannot authorize final archive: no stable spec is promoted.
            self.assertFalse((root / 'openspec/specs/receipt/spec.md').exists())
            self.assertIn('[ ]', (change / 'tasks.md').read_text())
            # Execute actual producer/consumer code before final archive acceptance.
            app = root / 'app'
            app.mkdir()
            cart = (ROOT / 'tests/v2/scenarios/delivery/after/cart.py').read_text()
            shutil.copy(ROOT / 'tests/v2/scenarios/delivery/after/receipt.py', app / 'receipt.py')
            (app / 'cart.py').write_text(cart.replace('price * quantity', 'price'))
            broken = subprocess.run(['python3', str(app / 'receipt.py')], input='{"lines":[[199,2]],"currency":"EUR"}', capture_output=True, text=True)
            self.assertEqual(broken.returncode, 0, broken.stderr)
            self.assertEqual(broken.stdout.strip(), 'EUR 1.99')
            self.assertNotEqual(broken.stdout.strip(), 'EUR 3.98')
            (app / 'cart.py').write_text(cart)
            proof = subprocess.run(['python3', str(app / 'receipt.py')], input='{"lines":[[199,2]],"currency":"EUR"}', capture_output=True, text=True)
            self.assertEqual(proof.returncode, 0, proof.stderr)
            self.assertEqual(proof.stdout.strip(), 'EUR 3.98')
            # Closing owner confirms implemented acceptance before native archive.
            (change / 'tasks.md').write_text('- [x] 1. Implement producer and consumer.\n')
            r = subprocess.run([str(CLI), 'archive', 'receipt-protocol', '--yes'], cwd=root, env={**os.environ, 'OPENSPEC_TELEMETRY': '0', 'DO_NOT_TRACK': '1'}, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            stable = root / 'openspec/specs/receipt/spec.md'
            self.assertIn('Quantity receipt', stable.read_text())
            self.assertFalse(change.exists())
            r = subprocess.run([str(CLI), 'validate', '--specs', '--strict', '--no-interactive'], cwd=root, env={**os.environ, 'OPENSPEC_TELEMETRY': '0', 'DO_NOT_TRACK': '1'}, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_rewrite_is_valid_and_active_with_environment_gate(self):
        r = subprocess.run([str(CLI), 'validate', 'workflow-v2-rewrite', '--strict', '--no-interactive'], cwd=ROOT, env={**os.environ, 'OPENSPEC_TELEMETRY': '0', 'DO_NOT_TRACK': '1'}, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((ROOT / 'openspec/changes/workflow-v2-rewrite/tasks.md').exists())

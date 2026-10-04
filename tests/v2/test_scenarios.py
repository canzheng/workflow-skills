import importlib.util
import json
import pathlib
import subprocess
import tempfile
import unittest
from test_setup import ROOT, init, commit, run


class ScenarioTests(unittest.TestCase):
    def test_real_pinned_bundle_installs_and_executes_its_own_checker(self):
        sha = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
        with tempfile.TemporaryDirectory() as td:
            target = pathlib.Path(td) / 'real consumer'
            init(target)
            (target / 'AGENTS.md').write_text('Unrelated rule: preserve customer data.\n')
            commit(target)
            run('setup', '--source', ROOT, '--revision', sha, '--target', target, '--repository', 'fixture/real-consumer', '--apply')
            self.assertEqual(run('setup', '--source', ROOT, '--revision', sha, '--target', target, '--repository', 'fixture/real-consumer', '--apply')['changes'], [])
            installed = target / 'tools/workflow/workflow.py'
            r = subprocess.run(['python3', str(installed), 'check', '--repo', str(target), '--json'], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            skills = {p.parent.name for p in (target / '.agents/skills').glob('*/SKILL.md')}
            self.assertEqual(skills, {'workflow-design-to-backlog', 'workflow-deliver-issue', 'workflow-risk-review'})
            self.assertFalse((target / 'skills/_workflow').exists())
            self.assertIn('preserve customer data', (target / 'AGENTS.md').read_text())
            run('doctor', '--repo', target)

    def test_cross_module_cli_consumes_total_and_configuration(self):
        cli = ROOT / 'tests/v2/scenarios/delivery/after/receipt.py'
        r = subprocess.run(['python3', str(cli)], input=json.dumps(dict(lines=[[199, 2], [299, 1]], shipping_cents=50, currency='EUR')), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), 'EUR 7.47')
        r = subprocess.run(['python3', str(cli)], input=json.dumps(dict(lines=[[199, 0]], currency='EUR')), capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn('Invalid line items', r.stderr)

    def test_actual_no_impact_bug_restoration_and_documented_feature_example(self):
        spec = importlib.util.spec_from_file_location('repaired', ROOT / 'tests/v2/scenarios/delivery/repaired/cart.py')
        repaired = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(repaired)
        self.assertEqual(repaired.total([(199, 2), (299, 1)]), 697)
        # Existing documentation remains accurate for this bounded repair.
        existing = (ROOT / 'tests/v2/scenarios/delivery/before/README.md').read_text()
        self.assertIn('price multiplied by positive quantity', existing)
        from test_delivery import load_cart
        after = load_cart('after')
        docs = (ROOT / 'tests/v2/scenarios/delivery/after/README.md').read_text()
        self.assertIn('default 0', docs)
        self.assertEqual(after.total([(199, 2), (299, 1)], 50), 747)
        self.assertIn('747 cents', docs)

import json
import pathlib
import subprocess
import tempfile
import unittest
from test_setup import ROOT


class RetirementTests(unittest.TestCase):
    def test_all_baseline_assets_have_reviewable_disposition_and_current_destinations(self):
        manifest = json.loads((ROOT / 'docs/validation/v1-asset-disposition.json').read_text())
        self.assertEqual(manifest['schema_version'], 1)
        paths = subprocess.check_output(['git', '-C', str(ROOT), 'ls-tree', '-r', '--name-only', manifest['baseline']], text=True).splitlines()
        entries = manifest['paths']
        self.assertEqual(len(entries), len(paths))
        self.assertEqual({x['path'] for x in entries}, set(paths))
        for entry in entries:
            self.assertIn(entry['disposition'], ('delete', 'translate', 'current-v2'))
            self.assertTrue(entry['reason'])
            if entry['disposition'] == 'delete':
                self.assertFalse((ROOT / entry['path']).exists(), entry['path'])
                self.assertEqual(entry['destinations'], [])
            else:
                self.assertTrue(entry['destinations'])
                for name in entry['destinations']:
                    self.assertTrue((ROOT / name).is_file(), name)
                if entry['disposition'] == 'current-v2':
                    self.assertEqual(entry['destinations'], [entry['path']])

    def test_clean_clone_has_no_retired_tree_and_keeps_archived_rewrite(self):
        with tempfile.TemporaryDirectory() as td:
            clone = pathlib.Path(td) / 'clone'
            subprocess.run(['git', 'clone', '-q', '--no-hardlinks', str(ROOT), str(clone)], check=True)
            for name in ('skills', 'docs/planning', 'docs/lessons', 'docs/superpowers',
                         'docs/history', 'AGENTS-global-workflow.md', 'install.sh', 'environment.yml', 'bin'):
                self.assertFalse((clone / name).exists(), name)
            self.assertFalse((clone / 'openspec/changes/workflow-v2-rewrite').exists())
            archive = clone / 'openspec/changes/archive/2026-10-05-workflow-v2-rewrite'
            self.assertTrue((archive / 'tasks.md').is_file())
            self.assertNotIn('[ ]', (archive / 'tasks.md').read_text())

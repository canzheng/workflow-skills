import json
import pathlib
import tempfile
import unittest
from test_setup import ROOT, init, commit, run


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name) / 'consumer'
        init(self.root)
        self.folder = self.root / 'docs/planning/versions/v1'
        (self.folder / 'features').mkdir(parents=True)

    def feature(self, fid, state, change=True, metadata_id=None, current='none'):
        p = self.folder / ('features/' + fid + '.md')
        cid = fid + '-example'
        p.write_text(f'# Feature\n- Feature ID: `{metadata_id or fid}`\n- Current Task: `{current}`\n' + (f'- OpenSpec Change: `{cid}`\n' if change else '') + '\nAcceptance: quantity total is 697.\nEvidence: existing result.\nBlocker: Ubuntu pending.\n')
        if change:
            (self.root / 'openspec/changes' / cid).mkdir(parents=True, exist_ok=True)
        return f'## [{state}]\n\n### `{fid}` [Example](features/{fid}.md)\n\n'

    def test_active_done_deferred_preserve_records_and_inspect_is_read_only(self):
        body = self.feature('v1-f001', 'READY') + self.feature('v1-f002', 'DONE') + self.feature('v1-f003', 'DEFER')
        (self.folder / 'BACKLOG.md').write_text('# Backlog\n' + body)
        commit(self.root)
        before = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file() and '.git' not in p.parts}
        r = run('migrate', 'inspect', '--repo', self.root)
        self.assertEqual(r['active_count'], 2)
        self.assertEqual(r['historical_done_count'], 1)
        self.assertEqual([x['proposed_disposition'] for x in r['records']], ['migrate', 'retain-history', 'defer'])
        self.assertIn('Ubuntu pending', r['records'][0]['original_record'])
        after = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file() and '.git' not in p.parts}
        self.assertEqual(before, after)

    def test_duplicate_missing_change_identity_and_malformed_records_do_not_guess(self):
        body = self.feature('v1-f001', 'READY', change=False)
        body += self.feature('v1-f001', 'DEFER', change=False, metadata_id='v1-f999')
        body += '## [UNKNOWN]\n### broken record\n'
        (self.folder / 'BACKLOG.md').write_text(body)
        r = run('migrate', 'inspect', '--repo', self.root, expect=1)
        codes = {x['code'] for x in r['findings']}
        self.assertTrue({'migration.duplicate', 'migration.change', 'migration.identity', 'migration.heading', 'migration.state'} <= codes)

    def test_done_with_current_task_is_inconsistent(self):
        (self.folder / 'BACKLOG.md').write_text(self.feature('v1-f002', 'DONE', current='2'))
        r = run('migrate', 'inspect', '--repo', self.root, expect=1)
        self.assertTrue(any(x['code'] == 'migration.inconsistent' for x in r['findings']))

    def test_final_source_is_empty_and_baseline_done_inventory_remains_reachable(self):
        import subprocess
        r = run('migrate', 'inspect', '--repo', ROOT)
        self.assertEqual(r['active_count'], 0)
        self.assertEqual(r['historical_done_count'], 0)
        baseline = pathlib.Path(self.temp.name) / 'baseline'
        subprocess.run(['git', 'clone', '-q', '--local', str(ROOT), str(baseline)], check=True)
        subprocess.run(['git', '-C', str(baseline), 'checkout', '-q', '--detach', 'd2aaf1904b2ccbe7fbab9733627e9c82fcf12f53'], check=True)
        result = run('migrate', 'inspect', '--repo', baseline)
        self.assertEqual(result['active_count'], 0)
        self.assertEqual(result['historical_done_count'], 19)

    def test_missing_feature_and_escaping_link_are_findings(self):
        (self.folder / 'BACKLOG.md').write_text('## [READY]\n### `v1-f001` [Missing](features/missing.md)\n### `v1-f002` [Escape](../../../../outside.md)\n')
        r = run('migrate', 'inspect', '--repo', self.root, expect=1)
        self.assertEqual(r['active_count'], 2)
        self.assertTrue(any(x['code'] == 'migration.feature' for x in r['findings']))

    def test_interrupted_cutover_reconciles_old_identity_and_preserves_human_edits(self):
        from core import Conflict
        from records import source_match, managed_update
        confirmed = dict(number=41, state='open', body='<!-- workflow-source: v1-f001 -->\nHuman acceptance')
        remote = [confirmed]  # response was lost after the first successful creation
        self.assertIs(source_match(remote, 'v1-f001'), confirmed)
        self.assertIsNone(source_match(remote, 'v1-f002'))
        with self.assertRaises(Conflict):
            source_match([confirmed, dict(confirmed, number=42)], 'v1-f001')
        body = '<!-- map:start -->\nold\n<!-- map:end -->'
        with self.assertRaises(Conflict):
            managed_update(body, body + '\nHuman blocker', 'new', '<!-- map:start -->', '<!-- map:end -->')
        self.assertIn('Human acceptance', confirmed['body'])

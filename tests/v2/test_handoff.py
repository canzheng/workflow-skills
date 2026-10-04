import json
import pathlib
import subprocess
import tempfile
import unittest
from test_setup import init, commit, fixture_source, run
from core import Conflict, content_identity
from records import source_match, managed_update


class HandoffTests(unittest.TestCase):
    def test_missing_branch_stale_revision_and_dirty_content_do_not_certify_head(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            source, target = root / 'source', root / 'target'
            sha = fixture_source(source)
            init(target)
            (target / 'file').write_text('tested original')
            revision = commit(target)
            run('setup', '--source', source, '--revision', sha, '--target', target, '--repository', 'fixture/consumer', '--apply')
            evidence = content_identity(target)
            self.assertTrue(evidence['dirty'])
            run('doctor', '--repo', target, '--expect-revision', revision, '--expect-content', evidence['content_digest'])
            (target / 'file').write_text('changed after pass')
            r = run('doctor', '--repo', target, '--expect-content', evidence['content_digest'], expect=1)
            self.assertTrue(any(x['code'] == 'target.mismatch' for x in r['findings']))
            run('doctor', '--repo', target, '--expect-branch', 'missing-branch', expect=1)
            run('doctor', '--repo', target, '--expect-revision', '0' * 40, expect=1)
            run('doctor', '--repo', root / 'missing-worktree', expect=2)

    def test_timeout_reconciliation_reuses_confirmed_creation(self):
        # Fault fixture: creation succeeded remotely but response was lost.
        remote, calls = [], []
        fid = 'WF2-F09'
        self.assertIsNone(source_match(remote, fid))
        calls.append('create')
        remote.append(dict(number=9, body='<!-- workflow-source: WF2-F09 -->', state='open'))
        # A timeout is unknown. Re-read both states before any retry.
        confirmed = source_match(remote, fid)
        self.assertEqual(confirmed['number'], 9)
        self.assertEqual(calls, ['create'])
        self.assertIs(source_match(remote, fid), confirmed)

    def test_permission_loss_midbatch_and_concurrent_human_update(self):
        remote = [dict(number=9, body='<!-- workflow-source: WF2-F09 -->')]
        confirmed = source_match(remote, 'WF2-F09')
        self.assertEqual(confirmed['number'], 9)
        with self.assertRaises(PermissionError):
            raise PermissionError('fixture denied second creation')
        self.assertIsNone(source_match(remote, 'WF2-F10'))
        body = '<!-- begin -->\nold\n<!-- end -->\nHuman description'
        with self.assertRaises(Conflict):
            managed_update(body, body + '\nHuman correction', 'new', '<!-- begin -->', '<!-- end -->')
        self.assertEqual(len(remote), 1)

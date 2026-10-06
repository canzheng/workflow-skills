"""Unrelated filesystem filenames must survive complete public verification."""
import os
import unittest

import test_setup
from core import git
from test_setup import run


class FilesystemPathTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def test_non_utf8_project_filename_preserves_bytes_index_and_json_results(self):
        for storage in ['tracked', 'ignored']:
            with self.subTest(storage=storage):
                root = self.base / ('consumer-' + storage)
                test_setup.init(root)
                run('setup', '--source', self.source, '--revision', self.sha,
                    '--target', root, '--repository', 'fixture/consumer',
                    '--skill-storage', storage, '--apply')
                name = os.fsencode(root) + b'/bad-\xff.txt'
                with open(name, 'wb') as f: f.write(b'Unrelated customer file\n')
                (root / 'unrelated-link').symlink_to(os.fsdecode(b'bad-\xff.txt'))
                test_setup.commit(root)
                index = (root / '.git/index').read_bytes()
                for command in ['check', 'doctor', 'bootstrap']:
                    report = run(command, '--repo', root)
                    self.assertTrue(report['ok'])
                    self.assertEqual((root / '.git/index').read_bytes(), index)
                    with open(name, 'rb') as f: self.assertEqual(f.read(), b'Unrelated customer file\n')
                self.assertEqual(git(root, 'status', '--porcelain'), b'')

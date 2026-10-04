"""Exercise the source-owned entrypoint against real consumer Git checkouts."""
import json
import pathlib
import subprocess
import unittest

import test_setup
from core import SKILLS, git, shared


class EnvironmentSetupTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def entrypoint(self):
        p = self.source / 'tools/workflow/environment-setup.sh'
        p.write_bytes((test_setup.TOOLS / 'environment-setup.sh').read_bytes())
        self.sha = test_setup.commit(self.source)
        return p

    def execute(self, script, target, success=True):
        r = subprocess.run(['bash', str(script), str(target), 'fixture/consumer'], capture_output=True, text=True)
        if success:
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        else:
            self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def test_source_entrypoint_adopts_unborn_root_and_repeats_without_index_or_file_changes(self):
        script = self.entrypoint()
        fresh = self.base / 'unborn consumer with spaces'
        test_setup.init(fresh)
        (fresh / 'AGENTS.md').write_text('Keep the human rule.\n')
        p = fresh / '.agents/skills/project-rules/SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('---\nname: project-rules\ndescription: Human policy\n---\nKeep me.\n')
        self.execute(script, fresh)
        manifest = json.loads((fresh / '.workflow/install-manifest.json').read_text())
        self.assertEqual(manifest['source_revision'], self.sha)
        identity = test_setup.run('doctor', '--repo', fresh)['content']
        self.assertIsNone(identity['revision'])
        self.assertTrue(identity['dirty'])
        self.assertIn('Keep the human rule.', (fresh / 'AGENTS.md').read_text())
        self.assertFalse((fresh / '.workflow/cloud-setup.sh').exists())
        self.assertFalse((fresh / 'tools/workflow/environment-setup.sh').exists())
        before = {p.relative_to(fresh): p.read_bytes() for p in fresh.rglob('*') if p.is_file() and '.git' not in p.relative_to(fresh).parts}
        index = git(fresh, 'ls-files', '--stage')
        second = self.execute(script, fresh)
        self.assertIn('"changes": []', second.stdout)
        self.assertEqual(git(fresh, 'ls-files', '--stage'), index)
        self.assertEqual(before, {p.relative_to(fresh): p.read_bytes() for p in fresh.rglob('*') if p.is_file() and '.git' not in p.relative_to(fresh).parts})
        for name in SKILLS:
            self.assertEqual(git(fresh, 'check-ignore', '.agents/skills/' + name + '/SKILL.md').strip(), ('.agents/skills/' + name + '/SKILL.md').encode())
        sha = test_setup.commit(fresh)
        tracked = git(fresh, 'ls-files', '-z').decode().split('\0')
        self.assertIn('.agents/skills/project-rules/SKILL.md', tracked)
        self.assertFalse(any(shared(name) for name in tracked))
        self.assertEqual(test_setup.run('doctor', '--repo', fresh)['content']['revision'], sha)
        self.assertEqual(git(fresh, 'status', '--porcelain'), b'')

    def test_existing_pin_wins_over_new_environment_seed(self):
        script = self.entrypoint()
        self.execute(script, self.target)
        old_pin = (self.target / '.workflow/install-manifest.json').read_bytes()
        test_setup.commit(self.target)
        (self.source / 'release-note.md').write_text('Different fetch seed.\n')
        self.assertNotEqual(test_setup.commit(self.source), self.sha)
        self.execute(script, self.target)
        self.assertEqual((self.target / '.workflow/install-manifest.json').read_bytes(), old_pin)
        self.assertEqual(git(self.target, 'status', '--porcelain'), b'')

    def test_wrong_target_and_old_adoption_fail_without_writes(self):
        script = self.entrypoint()
        nested = self.target / 'nested'
        nested.mkdir()
        self.execute(script, nested, success=False)
        self.assertFalse((nested / '.workflow').exists())
        self.assertFalse((self.target / '.workflow').exists())
        self.execute(script, self.base / 'missing', success=False)
        (self.target / '.workflow').mkdir()
        p = self.target / '.workflow/install-manifest.json'
        p.write_text('{"schema_version": 1}\n')
        before = p.read_bytes()
        self.execute(script, self.target, success=False)
        self.assertEqual(p.read_bytes(), before)
        self.assertFalse((self.target / 'tools').exists())

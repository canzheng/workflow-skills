"""Explicit shared-only installation into isolated home-like skill roots."""
import contextlib
import io
import json
import unittest
from unittest.mock import patch

import test_setup
import setup as installer
import workflow
from core import SKILLS, git
from test_setup import run


class GlobalSkillsTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def arguments(self):
        return ['install-skills', '--source', self.source, '--revision', self.sha,
                '--target', self.base / 'user/.agents/skills']

    def snapshot(self, root):
        return {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}

    def test_shared_only_dry_run_apply_repeat_and_default_home_path(self):
        args = self.arguments(); root = args[-1]
        project = root / 'other-project/SKILL.md'
        project.parent.mkdir(parents=True); project.write_text('Human skill')
        before = self.snapshot(root)
        run(*args)
        self.assertEqual(self.snapshot(root), before)
        result = run(*args, '--apply')
        self.assertEqual(set(result['changes']), {s + '/SKILL.md' for s in SKILLS} |
                         {'workflow-risk-review/references/methods.md', '.workflow-skills-install.json'})
        self.assertEqual(project.read_text(), 'Human skill')
        self.assertFalse((root / 'docs').exists())
        self.assertFalse((root / 'tools').exists())
        self.assertFalse((root / 'AGENTS.md').exists())
        before = self.snapshot(root)
        self.assertEqual(run(*args, '--apply')['changes'], [])
        self.assertEqual(self.snapshot(root), before)
        # Resolve the real default spelling without touching the actual user's home.
        argv = list(map(str, args[:-2])) + ['--apply', '--json']
        with patch('pathlib.Path.home', return_value=self.base / 'user'), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(argv), 0)
        self.assertEqual(self.snapshot(root), before)

    def test_unmanaged_modified_and_symlinked_skills_are_preserved(self):
        args = self.arguments(); root = args[-1]
        p = root / 'workflow-risk-review/SKILL.md'
        p.parent.mkdir(parents=True); p.write_text('Existing global workflow')
        run(*args, '--apply', expect=1)
        self.assertEqual(p.read_text(), 'Existing global workflow')
        p.unlink(); run(*args, '--apply')
        p.write_text('Human global modification'); before = self.snapshot(root)
        run(*args, '--apply', expect=1)
        self.assertEqual(self.snapshot(root), before)
        p.unlink(); p.symlink_to(self.source / '.agents/skills/workflow-risk-review/SKILL.md')
        run(*args, '--apply', expect=2)
        self.assertTrue(p.is_symlink())

    def test_interrupted_apply_rolls_back_and_bad_pin_does_not_write(self):
        args = self.arguments(); root = args[-1]
        root.mkdir(parents=True); before = self.snapshot(root)
        actual = installer.transaction
        with patch.object(installer, 'transaction', side_effect=lambda r, c: actual(r, c, fail_after=1)), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(list(map(str, args)) + ['--apply']), 1)
        self.assertEqual(self.snapshot(root), before)
        bad = args.copy(); bad[bad.index('--revision') + 1] = 'main'
        run(*bad, '--apply', expect=2)
        self.assertEqual(self.snapshot(root), before)
        run(*args, '--apply')

    def test_bounded_uninstall_preserves_other_skills_and_modified_residuals(self):
        args = self.arguments(); root = args[-1]
        run(*args, '--apply')
        other = root / 'other-project/SKILL.md'; other.parent.mkdir(); other.write_text('Keep')
        changed = root / 'workflow-risk-review/SKILL.md'; changed.write_text('Human edit')
        result = run('install-skills', '--target', root, '--uninstall', '--apply', expect=1)
        self.assertEqual(result['residuals'], ['workflow-risk-review/SKILL.md'])
        self.assertEqual(changed.read_text(), 'Human edit')
        self.assertEqual(other.read_text(), 'Keep')
        self.assertFalse((root / 'workflow-deliver-issue/SKILL.md').exists())
        self.assertEqual(json.loads((root / '.workflow-skills-install.json').read_text())['files'].keys(),
                         {'workflow-risk-review/SKILL.md'})

    def test_global_target_does_not_change_consumer_files_or_index(self):
        before = (self.target / 'AGENTS.md').read_bytes(), (self.target / '.git/index').read_bytes()
        run(*self.arguments(), '--apply')
        self.assertEqual(before, ((self.target / 'AGENTS.md').read_bytes(), (self.target / '.git/index').read_bytes()))
        self.assertEqual(git(self.target, 'status', '--porcelain'), b'')

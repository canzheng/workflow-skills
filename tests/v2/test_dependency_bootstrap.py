"""Real Git clones, scoped ignores, pinned assets and bootstrap failure boundaries."""
import contextlib
import io
import json
import pathlib
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_setup
import bootstrap as dependency
import workflow
from core import Conflict, SKILLS, content_identity, git, shared
from test_setup import commit, run


class DependencyBootstrapTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def adopt(self):
        project_skill = self.target / '.agents/skills/project-rules/SKILL.md'
        project_skill.parent.mkdir(parents=True)
        project_skill.write_text('---\nname: project-rules\ndescription: project-owned\n---\nKeep project rules.\n')
        run(*self.args, '--apply')
        commit(self.target)
        return project_skill

    def erase_dependency(self):
        for skill in SKILLS:
            shutil.rmtree(self.target / '.agents/skills' / skill)

    def tracked_bytes(self):
        return {name: (self.target / name).read_bytes() for name in git(self.target, 'ls-files', '-z').decode().split('\0') if name}

    def test_fresh_clone_bootstraps_ignored_skills_and_preserves_project_owned_files(self):
        project_skill = self.adopt()
        tracked = git(self.target, 'ls-files', '-z').decode().split('\0')
        self.assertIn(project_skill.relative_to(self.target).as_posix(), tracked)
        self.assertFalse(any(shared(name) for name in tracked))
        self.assertIn('.workflow/install-manifest.json', tracked)
        fresh = self.base / 'fresh clone'
        subprocess.run(['git', 'clone', '--quiet', '--no-local', str(self.target), str(fresh)], check=True)
        self.assertFalse((fresh / '.agents/skills/workflow-risk-review').exists())
        before = git(fresh, 'status', '--porcelain')
        preview = run('bootstrap', '--repo', fresh, '--source', self.source)
        self.assertEqual(len(preview['changes']), 3)
        self.assertFalse((fresh / '.agents/skills/workflow-risk-review').exists())
        result = subprocess.run([sys.executable, str(fresh / 'tools/workflow/workflow.py'), 'bootstrap', '--repo', str(fresh), '--source', str(self.source), '--apply', '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for skill in SKILLS:
            name = '.agents/skills/' + skill + '/SKILL.md'
            self.assertEqual((fresh / name).read_bytes(), (self.source / name).read_bytes())
        self.assertEqual(git(fresh, 'status', '--porcelain'), before)
        run('doctor', '--repo', fresh)
        self.assertEqual(run('bootstrap', '--repo', fresh, '--apply')['changes'], [])

    def test_bootstrap_does_not_rewrite_project_policy_config_docs_or_index(self):
        self.adopt()
        (self.target / 'AGENTS.md').write_text('Human project policy.\n' + (self.target / 'AGENTS.md').read_text())
        (self.target / 'docs/workflow/contract.md').write_text('Human-edited tracked contract.\n')
        cp = self.target / '.workflow/config.json'
        c = json.loads(cp.read_text())
        c['openspec'] = 'disabled'
        cp.write_text(json.dumps(c))
        before = self.tracked_bytes()
        index = git(self.target, 'ls-files', '--stage')
        self.erase_dependency()
        run('bootstrap', '--repo', self.target, '--source', self.source, '--apply')
        self.assertEqual(self.tracked_bytes(), before)
        self.assertEqual(git(self.target, 'ls-files', '--stage'), index)

    def test_modified_extra_or_symlinked_dependency_fails_before_any_writes(self):
        self.adopt()
        p = self.target / '.agents/skills/workflow-risk-review/SKILL.md'
        original = p.read_bytes()
        p.write_text('Human dependency edit')
        before = self.tracked_bytes()
        run('bootstrap', '--repo', self.target, '--source', self.source, '--apply', expect=1)
        self.assertEqual(p.read_text(), 'Human dependency edit')
        self.assertEqual(self.tracked_bytes(), before)
        p.write_bytes(original)
        extra = p.parent / 'unmanaged.md'
        extra.write_text('Human addition')
        run('bootstrap', '--repo', self.target, '--apply', expect=1)
        run('doctor', '--repo', self.target, expect=1)
        self.assertEqual(extra.read_text(), 'Human addition')
        extra.unlink()
        p.unlink()
        p.symlink_to(self.source / '.agents/skills/workflow-risk-review/SKILL.md')
        run('bootstrap', '--repo', self.target, '--apply', expect=2)

    def test_ignored_dependency_edit_changes_content_identity_and_diagnostics(self):
        self.adopt()
        before = content_identity(self.target)
        p = self.target / '.agents/skills/workflow-risk-review/SKILL.md'
        p.write_text(p.read_text() + 'Changed ignored dependency.\n')
        self.assertEqual(git(self.target, 'status', '--porcelain'), b'')
        after = content_identity(self.target)
        self.assertNotEqual(after['content_digest'], before['content_digest'])
        self.assertTrue(after['dependency_modified'])
        self.assertTrue(after['dirty'])
        run('check', '--repo', self.target, expect=1)
        run('doctor', '--repo', self.target, expect=1)

    def test_fetch_uses_exact_pin_and_denied_fetch_preserves_checkout(self):
        self.adopt()
        self.erase_dependency()
        before = self.tracked_bytes()
        def fake_transport(folder, url, revision):
            self.assertEqual(url, 'https://github.com/canzheng/workflow-skills.git')
            self.assertEqual(revision, self.sha)
            shutil.copytree(self.source, folder, dirs_exist_ok=True)
        argv = ['bootstrap', '--repo', str(self.target), '--apply', '--json']
        with patch.object(dependency, 'fetch_source', side_effect=Conflict('denied fetch')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(argv), 1)
        self.assertEqual(self.tracked_bytes(), before)
        with patch.object(dependency, 'fetch_source', side_effect=fake_transport), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(argv), 0)
        self.assertEqual(self.tracked_bytes(), before)
        commands = []
        def capture(folder, *args):
            commands.append(args)
            return self.sha.encode() if args[:1] == ('rev-parse',) else b''
        with patch.object(dependency, 'git', side_effect=capture):
            dependency.fetch_source(self.base, 'https://github.com/canzheng/workflow-skills.git', self.sha)
        self.assertEqual(commands[1], ('fetch', '--no-tags', '--depth=1', 'https://github.com/canzheng/workflow-skills.git', self.sha))
        self.assertEqual(commands[2], ('checkout', '--detach', '--quiet', self.sha))

    def test_pin_mismatch_invalid_url_and_missing_ignore_policy_are_safe(self):
        self.adopt()
        self.erase_dependency()
        pin = self.target / '.workflow/install-manifest.json'
        original = pin.read_bytes()
        m = json.loads(original)
        m['files']['.agents/skills/workflow-risk-review/SKILL.md'] = '0' * 64
        pin.write_text(json.dumps(m))
        run('bootstrap', '--repo', self.target, '--source', self.source, '--apply', expect=1)
        self.assertFalse((self.target / '.agents/skills/workflow-risk-review').exists())
        m['source_url'] = 'https://user:secret@github.com/fixture/source.git'
        pin.write_text(json.dumps(m))
        result = run('bootstrap', '--repo', self.target, '--source', self.source, '--apply', expect=2)
        self.assertNotIn('user:secret', json.dumps(result))
        pin.write_bytes(original)
        (self.target / '.gitignore').write_text('# Human policy, dependency block removed\n')
        run('bootstrap', '--repo', self.target, '--source', self.source, '--apply', expect=1)

    def test_interrupted_materialization_restores_absence_then_retry_succeeds(self):
        self.adopt()
        self.erase_dependency()
        before = self.tracked_bytes()
        actual = dependency.transaction
        def interrupted(root, changes):
            return actual(root, changes, fail_after=1)
        argv = ['bootstrap', '--repo', str(self.target), '--source', str(self.source), '--apply', '--json']
        with patch.object(dependency, 'transaction', side_effect=interrupted), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(workflow.main(argv), 1)
        self.assertIn('original files restored', out.getvalue())
        self.assertEqual(self.tracked_bytes(), before)
        self.assertFalse(any((self.target / '.agents/skills' / s).exists() for s in SKILLS))
        run(*argv[:-1])
        run('doctor', '--repo', self.target)

    def test_old_tracked_shared_skills_require_explicit_untracking_without_data_loss(self):
        self.adopt()
        pin = self.target / '.workflow/install-manifest.json'
        m = json.loads(pin.read_text())
        m['schema_version'] = 1
        del m['source_url'], m['gitignore_block_hash']
        pin.write_text(json.dumps(m))
        (self.target / '.gitignore').write_text('# Existing user rules\n')
        prefixes = ['.agents/skills/' + s for s in SKILLS]
        git(self.target, 'add', '--', *prefixes)
        commit(self.target)
        before = self.tracked_bytes()
        run(*self.args, '--apply', expect=1)
        self.assertEqual(self.tracked_bytes(), before)
        git(self.target, 'rm', '--cached', '-r', '--', *prefixes)
        run(*self.args, '--apply')
        self.assertTrue(all((self.target / p / 'SKILL.md').exists() for p in prefixes))
        self.assertIn('.agents/skills/project-rules/SKILL.md', git(self.target, 'ls-files').decode())
        run('bootstrap', '--repo', self.target, '--apply')

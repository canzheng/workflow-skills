"""Tracked skill snapshots, explicit migration and read-only startup boundaries."""
import contextlib
import io
import json
import pathlib
import shutil
import subprocess
import unittest
from unittest.mock import patch

import test_setup
import setup as installer
import workflow
from core import IGNORE_START, IGNORE_END, SKILLS, content_identity, digest, git, shared
from test_setup import commit, run


class DependencyBootstrapTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def adopt(self):
        project = self.target / '.agents/skills/project-rules/SKILL.md'
        project.parent.mkdir(parents=True)
        project.write_text('---\nname: project-rules\ndescription: project-owned\n---\nKeep project rules.\n')
        run(*self.args, '--apply')
        commit(self.target)
        return project

    def snapshot(self):
        return ({p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                 if p.is_file() and '.git' not in p.relative_to(self.target).parts},
                (self.target / '.git/index').read_bytes())

    def legacy_ignored(self):
        self.adopt()
        block = IGNORE_START + '\n' + '\n'.join('/.agents/skills/' + s + '/' for s in SKILLS) + '\n' + IGNORE_END
        (self.target / '.gitignore').write_text('# Human ignore\n*.local\n' + block + '\n')
        pin = self.target / '.workflow/install-manifest.json'
        m = json.loads(pin.read_text())
        m['schema_version'] = 2
        m.pop('skill_storage')
        m['gitignore_block_hash'] = digest(block.encode())
        pin.write_text(json.dumps(m, indent=2) + '\n')
        git(self.target, 'rm', '--cached', '-r', '--', *['.agents/skills/' + s for s in SKILLS])
        commit(self.target)
        return pin, block

    def test_fresh_clone_has_all_tracked_skills_without_bootstrap_or_network(self):
        project = self.adopt()
        tracked = git(self.target, 'ls-files', '-z').decode().split('\0')
        expected = {name for name in json.loads((self.target / '.workflow/install-manifest.json').read_text())['files'] if shared(name)}
        self.assertTrue(expected <= set(tracked))
        self.assertIn(project.relative_to(self.target).as_posix(), tracked)
        self.assertFalse((self.target / '.gitignore').exists())
        fresh = self.base / 'fresh clone'
        subprocess.run(['git', 'clone', '--quiet', '--no-local', str(self.target), str(fresh)], check=True)
        for name in expected:
            self.assertEqual((fresh / name).read_bytes(), (self.source / name).read_bytes())
        # Remote removal makes a hidden fetch observable; startup still verifies.
        git(fresh, 'remote', 'remove', 'origin')
        before = (fresh / '.git/index').read_bytes()
        run('check', '--repo', fresh)
        run('doctor', '--repo', fresh)
        self.assertEqual(run('bootstrap', '--repo', fresh, '--apply')['changes'], [])
        self.assertEqual((fresh / '.git/index').read_bytes(), before)
        self.assertEqual(git(fresh, 'status', '--porcelain'), b'')

    def test_unborn_adoption_is_reviewable_then_committed_identity_is_clean(self):
        fresh = self.base / 'unborn'
        test_setup.init(fresh)
        run('setup', '--source', self.source, '--revision', self.sha, '--target', fresh, '--repository', 'fixture/consumer', '--apply')
        report = run('doctor', '--repo', fresh)
        self.assertIsNone(report['content']['revision'])
        self.assertTrue(report['content']['dirty'])
        sha = commit(fresh)
        report = run('doctor', '--repo', fresh)
        self.assertEqual(report['content']['revision'], sha)
        self.assertFalse(report['content']['dirty'])

    def test_missing_tracked_skill_is_not_recreated_even_with_apply_or_source(self):
        self.adopt()
        name = '.agents/skills/workflow-risk-review/SKILL.md'
        (self.target / name).unlink()
        before = self.snapshot()
        for args in [('bootstrap', '--repo', self.target, '--apply'),
                     ('bootstrap', '--repo', self.target, '--source', self.source, '--apply'),
                     ('check', '--repo', self.target), ('doctor', '--repo', self.target)]:
            run(*args, expect=1)
            self.assertEqual(self.snapshot(), before)
        git(self.target, 'restore', '--', name)
        self.assertEqual(run('bootstrap', '--repo', self.target, '--apply')['changes'], [])

    def test_untracked_shared_file_cannot_certify_an_adopted_checkout(self):
        self.adopt()
        name = '.agents/skills/workflow-risk-review/SKILL.md'
        git(self.target, 'rm', '--cached', '--', name)
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            r = run(command, '--repo', self.target, expect=1)
            self.assertIn('not tracked', json.dumps(r))
            self.assertEqual(self.snapshot(), before)

    def test_every_installed_asset_and_project_policy_must_remain_tracked(self):
        self.adopt()
        m = json.loads((self.target / '.workflow/install-manifest.json').read_text())
        required = set(m['files']) | {'.workflow/install-manifest.json', '.workflow/config.json', 'AGENTS.md'}
        for name in sorted(required):
            with self.subTest(path=name):
                git(self.target, 'rm', '--cached', '--', name)
                before = self.snapshot()
                try:
                    for command in ['check', 'doctor', 'bootstrap']:
                        r = run(command, '--repo', self.target, expect=1)
                        self.assertIn('not tracked', json.dumps(r))
                        self.assertEqual(self.snapshot(), before)
                finally:
                    git(self.target, 'restore', '--staged', '--', name)
        run('check', '--repo', self.target)

    def test_broken_staged_bytes_cannot_hide_behind_good_working_tree(self):
        self.adopt()
        m = json.loads((self.target / '.workflow/install-manifest.json').read_text())
        required = set(m['files']) | {'.workflow/install-manifest.json', '.workflow/config.json', 'AGENTS.md'}
        for name in sorted(required):
            with self.subTest(path=name):
                p = self.target / name
                original = p.read_bytes()
                p.write_bytes(b'Broken staged content.\n')
                git(self.target, 'add', '--', name)
                p.write_bytes(original)
                before = self.snapshot()
                try:
                    for command in ['check', 'doctor', 'bootstrap']:
                        r = run(command, '--repo', self.target, expect=1)
                        self.assertIn('Staged workflow', json.dumps(r))
                        self.assertEqual(self.snapshot(), before)
                finally:
                    git(self.target, 'restore', '--staged', '--', name)
        run('check', '--repo', self.target)

    def test_staged_symlinks_and_unmerged_assets_fail_without_mutation(self):
        self.adopt()
        for name in ['tools/workflow/core.py', '.workflow/install-manifest.json',
                     '.workflow/config.json', 'AGENTS.md']:
            with self.subTest(path=name):
                # Index-only replacement leaves the real regular file untouched.
                blob = git(self.target, 'rev-parse', 'HEAD:' + name).decode().strip()
                git(self.target, 'update-index', '--cacheinfo', '120000,' + blob + ',' + name)
                before = self.snapshot()
                try:
                    for command in ['check', 'doctor', 'bootstrap']:
                        r = run(command, '--repo', self.target, expect=1)
                        self.assertIn('Staged workflow', json.dumps(r))
                        self.assertEqual(self.snapshot(), before)
                finally:
                    git(self.target, 'restore', '--staged', '--', name)
        name = 'tools/workflow/core.py'
        blob = git(self.target, 'rev-parse', 'HEAD:' + name).decode().strip()
        subprocess.run(['git', '-C', str(self.target), 'update-index', '--index-info'],
                       input=('0 ' + '0' * 40 + '\t' + name + '\n100644 ' + blob + ' 1\t' + name + '\n').encode(), check=True)
        before = self.snapshot()
        for command in ['check', 'doctor', 'bootstrap']:
            r = run(command, '--repo', self.target, expect=1)
            self.assertIn('Staged workflow', json.dumps(r))
            self.assertEqual(self.snapshot(), before)

    def test_valid_project_policy_changes_remain_independently_verifiable(self):
        self.adopt()
        p = self.target / '.workflow/config.json'
        staged = json.loads(p.read_text())
        staged['openspec'] = 'disabled'
        p.write_text(json.dumps(staged))
        git(self.target, 'add', '--', '.workflow/config.json')
        staged['openspec'] = 'on-demand'
        p.write_text(json.dumps(staged))
        before = self.snapshot()
        for command in ['check', 'doctor', 'bootstrap']:
            run(command, '--repo', self.target)
            self.assertEqual(self.snapshot(), before)

    def test_staged_policy_schema_and_document_references_are_validated(self):
        self.adopt()
        for name, field, value in [('.workflow/install-manifest.json', 'schema_version', 99),
                                   ('.workflow/install-manifest.json', 'source_revision', 'main'),
                                   ('.workflow/config.json', 'verification', {'local': [], 'integration': []}),
                                   ('.workflow/config.json', 'contract', 'docs/missing-staged-contract.md')]:
            with self.subTest(path=name, field=field):
                p = self.target / name
                original = p.read_bytes()
                staged = json.loads(original)
                staged[field] = value
                p.write_text(json.dumps(staged))
                git(self.target, 'add', '--', name)
                p.write_bytes(original)
                before = self.snapshot()
                try:
                    for command in ['check', 'doctor', 'bootstrap']:
                        r = run(command, '--repo', self.target, expect=1)
                        self.assertIn('Staged workflow', json.dumps(r))
                        self.assertEqual(self.snapshot(), before)
                finally:
                    git(self.target, 'restore', '--staged', '--', name)

    def test_staging_new_manifest_without_updated_asset_cannot_certify_commit(self):
        self.adopt()
        name = 'docs/workflow/README.md'
        (self.source / name).write_text('# Updated fixture guidance\n')
        revision = commit(self.source)
        args = self.args.copy()
        args[args.index('--revision') + 1] = revision
        run(*args, '--apply')
        git(self.target, 'add', '--', '.workflow/install-manifest.json')
        before = self.snapshot()
        for command in ['check', 'doctor', 'bootstrap']:
            r = run(command, '--repo', self.target, expect=1)
            self.assertIn('Staged workflow', json.dumps(r))
            self.assertEqual(self.snapshot(), before)
        git(self.target, 'add', '--', name)
        for command in ['check', 'doctor', 'bootstrap']:
            run(command, '--repo', self.target)

    def test_intent_to_add_asset_cannot_certify_staged_update(self):
        self.adopt()
        name = '.agents/skills/workflow-risk-review/references/additional.md'
        (self.source / name).write_text('# Additional fixture guidance\n')
        p = self.source / '.workflow/bundle.json'
        bundle = json.loads(p.read_text())
        bundle['assets'][name] = name
        p.write_text(json.dumps(bundle))
        revision = commit(self.source)
        args = self.args.copy()
        args[args.index('--revision') + 1] = revision
        run(*args, '--apply')
        git(self.target, 'add', '--', '.workflow/install-manifest.json')
        git(self.target, 'add', '-N', '--', name)
        before = self.snapshot()
        for command in ['check', 'doctor', 'bootstrap']:
            r = run(command, '--repo', self.target, expect=1)
            self.assertIn('Staged workflow', json.dumps(r))
            self.assertEqual(self.snapshot(), before)
        git(self.target, 'add', '--', name)
        for command in ['check', 'doctor', 'bootstrap']:
            run(command, '--repo', self.target)

    def test_ignored_provenance_policy_or_runtime_fails_preflight_without_writes(self):
        for name in ['.workflow/install-manifest.json', '.workflow/config.json', 'AGENTS.md',
                     'tools/workflow/core.py', 'docs/workflow/contract.md',
                     '.github/workflows/workflow-v2-verify.yml']:
            with self.subTest(path=name):
                (self.target / '.gitignore').write_text('/' + name + '\n')
                before = self.snapshot()
                for extra in [[], ['--apply']]:
                    r = run(*self.args, *extra, expect=1)
                    self.assertIn('path is ignored', json.dumps(r))
                    self.assertEqual(self.snapshot(), before)
                self.assertFalse((self.target / '.workflow').exists())

        (self.target / '.gitignore').unlink()
        for folder, rule in [('.workflow', 'install-manifest.json'),
                             ('tools/workflow', 'core.py'), ('docs/workflow', 'contract.md')]:
            with self.subTest(nested=folder):
                p = self.target / folder / '.gitignore'
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(rule + '\n')
                before = self.snapshot()
                try:
                    for extra in [[], ['--apply']]:
                        r = run(*self.args, *extra, expect=1)
                        self.assertIn('path is ignored', json.dumps(r))
                        self.assertEqual(self.snapshot(), before)
                finally:
                    p.unlink()

    def test_initial_unstaged_adoption_cannot_hide_its_provenance(self):
        run(*self.args, '--apply')
        (self.target / '.gitignore').write_text('/.workflow/install-manifest.json\n')
        before = self.snapshot()
        for command in ['check', 'doctor', 'bootstrap']:
            r = run(command, '--repo', self.target, expect=1)
            self.assertIn('path is ignored', json.dumps(r))
            self.assertEqual(self.snapshot(), before)

    def test_partial_staging_cannot_bypass_provenance_or_initial_review_exception(self):
        run(*self.args, '--apply')
        run('check', '--repo', self.target)  # Complete unstaged adoption is reviewable.
        git(self.target, 'add', '--', 'tools/workflow/core.py')
        before = self.snapshot()
        for command in ['check', 'doctor', 'bootstrap']:
            run(command, '--repo', self.target, expect=1)
            self.assertEqual(self.snapshot(), before)
        commit(self.target)
        run('check', '--repo', self.target)

    def test_modified_extra_or_symlinked_skills_are_preserved_on_failure(self):
        self.adopt()
        p = self.target / '.agents/skills/workflow-risk-review/SKILL.md'
        original = p.read_bytes()
        p.write_text('Human edit')
        before = self.snapshot()
        run('bootstrap', '--repo', self.target, '--apply', expect=1)
        run('doctor', '--repo', self.target, expect=1)
        self.assertEqual(self.snapshot(), before)
        self.assertTrue(content_identity(self.target)['dependency_modified'])
        p.write_bytes(original)
        extra = p.parent / 'unmanaged.md'
        extra.write_text('Human addition')
        before = self.snapshot()
        run('bootstrap', '--repo', self.target, '--apply', expect=1)
        run('doctor', '--repo', self.target, expect=1)
        self.assertEqual(self.snapshot(), before)
        extra.unlink()
        p.unlink()
        p.symlink_to(self.source / '.agents/skills/workflow-risk-review/SKILL.md')
        run('bootstrap', '--repo', self.target, '--apply', expect=2)
        self.assertTrue(p.is_symlink())

    def test_explicit_ignored_to_tracked_update_removes_only_owned_rules(self):
        pin, block = self.legacy_ignored()
        project = self.target / '.agents/skills/project-rules/SKILL.md'
        before_project = project.read_bytes()
        cp = self.target / '.workflow/config.json'
        c = json.loads(cp.read_text()); c['openspec'] = 'disabled'
        cp.write_text(json.dumps(c))
        before_config = cp.read_bytes()
        index = (self.target / '.git/index').read_bytes()
        run('bootstrap', '--repo', self.target, '--apply', expect=1)
        preview = run(*self.args)
        self.assertIn('.gitignore', preview['changes'])
        self.assertIn(block, (self.target / '.gitignore').read_text())
        run(*self.args, '--apply')
        self.assertEqual((self.target / '.gitignore').read_text(), '# Human ignore\n*.local\n')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        self.assertEqual(cp.read_bytes(), before_config)
        self.assertEqual(project.read_bytes(), before_project)
        self.assertEqual(json.loads(pin.read_text())['schema_version'], 3)
        # Deliberate staging/commit belongs to the caller, never setup/startup.
        commit(self.target)
        self.assertEqual(run('bootstrap', '--repo', self.target, '--apply')['changes'], [])
        self.assertEqual(run(*self.args, '--apply')['changes'], [])
        run('doctor', '--repo', self.target)

    def test_legacy_migration_conflicts_and_rollback_preserve_bytes_and_index(self):
        pin, block = self.legacy_ignored()
        ignore = self.target / '.gitignore'
        ignore.write_text(ignore.read_text().replace('/.agents/skills/workflow-risk-review/', '/.agents/skills/'))
        before = self.snapshot()
        run(*self.args, '--apply', expect=1)
        self.assertEqual(self.snapshot(), before)
        ignore.write_text('# Human ignore\n*.local\n' + block + '\n')
        p = self.target / '.agents/skills/workflow-risk-review/SKILL.md'
        p.write_text('Unreviewed dependency edit')
        before = self.snapshot()
        run(*self.args, '--apply', expect=1)
        self.assertEqual(self.snapshot(), before)
        p.write_bytes((self.source / '.agents/skills/workflow-risk-review/SKILL.md').read_bytes())
        before = self.snapshot()
        actual = installer.transaction
        def interrupted(root, changes):
            return actual(root, changes, fail_after=1)
        with patch.object(installer, 'transaction', side_effect=interrupted), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main([*map(str, self.args), '--apply', '--json']), 1)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(json.loads(pin.read_text())['schema_version'], 2)
        run(*self.args, '--apply')

    def test_broad_nested_or_info_excludes_cannot_hide_any_skills(self):
        self.adopt()
        for file, rule in [('.gitignore', '/.agents/skills/\n'),
                           ('.agents/skills/.gitignore', 'workflow-risk-review/\n'),
                           ('.git/info/exclude', '/.agents/skills/workflow-risk-review/\n')]:
            with self.subTest(file=file):
                p = self.target / file
                original = p.read_bytes() if p.exists() else None
                p.write_text(rule)
                before = self.snapshot()
                for command in ['bootstrap', 'check', 'doctor']:
                    r = run(command, '--repo', self.target, expect=1)
                    self.assertIn('path is ignored', json.dumps(r))
                    self.assertEqual(self.snapshot(), before)
                run(*self.args, '--apply', expect=1)
                self.assertEqual(self.snapshot(), before)
                if original is None: p.unlink()
                else: p.write_bytes(original)

    def test_pin_mismatch_invalid_source_and_schema_fail_without_writes(self):
        self.adopt()
        pin = self.target / '.workflow/install-manifest.json'
        original = pin.read_bytes()
        m = json.loads(original)
        m['files']['.agents/skills/workflow-risk-review/SKILL.md'] = '0' * 64
        pin.write_text(json.dumps(m))
        before = self.snapshot()
        run('bootstrap', '--repo', self.target, '--source', self.source, '--apply', expect=1)
        self.assertEqual(self.snapshot(), before)
        m['source_url'] = 'https://user:secret@github.com/fixture/source.git'
        pin.write_text(json.dumps(m))
        r = run('bootstrap', '--repo', self.target, '--apply', expect=2)
        self.assertNotIn('user:secret', json.dumps(r))
        m = json.loads(original); m['skill_storage'] = 'ignored'
        pin.write_text(json.dumps(m))
        run('bootstrap', '--repo', self.target, '--apply', expect=2)

    def test_schema_one_tracked_snapshot_updates_without_untracking(self):
        self.adopt()
        pin = self.target / '.workflow/install-manifest.json'
        m = json.loads(pin.read_text()); m['schema_version'] = 1
        del m['source_url'], m['skill_storage']
        pin.write_text(json.dumps(m)); commit(self.target)
        index = (self.target / '.git/index').read_bytes()
        run(*self.args, '--apply')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        self.assertEqual(json.loads(pin.read_text())['skill_storage'], 'tracked')
        self.assertTrue((self.target / '.agents/skills/project-rules/SKILL.md').is_file())
        run('bootstrap', '--repo', self.target)

"""Default ignored exact-pin dependencies with preserved tracked policy/index."""
import json
import os
import contextlib
import io
import subprocess
import unittest
from unittest.mock import patch

import test_setup
import bootstrap
import workflow
from core import SKILLS, git, shared, dependency
from test_setup import commit, run


class IgnoredDependencyTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def ignored_adopt(self):
        args = self.args.copy()
        del args[-2:]
        project = self.target / '.agents/skills/project-rules/SKILL.md'
        project.parent.mkdir(parents=True, exist_ok=True)
        project.write_text('---\nname: project-rules\ndescription: Human rules\n---\nKeep me.\n')
        run(*args, '--apply')
        commit(self.target)
        return args

    def snapshot(self, root=None):
        root = root or self.target
        return ({p.relative_to(root): p.read_bytes() for p in root.rglob('*')
                 if p.is_file() and '.git' not in p.relative_to(root).parts},
                (root / '.git/index').read_bytes() if (root / '.git/index').exists() else None)

    def fresh(self):
        self.ignored_adopt()
        fresh = self.base / 'fresh consumer'
        subprocess.run(['git', 'clone', '--quiet', '--no-local', str(self.target), str(fresh)], check=True)
        git(fresh, 'config', 'user.name', 'Fixture')
        git(fresh, 'config', 'user.email', 'test@example.invalid')
        return fresh

    def test_default_setup_ignores_only_shared_dirs_preserves_index_and_repeats(self):
        args = self.args[:-2]
        (self.target / '.gitignore').write_text('# Human rules\n*.local\n')
        before = self.snapshot()
        preview = run(*args)
        self.assertIn('.gitignore', preview['changes'])
        self.assertEqual(self.snapshot(), before)
        self.ignored_adopt()
        policy = (self.target / '.gitignore').read_text()
        self.assertTrue(policy.startswith('# Human rules\n*.local\n'))
        self.assertNotIn('\n/.agents/\n', policy)
        self.assertNotIn('\n/.agents/skills/\n', policy)
        for skill in SKILLS:
            self.assertEqual(git(self.target, 'ls-files', '--', '.agents/skills/' + skill), b'')
            self.assertIn('/.agents/skills/' + skill + '/', policy)
        self.assertIn('/.agents/tools/workflow/', policy)
        self.assertEqual(git(self.target, 'ls-files', '--', '.agents/tools/workflow'), b'')
        self.assertIn(b'project-rules', git(self.target, 'ls-files', '--', '.agents/skills'))
        m = json.loads((self.target / '.workflow/install-manifest.json').read_text())
        self.assertEqual((m['schema_version'], m['skill_storage'], m['source_revision']), (5, 'ignored', self.sha))
        before = self.snapshot()
        self.assertEqual(run(*args, '--apply')['changes'], [])
        run('check', '--repo', self.target)
        run('doctor', '--repo', self.target)
        self.assertEqual(self.snapshot(), before)

    def test_fresh_clone_dry_run_then_materialize_exact_pin_and_offline_repeat(self):
        fresh = self.fresh()
        manifest = json.loads((fresh / '.workflow/install-manifest.json').read_text())
        expected = {p for p in manifest['files'] if dependency(p, manifest)}
        self.assertTrue(all(not (fresh / p).exists() for p in expected))
        run('check', '--repo', fresh, expect=1)
        before = self.snapshot(fresh)
        report = run('bootstrap', '--repo', fresh, '--source', self.source)
        self.assertEqual(set(report['changes']), expected)
        self.assertEqual(self.snapshot(fresh), before)
        run('bootstrap', '--repo', fresh, '--source', self.source, '--apply')
        self.assertEqual((fresh / '.git/index').read_bytes(), before[1])
        mapping = {dest: src for src, dest in json.loads((self.source / '.workflow/bundle.json').read_text())['assets'].items()}
        self.assertTrue(all((fresh / p).read_bytes() == (self.source / mapping[p]).read_bytes() for p in expected))
        git(fresh, 'remote', 'remove', 'origin')
        before = self.snapshot(fresh)
        self.assertEqual(run('bootstrap', '--repo', fresh, '--apply')['changes'], [])
        run('check', '--repo', fresh)
        run('doctor', '--repo', fresh)
        self.assertEqual(self.snapshot(fresh), before)
        self.assertEqual(git(fresh, 'status', '--porcelain'), b'')

    def test_network_materialization_fetches_commit_not_latest(self):
        fresh = self.fresh()
        path = '.agents/skills/workflow-risk-review/SKILL.md'
        expected = (self.source / path).read_bytes()
        (self.source / path).write_bytes(expected + b'Later content must not install.\n')
        self.assertNotEqual(commit(self.source), self.sha)
        index = (fresh / '.git/index').read_bytes()
        # Process-local Git URL mapping exercises a real fetch with no external token.
        env = dict(os.environ, GIT_CONFIG_COUNT='1',
                   GIT_CONFIG_KEY_0='url.' + self.source.as_uri() + '.insteadOf',
                   GIT_CONFIG_VALUE_0='https://github.com/canzheng/workflow-skills.git')
        with patch.dict(os.environ, env):
            run('bootstrap', '--repo', fresh, '--apply')
        self.assertEqual((fresh / path).read_bytes(), expected)
        self.assertEqual((fresh / '.git/index').read_bytes(), index)
        self.assertEqual(json.loads((fresh / '.workflow/install-manifest.json').read_text())['source_revision'], self.sha)

    def test_missing_revision_fetch_fails_without_writes_or_latest_fallback(self):
        fresh = self.fresh()
        manifest = fresh / '.workflow/install-manifest.json'
        m = json.loads(manifest.read_text()); m['source_revision'] = '0' * 40
        manifest.write_text(json.dumps(m)); commit(fresh)
        before = self.snapshot(fresh)
        env = dict(os.environ, GIT_CONFIG_COUNT='1',
                   GIT_CONFIG_KEY_0='url.' + self.source.as_uri() + '.insteadOf',
                   GIT_CONFIG_VALUE_0='https://github.com/canzheng/workflow-skills.git')
        with patch.dict(os.environ, env):
            run('bootstrap', '--repo', fresh, '--apply', expect=2)
        self.assertEqual(self.snapshot(fresh), before)

    def test_modified_extra_symlink_and_project_edits_block_before_materialization(self):
        self.ignored_adopt()
        name = '.agents/skills/workflow-risk-review/SKILL.md'
        p = self.target / name; original = p.read_bytes()
        for fault in ['modified', 'extra', 'symlink', 'project']:
            with self.subTest(fault=fault):
                extra = p.parent / 'human.md'
                project = self.target / 'docs/workflow/README.md'; project_bytes = project.read_bytes()
                p.write_bytes(original)
                if fault == 'modified': p.write_text('Human dependency edit')
                elif fault == 'extra': extra.write_text('Human addition')
                elif fault == 'symlink':
                    p.unlink(); p.symlink_to(self.source / name)
                else: project.write_text('Human project edit')
                index = (self.target / '.git/index').read_bytes()
                run('bootstrap', '--repo', self.target, '--source', self.source, '--apply', expect=2 if fault == 'symlink' else 1)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                if fault == 'symlink': self.assertTrue(p.is_symlink()); p.unlink()
                elif fault == 'modified': self.assertEqual(p.read_text(), 'Human dependency edit')
                elif fault == 'extra': self.assertEqual(extra.read_text(), 'Human addition'); extra.unlink()
                else: self.assertEqual(project.read_text(), 'Human project edit')
                p.write_bytes(original); project.write_bytes(project_bytes)

    def test_force_tracked_dependency_is_rejected_without_mutation(self):
        self.ignored_adopt()
        name = '.agents/skills/workflow-risk-review/SKILL.md'
        git(self.target, 'add', '-f', '--', name)
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            report = run(command, '--repo', self.target, expect=1)
            self.assertIn('remains tracked', json.dumps(report))
            self.assertEqual(self.snapshot(), before)

    def test_newly_staged_initial_policy_requires_complete_adoption(self):
        for name in ['AGENTS.md', '.workflow/config.json', '.gitignore']:
            for existing in (False, True) if name in ('AGENTS.md', '.gitignore') else (False,):
                with self.subTest(path=name, preexisting=existing):
                    self.target = self.base / ('initial-' + name.replace('/', '-') + str(existing))
                    test_setup.init(self.target)
                    if existing:
                        (self.target / name).write_text('Preserve existing human policy.\n')
                        commit(self.target)
                    args = self.args[:-2]
                    args[args.index('--target') + 1] = self.target
                    run(*args, '--apply')
                    before = self.snapshot()
                    run('check', '--repo', self.target)
                    self.assertEqual(self.snapshot(), before)
                    git(self.target, 'add', '--', name)
                    before = self.snapshot()
                    for command in ['check', 'doctor', 'bootstrap']:
                        report = run(command, '--repo', self.target, expect=1)
                        self.assertIn('not tracked', json.dumps(report))
                        self.assertEqual(self.snapshot(), before)
                    commit(self.target)
                    run('check', '--repo', self.target)

    def test_runtime_dependencies_reject_edits_extras_and_tracking(self):
        args = self.ignored_adopt()
        p = self.target / '.agents/tools/workflow/core.py'
        original = p.read_bytes()
        for fault in ['bytes', 'extra', 'tracked']:
            with self.subTest(fault=fault):
                extra = p.parent / 'human.py'
                if fault == 'bytes':
                    p.write_bytes(b'Human runtime edit\n')
                elif fault == 'extra':
                    extra.write_bytes(b'Human runtime addition\n')
                else:
                    git(self.target, 'add', '-f', '--', str(p.relative_to(self.target)))
                before = self.snapshot()
                for command in ['bootstrap', 'check', 'doctor']:
                    run(command, '--repo', self.target, expect=1)
                    self.assertEqual(self.snapshot(), before)
                run(*args, '--apply', expect=1)
                self.assertEqual(self.snapshot(), before)
                if fault == 'tracked':
                    git(self.target, 'rm', '--cached', '--', str(p.relative_to(self.target)))
                if extra.exists():
                    extra.unlink()
                p.write_bytes(original)

    def test_fresh_setup_preserves_all_index_owned_deletions(self):
        from core import PROJECT_FILES
        assets = json.loads((self.source / '.workflow/bundle.json').read_text())['assets'].values()
        names = sorted({name for name in assets if not shared(name)
                        and not name.startswith('.agents/tools/workflow/')} | PROJECT_FILES | {'.gitignore'})
        for i, name in enumerate(names):
            for state in ['staged', 'committed', 'removed-index']:
                with self.subTest(path=name, state=state):
                    self.target = self.base / ('deleted-owned-' + str(i) + '-' + state)
                    test_setup.init(self.target)
                    (self.target / 'baseline').write_text('Human baseline\n')
                    commit(self.target)
                    p = self.target / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(b'Human indexed content\n')
                    git(self.target, 'add', '--', name)
                    if state != 'staged':
                        git(self.target, 'commit', '-qm', 'Fixture existing owned destination')
                    if state == 'removed-index':
                        git(self.target, 'rm', '--cached', '--', name)
                    p.unlink()
                    before = self.snapshot()
                    args = self.args[:-2]
                    args[args.index('--target') + 1] = self.target
                    for flags in [[], ['--apply']]:
                        with self.subTest(flags=flags):
                            report = run(*args, *flags, expect=1)
                            self.assertIn('indexed', json.dumps(report).lower())
                            self.assertEqual(self.snapshot(), before)

    def test_project_tools_remain_trackable_in_working_and_staged_policy(self):
        self.ignored_adopt()
        name = '.agents/tools/project-check/check.py'
        p = self.target / name
        p.parent.mkdir(parents=True)
        p.write_bytes(b'Project-owned tool\n')
        commit(self.target)
        policy = self.target / '.agents/tools/project-check/.gitignore'
        policy.write_bytes(b'*\n')
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            report = run(command, '--repo', self.target, expect=1)
            self.assertIn('skill/tool path is ignored', json.dumps(report))
            self.assertEqual(self.snapshot(), before)
        git(self.target, 'add', '-f', '--', str(policy.relative_to(self.target)))
        policy.unlink()
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            report = run(command, '--repo', self.target, expect=1)
            self.assertIn('Staged workflow', json.dumps(report))
            self.assertEqual(self.snapshot(), before)
        git(self.target, 'restore', '--staged', '--', str(policy.relative_to(self.target)))
        run('check', '--repo', self.target)

    def test_setup_update_rejects_tracked_ignored_dependency_before_writes(self):
        self.assert_rejected_setup_update(committed=False)

    def test_fresh_setup_rejects_deleted_indexed_shared_paths_before_writes(self):
        args = self.args[:-2]
        paths = ['.agents/skills/' + skill + '/SKILL.md' for skill in SKILLS]
        paths += ['.agents/skills/workflow-risk-review/references/human.md',
                  '.agents/skills/workflow-deliver-issue',
                  '.agents/tools/workflow/core.py', '.agents/tools/workflow']
        for i, name in enumerate(paths):
            for committed in (False, True):
                with self.subTest(path=name, committed=committed):
                    self.target = self.base / ('indexed-shared-' + str(i) + '-' + str(committed))
                    test_setup.init(self.target)
                    args = self.args[:-2]
                    args[args.index('--target') + 1] = self.target
                    p = self.target / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(b'Indexed human content\n')
                    git(self.target, 'add', '--', name)
                    if committed:
                        git(self.target, 'commit', '-qm', 'Fixture existing shared path')
                    p.unlink()
                    before = self.snapshot()
                    for flags in ([], ['--apply']):
                        with self.subTest(flags=flags):
                            report = run(*args, *flags, expect=1)
                            self.assertIn('remains tracked', json.dumps(report))
                            self.assertEqual(self.snapshot(), before)
                    git(self.target, 'rm', '--cached', '--', name)
        before = self.snapshot()
        run(*args, '--apply')
        self.assertEqual((self.target / '.git/index').read_bytes(), before[1])
        self.assertTrue(all((self.target / name).is_file() for name in paths[:3]))

    def test_setup_update_rejects_committed_ignored_dependency_before_writes(self):
        self.assert_rejected_setup_update(committed=True)

    def assert_rejected_setup_update(self, committed):
        args = self.ignored_adopt()
        name = '.agents/skills/workflow-risk-review/SKILL.md'
        git(self.target, 'add', '-f', '--', name)
        if committed:
            git(self.target, 'commit', '-qm', 'Fixture invalid tracked dependency')
        old = (self.target / name).read_bytes()
        (self.source / name).write_bytes(old + b'New pinned skill content.\n')
        revision = commit(self.source)
        args = list(args)
        args[args.index('--revision') + 1] = revision
        before = self.snapshot()
        for flags in [[], ['--apply']]:
            with self.subTest(flags=flags):
                report = run(*args, *flags, expect=1)
                self.assertIn('remains tracked', json.dumps(report))
                self.assertEqual(self.snapshot(), before)
        git(self.target, 'rm', '--cached', '--', name)
        index = (self.target / '.git/index').read_bytes()
        run(*args, '--apply')
        self.assertEqual((self.target / name).read_bytes(), old + b'New pinned skill content.\n')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        commit(self.target)
        run('check', '--repo', self.target)

    def test_staged_nested_ignores_are_checked_without_working_tree_copies(self):
        self.ignored_adopt()
        for name, policy in [('.agents/.gitignore', '/skills/\n'),
                             ('.agents/skills/.gitignore', '/project-rules/\n'),
                             ('.agents/skills/project-rules/.gitignore', '*\n'),
                             ('.github/.gitignore', '/workflows/\n'),
                             ('docs/workflow/.gitignore', '/README.md\n')]:
            with self.subTest(path=name):
                p = self.target / name
                p.write_text(policy)
                git(self.target, 'add', '-f', '--', name)
                p.unlink()
                before = self.snapshot()
                try:
                    for command in ['bootstrap', 'check', 'doctor']:
                        report = run(command, '--repo', self.target, expect=1)
                        self.assertIn('Staged workflow', json.dumps(report))
                        self.assertEqual(self.snapshot(), before)
                finally:
                    git(self.target, 'restore', '--staged', '--', name)

    def test_staged_new_project_skill_is_checked_against_index_only_ignore(self):
        self.ignored_adopt()
        project = self.target / '.agents/skills/new-project/SKILL.md'
        project.parent.mkdir()
        project.write_text('Human project policy.\n')
        policy = self.target / '.agents/skills/.gitignore'
        policy.write_text('/new-project/\n')
        git(self.target, 'add', '-f', '--', str(project.relative_to(self.target)), str(policy.relative_to(self.target)))
        project.unlink(); project.parent.rmdir(); policy.unlink()
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            report = run(command, '--repo', self.target, expect=1)
            self.assertIn('Staged workflow', json.dumps(report))
            self.assertEqual(self.snapshot(), before)

    def test_staged_nested_policy_modes_and_valid_policy_are_preserved(self):
        self.ignored_adopt()
        policy = self.target / '.agents/.gitignore'
        policy.write_text('# Indexed human rules\n*.local\n')
        git(self.target, 'add', '--', '.agents/.gitignore')
        policy.write_text('# Different working policy\n*.tmp\n')
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            run(command, '--repo', self.target)
            self.assertEqual(self.snapshot(), before)
        oid = git(self.target, 'hash-object', '-w', '--stdin').strip().decode()
        git(self.target, 'update-index', '--cacheinfo', '120000,' + oid + ',.agents/.gitignore')
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            report = run(command, '--repo', self.target, expect=1)
            self.assertIn('not a regular file', json.dumps(report))
            self.assertEqual(self.snapshot(), before)

    def test_corrupt_staged_policy_cannot_hide_behind_good_working_tree(self):
        self.ignored_adopt()
        for name in ['.gitignore', '.workflow/install-manifest.json', '.workflow/config.json',
                     'AGENTS.md', 'docs/workflow/README.md']:
            with self.subTest(path=name):
                p = self.target / name; original = p.read_bytes()
                p.write_text('Broken staged policy\n'); git(self.target, 'add', '--', name)
                p.write_bytes(original); before = self.snapshot()
                try:
                    for command in ['bootstrap', 'check', 'doctor']:
                        report = run(command, '--repo', self.target, expect=1)
                        self.assertIn('Staged workflow', json.dumps(report))
                        self.assertEqual(self.snapshot(), before)
                finally: git(self.target, 'restore', '--staged', '--', name)

    def test_staged_broad_ignore_is_rejected_with_intact_owned_block(self):
        self.ignored_adopt()
        p = self.target / '.gitignore'; original = p.read_bytes()
        p.write_bytes(original + b'/.agents/skills/\n')
        git(self.target, 'add', '--', '.gitignore'); p.write_bytes(original)
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            report = run(command, '--repo', self.target, expect=1)
            self.assertIn('Staged workflow', json.dumps(report))
            self.assertEqual(self.snapshot(), before)

    def test_interrupted_materialization_restores_missing_state_and_index(self):
        fresh = self.fresh(); before = self.snapshot(fresh)
        actual = bootstrap.transaction
        with patch.object(bootstrap, 'transaction', side_effect=lambda r, c: actual(r, c, fail_after=1)), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(['bootstrap', '--repo', str(fresh), '--source',
                                           str(self.source), '--apply', '--json']), 1)
        self.assertEqual(self.snapshot(fresh), before)
        run('bootstrap', '--repo', fresh, '--source', self.source, '--apply')

    def test_broad_ignore_cannot_hide_project_skills_and_modified_block_conflicts(self):
        self.ignored_adopt()
        p = self.target / '.gitignore'; original = p.read_text()
        p.write_text(original + '/.agents/skills/\n')
        before = self.snapshot()
        for command in ['bootstrap', 'check', 'doctor']:
            run(command, '--repo', self.target, expect=1)
            self.assertEqual(self.snapshot(), before)
        p.write_text(original.replace('/.agents/skills/workflow-risk-review/', '/.agents/skills/'))
        before = self.snapshot()
        run(*self.args[:-2], '--apply', expect=1)
        self.assertEqual(self.snapshot(), before)

    def test_tracked_migration_requires_explicit_untracking_and_preserves_index(self):
        run(*self.args, '--apply'); commit(self.target)
        index = (self.target / '.git/index').read_bytes()
        run(*self.args[:-2], '--apply')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        run('check', '--repo', self.target, expect=1)
        git(self.target, 'rm', '--cached', '-r', '--', *['.agents/skills/' + s for s in SKILLS], '.agents/tools/workflow')
        commit(self.target)
        run('check', '--repo', self.target)
        self.assertTrue(all((self.target / ('.agents/skills/' + s + '/SKILL.md')).exists() for s in SKILLS))

    def test_uninstall_removes_only_owned_ignore_block_and_preserves_human_rules(self):
        self.ignored_adopt()
        p = self.target / '.gitignore'; p.write_text(p.read_text() + '# More human rules\n*.tmp\n')
        before_index = (self.target / '.git/index').read_bytes()
        run('setup', '--target', self.target, '--uninstall', '--apply')
        self.assertEqual(p.read_text(), '# More human rules\n*.tmp\n')
        self.assertEqual((self.target / '.git/index').read_bytes(), before_index)
        self.assertTrue((self.target / '.agents/skills/project-rules/SKILL.md').exists())

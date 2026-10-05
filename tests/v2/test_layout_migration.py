"""Real index ownership and executable migration documentation, including old pins."""
import json
import pathlib
import shlex
import subprocess
import unittest

import test_setup
from core import IGNORE_START, IGNORE_END, LEGACY_RUNTIME_PREFIX, RUNTIME_PREFIX, SKILLS, Conflict, staged_installation, digest, git
from test_setup import commit, init, run


class LayoutMigrationTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def snapshot(self, root):
        index = root / '.git/index'
        return ({p.relative_to(root): p.read_bytes() for p in root.rglob('*')
                 if p.is_file() and '.git' not in p.relative_to(root).parts},
                index.read_bytes() if index.exists() else None)

    def args_for(self, root, storage='ignored'):
        return ['setup', '--source', self.source, '--revision', self.sha,
                '--target', root, '--repository', 'fixture/consumer', '--dependency-storage', storage]

    def old_adoption(self, schema, label):
        bundle = self.source / '.workflow/bundle.json'
        spec = json.loads(bundle.read_text())
        spec['assets'] = {src: dest.replace(RUNTIME_PREFIX, LEGACY_RUNTIME_PREFIX, 1)
                          for src, dest in spec['assets'].items()}
        bundle.write_text(json.dumps(spec))
        self.sha = (commit(self.source) if git(self.source, 'status', '--porcelain') else
                    git(self.source, 'rev-parse', 'HEAD').decode().strip())
        root = self.base / label
        init(root)
        (root / 'README.md').write_text('Human project.\n')
        commit(root)
        run(*self.args_for(root, 'tracked'), '--apply')
        # Project tools may be added beside the legacy tracked runtime.
        human = root / 'tools/workflow/project-helper.py'
        human.write_text('print("project-owned")\n')
        commit(root)
        if schema == 4:
            pin = root / '.workflow/install-manifest.json'
            m = json.loads(pin.read_text())
            block = IGNORE_START + '\n' + '\n'.join('/.agents/skills/' + s + '/' for s in SKILLS) + '\n' + IGNORE_END
            (root / '.gitignore').write_text(block + '\n')
            m.update(schema_version=4, skill_storage='ignored', gitignore_block_hash=digest(block.encode()))
            pin.write_text(json.dumps(m, indent=2) + '\n')
            commit(root)
            git(root, 'rm', '--cached', '-r', '--', *['.agents/skills/' + s for s in SKILLS])
            commit(root)
        spec['assets'] = {src: dest.replace(LEGACY_RUNTIME_PREFIX, RUNTIME_PREFIX, 1)
                          if src.startswith(LEGACY_RUNTIME_PREFIX) else dest
                          for src, dest in spec['assets'].items()}
        bundle.write_text(json.dumps(spec))
        self.sha = commit(self.source)
        return root

    def migrate(self, root, storage='ignored'):
        before_index = (root / '.git/index').read_bytes()
        run(*self.args_for(root, storage), '--apply')
        self.assertEqual((root / '.git/index').read_bytes(), before_index)
        cp = root / '.workflow/config.json'
        c = json.loads(cp.read_text())
        c['verification']['local'][0][1] = RUNTIME_PREFIX + 'workflow.py'
        cp.write_text(json.dumps(c, indent=2) + '\n')
        return json.loads((root / '.workflow/install-manifest.json').read_text())

    def stage_project(self, root, m):
        names = [name for name in m['files'] if m['schema_version'] != 5 or
                 not name.startswith(('.agents/skills/', RUNTIME_PREFIX))]
        names += ['.workflow/install-manifest.json', '.workflow/config.json', 'AGENTS.md']
        if (root / '.gitignore').exists():
            names.append('.gitignore')
        git(root, 'add', '--', *names)

    def test_each_retired_runtime_index_entry_blocks_partial_migration(self):
        for schema in (3, 4):
            for storage in ('ignored', 'tracked'):
                with self.subTest(schema=schema, storage=storage):
                    root = self.old_adoption(schema, 'old-' + str(schema) + '-' + storage)
                    m = self.migrate(root, storage)
                    if storage == 'ignored' and schema == 3:
                        git(root, 'rm', '--cached', '-r', '--', *['.agents/skills/' + s for s in SKILLS])
                    self.stage_project(root, m)
                    legacy = [LEGACY_RUNTIME_PREFIX + pathlib.PurePosixPath(n).name for n in m['files']
                              if n.startswith(RUNTIME_PREFIX)]
                    for name in legacy:
                        git(root, 'restore', '--staged', '--', *legacy)
                        git(root, 'add', '-u', '--', *legacy)
                        git(root, 'restore', '--staged', '--', name)
                        before = self.snapshot(root)
                        for command in ['check', 'doctor', 'bootstrap']:
                            result = run(command, '--repo', root, expect=1)
                            self.assertIn('Retired workflow runtime', json.dumps(result))
                            self.assertEqual(self.snapshot(root), before)
                        for extra in ([], ['--apply']):
                            run(*self.args_for(root, storage), *extra, expect=1)
                            self.assertEqual(self.snapshot(root), before)
                    git(root, 'restore', '--staged', '--', *legacy)
                    git(root, 'add', '-u', '--', *legacy)
                    run('check', '--repo', root, '--run-local')
                    self.assertEqual(run('bootstrap', '--repo', root, '--apply')['changes'], [])
                    self.assertIn('tools/workflow/project-helper.py', git(root, 'ls-files').decode())
                    self.assertEqual((root / 'tools/workflow/project-helper.py').read_text(), 'print("project-owned")\n')

    def test_index_owned_destination_ancestors_preserve_unrelated_deletions(self):
        spec = json.loads((self.source / '.workflow/bundle.json').read_text())
        paths = set(spec['assets'].values()) | {'.workflow/config.json', '.workflow/install-manifest.json', 'AGENTS.md', '.gitignore'}
        ancestors = sorted({p.as_posix() for n in paths for p in pathlib.PurePosixPath(n).parents if p.as_posix() != '.'})
        for i, name in enumerate(ancestors):
            for state in ('staged', 'committed', 'removed-from-index'):
                for storage in ('ignored', 'tracked'):
                    with self.subTest(path=name, state=state, storage=storage):
                        root = self.base / ('ancestor-' + str(i) + state + storage)
                        init(root)
                        p = root / name
                        p.parent.mkdir(parents=True, exist_ok=True)
                        p.write_bytes(b'Unrelated indexed ancestor.\n')
                        git(root, 'add', '--', name)
                        if state != 'staged':
                            commit(root)
                        p.unlink()
                        if state == 'removed-from-index':
                            git(root, 'rm', '--cached', '--', name)
                        before = self.snapshot(root)
                        for extra in ([], ['--apply']):
                            result = run(*self.args_for(root, storage), *extra, expect=1)
                            if state == 'removed-from-index':
                                self.assertIn('ancestor', json.dumps(result).lower())
                            self.assertEqual(self.snapshot(root), before)

    def test_fresh_adoption_rejects_reserved_legacy_runtime_without_writes(self):
        for i, filename in enumerate(('core.py', 'bootstrap.py', 'setup.py', 'workflow.py', 'checks.py', 'records.py', 'migration.py')):
            for storage in ('ignored', 'tracked'):
                root = self.base / ('reserved-' + str(i) + storage)
                init(root)
                p = root / LEGACY_RUNTIME_PREFIX / filename
                p.parent.mkdir(parents=True)
                p.write_bytes(b'Human legacy-name content.\n')
                commit(root)
                p.unlink()
                git(root, 'rm', '--cached', '--', p.relative_to(root).as_posix())
                before = self.snapshot(root)
                for extra in ([], ['--apply']):
                    result = run(*self.args_for(root, storage), *extra, expect=1)
                    self.assertIn('legacy runtime', json.dumps(result).lower())
                    self.assertEqual(self.snapshot(root), before)

    def test_documented_untrack_command_works_for_old_and_new_layouts(self):
        docs = [test_setup.ROOT / n for n in ('docs/operations.md', 'templates/consumer/operations.md')]
        commands = [next(line for line in p.read_text().splitlines() if line.startswith('git rm --cached')) for p in docs]
        self.assertEqual(commands[0], commands[1])
        for schema in (3, 4):
            root = self.old_adoption(schema, 'documented-' + str(schema))
            m = self.migrate(root)
            result = subprocess.run(shlex.split(commands[0]), cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            git(root, 'add', '-u', '--', LEGACY_RUNTIME_PREFIX.rstrip('/'))
            self.stage_project(root, m)
            run('check', '--repo', root, '--run-local')
            self.assertFalse(any(n.startswith(('.agents/skills/workflow-', RUNTIME_PREFIX))
                                 for n in git(root, 'ls-files').decode().splitlines()))
        # New-layout tracked compatibility actually indexes the runtime path.
        root = self.base / 'documented-new-layout'
        init(root)
        run(*self.args_for(root, 'tracked'), '--apply')
        commit(root)
        m = self.migrate(root)
        result = subprocess.run(shlex.split(commands[0]), cwd=root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.stage_project(root, m)
        run('check', '--repo', root, '--run-local')


    def test_mixed_runtime_source_and_provenance_fail_before_writes(self):
        bundle = self.source / '.workflow/bundle.json'
        spec = json.loads(bundle.read_text())
        extra = 'tools/workflow/legacy-core.py'
        (self.source / extra).write_bytes((self.source / 'tools/workflow/core.py').read_bytes())
        spec['assets'][extra] = 'tools/workflow/core.py'
        bundle.write_text(json.dumps(spec))
        self.sha = commit(self.source)
        before = self.snapshot(self.target)
        for command in ['setup', 'install-skills']:
            target = self.target if command == 'setup' else self.base / 'isolated-skills'
            for flags in ([], ['--apply']):
                args = self.args_for(target) if command == 'setup' else [command, '--source', self.source,
                       '--revision', self.sha, '--target', target]
                report = run(*args, *flags, expect=2)
                self.assertIn('Mixed legacy/new', json.dumps(report))
                self.assertEqual(self.snapshot(self.target), before)
                if command == 'install-skills':
                    self.assertFalse(target.exists())
        spec['assets'].pop(extra)
        bundle.write_text(json.dumps(spec))
        self.sha = commit(self.source)
        run(*self.args_for(self.target), '--apply')
        commit(self.target)
        pin = self.target / '.workflow/install-manifest.json'
        m = json.loads(pin.read_text())
        m['files']['tools/workflow/core.py'] = '0' * 64
        pin.write_text(json.dumps(m, indent=2) + '\n')
        before = self.snapshot(self.target)
        for command in ['check', 'doctor', 'bootstrap']:
            report = run(command, '--repo', self.target, expect=2)
            self.assertIn('Mixed legacy/new', json.dumps(report))
            self.assertEqual(self.snapshot(self.target), before)

    def test_index_only_dependency_ancestor_files_cannot_certify_bootstrap(self):
        run(*self.args_for(self.target), '--apply')
        commit(self.target)
        oid = git(self.target, 'rev-parse', 'HEAD:AGENTS.md').decode().strip()
        for name in ['.agents', '.agents/tools', '.agents/skills']:
            with self.subTest(path=name):
                git(self.target, 'update-index', '--add', '--cacheinfo', '100644,' + oid + ',' + name)
                before = self.snapshot(self.target)
                try:
                    with self.assertRaisesRegex(Conflict, 'ancestor'):
                        staged_installation(self.target)
                    for command in ['check', 'doctor', 'bootstrap']:
                        result = run(command, '--repo', self.target, expect=1)
                        self.assertIn('ancestor', json.dumps(result).lower())
                        self.assertEqual(self.snapshot(self.target), before)
                finally:
                    git(self.target, 'update-index', '--force-remove', '--', name)
        run('check', '--repo', self.target, '--run-local')
        self.assertEqual(run('bootstrap', '--repo', self.target, '--apply')['changes'], [])

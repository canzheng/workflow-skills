import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / 'tools/workflow'
sys.path.insert(0, str(TOOLS))
import setup as installer
import workflow


def run(*args, expect=0):
    command = [sys.executable, str(TOOLS / 'workflow.py'), *map(str, args), '--json']
    r = subprocess.run(command, capture_output=True, text=True)
    if r.returncode != expect:
        raise AssertionError((command, r.returncode, r.stdout, r.stderr))
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(('CLI returned invalid JSON', command, r.returncode, r.stdout, r.stderr)) from exc


def operation_path(path, dir_fd=None):
    """Resolve Linux test injection paths without changing production routing."""
    return pathlib.Path(path) if dir_fd is None else pathlib.Path(installer.os.readlink('/proc/self/fd/' + str(dir_fd))) / path


def init(root):
    root.mkdir(parents=True)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    for key, value in [('user.email', 'test@example.invalid'), ('user.name', 'Fixture')]:
        subprocess.run(['git', '-C', str(root), 'config', key, value], check=True)


def commit(root):
    subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(root), 'commit', '-qm', 'fixture'], check=True)
    return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip()


def fixture_source(root):
    init(root)
    assets = {}
    for file in ('core.py', 'setup.py', 'bootstrap.py', 'workflow.py', 'checks.py', 'records.py', 'migration.py'):
        name = 'tools/workflow/' + file
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes((TOOLS / file).read_bytes())
        assets[name] = name.replace('tools/workflow/', '.agents/tools/workflow/', 1)
    for name in installer.SKILLS:
        path = '.agents/skills/' + name + '/SKILL.md'
        p = root / path
        p.parent.mkdir(parents=True)
        p.write_text('---\nname: ' + name + '\ndescription: fixture\n---\nFixture skill.\n')
        assets[path] = path
    for name in ('contract.md', 'README.md'):
        path = 'docs/workflow/' + name
        p = root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# Fixture\n')
        assets[path] = path
    for source, dest in [('templates/consumer/development.md', 'docs/workflow/development.md'),
                         ('templates/consumer/operations.md', 'docs/workflow/operations.md'),
                         ('.github/ISSUE_TEMPLATE/feature.yml', '.github/ISSUE_TEMPLATE/feature.yml'),
                         ('.github/ISSUE_TEMPLATE/bug.yml', '.github/ISSUE_TEMPLATE/bug.yml'),
                         ('.github/pull_request_template.md', '.github/pull_request_template.md'),
                         ('.agents/skills/workflow-risk-review/references/methods.md', '.agents/skills/workflow-risk-review/references/methods.md')]:
        p = root / dest
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT / source).read_bytes())
        assets[dest] = dest
    for source, dest in [('templates/consumer/verify.yml', '.github/workflows/workflow-v2-verify.yml'),
                         ('.github/workflows/pr-metadata.yml', '.github/workflows/workflow-v2-pr-metadata.yml'),
                         ('.github/workflows/issue-completion.yml', '.github/workflows/workflow-v2-issue-completion.yml')]:
        p = root / dest
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes((ROOT / source).read_bytes())
        assets[dest] = dest
    (root / '.workflow').mkdir()
    (root / '.workflow/bundle.json').write_text(json.dumps(dict(schema_version=1, bundle_version='2.0.0', assets=assets)))
    return commit(root)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = pathlib.Path(self.temp.name)
        self.source = self.base / 'source'
        self.sha = fixture_source(self.source)
        self.target = self.base / 'consumer with spaces'
        init(self.target)
        (self.target / 'AGENTS.md').write_text('User rule: preserve data.\n')
        commit(self.target)
        self.args = ['setup', '--source', self.source, '--revision', self.sha,
                     '--target', self.target, '--repository', 'fixture/consumer', '--skill-storage', 'tracked']

    def test_nonstring_bundle_destinations_return_json_without_writes(self):
        bundle = self.source / '.workflow/bundle.json'
        original = json.loads(bundle.read_text())
        before = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                  if p.is_file() and '.git' not in p.relative_to(self.target).parts}
        index = (self.target / '.git/index').read_bytes()
        global_target = self.base / 'isolated global skills'
        for value in [[], {}, None, 1, True]:
            with self.subTest(destination=value):
                spec = json.loads(json.dumps(original))
                spec['assets']['tools/workflow/core.py'] = value
                bundle.write_text(json.dumps(spec))
                sha = commit(self.source)
                for command in [('setup', '--target', self.target, '--repository', 'fixture/consumer'),
                                ('install-skills', '--target', global_target)]:
                    report = run(*command, '--source', self.source, '--revision', sha, '--apply', expect=2)
                    self.assertFalse(report['ok'])
                    self.assertIn('destination', json.dumps(report))
                    self.assertEqual({p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                                      if p.is_file() and '.git' not in p.relative_to(self.target).parts}, before)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    self.assertFalse(global_target.exists())

    def test_os_invalid_bundle_paths_return_json_without_writes(self):
        bundle = self.source / '.workflow/bundle.json'
        original = json.loads(bundle.read_text())
        extra = self.source / 'tools/workflow/extra.py'
        extra.write_text('Extra fixture asset.\n')
        before = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                  if p.is_file() and '.git' not in p.relative_to(self.target).parts}
        index = (self.target / '.git/index').read_bytes()
        global_target = self.base / 'isolated global skills'
        for source, destination in [('tools/workflow/extra\0.py', 'tools/workflow/extra.py'),
                                    ('tools/workflow/extra.py', 'tools/workflow/extra\0.py'),
                                    ('tools/workflow/extra\ud800.py', 'tools/workflow/extra.py'),
                                    ('tools/workflow/extra.py', 'tools/workflow/extra\ud800.py')]:
            with self.subTest(source=source, destination=destination):
                spec = json.loads(json.dumps(original))
                spec['assets'][source] = destination
                bundle.write_text(json.dumps(spec))
                sha = commit(self.source)
                for command in [('setup', '--target', self.target, '--repository', 'fixture/consumer'),
                                ('install-skills', '--target', global_target)]:
                    for apply in [(), ('--apply',)]:
                        with self.subTest(command=command[0], apply=bool(apply)):
                            report = run(*command, '--source', self.source, '--revision', sha,
                                         *apply, expect=2)
                            self.assertFalse(report['ok'])
                            self.assertEqual(report['findings'][0]['code'], 'invalid')
                            self.assertEqual({p.relative_to(self.target): p.read_bytes()
                                              for p in self.target.rglob('*') if p.is_file()
                                              and '.git' not in p.relative_to(self.target).parts}, before)
                            self.assertEqual((self.target / '.git/index').read_bytes(), index)
                            self.assertFalse(global_target.exists())

    def test_staging_creation_race_preserves_external_file_and_symlink(self):
        run(*self.args, '--apply')
        changed = self.source / 'docs/workflow/contract.md'
        changed.write_text('Updated contract.\n')
        revision = commit(self.source)
        external = self.base / 'external-user-file'
        external.write_bytes(b'HUMAN')
        original = (self.target / 'docs/workflow/contract.md').read_bytes()
        manifest = (self.target / '.workflow/install-manifest.json').read_bytes()
        index = (self.target / '.git/index').read_bytes()
        injected = []
        actual_copy, actual_open = installer.shutil.copyfile, installer.os.open

        def race(path):
            p = pathlib.Path(path)
            if p.name.endswith('.wf2-staged') and not injected:
                p.symlink_to(external)
                injected.append(p)

        def copy(src, dst, *args, **kwargs):
            race(dst)
            return actual_copy(src, dst, *args, **kwargs)

        def open_file(path, *args, **kwargs):
            race(operation_path(path, kwargs.get("dir_fd")))
            return actual_open(path, *args, **kwargs)

        with patch.object(installer.shutil, 'copyfile', copy), patch.object(installer.os, 'open', open_file), \
                contextlib.redirect_stdout(io.StringIO()) as output:
            status = workflow.main(['setup', '--source', str(self.source), '--revision', revision,
                                    '--target', str(self.target), '--repository', 'fixture/consumer',
                                    '--skill-storage', 'tracked', '--apply', '--json'])
        self.assertEqual(external.read_bytes(), b'HUMAN')
        self.assertEqual(status, 1, output.getvalue())
        self.assertFalse(json.loads(output.getvalue())['ok'])
        self.assertEqual(len(injected), 1)
        self.assertTrue(injected[0].is_symlink())
        self.assertEqual((self.target / 'docs/workflow/contract.md').read_bytes(), original)
        self.assertEqual((self.target / '.workflow/install-manifest.json').read_bytes(), manifest)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_destination_edits_at_replacement_are_captured_without_loss(self):
        binding, attribute = (installer, 'replace_entry') if hasattr(installer, 'replace_entry') else (installer.os, 'replace')
        actual = getattr(binding, attribute)
        index = (self.target / '.git/index').read_bytes()
        external = self.base / 'external-race-data'
        external.write_bytes(b'External human content')
        for existing in (True, False):
            for case in ('bytes', 'mode', 'inode', 'symlink'):
                with self.subTest(existing=existing, case=case):
                    victim = self.target / ('destination-' + str(existing) + '-' + case)
                    if existing:
                        victim.write_bytes(b'Original content')
                    original = victim.read_bytes() if existing else None
                    mode = victim.stat().st_mode if existing else None
                    injected = []
                    def replace(src, dst, **kwargs):
                        if operation_path(dst, kwargs.get('dst_dir_fd')) == victim and not injected:
                            if case == 'inode':
                                new = self.base / 'foreign-inode'
                                new.write_bytes(b'Original content' if existing else b'Human creation')
                                if existing:
                                    new.chmod(mode)
                                    victim.unlink()
                                new.rename(victim)
                            elif case == 'symlink':
                                victim.unlink(missing_ok=True)
                                victim.symlink_to(external)
                            else:
                                victim.write_bytes(b'Concurrent human content')
                                if case == 'mode':
                                    victim.chmod(0o700)
                            injected.append(victim.lstat())
                        return actual(src, dst, **kwargs)
                    with patch.object(binding, attribute, replace), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
                        installer.transaction(self.target, {victim.name: b'Installer content'})
                    self.assertEqual(len(injected), 1)
                    self.assertEqual(victim.lstat().st_ino, injected[0].st_ino)
                    self.assertEqual(victim.lstat().st_mode, injected[0].st_mode)
                    if case == 'symlink':
                        self.assertTrue(victim.is_symlink())
                    elif case == 'inode':
                        self.assertEqual(victim.read_bytes(), b'Original content' if existing else b'Human creation')
                    else:
                        self.assertEqual(victim.read_bytes(), b'Concurrent human content')
                    self.assertEqual(external.read_bytes(), b'External human content')
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
                    self.addCleanup(installer.shutil.rmtree, recovery)
                    record = json.loads((recovery / 'recovery-index.json').read_text())[victim.name]
                    if existing:
                        self.assertEqual((recovery / record['backup']).read_bytes(), original)
                        self.assertEqual(record['mode'], mode)
                    else:
                        self.assertIsNone(record['backup'])

    def test_rollback_open_boundary_preserves_changed_installed_inode(self):
        actual = installer.os.open
        index = (self.target / '.git/index').read_bytes()
        for case in ('bytes', 'mode', 'inode', 'deleted', 'symlink'):
            with self.subTest(case=case):
                victim = self.target / ('restore-' + case)
                victim.write_bytes(b'Original content')
                mode = victim.stat().st_mode
                external = self.base / ('restore-external-' + case)
                external.write_bytes(b'External human content')
                injected = []
                def open_file(path, flags, *args, **kwargs):
                    resolved = operation_path(path, kwargs.get('dir_fd'))
                    if resolved in (victim, victim.with_name(victim.name + '.wf2-restore')) and flags & installer.os.O_WRONLY and not injected:
                        if case == 'inode':
                            new = self.base / 'rollback-foreign-inode'
                            new.write_bytes(victim.read_bytes())
                            new.chmod(victim.stat().st_mode)
                            victim.unlink()
                            new.rename(victim)
                        elif case == 'deleted':
                            victim.unlink()
                        elif case == 'symlink':
                            victim.unlink()
                            victim.symlink_to(external)
                        else:
                            victim.write_bytes(b'Concurrent human content')
                            if case == 'mode':
                                victim.chmod(0o700)
                        injected.append(victim.lstat() if victim.exists() or victim.is_symlink() else None)
                    return actual(path, flags, *args, **kwargs)
                with patch.object(installer.os, 'open', open_file), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
                    installer.transaction(self.target, {victim.name: b'Installer content'}, fail_after=1)
                self.assertEqual(len(injected), 1)
                if case == 'deleted':
                    self.assertFalse(victim.exists())
                else:
                    self.assertEqual(victim.lstat().st_ino, injected[0].st_ino)
                    self.assertEqual(victim.lstat().st_mode, injected[0].st_mode)
                    self.assertEqual(victim.read_bytes(), b'Installer content' if case == 'inode' else b'External human content' if case == 'symlink' else b'Concurrent human content')
                self.assertEqual(external.read_bytes(), b'External human content')
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
                self.addCleanup(installer.shutil.rmtree, recovery)
                record = json.loads((recovery / 'recovery-index.json').read_text())[victim.name]
                self.assertEqual((recovery / record['backup']).read_bytes(), b'Original content')
                self.assertEqual(record['mode'], mode)

    def test_deletion_boundary_preserves_concurrently_changed_entry(self):
        binding, attribute = (installer, 'remove_entry') if hasattr(installer, 'remove_entry') else (installer.os, 'unlink')
        actual = getattr(binding, attribute)
        victim = self.target / 'delete-race'
        victim.write_bytes(b'Original content')
        index = (self.target / '.git/index').read_bytes()
        def remove(path, **kwargs):
            if operation_path(path, kwargs.get('dir_fd')) == victim:
                victim.write_bytes(b'Concurrent human content')
            return actual(path, **kwargs)
        with patch.object(binding, attribute, remove), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
            installer.transaction(self.target, {victim.name: None})
        self.assertEqual(victim.read_bytes(), b'Concurrent human content')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(installer.shutil.rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())[victim.name]
        self.assertEqual((recovery / record['backup']).read_bytes(), b'Original content')

    def test_cleanup_captures_replaced_staging_entries_before_discard(self):
        binding, attribute = (installer, 'capture_entry') if hasattr(installer, 'capture_entry') else (installer.os, 'unlink')
        actual = getattr(binding, attribute)
        index = (self.target / '.git/index').read_bytes()
        actual_unlink = installer.os.unlink
        for suffix in ('.wf2-staged', '.wf2-restore', '.wf2-removed'):
            for kind in ('inode', 'symlink'):
                with self.subTest(suffix=suffix, kind=kind):
                    victim = self.target / ('cleanup' + suffix + '-' + kind)
                    victim.write_bytes(b'Original content')
                    staged = victim.with_name(victim.name + suffix)
                    external = self.base / ('cleanup-external' + suffix + '-' + kind)
                    external.write_bytes(b'Human content')
                    injected = []
                    def capture(path, **kwargs):
                        if operation_path(path, kwargs.get('dir_fd')) == staged and not injected:
                            actual_unlink(staged)
                            if kind == 'symlink':
                                staged.symlink_to(external)
                            else:
                                staged.write_bytes(b'Human content')
                            injected.append(staged.lstat())
                        return actual(path, **kwargs)
                    data = None if suffix == '.wf2-removed' else b'Installer content'
                    failure = 1 if suffix == '.wf2-restore' else None
                    with patch.object(binding, attribute, capture), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
                        installer.transaction(self.target, {victim.name: data}, fail_after=failure)
                    self.assertEqual(len(injected), 1)
                    self.assertEqual(staged.lstat().st_ino, injected[0].st_ino)
                    self.assertEqual(staged.read_bytes(), b'Human content')
                    self.assertEqual(staged.is_symlink(), kind == 'symlink')
                    self.assertEqual(external.read_bytes(), b'Human content')
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
                    self.addCleanup(installer.shutil.rmtree, recovery)
                    record = json.loads((recovery / 'recovery-index.json').read_text())[victim.name]
                    self.assertEqual((recovery / record['backup']).read_bytes(), b'Original content')

    def test_created_directory_cleanup_captures_actual_inode(self):
        binding, attribute = (installer, 'capture_entry') if hasattr(installer, 'capture_entry') else (installer.os, 'rmdir')
        actual = getattr(binding, attribute)
        directory = self.target / 'created-directory-race'
        index = (self.target / '.git/index').read_bytes()
        injected = []
        def capture(path, **kwargs):
            if operation_path(path, kwargs.get('dir_fd')) == directory and not injected:
                mode = directory.stat().st_mode
                directory.rename(directory.with_name('saved-created-directory'))
                directory.mkdir()
                directory.chmod(mode)
                injected.append(directory.stat())
            return actual(path, **kwargs)
        with patch.object(binding, attribute, capture), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
            installer.transaction(self.target, {'created-directory-race/file.md': b'Installer content'}, fail_after=1)
        self.assertEqual(len(injected), 1)
        self.assertEqual(directory.stat().st_ino, injected[0].st_ino)
        self.assertEqual(list(directory.iterdir()), [])
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(installer.shutil.rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())[directory.name]
        self.assertEqual(record['kind'], 'directory')
        self.assertIsNone(record['backup'])

    def test_quarantine_restore_collision_retains_both_entries(self):
        actual = installer.capture_entry
        victim = self.target / 'AGENTS.md'
        original = victim.read_bytes()
        staging = victim.with_name(victim.name + '.wf2-staged')
        index = (self.target / '.git/index').read_bytes()
        injected = []
        @contextlib.contextmanager
        def capture(path, **kwargs):
            with actual(path, **kwargs) as captured:
                if operation_path(path, kwargs.get('dir_fd')) == staging and not injected:
                    self.assertFalse(staging.exists())
                    staging.write_bytes(b'Concurrent public entry')
                    injected.append(True)
                yield captured
        with patch.object(installer, 'capture_entry', capture), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
            installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual(injected, [True])
        self.assertEqual(staging.read_bytes(), b'Concurrent public entry')
        self.assertEqual(victim.read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(installer.shutil.rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())['AGENTS.md.wf2-staged']
        retained = self.target / record['quarantine']
        self.assertEqual(retained.read_bytes(), original)
        self.assertEqual(retained.parent.stat().st_mode & 0o777, 0o700)

    def test_private_storage_birth_rejects_replaced_or_changed_directory(self):
        actual = installer.os.mkdir
        victim = self.target / 'AGENTS.md'
        original, index = victim.read_bytes(), (self.target / '.git/index').read_bytes()
        for case in ('public-replacement', 'same-mode-replacement', 'mode-change', 'symlink'):
            with self.subTest(case=case):
                victim.write_bytes(original)  # Reset only this owned reproduction fixture.
                injected = []
                def mkdir(path, *args, **kwargs):
                    result = actual(path, *args, **kwargs)
                    resolved = operation_path(path, kwargs.get('dir_fd'))
                    if resolved.name.startswith('.wf2-private-') and not injected:
                        saved = resolved.with_name(resolved.name + '-saved')
                        if case == 'mode-change':
                            resolved.chmod(0o777)
                        else:
                            resolved.rename(saved)
                            if case == 'symlink':
                                resolved.symlink_to(saved, target_is_directory=True)
                            else:
                                actual(resolved, mode=0o700)
                                resolved.chmod(0o777 if case == 'public-replacement' else 0o700)
                        injected.append((resolved, saved, resolved.lstat()))
                    return result
                with patch.object(installer.os, 'mkdir', mkdir), self.assertRaises((installer.Conflict, OSError)):
                    installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
                self.assertEqual(len(injected), 1)
                resolved, saved, metadata = injected[0]
                self.assertEqual(resolved.lstat().st_ino, metadata.st_ino)
                self.assertEqual(list(resolved.iterdir()), [])
                if saved.exists():
                    self.assertEqual(list(saved.iterdir()), [])
                self.assertEqual(victim.read_bytes(), original)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_private_staged_directory_birth_cannot_claim_concurrent_inode(self):
        actual = installer.os.mkdir
        index = (self.target / '.git/index').read_bytes()
        for mode in (0o700, 0o777):
            with self.subTest(mode=mode):
                injected = []
                destination = self.target / 'private-birth-race'
                def mkdir(path, *args, **kwargs):
                    result = actual(path, *args, **kwargs)
                    resolved = operation_path(path, kwargs.get('dir_fd'))
                    if resolved.name.startswith('directory-') and not injected:
                        saved = resolved.with_name(resolved.name + '-saved')
                        resolved.rename(saved)
                        actual(resolved, mode=mode)
                        resolved.chmod(mode)
                        injected.append((resolved, saved, resolved.stat()))
                    return result
                with patch.object(installer.os, 'mkdir', mkdir), self.assertRaises(installer.Conflict):
                    installer.transaction(self.target, {'private-birth-race/file.md': b'Installer content'})
                self.assertEqual(len(injected), 1)
                resolved, saved, metadata = injected[0]
                self.assertEqual(resolved.stat().st_ino, metadata.st_ino)
                self.assertEqual(list(resolved.iterdir()), [])
                self.assertEqual(list(saved.iterdir()), [])
                self.assertFalse(destination.exists())
                self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_directory_identity_is_validated_after_final_event_read(self):
        actual_read, actual_mkdir = installer.os.read, installer.os.mkdir
        victim = self.target / 'AGENTS.md'
        original, index = victim.read_bytes(), (self.target / '.git/index').read_bytes()
        for case in ('same-mode-inode', 'symlink', 'deleted', 'permissions'):
            with self.subTest(case=case):
                victim.write_bytes(original)  # Reset only this owned reproduction fixture.
                before = set((self.target / '.git').glob('.wf2-private-*'))
                injected = []
                def read(fd, size):
                    try:
                        return actual_read(fd, size)
                    except BlockingIOError:
                        if installer.os.readlink('/proc/self/fd/' + str(fd)) == 'anon_inode:inotify' and not injected:
                            created = set((self.target / '.git').glob('.wf2-private-*')) - before
                            self.assertEqual(len(created), 1)
                            directory = created.pop()
                            saved = directory.with_name(directory.name + '-saved')
                            if case == 'permissions':
                                directory.chmod(0o777)
                            else:
                                directory.rename(saved)
                                if case == 'symlink':
                                    directory.symlink_to(saved, target_is_directory=True)
                                elif case == 'same-mode-inode':
                                    actual_mkdir(directory, mode=0o700)
                            injected.append((directory, saved))
                        raise
                with patch.object(installer.os, 'read', read), self.assertRaises(installer.Conflict):
                    installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
                self.assertEqual(len(injected), 1)
                directory, saved = injected[0]
                if saved.exists():
                    self.assertEqual(list(saved.iterdir()), [])
                if directory.exists():
                    self.assertEqual(list(directory.iterdir()), [])
                self.assertEqual(victim.read_bytes(), original)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_directory_creation_observation_unavailable_preserves_project(self):
        original = (self.target / 'AGENTS.md').read_bytes()
        index = (self.target / '.git/index').read_bytes()
        before = set((self.target / '.git').iterdir())
        with patch.object(installer, 'directory_watch_functions', side_effect=installer.Conflict('Observation unavailable')):
            with self.assertRaisesRegex(installer.Conflict, 'Observation unavailable'):
                installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        self.assertEqual(set((self.target / '.git').iterdir()), before)

    def test_directory_creation_observation_overflow_fails_closed(self):
        import struct
        read_fd, write_fd = installer.os.pipe2(installer.os.O_NONBLOCK | installer.os.O_CLOEXEC)
        try:
            installer.os.write(write_fd, struct.pack('iIII', -1, 0x4000, 0, 0))
            with self.assertRaisesRegex(installer.Conflict, 'overflowed'):
                installer.directory_birth_events(read_fd, 'directory-fixture')
        finally:
            installer.os.close(read_fd)
            installer.os.close(write_fd)

    def test_private_storage_is_not_removed_by_a_checked_basename(self):
        actual = installer.os.rmdir
        index = (self.target / '.git/index').read_bytes()
        replacements = []
        def remove(path, **kwargs):
            resolved = operation_path(path, kwargs.get('dir_fd'))
            if resolved.name.startswith('.wf2-private-'):
                saved = resolved.with_name(resolved.name + '-saved')
                mode = resolved.stat().st_mode
                resolved.rename(saved)
                resolved.mkdir()
                resolved.chmod(mode)
                replacements.append(resolved)
            return actual(path, **kwargs)
        with patch.object(installer.os, 'rmdir', remove):
            installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual(replacements, [])
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), b'Installer content')
        retained = set((self.target / '.git').glob('.wf2-private-*'))
        self.assertTrue(retained)
        installer.transaction(self.target, {})
        self.assertEqual(set((self.target / '.git').glob('.wf2-private-*')), retained)

    def test_created_directory_publication_cannot_claim_concurrent_inode(self):
        binding, attribute = (installer, 'publish_directory') if hasattr(installer, 'publish_directory') else (installer.os, 'mkdir')
        actual = getattr(binding, attribute)
        actual_mkdir = installer.os.mkdir
        directory = self.target / 'published-directory-race'
        index = (self.target / '.git/index').read_bytes()
        injected = []
        def publish(path, *args, **kwargs):
            resolved = operation_path(path, kwargs.get('dir_fd'))
            if resolved != directory or injected:
                return actual(path, *args, **kwargs)
            if attribute == 'mkdir':
                actual(path, *args, **kwargs)
                directory.rename(directory.with_name('saved-published-directory'))
            actual_mkdir(directory)
            injected.append(directory.stat())
            if attribute != 'mkdir':
                return actual(path, *args, **kwargs)
        with patch.object(binding, attribute, publish), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
            installer.transaction(self.target, {'published-directory-race/file.md': b'Installer content'}, fail_after=1)
        self.assertEqual(len(injected), 1)
        self.assertEqual(directory.stat().st_ino, injected[0].st_ino)
        self.assertEqual(list(directory.iterdir()), [])
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(installer.shutil.rmtree, recovery)
        self.assertTrue((recovery / 'recovery-index.json').is_file())

    def test_cross_device_capture_storage_rejects_before_project_writes(self):
        actual = installer.os.fstat
        original = (self.target / 'AGENTS.md').read_bytes()
        index = (self.target / '.git/index').read_bytes()
        storage_before = set((self.target / '.git').iterdir())
        def metadata(fd):
            result = actual(fd)
            if pathlib.Path(installer.os.readlink('/proc/self/fd/' + str(fd))) == self.target / '.git':
                values = list(result)
                values[2] += 1
                return installer.os.stat_result(values)
            return result
        with patch.object(installer.os, 'fstat', metadata), self.assertRaisesRegex(installer.Conflict, 'share the target filesystem'):
            installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        self.assertEqual(set((self.target / '.git').iterdir()), storage_before)

    def test_captured_file_finalization_retains_replaced_entry(self):
        binding, attribute = (installer, 'retain_entry') if hasattr(installer, 'retain_entry') else (installer.os, 'unlink')
        actual = getattr(binding, attribute)
        actual_unlink = installer.os.unlink
        victim = self.target / 'AGENTS.md'
        original = victim.read_bytes()
        index = (self.target / '.git/index').read_bytes()
        injected = []
        def retain(path, **kwargs):
            resolved = operation_path(path, kwargs.get('dir_fd'))
            if resolved.name.endswith('AGENTS.md.wf2-staged') and not injected:
                actual_unlink(resolved)
                resolved.write_bytes(b'Concurrent captured content')
                injected.append((resolved, resolved.stat()))
            return actual(path, **kwargs)
        with patch.object(binding, attribute, retain), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
            installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual(len(injected), 1)
        preserved = injected[0][0] if injected[0][0].exists() else victim.with_name(victim.name + '.wf2-staged')
        self.assertEqual(preserved.read_bytes(), b'Concurrent captured content')
        self.assertEqual(preserved.stat().st_ino, injected[0][1].st_ino)
        self.assertEqual(victim.read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(installer.shutil.rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())['AGENTS.md.wf2-staged']
        self.assertEqual((recovery / record['concurrent_backup']).read_bytes(), b'Concurrent captured content')
        self.assertEqual(record['restored_to'], 'AGENTS.md.wf2-staged')
        self.assertNotIn('quarantine', record)

    def test_successful_replacement_retains_displaced_bytes_and_mode(self):
        victim = self.target / 'AGENTS.md'
        original = victim.read_bytes()
        mode = victim.stat().st_mode
        index = (self.target / '.git/index').read_bytes()
        installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        captures = list((self.target / '.git').glob('.wf2-private-*/*AGENTS.md.wf2-staged'))
        self.assertEqual(len(captures), 1)
        self.assertEqual(captures[0].read_bytes(), original)
        self.assertEqual(captures[0].stat().st_mode, mode)
        self.assertEqual(victim.read_bytes(), b'Installer content')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_atomic_replacement_unavailable_never_falls_back_to_overwrite(self):
        victim = self.target / 'AGENTS.md'
        original = victim.read_bytes()
        index = (self.target / '.git/index').read_bytes()
        with patch.object(installer.ctypes, 'CDLL', side_effect=OSError('unavailable')):
            with self.assertRaisesRegex(installer.Conflict, 'Atomic filesystem replacement unavailable'):
                installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual(victim.read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        self.assertFalse(victim.with_name(victim.name + '.wf2-staged').exists())

    def test_in_place_staging_cleanup_edit_is_preserved_in_recovery(self):
        actual = installer.retain_entry
        victim = self.target / 'AGENTS.md'
        original = victim.read_bytes()
        index = (self.target / '.git/index').read_bytes()
        injected = []
        def unlink(path, **kwargs):
            resolved = operation_path(path, kwargs.get('dir_fd'))
            if resolved.name.endswith(victim.name + '.wf2-staged') and not injected:
                resolved.write_bytes(b'Late concurrent staging content')
                injected.append(True)
            return actual(path, **kwargs)
        with patch.object(installer, 'replace_entry', side_effect=OSError('before replacement')):
            with patch.object(installer, 'retain_entry', unlink), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
                installer.transaction(self.target, {'AGENTS.md': b'Installer content'})
        self.assertEqual(injected, [True])
        self.assertEqual(victim.read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(installer.shutil.rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())['AGENTS.md.wf2-staged']
        self.assertEqual((recovery / record['concurrent_backup']).read_bytes(), b'Late concurrent staging content')

    def test_successful_replace_rejects_foreign_staging_or_changed_destination(self):
        run(*self.args, '--apply')
        changed = self.source / 'docs/workflow/contract.md'
        changed.write_text('Updated contract.\n')
        revision = commit(self.source)
        victim = self.target / 'docs/workflow/contract.md'
        original, mode = victim.read_bytes(), victim.stat().st_mode
        manifest = (self.target / '.workflow/install-manifest.json').read_bytes()
        index = (self.target / '.git/index').read_bytes()
        external = self.base / 'external'
        external.write_bytes(b'External human content.\n')
        actual_replace = installer.replace_entry
        for case in ('bytes', 'mode', 'same-content-inode', 'symlink', 'deleted'):
            with self.subTest(case=case):
                try:
                    injected = []
                    def replace(src, dst, **kwargs):
                        if operation_path(dst, kwargs.get('dst_dir_fd')) != victim:
                            return actual_replace(src, dst, **kwargs)
                        staged = operation_path(src, kwargs.get('src_dir_fd'))
                        if case == 'bytes':
                            staged.write_bytes(b'HUMAN-RACE')
                        elif case == 'mode':
                            staged.chmod(0o700)
                        elif case == 'same-content-inode':
                            replacement = self.base / 'foreign-same-content'
                            replacement.write_bytes(staged.read_bytes())
                            replacement.chmod(staged.stat().st_mode)
                            staged.unlink()
                            replacement.rename(staged)
                        elif case == 'symlink':
                            staged.unlink()
                            staged.symlink_to(external)
                        actual_replace(src, dst, **kwargs)
                        if case == 'deleted':
                            victim.unlink()
                        injected.append(True)
                    with patch.object(installer, 'replace_entry', replace), contextlib.redirect_stdout(io.StringIO()) as output:
                        status = workflow.main(['setup', '--source', str(self.source), '--revision', revision,
                                                '--target', str(self.target), '--repository', 'fixture/consumer',
                                                '--skill-storage', 'tracked', '--apply', '--json'])
                    self.assertEqual(status, 1, output.getvalue())
                    self.assertEqual(injected, [True])
                    report = json.loads(output.getvalue())
                    self.assertFalse(report['ok'])
                    message = report['findings'][0]['message']
                    self.assertIn('Rollback residuals: docs/workflow/contract.md', message)
                    self.assertEqual((self.target / '.workflow/install-manifest.json').read_bytes(), manifest)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    self.assertEqual(external.read_bytes(), b'External human content.\n')
                    if case == 'bytes':
                        self.assertEqual(victim.read_bytes(), b'HUMAN-RACE')
                    elif case == 'mode':
                        self.assertEqual(victim.stat().st_mode & 0o777, 0o700)
                    elif case == 'same-content-inode':
                        self.assertEqual(victim.read_bytes(), changed.read_bytes())
                    elif case == 'symlink':
                        self.assertTrue(victim.is_symlink())
                    else:
                        self.assertFalse(victim.exists())
                    recovery = pathlib.Path(message.split('recoverable originals: ', 1)[1])
                    self.addCleanup(installer.shutil.rmtree, recovery)
                    record = json.loads((recovery / 'recovery-index.json').read_text())['docs/workflow/contract.md']
                    self.assertEqual((recovery / record['backup']).read_bytes(), original)
                    self.assertEqual(record['mode'], mode)
                finally:
                    if victim.is_symlink():
                        victim.unlink()
                    victim.write_bytes(original)
                    victim.chmod(mode)  # Explicit recovery only in this owned fixture.
                    (self.target / '.workflow/install-manifest.json').write_bytes(manifest)

    def test_failed_replace_preserves_concurrent_staging_changes(self):
        run(*self.args, '--apply')
        changed = self.source / 'docs/workflow/contract.md'
        changed.write_text('Updated contract.\n')
        revision = commit(self.source)
        target = self.target / 'docs/workflow/contract.md'
        staged = target.with_name(target.name + '.wf2-staged')
        external = self.base / 'external-user-file'
        external.write_bytes(b'HUMAN')
        original = target.read_bytes()
        manifest = (self.target / '.workflow/install-manifest.json').read_bytes()
        index = (self.target / '.git/index').read_bytes()
        for case in ('unchanged', 'bytes', 'mode', 'replacement', 'symlink'):
            with self.subTest(case=case):
                def replace(src, dst, **kwargs):
                    self.assertEqual(operation_path(src, kwargs.get("src_dir_fd")), staged)
                    if case == 'bytes':
                        staged.write_bytes(b'Concurrent staging content.')
                    elif case == 'mode':
                        staged.chmod(0o700 if staged.stat().st_mode & 0o777 != 0o700 else 0o750)
                    elif case == 'replacement':
                        contents, mode = staged.read_bytes(), staged.stat().st_mode
                        replacement = self.base / 'replacement'
                        replacement.write_bytes(contents)
                        replacement.chmod(mode)
                        staged.unlink()
                        replacement.rename(staged)
                    elif case == 'symlink':
                        staged.unlink()
                        staged.symlink_to(external)
                    raise OSError('Injected replace failure')

                with patch.object(installer, 'replace_entry', replace), \
                        contextlib.redirect_stdout(io.StringIO()) as output:
                    status = workflow.main(['setup', '--source', str(self.source), '--revision', revision,
                                            '--target', str(self.target), '--repository', 'fixture/consumer',
                                            '--skill-storage', 'tracked', '--apply', '--json'])
                self.assertEqual(status, 1, output.getvalue())
                report = json.loads(output.getvalue())
                message = report['findings'][0]['message']
                self.assertEqual(target.read_bytes(), original)
                self.assertEqual(external.read_bytes(), b'HUMAN')
                self.assertEqual((self.target / '.workflow/install-manifest.json').read_bytes(), manifest)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                if case == 'unchanged':
                    self.assertFalse(staged.exists())
                    self.assertIn('original files restored', message)
                else:
                    self.assertTrue(staged.exists() or staged.is_symlink())
                    if case == 'bytes':
                        self.assertEqual(staged.read_bytes(), b'Concurrent staging content.')
                    if case == 'symlink':
                        self.assertTrue(staged.is_symlink())
                    self.assertIn('Rollback residuals: docs/workflow/contract.md.wf2-staged', message)
                    recovery = pathlib.Path(message.split('recoverable originals: ', 1)[1])
                    metadata = json.loads((recovery / 'recovery-index.json').read_text())
                    self.assertEqual(metadata['docs/workflow/contract.md.wf2-staged']['kind'], 'staging')
                    self.assertEqual((recovery / metadata['docs/workflow/contract.md']['backup']).read_bytes(), original)
                    installer.shutil.rmtree(recovery)
                    staged.unlink()  # Explicit recovery cleanup only in this owned fixture.

    def test_annotated_tag_object_is_not_accepted_as_a_commit_pin(self):
        subprocess.run(['git', '-C', str(self.source), '-c', 'tag.gpgSign=false', 'tag', '-a', 'wf2-fixture', '-m', 'Immutable tag object'], check=True)
        tag = subprocess.check_output(['git', '-C', str(self.source), 'rev-parse', 'wf2-fixture'], text=True).strip()
        self.assertNotEqual(tag, self.sha)
        before = subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage'])
        report = run('setup', '--source', self.source, '--revision', tag, '--target', self.target, '--repository', 'fixture/consumer', '--apply', expect=2)
        self.assertFalse(report['ok'])
        self.assertFalse((self.target / '.workflow/install-manifest.json').exists())
        self.assertEqual((self.target / 'AGENTS.md').read_text(), 'User rule: preserve data.\n')
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage']), before)
        run(*self.args, '--apply')
        self.assertEqual(json.loads((self.target / '.workflow/install-manifest.json').read_text())['source_revision'], self.sha)

    def test_replacement_refs_cannot_change_pinned_source_bytes(self):
        name = '.agents/skills/workflow-design-to-backlog/SKILL.md'
        path = self.source / name
        original = path.read_bytes()
        replacement_bytes = original + b'Local replacement content.\n'
        path.write_bytes(replacement_bytes)
        replacement = commit(self.source)
        subprocess.run(['git', '-C', str(self.source), 'replace', self.sha, replacement], check=True)
        # Git normally serves the replacement bytes under the original commit ID.
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.source), 'show', self.sha + ':' + name]), replacement_bytes)
        before = subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage'])
        result = run(*self.args, '--apply', expect=1)
        self.assertIn('Source bytes differ from pinned revision', json.dumps(result))
        self.assertFalse((self.target / '.workflow/install-manifest.json').exists())
        self.assertEqual((self.target / 'AGENTS.md').read_text(), 'User rule: preserve data.\n')
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage']), before)

        # Canonical worktree bytes can still install without deleting local refs.
        path.write_bytes(original)
        run(*self.args, '--apply')
        self.assertEqual((self.target / name).read_bytes(), original)
        pin = json.loads((self.target / '.workflow/install-manifest.json').read_text())
        self.assertEqual(pin['source_revision'], self.sha)
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.source), 'rev-parse', 'refs/replace/' + self.sha], text=True).strip(), replacement)
        commit(self.target)
        tracked = {p: (self.target / p).read_bytes() for p in subprocess.check_output(['git', '-C', str(self.target), 'ls-files'], text=True).splitlines()}
        before = subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage'])
        missing = [p for p in pin['files'] if installer.shared(p)]
        for p in missing:
            (self.target / p).unlink()

        # A separate source clone without local replacements reproduces that pin.
        clone = self.base / 'canonical-source'
        subprocess.run(['git', 'clone', '--quiet', '--no-local', str(self.source), str(clone)], check=True)
        subprocess.run(['git', '-C', str(clone), 'checkout', '--detach', '--quiet', self.sha], check=True)
        self.assertEqual(subprocess.check_output(['git', '-C', str(clone), 'for-each-ref', 'refs/replace']), b'')
        run('bootstrap', '--repo', self.target, '--source', clone, '--apply', expect=1)
        self.assertTrue(all(not (self.target / p).exists() for p in missing))
        # Restore the committed canonical consumer bytes, then verify against a
        # separate source clone: startup never fetches/recreates tracked assets.
        subprocess.run(['git', '-C', str(self.target), 'restore', '--', *missing], check=True)
        self.assertEqual(run('bootstrap', '--repo', self.target, '--source', clone, '--apply')['changes'], [])
        self.assertEqual((self.target / name).read_bytes(), original)
        self.assertEqual({p: (self.target / p).read_bytes() for p in tracked}, tracked)
        self.assertEqual(subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage']), before)

    def test_omitted_public_runtime_module_fails_before_install(self):
        bundle = self.source / '.workflow/bundle.json'
        original = json.loads(bundle.read_text())
        for module in ('workflow.py', 'core.py', 'setup.py', 'bootstrap.py', 'checks.py', 'records.py', 'migration.py'):
            with self.subTest(module=module):
                spec = json.loads(json.dumps(original))
                del spec['assets']['tools/workflow/' + module]
                bundle.write_text(json.dumps(spec))
                sha = commit(self.source)
                result = run('setup', '--source', self.source, '--revision', sha, '--target', self.target, '--repository', 'fixture/consumer', '--apply', expect=1)
                self.assertIn('Incomplete production bundle', json.dumps(result))
                self.assertFalse((self.target / '.workflow').exists())
                self.assertEqual((self.target / 'AGENTS.md').read_text(), 'User rule: preserve data.\n')

    def test_required_docs_templates_and_reference_cannot_be_omitted(self):
        bundle = self.source / '.workflow/bundle.json'
        original = json.loads(bundle.read_text())
        required = ['docs/workflow/' + name for name in ('contract.md', 'README.md', 'development.md', 'operations.md')]
        required += ['.github/ISSUE_TEMPLATE/feature.yml', '.github/ISSUE_TEMPLATE/bug.yml', '.github/pull_request_template.md', '.agents/skills/workflow-risk-review/references/methods.md']
        for name in required:
            with self.subTest(asset=name):
                spec = json.loads(json.dumps(original))
                del spec['assets'][name]
                bundle.write_text(json.dumps(spec))
                sha = commit(self.source)
                result = run('setup', '--source', self.source, '--revision', sha, '--target', self.target, '--repository', 'fixture/consumer', '--apply', expect=1)
                self.assertIn('Incomplete production bundle', json.dumps(result))
                self.assertFalse((self.target / '.workflow').exists())

    def test_fresh_dry_run_apply_noop_doctor_and_uninstall(self):
        original = (self.target / 'AGENTS.md').read_bytes()
        preview = run(*self.args)
        self.assertTrue(preview['changes'])
        self.assertFalse((self.target / '.workflow').exists())
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), original)
        run(*self.args, '--apply')
        self.assertIn('User rule', (self.target / 'AGENTS.md').read_text())
        self.assertEqual(run(*self.args, '--apply')['changes'], [])
        report = run('doctor', '--repo', self.target)
        self.assertEqual(report['mode'], 'installed-consumer')
        self.assertEqual(report['capabilities']['github_write'], 'unprobed')
        m = json.loads((self.target / '.workflow/install-manifest.json').read_text())
        self.assertEqual(m['source_revision'], self.sha)
        self.assertNotIn('.workflow/install-manifest.json', m['files'])
        run('setup', '--target', self.target, '--uninstall', '--apply')
        self.assertTrue((self.target / '.workflow/config.json').exists())
        self.assertIn('User rule', (self.target / 'AGENTS.md').read_text())
        self.assertFalse((self.target / '.agents/skills/workflow-risk-review/SKILL.md').exists())

    def test_missing_target_subdir_symlink_and_traversal(self):
        run('setup', '--target', self.base / 'missing', '--uninstall', expect=2)
        sub = self.target / 'sub'
        sub.mkdir()
        run('setup', '--target', sub, '--uninstall', expect=2)
        alias = self.base / 'alias'
        alias.symlink_to(self.target, target_is_directory=True)
        run('setup', '--target', alias, '--uninstall', expect=2)
        (self.target / '.agents').symlink_to(self.source, target_is_directory=True)
        run(*self.args, '--apply', expect=2)
        self.assertFalse((self.target / '.workflow').exists())

    def test_marker_and_unmanaged_collision_preflight(self):
        (self.target / 'AGENTS.md').write_text(installer.START)
        run(*self.args, '--apply', expect=1)
        self.assertFalse((self.target / '.workflow').exists())
        (self.target / 'AGENTS.md').write_text('Unrelated\n')
        p = self.target / '.agents/tools/workflow/core.py'
        p.parent.mkdir(parents=True)
        p.write_text('human')
        run(*self.args, '--apply', expect=1)
        self.assertEqual(p.read_text(), 'human')
        self.assertFalse((self.target / '.workflow').exists())

    def test_update_preserves_config_and_rejects_modified_asset(self):
        run(*self.args, '--apply')
        cp = self.target / '.workflow/config.json'
        c = json.loads(cp.read_text())
        c['openspec'] = 'disabled'
        c['author_local_review'] = 'required'
        cp.write_text(json.dumps(c))
        run(*self.args, '--apply')
        self.assertEqual(json.loads(cp.read_text())['openspec'], 'disabled')
        self.assertEqual(json.loads(cp.read_text())['author_local_review'], 'required')
        p = self.target / 'docs/workflow/contract.md'
        p.write_text('local modifications')
        run(*self.args, '--apply', expect=1)
        r = run('setup', '--target', self.target, '--uninstall', '--apply', expect=1)
        self.assertIn('docs/workflow/contract.md', r['residuals'])
        self.assertEqual(p.read_text(), 'local modifications')

    def test_pinned_source_mismatch_and_incomplete_bundle(self):
        p = self.source / 'docs/workflow/contract.md'
        p.write_text('uncommitted')
        run(*self.args, '--apply', expect=1)
        self.assertFalse((self.target / '.workflow').exists())
        p.write_text('# Fixture\n')
        specpath = self.source / '.workflow/bundle.json'
        spec = json.loads(specpath.read_text())
        del spec['assets']['.agents/skills/workflow-risk-review/SKILL.md']
        specpath.write_text(json.dumps(spec))
        sha = commit(self.source)
        args = self.args.copy()
        args[args.index('--revision') + 1] = sha
        run(*args, '--apply', expect=1)

    def test_failure_during_public_apply_restores_originals(self):
        original = (self.target / 'AGENTS.md').read_bytes()
        actual = installer.replace_entry
        calls = 0
        def fail(src, dst, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 4:
                raise OSError('simulated disk failure')
            return actual(src, dst, **kwargs)
        argv = [str(x) for x in self.args] + ['--apply', '--json']
        with patch.object(installer, 'replace_entry', side_effect=fail), contextlib.redirect_stdout(io.StringIO()) as out:
            code = workflow.main(argv)
        self.assertEqual(code, 1)
        self.assertIn('original files restored', out.getvalue())
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), original)
        self.assertFalse((self.target / '.workflow').exists())
        run(*self.args, '--apply')

    def test_public_update_rollback_preserves_concurrent_edits(self):
        run(*self.args, '--apply')
        commit(self.target)
        names = ['docs/workflow/contract.md', 'docs/workflow/operations.md']
        originals = {name: (self.target / name).read_bytes() for name in names}
        for name in names:
            (self.source / name).write_bytes(originals[name] + b'Updated source.\n')
        sha = commit(self.source)
        args = [str(x) for x in self.args]
        args[args.index('--revision') + 1] = sha
        index_before = (self.target / '.git/index').read_bytes()
        external = self.base / 'external'
        external.mkdir()
        external_file = external / 'contract.md'
        external_file.write_bytes(b'External user content.\n')
        p = self.target / names[0]
        actual = installer.replace_entry
        for edit in ('bytes', 'mode', 'deleted', 'symlink', 'parent-symlink'):
            with self.subTest(edit=edit):
                calls = 0
                def replace(src, dst, **kwargs):
                    nonlocal calls
                    calls += 1
                    if calls == 2:
                        raise OSError('later replacement failed')
                    actual(src, dst, **kwargs)
                    if edit == 'bytes':
                        p.write_bytes(b'Concurrent user edit.\n')
                    elif edit == 'mode':
                        p.chmod(0o600)
                    elif edit == 'deleted':
                        p.unlink()
                    elif edit == 'symlink':
                        p.unlink()
                        p.symlink_to(external_file)
                    else:
                        p.parent.rename(p.parent.with_name('saved-workflow'))
                        p.parent.symlink_to(external, target_is_directory=True)
                with patch.object(installer, 'replace_entry', side_effect=replace), contextlib.redirect_stdout(io.StringIO()) as out:
                    code = workflow.main(args + ['--apply', '--json'])
                self.assertEqual(code, 1)
                report = json.loads(out.getvalue())
                message = report['findings'][0]['message']
                self.assertIn('Rollback residuals: ' + names[0], message)
                self.assertNotIn('original files restored', message)
                recovery = pathlib.Path(message.split('recoverable originals: ', 1)[1])
                self.addCleanup(__import__('shutil').rmtree, recovery)
                recovery_index = json.loads((recovery / 'recovery-index.json').read_text())
                self.assertEqual((recovery / recovery_index[names[0]]['backup']).read_bytes(), originals[names[0]])
                self.assertEqual(external_file.read_bytes(), b'External user content.\n')
                self.assertEqual((self.target / '.git/index').read_bytes(), index_before)
                if edit == 'bytes':
                    self.assertEqual(p.read_bytes(), b'Concurrent user edit.\n')
                elif edit == 'mode':
                    self.assertEqual(p.stat().st_mode & 0o777, 0o600)
                    self.assertEqual(p.read_bytes(), originals[names[0]] + b'Updated source.\n')
                elif edit == 'deleted':
                    self.assertFalse(p.exists())
                elif edit == 'symlink':
                    self.assertTrue(p.is_symlink())
                    p.unlink()
                else:
                    self.assertTrue(p.parent.is_symlink())
                    p.parent.unlink()
                    p.parent.with_name('saved-workflow').rename(p.parent)
                p.write_bytes(originals[names[0]])
                p.chmod(0o644)
                self.assertEqual((self.target / names[1]).read_bytes(), originals[names[1]])
        run(*args, '--apply')  # explicit fixture recovery permits a normal retry

    def test_public_rollback_preserves_changed_created_directory(self):
        index = (self.target / '.git/index').read_bytes()
        actual = installer.replace_entry
        calls = 0
        created = None
        changed_mode = None
        def replace(src, dst, **kwargs):
            nonlocal calls, created, changed_mode
            if not str(src).endswith('.wf2-staged'):
                return actual(src, dst, **kwargs)
            calls += 1
            if calls == 2:
                raise OSError('later replacement failure')
            actual(src, dst, **kwargs)
            created = operation_path(dst, kwargs.get("dst_dir_fd")).parent
            changed_mode = 0o700 if created.stat().st_mode & 0o777 != 0o700 else 0o750
            created.chmod(changed_mode)
        args = [str(x) for x in self.args] + ['--apply', '--json']
        with patch.object(installer, 'replace_entry', replace), contextlib.redirect_stdout(io.StringIO()) as out:
            status = workflow.main(args)
        self.assertEqual(status, 1)
        message = json.loads(out.getvalue())['findings'][0]['message']
        self.assertIn('Rollback residuals:', message)
        self.assertIn(created.relative_to(self.target).as_posix(), message)
        self.assertTrue(created.is_dir())
        self.assertEqual(created.stat().st_mode & 0o777, changed_mode)
        self.assertEqual(list(created.iterdir()), [])  # unchanged file still rolls back
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(message.split('recoverable originals: ', 1)[1])
        self.addCleanup(__import__('shutil').rmtree, recovery)
        directory = json.loads((recovery / 'recovery-index.json').read_text())[created.relative_to(self.target).as_posix()]
        self.assertEqual(directory['kind'], 'directory')
        self.assertIsNone(directory['backup'])  # no original directory existed

    def test_rollback_preserves_replaced_created_directory_and_new_contents(self):
        for edit in ('replacement', 'new-content'):
            with self.subTest(edit=edit):
                name = 'new-' + edit + '/file.md'
                directory = (self.target / name).parent
                actual = installer.replace_entry
                def replace(src, dst, **kwargs):
                    actual(src, dst, **kwargs)
                    if edit == 'replacement':
                        mode = directory.stat().st_mode
                        directory.rename(directory.with_name(directory.name + '-moved'))
                        directory.mkdir()
                        directory.chmod(mode)
                    else:
                        (directory / 'human.md').write_bytes(b'Concurrent directory content.\n')
                with patch.object(installer, 'replace_entry', replace), self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
                    installer.transaction(self.target, {name: b'Installer file.\n'}, fail_after=1)
                self.assertTrue(directory.is_dir())
                self.assertIn(directory.relative_to(self.target).as_posix(), str(raised.exception))
                if edit == 'replacement':
                    self.assertFalse((self.target / name).exists())
                    self.assertEqual((directory.with_name(directory.name + '-moved') / 'file.md').read_bytes(), b'Installer file.\n')
                else:
                    self.assertEqual((directory / 'human.md').read_bytes(), b'Concurrent directory content.\n')
                    self.assertFalse((self.target / name).exists())
                recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
                self.addCleanup(__import__('shutil').rmtree, recovery)

    def test_parent_swap_at_unlink_never_deletes_replacement_directory_content(self):
        directory = self.target / 'existing-parent'
        directory.mkdir()
        victim = directory / 'owned.md'
        victim.write_bytes(b'Original owned content.\n')
        saved = directory.with_name('saved-parent')
        actual_path_unlink = pathlib.Path.unlink
        actual_fd_unlink = installer.remove_entry
        injected = False
        def swap():
            nonlocal injected
            if not injected:
                directory.rename(saved)
                directory.mkdir()
                victim.write_bytes(b'Concurrent human content.\n')
                injected = True
        def path_unlink(path, *args, **kwargs):
            if path == victim:
                swap()
            return actual_path_unlink(path, *args, **kwargs)
        def fd_unlink(path, *args, **kwargs):
            if pathlib.Path(path).name == victim.name:
                swap()
            return actual_fd_unlink(path, *args, **kwargs)
        index = (self.target / '.git/index').read_bytes()
        with patch.object(pathlib.Path, 'unlink', path_unlink), \
             patch.object(installer, 'remove_entry', fd_unlink), \
             self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
            installer.transaction(self.target, {'existing-parent/owned.md': None}, fail_after=1)
        self.assertTrue(injected)
        self.assertTrue(victim.exists(), 'The replacement directory lost its human file')
        self.assertEqual(victim.read_bytes(), b'Concurrent human content.\n')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(__import__('shutil').rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())['existing-parent/owned.md']
        self.assertEqual((recovery / record['backup']).read_bytes(), b'Original owned content.\n')

    def test_parent_swaps_at_mutation_boundaries_preserve_human_files(self):
        import shutil
        for boundary in ('stage-open', 'replace', 'restore', 'stage-cleanup'):
            for depth in ('parent', 'ancestor'):
                with self.subTest(boundary=boundary, depth=depth):
                    name = boundary + '-' + depth + '/child/owned.md'
                    victim = self.target / name
                    victim.parent.mkdir(parents=True)
                    victim.write_bytes(b'Original owned content.\n')
                    directory = victim.parent if depth == 'parent' else victim.parent.parent
                    saved = directory.with_name(directory.name + '-saved')
                    index = (self.target / '.git/index').read_bytes()
                    actual_open, actual_replace, actual_unlink = installer.os.open, installer.replace_entry, installer.retain_entry
                    injected = False
                    def swap():
                        nonlocal injected
                        if not injected:
                            directory.rename(saved)
                            victim.parent.mkdir(parents=True)
                            victim.write_bytes(b'Concurrent human content.\n')
                            victim.with_name(victim.name + '.wf2-staged').write_bytes(b'Human staging file.\n')
                            injected = True
                    def open_file(path, *args, **kwargs):
                        if boundary == 'stage-open' and pathlib.Path(path).name.endswith('.wf2-staged') and args[0] & installer.os.O_CREAT:
                            swap()
                        if boundary == 'restore' and pathlib.Path(path).name == victim.name + '.wf2-restore' and args[0] & installer.os.O_WRONLY:
                            swap()
                        return actual_open(path, *args, **kwargs)
                    def replace(src, dst, **kwargs):
                        if boundary == 'stage-cleanup':
                            raise OSError('Injected replace failure')
                        if boundary == 'replace':
                            swap()
                        return actual_replace(src, dst, **kwargs)
                    def unlink(path, *args, **kwargs):
                        if boundary == 'stage-cleanup' and pathlib.Path(path).name.endswith('.wf2-staged'):
                            swap()
                        return actual_unlink(path, *args, **kwargs)
                    with patch.object(installer.os, 'open', open_file), patch.object(installer, 'replace_entry', replace), \
                         patch.object(installer, 'retain_entry', unlink), \
                         self.assertRaisesRegex(installer.Conflict, 'Rollback residuals:') as raised:
                        installer.transaction(self.target, {name: b'Installer replacement.\n'}, fail_after=1)
                    self.assertTrue(injected, boundary)
                    self.assertEqual(victim.read_bytes(), b'Concurrent human content.\n')
                    self.assertEqual(victim.with_name(victim.name + '.wf2-staged').read_bytes(), b'Human staging file.\n')
                    self.assertFalse((saved / ('owned.md.wf2-staged' if depth == 'parent' else 'child/owned.md.wf2-staged')).exists())
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
                    self.addCleanup(shutil.rmtree, recovery)
                    record = json.loads((recovery / 'recovery-index.json').read_text())[name]
                    self.assertEqual((recovery / record['backup']).read_bytes(), b'Original owned content.\n')

    def test_forward_apply_preserves_replaced_existing_parent_before_second_write(self):
        import shutil
        name = 'existing-parent/owned.md'
        second = self.target / name
        second.parent.mkdir()
        second.write_bytes(b'Original second file.\n')
        original = (self.target / 'AGENTS.md').read_bytes()
        index = (self.target / '.git/index').read_bytes()
        actual = installer.replace_entry
        calls = 0
        def replace(src, dst, **kwargs):
            nonlocal calls
            if pathlib.Path(src).name.endswith('.wf2-restore'):
                return actual(src, dst, **kwargs)
            calls += 1
            actual(src, dst, **kwargs)
            if calls == 1:
                saved = second.parent.with_name('saved-parent')
                second.parent.rename(saved)
                shutil.copytree(saved, second.parent)
        with patch.object(installer, 'replace_entry', replace), \
             self.assertRaisesRegex(installer.Conflict, 'Rollback residuals: existing-parent') as raised:
            installer.transaction(self.target, {'AGENTS.md': b'First replacement.', name: b'Second replacement.'},
                                  fail_after=2)
        self.assertEqual(calls, 1)  # Replacement parent is rejected before another write.
        self.assertEqual(second.read_bytes(), b'Original second file.\n')
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(shutil.rmtree, recovery)
        record = json.loads((recovery / 'recovery-index.json').read_text())
        self.assertEqual(record['existing-parent']['kind'], 'parent-directory')
        self.assertEqual((recovery / record[name]['backup']).read_bytes(), b'Original second file.\n')

    def test_public_deleted_file_rollback_preserves_replaced_parent_chain(self):
        import shutil
        retired = '.agents/skills/workflow-risk-review/references/retired.md'
        bundle = self.source / '.workflow/bundle.json'
        for depth in ('parent', 'ancestor'):
            for edit in ('replacement', 'same-content', 'symlink'):
                with self.subTest(depth=depth, edit=edit):
                    spec = json.loads(bundle.read_text())
                    spec['assets'][retired] = retired
                    source_file = self.source / retired
                    source_file.write_bytes(b'Original retired asset.\n')
                    bundle.write_text(json.dumps(spec))
                    sha = commit(self.source)
                    target = self.base / ('rollback-' + depth + '-' + edit)
                    init(target)
                    (target / 'README.md').write_text('Human project.\n')
                    commit(target)
                    args = ['setup', '--source', str(self.source), '--revision', sha, '--target', str(target),
                            '--repository', 'fixture/consumer', '--dependency-storage', 'tracked']
                    run(*args, '--apply')
                    commit(target)
                    index = (target / '.git/index').read_bytes()
                    spec['assets'].pop(retired)
                    bundle.write_text(json.dumps(spec))
                    source_file.unlink()
                    operations = self.source / 'docs/workflow/operations.md'
                    operations.write_bytes(operations.read_bytes() + b'Updated operations.\n')
                    sha = commit(self.source)
                    args[args.index('--revision') + 1] = sha
                    deleted = target / retired
                    directory = deleted.parent if depth == 'parent' else deleted.parent.parent
                    saved = directory.with_name(directory.name + '-saved')
                    external = self.base / ('external-' + depth + '-' + edit)
                    actual_remove = installer.remove_entry
                    actual_replace = installer.replace_entry
                    def remove(path, **kw):
                        resolved = operation_path(path, kw.get("dir_fd"))
                        result = actual_remove(path, **kw)
                        if resolved == deleted:
                            directory.rename(saved)
                            if edit == 'same-content':
                                shutil.copytree(saved, directory)
                            elif edit == 'symlink':
                                external.mkdir()
                                (external / 'human.md').write_bytes(b'External human content.\n')
                                directory.symlink_to(external, target_is_directory=True)
                            else:
                                directory.mkdir()
                                (directory / 'human.md').write_bytes(b'Concurrent human content.\n')
                        return result
                    def replace(src, dst, **kw):
                        if str(src).endswith('.wf2-staged'):
                            raise OSError('later apply failure')
                        return actual_replace(src, dst, **kw)
                    with patch.object(installer, 'remove_entry', remove), \
                         patch.object(installer, 'replace_entry', replace), \
                         contextlib.redirect_stdout(io.StringIO()) as out:
                        status = workflow.main(args + ['--apply', '--json'])
                    self.assertEqual(status, 1)
                    message = json.loads(out.getvalue())['findings'][0]['message']
                    self.assertIn('Rollback residuals:', message)
                    self.assertIn(retired, message)
                    self.assertNotIn('original files restored', message)
                    self.assertFalse(deleted.exists())
                    self.assertEqual((target / '.git/index').read_bytes(), index)
                    recovery = pathlib.Path(message.split('recoverable originals: ', 1)[1])
                    self.addCleanup(shutil.rmtree, recovery)
                    record = json.loads((recovery / 'recovery-index.json').read_text())[retired]
                    self.assertEqual((recovery / record['backup']).read_bytes(), b'Original retired asset.\n')
                    self.assertIn('parent_directories', record)
                    self.assertIn(directory.relative_to(target).as_posix(), record['parent_directories'])
                    if edit == 'symlink':
                        self.assertTrue(directory.is_symlink())
                        self.assertEqual((external / 'human.md').read_bytes(), b'External human content.\n')
                    elif edit == 'replacement':
                        self.assertEqual((directory / 'human.md').read_bytes(), b'Concurrent human content.\n')

    def test_rollback_preserves_recreated_deletions_and_edited_new_files(self):
        p = self.target / 'AGENTS.md'
        actual_unlink = installer.remove_entry
        def unlink(path, *args, **kwargs):
            resolved = operation_path(path, kwargs.get("dir_fd"))
            result = actual_unlink(path, *args, **kwargs)
            if resolved == p:
                p.write_bytes(b'Concurrent recreation.\n')
            return result
        for changes in [{'AGENTS.md': None}, {'new.md': b'Installed content.\n'}]:
            name = next(iter(changes))
            path = self.target / name
            patcher = patch.object(installer, 'remove_entry', unlink)
            if name == 'new.md':
                actual_replace = installer.replace_entry
                def replace(src, dst, **kwargs):
                    actual_replace(src, dst, **kwargs)
                    path.write_bytes(b'Concurrent new-file edit.\n')
                patcher = patch.object(installer, 'replace_entry', replace)
            with patcher, self.assertRaisesRegex(installer.Conflict, 'Rollback residuals: ' + name) as raised:
                installer.transaction(self.target, changes, fail_after=1)
            expected = b'Concurrent recreation.\n' if name == 'AGENTS.md' else b'Concurrent new-file edit.\n'
            self.assertEqual(path.read_bytes(), expected)
            recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
            self.addCleanup(__import__('shutil').rmtree, recovery)
            data = json.loads((recovery / 'recovery-index.json').read_text())[name]
            if name == 'AGENTS.md':
                self.assertEqual((recovery / data['backup']).read_bytes(), b'User rule: preserve data.\n')
            else:
                self.assertIsNone(data['backup'])

    def test_doctor_duplicate_names_and_malformed_config(self):
        run(*self.args, '--apply')
        duplicate = self.base / 'other-skills'
        p = duplicate / 'elsewhere/SKILL.md'
        p.parent.mkdir(parents=True)
        p.write_text('---\nname: workflow-risk-review\ndescription: duplicate\n---\n')
        report = run('doctor', '--repo', self.target, '--skill-root', duplicate, expect=1)
        self.assertTrue(any(x['code'] == 'discovery.duplicate' for x in report['findings']))
        p = self.target / '.workflow/config.json'
        c = json.loads(p.read_text())
        c['verification']['local'] = ['echo unsafe']
        p.write_text(json.dumps(c))
        run('doctor', '--repo', self.target, expect=2)

    def test_legacy_instruction_block_and_bad_parent_fail_before_writes(self):
        original = '<!-- Beginning of Workflow Section -->\nUse v1\n<!-- End of Workflow Section -->'
        (self.target / 'AGENTS.md').write_text(original)
        run(*self.args, '--apply', expect=1)
        self.assertEqual((self.target / 'AGENTS.md').read_text(), original)
        self.assertFalse((self.target / '.workflow').exists())
        (self.target / 'AGENTS.md').write_text('Preserve unrelated rule.\n')
        (self.target / '.agents').write_text('human file instead of directory')
        r = run(*self.args, '--apply', expect=1)
        self.assertIn('not a directory', r['findings'][0]['message'])
        self.assertEqual((self.target / '.agents').read_text(), 'human file instead of directory')

    def test_successful_pinned_update_and_marker_modification_conflict(self):
        run(*self.args, '--apply')
        p = self.source / 'docs/workflow/contract.md'
        p.write_text('# Updated contract\n')
        new_sha = commit(self.source)
        args = self.args.copy()
        args[args.index('--revision') + 1] = new_sha
        run(*args, '--apply')
        self.assertEqual((self.target / 'docs/workflow/contract.md').read_text(), '# Updated contract\n')
        self.assertEqual(run(*args, '--apply')['changes'], [])
        agents = self.target / 'AGENTS.md'
        agents.write_text(agents.read_text().replace('Never use obsolete', 'Human changed: Never use obsolete'))
        run(*args, '--apply', expect=1)
        r = run('setup', '--target', self.target, '--uninstall', '--apply', expect=1)
        self.assertIn('AGENTS.md managed block', r['residuals'])
        self.assertIn('Human changed', agents.read_text())

    def test_staging_failure_and_rollback_residual_have_exact_recovery(self):
        # Stage failure happens before destination writes.
        argv = [str(x) for x in self.args] + ['--apply', '--json']
        with patch.object(installer.pathlib.Path, 'write_bytes', side_effect=OSError('staging disk full')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(argv), 1)
        self.assertFalse((self.target / '.workflow').exists())
        p = self.target / 'AGENTS.md'
        original = p.read_bytes()
        actual = installer.os.open
        def fail_restore(path, *args, **kwargs):
            if operation_path(path, kwargs.get('dir_fd')) == p.with_name(p.name + '.wf2-restore') and args[0] & installer.os.O_WRONLY:
                raise OSError('restoration denied')
            return actual(path, *args, **kwargs)
        with patch.object(installer.os, 'open', fail_restore):
            with self.assertRaisesRegex(installer.Conflict, 'Rollback residuals: AGENTS.md') as raised:
                installer.transaction(self.target, {'AGENTS.md': b'replacement'}, fail_after=1)
        recovery = pathlib.Path(str(raised.exception).split('recoverable originals: ', 1)[1])
        self.addCleanup(__import__('shutil').rmtree, recovery)
        index = json.loads((recovery / 'recovery-index.json').read_text())
        self.assertEqual((recovery / index['AGENTS.md']['backup']).read_bytes(), original)
        self.assertIsNotNone(index['AGENTS.md']['mode'])
        p.write_bytes(original)  # explicit fixture recovery before retry
        run(*self.args, '--apply')

    def test_tampered_manifest_path_and_unsupported_source_schema_fail(self):
        run(*self.args, '--apply')
        p = self.target / '.workflow/install-manifest.json'
        m = json.loads(p.read_text())
        m['files']['README.md'] = '0' * 64
        p.write_text(json.dumps(m))
        run('setup', '--target', self.target, '--uninstall', '--apply', expect=2)
        spec = self.source / '.workflow/bundle.json'
        m = json.loads(spec.read_text())
        m['schema_version'] = 99
        spec.write_text(json.dumps(m))
        sha = commit(self.source)
        args = self.args.copy()
        args[args.index('--revision') + 1] = sha
        # Manifest corruption is rejected before considering any new source writes.
        run(*args, '--apply', expect=2)

    def test_source_schema_is_rejected_on_fresh_target(self):
        p = self.source / '.workflow/bundle.json'
        spec = json.loads(p.read_text())
        spec['schema_version'] = 99
        p.write_text(json.dumps(spec))
        sha = commit(self.source)
        fresh = self.base / 'fresh-schema-target'
        init(fresh)
        run('setup', '--source', self.source, '--revision', sha, '--target', fresh, '--repository', 'fixture/fresh', '--apply', expect=2)
        self.assertFalse((fresh / '.workflow').exists())

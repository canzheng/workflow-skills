"""Repository-scoped install/update/uninstall with preflight and rollback."""
import contextlib
import ctypes
import json
import os
import pathlib
import re
import secrets
import shutil
import stat
import tempfile

from core import (Conflict, Invalid, START, END, SKILLS, CI_ASSETS, IGNORE_START, IGNORE_END,
                  SOURCE_URL, REQUIRED_ASSETS, block, config, digest, git, ignore_block, load, manifest,
                  owned, repository, safe, shared, shared_files, source_url, effective_ignore_policy, valid_bundle_version,
                  dependency_policy, relative, untracked_shared_policy, PROJECT_FILES, head_revision, dependency, dependency_files, required_assets, runtime_prefix, RUNTIME_PREFIX, LEGACY_RUNTIME_PREFIX, LEGACY_RUNTIME_ASSETS, retired_runtime_policy, indexed_ancestor_policy)


def source_bundle(source, revision):
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise Invalid('source revision must be a full 40-character commit SHA')
    source = repository(source)
    resolved = git(source, '--no-replace-objects', 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
    if resolved != revision:
        raise Invalid('source revision must identify the commit itself, not an annotated tag object')
    spec = load(safe(source, '.workflow/bundle.json'))
    if not isinstance(spec, dict) or type(spec.get('schema_version')) is not int or spec.get('schema_version') != 1 or not valid_bundle_version(spec.get('bundle_version')) or not isinstance(spec.get('assets'), dict):
        raise Invalid('Unsupported source bundle schema')
    assets = spec['assets']
    if any(not isinstance(dest, str) for dest in assets.values()):
        raise Invalid('Source asset destinations must be repository-relative strings')
    # Validate every entry before filesystem access, including non-skill assets
    # that the optional shared-only installer will not materialize.
    for name, dest in assets.items():
        relative(name)
        relative(dest)
    required = required_assets(assets.values())
    if not required <= set(assets.values()):
        raise Conflict('Incomplete production bundle: required consumer assets omitted: ' + ', '.join(sorted(required - set(assets.values()))))
    paths = {'.workflow/bundle.json', *assets.keys()}
    result = {}
    for name in sorted(paths):
        p = safe(source, name)
        if not p.is_file():
            raise Conflict('Missing source asset: ' + name)
        data = git(source, '--no-replace-objects', 'show', revision + ':' + name)
        if p.read_bytes() != data:
            raise Conflict('Source bytes differ from pinned revision: ' + name)
        if name in assets:
            dest = assets[name]
            if not owned(dest) or dest in result:
                raise Invalid('Unsafe or duplicate bundle destination: ' + str(dest))
            result[dest] = data
    return spec['bundle_version'], result


def preflight_destinations(root, names):
    for name in names:
        p = safe(root, name)
        if p.exists() and not p.is_file():
            raise Conflict('Owned file destination is not a file: ' + name)
        for parent in p.parents:
            if parent == root:
                break
            if parent.exists() and not parent.is_dir():
                raise Conflict('Destination parent is not a directory: ' + str(parent))
        for suffix in ('.wf2-staged', '.wf2-restore', '.wf2-removed'):
            staged = p.with_name(p.name + suffix)
            if staged.exists() or staged.is_symlink():
                raise Conflict('Staging collision: ' + str(staged))


def atomic_rename_function():
    try:
        return ctypes.CDLL(None, use_errno=True).renameat2
    except (OSError, AttributeError) as exc:
        raise Conflict('Atomic filesystem replacement unavailable; Linux renameat2 is required') from exc


def atomic_rename(src, dst, *, src_dir_fd, dst_dir_fd, exchange):
    """Capture the actual replaced entry, or atomically require absence on Linux."""
    rename = atomic_rename_function()
    rename.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    rename.restype = ctypes.c_int
    if rename(src_dir_fd, os.fsencode(src), dst_dir_fd, os.fsencode(dst), 2 if exchange else 1):
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), dst)


def replace_entry(src, dst, *, src_dir_fd, dst_dir_fd, exchange):
    atomic_rename(src, dst, src_dir_fd=src_dir_fd, dst_dir_fd=dst_dir_fd, exchange=exchange)


def remove_entry(basename, *, dir_fd):
    captured = basename + '.wf2-removed'
    replace_entry(basename, captured, src_dir_fd=dir_fd, dst_dir_fd=dir_fd, exchange=False)
    return captured


@contextlib.contextmanager
def private_storage(root, names):
    # Git-private storage keeps retained capture directories out of project state.
    # Explicit shared-only installation uses TMPDIR instead of adopting a project.
    try:
        base = pathlib.Path(git(root, 'rev-parse', '--absolute-git-dir').decode().strip())
    except (Invalid, Conflict):
        base = pathlib.Path(tempfile.gettempdir())
    base_fd = os.open(base, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    fd = None
    try:
        device = os.fstat(base_fd).st_dev
        for name in names:
            parent = (root / name).parent
            while not parent.exists():
                parent = parent.parent
            if parent.stat().st_dev != device:
                raise Conflict('Private capture storage must share the target filesystem; choose a same-filesystem TMPDIR for shared-only installation')
        private = '.wf2-private-' + secrets.token_hex(16)
        os.mkdir(private, mode=0o700, dir_fd=base_fd)
        fd = os.open(private, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=base_fd)
        yield fd, base / private
    finally:
        if fd is not None:
            os.close(fd)
        os.close(base_fd)
        # Linux has no conditional rmdir for an opened directory. Retain storage
        # rather than deleting whichever inode now occupies its public basename.


def publish_directory(basename, *, dir_fd, source_fd, source_name):
    atomic_rename(source_name, basename, src_dir_fd=source_fd, dst_dir_fd=dir_fd, exchange=False)


def retain_entry(basename, *, dir_fd):
    fd = os.open(basename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=dir_fd)
    with os.fdopen(fd, 'rb') as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode):
            raise Conflict('Captured entry is not a regular file: ' + basename)
        return (stream.read(), metadata.st_mode, metadata.st_dev, metadata.st_ino)


@contextlib.contextmanager
def capture_entry(basename, *, dir_fd, storage_fd, storage_path, record=None):
    """Capture the actual entry in retained same-filesystem transaction storage."""
    captured = secrets.token_hex(16) + '-' + basename
    if record:
        record(str(storage_path), captured)
    moved = False
    try:
        atomic_rename(basename, captured, src_dir_fd=dir_fd, dst_dir_fd=storage_fd, exchange=False)
        moved = True
        yield storage_fd, captured, str(storage_path)
    except Exception:
        if moved:
            try:
                os.stat(captured, dir_fd=storage_fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                try:
                    atomic_rename(captured, basename, src_dir_fd=storage_fd, dst_dir_fd=dir_fd, exchange=False)
                    if record:
                        record(None, basename)
                except (OSError, Conflict) as exc:
                    raise Conflict('Quarantine residual: ' + str(storage_path / captured)) from exc
        raise


def transaction(root, changes, fail_after=None):
    """Restore only our unchanged writes; retain backups for conflicting rollback."""
    if not changes:
        return
    preflight_destinations(root, changes)
    atomic_rename_function()  # Missing libc support must fail before creating staging files.
    created_dirs = {}
    created_owners = {}
    originals = {}
    parent_chains = {}
    parent_residuals = set()
    def directory_name(path):
        return path.relative_to(root).as_posix() if path != root and path.is_relative_to(root) else str(path)
    def directory_metadata(path):
        # Optional skill-only targets may start with missing root/ancestors.
        # Revalidate their full path too; never follow a replaced parent symlink.
        for part in (path, *path.parents):
            if part.is_symlink():
                raise Invalid('Symlink directory during rollback: ' + str(part))
        return path.lstat()
    with private_storage(root, changes) as (storage_fd, storage_path), tempfile.TemporaryDirectory(prefix='wf2-stage-') as td:
        stage = pathlib.Path(td)
        for i, (name, data) in enumerate(changes.items()):
            p = safe(root, name)
            parent_chains[name] = {}
            for parent in p.parents:
                if parent.exists():
                    metadata = directory_metadata(parent)
                    if not stat.S_ISDIR(metadata.st_mode):
                        raise Conflict('Destination parent is not a directory: ' + str(parent))
                    parent_chains[name][parent] = (metadata.st_dev, metadata.st_ino)
            originals[name] = (p.read_bytes(), p.stat().st_mode) if p.exists() else None
            if originals[name] is not None:
                (stage / ('backup-' + str(i))).write_bytes(originals[name][0])
            if data is not None:
                (stage / str(i)).write_bytes(data)
        recovery_index = {name: {'backup': 'backup-' + str(i) if originals[name] is not None else None,
                                 'mode': originals[name][1] if originals[name] is not None else None}
                          for i, name in enumerate(changes)}
        (stage / 'recovery-index.json').write_text(json.dumps(recovery_index, indent=2))
        def validate_parents(name, path=None):
            # File absence/inode alone cannot certify a concurrently replaced
            # parent or ancestor. Preserve that directory and our original backup.
            for parent, expected in parent_chains[name].items():
                if path is not None and parent not in path.parents:
                    continue
                try:
                    metadata = directory_metadata(parent)
                    if not stat.S_ISDIR(metadata.st_mode) or (metadata.st_dev, metadata.st_ino) != expected:
                        raise Conflict('Concurrent parent directory replacement: ' + str(parent))
                except (OSError, Invalid, Conflict):
                    directory = directory_name(parent)
                    parent_residuals.add(directory)
                    if directory not in recovery_index:
                        recovery_index[directory] = {'kind': 'parent-directory', 'backup': None,
                                                     'expected_device': expected[0], 'expected_inode': expected[1]}
                    raise
        @contextlib.contextmanager
        def bound_parent(name, path):
            # Walk one component at a time with O_NOFOLLOW. A final-parent
            # O_NOFOLLOW alone would still resolve a swapped ancestor symlink.
            validate_parents(name, path)
            fd = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                current = pathlib.Path(path.anchor)
                for component in path.parent.parts[1:]:
                    child = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    os.close(fd)
                    fd = child
                    current /= component
                    metadata = os.fstat(fd)
                    if (metadata.st_dev, metadata.st_ino) != parent_chains[name].get(current):
                        raise Conflict('Concurrent parent directory replacement: ' + str(current))
                validate_parents(name, path)
                yield fd
            finally:
                os.close(fd)

        def file_state(parent_fd, basename):
            try:
                fd = os.open(basename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
            except FileNotFoundError:
                return None
            with os.fdopen(fd, 'rb') as stream:
                metadata = os.fstat(stream.fileno())
                if not stat.S_ISREG(metadata.st_mode):
                    raise Conflict('Destination is not a regular file: ' + basename)
                return (stream.read(), metadata.st_mode, metadata.st_dev, metadata.st_ino)

        def record_parents(name):
            recovery_index[name]['parent_directories'] = {
                directory_name(parent): {'device': identity[0], 'inode': identity[1]}
                for parent, identity in parent_chains[name].items()}
        for name in changes:
            record_parents(name)
        applied = {}
        staging_residuals = []

        def cleanup_entry(name, parent_fd, basename, expected):
            try:
                staged = file_state(parent_fd, basename)
                if staged is not None:
                    if staged != expected:
                        raise Conflict('Concurrent staging edit: ' + name)
                    def record_capture(private, captured):
                        if private is None:
                            recovery_index[name].pop('quarantine', None)
                            recovery_index[name]['restored_to'] = name
                        else:
                            recovery_index[name]['quarantine'] = (pathlib.Path(name).parent / private / captured).as_posix()
                    with capture_entry(basename, dir_fd=parent_fd, storage_fd=storage_fd, storage_path=storage_path, record=record_capture) as (private_fd, captured, private):
                        if file_state(private_fd, captured) != expected:
                            raise Conflict('Concurrent staging edit: ' + name)
                        if file_state(parent_fd, basename) is not None:
                            raise Conflict('Concurrent staging recreation: ' + name)
                        # Conditional unlink-by-inode is unavailable too. Keep
                        # captured files, rather than deleting a replaced name.
                        actual = retain_entry(captured, dir_fd=private_fd)
                        if actual != expected:
                            backup = 'concurrent-' + str(len(recovery_index))
                            (stage / backup).write_bytes(actual[0])
                            recovery_index[name]['concurrent_backup'] = backup
                            recovery_index[name]['concurrent_mode'] = actual[1]
                            raise Conflict('Concurrent displaced-inode edit: ' + name)
                        if file_state(parent_fd, basename) is not None:
                            raise Conflict('Concurrent staging recreation: ' + name)
            except (OSError, Invalid, Conflict) as cleanup_error:
                staging_residuals.append(name)
                raise Conflict('Staging cleanup residual: ' + name) from cleanup_error

        @contextlib.contextmanager
        def staged_file(name, p, parent_fd, data, mode, suffix):
            basename, tmp_name = p.name + suffix, name + suffix
            expected = [None]
            created = False
            try:
                fd = os.open(basename, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             os.O_NOFOLLOW, 0o666, dir_fd=parent_fd)
                created = True
                with os.fdopen(fd, 'wb') as output:
                    metadata = os.fstat(output.fileno())
                    expected[0] = (b'', metadata.st_mode, metadata.st_dev, metadata.st_ino)
                    recovery_index[tmp_name] = {
                        'kind': 'staging', 'backup': None, 'mode': None,
                        'created_mode': metadata.st_mode, 'created_device': metadata.st_dev,
                        'created_inode': metadata.st_ino}
                    if mode is not None:
                        os.fchmod(output.fileno(), mode)
                    output.write(data)
                    output.flush()
                    metadata = os.fstat(output.fileno())
                    expected[0] = (data, metadata.st_mode, metadata.st_dev, metadata.st_ino)
                if file_state(parent_fd, basename) != expected[0]:
                    raise Conflict('Concurrent staging edit: ' + tmp_name)
                yield basename, expected
            finally:
                if created:
                    cleanup_entry(tmp_name, parent_fd, basename, expected[0])
                validate_parents(name)

        def checked_replace(name, p, parent_fd, basename, staging, expected_dst, record=None):
            expected_src = staging[0]
            validate_parents(name)
            try:
                replace_entry(basename, p.name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd,
                              exchange=expected_dst is not None)
            except (OSError, Conflict):
                try:
                    changed = file_state(parent_fd, p.name) != expected_dst
                except (OSError, Invalid, Conflict):
                    changed = True
                if changed:
                    staging_residuals.append(name)
                raise
            # An exchange retains the actual displaced inode at the staging name.
            # Never truncate a live destination or discard the unvalidated input.
            staging[0] = expected_dst
            if expected_dst is not None:
                recovery_index[name + ('.wf2-restore' if basename.endswith('.wf2-restore') else '.wf2-staged')]['displaced_from'] = name
            if record:
                record(expected_src)
            if expected_dst is not None:
                try:
                    captured = file_state(parent_fd, basename)
                except (OSError, Invalid, Conflict):
                    captured = None
                if captured != expected_dst:
                    # Put the actual human entry back when our own write remains
                    # unchanged. Exchange also retains any late competing entry.
                    if file_state(parent_fd, p.name) == expected_src:
                        replace_entry(basename, p.name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd,
                                      exchange=True)
                        staging[0] = expected_src
                    raise Conflict('Concurrent destination edit captured during replacement: ' + name)
            if file_state(parent_fd, p.name) != expected_src:
                raise Conflict('Concurrent destination change after replacement: ' + name)

        def checked_remove(name, p, parent_fd, expected, record=None):
            validate_parents(name)
            try:
                captured = remove_entry(p.name, dir_fd=parent_fd)
            except (OSError, Conflict):
                try:
                    changed = file_state(parent_fd, p.name) != expected
                except (OSError, Invalid, Conflict):
                    changed = True
                if changed:
                    staging_residuals.append(name)
                raise
            captured_name = name + '.wf2-removed'
            recovery_index[captured_name] = {
                'kind': 'capture', 'backup': None, 'displaced_from': name,
                'expected_mode': expected[1], 'expected_device': expected[2], 'expected_inode': expected[3]}
            if record:
                record()
            try:
                try:
                    state = file_state(parent_fd, captured)
                except (OSError, Invalid, Conflict):
                    state = None
                if state != expected:
                    try:
                        replace_entry(captured, p.name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd, exchange=False)
                    except (OSError, Conflict):
                        staging_residuals.append(captured_name)
                    staging_residuals.append(name)
                    raise Conflict('Concurrent deletion edit captured: ' + name)
                if file_state(parent_fd, p.name) is not None:
                    raise Conflict('Concurrent destination recreation: ' + name)
            finally:
                cleanup_entry(captured_name, parent_fd, captured, expected)
                validate_parents(name)

        try:
            for i, (name, data) in enumerate(changes.items()):
                p = safe(root, name)
                for parent in p.parents:
                    if parent in created_dirs:
                        parent_chains[name].setdefault(parent, created_dirs[parent][1:])
                record_parents(name)
                validate_parents(name)
                now = (p.read_bytes(), p.stat().st_mode) if p.exists() else None
                if now != originals[name]:
                    raise Conflict('Concurrent local edit detected: ' + name)
                parents = []
                for parent in p.parents:
                    if parent.exists():
                        break
                    parents.append(parent)
                for parent in reversed(parents):
                    directory_metadata(parent.parent)
                    with bound_parent(name, parent) as parent_fd:
                        staging_name = 'directory-' + secrets.token_hex(16)
                        os.mkdir(staging_name, dir_fd=storage_fd)
                        child_fd = os.open(staging_name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=storage_fd)
                        try:
                            metadata = os.fstat(child_fd)
                            created_owners[parent] = name
                            created_dirs[parent] = (metadata.st_mode, metadata.st_dev, metadata.st_ino)
                            recovery_index[directory_name(parent)] = {
                                'kind': 'directory', 'backup': None, 'mode': None,
                                'created_mode': metadata.st_mode, 'created_device': metadata.st_dev,
                                'created_inode': metadata.st_ino,
                                'creation_staging': str(storage_path / staging_name)}
                            publish_directory(parent.name, dir_fd=parent_fd, source_fd=storage_fd, source_name=staging_name)
                            actual = os.stat(parent.name, dir_fd=parent_fd, follow_symlinks=False)
                            if (actual.st_mode, actual.st_dev, actual.st_ino) != created_dirs[parent]:
                                raise Conflict('Concurrent directory publication change: ' + directory_name(parent))
                        finally:
                            os.close(child_fd)
                    parent_chains[name][parent] = (metadata.st_dev, metadata.st_ino)
                for parent in p.parents:
                    if parent in created_dirs:
                        parent_chains[name].setdefault(parent, created_dirs[parent][1:])
                record_parents(name)
                validate_parents(name)
                with bound_parent(name, p) as parent_fd:
                    current = file_state(parent_fd, p.name)
                    if (current[:2] if current else None) != originals[name]:
                        raise Conflict('Concurrent local edit detected: ' + name)
                    if data is None:
                        if current is not None:
                            checked_remove(name, p, parent_fd, current, lambda: applied.__setitem__(name, None))
                        else:
                            applied[name] = None
                    else:
                        mode = originals[name][1] if originals[name] else None
                        with staged_file(name, p, parent_fd, data, mode, '.wf2-staged') as (basename, staging):
                            checked_replace(name, p, parent_fd, basename, staging, current,
                                            lambda state: applied.__setitem__(name, state))
                validate_parents(name)
                if fail_after is not None and len(applied) == fail_after:
                    raise OSError('Injected apply failure')
        except Exception as exc:
            residuals = list(staging_residuals)
            for name in reversed(applied):
                try:
                    p = root / name
                    with bound_parent(name, p) as parent_fd:
                        current = file_state(parent_fd, p.name)
                        if current != applied[name]:
                            raise Conflict('Concurrent edit during rollback: ' + name)
                        original = originals[name]
                        if original is None:
                            if current is not None:
                                checked_remove(name, p, parent_fd, current)
                        else:
                            with staged_file(name, p, parent_fd, original[0], original[1], '.wf2-restore') as (basename, staging):
                                checked_replace(name, p, parent_fd, basename, staging, current)
                    validate_parents(name)
                except (OSError, Invalid, Conflict):
                    residuals.append(name)
            residuals.extend(name for name in staging_residuals if name not in residuals)
            residuals.extend(sorted(parent_residuals))
            for p in sorted(created_dirs, key=lambda p: len(p.parts), reverse=True):
                name = directory_name(p)
                try:
                    with bound_parent(created_owners[p], p) as parent_fd:
                        metadata = os.stat(p.name, dir_fd=parent_fd, follow_symlinks=False)
                        if not stat.S_ISDIR(metadata.st_mode) or (metadata.st_mode, metadata.st_dev, metadata.st_ino) != created_dirs[p]:
                            raise Conflict('Concurrent directory change during rollback: ' + name)
                        def record_capture(private, captured):
                            if private is None:
                                recovery_index[name].pop('quarantine', None)
                                recovery_index[name]['restored_to'] = name
                            else:
                                recovery_index[name]['quarantine'] = directory_name(p.parent / private / captured)
                        with capture_entry(p.name, dir_fd=parent_fd, storage_fd=storage_fd, storage_path=storage_path, record=record_capture) as (private_fd, captured, private):
                            actual = os.stat(captured, dir_fd=private_fd, follow_symlinks=False)
                            if not stat.S_ISDIR(actual.st_mode) or (actual.st_mode, actual.st_dev, actual.st_ino) != created_dirs[p]:
                                raise Conflict('Concurrent directory replacement during rollback: ' + name)
                            try:
                                os.stat(p.name, dir_fd=parent_fd, follow_symlinks=False)
                            except FileNotFoundError:
                                pass
                            else:
                                raise Conflict('Concurrent directory recreation during rollback: ' + name)
                            captured_fd = os.open(captured, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=private_fd)
                            try:
                                if os.listdir(captured_fd):
                                    raise Conflict('Concurrent directory content during rollback: ' + name)
                            finally:
                                os.close(captured_fd)
                            try:
                                os.stat(p.name, dir_fd=parent_fd, follow_symlinks=False)
                            except FileNotFoundError:
                                pass
                            else:
                                raise Conflict('Concurrent directory recreation during rollback: ' + name)
                except FileNotFoundError:
                    pass  # already absent; never recreate a concurrent deletion
                except (OSError, Invalid, Conflict):
                    residuals.append(name)
            if residuals:
                (stage / 'recovery-index.json').write_text(json.dumps(recovery_index, indent=2))
                recovery = pathlib.Path(tempfile.mkdtemp(prefix='wf2-recovery-'))
                shutil.copytree(stage, recovery, dirs_exist_ok=True)
                raise Conflict('Rollback residuals: ' + ', '.join(residuals) + '; recoverable originals: ' + str(recovery)) from exc
            raise Conflict('Apply failed; original files restored: ' + str(exc)) from exc


def setup(args):
    root = repository(args.target)
    indexed = set(os.fsdecode(git(root, 'ls-files', '--cached', '-z')).split('\0')) - {''}
    committed = (set(os.fsdecode(git(root, 'ls-tree', '-r', '--name-only', '-z', 'HEAD')).split('\0')) - {''}
                 if head_revision(root) else set())
    index_owned = indexed | committed
    if not args.uninstall:
        for name in PROJECT_FILES | {'.gitignore'}:
            if name in index_owned and not safe(root, name).exists():
                raise Conflict('Indexed project policy deletion preserved: ' + name)
    old = manifest(root)
    agents = safe(root, 'AGENTS.md')
    text = agents.read_text() if agents.exists() else ''
    current = block(text)
    ignore_path = safe(root, '.gitignore')
    ignore_text = ignore_path.read_text(encoding='utf-8') if ignore_path.exists() else ''
    current_ignore = ignore_block(ignore_text)
    if not args.uninstall and ('<!-- Beginning of Workflow Section -->' in text or
                               'bash install.sh' in text or 'must invoke `start-task`' in text):
        raise Conflict('Active legacy instruction routing; inspect migration and perform a bounded cutover first')
    if not old and current:
        raise Conflict('Unmanaged workflow-v2 block; resolve ownership first')
    changes, residuals = {}, []
    if args.uninstall:
        if not old:
            return [], []
        remaining = {}
        for name, h in old['files'].items():
            p = safe(root, name)
            if p.exists() and digest(p.read_bytes()) != h:
                residuals.append(name)
                remaining[name] = h
            elif p.exists():
                changes[name] = None
        if current and digest(current.encode()) == old['agents_block_hash']:
            changes['AGENTS.md'] = text.replace(current, '', 1).encode()
        elif current:
            residuals.append('AGENTS.md managed block')
        if old['schema_version'] in (2, 4, 5) and current_ignore:
            if digest(current_ignore.encode()) != old['gitignore_block_hash']:
                residuals.append('.gitignore managed block')
            elif not any(dependency(name, old) for name in remaining):
                changes['.gitignore'] = ignore_text.replace(current_ignore + ('\n' if current_ignore + '\n' in ignore_text else ''), '', 1).encode()
        mpath = '.workflow/install-manifest.json'
        if residuals:
            updated = {**old, 'files': remaining}
            changes[mpath] = (json.dumps(updated, indent=2) + '\n').encode()
        else:
            changes[mpath] = None
    else:
        if not args.source or not args.revision:
            raise Invalid('setup requires --source and --revision')
        version, assets = source_bundle(args.source, args.revision)
        url = source_url(getattr(args, 'source_url', SOURCE_URL))
        if args.skill_storage == 'ignored' and runtime_prefix(assets) != RUNTIME_PREFIX:
            raise Conflict('Ignored dependency runtime layout requires .agents/tools/workflow/; keep legacy runtime tracked or update the source bundle')
        if args.skill_storage == 'ignored' and (not old or old['schema_version'] in (4, 5)):
            untracked_shared_policy(root, runtime=runtime_prefix(assets))
        # An indexed/HEAD-owned file or gitlink can be an absent destination
        # ancestor. Never repurpose its deletion as an installer directory.
        indexed_ancestor_policy(assets, index_owned)
        if runtime_prefix(assets) == RUNTIME_PREFIX:
            if not old or runtime_prefix(old['files']) == LEGACY_RUNTIME_PREFIX:
                for name in LEGACY_RUNTIME_ASSETS:
                    if name in index_owned and (not old or name not in old['files']):
                        raise Conflict('Unmanaged legacy runtime collision preserved: ' + name)
            else:
                retired_runtime_policy(assets, indexed)
        for name in dependency_files(root, {'schema_version': 5, 'files': assets}):
            safe(root, name)
            if name not in assets and (not old or name not in old['files']):
                raise Conflict('Unmanaged shared dependency asset: ' + name)
        if current_ignore and (not old or old['schema_version'] not in (2, 4, 5)):
            raise Conflict('Unmanaged shared-dependency gitignore block; resolve ownership first')
        if old and old['schema_version'] in (2, 4, 5) and (not current_ignore or digest(current_ignore.encode()) != old['gitignore_block_hash']):
            raise Conflict('Managed shared-dependency ignore block modified or missing')
        # Existing configuration is user owned and must remain valid.
        cp = safe(root, '.workflow/config.json')
        if cp.exists():
            config(root)
        if old:
            if not current or digest(current.encode()) != old['agents_block_hash']:
                raise Conflict('Managed AGENTS block modified or missing')
            if old['schema_version'] in (4, 5):
                dependency_policy(root, old)
            for name, h in old['files'].items():
                p = safe(root, name)
                if dependency(name, old) and old['schema_version'] in (2, 4, 5) and not p.exists():
                    continue  # Legacy ignored dependencies may be absent in fresh clones.
                if not p.is_file() or digest(p.read_bytes()) != h:
                    raise Conflict('Modified/missing managed file: ' + name)
                if name not in assets:
                    changes[name] = None
        for name, data in assets.items():
            p = safe(root, name)
            if (p.exists() or name in index_owned) and (not old or name not in old['files']):
                raise Conflict('Unmanaged indexed/working target collision: ' + name)
            if not p.exists() or p.read_bytes() != data:
                changes[name] = data
        ignored_dependency = args.skill_storage == 'ignored'
        entry = (START + '\nUse the repo-local workflow-skills v2 in .agents/skills/. Read\n'
                 'docs/workflow/contract.md and docs/workflow/README.md.\n'
                 'Run pinned bootstrap before Codex starts; then verify with\n'
                 'python3 ' + runtime_prefix(assets) + 'workflow.py check --repo .\n'
                 'Historical planning directories do not select v1. Never use obsolete\n'
                 'repository wrappers or global installation here. Preserve unrelated rules.\n' + END)
        new_text = text.replace(current, entry, 1) if current else text + ('\n' if text and not text.endswith('\n') else '') + entry + '\n'
        if new_text != text:
            changes['AGENTS.md'] = new_text.encode()
        # Only the verified schema-2 owned block is removed on explicit update.
        # Other root/nested/global ignores are preserved and checked for conflicts.
        new_ignore = ignore_text.replace(current_ignore + ('\n' if current_ignore + '\n' in ignore_text else ''), '', 1) if current_ignore else ignore_text
        if ignored_dependency:
            dependency_ignore = (IGNORE_START + '\n' + '\n'.join('/.agents/skills/' + s + '/' for s in SKILLS) + '\n/' + runtime_prefix(assets) + '\n' + IGNORE_END)
            new_ignore += ('\n' if new_ignore and not new_ignore.endswith('\n') else '') + dependency_ignore + '\n'
        effective_ignore_policy(root, assets, proposed=new_ignore, ignored_shared=ignored_dependency, ignored_runtime=ignored_dependency)
        if new_ignore != ignore_text:
            changes['.gitignore'] = new_ignore.encode()
        if not cp.exists():
            if not args.repository or not re.fullmatch(r'[\w.-]+/[\w.-]+', args.repository):
                raise Invalid('Fresh setup requires --repository owner/name')
            c = dict(schema_version=1, workflow='github-v2', repository=args.repository,
                     docs_index='docs/workflow/README.md', contract='docs/workflow/contract.md',
                     openspec='on-demand', verification={'local': [['python3', runtime_prefix(assets) + 'workflow.py', 'check', '--repo', '.']], 'integration': []})
            changes['.workflow/config.json'] = (json.dumps(c, indent=2) + '\n').encode()
        m = dict(schema_version=5 if ignored_dependency else 3, skill_storage=args.skill_storage, bundle_version=version, source_revision=args.revision, source_url=url,
                 files={name: digest(data) for name, data in assets.items()}, agents_block_hash=digest(entry.encode()))
        if ignored_dependency:
            m['dependency_storage'] = 'ignored'
            m['gitignore_block_hash'] = digest(dependency_ignore.encode())
        data = (json.dumps(m, indent=2) + '\n').encode()
        p = safe(root, '.workflow/install-manifest.json')
        if not p.exists() or p.read_bytes() != data:
            changes['.workflow/install-manifest.json'] = data
    preflight_destinations(root, changes)
    if args.apply:
        transaction(root, changes)
    return list(changes), residuals


def install_skills(args):
    """Explicit optional global installation; never change project policy/auth/config."""
    root = pathlib.Path(args.target).absolute()
    if not pathlib.Path(args.target).is_absolute():
        raise Invalid('Global/custom skill target must be an explicit absolute path')
    for p in (root, *root.parents):
        if p.is_symlink():
            raise Invalid('Global skill target contains a symlink')
        if p.exists() and not p.is_dir():
            raise Invalid('Global skill target is not a directory')
    pin_name = '.workflow-skills-install.json'
    pin = safe(root, pin_name)
    old = load(pin) if pin.exists() else None
    if old is not None:
        if (not isinstance(old, dict) or type(old.get('schema_version')) is not int or
                old['schema_version'] != 1 or not isinstance(old.get('files'), dict) or
                not re.fullmatch(r'[0-9a-f]{40}', str(old.get('source_revision', ''))) or
                not valid_bundle_version(old.get('bundle_version'))):
            raise Invalid('Invalid shared-skills installation provenance')
        source_url(old.get('source_url'))
        for name, h in old['files'].items():
            if (not any(name.startswith(s + '/') for s in SKILLS) or
                    not isinstance(h, str) or not re.fullmatch(r'[0-9a-f]{64}', h)):
                raise Invalid('Unsafe shared-skills provenance path/hash')
            safe(root, name)
    changes, residuals = {}, []
    if args.uninstall:
        if not old:
            return [], []
        remaining = {}
        for name, h in old['files'].items():
            p = safe(root, name)
            if p.exists() and (not p.is_file() or digest(p.read_bytes()) != h):
                residuals.append(name); remaining[name] = h
            elif p.exists():
                changes[name] = None
        changes[pin_name] = (json.dumps({**old, 'files': remaining}, indent=2) + '\n').encode() if residuals else None
    else:
        if not args.source or not args.revision:
            raise Invalid('install-skills requires --source and --revision')
        version, assets = source_bundle(args.source, args.revision)
        prefix = '.agents/skills/'
        skills = {name[len(prefix):]: data for name, data in assets.items() if shared(name)}
        for s in SKILLS:
            folder = safe(root, s)
            if folder.exists() and not folder.is_dir():
                raise Conflict('Shared skill destination is not a directory: ' + s)
            for p in folder.rglob('*') if folder.exists() else ():
                name = p.relative_to(root).as_posix(); safe(root, name)
                if p.is_file() and (not old or name not in old['files']):
                    raise Conflict('Unmanaged global shared-skill collision: ' + name)
        if old:
            for name, h in old['files'].items():
                p = safe(root, name)
                if not p.is_file() or digest(p.read_bytes()) != h:
                    raise Conflict('Modified/missing global skill preserved: ' + name)
                if name not in skills:
                    changes[name] = None
        for name, data in skills.items():
            p = safe(root, name)
            if p.exists() and (not old or name not in old['files']):
                raise Conflict('Unmanaged global shared-skill collision: ' + name)
            if not p.exists() or p.read_bytes() != data:
                changes[name] = data
        m = dict(schema_version=1, bundle_version=version, source_revision=args.revision,
                 source_url=source_url(args.source_url), files={n: digest(d) for n, d in skills.items()})
        data = (json.dumps(m, indent=2) + '\n').encode()
        if not pin.exists() or pin.read_bytes() != data:
            changes[pin_name] = data
    preflight_destinations(root, changes)
    if args.apply:
        transaction(root, changes)
    return list(changes), residuals

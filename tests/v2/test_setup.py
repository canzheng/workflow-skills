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
        assets[name] = name
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
                         ('.github/workflows/pr-metadata.yml', '.github/workflows/workflow-v2-pr-metadata.yml')]:
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
        p = self.target / 'tools/workflow/core.py'
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
        cp.write_text(json.dumps(c))
        run(*self.args, '--apply')
        self.assertEqual(json.loads(cp.read_text())['openspec'], 'disabled')
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
        actual = installer.os.replace
        calls = 0
        def fail(src, dst):
            nonlocal calls
            calls += 1
            if calls == 4:
                raise OSError('simulated disk failure')
            return actual(src, dst)
        argv = [str(x) for x in self.args] + ['--apply', '--json']
        with patch.object(installer.os, 'replace', side_effect=fail), contextlib.redirect_stdout(io.StringIO()) as out:
            code = workflow.main(argv)
        self.assertEqual(code, 1)
        self.assertIn('original files restored', out.getvalue())
        self.assertEqual((self.target / 'AGENTS.md').read_bytes(), original)
        self.assertFalse((self.target / '.workflow').exists())
        run(*self.args, '--apply')

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
        (self.target / 'tools').write_text('human file instead of directory')
        r = run(*self.args, '--apply', expect=1)
        self.assertIn('not a directory', r['findings'][0]['message'])
        self.assertFalse((self.target / '.agents').exists())

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
        actual = pathlib.Path.write_bytes
        def fail_restore(path, data):
            if path == p:
                raise OSError('restoration denied')
            return actual(path, data)
        with patch.object(pathlib.Path, 'write_bytes', fail_restore):
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

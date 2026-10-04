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
    r = subprocess.run([sys.executable, str(TOOLS / 'workflow.py'), *map(str, args), '--json'], capture_output=True, text=True)
    if r.returncode != expect:
        raise AssertionError((r.returncode, r.stdout, r.stderr))
    return json.loads(r.stdout)


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
    for file in ('core.py', 'setup.py', 'workflow.py'):
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
        self.args = ['setup', '--source', self.source, '--revision', self.sha,
                     '--target', self.target, '--repository', 'fixture/consumer']

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

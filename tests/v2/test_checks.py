import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

from test_setup import ROOT, init, fixture_source, commit, run
from core import LEGACY_RUNTIME_PREFIX, RUNTIME_PREFIX

BODY = '''## Assignment
Approved bounded source.
## Changes
Repair existing behavior.
## Evidence
Local Python test passed; exact revision recorded in handoff, merge pending.
## Documentation
No impact: restores accurately documented existing behavior.
## Remaining
Required review and merge pending.
'''


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.source, self.target = self.root / 'source', self.root / 'consumer'
        sha = fixture_source(self.source)
        self.sha = sha
        init(self.target)
        (self.target / 'original').write_text('baseline')
        commit(self.target)
        run('setup', '--source', self.source, '--revision', sha, '--target', self.target, '--repository', 'fixture/consumer', '--apply')

    def snapshot(self, body):
        p = self.root / 'pr.json'
        p.write_text(json.dumps(dict(repository='fixture/consumer', body=body)))
        return p

    def test_public_installed_checker_and_no_impact_pr(self):
        run('check', '--repo', self.target)
        run('check', '--repo', self.target, '--pr-json', self.snapshot(BODY))
        installed = self.target / '.agents/tools/workflow/workflow.py'
        r = subprocess.run(['python3', str(installed), 'check', '--repo', str(self.target)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_source_and_installed_checks_agree_for_supported_tracked_layouts(self):
        (self.source / '.workflow/config.json').write_bytes((self.target / '.workflow/config.json').read_bytes())
        bundle = self.source / '.workflow/bundle.json'
        original = json.loads(bundle.read_text())
        for i, prefix in enumerate((RUNTIME_PREFIX, LEGACY_RUNTIME_PREFIX)):
            with self.subTest(layout=prefix):
                spec = json.loads(json.dumps(original))
                spec['assets'] = {src: dest.replace(RUNTIME_PREFIX, prefix, 1)
                                  for src, dest in spec['assets'].items()}
                bundle.write_text(json.dumps(spec))
                sha = commit(self.source)
                target = self.root / ('tracked-layout-' + str(i))
                init(target)
                run('setup', '--source', self.source, '--revision', sha, '--target', target,
                    '--repository', 'fixture/consumer', '--dependency-storage', 'tracked', '--apply')
                commit(target)
                installed = target / prefix / 'workflow.py'
                result = subprocess.run([sys.executable, str(installed), 'check', '--repo', str(target),
                                         '--run-local', '--json'], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue(json.loads(result.stdout)['ok'])
                index = (self.source / '.git/index').read_bytes()
                run('check', '--repo', self.source)
                self.assertEqual((self.source / '.git/index').read_bytes(), index)

    def test_source_check_rejects_omitted_installed_runtime_mapping(self):
        (self.source / '.workflow/config.json').write_bytes((self.target / '.workflow/config.json').read_bytes())
        run('check', '--repo', self.source)
        p = self.source / '.workflow/bundle.json'
        original = json.loads(p.read_text())
        for prefix in (RUNTIME_PREFIX, LEGACY_RUNTIME_PREFIX):
            for module in ('workflow.py', 'core.py', 'setup.py', 'bootstrap.py', 'checks.py', 'records.py', 'migration.py'):
                with self.subTest(layout=prefix, module=module):
                    spec = json.loads(json.dumps(original))
                    spec['assets'] = {src: dest.replace(RUNTIME_PREFIX, prefix, 1)
                                      for src, dest in spec['assets'].items()}
                    del spec['assets']['tools/workflow/' + module]
                    p.write_text(json.dumps(spec))
                    result = run('check', '--repo', self.source, expect=1)
                    missing = next(x for x in result['findings'] if x['code'] == 'bundle.incomplete')
                    self.assertIn(prefix + module, missing['message'])

    def test_source_check_and_setup_reject_invalid_bundle_versions(self):
        (self.source / '.workflow/config.json').write_bytes((self.target / '.workflow/config.json').read_bytes())
        p = self.source / '.workflow/bundle.json'
        original = json.loads(p.read_text())
        for version in ('not-a-version', '1.0.0', '2.0', '2.0.0-extra'):
            with self.subTest(version=version):
                spec = dict(original, bundle_version=version)
                p.write_text(json.dumps(spec))
                sha = commit(self.source)
                checked = run('check', '--repo', self.source, expect=2)
                self.assertFalse(checked['ok'])
                run('setup', '--source', self.source, '--revision', sha, '--target', self.target, '--repository', 'fixture/consumer', '--apply', expect=2)
        p.write_text(json.dumps(original))
        run('check', '--repo', self.source)

    def test_installed_manifest_cannot_hide_deleted_runtime_or_ci_asset(self):
        pin = self.target / '.workflow/install-manifest.json'
        original = pin.read_bytes()
        for name in ('.agents/tools/workflow/migration.py', '.github/workflows/workflow-v2-verify.yml', '.github/workflows/workflow-v2-pr-metadata.yml',
                     '.github/ISSUE_TEMPLATE/feature.yml', '.github/ISSUE_TEMPLATE/bug.yml', '.github/pull_request_template.md',
                     'docs/workflow/contract.md', 'docs/workflow/README.md', 'docs/workflow/development.md', 'docs/workflow/operations.md',
                     '.agents/skills/workflow-risk-review/references/methods.md'):
            with self.subTest(asset=name):
                asset = self.target / name
                contents = asset.read_bytes()
                m = json.loads(original)
                del m['files'][name]
                asset.unlink()
                pin.write_text(json.dumps(m))
                result = run('check', '--repo', self.target, expect=1)
                self.assertTrue(any(x['code'] == 'bundle.incomplete' for x in result['findings']))
                run('doctor', '--repo', self.target, expect=1)
                run('bootstrap', '--repo', self.target, '--apply', expect=1)
                self.assertFalse(asset.exists())
                self.assertEqual(json.loads(pin.read_text()), m)
                asset.write_bytes(contents)
                pin.write_bytes(original)

    def test_installed_manifest_rejects_invalid_versions_before_bootstrap(self):
        p = self.target / '.workflow/install-manifest.json'
        original = json.loads(p.read_text())
        before = subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage'])
        for version in ('not-a-version', '1.0.0', '2.0', '2.0.0-extra'):
            with self.subTest(version=version):
                p.write_text(json.dumps(dict(original, bundle_version=version)))
                contents = p.read_bytes()
                for command in ('check', 'doctor'):
                    run(command, '--repo', self.target, expect=2)
                run('bootstrap', '--repo', self.target, '--apply', expect=2)
                self.assertEqual(p.read_bytes(), contents)
                self.assertEqual(subprocess.check_output(['git', '-C', str(self.target), 'ls-files', '--stage']), before)

    def test_missing_sections_broken_files_and_anchors_fail(self):
        p = self.snapshot(BODY.replace('## Documentation', '## Unrelated'))
        r = run('check', '--repo', self.target, '--pr-json', p, expect=1)
        self.assertTrue(any(x['code'] == 'pr.section' for x in r['findings']))
        for link in ('[missing](docs/missing.md)', '[missing](docs/workflow/README.md#absent)'):
            r = run('check', '--repo', self.target, '--pr-json', self.snapshot(BODY + link), expect=1)
            self.assertTrue(any(x['code'].startswith('links.') for x in r['findings']))
        run('check', '--repo', self.target, '--pr-json', self.snapshot(BODY + '\n## Evidence\nDuplicated'), expect=1)

    def test_local_doc_link_and_owned_modifications_are_detected(self):
        p = self.target / 'README.md'
        p.write_text('[broken](docs/absent.md)')
        r = run('check', '--repo', self.target, expect=1)
        self.assertTrue(any(x['code'] == 'links.path' for x in r['findings']))
        p.unlink()
        p = self.target / '.agents/skills/workflow-risk-review/SKILL.md'
        p.write_text('modified owned content')
        r = run('check', '--repo', self.target, expect=1)
        self.assertTrue(any(x['code'] == 'bundle.modified' for x in r['findings']))

    def test_untrusted_metadata_and_head_blobs_cannot_execute(self):
        marker = self.root / 'DO_NOT_CREATE'
        malicious = f'$(touch {marker}) `touch {marker}`; touch {marker}'
        # Malicious executable at the PR head is only read through Git data.
        (self.target / 'evil.py').write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
        sha = commit(self.target)
        snapshot = dict(repository={'full_name': 'fixture/consumer'}, pull_request=dict(body=BODY + '\n' + malicious + '\n[code](evil.py)', head={'sha': sha}, base={'repo': {'full_name': 'fixture/consumer'}}))
        p = self.root / 'event.json'
        p.write_text(json.dumps(snapshot))
        run('check', '--repo', self.target, '--pr-json', p, '--metadata-only')
        self.assertFalse(marker.exists())
        snapshot['pull_request']['head']['sha'] = '; touch ' + str(marker)
        p.write_text(json.dumps(snapshot))
        run('check', '--repo', self.target, '--pr-json', p, '--metadata-only', expect=2)
        self.assertFalse(marker.exists())

    def test_wrong_repository_and_invalid_schema_are_invocation_errors(self):
        p = self.snapshot(BODY)
        s = json.loads(p.read_text())
        s['repository'] = 'wrong/repo'
        p.write_text(json.dumps(s))
        run('check', '--repo', self.target, '--pr-json', p, expect=2)
        cp = self.target / '.workflow/config.json'
        c = json.loads(cp.read_text())
        c['contract'] = '../outside.md'
        cp.write_text(json.dumps(c))
        run('check', '--repo', self.target, expect=2)

    def test_issue_closure_audit_distinguishes_mechanical_and_semantic_limits(self):
        p = self.root / 'issues.json'
        p.write_text(json.dumps(dict(repository='fixture/consumer', issues=[dict(number=1, state='closed', state_reason='completed', labels=['wf:review'])])))
        r = run('check', '--repo', self.target, '--issues-json', p, expect=1)
        self.assertTrue(any(x['code'] == 'issue.inconsistent' for x in r['findings']))

    def test_issue_snapshot_entries_reject_malformed_shapes_without_tracebacks(self):
        snapshot = self.root / 'issues.json'
        index = (self.target / '.git/index').read_bytes()
        malformed = [None, [], 'issue', 1, True, {'labels': None}, {'labels': {}},
                     {'labels': [None]}, {'labels': [{}]}, {'labels': [{'name': []}]},
                     {'labels': [42]}, {'labels': [['wf:ready']]}, {'state': None}, {'state': []}]
        for item in malformed:
            with self.subTest(item=item):
                snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[item])))
                original = snapshot.read_bytes()
                result = subprocess.run([sys.executable, str(self.target / '.agents/tools/workflow/workflow.py'),
                                         'check', '--repo', str(self.target), '--issues-json', str(snapshot), '--json'],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                report = json.loads(result.stdout)
                self.assertFalse(report['ok'])
                self.assertEqual(report['findings'][0]['code'], 'invalid')
                self.assertEqual(result.stderr, '')
                self.assertEqual(snapshot.read_bytes(), original)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
        snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[
            dict(number=1, state='open', labels=['wf:ready']),
            dict(number=2, state='open', labels=[{'name': 'wf:review'}, {'name': 'security'}])
        ])))
        run('check', '--repo', self.target, '--issues-json', snapshot)

    def test_ci_event_and_trust_boundaries_are_explicit(self):
        metadata = (ROOT / '.github/workflows/pr-metadata.yml').read_text()
        code = (ROOT / '.github/workflows/verify.yml').read_text()
        self.assertIn('pull_request_target:', metadata)
        self.assertIn('edited, synchronize', metadata)
        self.assertIn('github.event.pull_request.base.sha', metadata)
        self.assertNotIn('github.event.pull_request.head.sha', metadata)
        self.assertNotIn('github.event.pull_request.body', metadata)
        self.assertIn('contents: read', metadata)
        self.assertNotIn('write', metadata)
        self.assertIn('"$GITHUB_EVENT_PATH"', metadata)
        self.assertIn('pull_request:', code)
        self.assertIn('synchronize', code)
        self.assertIn('python3 tools/workflow/verify.py', code)

    def test_declared_verification_has_actual_argv_consumer(self):
        p = self.target / '.workflow/config.json'
        c = json.loads(p.read_text())
        c['verification']['local'] = [['python3', '-c', "from pathlib import Path; Path('verification-ran').write_text('yes')"]]
        p.write_text(json.dumps(c))
        r = run('check', '--repo', self.target, '--run-local')
        self.assertEqual((self.target / 'verification-ran').read_text(), 'yes')
        self.assertTrue(any(x['code'] == 'verification.passed' for x in r['findings']))
        c['verification']['local'] = [['python3', '-c', 'import sys; sys.exit(7)']]
        p.write_text(json.dumps(c))
        r = run('check', '--repo', self.target, '--run-local', expect=1)
        self.assertTrue(any(x['code'] == 'verification.failed' for x in r['findings']))
        c['verification']['local'] = [['definitely-missing-wf2-runtime']]
        p.write_text(json.dumps(c))
        r = run('check', '--repo', self.target, '--run-local', expect=1)
        self.assertTrue(any(x['code'] == 'verification.unavailable' for x in r['findings']))
        run('check', '--repo', self.target, '--pr-json', self.snapshot(BODY), '--metadata-only', '--run-local', expect=2)

    def test_invalid_native_argv_rejects_all_commands_before_execution(self):
        p = self.target / '.workflow/config.json'
        original = json.loads(p.read_text())
        marker = self.target / 'MUST_NOT_RUN'
        first = [sys.executable, '-c', "from pathlib import Path; Path('MUST_NOT_RUN').touch()"]
        index = (self.target / '.git/index').read_bytes()
        for category in ('local', 'integration'):
            for invalid in ('nul\0argument', 'unencodable\ud800argument'):
                with self.subTest(category=category, argument=invalid):
                    c = json.loads(json.dumps(original))
                    c['verification']['local'] = [first]
                    c['verification'][category].append([sys.executable, '-c', invalid])
                    p.write_text(json.dumps(c))
                    before = {x.relative_to(self.target): x.read_bytes()
                              for x in self.target.rglob('*') if x.is_file()
                              and '.git' not in x.relative_to(self.target).parts}
                    r = run('check', '--repo', self.target, '--run-local', '--run-integration', expect=2)
                    self.assertEqual(r['findings'][0]['code'], 'invalid')
                    self.assertFalse(marker.exists())
                    self.assertEqual({x.relative_to(self.target): x.read_bytes()
                                      for x in self.target.rglob('*') if x.is_file()
                                      and '.git' not in x.relative_to(self.target).parts}, before)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_malformed_document_and_metadata_urls_report_findings(self):
        p = self.target / 'README.md'
        index = (self.target / '.git/index').read_bytes()
        for target in ('https://[malformed', 'https://[not-an-ipv6]/path'):
            with self.subTest(url=target):
                link = '[malformed](' + target + ')'
                p.write_text(link)
                contents = p.read_bytes()
                r = run('check', '--repo', self.target, expect=1)
                self.assertTrue(any(x['code'] == 'links.url' for x in r['findings']))
                self.assertEqual(p.read_bytes(), contents)
                r = run('check', '--repo', self.target, '--pr-json', self.snapshot(BODY + link),
                        '--metadata-only', expect=1)
                self.assertTrue(any(x['code'] == 'links.url' for x in r['findings']))
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
        p.write_text('[valid](https://example.invalid/path#anchor)')
        run('check', '--repo', self.target)

    def test_plain_text_findings_escape_unencodable_metadata(self):
        from test_setup import TOOLS
        index = (self.target / '.git/index').read_bytes()
        for target, code in [('https://[bad\ud800', 'links.url'),
                             ('missing\ud800.md', 'links.path'),
                             ('missing-\u2603.md', 'links.path')]:
            snapshot = self.snapshot(BODY + '[bad](' + target + ')')
            before = snapshot.read_bytes()
            for encoding in ('utf-8:strict', 'ascii:strict'):
                with self.subTest(url=ascii(target), encoding=encoding):
                    r = subprocess.run([sys.executable, str(TOOLS / 'workflow.py'),
                                        'check', '--repo', str(self.target), '--pr-json', str(snapshot),
                                        '--metadata-only'], capture_output=True,
                                       env=dict(os.environ, PYTHONIOENCODING=encoding))
                    self.assertEqual(r.returncode, 1, (r.stdout, r.stderr))
                    self.assertIn(code.encode(), r.stdout)
                    self.assertIn(b'FAILED', r.stdout)
                    self.assertEqual(r.stderr, b'')
                    self.assertEqual(snapshot.read_bytes(), before)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
            report = run('check', '--repo', self.target, '--pr-json', snapshot,
                         '--metadata-only', expect=1)
            self.assertTrue(any(x['code'] == code for x in report['findings']))

    def test_doctor_continues_after_an_undecodable_discovery_file(self):
        folder = self.root / 'isolated-discovery'
        bad = folder / 'a-unrelated/SKILL.md'
        good = folder / 'z-valid/SKILL.md'
        bad.parent.mkdir(parents=True)
        good.parent.mkdir(parents=True)
        bad.write_bytes(b'\xff\xfeinvalid UTF-8')
        good.write_text('---\nname: workflow-deliver-issue\ndescription: duplicate fixture\n---\n')
        index = (self.target / '.git/index').read_bytes()
        r = run('doctor', '--repo', self.target, '--skill-root', folder, expect=1)
        self.assertTrue(any(x['code'] == 'discovery.invalid' and x['path'] == str(bad)
                            and x['severity'] == 'warning' for x in r['findings']))
        self.assertTrue(any(x['code'] == 'discovery.duplicate' for x in r['findings']))
        good.unlink()  # Remove only the disposable duplicate; invalid file remains.
        r = run('doctor', '--repo', self.target, '--skill-root', folder)
        self.assertTrue(r['ok'])
        self.assertTrue(any(x['code'] == 'discovery.invalid' for x in r['findings']))
        self.assertEqual(bad.read_bytes(), b'\xff\xfeinvalid UTF-8')
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_invalid_project_text_returns_json_without_mutation(self):
        index = (self.target / '.git/index').read_bytes()
        cases = {'AGENTS.md': ('check', 'doctor', 'bootstrap', 'setup'),
                 '.gitignore': ('check', 'doctor', 'bootstrap', 'setup'),
                 'README.md': ('check',),
                 '.agents/skills/workflow-risk-review/SKILL.md': ('check',)}
        for name, commands in cases.items():
            with self.subTest(path=name):
                p = self.target / name
                original = p.read_bytes() if p.exists() else None
                p.write_bytes(b'\xff\xfeinvalid UTF-8')
                before = {x.relative_to(self.target): x.read_bytes()
                          for x in self.target.rglob('*') if x.is_file()
                          and '.git' not in x.relative_to(self.target).parts}
                for command in commands:
                    with self.subTest(command=command):
                        args = (('--source', self.source, '--revision', self.sha, '--target', self.target,
                                 '--repository', 'fixture/consumer', '--apply') if command == 'setup'
                                else ('--repo', self.target, *(('--apply',) if command == 'bootstrap' else ())))
                        r = run(command, *args, expect=2)
                        self.assertEqual(r['findings'][0]['code'], 'invalid')
                        self.assertEqual({x.relative_to(self.target): x.read_bytes()
                                          for x in self.target.rglob('*') if x.is_file()
                                          and '.git' not in x.relative_to(self.target).parts}, before)
                        self.assertEqual((self.target / '.git/index').read_bytes(), index)
                if original is None:
                    p.unlink()
                else:
                    p.write_bytes(original)

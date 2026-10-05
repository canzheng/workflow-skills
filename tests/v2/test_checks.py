import json
import contextlib
import io
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

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

    def test_pr_fragments_use_body_anchors_without_synthetic_head_file(self):
        sha = commit(self.target)
        index = (self.target / '.git/index').read_bytes()
        def event(body):
            return dict(repository={'full_name': 'fixture/consumer'}, pull_request=dict(
                base={'repo': {'full_name': 'fixture/consumer'}}, head={'sha': sha}, body=body))
        for native in (False, True):
            for fragment, expected in [('#changes', 0), ('#documentation', 0), ('#%63hanges', 0),
                                       ('#', 0), ('#missing-heading', 1)]:
                with self.subTest(native=native, fragment=fragment):
                    body = BODY + '\n[Jump](' + fragment + ')\n'
                    snapshot = self.snapshot(body)
                    if native:
                        snapshot.write_text(json.dumps(event(body)))
                    r = run('check', '--repo', self.target, '--pr-json', snapshot, '--metadata-only', expect=expected)
                    if expected:
                        self.assertTrue(any(x['code'] == 'links.anchor' for x in r['findings']))
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
        # A real tracked file with this synthetic name must not supply PR anchors.
        (self.target / 'PR.md').write_text('# File-only heading\n')
        sha = commit(self.target)
        for native in (False, True):
            with self.subTest(native=native, decoy=True):
                body = BODY + '\n[Wrong surface](#file-only-heading)\n'
                snapshot = self.snapshot(body)
                if native:
                    snapshot.write_text(json.dumps(event(body)))
                r = run('check', '--repo', self.target, '--pr-json', snapshot, '--metadata-only', expect=1)
                self.assertTrue(any(x['code'] == 'links.anchor' for x in r['findings']))

    def test_pr_event_shapes_reject_before_fetch_without_tracebacks_or_writes(self):
        snapshot = self.root / 'event.json'
        fetched = self.root / 'MUST_NOT_FETCH'
        wrapper = self.root / 'isolated-bin/git'
        wrapper.parent.mkdir()
        wrapper.write_text('#!' + sys.executable + '\nimport pathlib, subprocess, sys\n'
                           'if "fetch" in sys.argv[1:]:\n'
                           '    pathlib.Path(' + repr(str(fetched)) + ').touch()\n'
                           '    sys.exit(69)\n'
                           'sys.exit(subprocess.call([' + repr(shutil.which('git')) + ', *sys.argv[1:]]))\n')
        wrapper.chmod(0o755)
        env = dict(os.environ, PATH=str(wrapper.parent) + os.pathsep + os.environ['PATH'])
        event = dict(repository={'full_name': 'fixture/consumer'}, pull_request=dict(
            base={'repo': {'full_name': 'fixture/consumer'}}, head={'sha': 'f' * 40}, body=BODY))
        index = (self.target / '.git/index').read_bytes()
        malformed = [(('repository',), value) for value in (None, [], '', 1, True)]
        malformed += [(('repository', 'full_name'), value) for value in (None, [], {}, True, 'other/repo')]
        for path in (('pull_request',), ('pull_request', 'base'),
                     ('pull_request', 'base', 'repo'), ('pull_request', 'head')):
            malformed += [(path, value) for value in (None, [], '', 1, True)]
        malformed += [(('pull_request', 'head', 'sha'), value) for value in (None, [], {}, 1, True, 'garbage')]
        malformed += [(('pull_request', 'body'), value) for value in ([], {}, 0, False, {'text': BODY})]
        for path, value in malformed:
            with self.subTest(path=path, value=value):
                fetched.unlink(missing_ok=True)
                item = json.loads(json.dumps(event))
                parent = item
                for key in path[:-1]:
                    parent = parent[key]
                parent[path[-1]] = value
                snapshot.write_text(json.dumps(item))
                original = snapshot.read_bytes()
                r = subprocess.run([sys.executable, str(self.target / '.agents/tools/workflow/workflow.py'),
                                    'check', '--repo', str(self.target), '--pr-json', str(snapshot),
                                    '--metadata-only', '--json'], env=env, capture_output=True, text=True)
                self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                self.assertEqual(json.loads(r.stdout)['findings'][0]['code'], 'invalid')
                self.assertEqual(r.stderr, '')
                self.assertFalse(fetched.exists())
                self.assertEqual(snapshot.read_bytes(), original)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
        event['pull_request']['head']['sha'] = subprocess.check_output(
            ['git', '-C', str(self.target), 'rev-parse', 'HEAD'], text=True).strip()
        for body, expected in ((BODY, 0), (None, 1), ('', 1)):
            with self.subTest(valid_body=body):
                fetched.unlink(missing_ok=True)
                event['pull_request']['body'] = body
                snapshot.write_text(json.dumps(event))
                r = subprocess.run([sys.executable, str(self.target / '.agents/tools/workflow/workflow.py'),
                                    'check', '--repo', str(self.target), '--pr-json', str(snapshot),
                                    '--metadata-only', '--json'], env=env, capture_output=True, text=True)
                self.assertEqual(r.returncode, expected, r.stdout + r.stderr)
                self.assertEqual(r.stderr, '')
                self.assertFalse(fetched.exists())
                self.assertEqual((self.target / '.git/index').read_bytes(), index)

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
                     {'labels': [42]}, {'labels': [['wf:ready']]}, {'state': None}, {'state': []},
                     {'state': 'garbage', 'labels': ['wf:ready']}, {'state': '', 'labels': ['wf:ready']},
                     {'state': 'completed', 'labels': ['wf:ready']}]
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
            dict(number=2, state='OPEN', labels=[{'name': 'wf:review'}, {'name': 'security'}]),
            dict(number=3, state='CLOSED', labels=[])
        ])))
        run('check', '--repo', self.target, '--issues-json', snapshot)

    def test_issue_snapshot_closure_reasons_validate_and_normalize(self):
        snapshot = self.root / 'issues.json'
        index = (self.target / '.git/index').read_bytes()
        for reason in ('garbage', '', 'unknown', 1, True, [], {}):
            with self.subTest(reason=reason):
                snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[
                    dict(state='closed', state_reason=reason, labels=[])])))
                original = snapshot.read_bytes()
                result = subprocess.run([sys.executable, str(self.target / '.agents/tools/workflow/workflow.py'),
                                         'check', '--repo', str(self.target), '--issues-json', str(snapshot), '--json'],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)['ok'])
                self.assertEqual(json.loads(result.stdout)['findings'][0]['code'], 'invalid')
                self.assertEqual(result.stderr, '')
                self.assertEqual(snapshot.read_bytes(), original)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
        for reason in ('completed', 'COMPLETED'):
            with self.subTest(reason=reason):
                snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[
                    dict(state='closed', state_reason=reason, labels=[])])))
                r = run('check', '--repo', self.target, '--issues-json', snapshot, expect=1)
                self.assertTrue(any(x['code'] == 'issue.inconsistent' for x in r['findings']))
        snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[
            dict(state='closed', state_reason=None, labels=[]),
            dict(state='closed', state_reason='NOT_PLANNED', labels=[]),
            dict(state='closed', state_reason='DUPLICATE', labels=[]),
            dict(state='open', state_reason='REOPENED', labels=['wf:ready']),
            dict(state='CLOSED', state_reason='COMPLETED', labels=[], delivery_evidence='Inspect linked PR manually')
        ])))
        run('check', '--repo', self.target, '--issues-json', snapshot)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_issue_snapshot_state_reason_pairs_validate_before_classification(self):
        snapshot = self.root / 'issues.json'
        index = (self.target / '.git/index').read_bytes()
        for state in ('open', 'OPEN', 'closed', 'CLOSED'):
            for reason in (None, 'completed', 'COMPLETED', 'not_planned', 'NOT_PLANNED',
                           'duplicate', 'DUPLICATE', 'reopened', 'REOPENED'):
                valid = reason is None or ((state.lower() == 'open') == (reason.lower() == 'reopened'))
                with self.subTest(state=state, reason=reason):
                    item = dict(state=state, state_reason=reason,
                                labels=['wf:ready'] if state.lower() == 'open' else [],
                                delivery_evidence='PR reference; verify acceptance manually')
                    snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[item])))
                    original = snapshot.read_bytes()
                    result = subprocess.run([sys.executable, str(self.target / '.agents/tools/workflow/workflow.py'),
                                             'check', '--repo', str(self.target), '--issues-json', str(snapshot), '--json'],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0 if valid else 2, result.stdout + result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report['ok'], valid)
                    if not valid:
                        self.assertEqual(report['findings'][0]['code'], 'invalid')
                    self.assertEqual(result.stderr, '')
                    self.assertEqual(snapshot.read_bytes(), original)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_issue_snapshot_delivery_evidence_is_an_optional_nonblank_reference(self):
        snapshot = self.root / 'issues.json'
        index = (self.target / '.git/index').read_bytes()
        for state, reason, labels in [('closed', 'completed', []), ('closed', 'duplicate', []),
                                     ('open', 'reopened', ['wf:ready'])]:
            for evidence in (None, '', ' ', '\n\t', 'PR #17; inspect manually', 0, 1, False, True, [],
                             ['PR #17'], {}, {'bogus': True}):
                malformed = evidence is not None and not isinstance(evidence, str)
                missing = state == 'closed' and reason == 'completed' and not (
                    isinstance(evidence, str) and evidence.strip())
                expected = 2 if malformed else 1 if missing else 0
                with self.subTest(state=state, reason=reason, evidence=evidence):
                    item = dict(state=state, state_reason=reason, labels=labels, delivery_evidence=evidence)
                    snapshot.write_text(json.dumps(dict(repository='fixture/consumer', issues=[item])))
                    original = snapshot.read_bytes()
                    result = subprocess.run([sys.executable, str(self.target / '.agents/tools/workflow/workflow.py'),
                                             'check', '--repo', str(self.target), '--issues-json', str(snapshot), '--json'],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    report = json.loads(result.stdout)
                    self.assertEqual(report['ok'], expected == 0)
                    if expected:
                        self.assertEqual(report['findings'][0]['code'], 'invalid' if malformed else 'issue.inconsistent')
                    self.assertEqual(result.stderr, '')
                    self.assertEqual(snapshot.read_bytes(), original)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)

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

    def test_doctor_tool_timeouts_continue_with_private_output_suppressed(self):
        import test_setup
        module = test_setup.workflow
        folder = self.root / 'diagnostic-executables'
        folder.mkdir()
        for tool in ('git', 'gh', 'node', 'openspec'):
            program = folder / tool
            program.write_text('#!' + sys.executable + '\n' +
                "import os,pathlib,sys,time\n" +
                "name=pathlib.Path(sys.argv[0]).name\n" +
                "operation=name+(':version' if sys.argv[1:]==['--version'] else ':auth')\n" +
                "if operation==os.environ.get('WF2_HANG_PROBE'):\n" +
                " print('TEST_PRIVATE_PROBE_OUTPUT',flush=True)\n" +
                " print('TEST_PRIVATE_PROBE_ERROR',file=sys.stderr,flush=True)\n" +
                " time.sleep(30)\n" +
                "elif sys.argv[1:]==['--version']: print(name+' fixture')\n" +
                "else: print('TEST_PRIVATE_AUTH_OUTPUT')\n")
            program.chmod(0o755)
        actual = subprocess.run
        index = (self.target / '.git/index').read_bytes()
        tracked = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                   if p.is_file() and '.git' not in p.relative_to(self.target).parts}
        for selected in ('git:version', 'gh:version', 'node:version', 'openspec:version', 'gh:auth'):
            with self.subTest(probe=selected):
                calls = []
                def execute(command, **kwargs):
                    # Exercise real executable timeout/kill with an accelerated
                    # test deadline; production still declares ten seconds.
                    if pathlib.Path(command[0]).parent == folder or command[:3] == ['gh', 'auth', 'status']:
                        self.assertEqual(kwargs['timeout'], 10)
                        command = [str(folder / pathlib.Path(command[0]).name), *command[1:]]
                        operation = pathlib.Path(command[0]).name + (':version' if command[1:] == ['--version'] else ':auth')
                        if operation == selected:
                            kwargs['timeout'] = 0.1
                        calls.append(command)
                    return actual(command, **kwargs)
                with patch.object(module.shutil, 'which', lambda name: str(folder / name)), \
                        patch.object(module.subprocess, 'run', execute), \
                        patch.dict(os.environ, {'WF2_HANG_PROBE': selected}), \
                        contextlib.redirect_stdout(io.StringIO()) as output:
                    try:
                        status = module.main(['doctor', '--repo', str(self.target), '--json'])
                    except subprocess.TimeoutExpired:
                        self.fail('Public doctor leaked a timed-out tool probe instead of producing JSON')
                self.assertEqual(status, 0, output.getvalue())
                report = json.loads(output.getvalue())
                self.assertTrue(report['ok'])
                self.assertEqual(len(calls), 5)  # Other probes and auth still run.
                self.assertTrue(any(x['code'] == 'tool.probe' and x['severity'] == 'warning'
                                    and 'timed out' in x['message'] for x in report['findings']))
                if selected == 'gh:auth':
                    self.assertEqual(report['capabilities']['gh_authentication'], 'unavailable')
                else:
                    self.assertEqual(report['tools'][selected.split(':')[0]], 'unavailable')
                for tool in ('git', 'gh', 'node', 'openspec'):
                    if selected != tool + ':version':
                        self.assertEqual(report['tools'][tool], tool + ' fixture')
                self.assertNotIn('TEST_PRIVATE', output.getvalue())
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                self.assertEqual({p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                                  if p.is_file() and '.git' not in p.relative_to(self.target).parts}, tracked)

    def test_doctor_unexecutable_and_invalid_tool_output_continue(self):
        import test_setup
        module = test_setup.workflow
        folder = self.root / 'diagnostic-failures'
        folder.mkdir()
        index = (self.target / '.git/index').read_bytes()
        actual = subprocess.run
        def execute(command, **kwargs):
            if command[:3] == ['gh', 'auth', 'status']:
                command = [str(folder / 'gh'), *command[1:]]
            return actual(command, **kwargs)
        for case in ('missing-executable', 'invalid-version', 'failed-version', 'failed-auth'):
            with self.subTest(case=case):
                for tool in ('git', 'gh', 'node', 'openspec'):
                    program = folder / tool
                    program.write_text('#!' + sys.executable + '\n' +
                        "import os,pathlib,sys\n" +
                        "name=pathlib.Path(sys.argv[0]).name\n" +
                        "version=sys.argv[1:]==['--version']\n" +
                        "case=os.environ.get('WF2_FAILED_PROBE')\n" +
                        "if name=='node' and version and case=='invalid-version': sys.stdout.buffer.write(b'\\xff')\n" +
                        "elif (name=='node' and version and case=='failed-version') or (name=='gh' and not version and case=='failed-auth'):\n" +
                        " print('TEST_PRIVATE_TOOL_ERROR',file=sys.stderr);sys.exit(3)\n" +
                        "elif version: print(name+' fixture')\n" +
                        "else: print('TEST_PRIVATE_AUTH_OUTPUT')\n")
                    program.chmod(0o755)
                def locate(name):
                    return str(folder / ('missing' if name == 'node' and case == 'missing-executable' else name))
                with patch.object(module.shutil, 'which', locate), \
                        patch.object(module.subprocess, 'run', execute), \
                        patch.dict(os.environ, {'WF2_FAILED_PROBE': case}), \
                        contextlib.redirect_stdout(io.StringIO()) as output:
                    status = module.main(['doctor', '--repo', str(self.target), '--json'])
                self.assertEqual(status, 0, output.getvalue())
                report = json.loads(output.getvalue())
                self.assertTrue(report['ok'])
                self.assertEqual(report['tools']['openspec'], 'openspec fixture')
                if case == 'failed-auth':
                    self.assertEqual(report['capabilities']['gh_authentication'], 'unavailable')
                else:
                    self.assertEqual(report['tools']['node'], 'unavailable')
                self.assertNotIn('TEST_PRIVATE', output.getvalue())
                self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_doctor_rejects_blank_version_headers_and_continues_healthy_probes(self):
        import test_setup
        module = test_setup.workflow
        folder = self.root / 'blank-version-executables'
        folder.mkdir()
        for tool in ('git', 'gh', 'node', 'openspec'):
            program = folder / tool
            program.write_text('#!' + sys.executable + '\n' +
                "import os,pathlib,sys\n" +
                "name=pathlib.Path(sys.argv[0]).name\n" +
                "if sys.argv[1:]==['--version']:\n" +
                " data=(bytes.fromhex(os.environ['WF2_VERSION_BYTES']) if name==os.environ['WF2_VERSION_TOOL'] else (name+' fixture\\n').encode())\n" +
                " sys.stdout.buffer.write(data)\n" +
                "else: print('TEST_PRIVATE_AUTH_OUTPUT')\n")
            program.chmod(0o755)
        index = (self.target / '.git/index').read_bytes()
        contents = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                    if p.is_file() and '.git' not in p.relative_to(self.target).parts}
        outputs = (b'', b'\nnot-a-version\n', b'\r\nnot-a-version\n',
                   b' \t\nnot-a-version\n', '\u00a0\u2003\nnot-a-version\n'.encode(),
                   b'valid fixture\nignored later line\n')
        for selected in ('git', 'gh', 'node', 'openspec'):
            for data in outputs:
                with self.subTest(tool=selected, output=data):
                    with patch.object(module.shutil, 'which', lambda name: str(folder / name)), \
                            patch.dict(os.environ, {'WF2_VERSION_TOOL': selected,
                                                    'WF2_VERSION_BYTES': data.hex()}), \
                            contextlib.redirect_stdout(io.StringIO()) as output:
                        status = module.main(['doctor', '--repo', str(self.target), '--json'])
                    self.assertEqual(status, 0, output.getvalue())
                    report = json.loads(output.getvalue())
                    self.assertTrue(report['ok'])
                    valid = data.startswith(b'valid fixture')
                    self.assertEqual(report['tools'][selected], 'valid fixture' if valid else 'unavailable')
                    warnings = [x for x in report['findings'] if x['code'] == 'tool.probe'
                                and x['path'] == str(folder / selected)]
                    self.assertEqual(len(warnings), 0 if valid else 1)
                    if warnings:
                        self.assertEqual(warnings[0]['severity'], 'warning')
                        self.assertIn('version output is invalid', warnings[0]['message'])
                    for tool in ('git', 'gh', 'node', 'openspec'):
                        if tool != selected:
                            self.assertEqual(report['tools'][tool], tool + ' fixture')
                    self.assertEqual(report['capabilities']['gh_authentication'], 'authenticated')
                    self.assertNotIn('TEST_PRIVATE', output.getvalue())
                    self.assertNotIn('not-a-version', output.getvalue())
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    self.assertEqual({p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                                      if p.is_file() and '.git' not in p.relative_to(self.target).parts}, contents)

    def _read_fault_cli(self, command, injection, expect):
        import test_setup
        code = ('import pathlib,os,checks,core,migration,workflow\n' + injection +
                '\nraise SystemExit(workflow.main(' +
                repr([command, *(['inspect'] if command == 'migrate' else []),
                      '--repo', str(self.target), '--json']) + '))\n')
        try:
            result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True,
                                    timeout=20, env={**os.environ, 'PYTHONPATH': str(test_setup.TOOLS)})
        except subprocess.TimeoutExpired:
            self.fail('Public reader blocked instead of returning structured diagnostics')
        self.assertEqual(result.returncode, expect, result.stdout + result.stderr)
        self.assertNotIn('TEST_PRIVATE_BOUND_READ', result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_document_reads_are_bound_and_reject_nonregular_entries(self):
        external = self.root / 'private-documents/race.md'
        external.parent.mkdir()
        external.write_text('[private](https://[TEST_PRIVATE_BOUND_READ)\n')
        private = external.read_bytes()
        index = (self.target / '.git/index').read_bytes()
        for case in ('symlink', 'fifo', 'ancestor', 'after-open'):
            with self.subTest(case=case):
                parent = self.target / 'docs' / ('race-' + case)
                parent.mkdir()
                path = parent / 'race.md'
                path.write_text('# Safe\n')
                moved = self.target / 'docs/saved-ancestor'
                action = ("p.unlink(); p.symlink_to(external)" if case != 'fifo'
                          else "p.unlink(); os.mkfifo(p)")
                prefix = 'p=pathlib.Path(' + repr(str(path)) + ')\nexternal=pathlib.Path(' + repr(str(external)) + ')\nchanged=False\n'
                if case == 'after-open':
                    injection = prefix + (
                        "actual=core.os.open\n"
                        "def open_file(name, *args, **kwargs):\n"
                        "    global changed\n"
                        "    fd=actual(name, *args, **kwargs)\n"
                        "    if name == 'race.md' and kwargs.get('dir_fd') is not None and not changed:\n"
                        "        changed=True\n"
                        "        p.unlink(); p.symlink_to(external)\n"
                        "    return fd\n"
                        "core.os.open=open_file\n")
                else:
                    if case == 'ancestor':
                        action = 'p.parent.rename(' + repr(str(moved)) + '); p.parent.symlink_to(external.parent, target_is_directory=True)'
                    injection = prefix + (
                        "actual=checks.safe\n"
                        "def safe(root, name):\n"
                        "    global changed\n"
                        "    found=actual(root, name)\n"
                        "    if found == p and not changed:\n"
                        "        changed=True\n"
                        "        " + action + "\n"
                        "    return found\n"
                        "checks.safe=safe\n")
                try:
                    report = self._read_fault_cli('check', injection, 0 if case == 'after-open' else 1)
                    if case != 'after-open':
                        self.assertTrue(any(x['code'] == 'docs.unsafe' for x in report['findings']), report)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    self.assertEqual(external.read_bytes(), private)
                    if case == 'ancestor':
                        self.assertEqual(parent.readlink(), external.parent)
                        self.assertEqual((moved / 'race.md').read_text(), '# Safe\n')
                    elif case == 'fifo':
                        import stat
                        self.assertTrue(stat.S_ISFIFO(path.lstat().st_mode))
                    else:
                        self.assertEqual(path.readlink(), external)
                finally:
                    if parent.is_symlink():
                        parent.unlink()
                        moved.rename(parent)
                    path.unlink()
                    parent.rmdir()

    def test_doctor_nonregular_entries_warn_and_continue(self):
        import stat
        import test_setup
        bad = self.root / 'unsupported-catalog/unsupported/SKILL.md'
        bad.parent.mkdir(parents=True)
        good = self.root / 'healthy-catalog/valid/SKILL.md'
        good.parent.mkdir(parents=True)
        good.write_text('---\nname: workflow-deliver-issue\ndescription: duplicate\n---\n')
        external = self.root / 'private-skill'
        external.write_bytes(b'\xffTEST_PRIVATE_BOUND_READ')
        index = (self.target / '.git/index').read_bytes()
        for case in ('fifo', 'symlink', 'directory'):
            with self.subTest(case=case):
                if case == 'fifo':
                    os.mkfifo(bad)
                elif case == 'symlink':
                    bad.symlink_to(external)
                else:
                    bad.mkdir()
                try:
                    result = subprocess.run([sys.executable, str(test_setup.TOOLS / 'workflow.py'),
                                             'doctor', '--repo', str(self.target), '--json',
                                             '--skill-root', str(bad.parent.parent),
                                             '--skill-root', str(good.parent.parent)],
                                            capture_output=True, text=True, timeout=20)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    report = json.loads(result.stdout)
                    self.assertTrue(any(x['code'] == 'discovery.inaccessible' and x['path'] == str(bad)
                                        for x in report['findings']), report)
                    self.assertTrue(any(x['code'] == 'discovery.duplicate' for x in report['findings']))
                    self.assertIn('tools', report)
                    self.assertNotIn('TEST_PRIVATE_BOUND_READ', result.stdout + result.stderr)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    self.assertEqual(external.read_bytes(), b'\xffTEST_PRIVATE_BOUND_READ')
                    if case == 'fifo':
                        self.assertTrue(stat.S_ISFIFO(bad.lstat().st_mode))
                    elif case == 'symlink':
                        self.assertEqual(bad.readlink(), external)
                except subprocess.TimeoutExpired:
                    self.fail('Public doctor blocked on an unsupported catalog entry')
                finally:
                    bad.rmdir() if case == 'directory' else bad.unlink()

    def test_required_openspec_probes_are_bounded_and_suppress_partial_output(self):
        import test_setup
        cli = self.target / 'node_modules/.bin/openspec'
        cli.parent.mkdir(parents=True)
        index = (self.target / '.git/index').read_bytes()
        actual = subprocess.run
        for phase in ('version', 'validate'):
            with self.subTest(phase=phase):
                cli.write_text('#!' + sys.executable + '\nimport sys,time\n'
                               'version="--version" in sys.argv\n'
                               'if version and ' + repr(phase == 'validate') + ':\n'
                               '    print("1.14.0")\n'
                               'else:\n'
                               '    print("TEST_PRIVATE_SPEC_TIMEOUT", flush=True)\n'
                               '    print("TEST_PRIVATE_SPEC_TIMEOUT", file=sys.stderr, flush=True)\n'
                               '    time.sleep(2)\n')
                cli.chmod(0o755)
                calls = []
                def bounded(command, **kwargs):
                    if command[0] == str(cli):
                        expected = 10 if '--version' in command else 120
                        self.assertEqual(kwargs.get('timeout'), expected)
                        calls.append(expected)
                        kwargs['timeout'] = 0.1
                    return actual(command, **kwargs)
                with patch.object(subprocess, 'run', bounded), contextlib.redirect_stdout(io.StringIO()) as output:
                    status = test_setup.workflow.main(['check', '--repo', str(self.target), '--specs', '--json'])
                self.assertEqual(status, 1, output.getvalue())
                report = json.loads(output.getvalue())
                self.assertTrue(any(x['code'] == 'specs.timeout' and x['severity'] == 'error'
                                    for x in report['findings']))
                self.assertEqual(calls, [10] if phase == 'version' else [10, 120])
                self.assertNotIn('TEST_PRIVATE_SPEC_TIMEOUT', output.getvalue())
                self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_migration_record_reads_are_bound_and_nonblocking(self):
        folder = self.target / 'docs/planning/versions/mvp'
        folder.mkdir(parents=True)
        ledger, feature = folder / 'BACKLOG.md', folder / 'feature.md'
        tick = chr(96)
        ledger_text = '## [READY]\n### ' + tick + 'mvp-f01' + tick + ' [Feature](feature.md)\nOriginal notes.\n'
        feature_text = '- Feature ID: ' + tick + 'mvp-f01' + tick + '\n- OpenSpec Change: ' + tick + 'legacy-feature' + tick + '\nOriginal feature.\n'
        change = self.target / 'openspec/changes/legacy-feature'
        change.mkdir(parents=True)
        external = self.root / 'private-legacy.md'
        external.write_text('## [READY]\n### ' + tick + 'private-f99' + tick + ' Confidential\nTEST_PRIVATE_BOUND_READ\n')
        index = (self.target / '.git/index').read_bytes()
        for selected in (ledger, feature):
            for kind in ('symlink', 'fifo'):
                with self.subTest(path=selected.name, kind=kind):
                    ledger.write_text(ledger_text)
                    feature.write_text(feature_text)
                    prefix = 'p=pathlib.Path(' + repr(str(selected)) + ')\nexternal=pathlib.Path(' + repr(str(external)) + ')\nchanged=False\n'
                    action = 'p.unlink(); p.symlink_to(external)' if kind == 'symlink' else 'p.unlink(); os.mkfifo(p)'
                    if selected == ledger:
                        injection = prefix + (
                            "actual=pathlib.Path.is_file\n"
                            "def is_file(path):\n"
                            "    global changed\n"
                            "    found=actual(path)\n"
                            "    if path == p and not changed:\n"
                            "        changed=True\n"
                            "        " + action + "\n"
                            "    return found\n"
                            "pathlib.Path.is_file=is_file\n")
                    else:
                        injection = prefix + (
                            "actual=migration.safe\n"
                            "def safe(root, name):\n"
                            "    global changed\n"
                            "    found=actual(root, name)\n"
                            "    if found == p and not changed:\n"
                            "        changed=True\n"
                            "        " + action + "\n"
                            "    return found\n"
                            "migration.safe=safe\n")
                    try:
                        report = self._read_fault_cli('migrate', injection, 1)
                        code = 'migration.record' if selected == ledger else 'migration.feature'
                        self.assertTrue(any(x['code'] == code for x in report['findings']), report)
                        self.assertEqual((self.target / '.git/index').read_bytes(), index)
                        self.assertIn('TEST_PRIVATE_BOUND_READ', external.read_text())
                    finally:
                        selected.unlink()
        ledger.write_text(ledger_text)
        feature.write_text(feature_text)
        report = run('migrate', 'inspect', '--repo', self.target)
        self.assertEqual(report['records'][0]['original_record'], feature_text)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_public_commands_do_not_require_a_resolvable_home(self):
        import test_setup
        cli = test_setup.TOOLS / 'workflow.py'
        prefix = ('import pathlib,runpy,sys; '
                  'pathlib.Path.home=classmethod(lambda cls: '
                  '(_ for _ in ()).throw(RuntimeError("TEST_PRIVATE_HOME_LOOKUP"))); ')
        index = (self.target / '.git/index').read_bytes()
        contents = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                    if p.is_file() and '.git' not in p.relative_to(self.target).parts}
        custom = self.root / 'explicit-global-target'
        cases = [(['check', '--repo', str(self.target)], 0),
                 (['bootstrap', '--repo', str(self.target), '--apply'], 0),
                 (['migrate', 'inspect', '--repo', str(self.target)], 0),
                 (['setup', '--source', str(self.source), '--revision', self.sha,
                   '--target', str(self.target), '--repository', 'fixture/consumer'], 0),
                 (['doctor', '--repo', str(self.target)], 0),
                 (['install-skills', '--source', str(self.source), '--revision', self.sha,
                   '--target', str(custom)], 0),
                 (['install-skills', '--source', str(self.source), '--revision', self.sha], 2)]
        for args, expected in cases:
            with self.subTest(command=args[0], explicit_target='--target' in args):
                code = prefix + 'sys.argv=' + repr([str(cli), *args, '--json']) + '; runpy.run_path(' + repr(str(cli)) + ',run_name="__main__")'
                result = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True,
                                        env={**os.environ, 'PYTHONPATH': str(cli.parent)})
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report['ok'], expected == 0)
                self.assertNotIn('TEST_PRIVATE_HOME_LOOKUP', result.stdout + result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                if args[0] == 'doctor':
                    self.assertTrue(any(x['code'] == 'discovery.inaccessible' and x['severity'] == 'warning'
                                        for x in report['findings']))
                    self.assertIn('tools', report)
                if expected == 2:
                    self.assertIn('--target', report['findings'][0]['remediation'] + report['findings'][0]['message'])
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                self.assertEqual({p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                                  if p.is_file() and '.git' not in p.relative_to(self.target).parts}, contents)
                self.assertFalse(custom.exists())  # Preview must not create a global target.
        # A resolvable default still selects only that isolated home, never the real host.
        home = self.root / 'isolated-default-home'
        with patch.object(pathlib.Path, 'home', return_value=home), contextlib.redirect_stdout(io.StringIO()) as output:
            status = test_setup.workflow.main(['install-skills', '--source', str(self.source),
                                               '--revision', self.sha, '--apply', '--json'])
        self.assertEqual(status, 0, output.getvalue())
        self.assertTrue((home / '.agents/skills/workflow-deliver-issue/SKILL.md').is_file())
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_document_symlinks_never_read_or_disclose_external_content(self):
        import test_setup
        external = self.root / 'private-external.md'
        secret = 'TEST_PRIVATE_DOCUMENT_CONTENT'
        external.write_text('[private](https://[' + secret + ')\n')
        original = external.read_bytes()
        index = (self.target / '.git/index').read_bytes()
        for name in ('README.md', 'CLAUDE.md', 'docs/private.md',
                     'openspec/specs/private/spec.md',
                     'openspec/changes/workflow-v2-rewrite/private.md'):
            with self.subTest(path=name):
                p = self.target / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.symlink_to(external)
                try:
                    report = run('check', '--repo', self.target, expect=1)
                    self.assertNotIn(secret, json.dumps(report))
                    self.assertTrue(any(x['code'] == 'docs.unsafe' and x['path'] == name for x in report['findings']), report)
                    self.assertEqual(p.readlink(), external)
                    self.assertEqual(external.read_bytes(), original)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                    reads = []
                    actual_read = pathlib.Path.read_text
                    def read(path, *args, **kwargs):
                        if path == p or path == external:
                            reads.append(path)
                        return actual_read(path, *args, **kwargs)
                    with patch.object(pathlib.Path, 'read_text', read), contextlib.redirect_stdout(io.StringIO()) as output:
                        status = test_setup.workflow.main(['check', '--repo', str(self.target), '--json'])
                    self.assertEqual(status, 1, output.getvalue())
                    self.assertEqual(reads, [])
                    self.assertNotIn(secret, output.getvalue())
                finally:
                    p.unlink()
        # Also reject dangling/cyclic links and safe-looking in-repository targets.
        for name, target in (('docs/loop.md', self.root / 'absent.md'),
                             ('docs/loop.md', self.target / 'docs/loop.md'),
                             ('docs/loop.md', self.target / 'docs/workflow/README.md'),
                             ('README.md', self.root / 'absent.md'),
                             ('README.md', self.target / 'README.md')):
            with self.subTest(path=name, target=str(target)):
                p = self.target / name
                p.symlink_to(target)
                try:
                    report = run('check', '--repo', self.target, expect=1)
                    self.assertTrue(any(x['code'] == 'docs.unsafe' for x in report['findings']), report)
                    self.assertEqual(p.readlink(), target)
                    self.assertEqual((self.target / '.git/index').read_bytes(), index)
                finally:
                    p.unlink()
        # Rejection must not suppress ordinary repository-local URL diagnostics.
        regular = self.target / 'docs/regular.md'
        regular.write_bytes(original)
        report = run('check', '--repo', self.target, expect=1)
        self.assertTrue(any(x['code'] == 'links.url' and secret in x['message'] for x in report['findings']), report)
        self.assertEqual(regular.read_bytes(), original)
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

    def test_doctor_discovery_root_failures_continue_without_global_writes(self):
        import test_setup
        module = test_setup.workflow
        loop = self.root / 'catalog-loop'
        loop.symlink_to(loop.name)
        first, second = self.root / 'catalog-a', self.root / 'catalog-b'
        first.symlink_to(second.name)
        second.symlink_to(first.name)
        home = self.root / 'isolated-home'
        (home / '.agents').mkdir(parents=True)
        global_loop = home / '.agents/skills'
        global_loop.symlink_to('skills')
        good = self.root / 'healthy-catalog/duplicate/SKILL.md'
        good.parent.mkdir(parents=True)
        good.write_text('---\nname: workflow-deliver-issue\ndescription: duplicate\n---\n')
        unavailable = self.root / 'inaccessible-catalog'
        unavailable.mkdir()
        root_file = self.root / 'catalog-file'
        root_file.write_bytes(b'Human catalog-path content.')
        index = (self.target / '.git/index').read_bytes()
        contents = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                    if p.is_file() and '.git' not in p.relative_to(self.target).parts}
        actual_resolve, actual_exists = pathlib.Path.resolve, pathlib.Path.exists
        actual_listdir, actual_scandir = os.listdir, os.scandir
        for case in ('self-cycle', 'mutual-cycle', 'default-cycle', 'resolve-denied',
                     'stat-denied', 'scan-denied', 'root-file'):
            with self.subTest(case=case):
                selected = {'self-cycle': loop, 'mutual-cycle': first,
                            'default-cycle': global_loop, 'root-file': root_file}.get(case, unavailable)
                args = ['doctor', '--repo', str(self.target), '--json', '--skill-root', str(good.parent.parent)]
                if case != 'default-cycle':
                    # Visit the failed extra root before the healthy extra catalog.
                    args[args.index('--skill-root'):args.index('--skill-root')] = ['--skill-root', str(selected)]
                def resolve(path, *args, **kwargs):
                    if path == unavailable and case == 'resolve-denied':
                        raise PermissionError('TEST_PRIVATE_RESOLUTION_ERROR')
                    return actual_resolve(path, *args, **kwargs)
                def exists(path):
                    if path == unavailable and case == 'stat-denied':
                        raise PermissionError('TEST_PRIVATE_STAT_ERROR')
                    return actual_exists(path)
                def listdir(path):
                    if not isinstance(path, int) and pathlib.Path(os.fsdecode(path)) == unavailable and case == 'scan-denied':
                        raise PermissionError('TEST_PRIVATE_SCAN_ERROR')
                    return actual_listdir(path)
                def scandir(path):
                    if not isinstance(path, int) and pathlib.Path(os.fsdecode(path)) == unavailable and case == 'scan-denied':
                        raise PermissionError('TEST_PRIVATE_SCAN_ERROR')
                    return actual_scandir(path)
                with patch.object(pathlib.Path, 'home', return_value=home if case == 'default-cycle' else self.root / 'empty-home'), \
                        patch.object(pathlib.Path, 'resolve', resolve), \
                        patch.object(pathlib.Path, 'exists', exists), \
                        patch.object(os, 'listdir', listdir), patch.object(os, 'scandir', scandir), \
                        contextlib.redirect_stdout(io.StringIO()) as output:
                    try:
                        status = module.main(args)
                    except RuntimeError:
                        self.fail('Public doctor leaked cyclic catalog resolution instead of continuing')
                self.assertEqual(status, 1, output.getvalue())  # The healthy duplicate still fails.
                report = json.loads(output.getvalue())
                self.assertTrue(any(x['code'] == 'discovery.inaccessible' and x['path'] == str(selected)
                                    and x['severity'] == 'warning' for x in report['findings']))
                self.assertTrue(any(x['code'] == 'discovery.duplicate' for x in report['findings']))
                self.assertIn('tools', report)  # Later tool diagnostics still execute.
                self.assertNotIn('TEST_PRIVATE', output.getvalue())
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                self.assertEqual({p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                                  if p.is_file() and '.git' not in p.relative_to(self.target).parts}, contents)
                self.assertEqual(loop.readlink(), pathlib.Path(loop.name))
                self.assertEqual(first.readlink(), pathlib.Path(second.name))
                self.assertEqual(second.readlink(), pathlib.Path(first.name))
                self.assertEqual(global_loop.readlink(), pathlib.Path('skills'))
                self.assertEqual(root_file.read_bytes(), b'Human catalog-path content.')
        good.unlink()
        report = run('doctor', '--repo', self.target, '--skill-root', loop)
        self.assertTrue(report['ok'])  # A bad optional catalog alone is a warning.
        self.assertTrue(any(x['code'] == 'discovery.inaccessible' and x['path'] == str(loop)
                            for x in report['findings']))
        self.assertEqual((self.target / '.git/index').read_bytes(), index)

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

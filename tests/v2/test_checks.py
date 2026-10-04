import json
import pathlib
import subprocess
import tempfile
import unittest

from test_setup import ROOT, init, fixture_source, commit, run

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
        installed = self.target / 'tools/workflow/workflow.py'
        r = subprocess.run(['python3', str(installed), 'check', '--repo', str(self.target)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_source_check_rejects_omitted_installed_runtime_mapping(self):
        (self.source / '.workflow/config.json').write_bytes((self.target / '.workflow/config.json').read_bytes())
        run('check', '--repo', self.source)
        p = self.source / '.workflow/bundle.json'
        original = json.loads(p.read_text())
        for module in ('workflow.py', 'core.py', 'setup.py', 'bootstrap.py', 'checks.py', 'records.py', 'migration.py'):
            with self.subTest(module=module):
                spec = json.loads(json.dumps(original))
                del spec['assets']['tools/workflow/' + module]
                p.write_text(json.dumps(spec))
                result = run('check', '--repo', self.source, expect=1)
                self.assertTrue(any(x['code'] == 'bundle.incomplete' for x in result['findings']))

    def test_installed_manifest_cannot_hide_deleted_runtime_or_ci_asset(self):
        pin = self.target / '.workflow/install-manifest.json'
        original = pin.read_bytes()
        for name in ('tools/workflow/migration.py', '.github/workflows/workflow-v2-verify.yml', '.github/workflows/workflow-v2-pr-metadata.yml',
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

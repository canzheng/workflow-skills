"""Execute the shipped Issue Action, not a duplicate label implementation."""
import json
import pathlib
import re
import shutil
import subprocess
import textwrap
import unittest

from test_setup import ROOT, run, commit
import test_setup

ACTION = ROOT / '.github/workflows/issue-completion.yml'
HARNESS = ROOT / 'tests/v2/fixtures/issue-api.cjs'


def execute(path=ACTION, *, state='closed', reason='completed', labels=None, marker=True, **options):
    node = shutil.which('node')
    if not node:
        raise AssertionError('Node >=20 is required to verify the shipped Issue Action')
    text = path.read_text()
    script = textwrap.dedent(text.split('          script: |\n', 1)[1])
    issue = dict(number=17, state=state, state_reason=reason,
                 body='<!-- workflow-source: fixture -->' if marker else 'Ordinary Issue',
                 labels=[{'name': name} for name in (labels if labels is not None else
                         ['wf:review', 'wf:blocked', 'security', 'wf:custom'])])
    issue.update(options.pop('issue', {}))
    result = subprocess.run([node, str(HARNESS)], input=json.dumps(dict(script=script, issue=issue, **options)),
                            capture_output=True, text=True, timeout=10)
    if result.returncode:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def label_names(result):
    return {label if isinstance(label, str) else label['name'] for label in result['issue']['labels']}


class IssueCompletionTests(unittest.TestCase):
    def test_completed_closure_preserves_custom_labels_and_is_idempotent(self):
        result = execute()
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:done', 'security', 'wf:custom'})
        rerun = execute(labels=sorted(label_names(result)), dispatch=True)
        self.assertIsNone(rerun['failure'])
        self.assertEqual(label_names(rerun), label_names(result))
        self.assertEqual([call['method'] for call in rerun['calls']], ['get', 'get'])

    def test_cancelled_and_duplicate_closure_do_not_assert_completion(self):
        for reason in ['not_planned', 'duplicate']:
            with self.subTest(reason=reason):
                result = execute(reason=reason, labels=['wf:review', 'wf:done', 'wf:deferred', 'triage', 'wf:custom'])
                self.assertIsNone(result['failure'])
                self.assertEqual(label_names(result), {'triage', 'wf:custom'})

    def test_reopen_returns_to_backlog_without_dispatching_execution(self):
        result = execute(state='open', reason='reopened', labels=['wf:done', 'security'])
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:backlog', 'security'})

    def test_reopen_preserves_existing_phase_and_modifiers(self):
        result = execute(state='open', reason='reopened', labels=['wf:done', 'wf:ready', 'wf:blocked', 'human'])
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:ready', 'wf:blocked', 'human'})

    def test_nonworkflow_issue_and_pr_are_untouched(self):
        for options in [dict(marker=False, labels=['security', 'wf:custom']),
                        dict(issue={'pull_request': {'url': 'https://example.invalid/pr/17'}})]:
            with self.subTest(options=options):
                result = execute(**options)
                self.assertIsNone(result['failure'])
                self.assertEqual([call['method'] for call in result['calls']], ['get'])

    def test_known_label_opts_in_without_marker_and_string_labels_work(self):
        result = execute(marker=False, issue={'labels': ['wf:review', 'human']})
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:done', 'human'})

    def test_source_marker_retains_workflow_identity_after_cancellation(self):
        result = execute(state='open', reason='reopened', labels=['human'], dispatch=True)
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:backlog', 'human'})

    def test_unknown_reason_and_ambiguous_phase_fail_without_writes(self):
        for options in [dict(reason=None), dict(reason='unknown'),
                        dict(state='open', reason='reopened', labels=['wf:ready', 'wf:review', 'wf:done'])]:
            with self.subTest(options=options):
                result = execute(**options)
                self.assertIsNotNone(result['failure'])
                self.assertEqual([call['method'] for call in result['calls']], ['get'])

    def test_dispatch_validates_number_before_api_use(self):
        for number in ['0', '-1', '17;touch /tmp/not-executed', '', '9007199254740993']:
            with self.subTest(number=number):
                result = execute(dispatch=True, number=number)
                self.assertIn('positive Issue number', result['failure'])
                self.assertEqual(result['calls'], [])
        result = execute(dispatch=True, number='17')
        self.assertIsNone(result['failure'])
        self.assertTrue(all(call['args'].get('issue_number', 17) == 17 for call in result['calls']))

    def test_permission_failures_are_not_reported_as_success(self):
        for operation in ['get', 'getLabel', 'createLabel', 'addLabels', 'removeLabel']:
            with self.subTest(operation=operation):
                result = execute(fail=operation, repository_labels=[])
                self.assertIn('Denied fixture operation', result['failure'])
                self.assertIn('security', label_names(result))
                self.assertFalse(any('Reconciled' in log for log in result['logs']))

    def test_missing_label_is_created_and_concurrent_creation_is_reconciled(self):
        for race in [False, True]:
            with self.subTest(race=race):
                result = execute(repository_labels=[], label_creation_race=race)
                self.assertIsNone(result['failure'])
                self.assertIn('wf:done', result['repository_labels'])
                self.assertEqual(label_names(result), {'wf:done', 'security', 'wf:custom'})
                self.assertEqual(sum(call['method'] == 'createLabel' for call in result['calls']), 1)

    def test_concurrent_custom_edit_and_removed_label_are_preserved(self):
        result = execute(add_custom_label=True, remove_404=True)
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:done', 'security', 'wf:custom', 'human-added-during-run'})

    def test_delayed_close_event_uses_current_reopened_state(self):
        result = execute(state='open', reason='reopened', labels=['wf:done', 'human'],
                         event_labels=[{'name': 'wf:review'}])
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:backlog', 'human'})

    def test_state_changes_during_mutation_converge_from_fresh_state(self):
        for options, expected in [(dict(reopen_after_add=True), {'wf:backlog', 'security', 'wf:custom'}),
                                  (dict(state='open', reason='reopened', labels=['wf:done', 'human'],
                                        close_after_remove=True), {'wf:done', 'human'})]:
            with self.subTest(options=options):
                result = execute(**options)
                self.assertIsNone(result['failure'])
                self.assertEqual(label_names(result), expected)

    def test_repeated_competing_edits_fail_visibly(self):
        result = execute(continuous_edit=True)
        self.assertIn('changed repeatedly', result['failure'])
        self.assertFalse(any('Reconciled' in log for log in result['logs']))

    def test_action_has_bounded_permissions_and_never_executes_issue_text(self):
        text = ACTION.read_text()
        self.assertIn('types: [closed, reopened]', text)
        self.assertIn('workflow_dispatch:', text)
        self.assertIn('issues: write', text)
        self.assertNotIn('actions/checkout', text)
        self.assertNotIn('pull_request_target', text)
        self.assertNotRegex(text, r'(?m)^\s+(contents|pull-requests|actions):\s*write')
        self.assertNotIn('${{', text.split('          script: |\n', 1)[1])
        result = execute(issue={'body': '<!-- workflow-source: fixture -->\n${{ secrets.TOKEN }}; throw new Error("BODY EXECUTED")'})
        self.assertIsNone(result['failure'])


class InstalledCompletionTests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp

    def test_installed_action_executes_same_completion_behavior(self):
        run(*self.args, '--apply')
        path = self.target / '.github/workflows/workflow-v2-issue-completion.yml'
        self.assertEqual(path.read_bytes(), ACTION.read_bytes())
        result = execute(path)
        self.assertIsNone(result['failure'])
        self.assertEqual(label_names(result), {'wf:done', 'security', 'wf:custom'})
        manifest = json.loads((self.target / '.workflow/install-manifest.json').read_text())
        self.assertIn(path.relative_to(self.target).as_posix(), manifest['files'])

    def test_completion_workflow_collision_and_modified_uninstall_preserve_customer(self):
        path = self.target / '.github/workflows/workflow-v2-issue-completion.yml'
        path.parent.mkdir(parents=True)
        path.write_text('customer-owned completion workflow')
        result = run(*self.args, '--apply', expect=1)
        self.assertFalse(result['ok'])
        self.assertEqual(path.read_text(), 'customer-owned completion workflow')
        self.assertFalse((self.target / '.workflow').exists())
        path.unlink()
        run(*self.args, '--apply')
        path.write_text('human modified completion workflow')
        run(*self.args, '--apply', expect=1)
        result = run('setup', '--target', self.target, '--uninstall', '--apply', expect=1)
        self.assertIn(path.relative_to(self.target).as_posix(), result['residuals'])
        self.assertEqual(path.read_text(), 'human modified completion workflow')

    def test_old_pin_remains_valid_and_explicit_update_installs_new_required_asset(self):
        bundle = self.source / '.workflow/bundle.json'
        spec = json.loads(bundle.read_text())
        path = '.github/workflows/workflow-v2-issue-completion.yml'
        spec['assets'] = {source: dest for source, dest in spec['assets'].items() if dest != path}
        bundle.write_text(json.dumps(spec))
        old_sha = commit(self.source)
        args = ['setup', '--source', self.source, '--revision', old_sha, '--target', self.target,
                '--repository', 'fixture/consumer']
        run(*args, '--apply')
        commit(self.target)
        run('check', '--repo', self.target)
        self.assertFalse((self.target / path).exists())
        spec['bundle_version'] = '2.1.0'
        bundle.write_text(json.dumps(spec))
        incomplete_sha = commit(self.source)
        run('setup', '--source', self.source, '--revision', incomplete_sha,
            '--target', self.target, '--repository', 'fixture/consumer', '--apply', expect=1)
        self.assertFalse((self.target / path).exists())
        spec['assets'][path] = path
        bundle.write_text(json.dumps(spec))
        new_sha = commit(self.source)
        update = ['setup', '--source', self.source, '--revision', new_sha,
                  '--target', self.target, '--repository', 'fixture/consumer']
        preview = run(*update)
        self.assertTrue(preview['ok'])
        self.assertFalse((self.target / path).exists())
        run(*update, '--apply')
        commit(self.target)
        run('check', '--repo', self.target)
        self.assertEqual((self.target / path).read_bytes(), ACTION.read_bytes())
        run(*update, '--apply')  # Matching adoption is an offline no-op.
        run('setup', '--target', self.target, '--uninstall', '--apply')
        self.assertFalse((self.target / path).exists())

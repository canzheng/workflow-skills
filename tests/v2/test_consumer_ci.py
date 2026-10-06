"""Installed CI executes consumer configuration and respects setup ownership."""
import json
import os
import textwrap
import re
import subprocess
import unittest

import test_setup
from test_setup import run


class ConsumerCITests(unittest.TestCase):
    setUp = test_setup.SetupTests.setUp
    def test_installed_workflow_runs_application_commands_and_propagates_failure(self):
        run(*self.args, '--apply')
        workflow = self.target / '.github/workflows/workflow-v2-verify.yml'
        text = workflow.read_text()
        self.assertNotIn('npm ci', text)
        self.assertNotIn('tools/workflow/verify.py', text)
        self.assertIn('contents: read', text)
        self.assertNotIn('pull_request_target', text)
        scripts = re.findall(r'^\s+run: (.+)$|^      - run: (.+)$', text, re.M)
        steps = [left or right for left, right in scripts]
        self.assertEqual(len(steps), 3)
        preparation = re.search(r'run: \|\n((?:          .*\n)+)', text).group(1)
        environment = self.base / 'github-env'
        runner = self.base / 'runner-temp'
        runner.mkdir()
        env = dict(os.environ, GITHUB_ENV=str(environment), RUNNER_TEMP=str(runner),
                   GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='url.' + self.source.as_uri() + '.insteadOf',
                   GIT_CONFIG_VALUE_0='https://github.com/canzheng/workflow-skills.git')
        result = subprocess.run(textwrap.dedent(preparation), shell=True, executable='/bin/bash',
                                cwd=self.target, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        env.update(line.split('=', 1) for line in environment.read_text().splitlines())
        steps = steps[1:]
        self.assertIn('bootstrap --repo . --apply --json', text)
        self.assertEqual(subprocess.run(steps[0], shell=True, cwd=self.target,
                                       capture_output=True, env=env).returncode, 0)
        script = steps[1]
        cp = self.target / '.workflow/config.json'
        config = json.loads(cp.read_text())
        config['verification']['local'] = [['python3', '-c', "from pathlib import Path; Path('application-ran').write_text('yes')"]]
        cp.write_text(json.dumps(config))
        result = subprocess.run(script, shell=True, cwd=self.target, capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.target / 'application-ran').read_text(), 'yes')
        evidence = json.loads((self.target / 'verification.json').read_text())
        self.assertTrue(any(x['code'] == 'verification.passed' for x in evidence['findings']))
        config['verification']['local'] = [['python3', '-c', 'import sys; sys.exit(7)']]
        cp.write_text(json.dumps(config))
        result = subprocess.run(script, shell=True, cwd=self.target, capture_output=True, text=True, env=env)
        self.assertEqual(result.returncode, 1)
        evidence = json.loads((self.target / 'verification.json').read_text())
        self.assertTrue(any(x['code'] == 'verification.failed' and 'exited 7' in x['message'] for x in evidence['findings']))
        # Integration is deliberately not launched by the generic local CI job.
        config['verification']['local'] = [['python3', '-c', 'pass']]
        config['verification']['integration'] = [['python3', '-c', "from pathlib import Path; Path('wrong-environment').touch()"]]
        cp.write_text(json.dumps(config))
        self.assertEqual(subprocess.run(script, shell=True, cwd=self.target, capture_output=True, env=env).returncode, 0)
        self.assertFalse((self.target / 'wrong-environment').exists())
        metadata = (self.target / '.github/workflows/workflow-v2-pr-metadata.yml').read_text()
        self.assertIn('github.event.pull_request.base.sha', metadata)
        self.assertIn('edited, synchronize', metadata)
        self.assertIn('--metadata-only', metadata)
        self.assertNotIn('--run-local', metadata)
        self.assertNotRegex(metadata, r'(?m)^\s+(?:contents|pull-requests):\s*write')

    def test_workflow_collision_and_modified_update_uninstall_preserve_customer_files(self):
        p = self.target / '.github/workflows/workflow-v2-verify.yml'
        p.parent.mkdir(parents=True)
        p.write_text('customer-owned workflow')
        run(*self.args, '--apply', expect=1)
        self.assertEqual(p.read_text(), 'customer-owned workflow')
        self.assertFalse((self.target / '.workflow').exists())
        p.unlink()
        run(*self.args, '--apply')
        p.write_text('modified managed workflow')
        run(*self.args, '--apply', expect=1)
        self.assertEqual(p.read_text(), 'modified managed workflow')
        result = run('setup', '--target', self.target, '--uninstall', '--apply', expect=1)
        self.assertIn('.github/workflows/workflow-v2-verify.yml', result['residuals'])
        self.assertEqual(p.read_text(), 'modified managed workflow')

    def test_consumer_manifest_wins_over_unrelated_bundle_marker_in_both_workflows(self):
        marker = self.target / '.workflow/bundle.json'
        marker.parent.mkdir()
        marker.write_text('{"project_owned": "not a workflow source"}\n')
        test_setup.commit(self.target)
        run(*self.args, '--apply')
        head = test_setup.commit(self.target)
        index = (self.target / '.git/index').read_bytes()
        original = marker.read_bytes()
        from test_checks import BODY
        event = self.base / 'event.json'
        event.write_text(json.dumps(dict(repository={'full_name': 'fixture/consumer'},
                         pull_request=dict(body=BODY, head={'sha': head},
                                           base={'repo': {'full_name': 'fixture/consumer'}}))))
        for name in ['workflow-v2-verify.yml', 'workflow-v2-pr-metadata.yml']:
            with self.subTest(workflow=name):
                text = (self.target / '.github/workflows' / name).read_text()
                preparation = re.search(r'run: \|\n((?:          .*\n)+)', text).group(1)
                runner = self.base / name
                runner.mkdir()
                environment = runner / 'env'
                env = dict(os.environ, GITHUB_ENV=str(environment), RUNNER_TEMP=str(runner),
                           GITHUB_EVENT_PATH=str(event), GIT_CONFIG_COUNT='1',
                           GIT_CONFIG_KEY_0='url.' + self.source.as_uri() + '.insteadOf',
                           GIT_CONFIG_VALUE_0='https://github.com/canzheng/workflow-skills.git')
                q = subprocess.run(textwrap.dedent(preparation), shell=True, executable='/bin/bash',
                                   cwd=self.target, env=env, capture_output=True, text=True)
                self.assertEqual(q.returncode, 0, q.stdout + q.stderr)
                env.update(line.split('=', 1) for line in environment.read_text().splitlines())
                checker = test_setup.pathlib.Path(env['WF2_CHECKER'])
                self.assertTrue(checker.is_file(), str(checker))
                self.assertNotEqual(checker.parent.parent.parent, self.target)
                scripts = re.findall(r'^      - run: (.+)$', text, re.M)
                for script in scripts:
                    q = subprocess.run(script, shell=True, cwd=self.target, env=env,
                                       capture_output=True, text=True)
                    self.assertEqual(q.returncode, 0, q.stdout + q.stderr)
                self.assertEqual(marker.read_bytes(), original)
                self.assertEqual((self.target / '.git/index').read_bytes(), index)
                self.assertEqual(run('doctor', '--repo', self.target)['mode'], 'installed-consumer')

    def test_verification_uses_manifest_runtime_for_legacy_tracked_consumer(self):
        from core import RUNTIME_PREFIX, LEGACY_RUNTIME_PREFIX
        bundle = self.source / '.workflow/bundle.json'
        spec = json.loads(bundle.read_text())
        spec['assets'] = {src: dest.replace(RUNTIME_PREFIX, LEGACY_RUNTIME_PREFIX, 1)
                          for src, dest in spec['assets'].items()}
        bundle.write_text(json.dumps(spec))
        sha = test_setup.commit(self.source)
        run('setup', '--source', self.source, '--revision', sha, '--target', self.target,
            '--repository', 'fixture/consumer', '--dependency-storage', 'tracked', '--apply')
        test_setup.commit(self.target)
        text = (self.target / '.github/workflows/workflow-v2-verify.yml').read_text()
        preparation = re.search(r'run: \|\n((?:          .*\n)+)', text).group(1)
        runner = self.base / 'legacy-runner'
        runner.mkdir()
        environment = runner / 'env'
        env = dict(os.environ, GITHUB_ENV=str(environment), RUNNER_TEMP=str(runner),
                   GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='url.' + self.source.as_uri() + '.insteadOf',
                   GIT_CONFIG_VALUE_0='https://github.com/canzheng/workflow-skills.git')
        q = subprocess.run(textwrap.dedent(preparation), shell=True, executable='/bin/bash',
                           cwd=self.target, env=env, capture_output=True, text=True)
        self.assertEqual(q.returncode, 0, q.stdout + q.stderr)
        env.update(line.split('=', 1) for line in environment.read_text().splitlines())
        self.assertEqual(env['WF2_RUNTIME'], str(self.target / 'tools/workflow/workflow.py'))
        for script in re.findall(r'^      - run: (.+)$', text, re.M):
            q = subprocess.run(script, shell=True, cwd=self.target, env=env, capture_output=True, text=True)
            self.assertEqual(q.returncode, 0, q.stdout + q.stderr)
        self.assertTrue(json.loads((self.target / 'verification.json').read_text())['ok'])

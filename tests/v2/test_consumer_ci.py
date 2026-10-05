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
        env['WF2_CHECKER'] = environment.read_text().strip().split('=', 1)[1]
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

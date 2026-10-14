"""Execute the YAML fetch against a real auth-gated local Git HTTP backend.

This models private-repository transport, not GitHub Actions or token policy.
"""
import base64
import http.server
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest

from test_setup import ROOT, TOOLS, init, commit, fixture_source, run
from test_checks import BODY


class MetadataCredentialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        source, target = self.root / 'source', self.root / 'target'
        revision = fixture_source(source)
        init(target)
        (target / 'baseline').write_text('base')
        commit(target)
        run('setup', '--source', source, '--revision', revision, '--target', target,
            '--repository', 'fixture/consumer', '--apply')
        self.base = commit(target)
        # Only head contains this link target and executable-looking data.
        (target / 'head-only.md').write_text('# Head\n')
        (target / 'never-run.py').write_text("raise RuntimeError('HEAD CODE EXECUTED')\n")
        self.head = commit(target)
        bare = self.root / 'fixture/consumer.git'
        bare.parent.mkdir()
        subprocess.run(['git', 'clone', '--bare', '-q', str(target), str(bare)], check=True)
        self.checkout = self.root / 'checkout'
        init(self.checkout)
        self.git('fetch', '-q', '--depth=1', bare.as_uri(), self.base)
        self.git('checkout', '-q', '--detach', self.base)
        self.token = 'synthetic-regression-token-NOT-A-GITHUB-CREDENTIAL'
        expected = 'AUTHORIZATION: basic ' + base64.b64encode(
            ('x-access-token:' + self.token).encode()).decode()
        self.requests = []
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                self.handle_git()

            def do_POST(self):
                self.handle_git()

            def handle_git(self):
                authorized = self.headers.get('Authorization') == expected.split(': ', 1)[1]
                outer.requests.append(authorized)
                if not authorized:
                    self.send_response(401)
                    self.send_header('WWW-Authenticate', 'Basic realm="private-fixture"')
                    self.end_headers()
                    return
                path, _, query = self.path.partition('?')
                env = dict(os.environ, GIT_PROJECT_ROOT=str(outer.root), GIT_HTTP_EXPORT_ALL='1',
                           PATH_INFO=path, QUERY_STRING=query, REQUEST_METHOD=self.command,
                           CONTENT_TYPE=self.headers.get('Content-Type', ''),
                           CONTENT_LENGTH=self.headers.get('Content-Length', '0'),
                           REMOTE_USER='fixture', SERVER_PROTOCOL='HTTP/1.1')
                result = subprocess.run(['git', 'http-backend'], env=env,
                                        input=self.rfile.read(int(env['CONTENT_LENGTH'])),
                                        capture_output=True, check=True)
                headers, body = result.stdout.split(b'\r\n\r\n', 1)
                self.send_response(200)
                for header in headers.decode().split('\r\n'):
                    key, value = header.split(':', 1)
                    self.send_header(key, value.strip())
                self.end_headers()
                self.wfile.write(body)

        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        def stop():
            self.server.shutdown()
            self.server.server_close()
            thread.join()
        self.addCleanup(stop)
        server_url = 'http://127.0.0.1:' + str(self.server.server_port)
        self.url = server_url + '/fixture/consumer.git'
        self.git('remote', 'add', 'origin', self.url)
        self.event = self.root / 'event.json'
        self.payload = dict(repository={'full_name': 'fixture/consumer'}, pull_request=dict(
            body=BODY.replace('Repair existing behavior.', '[Head](head-only.md).'),
            head={'sha': self.head, 'repo': {'clone_url': 'https://attacker.invalid/fork.git'}},
            base={'repo': {'full_name': 'fixture/consumer'}}))
        self.event.write_text(json.dumps(self.payload))
        self.environment = dict(os.environ, GITHUB_REPOSITORY='fixture/consumer',
                                GITHUB_SERVER_URL=server_url, GITHUB_EVENT_PATH=str(self.event),
                                GIT_TERMINAL_PROMPT='0')
        # Observe the actual process boundary without recording credential values.
        self.audit = self.root / 'git-audit.jsonl'
        wrapper_dir = self.root / 'bin'
        wrapper_dir.mkdir()
        wrapper = wrapper_dir / 'git'
        real_git = shutil.which('git')
        wrapper.write_text('#!' + sys.executable + '\n' + textwrap.dedent("""
            import json, os, sys
            with open(os.environ['WF2_TEST_AUDIT'], 'a') as output:
                output.write(json.dumps(dict(
                    fetch='fetch' in sys.argv[1:],
                    token='WF2_FETCH_TOKEN' in os.environ,
                    auth='WF2_FETCH_AUTH' in os.environ,
                    secret_in_argv=any('AUTHORIZATION: basic ' in arg for arg in sys.argv[1:])
                )) + '\\n')
            os.execv(REAL_GIT, [REAL_GIT, *sys.argv[1:]])
        """.replace('REAL_GIT', repr(real_git))))
        wrapper.chmod(0o755)
        self.environment.update(PATH=str(wrapper_dir) + os.pathsep + os.environ['PATH'],
                                WF2_TEST_AUDIT=str(self.audit))
        workflow = (ROOT / '.github/workflows/pr-metadata.yml').read_text()
        fetch_step = workflow.split('      - name: Fetch PR head objects\n', 1)[1]
        block = re.search(r'        run: \|\n((?:          .*\n)+)', fetch_step).group(1)
        self.script = textwrap.dedent(block)
        self.config = (self.checkout / '.git/config').read_bytes()
        self.index = (self.checkout / '.git/index').read_bytes()

    def git(self, *args, **kwargs):
        return subprocess.run(['git', '-C', str(self.checkout), *map(str, args)],
                              capture_output=True, check=kwargs.pop('check', True), **kwargs)

    def fetch(self, token=None):
        env = dict(self.environment, WF2_FETCH_TOKEN=self.token if token is None else token)
        result = subprocess.run(['bash', '-e', '-c', self.script], cwd=self.checkout,
                                env=env, capture_output=True, text=True)
        self.assertNotIn(self.token, result.stdout + result.stderr)
        encoded = base64.b64encode(('x-access-token:' + self.token).encode()).decode()
        self.assertNotIn(encoded, result.stdout + result.stderr)
        return result

    def assert_unchanged(self):
        self.assertEqual((self.checkout / '.git/config').read_bytes(), self.config)
        self.assertEqual((self.checkout / '.git/index').read_bytes(), self.index)
        self.assertEqual(self.git('rev-parse', 'HEAD').stdout.decode().strip(), self.base)
        self.assertFalse((self.checkout / 'head-only.md').exists())
        self.assertEqual(self.git('status', '--porcelain').stdout, b'')

    def test_missing_private_head_fetches_then_checker_runs_without_credentials(self):
        self.assertNotEqual(self.git('cat-file', '-e', self.head, check=False).returncode, 0)
        # Negative control: disabling persistence without prefetch breaks private fetch.
        denied = self.git('fetch', '--no-tags', 'origin', self.head, check=False,
                          env=self.environment)
        self.assertNotEqual(denied.returncode, 0)
        self.assertFalse(any(self.requests))
        self.requests.clear()
        # Prefetch must use the trusted base URL rather than origin or head.repo.
        self.git('remote', 'set-url', 'origin', 'http://127.0.0.1:1/unreachable.git')
        result = self.fetch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.requests)
        self.assertTrue(all(self.requests))
        count = len(self.requests)
        audit = [json.loads(line) for line in self.audit.read_text().splitlines()]
        authenticated = [row for row in audit if row['auth']]
        self.assertEqual(len(authenticated), 1)
        self.assertTrue(authenticated[0]['fetch'])
        self.assertFalse(any(row['token'] or row['secret_in_argv'] for row in audit))
        self.audit.write_text('')
        # Invalid origin proves the checker uses already-fetched blobs, no auth/network.
        self.git('remote', 'set-url', 'origin', 'http://127.0.0.1:1/unreachable.git')
        result = subprocess.run([sys.executable, str(TOOLS / 'workflow.py'), 'check',
                                 '--repo', str(self.checkout), '--pr-json', str(self.event),
                                 '--metadata-only', '--json'], env=self.environment,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)['ok'])
        self.assertEqual(len(self.requests), count)
        audit = [json.loads(line) for line in self.audit.read_text().splitlines()]
        self.assertTrue(audit)
        self.assertFalse(any(row['auth'] or row['token'] or row['fetch'] for row in audit))
        self.git('remote', 'set-url', 'origin', self.url)
        self.assert_unchanged()

    def test_present_head_does_not_fetch(self):
        self.assertEqual(self.fetch().returncode, 0)
        self.requests.clear()
        self.assertEqual(self.fetch(token='invalid').returncode, 0)
        self.assertEqual(self.requests, [])
        self.assert_unchanged()

    def test_denied_fetch_stops_without_persisting_credentials(self):
        result = self.fetch(token='invalid')
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(self.requests)
        self.assertFalse(any(self.requests))
        self.assertNotEqual(self.git('cat-file', '-e', self.head, check=False).returncode, 0)
        self.assert_unchanged()

    def test_invalid_sha_or_wrong_repository_never_fetches(self):
        for sha, repository in [('HEAD; touch injected', 'fixture/consumer'),
                                (self.head, 'attacker/other')]:
            with self.subTest(sha=sha, repository=repository):
                self.payload['pull_request']['head']['sha'] = sha
                self.payload['repository']['full_name'] = repository
                self.event.write_text(json.dumps(self.payload))
                self.assertNotEqual(self.fetch().returncode, 0)
                self.assertEqual(self.requests, [])
                self.assert_unchanged()

    def test_yaml_limits_token_to_fetch_step(self):
        text = (ROOT / '.github/workflows/pr-metadata.yml').read_text()
        self.assertIn('persist-credentials: false', text)
        self.assertEqual(text.count('${{ github.token }}'), 1)
        before, after = text.split('      - uses: actions/setup-python@v5')
        self.assertIn('WF2_FETCH_TOKEN:', before)
        self.assertNotIn('WF2_FETCH_TOKEN', after)
        self.assertNotIn('WF2_FETCH_AUTH', after)
        self.assertNotIn('GITHUB_ENV', self.script)
        self.assertNotIn('git config', self.script)
        self.assertNotIn('write', text)

    def test_persisted_header_is_readable_and_reversible_by_child(self):
        encoded = base64.b64encode(('x-access-token:' + self.token).encode()).decode()
        self.git('config', 'http.https://github.com/.extraheader', 'AUTHORIZATION: basic ' + encoded)
        # Reproduce checkout's persisted format with synthetic data only.
        probe = subprocess.run([sys.executable, '-c',
            "import base64, subprocess; "
            "value=subprocess.check_output(['git','config','--get',"
            "'http.https://github.com/.extraheader'], text=True).strip(); "
            "assert base64.b64decode(value.split()[-1]).decode().startswith('x-access-token:')"],
            cwd=self.checkout, capture_output=True)
        self.assertEqual(probe.returncode, 0)
        self.assertEqual(probe.stdout, b'')
        self.assertEqual(probe.stderr, b'')

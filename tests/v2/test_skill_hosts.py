"""Skill hosts: Codex (.agents/skills), Claude Code (.claude/skills) or both (#26)."""
import json
import os
import shutil
import subprocess
import sys
import unittest

import test_setup
from core import IGNORE_START, SKILLS, git
from test_setup import ROOT, TOOLS, commit, init

SHARED = [s + '/SKILL.md' for s in SKILLS] + ['workflow-risk-review/references/methods.md']
V1_SECTION = ('<!-- Beginning of Workflow Section -->\n<!-- DO NOT EDIT BELOW SECTION MANUALLY. -->\n'
              'Invoke start-task.\n<!-- End of Workflow Section -->\n')


def documented(intro):
    """The shell block after an intro line, identical in source and consumer operations docs."""
    blocks = []
    for name in ('docs/operations.md', 'templates/consumer/operations.md'):
        text = (ROOT / name).read_text()
        start = text.index('```sh\n', text.index(intro)) + len('```sh\n')
        blocks.append(text[start:text.index('```', start)])
    assert blocks[0] == blocks[1], 'operations docs disagree: ' + intro
    return blocks[0]


class DocumentedV1CleanupTests(unittest.TestCase):
    """Run the documented cleanup in bash and zsh against the same fixture."""

    def setUp(self):
        self.temp = test_setup.tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = test_setup.pathlib.Path(self.temp.name)

    def shells(self):
        found = [s for s in ('bash', 'zsh') if shutil.which(s)]
        if 'zsh' not in found:
            self.skipTest('zsh is not installed; the bash run alone cannot prove zsh behavior')
        return found

    def write(self, path, text, mode=0o644):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        path.chmod(mode)

    def seed(self, root, prefix):
        """v1 folder, v1 package, live and dangling links, third-party and v2 skills."""
        self.write(root / prefix / '.agents/skills/start-task/SKILL.md', 'Update docs/planning/BACKLOG.md.\n')
        self.write(root / prefix / '.agents/skills/_workflow/cli_helpers.py', 'LEDGER = "docs/planning/BACKLOG.md"\n')
        self.write(root / prefix / '.agents/skills/fastlane/SKILL.md', '---\nname: fastlane\n---\nShip iOS apps.\n')
        self.write(root / prefix / '.agents/skills/workflow-deliver-issue/SKILL.md', 'v2 skill.\n')
        (root / prefix / '.claude/skills').mkdir(parents=True)
        (root / prefix / '.claude/skills/start-task').symlink_to('../../.agents/skills/start-task')
        (root / prefix / '.claude/skills/complete-task').symlink_to('/nonexistent/v1/complete-task')

    def test_documented_global_cleanup_moves_exactly_v1_items(self):
        script = documented('Global skills, from any directory:')
        results = []
        for shell in self.shells():
            home = self.base / (shell + '-home')
            self.seed(home, '')
            dangling = home / '.codex/skills/audit-workflow'
            dangling.parent.mkdir(parents=True)
            dangling.symlink_to('/Users/someone/.agent/skills/audit-workflow')
            self.write(home / '.agents/AGENTS.md', 'Keep this.\n' + V1_SECTION + 'And this.\n', 0o600)
            r = subprocess.run([shell, '-f' if shell == 'zsh' else '--norc', '-c', script], capture_output=True,
                               text=True, env={**os.environ, 'HOME': str(home)})
            self.assertEqual(r.returncode, 0, shell + r.stdout + r.stderr)
            backups = list(home.glob('.workflow-v1-backup-*'))
            self.assertEqual(len(backups), 1, shell)
            moved = sorted(p.relative_to(backups[0]).as_posix() for p in backups[0].glob('.*/skills/*'))
            kept = sorted(p.relative_to(home).as_posix() for p in home.glob('.*/skills/*'))
            agents = home / '.agents/AGENTS.md'
            results.append((moved, kept, agents.read_text(), agents.stat().st_mode & 0o777))
            self.assertTrue((backups[0] / '.agents-AGENTS.md').is_file())
        self.assertEqual(results[0][0], ['.agents/skills/_workflow', '.agents/skills/start-task',
                                         '.claude/skills/complete-task', '.claude/skills/start-task',
                                         '.codex/skills/audit-workflow'])
        self.assertEqual(results[0][1], ['.agents/skills/fastlane', '.agents/skills/workflow-deliver-issue'])
        self.assertEqual(results[0][2:], ('Keep this.\nAnd this.\n', 0o600))
        self.assertEqual(results[0], results[1])  # bash and zsh agree.

    def test_documented_repository_cleanup_moves_exactly_v1_items(self):
        script = documented('Repository-local copies, from the repository root:')
        results = []
        for shell in self.shells():
            repo = self.base / (shell + '-repo')
            init(repo)
            self.seed(repo, '')
            self.write(repo / 'AGENTS.md', 'Keep this.\n' + V1_SECTION)
            commit(repo)
            r = subprocess.run([shell, '-f' if shell == 'zsh' else '--norc', '-c', script], cwd=repo,
                               capture_output=True, text=True, env={**os.environ, 'HOME': str(self.base / 'unused')})
            self.assertEqual(r.returncode, 0, shell + r.stdout + r.stderr)
            kept = sorted(p.relative_to(repo).as_posix() for p in repo.glob('.*/skills/*'))
            status = sorted(git(repo, 'status', '--porcelain').decode().splitlines())
            results.append((kept, status, (repo / 'AGENTS.md').read_text()))
            self.assertEqual(len(list((repo / '.git').glob('workflow-v1-backup-*'))), 1)
        self.assertEqual(results[0][0], ['.agents/skills/fastlane', '.agents/skills/workflow-deliver-issue'])
        self.assertEqual(results[0][1], [' D .agents/skills/_workflow/cli_helpers.py', ' D .agents/skills/start-task/SKILL.md',
                                         ' D .claude/skills/complete-task', ' D .claude/skills/start-task', ' M AGENTS.md'])
        self.assertEqual(results[0][2], 'Keep this.\n')
        self.assertEqual(results[0], results[1])


class SkillHostTests(unittest.TestCase):
    def setUp(self):
        test_setup.SetupTests.setUp(self)
        self.home = self.base / 'home'
        self.home.mkdir()
        self.setup = self.args[:-2]  # Default ignored dependency storage.

    def cli(self, *args, expect=0, home=None):
        command = [sys.executable, str(TOOLS / 'workflow.py'), *map(str, args), '--json']
        r = subprocess.run(command, capture_output=True, text=True,
                           env={**os.environ, 'HOME': str(home or self.home)})
        self.assertEqual(r.returncode, expect, (command, r.stdout, r.stderr))
        return json.loads(r.stdout)

    def adopt(self, *extra):
        result = self.cli(*self.setup, *extra, '--apply')
        commit(self.target)
        return result

    def manifest(self, root=None):
        return json.loads(((root or self.target) / '.workflow/install-manifest.json').read_text())

    def policy(self):
        return (self.target / '.gitignore').read_text()

    def snapshot(self):
        files = {p.relative_to(self.target): p.read_bytes() for p in self.target.rglob('*')
                 if p.is_file() and not p.is_symlink() and '.git' not in p.relative_to(self.target).parts}
        return files, (self.target / '.git/index').read_bytes()

    def assert_installed(self, folder, root=None):
        root = root or self.target
        source = self.source / '.agents/skills'
        for name in SHARED:
            self.assertEqual((root / folder / name).read_bytes(), (source / name).read_bytes(), folder + '/' + name)

    def assert_absent(self, folder, root=None):
        for name in SHARED:
            self.assertFalse(((root or self.target) / folder / name).exists(), folder + '/' + name)

    def test_default_is_codex_and_omitted_host_keeps_recorded_choice(self):
        self.adopt()
        self.assert_installed('.agents/skills')
        self.assertNotIn('hosts', self.manifest())
        self.assertNotIn('.claude', self.policy())
        self.assertFalse((self.target / '.claude').exists())
        self.adopt('--host', 'claude')
        self.assertEqual(self.manifest()['hosts'], ['claude'])
        before = self.snapshot()
        self.assertEqual(self.cli(*self.setup, '--apply')['changes'], [])  # Forgetting --host never switches.
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.manifest()['hosts'], ['claude'])

    def test_claude_only_installs_ignored_copies_and_keeps_one_runtime(self):
        self.adopt('--host', 'claude')
        self.assert_installed('.claude/skills')
        self.assert_absent('.agents/skills')
        self.assertTrue((self.target / '.agents/tools/workflow/workflow.py').is_file())
        self.assertFalse((self.target / '.claude/tools').exists())
        self.assertEqual(git(self.target, 'ls-files', '--', '.claude', '.agents'), b'')
        for s in SKILLS:
            self.assertIn('/.claude/skills/' + s + '/', self.policy())
            self.assertNotIn('/.agents/skills/' + s + '/', self.policy())
        agents = (self.target / 'AGENTS.md').read_text()
        self.assertIn('workflow-skills v2 in .claude/skills/.', agents)
        self.assertIn('before Claude Code starts', agents)
        self.assertEqual(self.manifest()['hosts'], ['claude'])
        self.cli('check', '--repo', self.target)
        self.cli('doctor', '--repo', self.target)

    def test_both_installs_identical_copies_in_each_folder(self):
        self.adopt('--host', 'both')
        self.assert_installed('.agents/skills')
        self.assert_installed('.claude/skills')
        self.assertEqual(self.manifest()['hosts'], ['codex', 'claude'])
        self.assertIn('before Codex or Claude Code starts', (self.target / 'AGENTS.md').read_text())
        self.cli('check', '--repo', self.target)
        self.cli('doctor', '--repo', self.target)

    def test_fresh_clone_bootstrap_restores_exactly_the_recorded_folders(self):
        for host, present, absent in [('claude', ['.claude/skills'], ['.agents/skills']),
                                      ('both', ['.agents/skills', '.claude/skills'], [])]:
            with self.subTest(host=host):
                target = self.base / ('consumer-' + host)
                init(target)
                (target / 'AGENTS.md').write_text('User rule.\n')
                commit(target)
                self.cli('setup', '--source', self.source, '--revision', self.sha, '--target', target,
                         '--repository', 'fixture/consumer', '--host', host, '--apply')
                commit(target)
                fresh = self.base / ('fresh-' + host)
                subprocess.run(['git', 'clone', '--quiet', '--no-local', str(target), str(fresh)], check=True)
                for folder in present + absent:
                    self.assert_absent(folder, fresh)
                self.cli('bootstrap', '--repo', fresh, '--source', self.source, '--apply')
                for folder in present:
                    self.assert_installed(folder, fresh)
                for folder in absent:
                    self.assert_absent(folder, fresh)
                git(fresh, 'remote', 'remove', 'origin')
                self.assertEqual(self.cli('bootstrap', '--repo', fresh, '--apply')['changes'], [])
                self.cli('check', '--repo', fresh)
                self.assertEqual(git(fresh, 'status', '--porcelain'), b'')

    def test_changing_hosts_moves_only_owned_copies_and_keeps_modified_ones(self):
        project = self.target / '.agents/skills/project-rules/SKILL.md'
        project.parent.mkdir(parents=True)
        project.write_text('---\nname: project-rules\ndescription: Human rules\n---\n')
        self.adopt()
        self.adopt('--host', 'both')
        self.assert_installed('.agents/skills')
        self.assert_installed('.claude/skills')
        self.adopt('--host', 'claude')
        self.assert_installed('.claude/skills')
        for name in SHARED:
            self.assertFalse((self.target / '.agents/skills' / name).exists())
        self.assertNotIn('/.agents/skills/', self.policy())
        self.assertTrue(project.is_file())
        self.cli('check', '--repo', self.target)
        edited = self.target / '.claude/skills/workflow-risk-review/SKILL.md'
        edited.write_text('Human edit.\n')
        before = self.snapshot()
        self.cli(*self.setup, '--host', 'codex', '--apply', expect=1)
        self.assertEqual(self.snapshot(), before)

    def test_linked_claude_folder_is_written_once_at_its_real_location(self):
        for host, recorded in [('claude', ['claude']), ('both', ['codex', 'claude'])]:
            with self.subTest(host=host):
                target = self.base / ('linked-' + host)
                init(target)
                (target / 'AGENTS.md').write_text('User rule.\n')
                project = target / '.agents/skills/project-rules/SKILL.md'
                project.parent.mkdir(parents=True)
                project.write_text('---\nname: project-rules\ndescription: Human rules\n---\n')
                (target / '.claude').mkdir()
                (target / '.claude/skills').symlink_to('../.agents/skills')
                commit(target)
                self.cli('setup', '--source', self.source, '--revision', self.sha, '--target', target,
                         '--repository', 'fixture/consumer', '--host', host, '--apply')
                commit(target)
                self.assertEqual(os.readlink(target / '.claude/skills'), '../.agents/skills')
                self.assertIn(b'.claude/skills', git(target, 'ls-files', '--', '.claude'))
                self.assert_installed('.agents/skills', target)
                m = self.manifest(target)
                self.assertEqual(m['hosts'], recorded)
                self.assertFalse(any(name.startswith('.claude/') for name in m['files']))
                self.assertNotIn('/.claude/skills/', (target / '.gitignore').read_text())
                self.cli('check', '--repo', target)
                self.cli('doctor', '--repo', target)
                (target / '.claude/skills').unlink()  # Claude can no longer discover the skills.
                findings = self.cli('doctor', '--repo', target, expect=1)['findings']
                self.assertTrue(any(f['code'] == 'bundle.incomplete' and f['path'].startswith('.claude/skills/')
                                    for f in findings), findings)

    def test_staged_claude_link_is_validated_from_the_index(self):
        (self.target / '.claude').mkdir()
        (self.target / '.claude/skills').symlink_to('../.agents/skills')
        commit(self.target)
        self.adopt('--host', 'claude')

        def stage_link(destination):
            oid = subprocess.run(['git', '-C', str(self.target), 'hash-object', '-w', '--stdin'],
                                 input=os.fsencode(destination), capture_output=True, check=True).stdout
            git(self.target, 'update-index', '--add', '--cacheinfo', '120000,' + oid.decode().strip() + ',.claude/skills')

        # The working link stays correct throughout: only the commit candidate changes.
        for label, change, message in [
                ('deleted', lambda: git(self.target, 'rm', '-q', '--cached', '--', '.claude/skills'), 'Recorded claude host'),
                ('elsewhere', lambda: stage_link('../elsewhere'), 'relative link'),
                ('absolute', lambda: stage_link(str(self.target / '.agents/skills')), 'relative link')]:
            with self.subTest(staged=label):
                change()
                self.assertEqual(os.readlink(self.target / '.claude/skills'), '../.agents/skills')
                for command in ('check', 'doctor'):
                    report = self.cli(command, '--repo', self.target, expect=1)
                    self.assertIn(message, json.dumps(report['findings']), command)
                git(self.target, 'add', '--', '.claude/skills')
                self.cli('check', '--repo', self.target)

    def test_unsupported_claude_folders_refuse_without_writes(self):
        outside = self.base / 'outside skills'
        outside.mkdir()
        (self.target / 'docs').mkdir()
        claude = self.target / '.claude'
        claude.mkdir()
        folder = claude / 'skills'
        cases = {'link inside repository': lambda: folder.symlink_to('../docs'),
                 'link outside repository': lambda: folder.symlink_to(outside),
                 'not a directory': lambda: folder.write_text('file'),
                 'unmanaged shared file': lambda: ((folder / 'workflow-risk-review').mkdir(parents=True),
                                                   (folder / 'workflow-risk-review/SKILL.md').write_text('Mine.\n'))}
        for case, make in cases.items():
            with self.subTest(case=case):
                make()
                before = self.snapshot()
                for host in ('claude', 'both'):
                    self.cli(*self.setup, '--host', host, '--apply', expect=1)
                    self.assertEqual(self.snapshot(), before)
                if folder.is_symlink() or folder.is_file():
                    folder.unlink()
                else:
                    (folder / 'workflow-risk-review/SKILL.md').unlink()
                    (folder / 'workflow-risk-review').rmdir()
                    folder.rmdir()
        command = [sys.executable, str(TOOLS / 'workflow.py'), *map(str, self.setup), '--host', 'cursor', '--json']
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)

    def test_linked_shared_skill_inside_a_real_claude_folder_is_refused(self):
        real = self.target / '.agents/skills/workflow-risk-review'
        real.mkdir(parents=True)
        link = self.target / '.claude/skills/workflow-risk-review'
        link.parent.mkdir(parents=True)
        link.symlink_to('../../.agents/skills/workflow-risk-review')
        before = self.snapshot()
        self.cli(*self.setup, '--host', 'claude', '--apply', expect=2)
        self.assertEqual(self.snapshot(), before)
        self.assertTrue(link.is_symlink())
        self.assertEqual(list(real.iterdir()), [])

    def test_interrupted_second_global_target_keeps_the_first_and_rerun_completes(self):
        import contextlib
        import io
        import pathlib
        from unittest.mock import patch
        import setup as installer
        import workflow
        args = ['install-skills', '--source', str(self.source), '--revision', self.sha, '--host', 'both', '--apply', '--json']
        claude, codex = self.home / '.claude/skills', self.home / '.agents/skills'
        actual = installer.transaction

        def interrupt_claude(root, changes):
            return actual(root, changes, fail_after=1 if root == claude else None)

        with patch.object(installer, 'transaction', interrupt_claude), \
                patch.object(pathlib.Path, 'home', return_value=self.home), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(workflow.main(args), 1)
        self.assert_installed('', codex)
        self.assert_absent('', claude)  # The interrupted target is rolled back.
        self.cli(*args[:-1])
        self.assert_installed('', claude)

    def test_dropping_a_recorded_host_cannot_shrink_requirements_and_setup_repairs(self):
        for dropped in ('.claude/skills/', '.agents/skills/'):
            with self.subTest(dropped=dropped):
                target = self.base / ('dropped-' + dropped.split('/')[0].strip('.'))
                init(target)
                (target / 'AGENTS.md').write_text('User rule.\n')
                commit(target)
                adopt = ('setup', '--source', self.source, '--revision', self.sha, '--target', target,
                         '--repository', 'fixture/consumer')
                self.cli(*adopt, '--host', 'both', '--apply')
                commit(target)
                path = target / '.workflow/install-manifest.json'
                m = json.loads(path.read_text())
                m['files'] = {n: h for n, h in m['files'].items() if not n.startswith(dropped)}
                path.write_text(json.dumps(m, indent=2) + '\n')
                for name in SHARED:
                    (target / dropped / name).unlink()
                commit(target)  # Staged and committed: the tampered snapshot is the candidate.
                for args in [('check', '--repo', target), ('doctor', '--repo', target),
                             ('bootstrap', '--repo', target, '--source', self.source, '--apply')]:
                    report = self.cli(*args, expect=1)
                    self.assertIn('Recorded', json.dumps(report['findings']), args[0])
                self.cli(*adopt, '--apply')  # Omitted --host keeps both and restores the folder.
                self.assert_installed(dropped.rstrip('/'), target)
                commit(target)
                self.cli('check', '--repo', target)

    def test_setup_repairs_a_removed_claude_link_into_real_copies(self):
        (self.target / '.claude').mkdir()
        (self.target / '.claude/skills').symlink_to('../.agents/skills')
        commit(self.target)
        self.adopt('--host', 'claude')
        git(self.target, 'rm', '-q', '--cached', '.claude/skills')
        (self.target / '.claude/skills').unlink()
        commit(self.target)
        self.cli('check', '--repo', self.target, expect=1)
        self.adopt()  # The recorded claude host now lands in a real .claude/skills folder.
        self.assert_installed('.claude/skills')
        self.assert_absent('.agents/skills')
        self.cli('check', '--repo', self.target)
        self.cli('doctor', '--repo', self.target)

    def test_duplicate_skills_are_reported_within_each_host(self):
        self.adopt('--host', 'claude')
        duplicate = self.home / '.claude/skills/workflow-deliver-issue/SKILL.md'
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text('---\nname: workflow-deliver-issue\ndescription: global copy\n---\n')
        findings = self.cli('doctor', '--repo', self.target, expect=1)['findings']
        self.assertTrue(any(f['code'] == 'discovery.duplicate' and 'claude' in f['message'] for f in findings), findings)
        duplicate.unlink()
        self.cli('doctor', '--repo', self.target)

    def test_linked_skill_folders_are_discovered_like_copies(self):
        self.adopt('--host', 'claude')
        store = self.base / 'store'

        def skill(name, folder=store):
            path = folder / name / 'SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text('---\nname: ' + name + '\ndescription: elsewhere\n---\n')
            return path.parent

        def link(catalog, name, destination):
            (self.home / catalog).mkdir(parents=True, exist_ok=True)
            (self.home / catalog / name).symlink_to(destination)

        def doctor(expect):
            findings = self.cli('doctor', '--repo', self.target, expect=expect)['findings']
            return ({f['message'].split(':')[0] for f in findings if f['code'] == 'discovery.duplicate'},
                    [f['path'] for f in findings if f['code'] == 'discovery.inaccessible'])

        # Working links to other skills, a dangling link and one copy per host: nothing to report.
        for catalog in ('.agents/skills', '.codex/skills', '.claude/skills'):
            link(catalog, 'other-' + catalog.split('/')[0].strip('.'), skill('other-' + catalog.split('/')[0].strip('.')))
        link('.claude/skills', 'gone', self.base / 'nowhere')
        self.assertEqual(doctor(0), (set(), []))
        # Home Claude links into home .agents/skills, the common layout: a Claude duplicate,
        # not an unreadable file. The home .agents copy alone is not a Codex duplicate.
        link('.claude/skills', 'workflow-deliver-issue', '../../.agents/skills/workflow-deliver-issue')
        skill('workflow-deliver-issue', self.home / '.agents/skills')
        self.assertEqual(doctor(1), ({'Duplicate active claude name'}, []))
        # A linked Codex catalog entry counts like a copy too.
        (self.home / '.claude/skills/workflow-deliver-issue').unlink()
        link('.codex/skills', 'workflow-deliver-issue', skill('workflow-deliver-issue'))
        self.assertEqual(doctor(1), ({'Duplicate active codex name'}, []))
        # The link is followed only to the skill folder: a linked SKILL.md still is not read.
        (self.home / '.codex/skills/workflow-deliver-issue').unlink()
        target = skill('linked-file')
        (target / 'SKILL.md').rename(target / 'real.md')
        (target / 'SKILL.md').symlink_to('real.md')
        link('.claude/skills', 'linked-file', target)
        self.assertEqual(doctor(0), (set(), [str(self.home / '.claude/skills/linked-file/SKILL.md')]))

    def test_claude_project_skills_must_stay_trackable(self):
        (self.target / '.gitignore').write_text('/.claude/\n')
        commit(self.target)
        before = self.snapshot()
        report = self.cli(*self.setup, '--host', 'claude', '--apply', expect=1)
        self.assertIn('Project-specific skill/tool path is ignored', report['findings'][0]['message'])
        self.assertEqual(self.snapshot(), before)
        (self.target / '.gitignore').write_text('/.claude/settings.local.json\n')
        commit(self.target)
        self.adopt('--host', 'claude')
        self.cli('check', '--repo', self.target)

    def test_recorded_hosts_must_match_installed_folders(self):
        self.adopt('--host', 'both')
        path = self.target / '.workflow/install-manifest.json'
        original = path.read_text()
        for recorded in (['cursor'], ['claude', 'codex'], 'claude', ['codex']):
            with self.subTest(hosts=recorded):
                path.write_text(json.dumps({**json.loads(original), 'hosts': recorded}))
                self.cli('check', '--repo', self.target, expect=2)
        path.write_text(original)
        self.cli('check', '--repo', self.target)

    def test_environment_host_selects_fresh_adoption_and_rejects_a_different_choice(self):
        script = self.source / 'tools/workflow/environment-setup.sh'
        script.write_bytes((TOOLS / 'environment-setup.sh').read_bytes())
        commit(self.source)

        def execute(host, code=0):
            env = {**os.environ, 'HOME': str(self.home)}
            if host is not None:
                env['WF2_HOST'] = host
            r = subprocess.run(['bash', str(script), str(self.target), 'fixture/consumer'],
                               capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode != 0, code != 0, r.stdout + r.stderr)
            if code:
                self.assertEqual(r.returncode, code, r.stdout + r.stderr)
            return r

        execute('both')
        self.assertEqual(self.manifest()['hosts'], ['codex', 'claude'])
        self.assert_installed('.claude/skills')
        commit(self.target)
        execute(None)
        execute('both')
        self.assertIn('differs from the recorded skill hosts', execute('claude', code=1).stderr)
        execute('cursor', code=2)

    def test_uninstall_removes_claude_copies_and_their_ignore_lines(self):
        self.adopt('--host', 'both')
        self.cli('setup', '--target', self.target, '--uninstall', '--apply')
        for folder in ('.agents/skills', '.claude/skills'):
            for name in SHARED:
                self.assertFalse((self.target / folder / name).exists())
        self.assertNotIn(IGNORE_START, self.policy() if (self.target / '.gitignore').exists() else '')

    def test_global_hosts_targets_uninstall_and_linked_target(self):
        args = ('install-skills', '--source', self.source, '--revision', self.sha)
        claude, codex = self.home / '.claude/skills', self.home / '.agents/skills'
        blocker = claude / 'workflow-risk-review/SKILL.md'
        blocker.parent.mkdir(parents=True)
        blocker.write_text('Mine.\n')
        self.cli(*args, '--host', 'both', '--apply', expect=1)
        self.assertFalse(codex.exists())  # A conflict in one target writes no target.
        blocker.unlink()
        self.cli(*args, '--host', 'claude', '--apply')
        self.assert_installed('', claude)
        self.assertTrue((claude / '.workflow-skills-install.json').is_file())
        self.assertFalse(codex.exists())
        result = self.cli(*args, '--host', 'both', '--apply')
        self.assertTrue(all(name.startswith(str(codex) + '/') for name in result['changes']), result)
        self.assert_installed('', codex)
        self.assertTrue((codex / '.workflow-skills-install.json').is_file())
        self.cli(*args, '--host', 'both', '--target', self.base / 'custom', expect=2)
        self.assertFalse((self.base / 'custom').exists())
        self.cli('install-skills', '--host', 'claude', '--uninstall', '--apply')
        self.assert_absent('', claude)
        self.assert_installed('', codex)
        linked_home = self.base / 'linked home'
        real = self.base / 'dotfiles/claude-skills'
        real.mkdir(parents=True)
        (linked_home / '.claude').mkdir(parents=True)
        (linked_home / '.claude/skills').symlink_to(real)
        self.cli(*args, '--host', 'claude', '--apply', home=linked_home)
        self.assert_installed('', real)
        self.assertTrue((linked_home / '.claude/skills').is_symlink())

    def test_likely_v1_skills_are_reported_never_removed(self):
        self.adopt()
        v1 = self.home / '.agents/skills/start-task/SKILL.md'
        v1.parent.mkdir(parents=True)
        v1.write_text('---\nname: start-task\n---\nUpdate docs/planning/BACKLOG.md.\n')
        package = self.home / '.agents/skills/_workflow/cli_helpers.py'
        package.parent.mkdir(parents=True)
        package.write_text('LEDGER = "docs/planning/BACKLOG.md"\n')
        dangling = self.home / '.codex/skills/complete-task'
        dangling.parent.mkdir(parents=True)
        dangling.symlink_to('/nonexistent/v1/complete-task')
        third_party = self.home / '.claude/skills/fastlane/SKILL.md'
        third_party.parent.mkdir(parents=True)
        third_party.write_text('---\nname: fastlane\ndescription: Ship iOS apps\n---\nRun fastlane.\n')
        repo_v1 = self.target / '.claude/skills/audit-workflow/SKILL.md'
        repo_v1.parent.mkdir(parents=True)
        repo_v1.write_text('Run skills/_workflow/audit.py.\n')
        expected = {str(v1.parent), str(package.parent), str(dangling), str(repo_v1.parent)}
        for args in [self.setup, ('doctor', '--repo', self.target),
                     ('install-skills', '--source', self.source, '--revision', self.sha, '--target', self.base / 'custom')]:
            with self.subTest(command=args[0]):
                findings = self.cli(*args)['findings']  # Warnings never fail a command.
                legacy = {f['path'] for f in findings if f['code'] == 'discovery.legacy'}
                self.assertTrue(all(f['severity'] == 'warning' for f in findings if f['code'] == 'discovery.legacy'))
                # Repository folders are scanned by setup and doctor, not by a global install.
                self.assertEqual(legacy, expected if args[0] != 'install-skills' else expected - {str(repo_v1.parent)})
        for path in (v1, package, third_party, repo_v1):
            self.assertTrue(path.is_file())
        self.assertTrue(dangling.is_symlink())


if __name__ == '__main__':
    unittest.main()

"""Negative controls for test_skill_hosts.py: each defect must fail its named test.

Run: python3 tests/v2/mutate_skill_hosts.py   (not collected by verify.py)
Each mutant edits production files (or both operations docs), runs one test, and
always restores them.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOLS = ROOT / 'tools/workflow'
TESTS = ROOT / 'tests/v2'
DOCS = ('docs/operations.md', 'templates/consumer/operations.md')
GLOBAL = 'DocumentedV1CleanupTests.test_documented_global_cleanup_moves_exactly_v1_items'

MUTANTS = [
    ('a .claude/skills link is written through instead of resolved',
     'core.py', '    if folder.is_symlink() or folder.parent.is_symlink():', '    if False:',
     'test_linked_claude_folder_is_written_once_at_its_real_location'),
    ('omitted --host forgets the recorded choice',
     'setup.py', "if requested else hosts(old) if old else HOST_CHOICES['codex']", "if requested else HOST_CHOICES['codex']",
     'test_default_is_codex_and_omitted_host_keeps_recorded_choice'),
    ('claude-only still installs .agents/skills',
     'core.py', "    real = {HOST_SKILL_ROOTS[h] if h == 'codex'", "    real = {HOST_SKILL_ROOTS['codex']} | {HOST_SKILL_ROOTS[h] if h == 'codex'",
     'test_claude_only_installs_ignored_copies_and_keeps_one_runtime'),
    ('ignore block omits the Claude folder',
     'setup.py', "'\\n'.join('/' + r + '/' + s + '/' for r in roots for s in SKILLS)",
     "'\\n'.join('/' + r + '/' + s + '/' for r in ('.agents/skills',) for s in SKILLS)",
     'test_claude_only_installs_ignored_copies_and_keeps_one_runtime'),
    ('check only looks in .agents/skills',
     'checks.py', "roots = skill_roots(m['files']) if m else ('.agents/skills',)", "roots = ('.agents/skills',)",
     'test_claude_only_installs_ignored_copies_and_keeps_one_runtime'),
    ('doctor ignores the Claude discovery path',
     'workflow.py', "for host in hosts(m) if m else ('codex',):", "for host in ('codex',):",
     'test_linked_claude_folder_is_written_once_at_its_real_location'),
    ('bootstrap ignores the recorded folders',
     'bootstrap.py', "        assets = host_assets(assets, skill_roots(m['files']))\n", '',
     'test_fresh_clone_bootstrap_restores_exactly_the_recorded_folders'),
    ('project Claude skills may be ignored',
     'core.py', "    if HOST_SKILL_ROOTS['claude'] in skill_roots(names):\n        # Project-owned",
     "    if False:\n        # Project-owned",
     'test_claude_project_skills_must_stay_trackable'),
    ('recorded hosts are not validated',
     'core.py', 'tuple(selected) not in HOST_CHOICES.values()):', 'False):',
     'test_recorded_hosts_must_match_installed_folders'),
    ('install-skills ignores --host',
     'setup.py', "for h in HOST_CHOICES[requested or 'codex']]", "for h in HOST_CHOICES['codex']]",
     'test_global_hosts_targets_uninstall_and_linked_target'),
    ('install-skills writes each target before planning the next',
     'setup.py', '    preflight_destinations(root, changes)\n    return root, changes, residuals',
     '    preflight_destinations(root, changes)\n    if args.apply:\n        transaction(root, changes)\n'
     '    return root, {} if args.apply else changes, residuals',
     'test_global_hosts_targets_uninstall_and_linked_target'),
    ('v1 detection matches names without content',
     'core.py', 'elif entry.exists() and v1_content(entry.resolve(strict=True)):', 'elif entry.exists():',
     'test_likely_v1_skills_are_reported_never_removed'),
    ('dangling v1 links are not reported',
     'core.py', '                if entry.is_symlink() and not entry.exists():', '                if False:',
     'test_likely_v1_skills_are_reported_never_removed'),
    ('WF2_HOST is not passed to setup',
     'environment-setup.sh', 'set -- "$@" --host "$WF2_HOST"; fi', 'true; fi',
     'test_environment_host_selects_fresh_adoption_and_rejects_a_different_choice'),
    ('a recorded host may silently drop its folder',
     'core.py', "    if 'hosts' not in m:\n        return\n    present", "    if True:\n        return\n    present",
     'test_dropping_a_recorded_host_cannot_shrink_requirements_and_setup_repairs'),
    ('staged validation trusts the working Claude link',
     'core.py', 'recorded_hosts_policy(root, m, lambda root: staged_claude_skill_root(root, entries))',
     'recorded_hosts_policy(root, m)', 'test_staged_claude_link_is_validated_from_the_index'),
    ('a staged absolute Claude link is accepted',
     'core.py', 'if posixpath.isabs(target) or real != codex:', 'if real != codex and not posixpath.isabs(target):',
     'test_staged_claude_link_is_validated_from_the_index'),
    ('setup cannot repair a dropped or relinked host',
     'setup.py', 'dependency_policy(root, old, hosts_policy=False)', 'dependency_policy(root, old)',
     'test_setup_repairs_a_removed_claude_link_into_real_copies'),
    ('doctor reads linked skill folders without following them',
     'workflow.py', 'real = child.resolve(strict=True) if child.is_symlink() else resolved / child.name',
     'real = resolved / child.name', 'test_linked_skill_folders_are_discovered_like_copies'),
    ('doctor follows a linked SKILL.md too',
     'workflow.py', 'text = read_regular(real / p.name)', 'text = read_regular((real / p.name).resolve())',
     'test_linked_skill_folders_are_discovered_like_copies'),
    ('doctor skips the repository Claude catalog',
     'workflow.py', "'claude': [root / '.claude/skills']}", "'claude': []}",
     'test_duplicate_skills_are_reported_within_each_host'),
    ('documented cleanup matches names without content',
     DOCS, 'grep -rqsE \'docs/planning|_workflow|audit-workflow\' "$entry"; then :\n    else continue; fi\n    mkdir -p "$backup${root', 'true; then :\n    else continue; fi\n    mkdir -p "$backup${root', GLOBAL),
    ('documented cleanup relies on word splitting, which zsh does not do',
     DOCS, 'for root in "$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.codex/skills"; do',
     'roots="$HOME/.agents/skills $HOME/.claude/skills $HOME/.codex/skills"; for root in $roots; do', GLOBAL),
]


def main():
    failures = 0
    for label, names, old, new, test in MUTANTS:
        paths = [ROOT / n for n in names] if isinstance(names, tuple) else [TOOLS / names]
        originals = {path: path.read_bytes() for path in paths}
        if any(data.decode().count(old) != 1 for data in originals.values()):
            print('SKIPPED  ' + label + ': pattern not found exactly once in ' + str(names))
            failures += 1
            continue
        test = test if '.' in test else 'SkillHostTests.' + test
        try:
            for path, data in originals.items():
                path.write_text(data.decode().replace(old, new))
            r = subprocess.run([sys.executable, '-m', 'unittest', 'test_skill_hosts.' + test],
                               cwd=TESTS, capture_output=True, text=True)
        finally:
            for path, data in originals.items():
                path.write_bytes(data)
        # A skipped test (for example without zsh) is not a kill.
        if 'skipped' in r.stderr and r.returncode == 0:
            print('SKIPPED  ' + label + ': test skipped')
            failures += 1
            continue
        # A mutant that only breaks parsing/imports proves nothing about the test.
        broken = any(error in r.stdout + r.stderr for error in ('SyntaxError', 'ImportError', 'IndentationError'))
        killed = r.returncode != 0 and not broken
        failures += not killed
        print(('KILLED   ' if killed else 'INVALID  ' if broken else 'SURVIVED ') + label + ' -> ' + test)
    print(str(len(MUTANTS) - failures) + '/' + str(len(MUTANTS)) + ' mutants killed')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())

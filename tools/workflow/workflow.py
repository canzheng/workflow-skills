"""Public deterministic workflow utilities. No lifecycle runtime."""
import argparse
import json
import pathlib
import shutil
import subprocess
import sys

# Bootstrap should not create untracked utility cache files in a fresh consumer.
sys.dont_write_bytecode = True

from core import (Conflict, Invalid, SKILLS, START, block, config, content_identity, digest, finding,
                  SOURCE_URL, REQUIRED_ASSETS, required_assets, dependency_policy, manifest, repository, safe, read_regular)
from setup import setup


def doctor(root, skill_roots=()):
    c = config(root)
    findings = []
    m = manifest(root)
    source = not m and safe(root, '.workflow/bundle.json').exists()
    if not m and not source:
        findings.append(finding('provenance.missing', '.workflow', 'Neither source bundle nor consumer manifest exists', 'Use pinned setup'))
    text = read_regular(safe(root, 'AGENTS.md')).decode('utf-8') if safe(root, 'AGENTS.md').exists() else ''
    block(text)
    if 'github-v2' not in text and 'workflow-skills v2' not in text:
        findings.append(finding('instructions.missing', 'AGENTS.md', 'v2 routing is missing', 'Restore the repository entrypoint'))
    for marker in ('<!-- Beginning of Workflow Section -->', 'bash install.sh', 'bin/run-python.sh', 'must invoke `start-task`', 'use Superpowers'):
        if marker in text:
            findings.append(finding('instructions.legacy', 'AGENTS.md', 'Active legacy routing: ' + marker, 'Cut over only the conflicting workflow rule'))
    if m:
        if not required_assets(m['files']) <= m['files'].keys():
            findings.append(finding('bundle.incomplete', '.workflow/install-manifest.json', 'Installed manifest omits required assets', 'Restore reviewed complete adoption'))
        if m:
            try:
                dependency_policy(root, m)
            except Conflict as exc:
                findings.append(finding('dependency.policy', '.gitignore', str(exc), 'Review adoption, shared dependency ignores and tracked project files'))
        for name, h in m['files'].items():
            p = safe(root, name)
            if not p.is_file() or digest(read_regular(p)) != h:
                findings.append(finding('bundle.modified', name, 'Managed bytes differ or are missing', 'Review local edits before update'))
        b = block(text)
        if not b or digest(b.encode()) != m['agents_block_hash']:
            findings.append(finding('instructions.modified', 'AGENTS.md', 'Managed block differs', 'Resolve ownership before setup'))
    discovered = {}
    roots = [root / '.agents/skills']
    try:
        home = pathlib.Path.home()
        roots.extend((home / '.agents/skills', home / '.codex/skills'))
    except (OSError, RuntimeError):
        findings.append(finding('discovery.inaccessible', 'home skills catalogs',
                                'Cannot resolve home skills locations',
                                'Inspect home configuration; repository and explicit catalogs still run', 'warning'))
    roots.extend(map(pathlib.Path, skill_roots))
    seen = set()
    for folder in roots:
        try:
            resolved = folder.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            if not folder.exists():
                continue
            if not folder.is_dir():
                raise NotADirectoryError('Discovery root is not a directory')
            # glob suppresses directory read failures on supported Python versions.
            # Enumerate the root explicitly so an unreadable catalog is reported.
            paths = (p for child in folder.iterdir() if child.is_dir()
                     for p in child.glob('SKILL.md'))
            for p in paths:
                try:
                    text = read_regular(resolved / p.relative_to(folder)).decode('utf-8')
                except UnicodeError:
                    findings.append(finding('discovery.invalid', p, 'Skill file is not valid UTF-8',
                                            'Review the invalid skill in the actual host', 'warning'))
                    continue
                except (Invalid, OSError):
                    findings.append(finding('discovery.inaccessible', p, 'Cannot read skill file',
                                            'Inspect permissions in the actual host', 'warning'))
                    continue
                import re
                match = re.search(r'^name:\s*(.+)$', text, re.M)
                name = match.group(1).strip(' \"\'') if match else p.parent.name
                discovered.setdefault(name, []).append(str(p))
        except (OSError, RuntimeError):
            findings.append(finding('discovery.inaccessible', folder, 'Cannot inspect skills location', 'Inspect in the actual host', 'warning'))
    for s in SKILLS:
        if not safe(root, '.agents/skills/' + s + '/SKILL.md').is_file():
            findings.append(finding('bundle.incomplete', s, 'Required skill missing', 'Assemble all three canonical skills'))
        if len(discovered.get(s, [])) > 1:
            findings.append(finding('discovery.duplicate', s, 'Duplicate active name: ' + ', '.join(discovered[s]), 'Choose one discovery source; do not auto-delete globals'))
    for name, paths in discovered.items():
        if name in ('start-task', 'complete-task', 'audit-workflow'):
            findings.append(finding('discovery.legacy', paths[0], 'Legacy skill discoverable; v2 guidance must take precedence', 'Resolve applicable host routing manually', 'warning'))
    tools = {'python': sys.version.split()[0]}
    def probe(command, label):
        try:
            return subprocess.run(command, capture_output=True, timeout=10, check=False)
        except subprocess.TimeoutExpired:
            reason = 'timed out'
        except OSError:
            reason = 'could not execute'
        # Never expose captured output or exception details from auth/tool probes.
        findings.append(finding('tool.probe', command[0], label + ' ' + reason,
                                'Inspect the executable/environment; other diagnostics continue', 'warning'))
        return None
    executables = {}
    for tool in ('git', 'gh', 'node', 'openspec'):
        exe = shutil.which(tool)
        executables[tool] = exe
        tools[tool] = 'unavailable'
        if exe:
            r = probe([exe, '--version'], tool + ' version probe')
            if r is not None and r.returncode == 0:
                try:
                    lines = r.stdout.decode('utf-8').splitlines()
                except UnicodeError:
                    lines = []
                if lines and lines[0].strip():
                    tools[tool] = lines[0]
                else:
                    findings.append(finding('tool.probe', exe, tool + ' version output is invalid',
                                            'Inspect executable output; other diagnostics continue', 'warning'))
    # No token or CLI authentication output is emitted.
    auth = 'unavailable'
    if executables['gh']:
        r = probe([executables['gh'], 'auth', 'status'], 'gh authentication probe')
        auth = 'authenticated' if r is not None and r.returncode == 0 else 'unavailable'
    capabilities = dict(gh_authentication=auth, github_read='unprobed', github_write='unprobed', branch_publication='unprobed', actions_administration='unprobed', merge_enforcement='unprobed', github_ci_execution='unprobed', host_skill_discovery='unprobed')
    return findings, dict(mode='installed-consumer' if m else 'source-checkout' if source else 'unknown', tools=tools, capabilities=capabilities, context=c)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('setup')
    s.add_argument('--target', required=True)
    s.add_argument('--source')
    s.add_argument('--revision')
    s.add_argument('--source-url', default=SOURCE_URL)
    s.add_argument('--dependency-storage', '--skill-storage', dest='skill_storage', choices=('ignored', 'tracked'), default='ignored',
                   help='Ignored pinned dependency by default; tracked is legacy compatibility')
    s.add_argument('--repository')
    s.add_argument('--apply', action='store_true')
    s.add_argument('--uninstall', action='store_true')
    s.add_argument('--json', action='store_true')
    g = sub.add_parser('install-skills', help='Explicit shared-skills-only global/custom-root installation')
    g.add_argument('--target', help='Defaults to ~/.agents/skills only when this command is selected')
    g.add_argument('--source')
    g.add_argument('--revision')
    g.add_argument('--source-url', default=SOURCE_URL)
    g.add_argument('--apply', action='store_true')
    g.add_argument('--uninstall', action='store_true')
    g.add_argument('--json', action='store_true')
    b = sub.add_parser('bootstrap')
    b.add_argument('--repo', required=True)
    b.add_argument('--source', help='Optional canonical pinned source checkout; otherwise missing ignored skills fetch the exact pin')
    b.add_argument('--apply', action='store_true')
    b.add_argument('--json', action='store_true')
    d = sub.add_parser('doctor')
    d.add_argument('--repo', required=True)
    d.add_argument('--skill-root', action='append', default=[])
    d.add_argument('--expect-branch')
    d.add_argument('--expect-revision')
    d.add_argument('--expect-content')
    d.add_argument('--json', action='store_true')
    # Added implementations are imported only by their public command.
    k = sub.add_parser('check')
    k.add_argument('--repo', required=True)
    k.add_argument('--pr-json')
    k.add_argument('--metadata-only', action='store_true')
    k.add_argument('--specs', action='store_true')
    k.add_argument('--run-local', action='store_true')
    k.add_argument('--run-integration', action='store_true')
    k.add_argument('--issues-json')
    k.add_argument('--json', action='store_true')
    m = sub.add_parser('migrate')
    m.add_argument('operation', choices=['inspect'])
    m.add_argument('--repo', required=True)
    m.add_argument('--json', action='store_true')
    args = p.parse_args(argv)
    extra, findings, code = {}, [], 0
    try:
        if args.command in ('setup', 'install-skills'):
            if args.command == 'install-skills':
                if args.target is None:
                    try:
                        args.target = str(pathlib.Path.home() / '.agents/skills')
                    except (OSError, RuntimeError) as exc:
                        raise Invalid('Cannot resolve default global skills target; provide --target') from exc
                from setup import install_skills
                changes, residuals = install_skills(args)
            else:
                changes, residuals = setup(args)
            extra = dict(applied=args.apply, changes=changes, residuals=residuals)
            findings = [finding('uninstall.residual', x, 'Modified asset preserved', 'Review and remove manually if desired', 'warning') for x in residuals]
            code = 1 if residuals else 0
        elif args.command == 'bootstrap':
            from bootstrap import bootstrap
            extra = dict(applied=args.apply, changes=bootstrap(args))
        elif args.command == 'doctor':
            root = repository(args.repo)
            findings, extra = doctor(root, args.skill_root)
            identity = content_identity(root)
            extra['content'] = identity
            for field, expected in [('branch', args.expect_branch), ('revision', args.expect_revision), ('content_digest', args.expect_content)]:
                if expected is not None and identity[field] != expected:
                    findings.append(finding('target.mismatch', root, field + ' does not match intended handoff', 'Select the recorded branch/content explicitly; never fall back'))
        elif args.command == 'check':
            from checks import check
            findings = check(repository(args.repo), args)
        else:
            from migration import inspect
            findings, extra = inspect(repository(args.repo))
        if any(x['severity'] == 'error' for x in findings):
            code = 1
    except (Invalid, UnicodeError) as exc:
        findings = [finding('invalid', getattr(args, 'repo', getattr(args, 'target', '')), str(exc), 'Correct invocation/configuration and retry')]
        code = 2
    except (Conflict, OSError) as exc:
        findings = [finding('conflict', getattr(args, 'repo', getattr(args, 'target', '')), str(exc), 'Resolve finding without overwriting user changes')]
        code = 1
    result = dict(schema_version=1, ok=code == 0, findings=findings, **extra)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print('OK' if code == 0 else 'FAILED')
        for f in findings:
            line = f"{f['severity']} {f['code']} {f['path']}: {f['message']} -> {f['remediation']}"
            encoding = sys.stdout.encoding or 'utf-8'
            print(line.encode(encoding, errors='backslashreplace').decode(encoding))
        for key, value in extra.items():
            print(key + ': ' + json.dumps(value))
    return code


if __name__ == '__main__':
    raise SystemExit(main())

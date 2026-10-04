# Fresh consumer Cloud bootstrap handoff

Use existing repository canzheng/workflow-skills-test, branch
`pilot/shared-skill-bootstrap`, exact tested consumer SHA
`539580779e52eef5b976a0460d7d18e16833c2b0` (PR8, Issue7).
The tracked manifest pins workflow source
`47320c363e538d2c8423e11e5ca9121c2d0303da`. Main has the older tracked-skill model;
no merge is authorized. Select this branch for preparation and the fresh task.
Do not discard user changes or silently substitute main.

## Published environment preparation

Put this idempotent script in the actual Cloud setup/preparation hook; use the same
script in the maintenance hook if the host offers one. Ensure checkout precedes it
and agent skill discovery follows it. Publish/apply the environment configuration
and use a new task outside the onboarding conversation. The host's actual ordering
is a gate to test, not a fact established by this document.

```sh
set -eu
cd /workspace/workflow-skills-test
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python >=3.10 is required"; print(sys.version.split()[0])'
git --version
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
git status --short --untracked-files=all
```

Require exit0 and ok:true for bootstrap/check/doctor; preserve and report unexpected
working-tree changes. The bootstrap adds no ignore rules during preparation: adoption
already tracked the scoped ignore block and manifest. It materializes only the three
ignored namespaces and no project-owned files. Repeat returns changes:[]; no source
SHA is duplicated in environment settings. Do not run one-time setup at every launch.
No Node/Conda/OpenSpec/global skill install is needed for this workflow-only branch.
Git HTTPS access to the exact pinned source is required for an empty clone. GitHub
API operations separately need api.github.com network/auth permission; apply the
existing network draft if those operations remain proxy-blocked. Never print tokens.

## Fresh task prompt

```text
Use the existing isolated checkout /workspace/workflow-skills-test. Do not create
another worktree. Verify pilot/shared-skill-bootstrap at
539580779e52eef5b976a0460d7d18e16833c2b0; preserve local changes and report mismatches.
Read AGENTS.md, docs/workflow/contract.md, docs/workflow/README.md and docs/design.md.
Continue F14 validation for Issue7/Ready PR8, not application implementation.

First record the initial host skill catalog/discovery evidence before any agent-side
bootstrap. Confirm whether the three repo-local shared skills are discoverable from
preparation, then read/use workflow-design-to-backlog, workflow-deliver-issue and
workflow-risk-review where relevant. Explicit file reads alone are not automatic
host discovery. Record source pin and shared hashes, prove only shared namespaces
ignored/untracked and pantry-project tracked. Run bootstrap again (expect changes:[]),
check --run-local, doctor and Git status. Capture preparation logs/host profile.

Read existing open AND closed Issue identities before a safe design-to-backlog rerun.
Preserve the existing five MVP outcomes, links/dependencies and unresolved dietary
choice; do not create duplicates, coding-task Issues or begin implementation. Read
PR8 review/Actions evidence and report actual observed results separately from local
mechanical checks. Read-only enforcement inspection is allowed. If access is denied,
continue independent validation and report the specific missing capability.

Return consumer/source SHAs, preparation and initial discovery/use evidence, commands
and results, shaping-rerun output, review/CI state, documentation impact, remaining
Cloud/Ubuntu/admin gates and exact next action. Do not merge, close completed Issues,
change protections/rulesets, publish releases, delete remote branches or modify globals.
```

Send the resulting fresh task link/report back to the rewrite task. The existing
“Set up workflow-skills-test” chat is onboarding evidence and does not satisfy this
fresh-task gate. Ubuntu runtime bootstrap has passed at the same consumer/source
pins; actual Ubuntu agent-host discovery still needs its own observed evidence.

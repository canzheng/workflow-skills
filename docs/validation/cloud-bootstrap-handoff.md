# Fresh consumer Cloud bootstrap handoff

Use existing repository canzheng/workflow-skills-test, branch
`pilot/shared-skill-bootstrap`, exact tested consumer SHA
`79efd96276e25e2c1a706a3c7972dbebf32d2a0a` (PR8, Issue7).
The tracked manifest pins workflow source
`7e71186ec8146b682f4c4cf40c8da5ecb6d3f608`. Main has the older tracked-skill model;
no merge is authorized. Select this branch for preparation and the fresh task.
Do not discard user changes or silently substitute main.

## Published environment setup command

Use this single idempotent script in Cloud setup/preparation and, if available, the
maintenance hook. It works for a new Git checkout without tools/workflow: absence
of the dependency manifest triggers a pinned source fetch and initial adoption.
An adopted repository uses its own tracked pin and bootstrap without re-running
adoption or fetching the seed version. Change both explicit path and owner/name
for another repository; never infer a different target from the current directory.

```sh
set -eu
WF2_CONSUMER_ROOT=${WF2_CONSUMER_ROOT:-/workspace/workflow-skills-test}
WF2_CONSUMER_REPOSITORY=${WF2_CONSUMER_REPOSITORY:-canzheng/workflow-skills-test}
cd "$WF2_CONSUMER_ROOT"
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python >=3.10 is required"; print(sys.version.split()[0])'
git --version
if [ ! -f .workflow/install-manifest.json ]; then
    WF2_SOURCE_SHA=7e71186ec8146b682f4c4cf40c8da5ecb6d3f608
    WF2_SOURCE_DIR=$(mktemp -d)
    trap 'rm -rf -- "$WF2_SOURCE_DIR"' EXIT
    git -C "$WF2_SOURCE_DIR" init --quiet
    git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git "$WF2_SOURCE_SHA"
    git -C "$WF2_SOURCE_DIR" checkout --detach --quiet "$WF2_SOURCE_SHA"
    python3 "$WF2_SOURCE_DIR/tools/workflow/workflow.py" setup --source "$WF2_SOURCE_DIR" --revision "$WF2_SOURCE_SHA" --target "$PWD" --repository "$WF2_CONSUMER_REPOSITORY" --json
    python3 "$WF2_SOURCE_DIR/tools/workflow/workflow.py" setup --source "$WF2_SOURCE_DIR" --revision "$WF2_SOURCE_SHA" --target "$PWD" --repository "$WF2_CONSUMER_REPOSITORY" --apply --json
fi
python3 -c 'import json, pathlib, sys; m=json.loads(pathlib.Path(".workflow/install-manifest.json").read_text(encoding="utf-8")); sys.exit(0 if m.get("schema_version")==2 else "Existing adoption needs reviewed dependency migration; do not overwrite it during environment setup")'
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
git status --short --untracked-files=all
```

First adoption creates trackable tools/workflow, AGENTS, project workflow config/pin,
GitHub workflows/templates/docs and exactly three owned ignore entries. Review and
commit these generated adoption files so Git becomes the durable workflow authority;
shared dependencies are already ignored and project-specific skills remain trackable.
The script never changes the Git index, commits, publishes or silently migrates old
tracked skills. Existing tracked shared files need explicit reviewed migration in
operations. In an already adopted consumer, no project files are rewritten and
bootstrap repeats with changes:[]; the initial seed SHA does not override its pin.
The pilot branch has already committed adoption, so it takes that repeatable path.

Publish/apply the environment configuration and use a new task outside onboarding.
Ensure checkout precedes the hook and agent discovery follows it. Hook ordering,
setup-file persistence and fresh host discovery are acceptance to test, not facts
established by running the script in an already active chat. Run maintenance after
checkout/pin changes when that host requires it. Record actual preparation logs.

Require exit0 and ok:true for setup/bootstrap/check/doctor. For a fresh repository,
uncommitted adoption files are expected until reviewed and committed; preserve/report
other changes. An adopted pilot should remain Git-clean. No Node/Conda/OpenSpec/global
skill installation is needed. Git HTTPS read access to the exact source is required
for an empty dependency checkout. GitHub API access is separate: apply the existing
api.github.com network draft if API operations remain proxy-blocked. Never print tokens.

## Fresh task prompt

```text
Use the existing isolated checkout /workspace/workflow-skills-test. Do not create
another worktree. Verify pilot/shared-skill-bootstrap at
79efd96276e25e2c1a706a3c7972dbebf32d2a0a; preserve local changes and report mismatches.
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

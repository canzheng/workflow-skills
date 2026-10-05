# Fresh consumer Cloud bootstrap handoff

Use existing repository canzheng/workflow-skills-test, branch
`pilot/shared-skill-bootstrap`, exact tested consumer SHA
`fd4bf175e7b2ea22439511fdfef872ce8bc7c743` (PR8, Issue7).
The tracked manifest pins workflow source
`b1fe9e0242753db54cc16dfc8768502eb74cb3ea`. Main has the older tracked-skill model;
no merge is authorized. Select this branch for preparation and the fresh task.
Do not discard user changes or silently substitute main.

## Published environment setup command

Paste this fetch-and-run command into the Codex Cloud environment **install script**
field (and maintenance hook when available). For local/Ubuntu setup use the same Bash
command with the actual absolute consumer checkout path. The setup entrypoint belongs
only to workflow-skills, not to the target repository. A new target needs no tools;
the source-owned entrypoint adopts once, then bootstraps/checks/diagnoses. An adopted
repo uses its own tracked dependency pin even if the fetched entrypoint has a different
revision. Always fetch an explicit full SHA; never main/latest. The source
[README](../../README.md) documents both Cloud and local setup.

```sh
set -eu
WF2_SOURCE_SHA=b1fe9e0242753db54cc16dfc8768502eb74cb3ea
WF2_CONSUMER_ROOT=/workspace/workflow-skills-test
WF2_CONSUMER_REPOSITORY=canzheng/workflow-skills-test
WF2_SOURCE_DIR=$(mktemp -d)
trap 'rm -rf -- "$WF2_SOURCE_DIR"' EXIT
git -C "$WF2_SOURCE_DIR" init --quiet
git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git "$WF2_SOURCE_SHA"
git -C "$WF2_SOURCE_DIR" checkout --detach --quiet "$WF2_SOURCE_SHA"
bash "$WF2_SOURCE_DIR/tools/workflow/environment-setup.sh" "$WF2_CONSUMER_ROOT" "$WF2_CONSUMER_REPOSITORY"
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

## Published-run diagnosis before retry

The [fresh published-run transcript](f14-published-cloud-run.md) started on older
main, with no repository-local skills exposed. Agent-side recovery passed, but
pre-agent discovery and install-hook ordering remain unverified. Before another run,
obtain the actual published install/maintenance logs and confirm which branch the
host checked out at each preparation/discovery boundary. Do not interpret the
executor registration log as install output. Do not enable shell tracing or dump
credentials to collect this evidence.

The task prompt cannot select its initial checkout retroactively. Select
`pilot/shared-skill-bootstrap` at task creation and verify the full consumer SHA
above. If the install hook runs on main and a later checkout replaces its files,
identify a supported preparation hook after the selected checkout and before initial
skill discovery. The generic installer must not force a branch or silently override
an existing tracked pin. When files exist before discovery but skills are absent
from the catalog, investigate host discovery separately from materialization.

The transcript's failed source-fetch probe changed the credential helper to `gh`;
it did not execute the normal README fetch binding. Test the exact pinned command
in the intended preparation phase before requesting a token. Actual default-binding
fetch and host ordering need their own evidence.

## Start-skill entrypoint

The consumer owns its Start skill for environment initialization. The user reports
that the pinned command was placed in its published setup-command field. The
field's execution/timing and this Start skill's current definition are not directly
observable from the rewrite task. The earlier pasted Start-skill instruction ran
check/doctor without bootstrap; that instruction cannot materialize ignored skills.

Have the consumer Start skill read the **workflow-skills README and linked setup
guidance at the resolved full source pin**, then follow that documented procedure.
The tracked manifest selects the source URL/revision for an adopted repository;
first adoption requires an explicitly approved full source SHA. Do not require a
setup script or workflow helpers already in the consumer. Keep the setup implementation
in workflow-skills, rather than creating another installer or shared workflow skill.
This is startup routing, not a v1 task wrapper. Preserve unrelated host rules,
the existing isolated checkout, project files and the index. In the pilot, verify
the full expected consumer SHA and manifest pin first. Report a mismatch before
initialization; do not silently reset, migrate old main or substitute its source pin.

Suggested **pilot-only** instruction for the consumer Start skill:

```text
Initialize workflow-skills for /workspace/workflow-skills-test. Preserve host
instructions and user changes; do not create another consumer worktree or install
global skills. At your first executed step, emit WF2_START_BEGIN and record the
initial branch/full HEAD, working-tree status, manifest pin and exposed skills.
Capture ordinary initialization command output and exit status, without credentials
or shell tracing. These markers are execution evidence, not automatic discovery proof.

This disposable F14 pilot explicitly authorizes selecting its unmerged consumer
revision before initialization. Expected HEAD:
fd4bf175e7b2ea22439511fdfef872ce8bc7c743
If HEAD differs, require a clean working tree/index, fetch origin
pilot/shared-skill-bootstrap and verify FETCH_HEAD equals that exact SHA before
switching this existing checkout to it. A detached checkout is acceptable. Do not
reset, discard changes, force checkout or select another revision. If changes or
fetch/revision mismatches block safe selection, emit WF2_START_BLOCKED with the
specific reason and preserve the checkout. If HEAD already matches, no switch is
needed; a host-created branch name such as work is acceptable.

Read the selected consumer AGENTS.md and its tracked manifest. Expected source URL:
https://github.com/canzheng/workflow-skills.git
Expected full source revision:
b1fe9e0242753db54cc16dfc8768502eb74cb3ea
Require the selected manifest to contain that source URL and full revision; report
a missing field or mismatch rather than inferring a source, upgrading or proceeding.
Fetch that exact workflow-skills source, read README.md and linked development and
operations guidance at the same revision, and follow the documented source-owned
setup procedure. Use the resolved pin when adapting examples, not a different
sample seed. Do not assume consumer tools exist, fetch main/latest, copy installer
logic into this skill, change authentication or migrate older main during startup.

Require bootstrap/check --run-local/doctor exit0 and ok:true. Repeat bootstrap and
require changes:[] with tracked bytes/index preserved. Only the three shared skill
namespaces are ignored; project-specific skills remain trackable. Emit WF2_START_END
with the actual consumer/source revisions and verification results, or emit
WF2_START_FAILED with the failed command/exit result.

Record when skills became available and whether the host discovered/refreshed them
or you explicitly read their files. Do not infer discovery from these markers or
filesystem presence. No application execution, merge, completed Issue closure,
protection/ruleset change, release, branch deletion or global configuration changes.
```

The **normal consumer Start skill is branch-agnostic**: use the task-selected
checkout and its tracked dependency pin; first adoption needs an explicitly approved
full source revision. Do not add this pilot's branch/SHA to generic setup or the
workflow-skills installer. Its safe selection belongs only to the authorized pilot
startup routing while the test implementation remains unmerged.

The user supplied the current published Start definition after the second run. It
required the pilot HEAD but said to report mismatches before proceeding and not change
branches. Both launches were on older main, so that definition could not initialize
the intended pilot from their observed state. The rewrite author supplied that
contradictory instruction and corrected it here. This establishes an instruction
conflict, not proof that automatic Start executed or a diagnosis of catalog behavior.
The subsequent startup-only diagnostic reports remaining on older main without
confirmed initialization. Inspection of that commit's schema1 manifest confirms
it has no source_url; the current pilot schema2 manifest contains the exact URL
above. The pilot instruction now states both expected URL and revision explicitly,
then verifies them after safe checkout selection. This removes a source-resolution
ambiguity; it does not establish automatic invocation or a network failure.

The consumer skill loads setup behavior from the pinned source documentation rather
than depending on a separately supplied shell block or copying installer logic.
A new consumer need not contain any workflow tools beforehand. Its project-owned
Start skill remains separate from the three ignored shared workflow dependencies.
If Start runs only after initial agent discovery, initialization/explicit use cannot
silently change S34/F14's fresh-discovery contract. Establish actual host timing.

## Fresh task prompt

```text
Use the existing isolated checkout /workspace/workflow-skills-test. Do not create
another worktree. Verify pilot/shared-skill-bootstrap at
fd4bf175e7b2ea22439511fdfef872ce8bc7c743; preserve local changes and report mismatches.
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

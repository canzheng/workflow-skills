# Ubuntu workstation acceptance handoff

The user approved Ubuntu-only first-release acceptance on 2026-10-05. Cloud setup
and discovery are deferred, not reported as passed. Shared skills in consumers are
ignored exact-pin dependencies; the source's authored skills stay tracked. Optional
explicit global installation is separate from repo-local adoption.

The user's [Ubuntu workstation bootstrap report](ubuntu-workstation-bootstrap.md)
now passes installation/check/repeatability at the pinned consumer revision on
Ubuntu26.04/Python3.13.13/codex-cli0.160.0. The subsequent
[independent session](ubuntu-workstation-session.md) supplies initial native
discovery, actual three-skill use and no-chat continuation at the recorded pins.
Review repairs and affected runtime/consumer/CI checks are the remaining work;
do not repeat the original diagnostic merely because doctor says unprobed.

## Pinned targets

Source: canzheng/workflow-skills, rewrite/workflow-skills-v2, tested implementation
`a75c3f20e5f4032568b1d1a5cb17d001fc781918`. All107 tests/no skips and strict specs pass on Ubuntu24.04.5
and managed runtime; source push37280549959/PR37280555919 pass.
Consumer: canzheng/workflow-skills-test, pilot/shared-skill-bootstrap, existing
[Issue7](https://github.com/canzheng/workflow-skills-test/issues/7) and
[Ready PR8](https://github.com/canzheng/workflow-skills-test/pull/8). Its explicit
schema-4 migration is published at `9bd23d72dc24a741d669c1ea92532f8bf337aa42`,
pinning source `a75c3f20e5f4032568b1d1a5cb17d001fc781918`. Consumer push37280700304,
PR37280704952 and metadata37280702909 all pass. Existing main
and older consumerf6394326 still use tracked schema3; do not confuse that with new
ignored-dependency acceptance. No merge is needed to test an explicit Ubuntu branch.

## Fresh Ubuntu checkout command

Run outside an existing checkout, setting an unused absolute path. This selects
and verifies the exact consumer revision before bootstrap/agent discovery:

```sh
# Isolate errexit so a failed validation does not terminate a tmux pane's shell.
set +e
(
  set -eu
  : "${WF2_CONSUMER_ROOT:?Set an unused absolute path for the consumer clone}"
  test ! -e "$WF2_CONSUMER_ROOT"
  git clone --branch pilot/shared-skill-bootstrap https://github.com/canzheng/workflow-skills-test.git "$WF2_CONSUMER_ROOT"
  cd "$WF2_CONSUMER_ROOT"
  test "$(git rev-parse HEAD)" = "9bd23d72dc24a741d669c1ea92532f8bf337aa42"
  python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
  python3 tools/workflow/workflow.py check --repo . --run-local --json
  python3 tools/workflow/workflow.py doctor --repo . --expect-revision 9bd23d72dc24a741d669c1ea92532f8bf337aa42 --json
)
printf 'Validation exit status: %s\n' "$?"
```

The exact source pin for first adoption/global install is:

```sh
WF2_SOURCE_SHA=a75c3f20e5f4032568b1d1a5cb17d001fc781918
```

Fetch it using the source README command. Global installation uses that checked-out
source's install-skills command and separate session; never use main/latest.
If the branch has advanced, stop this frozen diagnostic and reconcile the current
Issue/PR checkpoint instead of resetting user files or silently certifying new content.

## Prepare repo-local skills before starting Codex

Use a fresh clone of the recorded consumer branch/SHA, or inspect your existing
checkout first. Never reset/switch a dirty checkout or create a worktree implicitly.
From the exact consumer root, capture these outputs with command exit statuses:

```sh
cat /etc/os-release
python3 --version
git --version
codex --version
pwd
git branch --show-current
git rev-parse HEAD
cat .workflow/install-manifest.json
git --no-optional-locks status --short --untracked-files=all
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 tools/workflow/workflow.py check --repo . --run-local --json
python3 tools/workflow/workflow.py doctor --repo . --json
python3 tools/workflow/workflow.py bootstrap --repo . --apply --json
git ls-files -- .agents/skills/workflow-design-to-backlog .agents/skills/workflow-deliver-issue .agents/skills/workflow-risk-review
git check-ignore --no-index -- .agents/skills/workflow-design-to-backlog/SKILL.md .agents/skills/workflow-deliver-issue/SKILL.md .agents/skills/workflow-risk-review/SKILL.md
git --no-optional-locks status --short --untracked-files=all
```

Expect bootstrap/check/doctor exit0/ok:true; repeat bootstrap changes:[]. Shared
files must exist and match the pin/hashes, shared git-ls-files output must be empty,
and all three files must be ignored. Project skills remain trackable. Capture before/
after tracked-file hashes and raw index hash as well as Git status; clean status alone
cannot demonstrate no index writes. First missing-file materialization needs source
read access; matching repeats are offline. Optional --source permits a checked-out
canonical source. Missing/modified project files or dependency edits are conflicts,
not permission to overwrite. Installer/checker tests cover negatives; do not damage
your working checkout merely to repeat them.

For fresh adoption without tools, use the source README's pinned fetch-and-run
command with your explicit root/owner/name. Review/commit only project-owned files,
helpers/CI/templates/docs/project skills, manifest and .gitignore. Never force-add
shared dependency files. Existing tracked consumers use the explicit migration in
[operations](../operations.md); startup never untracks or migrates automatically.

Launch `codex` from that repository root after bootstrap. A catalog probe can show
recognition; it does not substitute for this fresh agent session and actual use.

## Fresh Ubuntu task prompt

```text
Validate WF2-F14 in this Ubuntu checkout. Read host/repository instructions and
preserve user changes. Do not install or repair anything during this session.

Before explicitly reading any SKILL.md, report the initial available skill catalog,
working/project root, OS and Codex version. Identify workflow-design-to-backlog,
workflow-deliver-issue and workflow-risk-review and their discovery paths. If the
host cannot expose this evidence, report unprobed instead of inferring discovery.
Resolve the exact recorded consumer/source SHAs from the handoff and manifest;
stop only affected work on mismatch. No global/local duplicate shared names.

Use workflow-deliver-issue to resume the existing authorized adoption Issue7/PR8:
read its acceptance/checkpoint, inspect current implementation/config/docs, run
applicable installed verification, reassess documentation and record evidence.
This workflow-only adoption branch has no application suite; do not claim one ran.
Use workflow-risk-review on installer/bootstrap/index/ignore boundaries and assess
its required negative evidence. Report concrete findings and any actual remediation.
Do not count a file read or catalog query alone as successful skill execution.

Exercise workflow-design-to-backlog on the existing approved Pantry Planner design
and current open/closed Issue identities if those documents/remote reads are available.
Reconcile a single MVP outcome batch read-only: preserve stable IDs/human edits,
design/dependency links, Ready vs backlog/blocked separation, and unresolved dietary
policy. Do not create duplicate Issues, invent decisions or start application work.
If this branch lacks that design, use the already pinned source's initial-backlog
evaluation design and record candidate-only fixture evidence separately from GitHub.

Record results for discovery, actual skills used/artifacts, exact revisions,
commands/exits, repeat/no-write proof, docs impact, review findings and next action.
Retain previous actual Actions/review/Ubuntu evidence at its original revisions;
material changes require affected reruns. Do not merge, close Issues as completed,
change protections/authentication, publish releases or delete remote branches.
```

## Optional global-mode verification

Use a separate session/project without repo-local shared copies to avoid duplicate
names. Explicitly install only when you intend to change your own global skills:
fetch the same tested source pin, preview `install-skills --source /pinned/source
--revision FULL_SHA --json`, then repeat with --apply. Default is ~/.agents/skills.
It never creates global AGENTS, project config/helpers or authentication. Repeat must
report changes:[] and preserve unrelated skills. Global provenance lives at
~/.agents/skills/.workflow-skills-install.json. Provide hashes/path/pin plus initial
native catalog and actual use from the selected project. Its policy/docs still belong
to that project; global installation alone is not project adoption. Repo-local check/
doctor continue to require the project's declared repo-local dependencies; global
installer verification does not claim those checks passed in a global-only project.
This optional host evidence is separate from the required repo-local Ubuntu F14 path.

## Evidence to return

Return one report (text/Markdown or terminal transcript) with:

1. Ubuntu/Codex/Python/Git versions, source/consumer repo/branch/full SHAs, install mode.
2. Bootstrap/install commands, exit statuses, first/repeat JSON, pin/hashes, ignore/
   tracking outputs and before/after tracked/index proof; redact credentials.
3. Initial fresh-session catalog/discovery paths before explicit reads, plus actual
   skill-use artifacts/decisions. Record discovery and use separately.
4. Verification, documentation reassessment, review findings/remediation and exact
   current PR/Issue/Actions links. Identify unavailable remote access honestly.
5. Remaining acceptance and exact next action. No merge/completion simulation.

Merge→valid Issue-completion observation, additional administration and release
remain pending separate authorization. Cloud evidence is no longer requested.

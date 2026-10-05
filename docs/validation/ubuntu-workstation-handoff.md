# Ubuntu workstation acceptance handoff

The user approved Ubuntu-only first-release acceptance on 2026-10-05. Cloud setup
and discovery are deferred, not reported as passed. Shared skills in consumers are
ignored exact-pin dependencies alongside the Python runtime at
.agents/tools/workflow/; the source's authored skills stay tracked. Optional
explicit global installation is separate from repo-local adoption.

The user's [Ubuntu workstation bootstrap report](ubuntu-workstation-bootstrap.md)
passed installation/check/repeatability at original consumer9bd23d72/sourcea75c3f2 on
Ubuntu26.04/Python3.13.13/codex-cli0.160.0. The subsequent
[independent session](ubuntu-workstation-session.md) supplies initial native
discovery, actual three-skill use and no-chat continuation at the recorded pins.
Review repairs and affected runtime/consumer/CI checks are the remaining work;
do not repeat the original diagnostic merely because doctor says unprobed.

## Pinned targets

Current source repair candidate: canzheng/workflow-skills,
rewrite/workflow-skills-v2, implementation `dd0abff37c839bac3cdbcf3debbf344c46f2ec73`.
Four new review repairs and expected182 tests are authored but unrun because
the old workspace cannot start processes. Validate this source in a fresh healthy
Ubuntu checkout before updating any consumer. Read the latest checkpoint below
for the exact source/consumer distinction and required next verification.

Consumer remains published at `75ed97dd1030b64e806300686c86dc1ab3101304`
on pilot/shared-skill-bootstrap and pins source
`41df6a04ab04f436f5d5519bc7cc218c8fad6d17`.
Its review6002831610 is clear at that head; it has not adopted this new candidate.
Existing Issue7 and PR8 remain open; no merge or completed closure occurred.
Initial native Ubuntu discovery/use remains valid with unchanged shared-skill bytes.

## Fresh Ubuntu checkout command

This frozen command targets the PREVIOUS consumer/runtime, which retains the
newly reviewed defects. It is historical evidence, not current-candidate acceptance
or a recommendation to adopt that old pin. First validate the new source candidate,
then perform a reviewed source-owned consumer update and refresh this command.

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
  test "$(git rev-parse HEAD)" = "75ed97dd1030b64e806300686c86dc1ab3101304"
  WF2_SOURCE_DIR=$(mktemp -d)
  trap 'python3 -c "import shutil, sys; shutil.rmtree(sys.argv[1])" "$WF2_SOURCE_DIR"' EXIT
  git -C "$WF2_SOURCE_DIR" init --quiet
  git -C "$WF2_SOURCE_DIR" fetch --no-tags --depth=1 https://github.com/canzheng/workflow-skills.git 41df6a04ab04f436f5d5519bc7cc218c8fad6d17
  git -C "$WF2_SOURCE_DIR" checkout --detach --quiet 41df6a04ab04f436f5d5519bc7cc218c8fad6d17
  bash "$WF2_SOURCE_DIR/tools/workflow/environment-setup.sh" "$PWD" canzheng/workflow-skills-test
  python3 .agents/tools/workflow/workflow.py check --repo . --run-local --json
  python3 .agents/tools/workflow/workflow.py doctor --repo . --expect-revision 75ed97dd1030b64e806300686c86dc1ab3101304 --json
)
printf 'Validation exit status: %s\n' "$?"
```

The previous frozen source pin (not the new repair candidate) is:

```sh
WF2_SOURCE_SHA=41df6a04ab04f436f5d5519bc7cc218c8fad6d17
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
# On a fresh clone first fetch its exact pin and run the source entrypoint above.
python3 .agents/tools/workflow/workflow.py bootstrap --repo . --apply --json
python3 .agents/tools/workflow/workflow.py check --repo . --run-local --json
python3 .agents/tools/workflow/workflow.py doctor --repo . --json
python3 .agents/tools/workflow/workflow.py bootstrap --repo . --apply --json
git ls-files -- .agents/skills/workflow-design-to-backlog .agents/skills/workflow-deliver-issue .agents/skills/workflow-risk-review .agents/tools/workflow
git check-ignore --no-index -- .agents/skills/workflow-design-to-backlog/SKILL.md .agents/skills/workflow-deliver-issue/SKILL.md .agents/skills/workflow-risk-review/SKILL.md .agents/tools/workflow/workflow.py
git --no-optional-locks status --short --untracked-files=all
```

Expect bootstrap/check/doctor exit0/ok:true; repeat bootstrap changes:[]. Shared
files must exist and match the pin/hashes, shared git-ls-files output must be empty,
and all shared skill/runtime files must be ignored. Project skills remain trackable. Capture before/
after tracked-file hashes and raw index hash as well as Git status; clean status alone
cannot demonstrate no index writes. First missing-file materialization needs source
read access; matching repeats are offline. Optional --source permits a checked-out
canonical source. Missing/modified project files or dependency edits are conflicts,
not permission to overwrite. Installer/checker tests cover negatives; do not damage
your working checkout merely to repeat them.

For fresh adoption without tools, use the source README's pinned fetch-and-run
command with your explicit root/owner/name. Review/commit only project-owned files,
CI/templates/docs/project skills, manifest and .gitignore. Never force-add
shared dependency files. Existing tracked consumers use the explicit migration in
[operations](../operations.md); startup never untracks or migrates automatically.

Launch `codex` from that repository root after bootstrap. A catalog probe can show
recognition; it does not substitute for this fresh agent session and actual use.

## Fresh Ubuntu task prompt

Original discovery/use is already verified. For the repaired runtime, use this
only when affected consumer checks or independent review need a fresh session;
do not demand another discovery test for byte-identical skills. Source/consumer
runtime evidence is recorded above; final PR review remains the next gate.

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

## Latest diagnostic-probe checkpoint — 2026-10-05

Source implementation `dd0abff37c839bac3cdbcf3debbf344c46f2ec73` on `rewrite/workflow-skills-v2`
implements four new P2 review repairs. These repairs and four added regression
tests have NOT executed in this workspace; they are implemented, not locally
verified or delivered. F01–F13 retain their earlier revision-bound implementation
and verification evidence; F14 remains partial and blocked on current verification
and semantic review. Active OpenSpec task4 remains unchecked; no archive occurred.

Source review at41df6a04 returned findings4188772467,4188772484,4188772494
and4188772507, completed2026-10-05T21:02:58.663672Z. The five-minute monitor
observed completion and disarmed. Code inspection confirms pathname-read races,
blocking catalog entries and unbounded required OpenSpec probes. The reviewer
reports independent reproductions; this session has NOT executed reproductions
of these four findings because process creation is exhausted.

| Acceptance concern | Implementation / actual evidence |
| --- | --- |
| Markdown replacement or FIFO | Shared no-follow/nonblocking descriptor reader binds every directory and verifies a regular final file before reading; public regression covers symlink, FIFO, ancestor replacement and replacement after open. Authored, unrun. |
| Unsupported catalog entry | Doctor warns per file and continues healthy catalogs/tools; FIFO, symlink and directory regression has an outer deadline. Authored, unrun. |
| Legacy ledger / feature substitution | Migration reads both through the bound reader; symlink/FIFO substitutions, private canaries, index preservation and a normal record control are authored, unrun. |
| Required OpenSpec timeout | Version10s and validation120s bounds return required specs.timeout failures without partial captured output; both real sleeping-executable regressions authored, unrun. |
| Adjacent read consistency | JSON, integrity, policy and bootstrap content reads share the same regular-file primitive. Platforms lacking required descriptor primitives fail closed. No filesystem lock or atomic whole-repository snapshot is claimed. |
| Source suite | Expected182 tests (previous178 plus4 new methods), unrun at new implementation. |
| Previous static-symlink / home repairs | At41df6a04:17 failing-before controls/no harness errors;2 focused pass2.023s;30 checker tests pass35.778s. These do not verify the new bound reader. |
| Previous full source / installed consumer | Full178 failed86 assertions/13 errors150.543s with fork EAGAIN; installed55 failed55 fixture creations0.054s. Never passed. |
| Current consumer | Published75ed97dd1030b64e806300686c86dc1ab3101304, pin41df6a04ab04f436f5d5519bc7cc218c8fad6d17; not yet repinned to this repair. |
| Consumer review | Clear6002831610 completed2026-10-05T21:00:31.346623Z at75ed97dd. Does not review new source bytes. |
| Current-head GitHub / Ubuntu checks | New source publication triggers checks; results must be read separately. Healthy Ubuntu182/full and actual-installed affected tests, fresh/literal exact-pin and strict specs remain unperformed. |

At consumer75ed97dd, direct source-owned preview/apply and installed check/doctor/
offline repeat returned exit0/ok:true (repeat changes:[]), preserving all five skill
files, configuration and raw index
`7f482f98d4f35d867565c3813b0a15b9610c6deba14e30a7b73d12e07fe8c063`
before caller staging manifest/operations only. This is prior-runtime evidence,
not verification of the new candidate. Consumer tree98f25c18e047b6a1d4e718373696bcff4670d349
matches the independently reconstructed native commit75ed97dd.

The workspace has32344 unreaped zombies, including32127 Git processes; even new
exec and thread starts fail/hang. No PID1, host daemon, system-limit, authentication
or global configuration change was made. Source local HEAD last confirmed
c1361214b6ec4608fc7ba1db1a348b34ea9be8f8 remains a separate unpublished evidence
commit based on41df6a04; an EOF cleanup attempt has unconfirmed local state.
New repairs/docs are published through native GitHub Git objects with a guarded
non-force ref update. Local source has NOT been synchronized or reset; do not
claim it contains the new published code or is clean.

Native Ubuntu startup catalog and actual three-skill use at9bd23d72/a75c3f2 remain
verified with unchanged shared-skill hashes. Cloud is deferred; real global-host
use and historical Ubuntu26 invalid-JSON root cause remain unverified. Existing
source/consumer enforcement readbacks and actual consumer negative enforcement
proof remain revision-bound evidence. New trusted-base metadata deployment and
source PR-contract administration remain separate gates.

Next action for a fresh healthy Ubuntu task: fetch the published rewrite head;
read AGENTS, approved v2 documents and the latest Issue15/PR16 checkpoint; run the
four focused fault regressions, full182 with pinned OpenSpec1.14.0/no optional
skips and public strict-spec checks. Repair any failures before adoption. Then
use the actual source-owned setup at the exact verified implementation pin to
preview/update consumer75ed97dd, preserve project configuration/skill/index bytes,
commit only owned changes and repeat installed/fresh/literal checks (expected59
affected installed tests if the retained runner is used). Publish updated PR8,
observe actual push/PR/body-event Actions and obtain repaired-head semantic reviews.
Do not substitute source tests for actual installed bytes. Archive only after
required premerge acceptance; merge, valid completed closure, administrative
mutations, release and remote deletion still need separate authorization.

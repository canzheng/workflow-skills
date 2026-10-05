# v2 rewrite acceptance evidence

## Current user-approved Ubuntu and distribution scope — 2026-10-05

F14 now requires Ubuntu workstation discovery/use and portability; Cloud is
explicitly deferred, not passed. Consumer shared skills are ignored exact-pin
schema-4 dependencies, bootstrapped before Codex and CI; project files/provenance/
.gitignore/project skills stay tracked. Optional explicit global shared-only
install-skills is supported; no actual global installation is performed here.
Source canonical skills remain tracked. Existing schema-3 regressions are retained
as compatibility proof; new ignored/bootstrap/global paths have their own tests.

Current verified implementation: source `a75c3f20e5f4032568b1d1a5cb17d001fc781918`; all107 tests/no
skips and strict current/delta specs pass on managed runtime and Ubuntu24.04.5.
Actual source push37280549959/PR37280555919 pass. Initial Ubuntu run at186bcbd
found one fixture relying on a global Git identity; the fixture now configures its
clone locally, with no skipped/relaxed assertion. New filesystem review4181357146
was independently reproduced on old installed f639 code, fixed with surrogate
path round trips and exercised against the same unchanged files/index before
acceptance; public regression covers both tracked/ignored modes and symlink targets.
Thread replied/resolved after proof.

Actual consumer `9bd23d72dc24a741d669c1ea92532f8bf337aa42`, pilot/shared-skill-bootstrap,
pins `a75c3f20e5f4032568b1d1a5cb17d001fc781918`; existing Issue7/ReadyPR8 remain open. Source-owned
apply preserved raw index/config/pantry-project/unrelated ignores; caller explicitly
untracked4 shared files, staged/committed project assets and provenance. App publication
is guarded/non-force with reviewed treec03bfddff952dcfb36f8a3dcce6b087b56fa134a matching
local e2eb080af691a251e42ea6193c2dc8c9e0fa8088; parentf639 preserved, own original commit
retained in reflog. No main/global/auth/admin changes. Actual consumer push37280700304,
PR37280704952 and metadata37280702909 pass.

Fresh actual remote clones on managed runtime and Ubuntu initially lack shared
files; installed bootstrap fetches the full source pin and materializes4 files.
All20 hashes match, shared paths are ignored/untracked, pantry-project tracked,
check/doctor pass and repeat bootstrap is an offline no-op with tracked/index bytes
unchanged. Native codex-cli0.159.0-alpha.3 on both runtimes recognizes all3 repo skills
after bootstrap at the Git root with no parser errors; parent-root controls list none.
No model/session started by the catalog probe: required fresh Ubuntu agent use is
still pending. Global installer/rollback/no-op/conflict tests pass on Ubuntu at
isolated targets; the actual user's global home is untouched and global native-host
use remains optional/unperformed.

Required Ubuntu initial fresh-session catalog plus actual skill use and final
independent semantic review remain pending. Source latest reviewretry5989444116
failed unknown-error5989460204; a review failure is not approval. Real merge→Issue
completion remains pending separate authorization. Consumer enforcement previously
configured AND observed (24484016; actual fail37269275157→blocked, restore37269365402
→clean); source required-check configuration is still absent/separate. Cloud is
deferred/unverified, not an active blocker. OpenSpec remains active until required
acceptance completes; no archive/merged/delivered/released claim.
[Workstation procedure and evidence request](ubuntu-workstation-handoff.md) replaces
Cloud environment investigation. No merge/closure/admin/release/global mutation.

The following dated records preserve earlier exact revisions and acceptance scopes;
references to mandatory Cloud/committed consumer skills are superseded by this
approved scope update, not retroactively counted as passes.

## Native CLI discovery subset verified — 2026-10-05

Existing Codex CLI0.159.0-alpha.3 app-server initialize/skills-list query recognizes
all3 workflow skills plus pantry-project with repo scope/enabled/no repo errors at
consumerf6394326 Git root on managed runtime and Ubuntu24.04.5. Parent-root controls
return no repo workflow skills. A real fresh old-main5d055649 clone recognizes its
identical3 skills at the repo root; parent control returns none. Tracked/index/global
config bytes unchanged; no workflow globals or agent/model/thread execution.
[Actual root/catalog comparison](f14-published-cloud-run.md#native-codex-catalog-root-comparison--2026-10-05)
validates native CLI package discovery and a root negative, not published Cloud
initial discovery or proof of its deployed implementation. Ubuntu CLI catalog subset
is verified; Ubuntu agent invocation/end-to-end use and Cloud initial catalog/use
remain pending. Host root binding is a supported lead, not a proven Cloud cause.


## Recreated Cloud comparison and current consumer repair — 2026-10-05

Final enlarged-suite checkpoint: source `b0323c903901bc33fb16a144aec413f3b31ff087`
passes all89 tests/no skips and strict current/delta specs on managed runtime and
Ubuntu24.04.5. Executable bundle remains a4eb9f1; consumerf6394326 pins that exact
code/documentation revision. Source push37273309768 passed; PR37273314869 was still
running when recorded. Consumer's actual three runs passed as listed below.
Both staged-content review threads are replied/resolved on independently reproduced
and remediated evidence. Current final review remains pending; previous source
request5989224524 failed with unknown-error response5989241655, not a semantic pass.

The user's second fresh-environment report (16,163 bytes, SHA256
`d58e8524af55f6c08daf7e1dbedb857918b4a9eaba398de7e0be001a46a94d40`) again records
old main5d055649/source139e66d5, initial host/workspace cwd/workspace,55 plugin skills
without workflow entries, empty executor catalog, and unavailable separate project
root/full repo catalog. All4 tracked shared files match hashes and are unignored;
integrity passes, expected-pilot revision fails,25 files/raw index unchanged. The
environment identity changed but the result did not. This is supplied evidence, not
live chat inspection. [Detailed comparison](f14-published-cloud-run.md#recreated-environment-reproduced-catalog-absence--2026-10-05)
keeps discovery blocked/unverified; no further environment recreation or installer
redesign is recommended without new host information. Support/debugging should
establish current-flow repo/root binding, discovery catalog and checkout ordering.

After the diagnostic completed, consumer Issue7/ReadyPR8 was updated explicitly:
`pilot/shared-skill-bootstrap`, `f6394326cd410b82567b8fea76bfd5c44fa9261a`, source
`a4eb9f1303d80cc18f83b5bbd734063cac03b9c3`. Setup changed4 owned files and preserved
project config/AGENTS/ignores/pantry-project/raw index; caller updated README then
staged/committed. Local2a3f2c3501a710a4ed34ea8acc317fed8e9bf621 and app serverf6394326
have identical tree4e5d8ecbbddbd182080972fc2a9d30197726312d and parent0e3fbc53.
Guarded non-force publication/local metadata alignment preserves user content and
original local commit in reflog; no reset of the rewrite baseline or auth change.

Consumer finding4181129303 was validated before acceptance with old installed CLIs:
a real owned exact-source doc update with only new provenance staged returned
ok:true for check/doctor/bootstrap; repaired CLI rejects the same unchanged file/index
snapshot, and complete staging passes. Two new public regression cases cover that
partial-staging path and intent-to-add entries. Runtime fix already exists at
a4eb9f1; its87-test source/Ubuntu proof remains accurate; enlarged current test suite
verification is recorded after it runs, without pretending the old commit has89 tests.

Fresh actual f6394326 clones on managed runtime and Ubuntu24.04.5 have all4 shared
files and pantry-project tracked before hooks, match all20 hashes, repeat
check/doctor/read-only bootstrap twice without tracked/index writes. Missing skills,
five provenance/policy/runtime/CI untracking and corrupt-staged paths, and partial
provenance/doc staging fail without repair/validator mutation; owned clones restored
explicitly. Actual consumer
push[37272954548](https://github.com/canzheng/workflow-skills-test/actions/runs/37272954548),
PR[37272958814](https://github.com/canzheng/workflow-skills-test/actions/runs/37272958814)
and metadata[37272957270](https://github.com/canzheng/workflow-skills-test/actions/runs/37272957270)
pass. This proves current consumer integration of the review repair, not initial
host discovery. Current semantic review remains pending.

F01–F13 implemented/locally verified; F14 partial/in-progress/blocked and rewrite
change active/unarchived. Public consumer required-check gate remains configured/
observed. Initial Cloud and Ubuntu agent-host discovery/use and final semantic
review remain pending; actual merge→valid Issue completion and further administration/
release require separate authorization. No merged/delivered claim.


## Staged-candidate review repair — 2026-10-05

Source Ready-PR finding4181125358 was reproduced before acceptance: original code
passed broken staged blobs/modes behind intact working files, producing28 focused
negative-test failures. Source `a4eb9f1303d80cc18f83b5bbd734063cac03b9c3` adds read-only
canonical index validation of staged provenance/config schemas, configured document
paths, all managed asset hashes and AGENTS block. Regular files/stage0 are required.
Valid project-owned policy differences and a coherent schema-1 snapshot during an
explicit update remain supported. Four new tests cover23 corrupt paths, symlink and
merge modes, invalid policy/schema/document references and valid policy edits;
tracked working files and raw index stay unchanged on rejection.

All87 tests/no skips and strict current/delta specs pass at that exact source on
managed runtime and Ubuntu24.04.5. Actual source
push[37271835612](https://github.com/canzheng/workflow-skills/actions/runs/37271835612)
and PR[37271841711](https://github.com/canzheng/workflow-skills/actions/runs/37271841711)
pass. Review thread was replied to and resolved on this evidence; final independent
review of the repair remains pending.

Owned fresh clones of actual consumer0e3fbc53 explicitly updated to that source pass
installed check/doctor/bootstrap and five corrupt-staged-path negatives on both
runtimes, preserving project config/skill bytes and raw index during setup/verification.
Those local fixture commits (managed61a8237de8a2534f00597a55abb96294a17d30e9,
Ubuntu9a1e5062628e93360d9f332f4d41f6503ad0ba2b) were not pushed and do not establish
consumer Actions or initial host discovery for the new pin. Live consumer remains
`0e3fbc530f21c4981230a5ef968eac2a5dda3d5e`/sourceaceba714 while the user's fresh
environment diagnostic runs. Repin, consumer CI and final semantic review of this
repair are integration pending; do not silently change the diagnostic's revision.

Docs/specs updated: contract, architecture, operations/consumer operations, approved
F03 tracking clarification, current/delta adoption scenario and test corpus. Cloud
handoff now reflects the reported repository-only UI and official current flow, with
no assumed branch selector. F14 discovery and separately authorized merge/completion
remain pending; no release/archive/administration/global change.


## Latest submitted Cloud diagnostic — routing unresolved, 2026-10-05

The user's [submitted tracked-skill report](f14-published-cloud-run.md#latest-submitted-tracked-skill-diagnostic--2026-10-05)
again observes old consumer main5d055649/source139e66d5, not requested0e3fbc53/aceba714.
Old-checkout integrity passes, expected-revision check fails, tracked files/index
remain unchanged. Configured initial cwd `/workspace`, no matching consumer project
exposed and plugin/executor catalog observations leave complete repository discovery
unavailable. All4 shared files already exist in main, matching pilot shared blobs;
default-branch absence is not supported as an explanation. Resolve host task/project
routing and pre-agent checkout selection; do not repeat installation or merge as an
assumed fix. F14.1 current-revision discovery/use remains unverified. This does not
invalidate separately recorded runtime/CI/enforcement evidence below.

## Public consumer enforcement and tracking review checkpoint — 2026-10-05

The user changed canzheng/workflow-skills-test to public. Read-only GitHub confirmation:
visibility public; Protect-main24484016 is Active on refs/heads/main, requiring
v2 verification and v2 PR contract from GitHub Actions integration15368. No bypass
actors; current_user_can_bypass never; strict:false. The rule has no PR-only,
conversation-resolution, deletion or force-push requirements. This task did not change
repository visibility or administration. The earlier private-plan blocker is resolved.

Required-check enforcement is **configured and observed**: Ready PR8 at
6b9eb5d9fb8d2787544f962483e20e63c52f7231 was initially clean; temporarily omitting its
Documentation section caused metadata run[37269275157](https://github.com/canzheng/workflow-skills-test/actions/runs/37269275157)
/job111632600944 to fail with Missing or empty Documentation section/exit1. The latest
v2 PR contract check was failure and GitHub mergeable_state was blocked. Exact body
restoration triggered[37269365402](https://github.com/canzheng/workflow-skills-test/actions/runs/37269365402),
which passed; mergeable_state returned clean. HEAD/main were unchanged, no merge or
completed Issue closure occurred. This was a real check failure/block/restoration,
not simulated merge or YAML inspection. It proves the configured gate, not absent rules.

Independent source review4180988644 and consumer4180982685 were validated before
acceptance. Original implementation passed19 non-skill/policy index-removal cases;
tracking/ignore/partial-stage regressions had26 before-fix failures, and an additional
initial ignored-manifest regression failed on an owned original-source copy. Repair
requires every manifest asset, provenance/config/AGENTS indexed after any managed
asset is indexed/committed, using HEAD even if provenance leaves the index. Initial
unstaged review only allows trackable complete adoption. All required ignore paths
and ancestor rules are checked before writes; no manifest-only/shared-only bypass.
Four new public regressions cover all23 files, ignored/nested provenance/policy/
runtime/docs/CI, initial ignored manifest and partial staging, preserving files/index.
Both reviewer threads were replied to and resolved after actual remediation evidence.

Tested executable/source pin `aceba7143652ba127dbc62c98608e1b9943be31d`, rewrite/workflow-skills-v2: all83 tests/no
skips and strict current/delta OpenSpec checks pass on managed Cloud runtime and
fresh Ubuntu24.04.5 (Python3.12.14/3.12.3, Git2.52/2.43, Node24.19.0). Actual source
push[37269711408](https://github.com/canzheng/workflow-skills/actions/runs/37269711408)
and PR[37269717386](https://github.com/canzheng/workflow-skills/actions/runs/37269717386) pass.

Current consumer `pilot/shared-skill-bootstrap`, `0e3fbc530f21c4981230a5ef968eac2a5dda3d5e`, Issue7/ReadyPR8,
pins that source. Explicit update preserved project config, pantry-project and raw
index before caller commit. Localf19368f9ee69d993dd46608fb62acf6ea004048f and app-published
0e3fbc530f21c4981230a5ef968eac2a5dda3d5e have identical tree9388953945dcdb1ffaa904b120fc6e864ac3c17a; guarded non-force
publication and local alignment preserved user content and original commit in reflog.
Actual fresh Cloud-runtime/Ubuntu clones contain all4 committed shared files and
match20 hashes before any hook. Check/doctor/read-only bootstrap pass twice with
tracked/raw-index bytes unchanged; missing skills and provenance/config/AGENTS/
runtime/CI untracking fail without repair or mutation. Project skill remains tracked.
Actual current push[37269841401](https://github.com/canzheng/workflow-skills-test/actions/runs/37269841401),
PR[37269845466](https://github.com/canzheng/workflow-skills-test/actions/runs/37269845466)
and metadata[37269843410](https://github.com/canzheng/workflow-skills-test/actions/runs/37269843410) pass.
New current-head semantic review outcome is still pending; resolved findings alone
are not a final review pass. Earlier results retain their original revisions below.

F03/S34 tracking obligations and F14.6 consumer required-check enforcement have actual
positive/negative evidence above. F14.1 fresh Cloud catalog/discovery/use and Ubuntu
agent-host discovery remain unperformed; runtime clones cannot certify them. Source
repository currently emits only verification and lacks required-check/PR rules; its
metadata adoption/enforcement is separate from the tested consumer gate.
F01–F13 remain implemented/locally verified; F14 partial/in-progress/blocked. Rewrite
OpenSpec stays active/unarchived. Pending authorization remains real merge to intended
main followed by valid Issue-completion observation, additional administration and
release publication. No merge, completed closure, release/global change or delivered claim.

Current docs/specs reassessed: contract, operations/consumer operations, architecture,
approved F03 clarification, adoption spec/current delta, scenario corpus, checks
runbook, this evidence, OpenSpec tasks and [fresh Cloud handoff](cloud-bootstrap-handoff.md).
Exact next task: select consumer `0e3fbc530f21c4981230a5ef968eac2a5dda3d5e` before discovery, then use the updated
[read-only mini diagnostic](cloud-bootstrap-handoff.md#mini-diagnostic-task-prompt),
source pin `aceba7143652ba127dbc62c98608e1b9943be31d`. No install/recovery/switch in that diagnostic.

## Previous tracked-model checkpoint — superseded revisions and enforcement state


## Tracked-skill refinement — 2026-10-05

The user authorized committing shared skills instead of injecting ignored dependencies.
Source branch `rewrite/workflow-skills-v2`, starting revision
`ead664a722b040e144c44c431bfe4488c36d7c88`; tested executable pin `5615fc3f488edc41079dd60085440f0f265146f9`.
Consumer canzheng/workflow-skills-test, `pilot/shared-skill-bootstrap`,
`6b9eb5d9fb8d2787544f962483e20e63c52f7231`, [Issue7](https://github.com/canzheng/workflow-skills-test/issues/7)
and [Ready PR8](https://github.com/canzheng/workflow-skills-test/pull/8).
Schema3 tracks all three shared skill directories and risk references, project skills,
policy/configuration, helpers, CI/templates and docs. No global installation.

### Verified/completed under current authorization

All79 source tests/no skips and strict current/delta OpenSpec validation pass on managed
Cloud runtime (Debian13/Python3.12.14/Git2.52/Node24.19.0) and fresh Ubuntu24.04.5
(Python3.12.3/Git2.43/Node24.19.0), using an owned source copy. Source push
[37267258851](https://github.com/canzheng/workflow-skills/actions/runs/37267258851)
and PR[37267263959](https://github.com/canzheng/workflow-skills/actions/runs/37267263959)
pass at the executable pin. Old ignored-materialization/receipt expectations were
replaced under the approved storage change with tracked-clone, no-repair, migration,
effective-exclude and index-preservation obligations. Original code/history is retained.

Actual consumer migration started atfd4bf175e7b2ea22439511fdfef872ce8bc7c743.
Setup preserved project config, pantry-project, unrelated ignore rules and the index,
removed only its verified owned block and matched all20 bundle hashes. Before caller
staging, check/doctor correctly failed because shared files were untracked. After the
reviewed commit they pass. Shell consumer push authentication failed; the connected
app published an identical reviewed tree through a guarded non-force ref update.
Local6738e86810a6366c97da146e48b461ddfb3594a2 and server83424a5469137f9c79f4fb1a869717094d83caa5
have treebcfb75e9507803a57661f9f7bf755bbc3ef6d14a; final README correction locald102495daac708c61f354e445e4e3d9dafe032d6
and server6b9eb5d9fb8d2787544f962483e20e63c52f7231 have tree67e2eb7e597576af387be0f16d17ffb7eb2726c6.
Only metadata differs, and original local commits remain in the reflog. No user
content or baseline was reset; authentication/global configuration was unchanged.

Actual fresh consumer clones on Cloud runtime and Ubuntu at the final consumer SHA
contain all four shared files in HEAD before any hook. All20 committed/working hashes
match provenance. `check --run-local`, `doctor --expect-revision` and compatibility
`bootstrap --apply` pass twice, with tracked bytes/raw index unchanged and Git clean.
Effective ignore checks exclude neither shared files nor pantry-project. Deleting a
committed skill makes check/doctor/bootstrap fail without recreating it or changing
the index; explicit restoration returns clean. These are runtime tests, not agent-host
catalog proof. Initial adoption/update remains source-owned; repeat verification
requires neither workflow-source fetch nor environment-injected dependencies.

The implementation moved existing PR8 to draft/Issue7 in-progress, then Ready/wf:review
after self-verification and docs assessment. Actual initial tracked-model push
[37267365154](https://github.com/canzheng/workflow-skills-test/actions/runs/37267365154),
draft PR[37267369536](https://github.com/canzheng/workflow-skills-test/actions/runs/37267369536),
Ready PR[37267523005](https://github.com/canzheng/workflow-skills-test/actions/runs/37267523005)
and trusted-base metadata[37267523398](https://github.com/canzheng/workflow-skills-test/actions/runs/37267523398)
pass at83424a5. Final README-only head CI/review results are recorded after observation,
not attributed from the earlier head. Current Ready-boundary semantic reviews requested
in source5988616827 and consumer5988616946; outcomes not yet observed at this checkpoint.

One outstanding old source review P2 (4180443415) was independently reproduced:
redirecting the old receipt's `latest` through a symlink overwrites its target.
The current tracked-model handoff removes the entire receipt/Install writer, resolving
that operation; the reviewer thread was replied to and resolved. It does not claim
that the former command was safe. No current unresolved threads were observed.

Read-only consumer main summary reports `protected:false`, SHA5d05564919c55f1d4d0c2e1e020ad914252a2979.
Authoritative branch protection returns403 `Resource not accessible by integration`;
rulesets returns403 `Upgrade to GitHub Pro or make this repository public`.
Actual required-check enforcement remains unverified. Source read-only ruleset details
now expose Active Protect-main (24457981) on refs/heads/main, deletion/non-fast-forward
only, with no bypass actors or PR/status-check requirement. Consumer final6b9eb5d emits
both v2 verification and v2 PR contract; source final3a3b6d3 emits only verification.
Do not require the missing source metadata context before trusted-base adoption and
an observed follow-up PR. Source final3a3b6d3 passed79/no-skip tests/strict specs on both
runtimes plus push37267764301/PR37267770064. Consumer final6b9eb5d passed fresh clones
on both runtimes and push37267653526/PR37267656824/metadata37267655273. Current final
semantic requests5988657482/5988657642 are acknowledged with bot eyes reactions,
not a review pass. No administration was changed.

| Current acceptance | Actual evidence / boundary |
| --- | --- |
| F03.8–10; S34 tracked installation, migration, repeatability | Public CLI suite; real fd4→schema3 migration; final consumer clones on both runtimes; all20 hashes and four committed shared files; no repair/index changes |
| F14.1 fresh Cloud discovery | Pending: initial catalog in a genuinely fresh task at the final consumer SHA; file presence/manual reading does not pass |
| F14.2 continuation | Exact source/consumer branches/pins, existing Issue/PR and [read-only fresh-task prompt](cloud-bootstrap-handoff.md#mini-diagnostic-task-prompt) recorded |
| F14.3 Ubuntu | Source79 tests/strict specs and actual consumer clone/runtime verification pass; Ubuntu agent-host discovery remains unprobed |
| F14.4 live GitHub/CI/review | Real app-published branch, draft→Ready/phase transition, push/PR/metadata pass; current semantic review awaiting result |
| F14.5–7 scenarios/enforcement/ergonomics | Prior application/design/bug/risk/metadata-negative proofs retain original revisions below; protection403/tier limitation; no mandatory wrappers/plans/subagents |
| F14.8–9 reporting/archive | F01–F13 implemented/locally verified and ready for review; F14 partial/in-progress/blocked; change active/unarchived; no merged/delivered/released claim |

Documentation assessed and updated: source README, architecture/development/operations,
contract/handoff, consumer templates and pilot README/AGENTS/docs, candidate release notes,
approved design/capability map/F03 contract, current adoption spec and active delta,
OpenSpec tasks, this evidence, published-run history and fresh Cloud handoff. Root Git
ignores no longer contain the managed dependency block in the consumer. Project skill,
config and design were preserved. Historical injected-skill reports remain below.

### Pending environment/review gates and authorization

Still unperformed: initial automatic Cloud discovery at the committed consumer revision,
actual use after that initial capture, Ubuntu agent-host discovery, current final
semantic review acceptance and authoritative required-check enforcement observation.
A runtime clone or YAML inspection cannot satisfy these. The task-selection boundary
must supply this consumer revision before initial skill discovery; do not recover or
switch branches in the diagnostic and count it as startup proof.

Pending authorization: real merge→valid Issue-completion observation, any protections/
ruleset configuration, and release publication. No simulated merge/closure substitutes.
F14 and OpenSpec stay active until required acceptance is satisfied.

Exact next action for a fresh Codex Cloud task: select canzheng/workflow-skills-test at
`pilot/shared-skill-bootstrap`, `6b9eb5d9fb8d2787544f962483e20e63c52f7231`, publish/apply the read-only environment
verification command in [handoff](cloud-bootstrap-handoff.md#published-environment-setup-command),
then use its [mini diagnostic](cloud-bootstrap-handoff.md#mini-diagnostic-task-prompt).
Capture initial host catalogs/cwd routing before explicit SKILL.md reads; verify
committed files/hashes/source pin5615fc3f488edc41079dd60085440f0f265146f9 without installing/repairing. If the host
cannot select that unmerged revision before discovery, report the limitation. No
merge/default-branch mutation is authorized as a workaround.

## Historical checkpoints — superseded storage model

The following records describe earlier revisions and retain their original evidence.
Ignored-skill materialization/receipt procedures are not current setup instructions.


## Current source-owned setup checkpoint

Latest source repair `b1fe9e0242753db54cc16dfc8768502eb74cb3ea` passes 81 tests
without skips and strict specs on Cloud and fresh Ubuntu24.04.5; source push/PR
Actions37251965903/37251969459 pass. The c504 source review's Git replacement-ref
finding was reproduced before repair; canonical-object reads and a separate-clone
rematerialization regression now preserve the full-SHA identity. Current code-head Codex review5986640964 reports no major issues. Consumer
`pilot/shared-skill-bootstrap` now advances to `fd4bf175e7b2ea22439511fdfef872ce8bc7c743`,
pinning that repaired source. Its local check/doctor/no-op and fresh Ubuntu actual
README fetch/run twice pass with tracked bytes/index and hashes preserved; push
37252506795/PR37252510994/metadata37252507928 pass. Consumer current-head review5986706572 reports no major issues. Earlier uploaded f31/ef24 reports retain their original
revision identities. The outer entrypoint example uses the repaired source;
an adopted consumer still obeys its own tracked pin.

The second fresh task supplied report/snapshots/actual Actions logs. Those logs
confirm exact-head/test-merge execution, bootstrap ordering, metadata negative and
restoration, and resolved semantic review at both consumer/application heads. The
report also records successful normal source fetch/entrypoint execution during
recovery. Automatic Start definition/execution was unavailable to that task; empty
catalogs persisted after recovery. The user subsequently supplied the Start text:
it required the unmerged pilot revision but forbade selecting it from the observed
older main. The author corrected that pilot-only routing in the handoff, with
explicit safe selection and execution markers. This is not proof of automatic Start
or discovery; generic consumer startup remains branch-agnostic. Main's limited
branch summary reports protection disabled, while authoritative admin reads remain
denied and actual required-check enforcement unverified. See the published-run
record for attachment identities and precise evidence boundaries.

The source-owned `tools/workflow/environment-setup.sh` is excluded from the consumer
bundle. The source README documents the pinned fetch-and-run command for the Cloud
**install script** field and local/Ubuntu Bash. Consumer policy/configuration,
helpers, CI/templates and the dependency pin are tracked; only the three shared
skill namespaces are ignored. First adoption creates project-owned files; repeat
materialization preserves project bytes and the index and obeys the tracked pin.
The outer command fetches its exact entrypoint; matching skills need no bootstrap fetch.

Tested executable source `ef24d36f47dbbcdbb204375b53db055122c28269` passes 80 tests
without skips and strict OpenSpec validation on Debian Cloud and fresh Ubuntu 24.04.5
(Python 3.12.14/3.12.3, Git 2.52/2.43). Source push/PR Actions
37220660666/37220665034 succeeded. Actual source-suite history prerequisites were
executed on Ubuntu: a shallow clone fetched full history before baseline assertions.
A meaningful annotated-tag negative failed before repair; setup now requires a
canonical commit-object SHA, rejecting tag-object pins before writes. Completeness
covers all 20 assets, and source/installed versions and adopted config are validated
before dependency writes. Previous review fixes remain covered by the 80-test suite.

Consumer `pilot/shared-skill-bootstrap` at
`f31debf9810c8b989c924bc534add4848fffd6f3` pins that executable source. Actual fresh
Cloud-runtime/Ubuntu clones ran the README fetch-and-run command twice, verified
all four shared hashes, preserved project files/index and the tracked project skill,
and remained Git-clean. Actual fresh unborn Git roots adopted and repeated with
identical bytes/index; doctor reported null revision before the first reviewed
commit and the exact clean SHA afterward. These are runtime proofs, not host discovery.

Consumer push/PR/metadata Actions37221025297/37221028092/37221026987 succeeded;
metadata37222140846 also passed after the validation task corrected PR #8's body.
Current-head Codex review5982650245 reports no major issues; all six consumer review
threads are resolved. Issue7 and ReadyPR8 remain open. Application Issue1/ReadyPR6
remains at `f95f0cae3b87bc8031b00a4150cf9670251ae978`: 11 tests on Cloud/Ubuntu and
Python3.14, actual Actions and final review passed in earlier recorded executions.
The new validation task inspected, rather than reran, those application/source suites.

The user supplied the transcript of a genuinely fresh published Cloud task. It
started on branch `work` at older main `5d05564919c55f1d4d0c2e1e020ad914252a2979`,
with no repo-local skills in its initial catalogs. After agent-side branch recovery,
bootstrap/check/doctor, actual manual skill use, safe all-state backlog reconciliation
and targeted negative probes passed. This does not satisfy pre-agent discovery.
Available logs do not establish install-hook execution/order. See
[the validated published-run evidence](f14-published-cloud-run.md) for observations,
independently rechecked GitHub state and the credential-override probe limitation.

The selected retry uses **Install script, publish/apply, fresh mini diagnostic**;
Start is optional and unnecessary for this service-free pilot. The exact handoff
Install command was executed in fresh Ubuntu24.04.5 (Python3.12.3, Git2.43.0): it
selected the approved consumer revision, fetched the exact pinned source, verified
all20 asset hashes, and repeated with tracked bytes/index unchanged. Dirty-checkout
and ignored project-skill collision negatives refused selection while preserving
user bytes, HEAD and index. This establishes mechanical command behavior, not
Cloud Install execution, publication persistence or host discovery.

The latest supplied Install-only mini diagnostic still reports old main5d055649
and pin139e66d5, no workflow skills in initial metadata, unavailable Install logs,
a passing old-bundle check and expected-revision failure. Independent Git reads
confirm its skill sizes match old tracked files. No recovery ran; preservation
passed as reported. See [the diagnostic evidence](f14-published-cloud-run.md#latest-install-only-diagnostic-intended-preparation-not-demonstrated).
A separate Ready PR review's expected-HEAD dirty-manifest acceptance was reproduced
before repair; the pilot Install now refuses dirty trees before its HEAD condition.
The new regression exercises the actual documented command, with fixture routing.
Neither this repair nor marker absence explains the old checkout.

The user reports that the UI exposes no Install execution log/exit. The corrected
pilot command now saves a separate attempt log and exit-status receipt outside
Git, with initial/prepared HEAD/pin; the mini diagnostic reads it if available.
Receipt persistence is to be tested; absence does not establish nonexecution.

Next action: publish/apply [the capturing Install command](cloud-bootstrap-handoff.md#published-environment-setup-command)
and run [the updated mini diagnostic](cloud-bootstrap-handoff.md#mini-diagnostic-task-prompt)
in a fresh task before manual bootstrap or skill-file reads. Compare prepared
HEAD/pin in the receipt with the fresh checkout, and investigate configured host
cwd/project-root routing separately from shell cwd. Keep the frozen
consumer SHA/source pin above; Start markers are not required. Record initial
checkout, session/project root, pin and actual available-skills metadata. Preparation
must precede host discovery; inspect absent catalog exposure separately if files
are present. Cloud and Ubuntu agent-host discovery remain unverified. Source
code-head and consumer review passed; documentation-head results remain tied to
their explicitly reviewed revisions. Enforcement reads remain access-limited;
green Actions and workflow YAML do not prove required checks. Actual merge→valid
completed Issue observation and administration mutations require separate
authorization. F14 stays integration pending and OpenSpec active; F01–F13 are
implemented/locally verified and ready for review, not merged or delivered.

## Earlier implementation evidence


Recorded 2026-10-04 for canzheng/workflow-skills, branch
`rewrite/workflow-skills-v2`, [draft PR #16](https://github.com/canzheng/workflow-skills/pull/16)
and [parent #1](https://github.com/canzheng/workflow-skills/issues/1).
This is acceptance evidence, not another backlog. GitHub owns live phases.

F01–F13 are implemented and locally verified; their implementation is ready for
review. F14 is partially completed, with required host/review/enforcement gates
pending. The branch is neither merged nor delivered; no release was published.

## Revision and actual verification

Actual clean starting commit: `d2aaf1904b2ccbe7fbab9733627e9c82fcf12f53` on `work`.
No reset to the research reference occurred. The approved clean-tree clarification
at main `e5747944a7e0520cf766db263834c8485fe63012` was integrated on this branch.

Historical implementation/test revision: `3386d008f809d32ebc6cf4f849b47750845c1cb6`.
This includes consumer CI, the clarified PR boundary, actual consumer-before-archive
proof and complete shaping output. The earlier bbbf1e5 revision passed 49 tests; its
affected setup/consumer/spec evidence was superseded by the following 51-test reruns.
Subsequent documentation-only review records do not extend this SHA's evidence to
an untested head. The exact final head and rerun outcomes are recorded in Issue #15
and PR #16 after publication; resolve that explicit SHA before continuing.

| Environment | Observed versions / preparation | Result at implementation SHA |
| --- | --- | --- |
| Managed Cloud task checkout, Debian 13 | Python 3.12.14, Node 24.19.0, npm 11.9.0, OpenSpec 1.14.0; fresh venv installation and rerun | `python3 tools/workflow/verify.py`: 51 tests, no skips, public source check passed; `check --repo . --specs --json`: strict current/delta validation passed; diff check passed |
| Actual Ubuntu container, fresh remote clone | Ubuntu 24.04.5 LTS amd64, Python 3.12.3, Git 2.43.0, Node 24.19.0, npm 11.17.0; venv dependency install twice, npm ci | Same 51 tests with no skips, public source and strict specs checks passed; clean tree; exit 0 |
| GitHub Actions | Real `v2 verification` job, pull_request event; Python 3.12, Node 24 | [Run 37205386850](https://github.com/canzheng/workflow-skills/actions/runs/37205386850), job 111445388641: all verification/spec/artifact steps succeeded |

Current implementation/test revision: `139e66d5b43cfbd3821fe098c0119b93aaad4928`.
The user-authorized one-shot initial-backlog refinement and S33 now pass all
54 tests without skips, public check and strict current/delta spec validation on
the managed Debian checkout and a fresh same-SHA Ubuntu24.04 clone.
[Source Actions37206519129](https://github.com/canzheng/workflow-skills/actions/runs/37206519129)
succeeded. The complete source/evidence head
`ed6c6e099e921b62a26f904c738da581f456aabc` also passed all54 tests without skips,
public checks and strict current/delta specs on this managed checkout and a fresh
Ubuntu clone; [Actions37209497302](https://github.com/canzheng/workflow-skills/actions/runs/37209497302)
succeeded. Subsequent evidence-only updates retain explicit tested SHAs and actual
final-head checks in Issue15/PR16.
The [real consumer pilot](f14-consumer-pilot.md) separately records source bundle pin,
consumer branches/SHAs, actual Issues, Ready PR, successful generic/trusted-base CI,
intentional metadata failure/restoration, Codex findings/fixes and Ubuntu tests.

Ubuntu image recipe is [ubuntu.Dockerfile](../../tests/v2/environments/ubuntu.Dockerfile),
base digest pinned; tested local image ID
`sha256:e83c8f9c800507cab5301055e31534ecc788506add79b84bfb1f45a67e1fab93`.
A fresh clone checked out the explicit detached SHA; no mounted checkout or prepared
home supplied skills. Session CA was mounted only for network access, not baked into
the image. Initial mounted-clone ownership and cross-device hardlink failures were
resolved by remote/copying clones, without changing global Git configuration.
This proves Ubuntu portability, not a particular user's private Ubuntu host.

The current 54-test suite invokes the production pinned setup, installed checker, actual
consumer CLIs, failure injections and real pinned OpenSpec validate/archive.
Without Node, optional fixture checks are disclosed as skipped; that is not full
rewrite acceptance. Here no tests skipped. The offline required runner rejects an
empty/missing suite and missing required checker. CI uploads verification JSON with
14-day retention. Durable summaries remain here and in GitHub; temporary local logs
are not promised as retained artifacts.

## Feature acceptance mapping

Numbers refer to each feature's numbered acceptance in the approved catalog.
Every feature uses the tested implementation revision above; earlier per-feature
revisions/decisions are retained in the active rewrite's tasks. The common next
action for F01–F13 is review the implementation and complete the named external
proof, preserving their existing evidence. No feature is reported delivered.

| Feature / capabilities | Acceptance evidence and documentation impact | Remaining limitation / next action |
| --- | --- | --- |
| F01 / C01,C16 | 1: actual baseline and 321-path inventory; 2–3: test_bootstrap preserved rules, explicit v2 routing and final retirement; 4–5: approved links, single active rewrite plan, contract scope/docs/evidence. Docs: AGENTS, CLAUDE routing, index, contract, migration. | Fresh host instruction-chain discovery is F14; retain original baseline. |
| F02 / C02 | 1–2: clean venv and actual Ubuntu preparation/rerun; 3: token-free fixtures and required missing-runtime failures; 4: pinned Python development dependencies/Node/OpenSpec versions; 5: runner missing-suite/checker negatives and disclosed old-test dispositions. Docs: development, environment recipe. | Fresh published Cloud preparation/discovery remains pending. |
| F03 / C01,C03 | 1–2: test_setup public fresh/dry-run/apply, preserved unrelated data, source/marker/path/symlink/collision preflight; 3: no-op/update/conflicts; 4: staging/apply rollback and exact residual recovery; 5: bounded uninstall/user config; 6: doctor duplicate/legacy/config/target findings; 7: incomplete bundle rejection and test_scenarios actual production bundle. Docs: operations, consumer guides, bundle provenance; owned generic consumer CI with configured argv execution and collision/modified-workflow preservation proof in test_consumer_ci. | Filesystem presence is not host skill activation; do fresh discovery. |
| F04 / C04,C13 | 1–4: Issue forms, PR template, lifecycle guidance and test_records phase/modifier/closure/parent representation; 5: open/closed identity fixtures plus live identity-safe publication; 6: link-only index, no state mirror. Docs: GitHub runbook/templates/index. | Live cancel/reopen/closure are fixture-only; do not close partial rewrite. |
| F05 / C05 | 1–5: primary-author shaping/current.py inspection, bounded bodies, dependencies, unknown/exclusions; 6: identity/human-edit fixtures plus live reconciliation; 7–9: S33 realistic five-outcome one-shot MVP batch, durable design anchors, confirmed prerequisite URLs, Ready/blocked separation, no execution from approval alone, stable rerun/contradiction negatives. Actual consumer Issues #1–#5 published. Docs: skill/usage/evaluations, approved refinement and pilot report. | Fresh host triggering and independent shaping evaluation pending; bounded pilot #1 execution was separately authorized, #2–#5 remain unexecuted. |
| F06 / C06,C07,C10,C16 | 1–2: exact-target delivery instructions and ordinary feature/bug outputs; 3–4: shipping defaults/errors/example updated, quantity repair justified no-impact; 5–7: original 697 retained, denied-remote continuation and actual consumer Issue → draft → checks → Ready PR6 → wf:review → independent review/fixes/re-review. Nested-JSON report finding reproduced/remediated with ten actual tests. Docs: contract/skill/usage/evaluation/templates/pilot. | Fresh host execution and nested-data re-review pending; PR open is not delivery. |
| F07 / C08 | 1–3: bounded repair without change, significant receipt change with sole change-owned plan; 4–5: partial-owner obligation, disposable final archive/current-spec synchronization, real rewrite kept active; 6: actual CLI 1.14.0 strict validation plus producer/consumer proof before archive. test_openspec. Docs: OpenSpec runbook, four implemented current specs. | Real rewrite archive waits for F14; structural CLI alone permits premature archive, so owner/review remains necessary. |
| F08 / C09,C15 | 1–2,6: risk-specific primary-author skill findings with honest authorship; 3: wrong 9975 vs hand-expected 7500; 4: ignored currency/missing target negatives; 5: weakened 498 assertion rejected against original 697. test_risk/test_setup. Docs: methods/L-001/L-002/evaluation. | Independent review and fresh-host risk selection pending. |
| F09 / C02,C10,C11,C13,C16 | 1: actual initial 403 did not stop code; 2: timeout/human-edit/duplicate/permission fixtures and live reconciliation; 3: missing/ambiguous branch/revision no fallback; 5: actual same-SHA Ubuntu; 6: dirty-content identity invalidation/affected reruns; 7: separate read/write/push/admin evidence, no credentials emitted. Docs: handoff/evidence/GitHub guide. | 4 fresh context resume remains F14; live lost-response/permission-loss cases are simulated only. |
| F10 / C04,C07,C10,C12 | 1: actual config argv consumer; 2: missing sections/path/anchor negatives; 3–4: malicious-data fixtures and actual consumer push/PR/body/Ready events, trusted-base/read-only checks; deliberate Documentation omission failed with pr.section, restoration passed; 5: runbook/settings reads; 6: read-only Issue audit; 7: semantic limits. Generic consumer CI executes application commands. Docs: checks/architecture/enforcement runbook/pilot. | Source trusted-base metadata needs main adoption; consumer trusted-base checks are active. Required merge enforcement remains unobserved, no admin write. |
| F11 / C07,C09,C12,C15 | 1–3: ordinary/bug/cross-module/risk actual consumers, omission/contradiction/no-impact primary-author exercises and broken controls; 5–6: discriminating results, no widened expectations/hidden skips/model harness. test_scenarios/test_risk/corpus/evaluations. Docs: corpus/evidence/coverage. | 4 triggering only explicitly read in-turn, not automatic fresh Cloud discovery; retain gap. |
| F12 / C13,C14 | 1–3: test_migration read-only known-format active/Done/deferred/inconsistent/missing/unsafe/duplicate proof and baseline 19 Done/0 active; 4–6: explicit disposition/freeze/one-authority/rollback procedure and interrupted identity/human-edit fixtures. Docs: migration runbook/current spec. | No active source work exists to migrate; actual consumer cutover and remote rollback not performed; universal formats excluded. |
| F13 / C01,C08,C15 | 1: clean clone and pinned install have exactly 3 skills, no v1 tree/global installer; 2–3: all 321 baseline dispositions/destinations and retained risk regressions; 4–5: no ledger/synchronizer, current architecture; 6: active rewrite gate; 7: primary-author reviewed exhaustive manifest validated by test_retirement. Docs: all current routing/guides, disposition manifest, four specs, Git baseline. | Independent asset/spec/document review pending; no global cleanup performed. |
| F14 / C02,C08,C11,C12,C16 | 2: observed separate-context resume at9cf27f80 preserving local-only work; 3: actual source54 and consumer10-test same-SHA Ubuntu passes; 4: actual consumer design batch, claim/branch/draft/CI/Ready PR/review fixes and completed Codex re-review; 5–8: gap mapping, actual metadata negative/restoration, settings/access evidence and overhead; 9: rewrite active. Docs: acceptance/consumer pilot/release notes/handoff. | 1 and remaining2: fresh Cloud task discovery and live API-safe rerun, Ubuntu agent discovery, nested-data re-review, representative fresh-host scenarios and rewrite-wide independent review remain pending. Merge/completion and administrative mutations require separate authority. |

## Scenario proof and gaps

The following names are files under tests/v2. Skill evidence refers to
[actual primary-author evaluations](skill-evaluations.md), not independent review.

| Scenario | Actual proof | Residual obligation |
| --- | --- | --- |
| S01 | test_setup fresh public install and test_scenarios pinned production checker | Fresh Cloud discovery pending |
| S02 | fresh venv/reinstall, Ubuntu clean clone/rerun | Fresh published Cloud readiness pending |
| S03 | test_setup unsafe paths/markers/owned collisions, source/hash/schema omissions | No pending deterministic path |
| S04 | test_bootstrap instructions and test_migration preserved records; final clean head | Fresh instruction-chain evaluation pending |
| S05 | test_setup failure before/during apply, restore/residual/retry | No pending deterministic path |
| S06 | test_records phase/block/defer/cancel/reopen fixtures; actual live review labels | Live cancelled/reopened smoke not performed |
| S07 | closed-ID/duplicate fixtures and all-state live search/publication recheck | Ambiguous live create exercised only as fixture |
| S08 | actual design/current-code inspection and candidate bodies | Fresh-host shaping pending |
| S09 | unknown retention isolated, sync/dashboard excluded, candidates unapproved | Fresh-host scope evaluation pending |
| S10 | shipping consumed, 747 proof/docs and reviewable PR16 delivery contract | Fresh-host ordinary feature pending |
| S11 | original 697 contract restoration/no new OpenSpec fixture | Fresh-host bug pending |
| S12 | shipping omission detected/resolved in actual README exercise | Independent semantic review pending |
| S13 | default 50 docs vs actual 0 found/corrected by primary author | Independent semantic review pending |
| S14 | repaired quantity docs still true; reasoned no-impact | Fresh-host judgment pending |
| S15 | real disposable OpenSpec receipt: broken EUR 1.99 then expected EUR 3.98, archive and strict specs | Rewrite archive blocked by required F14 gates |
| S16 | actual 403 initial create, continued implementation, later confirmed IDs; permission-loss fixtures | Fresh-host degraded-mode pilot pending |
| S17 | same 3386d00 SHA on Cloud checkout and actual Ubuntu clone | Fresh independent Cloud continuation pending |
| S18 | write-success/response-loss fixture re-read avoids duplicate | No live response deliberately lost |
| S19 | wrong percent formula fails hand expectation 7500 | Fresh-host risk reasoning pending |
| S20 | parser-only currency fails EUR6.97 consumer, actual config argv executes | Fresh-host contract review pending |
| S21 | weakened 498 fixture rejected against697 | Independent semantic review pending |
| S22 | partial/open state retained, closure audit/stale/doc limits; no Issues closed | Final aggregate closure not attempted |
| S23 | duplicate/human-edit fixtures, compare-preserving live catalog updates | No simultaneous live race deliberately induced |
| S24 | partial OpenSpec tasks remain open, closing owner, disposable completion/archive | No live multi-PR delivering merge performed |
| S25 | original baseline/explicit dispositions, final clean clone, no dual ledger; rollback fixtures/guide | No active consumer rollback performed |
| S26 | missing worktree/branch/revision CLI fails without cwd fallback | No pending deterministic path |
| S27 | actual source/consumer push and PR Actions, Ready event, trusted-base body-edit missing Documentation failure and restoration success; malicious-data fixtures | No pending consumer deterministic event proof; source trusted-base adoption still pending |
| S28 | SHA/dirty content invalidation fixtures and actual reruns after changed tests | Final docs head verification recorded remotely |
| S29 | exact checkpoint/next action below | Required fresh Cloud task unperformed |
| S30 | denied targets/permissions, staging/apply/interrupted migration negatives | Fresh-host targeted analysis pending |
| S31 | rulesets GET returned []; branch-protection GET403 | Required contexts/merge blocking unobserved |
| S32 | known v1 active/Done/deferred/malformed and partial remote success fixtures | Actual source0active means no live import |
| S33 | realistic design, five actual published consumer Issues, user-authorized batch readiness with roots Ready/unknown and dependents blocked, preserved detail/design anchors, no task Issues/extra execution; test_initial_backlog link/dependency/rerun negatives | Fresh-host shaping rerun and discovery still pending; actual publication is proven separately from fixtures |

## GitHub, enforcement and review

After the user updated the connected app, writes succeeded. Parent #1 and F01–F14
Issues #2–#15 exist with stable source markers; searches covered open and closed
Issues before creation and on retry. Publication recheck found unique identities.
[Issue index](../v2/issue-links.md) holds links only. Draft PR16 and branch publication
are confirmed; no token was needed or exposed. Bodies/labels are read before scoped
updates, preserving human content and unrelated labels. Fault tests remain fixtures.

Read-only `GET /repos/canzheng/workflow-skills/rulesets` returned `[]`.
`GET /repos/canzheng/workflow-skills/branches/main/protection` returned403
Resource not accessible by integration. This does not prove classic protections
are absent. No protection settings were changed. Consumer CI is installed automatically
as owned files and actual Actions/trusted-base metadata passed in the newly adopted
consumer; intentional body-edit failure/restoration is recorded in the pilot report.
The consumer's ruleset/protection reads returned distinct403s, not proof of active
merge blocking. `v2 verification` and consumer `v2 PR contract` are observed;
`v2 PR contract` trusted-base metadata cannot run for first adoption while main
lacks the new checker/workflow. Actual merge blocking must be observed after
authorized configuration; see [runbook](../workflow/checks.md).
No authorization to merge, configure protection, publish or delete branches exists.

Semantic evaluations and final documentation assessment are primary-author.
A user-supplied external reviewer examined architecture/skills/templates/Actions and
reported targeted comments, validated in reviewer-findings.md. That limited input is
not final independent acceptance review of the revised code/specs/docs/dispositions.
Native independent Codex review of consumer PR6 completed with two P2 findings;
both were validated by reproduction and remediated with discriminating tests/docs
at the actual consumer head. Native re-review completed at2b4ecd69 and reported no
major issues; an earlier supplied Cloud report's separate nested-JSON finding was
then independently reproduced/remediated atcec53770 with ten-test Cloud/Ubuntu/CI
proof; its targeted re-review is tracked separately rather than waived by prior review.
The host's current Cloud platform-guide fetch returned403; no current published
profile behavior, secret lifetime or automatic skill synchronization is inferred.

Pilot overhead: no normal-implementation confirmations, per-task plans, new ledger
or forced reviewer/subagent rounds. Shipping required actual updated docs; quantity
repair required no-impact reasoning. Receipt significant change used its single
OpenSpec plan; risk cases used targeted proof. No speedup metric is invented.

## Documentation/specification completion

Reviewed the final runtime, config consumers, setup ownership, commands, tests and
instruction chain. Updated root AGENTS/CLAUDE/README, docs index/architecture,
development/operations/migration, contract/GitHub/usage/OpenSpec/risk/handoff/check
guides, installed consumer guidance, Issue/PR forms, scenario/evaluation records,
release notes and asset manifest. Reconciled current source-vs-baseline inventory
and Git-only old archives during final assessment. The three approved scope docs
contain human-approved design, not live status. The Issue index has no phase mirror.

Current specs: workflow-v2-adoption, workflow-v2-delivery, workflow-v2-migration,
workflow-v2-quality. Actual strict checks passed. Active workflow-v2-rewrite owns
remaining release gates and the only rewrite plan. Do not archive merely because
CLI structural validation permits it. Final required acceptance, then archive/current
spec synchronization and post-archive verification remain the closing obligation.

## Exact next Cloud action

Start a new Codex Cloud task for this repository at the explicit final SHA recorded
in Issue #15/PR16 on `rewrite/workflow-skills-v2`. If branch/SHA differ or are missing,
stop that item; never select another checkout. Read AGENTS.md, docs/README.md,
contract, all three approved scope docs, this report and the active rewrite tasks.
Do not repeat F01–F13 or create another plan/backlog. Use Issue #15 for remaining work.

1. Capture clean branch/full SHA, versions and actual Cloud preparation profile;
   install pinned requirements and npm dependencies, rerun after preparation changes.
   Run verify.py and `workflow.py check --repo . --specs --json`.
2. In fresh context discover the three intended repository skill names, read their
   SKILL.md files, and install the real full-SHA bundle into an explicit clean Git
   consumer using documented setup/doctor commands. Capture actual host discovery,
   not only files or doctor diagnostics; do not alter globals.
3. Exercise shaping plus ordinary feature, bug, receipt cross-module and targeted
   risk prompts from tests/v2/scenarios. Record actual outputs, consumer proof,
   scope/unknown handling, omitted/contradictory docs, valid no-impact and denied
   remote handling. Identify author/environment and keep fixtures distinct from live
   operations. Record continuation using existing Issue/PR references.
4. Preserve passed Ubuntu/Actions evidence if content is unchanged; rerun affected
   proof at any changed implementation SHA. Obtain final independent semantic review.
5. Continue the existing real consumer at the exact branch/SHA in
   [its report](f14-consumer-pilot.md), Issue1 and Ready PR6. Preserve actual passed
   publication/CI/Ubuntu/review-fix evidence; do not create another consumer or repeat
   completed work. Fresh Cloud task has been launched by the user; collect actual
   discovery/use, safe shaping rerun and continuation evidence. Ubuntu discovery
   must be observed in its actual agent host. Merge/completion can
   be observed only with separate merge authorization; until then keep that final
   path pending. Report trusted-base metadata adoption and administrative enforcement as still
   pending unless observed by an authorized owner. Changing protection or merging
   still needs separate authorization. Do not bypass gates or infer approval.
6. Only after required acceptance is satisfied, archive with pinned OpenSpec and
   rerun current-spec/docs/full verification on the archive diff; update PR/evidence
   and leave reviewable. Do not merge/publish or close delivery prematurely.

Ubuntu repeat recipe: build the tracked Dockerfile using the Cloud runtime's local
Docker socket and CA secret, then start that image with session CA mounted read-only.
Inside it clone the rewrite branch from GitHub, detach the explicitly recorded SHA,
create .venv, install requirements twice, run npm ci, verify.py, strict specs and Git
clean/diff checks. Do not reuse a mounted source checkout as fresh-host proof.

## User-authorized initial-backlog refinement

Follow-up scope explicitly approved by the user: make existing-design → initial/MVP
backlog the one-shot default, with internal optional decomposition, faithful detailed
design translation, delivery-level Issue granularity, one batch approval, separate
execution authority, stable reruns and lightweight direct prerequisite metadata.
S33 was added to the approved capability/feature/design contract and current delivery
spec, with realistic input/output and primary-author evaluation. This extends F05/F11
and the real F14 consumer pilot without a new state engine or mandatory artifact.
Earlier implementation-SHA results above remain historical evidence; the final revised
SHA/reruns and consumer pilot outcome are recorded in Issue15/PR16 after publication
and [the durable consumer report](f14-consumer-pilot.md).

## User-approved pinned dependency refinement (S34)

Source `47320c363e538d2c8423e11e5ca9121c2d0303da` passed all62 tests without skips,
public checks and strict specs on Debian Cloud and fresh Ubuntu24.04.5 remote clones.
Actual source push/PR Actions37213148746/37213152015 pass. Eight additional meaningful
bootstrap tests prove fresh Git clone/public CLI, scoped ignores/project skill tracking,
project bytes/index preservation, ignored-byte evidence invalidation, exact fetch pin,
denied fetch, modified/extra/symlinked assets, invalid URL/hash/policy, rollback/retry,
and explicit old tracked-file migration. Existing setup tests prove no-op adoption.
Approved design/capability/feature docs and adoption specs now describe S34 and the
small repeatable bootstrap; no extra backlog or distribution engine was introduced.

Consumer `pilot/shared-skill-bootstrap` at539580779e52eef5b976a0460d7d18e16833c2b0
pins that exact source. Cloud-runtime and Ubuntu fresh-clone materialization/hash/
no-op/clean-tree checks passed. Actual consumer push/draftPR/metadata Actions pass,
and the bootstrap job step was observed. PR8 is Ready and Issue7 wf:review; required
semantic result is pending until read. The older ingredient PR6 atf95f0cae3b87bc8031b00a4150cf9670251ae978
passes11 tests on Cloud/Ubuntu/Python3.14 and its current-head Codex review reports
no major issues, with all validated findings remediated and threads resolved.

Use [the exact environment script and fresh task prompt](cloud-bootstrap-handoff.md)
next. Fresh pre-agent Cloud discovery/use and Ubuntu agent-host discovery remain
integration pending. Merge → completed Issue observation and administrative mutations
remain pending authorization; enforcement read access is still limited. F14 remains
incomplete and the rewrite change active; F01–F13 implemented/locally verified is
not a merge or delivery claim. See [consumer evidence](f14-consumer-pilot.md) for actual
Issue/PR/Actions mapping and the distinction between older adoption and S34 proof.

Latest implementation evidence supersedes earlier refinement counts: source
`11fa051a7c4af359bd4728e1edf69cd8c7a61259` passes68 tests/no skips and strict specs
on Cloud/fresh Ubuntu, with actual source push/PR success. Independent PR findings
were validated and remediated with failing-before coverage for effective ignores,
runtime mapping omissions, extra ignored evidence identity and unsafe migration
archive paths. Consumer `5efc5f5ffdcab46a440b2cb2237924ee476a5bd9` pins that source;
actual fresh-clone same-pin bootstrap/hash/no-op/clean-tree checks and push/PR/metadata
pass. Final semantic review results must be read before claiming review completion.
The unified environment command was actually exercised from a new repo without tools
and rerun unchanged. Current script/pins and exact next Cloud prompt are in the handoff.
Documentation revisions update evidence/commands only; executable pin remains explicit.

Current environment checkpoint: source7e71186ec8146b682f4c4cf40c8da5ecb6d3f608 passes
70 tests/no skips and strict specs on Cloud/fresh Ubuntu; actual Actions pass. Consumer
79efd96276e25e2c1a706a3c7972dbebf32d2a0a includes the project-owned unified environment
shell script and corrected README, pins7e71186, and passes actual first-adoption/no-op/
index-preservation plus fresh Cloud-runtime/Ubuntu exact-pin script checks and real
push/PR/metadata CI. The standalone script, rather than implicit CLI adoption, handles
repos initially missing tools. See the current handoff and consumer report. Latest
requested semantic outcomes are not inferred from CI; native host discovery and
merge/admin requirements remain explicit pending gates. F14 remains partial.

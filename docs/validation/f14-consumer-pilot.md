# F14 real consumer pilot

## Latest directory-binding and native Issue-state checkpoint — 2026-10-05

Source `09998db554066b742f612d2e95a9c6bdb7c7b578` passes148/no skips on managed Python3.12.14
(143.175s) and Ubuntu24.04.5/Python3.12.3 (123.474s), plus strict OpenSpec all5 items.
Consumer `22a5c42c0eb43c9c0eda427061237e27f9079819`, pilot/shared-skill-bootstrap, Ready PR8/Issue7,
pins this source. Its push37338701217/PR37338713719/existing-main metadata37338708449
pass. Source pin Actions37338647841/37338660724 were running at recording; current
head results and semantic review are recorded separately in the live PR checkpoint.

Review5417258594 at300ab5c returned P2s4185998816/4185998828. Both independently
reproduced: swapping a parent inside unlink deletes human content in the replacement
directory; unknown state strings pass native Issue audit. Two controls fail four
subcases on the old implementation. Eight additional immediate-parent/ancestor
stage-open/replace/restore/cleanup controls also fail on the old implementation.
All controls now pass without narrowing prior concurrent-edit assertions. Apply,
staging/replacement/cleanup, rollback and created-directory operations bind relative
names to verified directory handles, opened component by component with no-follow
and expected inode checks. Replaced namespaces preserve human files and report
recoverable originals; recovery remains best-effort, with no multi-process lock.
Issue states normalize case and accept only open/closed; omitted state remains open.
Malformed input yields structured exit2 JSON without snapshot/index mutation.

The57 focused tests pass (24.178s). Fresh actual remote consumer clones on both
hosts bootstrap11 missing dependencies, match20 managed hashes, retain four narrow
ignore namespaces/tracked project skill and preserve files/raw index on offline
repeat. The25-test actual installed runtime suite passes both hosts (55.797s/51.551s),
including the new mutation controls, native states, both layouts, CI and isolated
optional-global fixtures. Literal exact-pin Ubuntu fetch-and-run first adoption/
repeat passes; absent index and repeat bytes remain unchanged. Actual global-host
installation was not performed. Source-owned consumer update preserved configuration,
all skill bytes and raw indexb942fe7aa710e079b8d5746cc981f580afccc625b4d49e66a95bcc48fa108d39
before caller staging. Published treea197399eb44b20431d574b3a64df5e4db3ac6684 matches
reviewed localc22af21676de7272d97ba2dff53e54b7ad150d8b; parentf860135; guarded non-force publication.

F01–F13 implemented/verified/review-ready; F14 partial pending repaired-head semantic
review and native archive/final checks. Previous consumer review5997917302 was clear
atf860135 and does not approve the repin. Native Ubuntu startup catalog/actual use
retains original9bd23d72/a75c3f2 evidence with unchanged shared hashes. Cloud deferred;
historical Ubuntu26 full-suite invalid-JSON cause remains unexplained. Consumer
required checks/source verification enforcement are read-only observed; new trusted
base metadata deployment and source PR-contract administration remain pending.
Real merge and valid completed Issue observation require separate authorization.
No merge/closure/admin/global/auth/release/remote deletion. Next: current-head review;
archive only after required premerge review clears. Five-minute monitors apply to
new review requests during this active turn, with no persistent wake-up claimed.

## Latest source-check compatibility checkpoint — 2026-10-05

Source `9d5489ffa11cf8bbde3f4c569c17a526e5d86c98` passes143/no skips on managed Python3.12.14
(148.826s) and Ubuntu24.04.5/Python3.12.3 (124.375s), plus strict specs.
Consumer `255371e48f46549b4099182d66c598d767235277`, Ready PR8/Issue7, pins it.
Fresh remote clones and the actual installed fourteen-test layout/CI/check suite
pass both hosts (52.824s/46.296s); Ubuntu literal pinned installation/repeat pass.
Review5416098884 at151476c returned P24185120389, independently reproduced and
repaired with layout-aware source requirements. Both supported tracked layouts
pass, all seven omitted-module cases in each layout fail, and mixed inventories
are rejected consistently. Consumer push37330126608/PR37330146379/existing-main
metadata37330140351 pass; current source CI is recorded in the PR checkpoint.
Current repaired-head semantic review and archive remain pending. Native Ubuntu
catalog/use retains unchanged-skill original evidence. Cloud is deferred; actual
merge/completed closure, deployed-base metadata and source PR-contract admin gates
remain pending separate authorization. See [wider review](wider-boundary-review.md).

## Latest layout/provenance checkpoint — 2026-10-05

Source4449a1e6d03b6e055446735b89c4630b0c8b9d85 passes142/no skips locally
and on Ubuntu24.04.5; consumer66913db29472d8277002b068205fc05db62b2bbf
pins it. Installed twelve-test layout/CI suite and source-first fresh-clone/index
proof pass on both hosts; literal Ubuntu pinned installation/repeat and consumer
push/PR/metadata Actions pass. Both source review P2s at946dffe were reproduced
and fixed; prior consumer review atb33b0d4 was clear. Current-head review/archive
remain pending. Native catalog/use retains unchanged-skill original evidence;
Cloud deferred, actual merge/completed closure/base deployment/admin gates pending.
See [wider review](wider-boundary-review.md) for exact acceptance and limitations.


## Latest implementation checkpoint — 2026-10-05

Source pin0f6b6766da7a86a039108891ec051306963425ae passes138/no skips on managed
runtime and Ubuntu24.04.5. Consumerb33b0d4a938b2718a3adb686f4899b4689d46b20
pins it; current-head push/PR/metadata Actions, source-first fresh-clone/index
proof and actual installed six-test suite pass. Literal Ubuntu fetch-and-run
first adoption/repeat pass. Native Ubuntu discovery/use remains revision-bound
to unchanged skills at original9bd23d72/a75c3f2. Current semantic review/archive
remain pending; Cloud deferred and real merge/valid completed closure/base
deployment/admin configuration require separate authorization. See
[wider review](wider-boundary-review.md) for exact tests, environments, CI and limitations.


## Latest verified runtime and consumer checkpoint — 2026-10-05

Source `f05cf27df47e008bf52e6f14a8dbd6bbf53e4f80`; consumer
`d8ed0abca40a7fa4ed092f4facfb25fefee30977`, pilot/shared-skill-bootstrap/ReadyPR8.
All137/no skips pass locally and Ubuntu24.04.5; current source/consumer docs/specs
cover indexed ancestors, complete runtime retirement and executable migration.
Actual remote fresh clones, installed public boundary tests and consumer push/PR/
metadata pass;11 pinned dependencies remain ignored/untracked under four namespaces.
[Exact current evidence](wider-boundary-review.md) supersedes earlier checkpoints.
[Source-first Ubuntu command](ubuntu-workstation-handoff.md) records both full SHAs.
Original native discovery/use keeps its actual unchanged skill hashes. Current-head
semantic review and final archive remain pending; deployed-base new metadata and
real merge→valid completion are separate authorization gates. Cloud deferred, real
global-host use unperformed and historical Ubuntu26 source-suite error unexplained.

## Current shared-runtime checkpoint — 2026-10-05

Source pin `ffe656fe8247ce96805fbf095fba8108c1253774`; consumer
`47784787f17803da3051deed92bd818bdae388c1`, pilot/shared-skill-bootstrap/ReadyPR8.
Schema5 materializes11 skill/runtime dependency files and ignores only the three
shared skills plus .agents/tools/workflow; project assets remain tracked.
All132 tests/no skips pass locally and Ubuntu24.04.5. Actual fresh remote clones
on both runtimes pass source-owned initialization,20 hashes, installed verification,
offline repeat/raw-index preservation and retained negative controls. Source and
consumer push/PR Actions pass; existing-main metadata also passes. The new trusted-
base pin-fetch YAML is locally exercised; actual deployment/event execution on main
awaits the separately authorized adoption merge.

[Exact evidence and review controls](wider-boundary-review.md) supersede earlier
current/default claims below; earlier revision-specific observations remain historical.
[Ubuntu setup handoff](ubuntu-workstation-handoff.md) records exact usable pins and
source-first commands. Both latest P2s were reproduced before repair; current-head
semantic review and final archive/docs/spec checks remain pending. Original native
Ubuntu discovery/use retains its unchanged skill hashes. Consumer ruleset requires
both checks; source ruleset now requires verification, while source PR-contract
administration/deployment and merge→valid Issue completion remain separate gates.
Cloud deferred, real global-host use unperformed, historical Ubuntu26 source-suite
error unexplained. No merge/completed closure/admin/global/auth/release/deletion.

## Created-directory rollback repair and host continuation design — 2026-10-05

While checking review completion, consumer Codex5993154072 reported no major issues
at1995bffe69; source4183335258 identified discarded directory permission changes.
Independently reproduced with public setup and separate replacement/nonempty controls.
Candidate c444a49 also failed two existing global-target tests; the final runtime
`b36fab26859ba6b497fa926e766d948b8981b113` restores absent-target creation/recovery,
with an additional isolated global-root regression. No assertion was weakened and
no real global home was changed. Newly created directories record inode/device/mode;
cleanup removes only unchanged empty directories, preserving/reporting changed or
nonempty paths and their creation metadata. Source/consumer operations and current/
delta adoption specs now explain those recovery semantics.

Source `381e51c4bc8c5086dd7b23c35d2dd480a5ecca81` passes118/no skips and strict
specs on managed runtime and Ubuntu24.04.5; installed bytes match the b36fab2 pin.
Consumer `7a74c9714774a4dd1533dd3e68ba80aabae1e5ea` pins it; reviewed tree
639f8a233ecf3d62c9a47dda4235b9629761160e matches own local2e44317f483a7ee368e8da0cb1146c6d31ce4524
with parent1995bffe retained and guarded non-force publication. Project/index/shared
hashes remain unchanged during source-owned update; source/consumer trees are clean.
Fresh actual remote clones on both runtimes bootstrap4 files/match20 hashes, pass
check/doctor/repeat offline/no-op and preserve project/index bytes. Actual installed
public setup proves changed-directory and concurrent-file recovery; retained force-
tracking/index-only nested-policy negatives still reject without mutation.
Consumer push37303704039/PR37303709363/metadata37303707010 pass. Source
push37303695349/PR37303702844 results are recorded in the latest PR/Issue checkpoint.
Final current-head reviews remain required; older consumer approval is not new-head
approval. User Ubuntu initial discovery/actual3-skill use remains at unchanged bytes;
Cloud deferred, intermittent Ubuntu26 source-suite cause still unresolved.

The user requested automatic review continuation. The optional
[host integration design](../workflow/review-continuation.md) specifies scoped
wake-ups, current-head completion evidence (including comments/reactions), duplicate/
concurrency controls, authorized remediation and the merge boundary. This chat exposes
notification scheduling but no Codex wake-up/event-subscription tool, so no monitor
is enabled or automatic coding continuation claimed. This adds no mandatory workflow
engine, database, installation requirement or acceptance gate. Next: inspect final
review outcomes, remediate valid findings, then archive/check after required premerge
acceptance; host integration requires an actual supported wake-up acceptance proof.
No merge/completed closure/admin/global/auth/release/remote-deletion action.

## Concurrent-edit rollback review repair — 2026-10-05

Source ReadyPR16 review4183164337 at e42e865 identified rollback overwriting an
edit made after an installer replacement and before a later failure. Independently
reproduced through public setup before accepting the finding. Source repair
`b444021557d1a67f2a2e04deb6bc4d87f2772bd5` records successful applied states from
staged bytes/mode/inode, revalidates safe paths and restores only unchanged writes.
Concurrent byte/mode edits, deletions, file/ancestor symlinks, recreated deleted files
and edited newly created files remain recoverable residuals with original backups.
Normal restoration and explicit fixture recovery/retry still pass; raw index is untouched.
Source and consumer operations/current+delta adoption specs document best-effort
recovery without promising multi-process locking or atomic multi-file transactions.

`python3 tools/workflow/verify.py`: 115 tests/no skips, OK, on managed runtime
(Python3.12.14) and Ubuntu24.04.5/Python3.12.3. `check --repo . --specs --json`:
exit0/ok:true on both; focused setup19 passes. The original concurrent-byte path
failed before repair; the broader before-fix run also exposed mode/deletion/symlink
cases and one cascading fixture failure, not seven independent production defects.

Consumer `1995bffe694f7f15ee8fe08d65067906a7b65341` pins b444021. Reviewed tree
193ec5897d6a28acd101c0f08887eb8f1acb9699 matches own localc864172ade5be44565b966f9201289b4f13c27d9,
parent2a59 preserved, guarded non-force publication; no main/global/admin changes.
Project policy/config/ignore/project skill/raw index and four shared hashes stayed
unchanged during update. Actual fresh remote clones on managed runtime and Ubuntu
materialize4 canonical files, match20 hashes, pass check/doctor/repeat offline/no-op,
and preserve tracked/index bytes. Installed public setup additionally preserves
concurrent user bytes, reports exact recovery, and retains force-tracking plus three
index-only nested-policy negatives. An initial disposable live-proof harness used
the source's nonexistent consumer operations path; resolving the bundle mapping
corrected that harness before both clean fresh-clone reruns passed.

Consumer push37299940648/PR37299946461/metadata37299942904 succeeded. Source
push37299931643/PR37299938408 both succeeded at the tested executable revision;
final documentation-head CI/review results belong to the latest PR/Issue evidence. Initial independent user Ubuntu startup
discovery/actual3-skill use remains verified at unchanged shared hashes. Earlier
Ubuntu26 source-suite intermittent invalid-JSON cause remains unresolved, not
claimed fixed. Cloud deferred; optional real global-host use unperformed.

F01–F13 remain implemented/verified/ready for review. F14 remains partial pending
final current-head semantic review and final archive/spec/docs checks. Actual merge
and valid Issue completion, administration and release require separate authorization.
Next: observe exact-head Actions, request final semantic review, then archive only
after the required premerge acceptance passes. Earlier checkpoints retain their pins.

## Malformed bundle review repair — 2026-10-05

Consumer ReadyPR8 at fd49a238121b0c0bc54754fb79f792f290d880ff received independent
Codex response5992697851: no major issues. This is review evidence at that exact
commit, not approval of subsequent commits. Source ReadyPR16 at caa29d523513219374b0789f2e12a000d8aa40cc
received P2 review4183023649: non-string source destinations reached set conversion,
producing an unhandled TypeError for arrays/objects. Independently reproduced before
acceptance; five bad destination cases failed on original code.

Tested executable repair `d1de33ac3c6e889ea0c189ec53b000fe0bfddecc` validates string
destinations before set conversion. A public regression covers array/object/null/
integer/boolean destinations through setup and explicit install-skills: exit2 with
ok:false JSON, unchanged target/index, no global-target creation. All113/no skips
pass on managed runtime and Ubuntu24.04.5; strict specs pass. This restores the
already documented invalid-configuration/structured-error/preflight contract, so
no product or specification change is required. It does not establish the cause
of the earlier intermittent Ubuntu26.04 source-suite error.

Current consumer `2a59be9b42719e020c7888d61f9ea59e5214035a` pins d1de33a. Source-owned
update preserved project policy/index and all four shared hashes. Reviewed tree
acc18ae2795ef8d9e27823157c615056dee046c0 matches own local52f34c1a0255961329372c622495446d4e5e0ede,
parentfd49 retained and original local commit in reflog. Guarded non-force publication;
no main/global/auth/admin change. Current consumer/source CI and final semantic
review are recorded in Issue15/PR16/PR8; do not carry the prior consumer review pass
forward as a new-head pass. Fresh-checkout/runtime/Ubuntu verification is affected
by runtime updates; initial native discovery/use remains at unchanged skill bytes.


Latest observed integration: source executable d1de33a push37297748431/PR37297752467
both succeeded; consumer2a59be9 push37297839256/PR37297846639/metadata37297841685
all succeeded. Fresh actual remote clones on runtime and Ubuntu materialize4 files,
match20 hashes, pass check/doctor/repeat with tracked/index bytes unchanged and retain
installed force-tracking/nested-index negatives. The malformed destination regression
also verifies both public installers return structured exit2 without writes.

F14 remains partial pending current-head review and final archive/spec/docs checks.
Both PRs are Ready/open/unmerged in different repositories: workflow-skills PR16
for source delivery, workflow-skills-test PR8 for consumer adoption. Cloud deferred;
merge/completed closure/admin/release require separate authorization.

## Ubuntu agent acceptance and reviewed repair — 2026-10-05

The [independent workstation session](ubuntu-workstation-session.md) proves native
initial discovery of all3 repo-local v2 skills before explicit reads, actual delivery/
risk/backlog use and no-chat continuation at consumer9bd23d72/sourcea75c3f2 on
Ubuntu26.04/Python3.13.13/codex-cli0.160.0. Prepared/fresh-clone raw-index hashes
match before/after; the five Pantry MVP identities/dependencies/phases reconcile
without duplicates, new Issues, invented dietary policy or application dispatch.
The live Issue collection independently confirms those identities/dependencies.
Doctor's unprobed host field is not a contradiction of the native startup catalog.

Source runtime repair `b5b8da40eef689852bdc3d7dfd644eeca4e878e8` independently fixes
consumer4181927560 (schema4 setup checks dependency/index policy before writes) and
source4181938333 (nested staged policies/project paths come from canonical index).
All112/no skips and strict specs pass on runtime/Ubuntu24.04.5; source actual
push37295605641/PR37295615153 pass. Consumer `fd49a238121b0c0bc54754fb79f792f290d880ff`
pins the repair, preserves project configuration/ignore/index, and all four shared
hashes remain unchanged from the successful workstation session. Fresh actual
runtime/Ubuntu clones pass exact materialization/all20 hashes/repeat/index proof and
installed force-tracked-setup/staged-nested-policy negatives. Consumer actual
push37295787146/PR37295793465/metadata37295789815 pass.

The workstation's one intermittent source-suite JSON error remains unreproduced;
its outer traceback identifies expected exit1/invalid stdout JSON but not command
or inner streams. The helper now retains those streams instead of discarding them.
Two OpenSpec skips reflect absent source-local pinned tooling, not a reported pass;
prepared source/Ubuntu runs above have no skips. Original107 evidence retains its
own environment/revision. Current-head final independent semantic review and final
rewrite archive/spec/docs verification remain pending; F14 stays partial. Cloud is
deferred. Merge/completed closure/admin/release need separate authorization.

Earlier dated evidence below retains its original revision and pending state;
this checkpoint supersedes earlier pending Ubuntu discovery/use wording.

## Actual user Ubuntu bootstrap — 2026-10-05

[Workstation evidence](ubuntu-workstation-bootstrap.md) now verifies first/repeat
bootstrap and installed check/expected-revision doctor at consumer9bd23d72 on the
reported Ubuntu26.04, Python3.13.13, Git2.53 and codex-cli0.160.0. Four shared files
were installed; repeat changes:[]; no shared files indexed and final Git status clean;
enclosing validation exit0. Three existing global v1 skills generated warnings,
with no global mutation. Fresh agent discovery/use, continuation and final semantic
review still need evidence. The workstation output did not run the source107-test
suite or prove raw-index byte identity; previous runtime/index/CI/enforcement
results retain their own revisions. Next: start Codex from the exact consumer root
and use the [fresh-session prompt](ubuntu-workstation-handoff.md#fresh-ubuntu-task-prompt).

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

## Current staged-snapshot repair and reproduced Cloud blocker — 2026-10-05

Consumer `pilot/shared-skill-bootstrap` now `f6394326cd410b82567b8fea76bfd5c44fa9261a`,
source `a4eb9f1303d80cc18f83b5bbd734063cac03b9c3`, reused Issue7/ReadyPR8. Actual
update preserved project config/AGENTS/ignores/project skill/raw index; app-published
reviewed tree4e5d8ecbbddbd182080972fc2a9d30197726312d matches local2a3f2c3, no force.
Fresh actual runtime/Ubuntu clones match20 hashes, repeat check/doctor/read-only
bootstrap without mutation, and reject missing/untracked/corrupt-staged/partial
manifest paths without repair. Actual push37272954548/PR37272958814/metadata37272957270
pass. Consumer finding4181129303 independently reproduced on old installed CLIs
before the existing source staged-validation repair was accepted; tests now also
cover partial provenance updates and intent-to-add. Current semantic review pending.

The user's recreated-environment report again observes old main5d055649/source139e66d5,
intact/unignored shared files, initial/workspace cwd/workspace and no workflow names
in exposed catalogs. Complete repo catalog/root unavailable; automatic discovery
remains blocked/unverified. Recreating environments did not resolve it; no further
installation or merge is inferred to fix it. See [current acceptance](v2-acceptance.md#recreated-cloud-comparison-and-current-consumer-repair--2026-10-05)
and [supplied report](f14-published-cloud-run.md#recreated-environment-reproduced-catalog-absence--2026-10-05).
Support/debugging needs actual host root/catalog/checkout ordering. Manual repo-skill
reading/use remains a fallback, not automatic discovery acceptance. Earlier exact
revisions/evidence remain below; no merge/closure/admin/global change.


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


Recorded 2026-10-04. This is immutable acceptance evidence, not a second backlog.
Live scope/phases belong to GitHub. The user authorized this disposable consumer
pilot through review and environment verification, excluding merge/completed closure
and repository administration. F14 remains partial; nothing is reported delivered.

## Verified/completed under current authorization

Repository: [canzheng/workflow-skills-test](https://github.com/canzheng/workflow-skills-test),
an existing private repository. Actual inspected initial main was
`a2f84e768e42e900d47ace5e21897f7e02e71f2a`, containing only the user's README.
Pinned workflow source: `139e66d5b43cfbd3821fe098c0119b93aaad4928` on
`rewrite/workflow-skills-v2`. Production setup dry-run/apply installed the three
skills, contract, provenance, configured checker and two generic owned workflows,
preserving the README. No global installation or configuration was changed.

Adoption main: `5d05564919c55f1d4d0c2e1e020ad914252a2979`. This direct bootstrap
publication added workflow assets/design, with the user's F14 authorization; it was
not an implementation PR merge. Actual app changes use
`pilot/ingredient-catalog`, current tested head
`f95f0cae3b87bc8031b00a4150cf9670251ae978`,
[Ready PR #6](https://github.com/canzheng/workflow-skills-test/pull/6),
non-closing reference to [Issue #1](https://github.com/canzheng/workflow-skills-test/issues/1).
Private CLI push was unavailable; connected Git-data APIs published trees whose
SHA matched the locally tested Git tree, with actual parent/ref checks and no force.
The actual remote commit was fetched and verified. No credential values were read.

### Design to initial backlog

The primary author explicitly read and used installed workflow-design-to-backlog,
workflow-deliver-issue and workflow-risk-review. The realistic
[MVP design](https://github.com/canzheng/workflow-skills-test/blob/main/docs/design.md)
was shaped in one coherent batch, using the smallest five verifiable outcomes.
Existing explicit examples/acceptance were retained; later Cloud/account/mobile
scope was unmaterialized. No engineering-task Issues or editable backlog file exist.
All-state search preceded creation; confirmed URLs populated direct prerequisite
JSON and matching readable links after all Issues existed.

| Outcome / stable source ID suffix | Actual Issue | Initial approved disposition | Confirmed direct prerequisites |
| --- | --- | --- | --- |
| Ingredient catalog / ingredients | [#1](https://github.com/canzheng/workflow-skills-test/issues/1) | Ready, then explicitly selected execution | [] |
| Recipe catalog / recipes | [#2](https://github.com/canzheng/workflow-skills-test/issues/2) | Ready, unexecuted | [] |
| Owner dietary choice / dietary-policy | [#3](https://github.com/canzheng/workflow-skills-test/issues/3) | Backlog + blocked, exact choice remains unresolved | [] |
| Meal plan / meal-plan | [#4](https://github.com/canzheng/workflow-skills-test/issues/4) | Backlog + blocked | #1, #2, #3 |
| Shopping export / shopping-list | [#5](https://github.com/canzheng/workflow-skills-test/issues/5) | Backlog + blocked | #4 |

All IDs use the `pantry-planner:` prefix. The user's F14 launch already authorized
the evaluation batch and bounded ingredient execution; no separate approval click
or execution from readiness alone is invented. A subsequent open/closed search and
actual Issue collection read confirmed exactly these five unique identities and
consistent dependency URLs; no additional Issue was created. Human edits/rerun
contradictions are meaningful fixture proof in test_initial_backlog/test_records,
not claimed as deliberately induced live human edits. Fresh-task shaping rerun is
still required to establish independent continuation/discovery.

### Actual execution, Actions and review

Issue #1 was claimed with branch/base evidence, moved Ready → in-progress, and
implemented on its branch. Seven initial tests exercised actual CLI/storage:
oats500g/lentils300g, empty/zero, duplicate/invalid/malformed/missing/symlink,
denied staging, replacement interruption/retry and file-mode preservation.
Application argv verification was added to user-owned config. PR #6 began draft;
generic installed CI actually executed these project commands on GitHub runners.

| Actual event / tested head | Evidence and result |
| --- | --- |
| Bootstrap push, 5d055649 | [37207162368](https://github.com/canzheng/workflow-skills-test/actions/runs/37207162368): success |
| Implementation push, 382c5bc2 | [37207375910](https://github.com/canzheng/workflow-skills-test/actions/runs/37207375910): success |
| Draft PR, 382c5bc2 | [37207378478](https://github.com/canzheng/workflow-skills-test/actions/runs/37207378478): verification success; [37207378577](https://github.com/canzheng/workflow-skills-test/actions/runs/37207378577): trusted-base PR contract success |
| Body edit negative, 382c5bc2 | [37207571778](https://github.com/canzheng/workflow-skills-test/actions/runs/37207571778), job111451878303: expected failure, `pr.section` / Missing or empty Documentation section |
| Body restoration, 382c5bc2 | [37207626975](https://github.com/canzheng/workflow-skills-test/actions/runs/37207626975): success |
| Ready event, 382c5bc2 | [37207722331](https://github.com/canzheng/workflow-skills-test/actions/runs/37207722331): verification success; [37207722655](https://github.com/canzheng/workflow-skills-test/actions/runs/37207722655): PR contract success |
| Review-fix push, 9cf27f80 | [37208493878](https://github.com/canzheng/workflow-skills-test/actions/runs/37208493878): success |
| Review-fix PR, 9cf27f80 | [37208497635](https://github.com/canzheng/workflow-skills-test/actions/runs/37208497635): verification success; [37208495431](https://github.com/canzheng/workflow-skills-test/actions/runs/37208495431): PR contract success |
| Fixture-fix push, 2b4ecd69 | [37208863474](https://github.com/canzheng/workflow-skills-test/actions/runs/37208863474): success |
| Fixture-fix PR, 2b4ecd69 | [37208867389](https://github.com/canzheng/workflow-skills-test/actions/runs/37208867389): verification success; [37208865045](https://github.com/canzheng/workflow-skills-test/actions/runs/37208865045): PR contract success |
| Nested-data fix push, cec53770 | [37209327819](https://github.com/canzheng/workflow-skills-test/actions/runs/37209327819): success |
| Nested-data fix PR, cec53770 | [37209330624](https://github.com/canzheng/workflow-skills-test/actions/runs/37209330624): verification success; [37209329155](https://github.com/canzheng/workflow-skills-test/actions/runs/37209329155): PR contract success |
| Python-compatible schema fix push, 0b40f50e | [37209800631](https://github.com/canzheng/workflow-skills-test/actions/runs/37209800631): success |
| Python-compatible schema fix PR, 0b40f50e | [37209803102](https://github.com/canzheng/workflow-skills-test/actions/runs/37209803102): verification success; [37209801935](https://github.com/canzheng/workflow-skills-test/actions/runs/37209801935): PR contract success |

The PR became Ready before Issue #1 entered wf:review. It remains open/unmerged.
Independent native Codex review was requested at the Ready boundary through
[comment5980815385](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5980815385).
Bot review completed at 382c5bc2 on 2026-10-04T14:05:02Z, reporting two P2 findings:

- [Permission-loss cleanup](https://github.com/canzheng/workflow-skills-test/pull/6#discussion_r4177990682): reproduced denied replacement plus unlink masking the original error and leaving staging. Fixed best-effort cleanup to report both errors/path, documented recoverable residue, and added an actual unprivileged permission-revocation/recovery test (including a privileged-runner child dropping to UID65534).
- [Post-commit output failure](https://github.com/canzheng/workflow-skills-test/pull/6#discussion_r4177990683): an actual closed pipe exited120 after writing the new catalog. Documented the commit/output boundary and retry inspection; flushed output explicitly and added a real closed-pipe test asserting persisted data and duplicate retry rejection.

No original acceptance was weakened. Both fixes are at 9cf27f80, with nine local
tests and configured checks passing, no skips. Re-review was requested at
[comment5980926400](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5980926400);
review completed at 9cf27f80 on 2026-10-04T14:17:26Z and found one test-fixture
defect: root with umask077 created a0600 root-owned catalog, so its privilege-dropped
child failed before staging. A real Ubuntu root/umask077 negative reproduced this.
At 2b4ecd69, the child chowns both catalog and directory before dropping privileges;
application behavior and assertions are unchanged. Nine tests and configured
local/integration checks passed at that exact SHA in fresh Ubuntu with umask077,
alongside managed Cloud and GitHub runs. A final re-review was requested via
[comment5980979384](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5980979384);
the bot completed that review at2b4ecd69 on 2026-10-04T14:23:16Z and
[reported no major issues](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5981003869).
The three reproduced/remediated threads were replied to and resolved. This actual
review result does not waive the newly confirmed nested-JSON finding below, required
environment evidence, or independent final review of the rewrite itself.

### Cloud and Ubuntu evidence, with limits

Managed Cloud execution used Debian13/Python3.12.14. Production pinned setup,
doctor/check, actual skill reading/use, shaping/publication and ingredient execution
occurred here. The user supplied a separate consumer environment-onboarding chat;
its explicit reads/use and continuation are observed below, but fresh automatic
host discovery remains unproven. A prepared environment or an empty Start-skill UI
shortcut is not discovery.
Local `codex exec` and Cloud-task API attempts failed with proxy403 before model
execution; those failed attempts are not semantic/discovery evidence.

Actual fresh Ubuntu24.04.5 LTS remote clones at 382c5bc2, 9cf27f80 and 2b4ecd69 passed
the respective seven/nine/nine application tests and configured local/integration
verification, no skips; Python3.12.3, clean checkout and exit0. At 9cf27f80 the real
permission-loss test passed even though the container parent was root, because the
writer subprocess explicitly used an unprivileged UID. The pinned recipe/image is
recorded in [source acceptance](v2-acceptance.md). This proves Ubuntu portability,
not automatic skill discovery by an Ubuntu agent host or the user's private host.
The final 2b4ecd69 repeat used restrictive umask077, proving the fixture correction.

Docs reassessed/updated: consumer README, design references, docs/catalog.md
(CLI/schema/defaults/errors/examples, single-writer and crash durability limits,
cleanup residue and output commit boundary) and config verification. No prior
application specs existed; this bounded explicit CLI outcome needed no new OpenSpec
change, mandatory per-task plan or independent pre-PR review stage.

Still required under existing authorization: fresh Cloud task evidence and safe
rerun/continuation, Ubuntu agent discovery when that host is available, re-review
of the separately remediated nested-JSON finding, remaining representative fresh-host scenario obligations
and final rewrite-wide independent code/spec/doc review. F14 and the rewrite change
remain open; no archive or final completion is claimed.

### Earlier user-supplied Cloud report

The user supplied report-F14-before-fix.md from an earlier consumer continuation.
It reports clean adoption5d055649, successful Git fetch/selection of382c5bc2, explicit
reading/use of all three skills, seven baseline tests and eight tests after an
unpublished local repair64e5a4d7c1e37172aad7474fa52b0370e167e361. These are attributed
report results, not direct observations of that task's terminal or a published PR
revision. The supplied skill/method hashes exactly match the installed bundle here.

The report correctly separates filesystem reading/use from automatic host discovery:
its host skill catalog did not include the three skills and executor skills.list
returned empty. It also discloses that its context continued onboarding rather than
proving a fresh independent published task. Do not count this as F14 acceptance1.
Its safe one-shot MVP analysis retained all five outcomes/unknowns/exclusions, but
API proxy403 blocked live all-state identity/readiness reconciliation. Git reads
succeeded; reported CONNECT403 occurred before an API credential authorization
response, so supplying a token alone would not establish API network access.
The report says an api.github.com network draft was saved, not published/applied;
no effective environment change is inferred here.

Its nested-JSON finding was independently reproduced here on current2b4ecd69:
a10000-level invalid array causes show and add to exit1 with an uncaught
RecursionError traceback while preserving original bytes. This violates documented
actionable data-error reporting and was not fixed by the earlier PR review changes.
The report's local commit was not on the remote branch. Reading the user-supplied
Cloud thread01a1072e-11d1-72a1-aaf2-28f8b59af012, host durable, title
"Set up workflow-skills-test", directly confirmed its idle status, actual command
results and onboarding context. Its update fetched9cf27f80, preserved local64e5a4d7
on its branch, detached for verification and passed nine tests/configured checks.
It did not replay the nested-data repair. This is observed separate-context
continuation/verification, not a fresh task's automatic skill discovery or successful
API reconciliation. No active conflicting implementation was observed.

The confirmed nested-data fix was then implemented on the canonical branch at
cec53770c17f670615f8f3bd610bde70d424434c: decoder-only RecursionError becomes
an actionable flat-schema ValueError. An actual show/add regression failed before
the fix (two subtests), then all ten tests passed with preserved bytes, empty stdout,
no traceback/residue and original assertions intact. Docs now explain this invalid
input. Same-SHA managed Cloud, fresh Ubuntu root/umask077 and configured
local/integration verification passed; actual push/PR/metadata runs passed above.
Native re-review atcec53770 completed and found a Python3.14 decoder difference:
deep arrays can decode successfully and then received generic shape errors, missing
the promised flat-schema guidance. Actual Python3.14.8 reproduced the original
two failing regression subtests. At0b40f50e, existing root/value schema validation
provides flat-schema guidance independently of decoder recursion; no artificial
depth limit or support-range narrowing. The unchanged no-traceback/preservation
assertions now exercise actual show/add on deep arrays, deep amount values and
already decoded invalid root/value shapes. Ten tests pass on managed Python3.12.14,
fresh Ubuntu3.12.3 with root/umask077, and a separate Python3.14.8 container with
root/umask077 using the exact clean0b40f50e checkout mounted read-only. That container
is not claimed to be an Ubuntu/fresh-agent clone; observed image digest is
`python@sha256:c3e521df8b2b498a7a682e7e18676771cb80c6b75b8699af886b2d554ce40151`.
[Final native re-review requested](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5981120139),
That historical request found locale-dependent catalog reads, then surrogate-escaped
CLI IDs. Both were reproduced and repaired, with an actual ASCII-locale round-trip
regression retaining malformed/duplicate/unchanged-byte assertions. At
`f95f0cae3b87bc8031b00a4150cf9670251ae978`, all 11 tests pass on Cloud Python3.12,
fresh Ubuntu Python3.12 and actual Python3.14.8 under root/umask077. Current-head
Codex review [5981620802](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5981620802)
reports no major issues; all addressed inline threads are resolved. Actual push
[37213062645](https://github.com/canzheng/workflow-skills-test/actions/runs/37213062645),
PR [37213065265](https://github.com/canzheng/workflow-skills-test/actions/runs/37213065265)
and metadata [37213064024](https://github.com/canzheng/workflow-skills-test/actions/runs/37213064024)
pass. No unrelated backlog work is dispatched. The report's task-specific no-publication
limit is evidence about that task, not a new authorization instruction for this one.

## Pending authorization

1. **Real merge → completed Issue observation.** PR #6 is Ready, Issue #1 is open
   wf:review. No merge, completed closure or simulated merge/closure occurred.
   With later explicit authority, perform the real reviewed merge and observe valid
   Issue completion only after the remaining delivery contract is satisfied.
2. **Required-check/protection/ruleset configuration.** Read-only consumer rulesets
   returned403: Upgrade to GitHub Pro or make this repository public to enable this
   feature. Classic main protection returned403: Resource not accessible by
   integration. Neither proves classic protection is absent. Actual successful
   `v2 verification` and `v2 PR contract` jobs prove execution, not required-check
   enforcement or blocked merge. Do not change visibility, account plan, protections
   or rulesets without separate authority. An owner can inspect the existing state;
   any later mutation follows the [enforcement runbook](../workflow/checks.md).

Release publication and remote branch deletion also remain unauthorized; neither
is needed for the currently authorized pilot path.

## Exact next fresh Cloud action

Use the existing consumer environment and isolated checkout at
`/workspace/workflow-skills-test`, branch `pilot/ingredient-catalog`, full SHA
`f95f0cae3b87bc8031b00a4150cf9670251ae978`. Inspect/preserve changes, fetch and
confirm the actual head; if another task moved it, coordinate rather than reset.
Read AGENTS.md, workflow contract/index/config, docs/design.md, all three installed
skills, Issues #1–#5 and PR #6. Capture actual host-discovered names and actual use.
Perform an identity-safe one-shot design backlog rerun without duplicates, acceptance
rewrites or dispatch of #2–#5. Verify #1/remediation and native review state, run
configured verification, record exact revision/OS/results and post a handoff on #1.
Do not merge, close completed, change administration, publish or delete branches.
Source Issue #15 owns aggregate F14 acceptance; keep consumer and source SHAs distinct.


## Pinned ignored dependency refinement (S34)

The user subsequently approved tracked project policy/config plus tracked dependency
pin, with only shared skills materialized locally and ignored. The older application
pilot above does not prove that revised installation model. Independent infrastructure
outcome [Issue7](https://github.com/canzheng/workflow-skills-test/issues/7) was searched
across open/closed identities before creation and claimed Ready → in-progress.
New branch `pilot/shared-skill-bootstrap` from unchanged main5d055649 uses source pin
`47320c363e538d2c8423e11e5ca9121c2d0303da` and consumer SHA
`539580779e52eef5b976a0460d7d18e16833c2b0`.

Existing managed hashes were verified before migration. New setup refused tracked
shared files before writes; explicit index-only untracking of exactly three namespaces
preserved bytes. Setup then updated owned policy/tools/docs/CI/pin and added exactly
three anchored ignore rules. Project-owned `pantry-project` remains tracked. Config,
README/design, old application branch/PR and main were preserved. Repeated setup and
bootstrap each returned `changes: []`. The native published tree exactly matched
local Git tree `b3a090864684ccc388c4a277e384db1e28bfe357`.

Source47320c3 passed 62 tests with no skips and strict current/delta OpenSpec checks on
Debian Cloud and fresh Ubuntu24.04.5 clones; source Actions
[37213148746](https://github.com/canzheng/workflow-skills/actions/runs/37213148746) and
[37213152015](https://github.com/canzheng/workflow-skills/actions/runs/37213152015) pass.
An initial Ubuntu run without optional npm dependencies had two explicit skips;
the prepared repeat installed pinned tooling and passed all62 without skips.

Actual fresh consumer clones in Cloud runtime and Ubuntu lacked shared skills,
fetched the same pinned source via Git, materialized four pinned assets, passed
configured check/doctor, repeated bootstrap as a no-op and remained Git-clean.
All shared hashes and tracked project skill matched in both environments. The
consumer has no application implementation on this branch; default checks certify
workflow integrity only, not application acceptance or native agent discovery.

[PR8](https://github.com/canzheng/workflow-skills-test/pull/8) began draft. Actual push
[37213277277](https://github.com/canzheng/workflow-skills-test/actions/runs/37213277277),
draft PR [37213280986](https://github.com/canzheng/workflow-skills-test/actions/runs/37213280986)
and trusted-base metadata [37213281196](https://github.com/canzheng/workflow-skills-test/actions/runs/37213281196)
passed. Job111468589629 explicitly ran `Materialize pinned shared skills` successfully.
After self-verification/docs reassessment, PR8 became Ready before Issue7 entered
wf:review. Native semantic review was requested via comment5981635279; its result
must be read before claiming review completion. No merge/Issue closure occurred.

The exact published environment script and fresh-task prompt are in
[Cloud bootstrap handoff](cloud-bootstrap-handoff.md). Native pre-agent discovery/use
on a fresh Cloud task and Ubuntu agent discovery remain unperformed. Actual merge →
valid Issue completion and enforcement configuration mutations remain pending separate
authorization; runtime bootstrap and workflow checks do not substitute for them.

### Reviewed corrections and current pinned consumer

Subsequent independent consumer review found broad excludes hiding project skills
and negations exposing shared skills during setup. Both were reproduced against the
exact old consumer clone, then fixed at source133dcff with effective Git policy preview
before writes plus bootstrap/check/doctor validation. Consumer3b64cf re-review reports
no major issues (comment5981763538); addressed threads resolved.

Source ReadyPR16 review independently found incomplete installed runtime validation
and extra ignored assets reported clean. Failing-before public regressions confirmed
both; sourcecb2cde7 requires all seven runtime modules and marks unmanaged dependency
content dirty. Further source review found source-check completeness drift and an
external OpenSpec archive accepted through a symlink. Failing-before tests confirmed
both; source11fa051 shares runtime requirements and validates archive root/matches.
No original acceptance/assertions were weakened. Targeted final reviews were requested;
read actual results before claiming final semantic acceptance.

Current consumer branch `pilot/shared-skill-bootstrap`, SHA
`5efc5f5ffdcab46a440b2cb2237924ee476a5bd9`, pins source
`11fa051a7c4af359bd4728e1edf69cd8c7a61259`. Source68 tests/no skips, public check and
strict OpenSpec checks pass on Cloud Debian and fresh same-SHA Ubuntu24.04.5;
source push[37214817774](https://github.com/canzheng/workflow-skills/actions/runs/37214817774)
and PR[37214821507](https://github.com/canzheng/workflow-skills/actions/runs/37214821507)
pass. Consumer exact-head fresh Cloud-runtime/Ubuntu clones fetch that pin, materialize
four exact hashes, repeat changes:[], pass check/doctor and remain Git-clean with
project skill tracked. Actual consumer push
[37214896516](https://github.com/canzheng/workflow-skills-test/actions/runs/37214896516),
PR[37214899407](https://github.com/canzheng/workflow-skills-test/actions/runs/37214899407),
metadata[37214897768](https://github.com/canzheng/workflow-skills-test/actions/runs/37214897768)
pass. No merge/completed closure/admin mutation occurred.

The user clarified that environment setup must handle a brand-new repo without tools.
The [unified published setup script](cloud-bootstrap-handoff.md) now fetches an exact
seed/adopts only when no tracked manifest exists; otherwise it bootstraps the existing
pin. The exact script passed on a new Git checkout without tools, then repeated with
no fetch/file changes; tools and pin are trackable, shared skills ignored. Generated
adoption files must be reviewed/committed. This proves the script's behavior, not the
host's preparation persistence/ordering or initial agent discovery. Those remain the
fresh published Cloud gate. Ubuntu agent discovery is also unperformed; merge→Issue
completion and enforcement mutations remain separately pending authorization.

### Current unified environment entrypoint

Source `7e71186ec8146b682f4c4cf40c8da5ecb6d3f608` also closes validated installed
manifest completeness and ledger-symlink gaps. Both have failing-before public tests;
all70 tests/no skips and strict checks pass on Debian Cloud and fresh Ubuntu24.04.5.
Source push[37215771822](https://github.com/canzheng/workflow-skills/actions/runs/37215771822)
and PR[37215776553](https://github.com/canzheng/workflow-skills/actions/runs/37215776553)
pass. Partial uninstall provenance is preserved for recovery; diagnostics no longer
mistake it for a complete installed bundle.

Consumer current branch `pilot/shared-skill-bootstrap`, SHA
`79efd96276e25e2c1a706a3c7972dbebf32d2a0a`, pins that exact source. The real project-owned
`.workflow/cloud-setup.sh` and README expose the same complete pastable environment
command. It was executed against a new Git root without tools: pinned fetch/adoption
succeeded; repeat skipped fetch, changed no file/index and returned bootstrap changes:[].
Exact-head fresh consumer clones on Cloud runtime and Ubuntu both ran that actual
script twice, matched pinned shared hashes, kept project skill tracked and remained
Git-clean. Consumer push
[37215967922](https://github.com/canzheng/workflow-skills-test/actions/runs/37215967922),
PR[37215972442](https://github.com/canzheng/workflow-skills-test/actions/runs/37215972442),
metadata[37215970011](https://github.com/canzheng/workflow-skills-test/actions/runs/37215970011)
pass. These are script/runtime/CI results, not native pre-agent skill discovery.

Consumer review's stale README omission was confirmed and fixed. The request to make
workflow.py bootstrap implicitly adopt an absent pin was not accepted: an entirely
unadopted repo has no CLI. The standalone environment script performs pinned fetch
and adoption before invoking CLI, while repeatable bootstrap retains its approved
pin-only/project-preservation contract. Review replies provide actual script evidence;
the concrete project-owned entrypoint removes the earlier visibility ambiguity.
Final current source/consumer review outcomes remain required and must be read.

Use the latest [Cloud handoff](cloud-bootstrap-handoff.md), publish/apply the full
command in environment setup/maintenance, select the current consumer branch/SHA,
and start a genuinely new task outside onboarding. Capture initial host discovery
before agent-side installation. Generated adoption files must be committed in a
new project; this pilot has already committed them. Ubuntu agent discovery, remaining
fresh-context scenario/semantic acceptance, real merge→Issue completion and admin
mutations remain separately pending. No merge or completed closure is simulated.

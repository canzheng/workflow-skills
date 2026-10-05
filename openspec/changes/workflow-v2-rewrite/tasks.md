# Rewrite implementation and acceptance

- [x] 1. Establish repository-scoped foundation (WF2-F01–F06).
- [x] 2. Implement specifications, risk proof, handoffs, checks and scenarios (WF2-F07–F11).
- [x] 3. Inventory migration and retire active v1 assets (WF2-F12–F13).
- [ ] 4. Complete required Ubuntu skill-use/runtime/GitHub/review/enforcement acceptance and archive (WF2-F14).

## Bootstrap checkpoint evidence

2026-10-04: F01 instruction cutover implemented from clean baseline
`d2aaf1904b2ccbe7fbab9733627e9c82fcf12f53` on `rewrite/workflow-skills-v2`.
Inventory inspected: 19 historical Done, zero active entries; unrelated style/testing/
commit constraints preserved. CLI GitHub authentication unavailable; connected-tool
search succeeded with no WF2 matches. Publication will be reconciled at F04.
Next: F02 portable environment, then F03 safe setup/doctor.

F01 tested at `6e6fffc`: instruction-chain comparison and baseline preservation;
focused routing regressions now pass in F02. F02 tested content: portable runner,
pinned optional pytest dependencies, config command and development guide;
`/tmp/wf2-clean-venv/bin/python tools/workflow/verify.py`: 3 tests passed;
missing-suite negative control fails for the intended reason. Clean venv install
and rerun succeeded (pytest 8.4.2). Docs: development/index/config. Actual fresh
Cloud discovery remains pending. Next: F03 public setup/doctor negative paths.

F02 committed at `35c0970`. F03 implemented public setup/doctor and minimal
provenance/config validators; tested working content with 10 offline tests
(`python3 -m unittest discover -s tests/v2 -v`). S01/S03/S05 fixture paths pass,
including source mismatch, user-owned config, duplicate skill discovery, missing
Git root, spaces and rollback. Production assembly deliberately incomplete until
F05/F06/F08/F10/F12 assets exist. Documentation: operations, consumer guidance,
bundle manifest and architecture-to-be. Next: F04 templates and Issue reconciliation.

F03 committed at `4bc7590`. F04: feature/bug forms, PR evidence template,
GitHub lifecycle guidance, deterministic catalog rendering and snapshot helpers
implemented. 14 tests pass (S06/S07/S23 include closed-ID reuse, duplicate rejection,
phase/modifier/cancel/reopen representation and compare-before-update). Source-ID
search across states returned no WF2/rewrite-parent matches. Connected-tool
repository read succeeded; parent create returned GitHub HTTP 403 Resource not
accessible by integration. No Issue number, write, label or parent creation is
claimed. `/tmp/wf2-issues.json` is reproducible via records.py, not a state store.
Docs: docs/workflow/github.md and forms/template. Next: F05 skill and sample shaping.

F04 committed at `6639c66`. F05 skill authored/read and exercised on the receipt
shaping input; actual candidate artifact is the S08/S09 table in
`docs/validation/skill-evaluations.md`. Unknown retention isolates its decision;
no excluded enhancement authorized. 14 regression tests pass; semantic exercise
is primary-author, not a fresh discovery run. Docs: usage and evaluation record.
Next: F06 deliver skill and actual feature/bug fixture outcomes.

F05 committed at `2f112c1`. F06 implemented/read deliver skill, ran actual cart
bug/ordinary-feature fixtures, preserved quantity expectation and invalid cases,
completed shipping default/error/example docs, and accepted no-impact for contract
restoration. 16 tests pass; primary-author semantic exercise in skill-evaluations.
Evidence belongs to current dirty content until this feature commit; no merge,
remote write, independent review or fresh Cloud discovery claimed. Next: F07 pinned
OpenSpec validation/archive fixtures and current implemented contracts.

F06 committed at `25b570c`. F07: OpenSpec 1.14.0 pinned/installed, supported commands
inspected, actual disposable validation/archive executed and current implemented
adoption/delivery specs added. 18 tests pass plus strict v2 spec validations.
Initial archive fixture failed because CLI-generated Purpose was placeholder/too
short; corrected the actual delta Purpose rather than weakening strict validation.
Partial fixture keeps unchecked work active; CLI structural validation cannot itself
prove acceptance. Current six legacy specs remain until F13 reconciliation, so no
all-spec v2 consistency claim yet. Docs: OpenSpec procedure/development/index;
rewrite delta retains pending F14 gates. Next: F08 risk methods and negative controls.

F07 committed at `65a01a9`. F08 implemented/read targeted risk skill and concise
L-001/L-002 references. 21 tests pass; deliberately wrong arithmetic, parser-only
currency consumer and weakened quantity expectation fail for their intended reasons.
Missing target/apply interruption tests retained. Documentation: risk methods,
primary-author findings and residual independent/fresh-host review limitations.
Next: F09 same-content handoff and native-operation fault fixtures.

F08 committed at `13f1bc8`. F09: doctor reports full revision/branch/dirty/content
digest and checks expected target/content without fallback. 24 tests pass, including
missing worktree, stale branch/revision, changed dirty content, creation response
loss reconciliation, repeated identities, permission loss and human edits. Remote
fixtures are explicitly fixtures; real connected-tool reads/403 write remain separate.
Docs: handoff/evidence/capability failure guide. Ubuntu/fresh Cloud acceptance pending;
this host is Debian 13, not Ubuntu. Next: F10 executable checks/trusted CI metadata.

F09 committed at `a3c5dc2`. F10: public check validates schemas/source-consumer
integrity/current links/anchors/PR sections and read-only Issue inconsistency
snapshots. Trusted-base metadata uses head Git blobs as data with read-only
permissions; body/head event coverage and injected shell/executable strings tested.
31 tests and source public check pass. Actual Actions and merge enforcement pending;
no repository settings changed. All-spec check remains intentionally sensitive to
legacy current contracts until F13 removal (never claimed passed). Docs: checks/
runbook/architecture/index. Next: F11 real bundle consumer/scenario proof.

F10 committed at `c36a85d`. F11: actual pinned production bundle installs, no-op
rerun works and installed checker executes; exactly three skills, no _workflow
runtime. Cross-module receipt CLI produces EUR 7.47 and denied quantity exits 1.
34 tests/public source check pass. Semantic omission/contradiction/no-impact outcomes
recorded as primary-author exercises, fresh-host triggering/independent review pending.
Docs: scenario corpus and actual evaluation records. Connected app was updated by
the user; a fresh identity search preceded successful parent Issue #1 and WF2 feature
Issues #2–#15. Read/write restored; no token captured. Subsequent shared lifecycle
uses GitHub; this existing plan retains technical acceptance evidence only.
Next: F12 read-only known-format migration, then F13 active runtime retirement.

F11 committed at `49f8543`. F12 implements read-only known v1 inventory, preserving
original acceptance/evidence/blockers, explicit proposed dispositions and findings
for malformed, duplicate, missing, unsafe or inconsistent records. Focused migration
fixtures pass; actual source inventory is 19 historical Done and zero active.
Interrupted-cutover fixtures reuse old IDs and preserve human edits. Docs: migration
cutover/rollback runbook, current architecture and implemented migration spec.
No historical Done Issues created; no consumer/global cutover performed. Live feature
records now own shared state. Next: F13 removal/reconciliation and full v2 checks.

F12 committed/tested at `dfaae09`: 40 tests and public source check passed. F13
retired active v1 skills/runtime/global installer/Conda launcher/ceremony tests and
six obsolete stable specs; history remains labeled/read-only and baseline reachable.
Final code inspection strengthened filesystem preflight/recovery and provided an
actual argv verification consumer (including failed/missing runtime paths), not
parser-only config. Focused checks and strict current spec validation pass; real
bundle regression reruns require the committed bundle bytes. Docs reconciled:
README, routing/index, architecture, development/operations, history labels,
asset/test disposition and current quality spec. Rewrite remains active for F14.
Branch publication through Git succeeded without exposing CLI credentials; remote
feature Issues exist. Next: committed full-suite rerun and F14 Ubuntu/Actions evidence.

F13 first implementation tested at `34b5e66430b58539bf98330701f0ccda908a4e0e`:
47 tests, public check and strict specs passed; branch pushed and draft PR #16 opened.
Main then contained human-approved cleanup clarifications at
`e5747944a7e0520cf766db263834c8485fe63012`; integrated them without resetting the
starting revision. F13 follow-up removes all v1-only in-tree history/archives,
updates current docs and accounts for every baseline path in an exhaustive asset
manifest. Prior "labeled history retained" records describe intermediate revisions,
not final source behavior. Fresh clone checks and baseline inventory regression
will be rerun at the cleanup commit. Next: F14 same-revision Ubuntu/Actions and
fresh Cloud discovery/required enforcement handoff.

F13 cleanup verified at `0363702b5b6f79a619eb70e5c53215eb2ca559eb`: 49 tests
and strict specs passed on this managed checkout, a fresh Ubuntu 24.04 remote clone,
and Actions. Cross-filesystem clone failures were repaired with copying clones.
Final consumer/archive proof and shaping artifacts verified at
`bbbf1e5e5df860dbb3eca2ebfad1377f39159348`: 49 tests, public check and strict
specs passed on both environments; Actions run 37204546568 succeeded.
F01–F13 implementation is ready for review, with host/integration limits retained.
F14 remains partial: fresh Cloud discovery/resume, independent review and observed
merge enforcement are pending; trusted-base metadata requires base adoption.
See docs/validation/v2-acceptance.md and native Issue #15 for exact continuation.
Do not archive or close the parent while required acceptance remains pending.

Validated user-supplied reviewer comments against approved design/actual bundle:
consumer CI absence confirmed, normal Ready-PR review boundary refined with fallback,
optional phase automation deferred and no closure bot. At
`3386d008f809d32ebc6cf4f849b47750845c1cb6`, 51 tests, public check and strict specs
passed on Cloud checkout and fresh Ubuntu clone; Actions37205386850 succeeded.
Consumer live CI and Cloud/Ubuntu agent discovery remain distinct pending gates.
No merge/protection authorization was inferred from the review. Final report links
all feature acceptance and scenarios; Issue15 owns the explicit final-SHA handoff.

User-authorized one-shot initial/MVP backlog refinement tested at
`139e66d5b43cfbd3821fe098c0119b93aaad4928`: 54 tests, strict current/delta specs
and public source checks passed on managed Cloud and fresh same-SHA Ubuntu clone;
Actions37206519129 succeeded. Docs/specs/skill/corpus updated together for S33.
Real consumer canzheng/workflow-skills-test adopted that pinned bundle; five Issues
published with actual prerequisite URLs, explicit unknown and no task explosion.
Issue1 was selected/claimed, implemented, published in draft PR6, then made Ready
before wf:review. Actual generic push/PR and trusted-base metadata passed; removing
Documentation produced its intended pr.section failure, restoration passed.
Independent native Codex review found two reproducible failure-path/doc issues;
both fixed at consumer `9cf27f803dd5cc2dc8b1ffbd12fe8fc643602fc6`, nine tests pass
on Cloud and fresh Ubuntu, consumer Actions pass. Re-review found/reproduced one
root/umask077 test-fixture defect, corrected at consumer
`2b4ecd69a3455e6fb3bd8744537a23ed5dd3071e`; same-SHA Cloud/Ubuntu restrictive-umask
and GitHub verification passes with original assertions. Final native re-review
completed at2b4ecd69 with no major issues reported; the three addressed threads are
resolved. An earlier user-supplied Cloud report's separate deeply nested JSON
traceback was reproduced on2b4ecd69, then remediated at consumer
`cec53770c17f670615f8f3bd610bde70d424434c` after reading the supplied task and
confirming it idle. Ten actual tests pass on Cloud/fresh Ubuntu root/umask077 and
real push/PR/metadata Actions. Re-review found/reproduced Python3.14's successful
deep-array decoding; at consumer `0b40f50ee12b3c07d0df9b15e93a0ef0a0b56b84`,
root/value schema errors state the flat contract independently of recursion. Ten
tests retain assertions and cover decoder-accepted shapes; passed on Cloud3.12,
fresh Ubuntu3.12 root/umask077 and actual Python3.14.8 root/umask077. Actual push/PR/
metadata passed; final targeted re-review pending. The linked task's observed
9cf27f80 continuation preserves local-only work, but is still onboarding context.
It is not fresh automatic discovery evidence; a separate fresh consumer task
remains required after supported environment/network draft publication by the user.
See docs/validation/f14-consumer-pilot.md for exact branches, runs and continuation.
F14 remains unchecked: preserve required fresh-host/scenario/final-review gates;
real merge/completed closure and administrative mutations are separately unauthorized.

### Narrow consumer dependency refinement

User-approved ownership clarification: keep project policy/config/utilities/CI/docs
and project-specific skills tracked; pin shared skills in the tracked installation
manifest and materialize only the three ignored namespaces. Setup adoption owns the
scoped ignore block; repeatable bootstrap preserves project files/index. Focused
clone, idempotence, preservation, hash/fetch/unsafe-path and rollback tests are added.
Full-head verification and real revised-model CI/Ubuntu/fresh Cloud discovery evidence
must be recorded before claiming those gates. F14 remains incomplete; merge/Issue
completion/admin mutation remain outside current authorization.

Refinement implementation tested at source47320c363e538d2c8423e11e5ca9121c2d0303da:
62 tests/no skips and strict specs pass on Cloud/fresh Ubuntu; source Actions pass.
Real consumer Issue7/ReadyPR8, branchpilot/shared-skill-bootstrap,
SHA539580779e52eef5b976a0460d7d18e16833c2b0, pins47320c3. Fresh Cloud-runtime/Ubuntu
clones materialize identical hashes, repeat no-op, preserve tracked project skill and
Git clean; actual CI bootstrap/push/PR/metadata pass. Native review requested, read
result before claiming completion. AppPR6 atf95f0cae3b87bc8031b00a4150cf9670251ae978
passes11 Cloud/Ubuntu/Python3.14 tests, final Codex review no major issues; addressed
threads resolved. Exact fresh published Cloud script/prompt is documented in
 docs/validation/cloud-bootstrap-handoff.md. F14 stays unchecked until actual fresh
host discovery/use and other required gates; merge/admin mutations need separate authority.

Current consumer/source checkpoint: pilot/shared-skill-bootstrap at
5efc5f5ffdcab46a440b2cb2237924ee476a5bd9 pins source11fa051a7c4af359bd4728e1edf69cd8c7a61259.
Source68 tests/no skips and strict checks passed on Cloud/fresh Ubuntu; actual source
and consumer CI passed. Source/consumer PR review findings were reproduced and fixed
with meaningful negatives; latest requested semantic results are not assumed passed.
Unified environment script now handles absent tools/pin by exact seed fetch/adoption,
then repeats via tracked-pin bootstrap with no fetch/file changes. Exact tested script
and fresh task prompt are in docs/validation/cloud-bootstrap-handoff.md. F14 remains
unchecked: actual fresh published Cloud pre-agent discovery/use, Ubuntu agent discovery,
remaining required scenarios/final semantic acceptance and actual enforcement evidence
remain distinct gates. Merge→valid completion/admin mutation need separate authorization.

Current checkpoint: executable source b1fe9e0242753db54cc16dfc8768502eb74cb3ea
passes81 tests/no skips and strict specs on Cloud/fresh Ubuntu24.04.5; source push
37251965903/PR37251969459 pass. Git replacement-ref finding was independently
reproduced/fixed; public canonical-object setup/separate-clone bootstrap preserve
instructions/index/local refs. Source Code Review5986640964 reports no major issues.
Consumer pilot/shared-skill-bootstrap now at fd4bf175e7b2ea22439511fdfef872ce8bc7c743
pins that same source. Local check/doctor/no-op, fresh Ubuntu actual README fetch/run
twice, hashes/index/tracked-byte preservation and push37252506795/PR37252510994/
metadata37252507928 pass. Consumer current-head review5986706572 reports no major issues.
Uploaded reports retain their historical f31/ef24 identities. They strengthen
runtime/CI proof but do not expose automatic consumer Start/discovery. User-supplied
Start text required pilot HEAD while forbidding selection from initial older main;
author corrected pilot-only safe routing/markers in the handoff. Generic consumer
startup stays branch-agnostic and uses its tracked pin. The selected retry now uses
Install script, publish/apply and the fresh mini diagnostic; Start is unnecessary
for this service-free pilot. The exact documented Install command passed in fresh
Ubuntu24.04.5/Python3.12.3/Git2.43.0: approved pilot selection, pinned fetch, all20
hashes and repeated tracked-byte/index preservation. Dirty-checkout and ignored
project-skill collision negatives preserve user bytes, HEAD and index on refusal.
Need actual Cloud Install output/exit, publication persistence and initial host
catalog before manual bootstrap/file reads; local command success does not prove
those gates. Limited main summary reports protection disabled; authoritative admin
reads denied, enforcement not proven. F14 stays unchecked/change active. Cloud/Ubuntu
agent-host acceptance and real merge→valid Issue completion/admin mutation remain
distinct; merges/closure/admin changes require separate authorization.


Latest Install-only diagnostic transcript still starts on work/oldmain5d05564919c55f1d4d0c2e1e020ad914252a2979,
pin139e66d5b43cfbd3821fe098c0119b93aaad4928; old-bundle check passes, expectedfd4 doctor
fails, no initial workflow metadata or Install output, no recovery; preservation
passed as reported. Independent old-commit reads confirm schema1 pin and three skill
sizes. Need saved Install command/publication log/exit before retry; distinguish
preparation from later checkout replacement and configured host cwd/root routing.
A separate Ready PR review's expected-HEAD dirty-manifest gap was reproduced in
Ubuntu and by a failing-before public-command regression; pilot guard now runs before
HEAD selection. Source-owned generic installer/bundle and consumer/source pins remain
unchanged. F14 stays unchecked/change active; exact new-head verification/CI/review
are recorded remotely after testing. No merge/completion/admin mutation authorized.

The user cannot obtain Install log/exit from the UI. The pilot handoff now captures
attempt stdout/stderr, exit and prepared revisions outside Git; mini reads the
receipt after initial catalog capture. This is temporary diagnostic evidence;
receipt persistence, freshness and actual pre-agent discovery are still to test.
Next: publish/apply the capturing command, then use updated mini without recovery.
The public-command regression verifies successful and refused attempt receipts,
user bytes and raw index preservation; no generic distribution/API change or repin.

Additional persistent-artifact feedback is applied as install-info.json with
timestamp, requested/fetched installer revision, initial/prepared consumer revision,
actual workflow pin, three-skill assertions and log hash. Both successful and refused
attempts get diagnostic receipts outside Git, keeping scoped ignores/idempotence.
The linked Learn page returns CONNECT403 here; lifecycle guarantees are not inferred.

Final capturing command SHA256 b1177ebfb4218ce9bd5e7ac33cf1f3ce628bdcbf57515e628fa74c4e1dcde421:
all82/no skips and strict specs pass on Cloud and fresh Ubuntu owned-source copy;
actual consumer clones pass receipt identity/hash, all20 assets, repeat/no-op and
expected/old-HEAD dirty and ignored-file refusals preserving bytes/raw index/HEAD.
First read-only bind failed Git ownership; disposable owned copy resolved it without
global trust changes. Publication persistence/discovery remain separate pending gates.

### User-approved tracked skills refinement — 2026-10-05

Starting source commit ead664a722b040e144c44c431bfe4488c36d7c88. Shared skills now
belong to committed consumer snapshots with schema-3 exact source provenance. Setup
performs explicit adoption/update; migration removes only its verified owned ignore
block. Bootstrap is read-only compatibility verification; CI verifies checkout files.
Current specs, approved F03/S34 and F14 instructions follow the new model. Earlier
ignored dependency/receipt checkpoints are historical. Verification/pilot migration
are pending at this checkpoint; F14 remains unchecked, no merge/archive/closure.

Tracked-model executable checkpoint 5615fc3f488edc41079dd60085440f0f265146f9: all79 tests/no skips and strict specs
pass on Cloud/Ubuntu; actual source push37267258851/PR37267263959 pass. Final consumer
6b9eb5d9fb8d2787544f962483e20e63c52f7231, source pin5615fc3, has all4 shared files committed and all20 hashes matched
before any hook. Fresh actual clones on both runtimes pass check/doctor/read-only
bootstrap twice, preserving tracked/index bytes and failing missing assets without
repair. Consumer Issue7/PR8 reuse actual draft→Ready/wf:review, push/PR/metadata
83424a5 pass. Final README-only CI/review are being observed. Old receipt latest
symlink P2 independently reproduced; the writer is removed in the current model and
thread resolved. Current independent review pending. Fresh host catalog and Ubuntu
agent-host discovery remain unperformed; required enforcement reads403. F14 stays
unchecked, change active; merge/completed closure/admin/release require authorization.

Read-only enforcement follow-up: source Active Protect-main24457981 targets main,
blocking deletion/non-fast-forward only, no bypass actors or required-check/PR rule.
Consumer has both observed v2 contexts; source metadata context is absent until
trusted-base adoption, so runbook stages that requirement after actual execution.
No settings changed. Final3a3b6d3 tests/strict specs pass on both runtimes, source
push37267764301/PR37267770064 and consumer6b9eb5d push37267653526/PR37267656824/
metadata37267655273 pass. Independent new review acknowledged but still pending.

### Public consumer enforcement and validated tracking reviews — 2026-10-05

Starting sourceebcdc8ff3df909c08108b0651fccc526891b6e4d; consumer6b9eb5d unchanged.
User made consumer public. Read-back Active ruleset24484016 targets main and requires
v2 verification/v2 PR contract from GitHub Actions15368, no bypass, strict:false,
other PR/conversation/deletion/force-push rules absent. Actual metadata-negative
37269275157 fails missing Documentation/exit1; PR8 reports blocked. Exact body restore
37269365402 passes and PR reports clean. No merge/closure/admin mutation by this task.

New source4180988644 and consumer4180982685 reviews were independently reproduced:
19 non-skill/policy tracking cases, ignored required paths and partial staging bypass
passed before repair (26 focused failing assertions); an additional initial ignored
manifest public check regression failed on a disposable original-source copy. Repair
requires all manifest assets/provenance/config/AGENTS indexed once any managed asset
is indexed/committed; initial unstaged review only allows trackable complete adoption.
Ignore preflight includes all required paths and ancestor rules. Four regressions cover
all23 paths, ignored/nested policy/runtime/docs/CI, unstaged ignored provenance and
partial staging, preserving files/raw index. Current verification/repin pending here;
F14 stays active/unarchived, fresh host discovery/merge-completion remain pending.

Validated review checkpoint: executableaceba7143652ba127dbc62c98608e1b9943be31d passes all83/no skips and strict
specs on Cloud/Ubuntu; source push37269711408/PR37269717386 pass. Consumer0e3fbc530f21c4981230a5ef968eac2a5dda3d5e
pins it, preserves project/index, fresh clones on both runtimes pass all20 hashes,
repeat/no-repair and provenance/config/AGENTS/runtime/CI untracking negatives.
Consumer push37269841401/PR37269845466/metadata37269843410 pass. Both source4180988644
and consumer4180982685 findings validated before repair, replied/resolved. F14.6
consumer enforcement configured/observed via user-public visibility and Active24484016,
actual missing-doc failure37269275157/blocked then exact-restored37269365402/clean.
No merge/closure/administration by this task. Fresh host/current final review/merge
completion remain pending; next exact diagnostic uses consumer0e3fbc530f21c4981230a5ef968eac2a5dda3d5e/sourceaceba7143652ba127dbc62c98608e1b9943be31d.

Submitted Cloud diagnostic follow-up2026-10-05 (Pasted text.txt SHA256
eeffe3cc30c3dfc83305b135618c58cb8ce760745aa77c2d6e3ae4abcf0ad6ca): requested
consumer0e3fbc53/sourceaceba714, actual branchwork/main5d055649/source139e66d5/schema1.
Old bundle integrity passes; expected-revision doctor fails;25 tracked files and raw
index unchanged. Initial configured/shell cwd/workspace, no matching consumer project
exposed,55 plugin skills/no workflow entries, executor empty, full repository catalog
unavailable. All4 skills already committed on main with identical pilot blobs, so
default-branch absence is not explanatory. Record as supplied evidence, not live
session inspection or proven Cloud root cause. Resolve initial project/checkout
routing before another diagnostic; no installer/global copy/merge workaround.
F14 current-revision discovery/use stays unverified; current runtime/CI/enforcement
evidence is unaffected. Updated published-run record, handoff and acceptance docs;
source707bc410 at start, managed executable pinaceba714/consumer0e3fbc53 unchanged.

Source Ready-PR review follow-up: reproduced staged-index bypass before accepting it
(28 new focused failures on original code). Added canonical blob/mode validation of
staged provenance/config/document paths/managed hashes/AGENTS independently from
working files, without index writes. Valid project policy differences and a coherent
schema-1 snapshot during explicit update remain supported. Four regressions cover23
corrupt staged paths, symlinks/unmerged stages, invalid schemas/document references
and valid policy edits. Focused18 tests pass; full source/Ubuntu/CI verification pending
before final claims. Current consumer0e3fbc/sourceaceba714 stays frozen while the user
runs fresh-environment discovery; consumer repin/integration remains separate.
User confirmed repo-only environment selection; official current Cloud docs do not
document a branch selector in the published-environment flow. Handoff now distinguishes
main discovery baseline from exact current schema-3 acceptance without an assumed UI.

Validated staged-candidate source a4eb9f1303d80cc18f83b5bbd734063cac03b9c3:87/no skips
and strict specs pass on managed runtime/Ubuntu24.04.5; actual source push37271835612
and PR37271841711 pass. Finding4181125358 replied/resolved. Actual consumer0e3fbc53
fresh clones updated only in owned temporary copies pass installed CLIs and five
staged corruption negatives preserving user config/skills/raw index; local fixture
commits61a8237de8a2534f00597a55abb96294a17d30e9 and9a1e5062628e93360d9f332f4d41f6503ad0ba2b
are not remote integration or host discovery. Live pilot/source pin stay unchanged
while the user compares a newly published environment. Next: collect that report,
then explicitly repin current consumer to verified repair, run actual CI/current
semantic review, and preserve any host routing/branch-selector limitations. Source
docs/specs/evidence updated; F14 active/unarchived. No merge/closure/admin/global change.

Recreated-environment supplied report SHA256d58e8524af55f6c08daf7e1dbedb857918b4a9eaba398de7e0be001a46a94d40
reproduces old-main5d055649/source139e66d5/workspace root/55-plugin/no-workflow catalog
absence with intact tracked/unignored skills, integrity pass/expected-pilot failure
and unchanged25 files/index. Different environment identity, same observation; full
repo discovery catalog/project root unavailable. No more env recreation/install
redesign recommended without host root/catalog/checkout evidence. F14 host gate blocked.
Consumer4181129303 independently reproduced on old installed CLIs: real owned source
doc update/staged-new-manifest only passed check/doctor/bootstrap; fixed CLI fails
the same snapshot and complete staging passes. Added partial-manifest and intent-to-add
regressions; focused20 tests pass, full enlarged suite pending.
After diagnostic completion, actual consumer updated to f6394326cd410b82567b8fea76bfd5c44fa9261a,
sourcea4eb9f1303d80cc18f83b5bbd734063cac03b9c3, identical local2a3f2c3/server tree4e5d8ec,
guarded non-force publication; project config/AGENTS/ignores/skills/raw index preserved
before caller staging. Actual fresh runtime/Ubuntu clones match20 hashes, repeat
verification/read-only bootstrap and reject missing/untracked/corrupt-staged/partial
provenance without validator writes. Actual push37272954548/PR37272958814/metadata37272957270
pass. Documentation/handoff/evidence updated; current semantic review and host routing
support remain pending, separate merge/completion/admin authorization unchanged.

Final source test/evidence b0323c903901bc33fb16a144aec413f3b31ff087 passes89/no skips
and strict specs on managed runtime/Ubuntu24.04.5; executable pin remainsa4eb9f1.
Actual source push37273309768 passed; PR37273314869 running when recorded. Actual
consumerf639/sourcea4eb fresh clone/repeat/negative proof and all3 Actions pass.
Both staged review threads replied/resolved; source review5989224524 failed with
unknown-error5989241655, so retry/current semantic outcome remains pending. Next
fresh Cloud task: continue from recorded source branch/consumerf639 and complete
authorized remaining checks using repo-local skills, reporting manual fallback
separately. For automatic discovery, host support/debugging must establish root,
repo catalog and pre-agent checkout controls; do not reinstall/recreate/merge as
an inferred fix. F14 stays blocked/active; no merge/closure/admin/global changes.

Additional native-host subset: existing Codex CLI0.159.0-alpha.3 app-server initialize
and skills/list (explicit cwds/forceReload) recognize3 workflows+pantry with repo
scope/enabled/no parser errors at consumerf639 Git root on managed runtime/Ubuntu24.04.5;
parent-root controls find none. Real fresh old-main5d clone recognizes its3 identical
workflow files at repo root; parent none. No model/thread, manual file read by probe,
workflow global install or config/index/tracked mutation. Existing CLI binary mounted
read-only in disposable Ubuntu container. Evidence stored in published-run/acceptance/
handoff. Ubuntu native CLI catalog subset verified; Ubuntu skill execution and
Cloud initial catalog/use still pending. This strengthens host root lead but does
not prove current Cloud implementation/root. No reinstall/main merge inferred fix.

## User-approved acceptance/storage refinement — 2026-10-05

Resume starts at source1f6aba5dcc4b0e9e801b638fd6eafc48b3f437bb. Ubuntu workstation
is the required F14 host; Cloud is deferred, historical reports retained unverified.
Shared consumer skills are ignored exact-pin schema-4 dependencies; setup owns only
three ignore entries, bootstrap materializes missing canonical bytes before agent/CI,
and matching repeats preserve project files/index offline. Tracked compatibility
regressions remain. Optional explicit global shared-only install-skills defaults to
~/.agents/skills and is tested only in isolated targets. Current/delta specs and
source/consumer docs are reconciled. Aggregate/committed Ubuntu/actual CI and real
consumer migration are being verified; Ubuntu fresh agent use/final review and
separately authorized merge/completion remain pending. No archive/global/admin change.
Next: record exact tested source/consumer pins in the Ubuntu workstation handoff.

Verified refinement checkpoint: source `a75c3f20e5f4032568b1d1a5cb17d001fc781918` all107/no skips and strict
specs pass managed runtime/Ubuntu24.04.5, actual source push37280549959/PR37280555919
pass. Consumer `9bd23d72dc24a741d669c1ea92532f8bf337aa42` pins it; actual push37280700304/PR37280704952/
metadata37280702909 pass. Fresh actual clones materialize4 ignored/untracked skills
from exact pin, match20 hashes, preserve tracked/index bytes and repeat offline/no-op.
Native Ubuntu catalog recognizes3 skills at root; parent negative passes, no agent
invocation claim. Isolated global installer tests pass; actual global home unchanged.
Non-UTF-8 reviewer finding4181357146 reproduced then repaired; public both-storage
regression preserves bytes/index, thread resolved. Required fresh Ubuntu agent use
and final review remain pending; Cloud deferred, real merge/completion/admin/release
requires separate authority. Next: user workstation run from ubuntu-workstation-handoff.


## Actual Ubuntu agent acceptance and review repair — 2026-10-05

Independent user session at consumer9bd23d72/sourcea75c3f2 on Ubuntu26.04/Python3.13/
codex-cli0.160 supplies native initial3-skill catalog, actual delivery/risk/backlog
use and no-chat continuation. Prepared/fresh index hashes unchanged, five MVP
identities/phases/dependencies reconcile without writes/default invention.
Two Ready-PR findings independently reproduced: consumer4181927560 setup mutation
before schema4 tracking rejection; source4181938333 staged nested ignore policies
read from working tree. b5b8da40eef689852bdc3d7dfd644eeca4e878e8 fixes both;112/no skips
and strict specs pass runtime/Ubuntu24.04.5, source actual push/PR pass. Consumer
fd49a238121b0c0bc54754fb79f792f290d880ff pins it, preserves policy/project/index and
unchanged shared hashes; actual push/PR/metadata/fresh bootstrap/index/negative
proof pass. User source-suite intermittent JSON error remains unreproduced; helper
now preserves command/streams for diagnosis; no assertion weakened/skipped.
Documentation/immutable consumer links and stale remote titles are reconciled;
final Ready-head review and final archive/spec/docs acceptance are next. F14 remains
unchecked until those complete; no Cloud/global/merge/closure/admin/release mutation.


### Latest malformed-bundle review — 2026-10-05

Consumer review5992697851 reports no major issues at fd49a23812. Source4183023649
independently reproduced before acceptance: array/object destinations cause unhandled
TypeError; scalar nonstrings also return wrong exit category. d1de33ac3c6e889ea0c189ec53b000fe0bfddecc
validates destination types before set conversion; regression exercises five types
through both public installers with structured exit2/no writes.113/no skips pass
runtime/Ubuntu24.04.5; strict specs pass, unchanged documented contract. Consumer
2a59be9b42719e020c7888d61f9ea59e5214035a pins repair, project/index/shared hashes preserved,
guarded identical-tree publication. Actual CI/current-head review evidence remains
revision-bound; previous review is not new-head approval. Next: finish affected
consumer/CI proof, resolve repaired finding, obtain final review and archive/checks.
No global/admin/merge/closure/release action; Ubuntu26 intermittent error cause not claimed fixed.

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
[host integration design](../../../docs/workflow/review-continuation.md) specifies scoped
wake-ups, current-head completion evidence (including comments/reactions), duplicate/
concurrency controls, authorized remediation and the merge boundary. This chat exposes
notification scheduling but no Codex wake-up/event-subscription tool, so no monitor
is enabled or automatic coding continuation claimed. This adds no mandatory workflow
engine, database, installation requirement or acceptance gate. Next: inspect final
review outcomes, remediate valid findings, then archive/check after required premerge
acceptance; host integration requires an actual supported wake-up acceptance proof.
No merge/completed closure/admin/global/auth/release/remote-deletion action.

## NUL-path review repair and active-session monitoring — 2026-10-05

The requested five-minute active-session timer observed completed consumer review
5993740628 at7a74c97147 (no major issues), then source review5413992766 atc5d18b1
with P2 comment4183600564. Completed targets were disarmed. This is an awaited
current-turn timer, not a persistent host wake-up or scheduled workflow engine.

The new path finding was independently reproduced before acceptance: an otherwise
complete committed bundle containing a NUL source key or destination caused an
unhandled filesystem ValueError or accepted an invalid unused destination. All eight
preview/apply cases through setup and isolated install-skills failed the new regression
before the fix. Runtime08346d2f0f29a1f7c3706578424ddad5d986b820 rejects NULs in
shared relative-path validation and prevalidates every source/destination before
filesystem access. Both installers return exit2/ok:false structured invalid JSON,
preserve consumer files/raw index and do not create the isolated global target.
This restores the existing documented invalid-configuration/preflight contract;
no behavior scope or skill content changed.

All119 tests/no skips pass at08346d2 on managed Python3.12.14 (69.371s) and
Ubuntu24.04.5/Python3.12.3 (55.222s); strict specs/check pass. Consumer
adaad276a1b2f41f135026de1f7781fc49cf24d7 pins08346d2. Treef9d75284a426253920aff8c837dd240e4c22d500
matches own local9ea8e5414c06fddd4a627e9b70957cf82481640d with parent7a74c9714;
publication was guarded/non-force. Only two runtime files/provenance changed;
project policy/shared skills/raw index were preserved during update. Fresh actual
remote clones on managed runtime and Ubuntu materialize4 exact files/match20 hashes,
pass check/doctor/repeat offline/no-op, preserve project/index bytes and exercise
installed public NUL rejection plus retained file/directory rollback and indexed-policy
negatives. An initial clone tried the source before publication and a separate
container proof used an incorrect CA path; corrected reruns passed without TLS bypass.
Initial consumer CI also ran before source publication and failed at fetch; affected
jobs are rerun and their actual results remain recorded separately in the PR checkpoint.

README now explicitly documents the existing managed AGENTS routing section,
preservation/idempotence, globally discoverable v1 wrappers and higher-level policies.
No installer routing change was necessary. Original independent Ubuntu discovery/
actual three-skill use remains verified at unchanged shared bytes. Cloud is deferred;
optional real global-host use unperformed; Ubuntu26 historical intermittent source
suite cause remains unresolved. Next: current-head Actions/semantic review with an
active-session five-minute timer, then archive/final checks only after acceptance.
No merge/completed closure/admin/global/auth/release/remote-deletion action.

## Wider local malformed-input review — 2026-10-05

The user clarified that the latest PR P2 was already addressed and requested wider
pattern review. [The local review](../../../docs/validation/wider-boundary-review.md) records three independently
reproduced analogous defects (argv partial execution, unencodable paths, malformed
Markdown URLs), their public negative controls and inspected rollback ownership cases.
Runtime7be9f1538b96d7dd98247e7e5eadffa042350496 passes121/no skips on managed runtime
and Ubuntu24.04.5, with strict checks/specs. Consumer e1d59ab460c4fc8cb2196a75f3b3c8a87cf15524
pins it; actual remote fresh-clone checks and installed public negatives pass on both
runtimes. Shared skill/project/index policy stays unchanged. These are primary-author
findings and runtime proof, not independent approval of this newly repaired content.
Final exact-head Actions/reviews and final archive/spec/docs verification remain the
next gates; older review results retain their actual revisions. No merge/closure/
admin/global/auth/release/remote deletion and no persistent-host wake-up claim.

Latest consumer documentation head0ec3e90d3fe5726f4a06a8b2c897d38b82473839 repairs
review4183725905: the stated source pin and immutable setup URL now match the
7be9f15 manifest. Original Ubuntu evidence links retain original revisions.
Full runtime121/no-skips and live source7be9f15/consumere1d59ab46 CI passed; latest
Ready-head reviews and documentation-head Actions remain separately required.

## Latest staging, discovery and adoption/output repairs — 2026-10-05

Required semantic review returned staging-symlink, invalid-discovery-text,
fresh-adoption index and plain-text output findings. Each was reproduced before
repair. The staging and discovery repair at cb6638ef6b3b43a942bb6a8b97f46f4281b8b64a
passed125/no skips on both runtimes and actual consumer e852af83ea086ae796e38ef69dc5f448a8bd04cb
fresh-clone/installed negative probes; its source/consumer Actions all succeeded.
The latest runtime is `9af59a503bc9d51f1570bb0d3c9385eaba7f528d`, with all127/no skips on managed Python3.12.14
(76.716s) and Ubuntu24.04.5/Python3.12.3 (67.470s), strict specs/check and diff hygiene.

Consumer `a0401b89702eca70a7956ce043e8b545364f78fb` pins that exact source. Its tree
a09356149c18e294768e3e94f22c334459223c69 matches own local
4b71e34134ebd26afa942db6c8f4cd0ce0d659b1, parent e852af83 preserved by guarded
non-force publication. Explicit update changes only core/setup/workflow, operations
and provenance; project policy, shared hashes and raw index remain unchanged before
caller staging. README now resolves source/setup links from the tracked manifest,
avoiding duplicated pin prose. Actual remote fresh clones on managed runtime and
Ubuntu materialize4 exact files/match20 hashes, pass check/run-local/doctor/offline
repeat, preserve project/index bytes and exercise installed negative paths: existing
force-tracking, three indexed-only nested policies, concurrent file/directory/staging
recovery, NUL/native argv/URL rejection, invalid discovery continuation,20 fresh
indexed-path preview/apply cases and default UTF8/ASCII diagnostics without traceback.

Current runtime source push37309308964/PR37309317868 and consumer
push37309447682/PR37309456606/metadata37309452510 succeed. These are exact-revision
implementation/integration results. Final current-head semantic review and archive
remain pending; older reviews do not approve this new content. The original independent
Ubuntu startup catalog/actual three-skill use remains valid at unchanged shared hashes.
No extra user workstation discovery session is required for these runtime-only repairs.
Cloud is deferred; real global installation unperformed; Ubuntu26 historical source
JSON error remains unexplained. Source required-check administration and real merge →
completed Issue observation remain pending separate authorization, not simulated.
See [wider boundary review](../../../docs/validation/wider-boundary-review.md) for discriminating controls and documentation impact.

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

[Exact evidence and review controls](../../../docs/validation/wider-boundary-review.md) supersede earlier
current/default claims below; earlier revision-specific observations remain historical.
[Ubuntu setup handoff](../../../docs/validation/ubuntu-workstation-handoff.md) records exact usable pins and
source-first commands. Both latest P2s were reproduced before repair; current-head
semantic review and final archive/docs/spec checks remain pending. Original native
Ubuntu discovery/use retains its unchanged skill hashes. Consumer ruleset requires
both checks; source ruleset now requires verification, while source PR-contract
administration/deployment and merge→valid Issue completion remain separate gates.
Cloud deferred, real global-host use unperformed, historical Ubuntu26 source-suite
error unexplained. No merge/completed closure/admin/global/auth/release/deletion.

## Latest verified runtime and consumer checkpoint — 2026-10-05

Source `f05cf27df47e008bf52e6f14a8dbd6bbf53e4f80`; consumer
`d8ed0abca40a7fa4ed092f4facfb25fefee30977`, pilot/shared-skill-bootstrap/ReadyPR8.
All137/no skips pass locally and Ubuntu24.04.5; current source/consumer docs/specs
cover indexed ancestors, complete runtime retirement and executable migration.
Actual remote fresh clones, installed public boundary tests and consumer push/PR/
metadata pass;11 pinned dependencies remain ignored/untracked under four namespaces.
[Exact current evidence](../../../docs/validation/wider-boundary-review.md) supersedes earlier checkpoints.
[Source-first Ubuntu command](../../../docs/validation/ubuntu-workstation-handoff.md) records both full SHAs.
Original native discovery/use keeps its actual unchanged skill hashes. Current-head
semantic review and final archive remain pending; deployed-base new metadata and
real merge→valid completion are separate authorization gates. Cloud deferred, real
global-host use unperformed and historical Ubuntu26 source-suite error unexplained.

## Current ancestor/index checkpoint — 2026-10-05

This checkpoint supersedes earlier current/default statements below. Tested source
implementation/pin `0f6b6766da7a86a039108891ec051306963425ae`,
`rewrite/workflow-skills-v2`: all138/no skips pass on managed Python3.12.14
(144.107s) and Ubuntu24.04.5/Python3.12.3 (120.835s). Strict specs and public
check pass. Consumer `b33b0d4a938b2718a3adb686f4899b4689d46b20`,
`pilot/shared-skill-bootstrap`, Ready PR8/Issue7, pins this source. Published
ce912ff51f434f04584e9875ab4356cf047b8271 matches reviewed local3fdef990 tree,
parentd8ed0ab, guarded non-force publication. Source-owned update preserves
config, all shared/project skill bytes and raw index
b8ab7d37b1ccbc2b9b088e892c95678d5da570a8d2cc8eff37d596023db5a659.

Additional wider review reproduced an index-only dependency ancestor file:
intact working directories hid a non-bootstrapable staged snapshot. The before
control fails3 subcases/no errors; centralized ancestor preflight now covers
setup, check, doctor, bootstrap and independently validated staged installation.
All reject without file/index changes; coherent migration still passes before
old HEAD is merged. Source/consumer operations, current/delta adoption specs,
README install example and Ubuntu handoff were reassessed. The delta now uses
MODIFIED for requirements already present in current specs and supplies the
release Purpose, so archive preparation does not duplicate implemented contracts.

Actual fresh remote clones on managed runtime and Ubuntu start with no shared
runtime/skills; source-first bootstrap installs11 canonical dependency files,
matches20 manifest hashes, passes check/run-local/doctor and offline no-op repeat,
and preserves tracked files/raw index. Prior installed rollback/native-input/
indexed-policy controls pass. The installed six-test layout suite passes on both
managed runtime (50.710s) and Ubuntu (37.311s). The literal pinned fetch-and-run
install command succeeds twice in a fresh Ubuntu Git root without creating an
index or requiring any existing consumer helper. Only the four dependency
namespaces are ignored; project skills/tools and v2 AGENTS routing remain tracked.
The first mounted-source Ubuntu attempt failed Git ownership policy; rerunning
with an owned source copy passed without changing global Git configuration.

Consumer current-head push[37320356900](https://github.com/canzheng/workflow-skills-test/actions/runs/37320356900),
PR[37320366947](https://github.com/canzheng/workflow-skills-test/actions/runs/37320366947)
and existing-main metadata[37320361118](https://github.com/canzheng/workflow-skills-test/actions/runs/37320361118)
pass. Source pin push37320277173/PR37320287331 and later documentation-head CI
are recorded in the live PR checkpoint. New trusted-base pin-fetch metadata is
locally exercised; actual deployment/event execution on main remains pending an
authorized merge, distinct from existing-main metadata success.

Native Ubuntu discovery/actual all3-skill use retains its original9bd23d72/a75c3f2
revision-bound evidence because all four shared skill hashes remain unchanged.
F01–F13 implemented/verified/review-ready; F14 partial pending final current-head
semantic review and rewrite archive/final specs/docs checks. Cloud deferred,
real global-host use unperformed, historical Ubuntu26 source JSON error unexplained.
Consumer two required checks and source required verification were observed;
source PR-contract configuration/deployment and real merge→valid completed Issue
observation remain separate authorization gates. No merge, completed closure,
admin, global/auth, release or remote branch deletion. Next: current-head semantic
reviews with awaited five-minute monitors; archive only after premerge acceptance.

## Latest runtime-layout and CI-provenance repair — 2026-10-05

This checkpoint supersedes earlier current/default statements below. Source
implementation/pin `4449a1e6d03b6e055446735b89c4630b0c8b9d85`,
rewrite/workflow-skills-v2: all142/no skips pass on managed Python3.12.14
(137.599s) and Ubuntu24.04.5/Python3.12.3 (116.116s), strict specs and public check.
Consumer `66913db29472d8277002b068205fc05db62b2bbf`,
pilot/shared-skill-bootstrap/Ready PR8/Issue7, pins this source. Published
bf8f8e5c1cba1b0858169a1053ab2991263c7add matches reviewed local740436647 tree,
parentb33b0d4 and guarded non-force publication. Update preserved config/all skills
and raw indexb56b1fa2e37bcd6cf57f47f6502fd1082a759be5f5145d281b53d95d4eb92d20.

The prior consumer review completed atb33b0d4 with no major issues (comment5996081813).
The source review5415759761 at946dffe returned P2s4184890020/4184890034.
Five-minute monitors detected completion and disarmed before fixes. Both findings
were independently reproduced before acceptance. Exact old946dffe helpers accept
legacy-layout ignored schema5 setup/check/run-local/doctor/bootstrap while the
installed CI command fails2 because the new CLI is absent. Before controls also
show both installed YAMLs selecting a nonexistent source checker when an unrelated
tracked bundle marker exists. New structural-layout/CLI controls fail before repair;
no fixture errors or permissive acceptance changes are counted as proof.

Schema5 now requires .agents/tools/workflow. Ignored setup from a legacy bundle
rejects before writes; existing schema3/4 verification and explicit tracked legacy
setup remain supported. Both CI preparations prioritize consumer provenance over
unrelated bundle markers. Verification chooses the installed runtime from the
manifest; PR metadata still uses only the trusted base pin. Doctor avoids probing
an unrelated source marker once consumer provenance exists. Regressions execute
both actual YAML preparations/commands, preserve unrelated marker bytes/raw index,
and prove legacy tracked verification succeeds at its real runtime path.
Current/delta adoption specs, source/consumer operations and architecture match.

Actual managed/Ubuntu fresh remote clones start with no helper/skills; source-first
initialization materializes11 exact files/matches20 managed hashes. Installed
check/run-local/doctor/offline repeat and raw-index/tracked-file proof pass; prior
rollback/native-input/index controls remain intact. The actual installed twelve-test
layout/CI suite passes on managed runtime (46.812s) and Ubuntu (42.605s). Literal
pinned GitHub fetch-and-run first adoption and repeat both pass on fresh Ubuntu
without an index or pre-existing helper. Four narrow ignore rules only; project
skills/tools and AGENTS/config/CI/docs/pin remain tracked.

Consumer current push[37322931564](https://github.com/canzheng/workflow-skills-test/actions/runs/37322931564),
PR[37322942245](https://github.com/canzheng/workflow-skills-test/actions/runs/37322942245)
and existing-main metadata[37322935924](https://github.com/canzheng/workflow-skills-test/actions/runs/37322935924)
pass. Source pin push37322805393/PR37322816322 and documentation-head CI are
recorded in the live PR checkpoint. New trusted-base metadata YAML is executed
locally; its actual deployment/events on main await authorized adoption merge.

Native Ubuntu catalog/use stays revision-bound to original9bd23d72/a75c3f2 and
unchanged skill hashes. F01–F13 implemented/verified/review-ready. F14 partial:
current semantic reviews, archive and final specs/docs checks remain, then real
merge→valid Issue completion and deployed-base observation require separate
permission. Cloud deferred, real global-host use unperformed, historical Ubuntu26
JSON error unexplained. Consumer two checks and source verification enforcement
were read-only confirmed; source PR-contract administrative configuration remains
pending. No merge/closure/admin/global/auth/release/remote deletion. Next: current
Ready-head review; archive only after premerge acceptance, then final checks/review.


## Source-check compatibility review repair — 2026-10-05

Review5416098884 at151476c735e274012d9bb597653908c9ae5fe96b returned
P2 comment4185120389. Independent public CLI reproduction confirms source check
rejects a complete legacy tracked bundle after setup and its installed checker
succeed. Wider control shows mixed source inventories accepted despite setup
rejecting them. Shared layout-aware requirements now govern source checking.
Before controls: three focused tests, two discriminating failures, no errors;
after: all three pass (2.275s), including missing-module negatives in both layouts.
Existing assertions remain intact. Development guidance records source/installer
agreement; compatibility specs already describe it, so no behavior-contract change
is needed. Full source/Ubuntu suites, consumer repin/proof, CI and new semantic
review are next; archive and real merge/completed closure remain pending.


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
remain pending separate authorization. See [wider review](../../../docs/validation/wider-boundary-review.md).

## Parent-chain recovery and Issue snapshot review repairs — 2026-10-05

Source review5416864834 at082e2257e1c8ef100fa128001037e9a8bf2021e9 returned
P2s4185701946/4185701969. Both reproduced with public setup/check before acceptance.
Deleted files were restored into replacement parents; malformed Issue entries
returned tracebacks/empty stdout. Wider author inspection adds ancestor/same-content/
symlink and forward-write controls. Recorded parent inode chains now gate writes
and restoration, with original backup/expected parent recovery metadata; shared
Issue helpers validate entry, label and state shapes before dereferencing.
All48 existing/focused setup/check/record tests pass (21.162s) and all3 new focused
tests pass (2.595s). Operations/source-consumer, architecture, checks guidance and
current/delta adoption scenarios are updated. Full local/Ubuntu suites, actual
installed proof, consumer repin/Actions, evidence and current semantic reviews are
next. Reviews are disarmed on completion; no archive/merge/closure/admin change.

## Latest post-drain identity checkpoint — 2026-10-05

Source implementation `0f6fc7b8a192d1843b41b3d7600f06a169871004` on
`rewrite/workflow-skills-v2` is implemented and verified. Consumer
`c9229e14825d5445c97ab4d277fd1fcf654be343` on `pilot/shared-skill-bootstrap`
pins that exact source. Both Ready PRs remain open; F14 Issue15 and consumer Issue7
remain open. F01–F13 are implemented/verified/review-ready; F14 remains partial.
Neither repository has merged or delivered.

The five-minute monitor observed source review5419306426 ated7b969 and consumer
clear6001189911 atde407cb6, then disarmed both targets. Source finding4187706836
is independently valid: pathname identity was cached before the final nonblocking
event read. Four old-code controls fail without errors at that boundary: same-mode
inode replacement, symlink, deletion and changed permissions. The repair performs
the final pathname/descriptor comparison after event draining; this comparison
defines the end of the observation window. All five focused birth/observation
controls pass (0.194s before commit; 0.371s at the committed revision).

| Verification | Actual result |
| --- | --- |
| Full source suite, managed Python3.12.14 | 172 tests, no skips, 184.944s, OK |
| Full source suite, Ubuntu24.04.5/Python3.12.3 | 172 tests, no skips, 167.686s, OK |
| Actual installed consumer tests, managed runtime | 49 tests, 84.651s, OK |
| Actual installed consumer tests, Ubuntu | 49 tests, 81.134s, OK |
| Strict OpenSpec and public spec checker | All5 items pass; ok:true |
| Literal exact-pin Ubuntu first adoption/repeat | Both exit0; absent index stays absent |
| Consumer push/PR/existing-main metadata Actions | 37361217469 /37361225271 /37361220449 pass |

Fresh managed clone of the API-verified remote commit and fresh Ubuntu remote clone
materialize11 ignored dependencies, match20 managed hashes, retain four narrow
ignores and the tracked project skill/config/files, and preserve raw index. Matching
repeat bootstrap is offline/no-op. Installed verification includes this final-read
regression and earlier birth, overflow/unavailable support, capture/parent/inode/
bytes/mode/symlink, force-tracking/index-only policy, layout, discovery, PR input/
rendering and actual consumer-CI controls. No original preservation assertion is weakened.

Source-owned update preserves all skill bytes/config/raw index
`95749f0e54ae5c9cc074915ba24292cfc48d90923dde902d781b9123c104cb85`
before caller staging only manifest and changed operations guidance. Native tree
`0845408f2970d398278abbde4e5ec967c8f477d9` equals reviewed local6ec0f690,
parentde407cb6. Native commit bytes independently hash toc9229e14; guarded non-force
publication and same-tree local ref reconciliation leave files/index clean.
Current source Actions and fresh reviews are recorded by exact head in the PR checkpoint.

Creation observation is a short-lived inotify parent watch, not a process lock or
persistent task monitor. Captured files/directories remain retained in Git-private
storage or same-filesystem TMPDIR, without automatic garbage collection. Current
operations/current+active adoption scenarios explicitly define the post-drain check.
Native Ubuntu startup discovery and actual three-skill use remain proven at
9bd23d72/a75c3f2 with unchanged shared hashes; no new native CLI session at this pin
is claimed. Cloud is deferred/unverified. Actual global-host discovery/use remains
unperformed; the historical Ubuntu26 full-suite JSON failure remains unexplained.

Repaired-head semantic review and native archive/final checks remain pending.
Green consumer metadata executes the existing main trusted checker; new schema5
trusted-base deployment/events require authorized adoption merge. Read-only ruleset
inspection2026-10-05T18:27:07Z confirms active/no-bypass source24457981 verification
and consumer24484016 both v2 checks. Source PR-contract administration, real merge
and valid Issue-completion observation remain pending separate authorization.
No merge/closure/admin/global/authentication/release/remote deletion occurred.
Next: repaired-head review, then native archive/final checks; obtain separate delivery
authorization only after those gates pass.

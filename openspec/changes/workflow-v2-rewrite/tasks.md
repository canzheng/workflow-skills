# Rewrite implementation and acceptance

- [x] 1. Establish repository-scoped foundation (WF2-F01–F06).
- [x] 2. Implement specifications, risk proof, handoffs, checks and scenarios (WF2-F07–F11).
- [x] 3. Inventory migration and retire active v1 assets (WF2-F12–F13).
- [ ] 4. Complete required Cloud/Ubuntu/GitHub/enforcement acceptance and archive (WF2-F14).

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
startup stays branch-agnostic and uses its tracked pin. Need actual automatic-run
output and host discovery ordering; this Start definition conflict does not prove
it ran. Limited main summary reports protection disabled; authoritative admin reads
denied, enforcement not proven. F14 stays unchecked/change active. Cloud/Ubuntu
agent-host acceptance and real merge→valid Issue completion/admin mutation remain
distinct; merges/closure/admin changes require separate authorization.

# Rewrite implementation and acceptance

- [ ] 1. Establish repository-scoped foundation (WF2-F01–F06).
- [ ] 2. Implement specifications, risk proof, handoffs, checks and scenarios (WF2-F07–F11).
- [ ] 3. Inventory migration and retire active v1 assets (WF2-F12–F13).
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

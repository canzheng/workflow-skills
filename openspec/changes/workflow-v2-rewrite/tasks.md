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

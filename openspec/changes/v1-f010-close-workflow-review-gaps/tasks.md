- [ ] 1 Tighten shared workflow structural validation
  - [ ] 1.1 Detect extra or out-of-order canonical backlog sections, including sections appended after `[DEFER]`
  - [ ] 1.2 Detect promoted-feature records that are missing linked `OpenSpec Specs` metadata

- [ ] 2 Align audit and diagnosis with the stricter structural checks
  - [ ] 2.1 Make `audit-workflow` fail on extra canonical sections and missing promoted-feature spec linkage
  - [ ] 2.2 Make `diagnose-workflow` emit structured findings for those same states instead of returning a false healthy status
  - Depends On:
    - `1`

- [ ] 3 Add validation coverage for all implementation findings
  - [ ] 3.1 Add audit coverage for extra sections after `[DEFER]`
  - [ ] 3.2 Add audit and diagnosis coverage for missing promoted-feature `OpenSpec Specs`
  - [ ] 3.3 Add diagnosis coverage proving malformed workflow states are not reported as healthy
  - Depends On:
    - `1`
    - `2`

- [ ] 4 Repair workflow source-of-truth artifacts called out by the review
  - [ ] 4.1 Reconcile `finish-feature` wording across `AGENTS-global-workflow.md` and `README.md`
  - [ ] 4.2 Replace placeholder version-goal and exit-bar text in `docs/planning/versions/v1/VERSION_SCOPE.md`
  - [ ] 4.3 Replace placeholder purpose text in `openspec/specs/openspec-change-integration/spec.md`
  - [ ] 4.4 Repair historical feature notes that currently contradict the accepted workflow contract

- [ ] 5 Record explicit finding-to-validation evidence
  - [ ] 5.1 Define validation steps that map each original review finding to a specific test or inspection
  - [ ] 5.2 Validate that the tightened change artifacts explicitly cover every finding before feature completion
  - Depends On:
    - `2`
    - `3`
    - `4`

## 1. Shared Workflow Validation

- [ ] 1.1 Add shared validation for canonical backlog sections so extra or out-of-order sections are detected consistently
- [ ] 1.2 Add shared validation for promoted-feature `OpenSpec Specs` metadata so missing linked spec paths are detectable

## 2. Audit And Diagnosis Alignment

- [ ] 2.1 Make `audit-workflow` fail when canonical board structure or promoted-feature spec linkage is invalid
- [ ] 2.2 Make `diagnose-workflow` report those same issues as structured findings without becoming a hard gate

## 3. Coverage

- [ ] 3.1 Add fixture coverage for extra sections after `[DEFER]` and missing promoted-feature `OpenSpec Specs`
- [ ] 3.2 Add diagnosis coverage for malformed board structure and missing promoted-feature spec linkage

## 4. Source-Of-Truth Cleanup

- [ ] 4.1 Reconcile `finish-feature` wording across workflow docs so the invocation point is consistent
- [ ] 4.2 Repair incomplete or contradictory planning/spec artifacts identified by the review

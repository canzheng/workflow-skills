## 1. Contract Alignment

- [x] 1 Update workflow guidance and stable specs so the reopened `v1-f018` remediation scope is explicit
  - [x] 1.1 Align `skills/complete-task/SKILL.md` and contract-doc assertions with the canonical `completion_handoff` continuation model
  - [x] 1.2 Align `skills/ready-feature/SKILL.md`, `skills/complete-task/SKILL.md`, and stable specs on required canonical structured review-verdict emission

## 2. Runtime Remediation

- [x] 2 Implement the missing runtime behavior behind the reopened `v1-f018` obligations
  - [x] 2.1 Make selected-feature continuation fail closed when the intended active feature worktree is missing or ambiguous
  - [x] 2.2 Add end-to-end structured review-verdict emission and at least one downstream consumer path that reads the emitted verdict state
  - [x] 2.3 Add or update regression tests for the fail-closed worktree path, structured verdict emission/consumption, and the aligned `complete-task` contract

## 3. Validation And Reclose

- [ ] 3 Run the narrowest combined validation slice for the reopened remediation scope
  - [ ] 3.1 Re-run workflow audit and the affected contract/runtime test targets
  - [ ] 3.2 Record the remediation evidence in the feature file so `v1-f018` can return to `finish-feature` cleanly

## 1. Shared Dependency Resolution

- [ ] 1 Shared Dependency Resolution
  - [ ] 1.1 Refactor OpenSpec-backed task status derivation to resolve cross-feature dependencies through the shared dependency model
  - [ ] 1.2 Extend linked-change lookup so completed archived features can still satisfy downstream dependencies

## 2. Resolver Alignment

- [ ] 2 Resolver Alignment
  - [ ] 2.1 Update start-task and related task-selection helpers to rely on the unified readiness result
  - [ ] 2.2 Confirm diagnostics and drift reporting stay consistent when upstream work is active versus archived

## 3. Regression Coverage

- [ ] 3 Regression Coverage
  - [ ] 3.1 Add shared-helper tests for active and archived cross-feature dependencies
  - [ ] 3.2 Add resolver-level fixture coverage proving valid cross-feature work becomes startable

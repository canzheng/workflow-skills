## 1. Active Change Enumeration

- [ ] 1 Active Change Enumeration
  - [ ] 1.1 Add helper logic that lists active unarchived change IDs and compares them against promoted-feature links
  - [ ] 1.2 Exclude archive directories and preserve the existing completed-feature rules

## 2. Health Check Integration

- [ ] 2 Health Check Integration
  - [ ] 2.1 Add structured orphan-change findings to diagnose-workflow
  - [ ] 2.2 Fail audit-workflow when active changes are not linked from promoted features

## 3. Coverage

- [ ] 3 Coverage
  - [ ] 3.1 Add diagnosis fixtures covering orphaned and repaired active-change states
  - [ ] 3.2 Add audit fixtures proving orphan active changes fail the gate

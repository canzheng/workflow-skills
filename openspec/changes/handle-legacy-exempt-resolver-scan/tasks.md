## 1. Resolver Update

- [ ] 1 Resolver Update
  - [ ] 1.1 Update `complete-task` to tolerate `[DONE]` `legacy-exempt` features that omit `OpenSpec Change` while scanning for active work
  - [ ] 1.2 Preserve strict OpenSpec linkage failures for active feature states that actually need change context

## 2. Regression Coverage

- [ ] 2 Regression Coverage
  - [ ] 2.1 Add an integration fixture with one active task and one `legacy-exempt` completed feature missing `OpenSpec Change`
  - [ ] 2.2 Prove `complete-task` resolves the active task in that mixed repository state without weakening active-state validation

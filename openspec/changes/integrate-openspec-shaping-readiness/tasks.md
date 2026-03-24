## 1. Contract and Templates

- [ ] 1.1 Update the managed workflow contract to define OpenSpec-backed shaping/readiness ownership and thin feature files
- [ ] 1.2 Update the workflow initializer/template so new feature files store execution metadata and OpenSpec links instead of embedded design and plan prose
- [ ] 1.3 Update the wrapper skill docs for `shape-backlog-item` and `ready-feature` to treat OpenSpec artifacts as their shaping/readiness inputs

## 2. Audit and Repair

- [ ] 2.1 Extend workflow parsing/helpers to recognize the new OpenSpec link metadata in feature files
- [ ] 2.2 Extend `audit-workflow` to validate required OpenSpec links and `[READY]` shaping prerequisites structurally
- [ ] 2.3 Update `repair-drift` guidance so OpenSpec-linked inconsistencies are handled as minimal structural repairs

## 3. Verification and Adoption

- [ ] 3.1 Add or update tests covering OpenSpec-linked shaping/readiness and expected audit failures
- [ ] 3.2 Validate the updated workflow and OpenSpec specs with the narrowest relevant commands
- [ ] 3.3 Document migration expectations for adopting the new model in future features

## 1. Contract and Templates

- [x] 1.1 Update the managed workflow contract to define OpenSpec-backed shaping/readiness ownership and thin feature files
- [x] 1.2 Update the workflow initializer/template so new feature files store execution metadata and OpenSpec links instead of embedded design and plan prose
- [x] 1.3 Update the wrapper skill docs for `shape-backlog-item` and `ready-feature` to treat OpenSpec artifacts as their shaping/readiness inputs

## 2. OpenSpec-Backed Task Authority

- [x] 2.1 Extend workflow parsing/helpers to recognize required OpenSpec link metadata in feature files and parse OpenSpec task status from `tasks.md`
- [x] 2.2 Extend `audit-workflow` to validate required OpenSpec links, `[READY]` shaping prerequisites, and OpenSpec task-state invariants structurally
- [x] 2.3 Update `start-task` and its resolver to select the next ready task from the linked OpenSpec change and mark it `in_progress`
- [x] 2.4 Update `complete-task` expectations so task completion records evidence locally but updates task status in OpenSpec
- [x] 2.5 Update `repair-drift` guidance so OpenSpec-linked inconsistencies are handled as minimal structural repairs

## 3. Verification and Adoption

- [x] 3.1 Add or update tests covering mandatory OpenSpec initialization, OpenSpec-linked shaping/readiness, OpenSpec task parsing, and expected audit failures
- [x] 3.2 Validate the updated workflow and OpenSpec specs with the narrowest relevant commands
- [x] 3.3 Document migration expectations for adopting the new model in future features

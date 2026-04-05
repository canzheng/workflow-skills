## 1. Record execution-time validation evidence

- [ ] 1 Make task execution record validation evidence as proof is produced
  - [ ] 1.1 Add a shared workflow helper that appends task-scoped validation entries to the feature file
  - [ ] 1.2 Update `start-task`, the workflow reference, and the feature template so execution owns evidence capture and `complete-task` owns reconciliation
  - [ ] 1.3 Add focused tests for the helper and any updated workflow expectations

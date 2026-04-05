## 1. Record execution-time validation evidence

- [x] 1 Make task execution record validation evidence as proof is produced
  - [x] 1.1 Add a shared workflow helper that appends task-scoped validation entries to the feature file
  - [x] 1.2 Update `start-task`, the workflow reference, and the feature template so execution owns evidence capture and `complete-task` owns reconciliation
  - [x] 1.3 Add focused tests for the helper and any updated workflow expectations

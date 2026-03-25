## 1. Feature Completion Handoff

- [x] 1 Feature Completion Handoff
- [x] 1.1 Define the completion-time conditions that make the final task hand off from `complete-task` into `finish-feature`
- [x] 1.2 Update task-completion helpers or resolver outputs so the final-task handoff is operationally explicit without moving the feature to `[DONE]`
- [x] 1.3 Make `complete-task` verify that all nested checklist items under the selected top-level task are already closed before it marks that top-level task done

## 2. Finish-Feature Alignment

- [x] 2 Finish-Feature Alignment
- [x] 2.1 Shift feature-state ownership so `finish-feature`, not `complete-task`, moves a feature from `[IN_PROGRESS]` to `[DONE]`
- [x] 2.2 Require `finish-feature` to run only when all top-level OpenSpec tasks are done and `Current Task` is `none`
- [x] 2.3 Update workflow audit and regression coverage for the new final-task-to-finish-feature boundary

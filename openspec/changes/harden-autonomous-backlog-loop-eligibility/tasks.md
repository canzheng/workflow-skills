- [x] 1 Eligibility validation
  - [x] 1.1 Require active features considered for `run_task_loop` to have valid OpenSpec linkage and no readiness drift
  - [x] 1.2 Stop with a clear workflow error when malformed active features would otherwise be selected

- [ ] 2 Shared policy alignment
  - [ ] 2.1 Reuse the shared dependency and readiness helpers instead of open-coding a weaker autonomous policy
  - [ ] 2.2 Confirm clean backlog and shaping cases still return shaping-oriented actions
  - Depends On:
    - `1`

- [ ] 3 Coverage
  - [ ] 3.1 Add autonomous-loop fixture coverage for malformed ready features and repaired states
  - [ ] 3.2 Add regression coverage for parity with start-task eligibility behavior
  - Depends On:
    - `1`
    - `2`

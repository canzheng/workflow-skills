- [x] 1 Eligibility validation
  - [x] 1.1 Require active features considered for `run_task_loop` to have valid OpenSpec linkage and no readiness drift
  - [x] 1.2 Stop with a clear workflow error when malformed active features would otherwise be selected

- [x] 2 Shared policy alignment
  - [x] 2.1 Reuse the shared dependency and readiness helpers instead of open-coding a weaker autonomous policy
  - [x] 2.2 Confirm clean backlog and shaping cases still return shaping-oriented actions
  - Depends On:
    - `1`

- [x] 3 Coverage
  - [x] 3.1 Add autonomous-loop fixture coverage for malformed ready features and repaired states
  - [x] 3.2 Add regression coverage for parity with start-task eligibility behavior
  - Depends On:
    - `1`
    - `2`

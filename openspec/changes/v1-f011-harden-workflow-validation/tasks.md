- [x] 1 Harden diagnosis fallback behavior
  - [x] 1.1 Prevent `diagnose-workflow` from raising when planning scaffold is missing
  - [x] 1.2 Keep diagnosis output structured and advisory for those malformed states

- [ ] 2 Enforce shaping artifact baseline and archived done-state rules
  - [ ] 2.1 Require `proposal.md`, `design.md`, and `tasks.md` for features in `[SHAPING]`
  - [ ] 2.2 Keep the existing stronger `[READY]` gate unchanged
  - [ ] 2.3 Tighten completed-feature validation around archived linked changes
  - Depends On:
    - `1`

- [ ] 3 Add focused regression coverage
  - [ ] 3.1 Cover missing planning scaffold in diagnosis
  - [ ] 3.2 Cover missing shaping artifacts in audit and diagnosis
  - [ ] 3.3 Cover the clarified archived `[DONE]` contract
  - Depends On:
    - `1`
    - `2`

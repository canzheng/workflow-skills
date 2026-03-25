## 1. Migration Contract

- [x] 1.1 Update the workflow contract and README to describe midstream OpenSpec adoption, baseline-spec expectations, and the `legacy-exempt` completed-feature marker
- [x] 1.2 Add spec deltas for audit, board lifecycle, and feature tracking to capture archived completed features and historical completed-feature exemptions

## 2. Audit Implementation

- [x] 2.1 Extend workflow metadata parsing to recognize the optional OpenSpec status marker
- [x] 2.2 Update `audit-workflow` so `[SHAPING]`, `[READY]`, and `[IN_PROGRESS]` require active changes, while `[DONE]` accepts either archived changes or explicit `legacy-exempt` status
- [x] 2.3 Keep post-adoption `[DONE]` features strict by failing missing-change completed features that are not explicitly `legacy-exempt`

## 3. Verification

- [x] 3.1 Add tests for legacy-exempt completed features, archived completed features, and invalid completed features with missing OpenSpec state
- [x] 3.2 Validate audit and change artifacts with the narrowest relevant commands

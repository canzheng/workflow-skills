- [ ] 1 Harden installer initialization behavior
  - [ ] 1.1 Keep missing target `AGENTS.md` as a hard failure
  - [ ] 1.2 Append the managed workflow section when an existing `AGENTS.md` lacks markers
  - [ ] 1.3 Document the installer's `rsync` dependency

- [ ] 2 Constrain the managed development environment
  - [ ] 2.1 Declare an explicit Python floor compatible with repo code
  - [ ] 2.2 Declare explicit Conda channels for repeatable resolution
  - Depends On:
    - `1`

- [ ] 3 Add regression coverage
  - [ ] 3.1 Cover missing-file versus missing-marker installer behavior
  - [ ] 3.2 Cover the managed-environment assumptions used by the wrapper and tests
  - Depends On:
    - `1`
    - `2`

- [x] 1 Harden installer initialization behavior
  - [x] 1.1 Keep missing target `AGENTS.md` as a hard failure
  - [x] 1.2 Append the managed workflow section when an existing `AGENTS.md` lacks markers
  - [x] 1.3 Document the installer's `rsync` dependency

- [ ] 2 Constrain the managed development environment
  - [ ] 2.1 Declare an explicit Python floor compatible with repo code
  - [ ] 2.2 Declare explicit Conda channels for repeatable resolution
  - Depends On:
    - `1`

- [ ] 3 Add regression coverage
  - [ ] 3.1 Cover the managed-environment assumptions used by the wrapper and tests
  - Depends On:
    - `1`
    - `2`

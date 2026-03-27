- [ ] 1 Align workflow gating language
  - [ ] 1.1 Update `finish-feature` metadata to describe the accepted `[IN_PROGRESS]` handoff
  - [ ] 1.2 Update autonomous-loop guidance to route completed features through `finish-feature`

- [ ] 2 Clarify design-mode wording without changing behavior
  - [ ] 2.1 Rewrite `design-mode` language to mean "does not act on active execution work"
  - [ ] 2.2 Preserve the current sanity-check validation behavior
  - Depends On:
    - `1`

- [ ] 3 Single-source template and clean tracked history
  - [ ] 3.1 Make the renderer use the tracked feature template file as its source
  - [ ] 3.2 Remove the machine-local absolute-path leak from the historical feature record
  - [ ] 3.3 Add focused validation for template/render alignment and the targeted history repair
  - Depends On:
    - `1`
    - `2`

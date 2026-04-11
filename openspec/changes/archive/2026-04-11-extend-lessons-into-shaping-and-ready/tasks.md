## 1. Contract Updates

- [x] 1 Update `docs/planning/WORKFLOW_REFERENCE.md` and any affected feature-file guidance so the canonical lesson lifecycle explicitly includes shaping-stage and readiness-stage retrieval, usage reconciliation, lesson capture, and consistent stage-scoped handoff-note lines
  - [x] 1.1 Update `docs/planning/WORKFLOW_REFERENCE.md` so the canonical lesson lifecycle explicitly includes shaping-stage retrieval, usage reconciliation, and lesson capture
  - [x] 1.2 Update `docs/planning/WORKFLOW_REFERENCE.md` so the canonical lesson lifecycle explicitly includes readiness-stage retrieval, usage reconciliation, and lesson capture
  - [x] 1.3 Update any affected feature-file guidance or templates so planning-stage lesson handoff notes use consistent stage-scoped canonical lines

## 2. Workflow Skill Integration

- [x] 2 Update the planning-stage workflow skills so they retrieve lessons before stage decisions, record usage before exit, and capture reusable planning lessons without introducing a separate planning-only lesson system
  - [x] 2.1 Update `skills/shape-backlog-item/SKILL.md` to retrieve relevant lessons before shaping is finalized, record planning-stage lesson usage before exit, and capture new reusable lessons at stage close
  - [x] 2.2 Update `skills/ready-feature/SKILL.md` to retrieve relevant lessons before the independent readiness review, record readiness-stage lesson usage before exit, and capture new reusable lessons at stage close
  - [x] 2.3 Keep the execution and finish-stage lesson lifecycle docs coherent with the new planning-stage flow without introducing a separate planning-only lesson system

## 3. Validation

- [x] 3 Add the narrowest relevant validation coverage for planning-stage lesson handoff behavior and verify the updated workflow contracts
  - [x] 3.1 Add or update narrow workflow tests for any helper, template, or parser behavior introduced by planning-stage lesson handoff state
  - [x] 3.2 Validate the updated workflow docs and skill contracts with the narrowest relevant checks, including `audit-workflow` and any affected repo tests

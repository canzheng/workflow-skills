# Workflow Skills v2 Feature List

Version: 1.0 • Baseline: 2026-10-04 • Target: `canzheng/workflow-skills`

This is the executable breakdown for the v2 rewrite. Read [the design](v2-design.md) for architectural decisions and [the capability map](v2-capability-map.md) for coverage and scenario definitions. The complete required implementation scope is **WF2-F01 through WF2-F14**. F01 is the starting point; do not first perform a v1 simplification project.

Copy these three files together into `docs/v2/`. Use the launch instruction below in Codex Cloud. No previous chat history is required.

## 1. Launch instruction

```text
Implement the workflow-skills v2 rewrite in this repository. Read
docs/v2/v2-feature-list.md, docs/v2/v2-design.md, and
docs/v2/v2-capability-map.md, then execute WF2-F01 through WF2-F14 in
dependency order. These files define the approved rewrite scope.

The v2 process replaces the obsolete repository-local v1 workflow process
for this rewrite. Perform the bounded instruction cutover in F01; preserve
unrelated project rules and all higher-level host policies. Do not require
the old start-task/complete-task wrappers to build their replacement.

Make routine implementation choices yourself. Implement code, tests,
necessary documentation, and migration/retirement work. When available,
you may create/update the corresponding GitHub Issues, labels, and draft
PRs, and publish the implementation branch. Preserve human edits and
reconcile existing items before creating new ones. Do not merge PRs,
publish a release, change repository protection rules, or change my global
skills/configuration without separate authorization.

Continue through all dependency-ready work within this run rather than
stopping after a plan or after each feature. Use the documented bootstrap
fallback if GitHub writes are unavailable. If a runtime/access limit blocks
completion, finish independent work and leave the exact branch/revision,
evidence, pending features, and next action. Never label unrun validation,
unpublished changes, or unmerged work as delivered.
```

This instruction authorizes a bounded implementation batch and related GitHub records; it does not supply missing service permissions. A Cloud run may need continuation. The repository artifacts and checkpoints must make continuation straightforward.

## 2. Execution protocol

### 2.1 First run and instruction cutover

Read the applicable host/repository instructions and the three v2 files. Inspect the working tree, branch, source revision, and current repository state. Preserve unrelated or uncommitted work. Record the baseline SHA before changing active workflow files. The design was researched at `27f86db43ad895a78e214a453df2069868118cb7`; do not reset a newer checkout to that revision.

F01 explicitly replaces v1's repository workflow routing for this rewrite. Preserve unrelated coding and safety constraints. Update the root instruction entrypoint early so later sessions do not reactivate old wrappers. Do not modify global files or higher-priority policies. If actual higher-level policy conflicts with this implementation, state the conflict and continue unaffected work; do not invent an override.

The delivered v2 skills are not prerequisites to implement F01–F05. Follow the contracts in these files directly until their corresponding entrypoints exist. Do not install v1 globally in Cloud to get started.

### 2.2 Working branch and feature dependencies

Default to a dedicated rewrite branch with coherent feature-level commits. Reuse a Cloud-isolated checkout; do not create redundant worktrees. A feature normally maps to one GitHub Issue, not necessarily one PR. Keep PR boundaries reviewable. One rolling draft rewrite PR is acceptable; split milestone PRs when the host supports it without forcing a merge pause after every feature.

Dependencies in this file mean the prerequisite output is present and sufficiently verified in the selected branch. They do not require every prerequisite to have merged before work can continue on the same authorized integration branch. Record that coupling in Issues/PRs. On separate branches, base work on the verified prerequisite branch/commit or wait for integration; do not pretend dependencies exist on the default branch.

Do not mark a prerequisite Done because a dependent feature can begin. Issue delivery still requires the full definition of done. Use non-closing references until all acceptance obligations of the referenced Issue are included in the delivering merge.

### 2.3 GitHub publication and no-write bootstrap

When GitHub access exists, create/reuse one rewrite parent Issue and feature Issues with stable body markers such as `<!-- workflow-source: WF2-F06 -->`. Search open and closed Issues before creation, preserve existing human edits, and keep a link-only mapping in the rewrite parent. GitHub owns live status. Do not add status checkboxes to this catalog as a parallel board.

When read/write access is missing, proceed serially from this approved catalog. Keep implementation commits and a concise append-only checkpoint in the active rewrite change's existing `tasks.md` or a linked handoff section. Record completed technical work, tested revision, evidence, pending scope, and exact next action. This is temporary execution evidence, not an alternative shared backlog. Do not invent Issue numbers, claim remote labels changed, or build an outbox/synchronization service.

When access returns, reconcile actual commits/PRs and existing Issues before publishing. Generated Issue bodies can be temporary outputs reproduced from this catalog; they are not authoritative live state. After publication, stop editing local lifecycle status and use GitHub. Retain historical checkpoint evidence where it belongs.

### 2.4 Per-feature delivery practice

For each feature: read its relevant design sections and capability/scenario entries, inspect the affected code, implement the smallest complete result, run focused meaningful checks, reassess documentation against the final diff, and record acceptance evidence. Broaden tests for a concrete integration risk or required gate. Do not defer all documentation and testing to the last feature.

Update the architecture document only for what exists at the branch revision. Keep target-only design explicitly labeled. If a contract cannot be implemented as specified, record the constraint and propose the smallest decision needed; do not silently weaken acceptance or modify tests to hide the gap.

Do not perform mandatory subagent orchestration or duplicate ordinary review into multiple invented review rounds. A specific risk or project requirement can justify additional review.

### 2.5 Feature result record

Use the PR/Issue, or the bootstrap checkpoint when remote writes are unavailable. A compact record is sufficient:

```text
Feature: WF2-Fxx
Scope implemented: ...
Revision / tested content: ...
Acceptance evidence: criterion -> command/inspection -> result
Documentation: paths updated, or a reasoned no-impact explanation
Review / integration / remote publication still pending: ...
Next action: ...
```

A completed implementation record does not itself close the GitHub Issue. Required Cloud, Ubuntu, permission, and enforcement tests must be reported separately when unavailable.

## 3. Ordered feature index

The default execution order below is already topological. All rows are required for the initial release; optional follow-ons are listed separately at the end.

| ID | Feature | Dependencies | Primary capabilities | Milestone |
| --- | --- | --- | --- | --- |
| WF2-F01 | Establish rewrite baseline and repository contract | None | C01, C16 | A |
| WF2-F02 | Make development and verification portable | F01 | C02 | A |
| WF2-F03 | Build safe repository-scoped setup and doctor | F02 | C01, C03 | A |
| WF2-F04 | Define GitHub delivery records and templates | F01, F02 | C04, C13 | A |
| WF2-F05 | Implement design to backlog skill | F04 | C05 | A |
| WF2-F06 | Implement issue delivery and documentation completion | F02, F04, F05 | C06, C07, C10, C16 | A |
| WF2-F07 | Integrate proportional OpenSpec and plan handling | F06 | C08 | B |
| WF2-F08 | Implement targeted risk review and retained lessons | F06 | C09, C15 | B |
| WF2-F09 | Support remote operations, evidence, and environment handoffs | F04, F06 | C02, C10, C11, C13, C16 | B |
| WF2-F10 | Add executable delivery checks and CI integration | F03, F07, F08, F09 | C04, C07, C10, C12 | B |
| WF2-F11 | Prove behavior with workflow scenarios and negative controls | F05, F07, F08, F09, F10 | C07, C09, C12, C15 | B |
| WF2-F12 | Build v1 migration inventory and cutover procedure | F03, F04, F09 | C13, C14 | C |
| WF2-F13 | Remove v1 files and reconcile the final v2 tree | F11, F12 | C01, C08, C15 | C |
| WF2-F14 | Run Cloud and Ubuntu acceptance and prepare release | F13 | C02, C08, C11, C12, C16 | C |

Milestone A: usable core with local/fixture proof. Milestone B: complete delivery and verification behavior. Milestone C: migration, retirement, and actual environment acceptance. Milestones are review groupings, not additional lifecycle states or required merge stops.

## 4. Feature specifications

### WF2-F01 Establish rewrite baseline and repository contract

**Outcome:** A new Codex session can begin and resume the rewrite without invoking the obsolete v1 engine.

**References:** design sections 1–4, 11–12; capabilities C01/C16; scenarios S04/S25/S29. **Dependencies:** none. **Risk:** instruction conflicts and history loss.

**Deliverables**

- Baseline and asset inventory in `docs/migration-v1-v2.md`, including current branch/SHA, dirty-tree observations, active v1 work, and proposed dispositions.
- Updated root `AGENTS.md`, `docs/README.md`, and a concise `docs/workflow/contract.md` covering ownership, documentation, evidence, and completion. Update any conflicting active `CLAUDE.md` workflow routing.
- A bounded `openspec/changes/workflow-v2-rewrite/` proposal/design/tasks structure referencing the three supplied files. Bootstrap files may be authored without requiring an unavailable CLI; F07 validates them with the selected version.
- Initial `.workflow/config.json` schema/example and a current-versus-target documentation convention.

**Acceptance**

1. Baseline is recorded without resetting or discarding newer work. The inventory identifies the real v1 artifacts and active work instead of assuming all projects match the researched snapshot.
2. Repository instructions clearly select v2 for this rewrite and no longer require `start-task`, `complete-task`, v1 audits, or global installation. Unrelated rules remain.
3. During the transition, retained `docs/planning/` does not select v1. F13 removes that v1-only tree from the final source checkout. The default instructions do not claim unimplemented v2 commands exist.
4. The three input documents are linked and discoverable. The rewrite change references their scope without copying full designs or creating another editable backlog.
5. The delivery contract includes documentation assessment, truthful evidence, scope limits, and no premature completion.

**Verification:** inspect the final instruction chain in a fresh context; compare preserved instruction sections and historical files; check local links. Add only focused checks that prevent real routing regressions. Do not manufacture a v1 feature to authorize the rewrite.

**Documentation with this feature:** migration baseline, document navigation, contract, bootstrap instructions. **Not included:** new skill implementations or a blanket deletion of v1 code.

### WF2-F02 Make development and verification portable

**Outcome:** Development and tests can run in a clean Cloud or Ubuntu checkout through documented commands.

**References:** design sections 4.4, 9; C02; S02/S16/S29. **Dependencies:** F01. **Risk:** environment-dependent success.

**Deliverables**

- A minimal pinned Python development environment and portable verification entrypoint; use standard-library runtime helpers unless a dependency has a concrete need.
- Explicit supported versions and setup commands in `docs/development.md`; optional Conda guidance separated from the required path.
- A Cloud preparation recipe that calls repository commands and checks actual installed versions, including changed dependencies after the environment was published.
- Initial hermetic fixture-test structure for v2; keep any still-relevant legacy validation explicitly identified during transition.

**Acceptance**

1. Documented setup and verification work without Conda, a pre-existing `.agents` directory, or global AGENTS file.
2. Setup can be rerun. No command silently falls back to an unrelated interpreter or hard-coded developer path.
3. Offline/hermetic tests require no GitHub token. Missing optional GitHub or OpenSpec access is distinguished from a failed required local test.
4. Runtime/package versions are captured and pinned appropriately. No unsupported exact version is invented from memory.
5. The CI/local entrypoint actually executes the selected tests. Disabled or retired legacy tests are disclosed with rationale rather than silently omitted to obtain a green suite.

**Verification:** a temporary virtual environment or clean container; run the documented commands and a missing-dependency case. Actual Cloud acceptance is repeated in F14.

**Documentation with this feature:** setup, test commands, environment assumptions, and troubleshooting. **Not included:** migrating the entire repository to a new packaging framework without need.

### WF2-F03 Build safe repository-scoped setup and doctor

**Outcome:** A bounded v2 bundle can be installed, updated, inspected, and removed without touching user-global configuration.

**References:** design section 4; C01/C03; S01/S03/S04/S05. **Dependencies:** F02. **Risk:** destructive or partial filesystem writes.

**Deliverables**

- Public `setup` dry-run/apply/update/uninstall behavior, repeatable pinned dependency `bootstrap`, and read-only `doctor`.
- Versioned install provenance with managed-file hashes and source commit identity.
- Consumer assets for a delimited AGENTS entrypoint, config, contract, templates, utilities, and the three canonical skill directories.
- Tests using minimal valid fixture bundles before all production skills exist; assembly of the real bundle once F05/F06/F08 are available.

**Acceptance**

1. Fresh-target setup has no hidden global prerequisite and preserves unrelated repository files/instructions.
2. Complete preflight precedes writes; malformed markers, source omissions, escaping paths, or unmanaged collisions fail safely.
3. Repeating unchanged setup is a no-op. An update detects modified owned files and preserves them instead of overwriting.
4. Injected apply failure restores original content or reports exact recoverable residuals; rerun succeeds after resolution.
5. Uninstall removes only unmodified managed assets and the managed instruction block, retaining user-owned documents/configuration as documented.
6. Doctor reports malformed config, active legacy routing, supported tool availability, and discoverable duplicate skills. It never deletes global skills or claims to inspect inaccessible host locations.
7. Incomplete production bundle assembly is a reported failure, not a falsely successful install of missing skills.
8. Adoption tracks project-owned files and the exact dependency pin, ignores only the three shared skill directories, and never alters the Git index. Project-specific skills remain trackable; old tracked shared files require reviewed untracking.
9. Bootstrap materializes/verifies the tracked full-SHA dependency without rewriting project policy/config/docs or using latest/global installation. Repetition is a no-op; missing/modified/extra/symlinked assets, denied fetch and pin mismatches have meaningful negative coverage (S34).
10. Cloud/local environment setup fetches a pinned source-owned entrypoint without copying it into the target; a fresh Git root needs no tools or first commit. Existing adoption retains its tracked pin on repeated runs. Source README documents Cloud install-script and local setup. Cloud/Ubuntu preparation and consumer CI run bootstrap before discovery/verification. Actual host discovery and same-pin environments are established separately in F14.

**Verification:** public CLI tests in temporary Git repositories, including dirty/modified files, symlinks, spaces in paths, partial failure, and provenance mismatch. At F14 verify actual skill discovery, beyond filesystem presence.

**Documentation with this feature:** setup/update/uninstall procedure and ownership/conflict policy. **Not included:** global installer compatibility, automatic repository discovery, or general plugin distribution.

### WF2-F04 Define GitHub delivery records and templates

**Outcome:** GitHub can represent v2 work without reintroducing the local feature ledger.

**References:** design section 5; C04/C13; S06/S07/S22/S23. **Dependencies:** F01/F02. **Risk:** duplicated or misleading state.

**Deliverables**

- Feature and bug Issue forms, a PR template, and documented phase/modifier labels.
- Readiness, dependency, blocked/deferred, cancel/reopen, parent/child, and final-closure guidance.
- A reproducible way to render this catalog into Issue bodies with stable source IDs. A simple template/script is sufficient; no queue engine.
- When launch authorization and access permit: create/reuse the rewrite parent and feature Issues, and publish a link-only mapping. Otherwise retain exact reproducible Issue bodies as temporary output and continue implementation.

**Acceptance**

1. Templates capture outcome, scope/exclusions, verifiable acceptance, design/spec links, dependencies, risks/environment, and documentation impact without requiring meaningless empty artifacts.
2. Open Issues have one phase and optional modifiers; completed and cancelled closure are distinct. Unrelated labels survive updates.
3. The model supports a small ready bug without an OpenSpec change and a parent with multiple child Issues/PRs.
4. Partial PRs use non-closing references. Parent closure requires aggregate acceptance, not one merged child.
5. Source-ID lookup checks open and closed matches; rerun reuses one match and rejects ambiguity.
6. No live status or priority is written back into the three design files. GitHub Projects is optional.

**Verification:** render and inspect representative forms/bodies; use remote-operation fixtures for rerun and lifecycle cases. Confirm any actual writes individually; inaccessible GitHub publication is pending integration, not failed local template implementation.

**Documentation with this feature:** lifecycle, source-ID mapping, record examples, and closing rules. **Not included:** Projects API integration, automated scheduling, or a closure bot.

### WF2-F05 Implement design to backlog skill

**Outcome:** An agent can turn a high-level design into a persistent, scoped, implementable backlog.

**References:** design sections 3, 5.3, 6.1; C05; S08/S09/S33. **Dependencies:** F04. **Risk:** hidden scope expansion or loss of design intent.

**Deliverables**

- `.agents/skills/workflow-design-to-backlog/SKILL.md` with focused triggering, inputs, outputs, boundaries, and stopping conditions.
- Only the references/templates needed for decomposition and readiness decisions.
- Representative input/output evaluation cases covering a new design and refinement of existing Issues.

**Acceptance**

1. The skill reads current implementation/contracts and distinguishes them from proposed design.
2. Agreed design intent is saved in appropriate project documents. Issue bodies reference that design without copying the whole document.
3. Decomposition produces bounded outcomes, explicit dependencies, and concrete acceptance rather than internal task ceremony.
4. A genuinely unresolved decision becomes a discovery item or blocks only affected readiness. Excluded enhancements remain excluded.
5. Candidate creation does not imply permission to execute. A user-approved batch can proceed without repeated product approval requests for the same scope.
6. Rerunning on an existing design updates/reuses candidates by identity and preserves human changes.
7. The default initial/MVP backlog is a single coherent batch from supplied existing design documents, with no mandatory persisted decomposition or repeated per-Issue invocation. Detailed intent is translated faithfully; high-level intent is shaped proportionally.
8. One batch approval enables specified dependency-ready Issues, keeps later/unresolved/unsatisfied work backlog/blocked appropriately, and never starts implementation unless execution is separately requested.
9. Delivery-level outcomes, stable logical identities, direct confirmed dependency links and design-section references provide lightweight design→Issue→PR traceability without coding-task Issue explosion or another editable backlog.

**Verification:** run the skill against a sample design containing a usable first release, optional enhancements, one dependency, and one unknown. Inspect actual output artifacts. Static SKILL.md validation alone is insufficient. S33 uses a fresh realistic project design with explicit MVP/later scope/dependencies/one unknown, one batch approval and no implementation dispatch; distinguish fixture proof from actual consumer GitHub/Cloud execution.

**Documentation with this feature:** usage example from high-level design to Issues and the skill's precise scope. **Not included:** a prioritization algorithm or mandatory complete-system design before any implementation.

### WF2-F06 Implement issue delivery and documentation completion

**Outcome:** An agent can implement a bounded Issue and prepare a truthful, documented delivery.

**References:** design sections 6.2, 7, 10–11; C06/C07/C10/C16; S10/S11/S12/S14/S22. **Dependencies:** F02/F04/F05. **Risk:** incomplete delivery represented as done.

**Deliverables**

- `.agents/skills/workflow-deliver-issue/SKILL.md` with Issue and approved-bootstrap-feature inputs.
- Documentation-impact guidance linked to the single delivery contract.
- Evidence and PR output examples; simple-feature and bug evaluation cases.

**Acceptance**

1. Skill resolves the intended assignment and checkout, reads issue-linked design/specs, and respects scope/dependency availability.
2. Ordinary work completes without mandatory per-task plans, feature files, wrapper audits, or independent subagents.
3. Documentation impact is assessed at start and against the final diff. A config/operation change includes accurate instructions and verified examples.
4. A valid no-document-change rationale is accepted for a repair that leaves current docs true. Missing required documentation stays unfinished.
5. Results distinguish implemented, locally verified, integration pending, review-ready, and delivered. Open PR or passing local tests cannot substitute for required merge/integration acceptance.
6. A bug fix preserves the original acceptance contract and discriminating tests; a changed contract is raised explicitly.
7. Skill produces a reviewable branch/PR with evidence and next actions even when remote publication is unavailable; it makes no fabricated remote claims.

**Verification:** actual small feature and reproducible bug fixtures; include a new config option with intentionally stale docs and an internal repair with no doc impact. F11 adds cross-scenario adversarial cases.

**Documentation with this feature:** ordinary delivery walkthrough, documentation matrix, progress vocabulary, PR evidence example. **Not included:** a persistent internal task resolver or forced review pipeline.

### WF2-F07 Integrate proportional OpenSpec and plan handling

**Outcome:** Complex changes preserve behavior and design without forcing every fix through a full change lifecycle.

**References:** design section 8; C08; S11/S15/S24. **Dependencies:** F06. **Risk:** specs describing unimplemented behavior or early archive.

**Deliverables**

- OpenSpec decision guidance in the relevant skills and contract, with a tested pinned tool/schema version.
- Single-plan rules and examples for change-owned versus non-OpenSpec long-running plans.
- Initial implemented v2 behavior specs and validation of the active rewrite change.
- Single-PR and multi-PR archive examples/tests.

**Acceptance**

1. Small fixes to clear existing behavior do not require a new change directory; inaccurate existing specs are still maintained.
2. Significant behavior or migration risk triggers suitable proposal/design/tasks/spec work.
3. The same work does not have both a change-owned implementation plan and duplicate `docs/plans` or per-task plans.
4. A multi-PR change has a clear closing owner. Intermediate work cannot archive pending scope or claim target behavior as current.
5. Final archive/spec synchronization and durable-document consolidation occur with the delivering code or remain an explicit open obligation.
6. OpenSpec structural validation is run through actual supported commands, and is not represented as proof of implemented behavior.

**Verification:** execute pinned CLI validation/archive on disposable fixtures, inspect before/after current specs, and show that a partial change cannot satisfy final closure. Verify active v2 docs do not inherit the old blanket prohibition on OpenSpec apply.

**Documentation with this feature:** selection criteria, plan homes, archive ownership, and command versions. **Not included:** custom OpenSpec schema machinery unless required by a demonstrated incompatibility.

### WF2-F08 Implement targeted risk review and retained lessons

**Outcome:** High-risk changes get specific proof methods while ordinary work remains lightweight.

**References:** design sections 6.3, 10.4; C09/C15; S19/S20/S21/S30. **Dependencies:** F06. **Risk:** weak fixtures, contract drift, missing negative paths.

**Deliverables**

- `.agents/skills/workflow-risk-review/SKILL.md` and concise references for relevant risk categories.
- Translated L-001/L-002 guidance with links to concrete regression cases.
- Examples for numerical/data semantics, migrations, permissions, filesystem operations, remote writes, and producer/consumer contracts.

**Acceptance**

1. Triggering follows material risk and does not mandate a separate review for every ordinary change.
2. Findings identify the actual contract/risk and missing proof, not generic checklist completion.
3. Numerical fixtures distinguish a plausible wrong result using an independently established expectation.
4. A parsed/emitted contract without a real consumer is insufficient; a missing resource cannot silently select an unrelated target.
5. Contract-weakening remediation is detected and cannot be accepted without an explicit approved behavior change.
6. Review authorship and independence are reported honestly; no invented separate reviewer or assumed subagent invocation.

**Verification:** deliberate negative controls for wrong formula, parser-only metadata, missing target, and assertion weakening. Test the skill's selection/analysis behavior as well as utility behavior. Reuse existing good fixtures where their outcome remains relevant.

**Documentation with this feature:** risk selection, expected proof, retained lessons. **Not included:** lesson counters, compulsory notes after every task, or a custom reviewer orchestration framework.

### WF2-F09 Support remote operations evidence and environment handoffs

**Outcome:** Work can resume across failures, sessions, and Cloud/Ubuntu boundaries without duplicate writes or false verification.

**References:** design sections 5.4, 9, 11; C02/C10/C11/C13/C16; S16/S17/S18/S23/S26/S28. **Dependencies:** F04/F06. **Risk:** wrong target, ambiguous remote outcomes, stale evidence.

**Deliverables**

- Skill guidance and small adapters only where needed for available host tools/`gh`; no custom GitHub SDK framework.
- Read-only capability diagnostics and a handoff example containing repo, Issue/feature, branch/SHA, document paths, evidence, blockers, and next action.
- Operation fixtures covering creation timeout, permission failure, repeated writes, and concurrent human edits.
- Revision/content-aware evidence conventions, including dirty-tree handling.

**Acceptance**

1. Missing GitHub write permission does not stop authorized local implementation or masquerade as successful state synchronization.
2. Creation/update retries reconcile current remote state first, preserving unrelated labels/body content and detecting duplicate source identities.
3. Ambiguous ownership or target blocks only that work; missing worktree/branch never falls back to the current directory.
4. A fresh session can resume from the recorded checkout/revision without previous chat context.
5. Ubuntu-required verification remains pending until actually run on the intended content. Cloud passes do not substitute for it.
6. Material changes invalidate affected evidence. Results from a dirty tree are tied to actual tested content and cannot certify an unrelated commit.
7. Read/write/authentication capabilities are tested separately; no raw credentials appear in logs or output.

**Verification:** operation fault fixtures and a handoff to a clean session. Exercise actual GitHub reads/writes only in an authorized test scope; report fixture-only proof separately. Real two-environment acceptance is F14.

**Documentation with this feature:** continuation procedure, capability failures, remote retry rules, evidence/retention guidance. **Not included:** distributed locking, an automated issue claimer, or cross-environment remote execution service.

### WF2-F10 Add executable delivery checks and CI integration

**Outcome:** Mechanical obligations run through real entrypoints and PR events, with their limits stated accurately.

**References:** design sections 4.4, 7, 10.3; C04/C07/C10/C12; S12/S13/S22/S27/S28/S31. **Dependencies:** F03/F07/F08/F09. **Risk:** checks that look authoritative but do not enforce the claimed behavior.

**Deliverables**

- Local `check` entrypoint for schema/bundle integrity, local links, relevant spec validation, and declared PR-section structure.
- Actions for v2 tests/checks and PR metadata validation with appropriate event coverage.
- A required-check/ruleset setup runbook and read-only enforcement verification instructions.
- Project review rules focused on semantic documentation consistency and acceptance rather than formatting already checked in CI.

**Acceptance**

1. Public commands, templates, and CI use consistent contract rules; no check only parses fields that nothing consumes.
2. Missing PR evidence/documentation sections and broken referenced local paths fail with actionable findings. A no-impact statement is allowed but remains subject to semantic review.
3. PR body edits refresh metadata checks; code/head updates refresh affected tests. Metadata is handled as data and cannot execute commands.
4. Metadata checks use trusted code/read-only permissions; no privileged workflow executes untrusted PR code.
5. Required-check setup is documented and observed separately from file creation. Do not claim merge protection exists because a workflow YAML file exists.
6. Manual Issue closure is recognized as outside PR merge protection. An on-demand read-only audit can flag inconsistent completed claims; a closure bot is unnecessary.
7. Semantic documentation truth is not falsely advertised as mechanically proven.

**Verification:** CI event fixtures, malicious metadata strings, failing and passing local checks, and actual Actions when available. Do not require admin access to complete the code/runbook; leave live enforcement configuration pending for F14 if unavailable.

**Documentation with this feature:** checks, known limits, repository settings, review responsibilities. **Not included:** a generic documentation semantic engine or automatically changing repository permissions.

### WF2-F11 Prove behavior with workflow scenarios and negative controls

**Outcome:** The rewrite is tested through actual consumer paths and agent behavior, beyond document/schema consistency.

**References:** design sections 10.4, 13; C07/C09/C12/C15; full scenario catalog, especially S10–S15/S19–S21/S27. **Dependencies:** F05/F07/F08/F09/F10. **Risk:** self-confirming tests.

**Deliverables**

- A small scenario corpus with prompts/input fixtures, expected outcomes, prohibited outcomes, execution procedure, and evidence format.
- Public-path deterministic integration tests for setup/check/consumer behavior.
- Host-driven or manual skill evaluations for semantic obligations; recorded outcomes distinguish actual runs from proposed cases.
- Traceability from capabilities to scenarios and implementation paths.

**Acceptance**

1. Ordinary feature, bug, cross-module change, and high-risk case each exercise a real intended usage path.
2. Documentation omission, documentation contradiction, and legitimate no-impact cases all behave correctly.
3. At least one deliberately broken consumer/target/fixture causes the relevant proof to fail. Do not rely solely on test names or assertions matching implementation.
4. Instructions are tested for triggering and resulting artifacts; static lint does not count as full skill verification.
5. Negative control failure is shown for the intended reason; passing tests cannot hide skipped required checks or broadened expected outputs.
6. Tests are focused on v2 outcomes; no mandatory model API harness, paid service dependency, or exhaustive mutation platform is introduced.

**Verification:** run the deterministic suite and available skill evaluations; inspect outputs and failure reasons. Record environment/model only for reproducibility, not as a permanent product dependency. Carry unavailable actual Cloud runs to F14.

**Documentation with this feature:** test/evaluation procedure and coverage/limitations. **Not included:** a new evaluation product or claims that one successful prompt proves universal reliability.

### WF2-F12 Build v1 migration inventory and cutover procedure

**Outcome:** Known v1 projects can move active work to GitHub with one authority and preserved provenance.

**References:** design section 12; C13/C14; S04/S23/S25/S32. **Dependencies:** F03/F04/F09. **Risk:** lost work and dual ownership.

**Deliverables**

- `migrate inspect` for known v1 records, producing an inventory and proposed dispositions without mutations.
- A guided, reviewable one-time cutover procedure using ordinary GitHub tools for authorized creation/update.
- Old feature-ID/Issue mapping and explicit history/rollback treatment.
- Migration fixtures for active, completed, deferred, inconsistent, duplicate, and missing-change records.

**Acceptance**

1. Inventory distinguishes historical Done records from remaining work and preserves relevant acceptance, specs, evidence, and blockers.
2. Empty active backlog, as observed in the reference repository, is valid; no fake migration Issues are created.
3. Missing/ambiguous records produce findings and a manual resolution path, not guessed state.
4. Each active item has one explicit disposition: finish v1, migrate, defer, or cancel. Migrated items stop being writable in the v1 ledger.
5. Retried partial migration reconciles existing remote IDs and preserves human edits; it does not recreate completed history or duplicate Issues.
6. Rollback restores code/instruction ownership deliberately without deleting remote history or reviving two-way synchronization.

**Verification:** known-format fixtures, interrupted migration, duplicate IDs, missing OpenSpec change, and read-only behavior. Reuse safe parsing code only if it does not pull in the old runtime engine.

**Documentation with this feature:** item dispositions, exact cutover steps, mapping, ambiguous cases, and rollback limits. **Not included:** universal legacy parser support or automatic migration of all the user's repositories/global installations.

### WF2-F13 Remove v1 files and reconcile the final v2 tree

**Outcome:** A fresh clone and installed consumer bundle present one coherent v2 system without a parallel v1 file tree.

**References:** design sections 1.3, 8, 12; C01/C08/C15; S04/S15/S24/S25. **Dependencies:** F11/F12. **Risk:** obsolete instructions/specs remaining active.

**Deliverables**

- Remove v1-only files from the checked-out source tree, including `AGENTS-global-workflow.md`, the legacy `skills/` tree (including `skills/_workflow/` and all wrapper directories), `docs/planning/`, `docs/superpowers/`, v1-only lesson records, ceremony-specific tests, and v1-only current or archived OpenSpec artifacts. Delete or replace the old `install.sh` in place with the v2 setup entrypoint; it must not retain global-install behavior.
- Migrate or retire v1 tests by the capability they protect. Preserve the old implementation through the recorded baseline commit and Git history, without copying it into a new in-tree legacy directory.
- Update README, current architecture, development/operations docs, templates, and any active alternate-agent routing.
- Reconcile current OpenSpec contracts and prepare the final documentation/spec consolidation. Leave the rewrite change active for F14 acceptance and archive.

**Acceptance**

1. A fresh clone and fresh v2 setup contain exactly the intended v2 skill bundle and no v1 resolver, wrapper, feature board, feature file, Superpowers artifact, or old global workflow policy.
2. Current docs/specs describe v2 behavior. V1 provenance remains reachable through the recorded baseline SHA, old-ID mapping, and Git history rather than checked-in duplicate history.
3. Useful safety regressions remain in the v2 suite; deleted ceremony-specific tests have a documented disposition.
4. No task ledger, current-task pointer, or two-way Markdown/GitHub status sync has reappeared under a new name.
5. Current architecture explains the actual implementation without requiring all historical changes to be read.
6. Required implementation/docs obligations are reconciled, but pending F14 acceptance is visible in the still-active rewrite change. Do not archive it at F13 to make the repository look finished.
7. A reviewed asset-disposition manifest accounts for every path identified by F01 as delete, translate/move, or current v2. No unexplained v1-only path remains in the final tree.

**Verification:** compare the final tree with the F01 asset inventory, inspect the installed bundle and instruction chain, run the v2 suite, and search for retired filenames, skill names, and commands. Manually classify legitimate migration-document references, which may name old paths but may not contain runnable copies. Clone the candidate branch into a clean directory and verify the deleted v1 paths do not reappear.

**Documentation with this feature:** final current system docs, asset-disposition table, baseline Git reference, and global-v1 cleanup guidance for users who installed it previously. **Not included:** deleting historical Git commits, modifying global skills automatically, or publishing a release.

### WF2-F14 Run Cloud and Ubuntu acceptance and prepare release

**Outcome:** The implementation has concrete evidence that it works in the intended operating model, with any remaining external actions identified precisely.

**References:** design sections 8–13; C02/C08/C11/C12/C16; S01/S02/S10/S11/S15/S17/S29/S31 and remaining scenario gaps. **Dependencies:** F13. **Risk:** declaring the rewrite complete from local structural checks alone.

**Deliverables**

- Actual fresh Cloud setup/discovery/execution evidence for the real bundle.
- Cloud-to-Ubuntu same-revision setup/verification handoff and result when that environment is available.
- Representative ordinary-feature, bug, cross-module, and high-risk pilot outcomes using the delivered workflow.
- Release-readiness report in a PR or `docs/validation/v2-acceptance.md`, identifying capabilities proven, pending acceptance, active checks/enforcement, versions, and revision.
- Archive of the rewrite change only after required acceptance completes, with final specification/document checks rerun after the archive diff. If acceptance remains blocked, leave the change active with exact remaining work.
- Reviewable PR(s) and release/migration notes; publication/merge only with separate authorization.

**Acceptance**

1. Fresh Cloud task discovers the intended skills and follows the short contract; no global installation or previous chat is needed.
2. A resumed task can continue from the recorded branch/revision and evidence without redoing completed work or inventing remote state.
3. The portable setup/verify command works on Ubuntu for the tested revision, or this required environmental acceptance is explicitly still pending.
4. Real GitHub Issue/PR operations and CI are exercised when authorized; fixtures and actual integration results are clearly distinguished.
5. All mandatory scenario obligations have results. Missing access, failed runs, unperformed independent review, or unconfigured required checks cannot be reported as passed.
6. Repository enforcement is reported as configured/observed or pending configuration. Lack of administrative access does not trigger an attempt to bypass it.
7. Pilot records show whether extra confirmations, plans, documentation edits, or reviews were needed; no invented speedup metric.
8. Final report separates implementation complete, Cloud validated, Ubuntu validated, merge protection configured, merged, and released. Only achieved outcomes are claimed.
9. The completed rewrite change is archived in the delivering branch only after required acceptance is satisfied. Archive does not claim that the branch has merged or a release has been published.

**Verification:** real selected environments and repository, plus targeted reruns after defects are fixed. If this Cloud task cannot spawn a fresh independent task or reach Ubuntu, finish the implementation and produce exact test instructions/checkpoint for that remaining gate. Do not substitute a local directory for a Cloud discovery test or pretend missing infrastructure can be fixed by prose.

**Documentation with this feature:** actual acceptance evidence, supported environment versions, release notes, remaining setup steps. **Not included:** automatic merge, release publication, or new product scope discovered during the pilot.

## 5. Cross-feature acceptance and release gates

Implementation is ready for final review when F01–F13 outputs and relevant local/scenario checks are complete, the real bundle is assembled, current docs/specs match, and no retired runtime dependency remains. This is not yet a declaration that every external acceptance gate passed.

Before reporting the rewrite as fully validated, establish:

| Gate | Required evidence | If unavailable |
| --- | --- | --- |
| Core behavior | Scenario results tied to implemented consumer paths | Fix or keep relevant feature acceptance pending |
| Documentation | Final-diff assessment plus actual current content and semantic review | Keep affected delivery unfinished |
| Cloud adoption | Fresh task loads and uses intended bundle | Mark Cloud acceptance pending; provide exact start procedure |
| Ubuntu portability | Same-content setup/verify result on Ubuntu | Mark Ubuntu acceptance pending; preserve handoff |
| GitHub integration | Confirmed identity-safe Issue/PR operations and Actions results | Mark live integration pending; retain fixture proof separately |
| Enforcement | Read-back/observed required checks and ruleset behavior | Provide setup steps; do not claim active merge blocking |
| Migration | Safe known-format inventory/cutover/rollback proof | Keep migration acceptance pending |
| Integration/release | Reviewed merge and, if authorized, release | Report review-ready or merged accurately; do not self-authorize publication |

The agent must not turn an unavailable environment into an excuse to leave independent code/docs work unimplemented. Conversely, finishing implementation cannot waive an explicit environmental gate.

## 6. Handling discoveries and scope changes

Within a feature, Codex may reorganize code, select appropriate supported dependencies, strengthen fixtures, and improve wording. Keep IDs and observable acceptance stable. Record consequential implementation decisions in current docs or a small decision record.

If a feature is too large, split implementation into linked child Issues or several PRs while retaining its parent acceptance. Do not replace this catalog with dozens of mandatory per-task records. If a previously unknown product decision changes scope, explain the alternatives and proceed on unaffected work; approval applies only to the changed commitment.

If reality contradicts a platform assumption, update the operational detail and evidence while preserving the architectural constraints. For example, unavailable `gh` can use an exposed GitHub tool; it does not justify building another backlog database.

## 7. Explicitly deferred extensions

Do not implement these as part of the approved rewrite unless separately requested:

- Global/plugin marketplace packaging and automatic updates across many repositories.
- GitHub Projects field synchronization or custom dashboards.
- Autonomous monitoring/draining of unapproved backlog and product reprioritization.
- Distributed Issue locks or a hosted multi-agent coordinator.
- Automatic merge/release, repository-administration changes, or a manual-closure enforcement bot.
- A universal semantic documentation validator or a standalone model evaluation platform.
- Full backward compatibility for v1 skill names, task metadata, feature files, or legacy resolver APIs.

## 8. Expected final handoff

Report the implemented features and reviewable branch/PR, the exact tested revision, verification evidence, documentation changes, migration/retirement result, and any remaining Cloud/Ubuntu/GitHub/admin steps. Keep the summary concise and link to durable records.

Do not finish with only a plan, a list of files created, or an offer to start implementation later. Execute the authorized scope until complete or genuinely blocked, and leave a continuation point that the next session can use directly.

# Workflow Skills v2 Capability Map

Version: 1.0 • Baseline: 2026-10-04 • Target: `canzheng/workflow-skills`

This document defines what v2 must enable, which component owns each responsibility, and how the rewrite proves coverage. It complements [the design](v2-design.md) and [the feature list](v2-feature-list.md). It is a scope and traceability map, not an implementation-status dashboard.

All capabilities C01–C16 are in the first release. A capability can be implemented partly through instructions and partly through code; a capability is not a requirement to create a new script or skill. GitHub, Codex, and OpenSpec retain their native responsibilities.

## 1. Capability domains

| Domain | Capabilities | Intended result |
| --- | --- | --- |
| Adoption and execution environment | C01–C03 | A clean Cloud or Ubuntu checkout can use one known workflow bundle |
| Design and delivery | C04–C08 | Approved intent becomes bounded, documented, verifiable delivery |
| Quality and continuity | C09–C12 | Verification is meaningful and survives reviews and environment changes |
| Shared state and transition | C13–C16 | Remote changes, migration, and continuation remain honest and bounded |

## 2. Capability catalog

### C01 Explicit workflow selection and guidance

**Outcome:** Codex can determine that this repository uses v2 without inferring from historical directories.

- Inputs: root/nested instructions, `.workflow/config.json`, document index, and bundle provenance.
- Owner: root `AGENTS.md`, the delivery contract, and read-only doctor.
- Outputs: the applicable workflow and context paths, or a clear conflicting/missing configuration finding.
- Required behavior: preserve unrelated instructions; resolve active v1/v2 contradictions deliberately; keep historical records from activating v1; do not modify user-global configuration implicitly.
- Proof: during migration, retained `docs/planning/` does not trigger old wrappers; in the final `workflow-skills` head, v1-only planning artifacts are absent. Malformed markers and duplicate names are surfaced.
- Implements: **WF2-F01, WF2-F03, WF2-F13**. Design: sections 3, 4, 12. Scenarios: **S01, S03, S04, S25**.

### C02 Portable development and Cloud readiness

**Outcome:** Runtime tools and verification work in a clean supported environment without a preconfigured home directory or Conda.

- Inputs: pinned dependency definitions, repository revision, available runtime, and required checks.
- Owner: setup/development entrypoints and `docs/development.md`.
- Outputs: tested commands, supported versions, and separate findings for missing runtime, network, or authentication.
- Required behavior: check the actual Cloud profile; separate environment preparation from agent/runtime access; never assume local skills or credentials synchronize to Cloud.
- Proof: clean setup, setup rerun, dependency change after environment preparation, and unavailable GitHub write access.
- Implements: **WF2-F02, WF2-F09, WF2-F14**. Design: section 9. Scenarios: **S02, S16, S17, S29**.

### C03 Versioned repository bundle setup

**Outcome:** A consumer repository adopts or updates v2 without global installation or destructive overwrites.

- Inputs: explicit target repository, pinned source revision, current managed-file hashes, and apply intent.
- Owner: `setup` adoption/update, read-only `bootstrap` verification and tracked installation provenance.
- Outputs: dry-run diff; applied version and managed-file provenance; conflicts or rollback report.
- Required behavior: preflight before writes, recover from partial failure, preserve modified/user-owned files, reject unsafe targets, support no-op rerun and bounded uninstall.
- Proof: exercise the public setup command in temporary repositories, including failures after staging and during apply.
- Implements: **WF2-F03**. Design: sections 4.2–4.4. Scenarios: **S01, S03, S04, S05, S34**.

### C04 GitHub delivery identity and lifecycle

**Outcome:** Each delivery item has one shared identity and a truthful phase and outcome.

- Inputs: repository/Issue identity, approved scope, dependency links, and evidence.
- Owner: GitHub Issues/PRs, the short label convention, and the delivery skill.
- Outputs: candidate/Ready/active/review/blocked/deferred state or completed/cancelled outcome.
- Required behavior: exactly one phase for open workflow Issues; preserve unrelated labels; no premature parent closure; no Markdown status mirror; no claim that labels implement an atomic lock.
- Proof: partial PR, blocked work, reopen, cancellation, duplicate assignment, and final closure scenarios.
- Implements: **WF2-F04, WF2-F06, WF2-F09, WF2-F10**. Design: sections 5, 10. Scenarios: **S06, S07, S18, S22, S23**.

### C05 Design to bounded backlog

**Outcome:** A high-level design produces implementable candidate Issues without losing intent or expanding authorization.

- Inputs: design, current system, product constraints, explicit release scope.
- Owner: `workflow-design-to-backlog`.
- Outputs: durable design decisions, bounded outcomes, acceptance criteria, dependencies, risks, and linked candidate Issues.
- Required behavior: distinguish current and target behavior; expose unresolved decisions; separate candidates from approved Ready work; reuse existing source IDs when rerun.
- Proof: decompose a design containing a known core, an unresolved decision, and an attractive but excluded enhancement.
- Implements: **WF2-F05**. Design: sections 5.3, 6.1. Scenarios: **S08, S09, S33**.

### C06 Issue-level implementation and review preparation

**Outcome:** Codex completes a bounded assignment without a mandatory internal task lifecycle.

- Inputs: Issue or approved bootstrap feature, code, relevant documents, and available verification.
- Owner: `workflow-deliver-issue` and native Codex execution.
- Outputs: implemented change, tests, required documents, PR or reviewable branch, and remaining limitations.
- Required behavior: use the intended checkout, preserve scope, distinguish implemented/verified/merged/delivered, and continue independent work when a remote status update is unavailable.
- Proof: ordinary feature and bug delivered without a feature ledger, per-task plan, or forced independent reviewer.
- Implements: **WF2-F06**. Design: sections 6.2, 10, 11. Scenarios: **S10, S11, S16, S22**.

### C07 Documentation impact and completion

**Outcome:** The delivery updates the explanations that would otherwise become wrong or incomplete.

- Inputs: agreed design and final code/configuration diff.
- Owner: delivery contract, delivery skill, and ordinary PR review; mechanical checks assist.
- Outputs: accurate current docs/specs or a defensible no-impact statement; unresolved obligations remain visible.
- Required behavior: reassess at the end; distinguish target/current/history; verify changed commands; do not accept an arbitrary Markdown edit as completion.
- Proof: detect stale configuration guidance and semantic contradictions, while permitting an internal repair with no documentation change.
- Implements: **WF2-F06, WF2-F10, WF2-F11**. Design: section 7. Scenarios: **S12, S13, S14**.

### C08 Proportional specifications and durable plans

**Outcome:** Complex changes preserve a behavior contract and implementation reasoning without multiplying plans.

- Inputs: change scope, existing specs, ambiguity/risk, and continuation needs.
- Owner: OpenSpec plus the design and delivery skills.
- Outputs: necessary change artifacts, validated deltas, archive, current system documentation, or a small non-OpenSpec plan.
- Required behavior: no mandatory change for every fix; no duplicate `docs/plans` and change-owned plan; archive only completed scope; code/current specs align at the branch revision.
- Proof: simple bug bypasses change creation, significant behavior change uses it, multi-PR work does not archive early.
- Implements: **WF2-F07, WF2-F13, WF2-F14**. Design: section 8. Scenarios: **S11, S15, S24**.

### C09 Risk-specific validation and contract preservation

**Outcome:** Material risks receive discriminating proof rather than a uniform extra review stage.

- Inputs: diff, acceptance, risk category, and relevant historical failures.
- Owner: `workflow-risk-review`, tests, and reviewers when required.
- Outputs: concrete findings, suitable proof, and residual uncertainty.
- Required behavior: load relevant methods only; preserve test strength; use independent expected values for calculations; cover missing resources and negative authorization paths.
- Proof: a plausible wrong calculation fails; a schema-only implementation with no consumer fails; a contract-weakening bug fix is rejected.
- Implements: **WF2-F08, WF2-F11**. Design: sections 6.3, 10.4. Scenarios: **S19, S20, S21, S30**.

### C10 Revision-bound verification evidence

**Outcome:** A reviewer can determine what was tested, where, and against which content.

- Inputs: commands, exit/results, revision or patch identity, environment, and artifacts.
- Owner: delivery skill, CI, and PR evidence section.
- Outputs: concise durable result summary and raw artifact references when useful.
- Required behavior: distinguish passed/failed/skipped/blocked; invalidate affected evidence after changes; do not bind dirty-tree results to an untested commit; record artifact retention assumptions.
- Proof: modify executable content after a pass and ensure the pass no longer satisfies completion.
- Implements: **WF2-F06, WF2-F09, WF2-F10**. Design: sections 9.3, 10. Scenarios: **S17, S22, S28**.

### C11 Cloud and Ubuntu handoff

**Outcome:** Another session or environment can resume without relying on prior conversation memory.

- Inputs: repository, branch/SHA, assignment, existing plan/spec references, evidence, and pending integration work.
- Owner: delivery skill and a concise Issue/PR handoff.
- Outputs: an unambiguous next action on the intended content.
- Required behavior: do not guess missing branches/worktrees; preserve uncommitted work; avoid cloning a new plan on each handoff; use the same revision for integration proof.
- Proof: fresh context resumes; missing or ambiguous revision blocks that item; Ubuntu-required verification remains pending until actually run.
- Implements: **WF2-F09, WF2-F14**. Design: section 9.3. Scenarios: **S17, S26, S29**.

### C12 Mechanical checks and semantic review

**Outcome:** Deterministic checks catch what they can prove, and reviewers examine claims requiring judgment.

- Inputs: repository content, PR metadata, target/head revisions, and project review requirements.
- Owner: local checker, Actions, and native PR review.
- Outputs: actionable checks/findings and an honest report of active enforcement.
- Required behavior: real command-path tests; PR-body edits refresh metadata checks; head changes refresh code checks; untrusted metadata is data; checks do not certify semantic truth.
- Proof: valid structure with false documentation still fails semantic evaluation; an unsafe metadata string cannot execute; unconfigured rulesets are not reported as enforced.
- Implements: **WF2-F10, WF2-F11, WF2-F14**. Design: sections 7, 10.3. Scenarios: **S13, S20, S27, S31**.

### C13 Bounded and retry-safe GitHub operations

**Outcome:** Authorized remote changes can be resumed without duplicates or loss of human edits.

- Inputs: repository and item identity, current remote snapshot, stable source ID, and authorized operation.
- Owner: host GitHub tools or `gh`, orchestrated by skills; no separate client framework.
- Outputs: confirmed remote identifiers/results, or an explicit partial/unknown outcome.
- Required behavior: search open and closed items; reconcile ambiguous outcomes before retry; preserve unrelated content; no assertion of atomic claim or remote-write success without confirmation.
- Proof: lost creation response, repeated batch, permission loss midway, concurrent body edit, and wrong repository.
- Implements: **WF2-F04, WF2-F09, WF2-F12**. Design: sections 5.4, 9.2. Scenarios: **S07, S16, S18, S23, S32**.

### C14 Deliberate v1 migration and rollback

**Outcome:** Existing projects move to one authority without losing remaining work or historical evidence.

- Inputs: known v1 backlog/feature/OpenSpec records and explicit item dispositions.
- Owner: migration inspector, migration runbook, and authorized GitHub operations.
- Outputs: read-only inventory, old/new mapping, preserved history, one-time authority cutover, and rollback instructions.
- Required behavior: no mass recreation of Done history; no two-way sync; ambiguous records require explicit resolution; rollback does not erase GitHub history.
- Proof: active, done, deferred, malformed, duplicated, missing-change, and interrupted-migration fixtures.
- Implements: **WF2-F12**. Design: section 12. Scenarios: **S04, S23, S25, S32**.

### C15 Retained engineering lessons and retired machinery

**Outcome:** Historical failure prevention survives while obsolete workflow requirements leave the active distribution.

- Inputs: existing skills/scripts/tests/specs and L-001/L-002.
- Owner: risk references, scenario corpus, migration inventory, and v2 packaging.
- Outputs: concise retained lessons, rewritten meaningful tests, retired commands/contracts, a clean v2 working tree, and a baseline Git-history reference.
- Required behavior: no Superpowers runtime dependency; no `_workflow` resolver, v1 wrapper, local v1 board, or v1-only archive in the final source tree; no tests requiring old ceremony in the v2 suite.
- Proof: tests still expose missing consumer/target failures while a fresh clone contains only v2-active files plus current v2 history/spec artifacts and cannot invoke an old wrapper.
- Implements: **WF2-F08, WF2-F11, WF2-F13**. Design: sections 1.3, 6.3, 12. Scenarios: **S20, S25, S26**.

### C16 Bounded continuation and rewrite bootstrap

**Outcome:** Codex can execute this approved feature sequence before the new tools exist and continue across sessions without inventing a new backlog engine.

- Inputs: these three files, user launch instruction, current branch, and completed implementation evidence.
- Owner: feature-list execution protocol, then the delivered skills.
- Outputs: dependency-respecting implementation commits and a precise checkpoint if interrupted.
- Required behavior: do not require v2 tools to build v2; do not wait for a merge between every feature on an authorized integration branch; distinguish local dependency availability from delivered status; do not autonomously add product scope.
- Proof: start with v1-only checkout, then resume a partial rewrite with no chat memory and with/without GitHub writes.
- Implements: **WF2-F01, WF2-F06, WF2-F09, WF2-F14**. Design: sections 3, 11, 13. Scenarios: **S09, S16, S26, S29**.

## 3. Acceptance scenario catalog

Use these IDs in tests, evaluation records, and PR evidence. A scenario ID is a stable proof obligation, not a required test function name. A scenario may require both deterministic tests and a skill evaluation; do not substitute one for the other.

| ID | Scenario and expected result | Proof type | Primary feature |
| --- | --- | --- | --- |
| S01 | Fresh consumer with no global AGENTS/skills: setup succeeds and instructions/skills are usable | Public CLI integration + discovery exercise | F03 |
| S02 | Clean runtime without Conda, then setup rerun: documented verify command works and rerun is safe | Clean-environment integration | F02 |
| S03 | Invalid markers, conflicting owned file, or unsafe destination: no unrelated writes or silent overwrite | Failure-injection integration | F03 |
| S04 | History retained beside v2: no old applicability rule fires; unrelated rules survive | Instruction and migration evaluation | F01/F12 |
| S05 | Failure partway through setup: originals restored or recoverable residuals precisely reported; rerun works | Failure-injection integration | F03 |
| S06 | Issue phases, blocked/deferred/reopen/cancel outcomes: representation matches the contract | Template/operation fixture | F04 |
| S07 | Same source feature imported twice, including a closed match: reuse; ambiguous matches block creation | Remote-operation fixture + authorized smoke | F04/F09 |
| S08 | High-level design decomposes into bounded outcomes with dependencies and verifiable acceptance | Skill evaluation | F05 |
| S09 | Unapproved enhancement or unresolved decision: not silently made Ready/executed | Skill evaluation | F05 |
| S10 | Ordinary feature: code, proof, docs assessment, and PR prepared with no feature ledger or per-task ceremony | Skill evaluation + actual code test | F06 |
| S11 | Reproducible internal bug: fix preserves contract/test strength; no unnecessary OpenSpec change | Skill evaluation + regression test | F06/F07 |
| S12 | New config setting but stale setup guidance: delivery identifies and resolves missing docs | Skill evaluation | F06/F11 |
| S13 | Docs file changed but describes behavior incorrectly: semantic review detects contradiction | Skill evaluation | F11 |
| S14 | Internal implementation repair leaves docs accurate: reasoned no-impact outcome is accepted | Skill evaluation | F06/F11 |
| S15 | Significant contract change: appropriate OpenSpec artifacts, real implementation, validated specs, and archive | End-to-end integration + review | F07 |
| S16 | GitHub writes unavailable: authorized code work proceeds; no fabricated issue/PR/status update | Adapter fixture + Cloud exercise | F09 |
| S17 | Cloud pass with required Ubuntu verification absent: integration pending; same-SHA handoff enables completion | Two-environment exercise | F09/F14 |
| S18 | Timeout or failure after a remote write: re-read before retry; no duplicate or false success | Fault-injection operation fixture | F09 |
| S19 | Plausible wrong formula or weak fixture: independent expected result distinguishes the defect | Risk evaluation + negative control | F08 |
| S20 | Structured metadata has parser support but no consumer: integration proof fails | Producer/consumer negative control | F08/F11 |
| S21 | Fix weakens assertions or drops relevant cases without approval: review rejects the contract change | Risk evaluation | F08 |
| S22 | PR open, docs incomplete, skipped checks, or stale evidence: cannot close as delivered | Skill/closure evaluation | F06/F10 |
| S23 | Duplicate/ambiguous ownership or human edit: stop conflicting mutation, preserve human work | Operation fixture | F09/F12 |
| S24 | Multi-PR OpenSpec change: partial PR does not archive or close parent; final PR completes obligations | Integration fixture | F07 |
| S25 | Cutover and rollback: old IDs/evidence remain reachable by mapping/Git history, one writable authority exists, and v1-only files are absent from the final `workflow-skills` working tree | Migration integration | F12/F13 |
| S26 | Resume with missing or ambiguous branch/worktree: no current-directory fallback | CLI/skill negative test | F09 |
| S27 | PR metadata changes/head changes: appropriate check reruns; injected shell content remains data | CI event fixture | F10 |
| S28 | Tested dirty tree or later material change: evidence identifies exact content and affected checks are rerun | Evidence evaluation | F09/F10 |
| S29 | Real fresh Cloud session follows the three files/installed skills and resumes a checkpoint | Host-run pilot | F14 |
| S30 | Permissions/migration/filesystem risk: denied, interrupted, missing-resource paths covered as relevant | Risk evaluation | F08 |
| S31 | CI exists but merge rules are not configured: report available checks, not active enforcement | Repository settings inspection | F10/F14 |
| S32 | Migration with done/active/deferred/malformed records and partial remote success: safe inventory and bounded resume | Migration integration | F12 |
| S33 | Fresh project with MVP/later scope, dependencies and one unknown: one design-to-backlog run produces a coherent outcome Issue batch, one approval yields correct Ready/backlog/blocked separation, design links survive reruns, no coding-task explosion or implementation starts | Skill evaluation + authorized consumer GitHub pilot | F05/F11/F14 |
| S34 | Fresh consumer clone contains all committed shared skills; startup verifies the tracked exact pin without network or writes, rejects missing/modified/ignored/untracked assets, and preserves project files/index; explicit setup/update safely migrates schema-2 ignores and validates pinned source bytes; fresh source-owned adoption works without tools/first commit, and Cloud/Ubuntu discovery is tested from the committed checkout | Public CLI clone/fault tests + real CI/environment pilot | F02/F03/F10/F11/F14 |

## 4. Platform responsibilities we reuse

| Capability | Platform owner | What v2 adds |
| --- | --- | --- |
| Code editing, internal planning, optional subagents | Codex host | Scope, context, documentation, and evidence contract |
| Shared backlog and delivery records | GitHub Issues/PRs | Small conventions, useful templates, authorized operation guidance |
| Branch isolation | Git/Codex environment | Verify intended target; no mandatory external worktree creation |
| Review execution | Native host/GitHub review | Project checks and targeted risk methods |
| Test scheduling and merge checks | GitHub Actions/rulesets | Test commands, metadata checks, documented setup and proof |
| Behavior deltas and archive | OpenSpec | Proportional use and links to Issue delivery |
| Credentials and network access | Host and service administrators | Capability diagnostics and honest degraded behavior |

These dependencies must be exercised, not reimplemented. No capability above implies that Codex automatically watches or drains the entire GitHub backlog.

## 5. v1 asset disposition

| Existing asset | Disposition | New destination or proof obligation |
| --- | --- | --- |
| `AGENTS-global-workflow.md` | Retire from v2 distribution | Explicit repo guidance; optional manual cleanup instructions for old global installs |
| Root `AGENTS.md`, `README.md`, `CLAUDE.md` | Rewrite active routing | Short contract, current usage, no old installer requirement |
| `initialize-workflow-artifacts` | Replace | C01/C03 setup, without old planning tree |
| `prioritize-backlog`, `shape-backlog-item`, `ready-feature` | Replace responsibilities | C04/C05, with human-approved scope and native Issues |
| `start-task`, `complete-task`, `finish-feature` | Replace | C06/C07/C10 and truthful completion |
| `fastlane` | Retire as a separate default path | Ordinary delivery is already lightweight |
| `defer-feature` | Replace | GitHub backlog/deferred or cancelled disposition |
| `audit-workflow`, `diagnose-workflow`, `repair-drift` | Retire engine; select useful checks | Small setup/check/doctor surface; no automatic semantic repair |
| `autonomous-backlog-loop` | Retire from first release | Explicit bounded batch execution through host instructions |
| `skills/_workflow/workflow_state.py` and task resolvers | Retire | No replacement state engine |
| `_workflow` evidence/contract/mutation checks | Inspect individually | Reuse only outcome-based validation with a current consumer |
| v1 board, feature files, per-task plans | Remove from final source tree after cutover | Git history plus old-ID mapping; one-time migration for active consumer work |
| Stable specs and archived OpenSpec changes | Review by meaning | Rewrite continuing contracts for v2; remove current and archived artifacts that only document the retired engine |
| Lessons L-001/L-002 | Preserve substance | Risk references and S20/S26, without retrieval counters |
| Superpowers | Remove required dependency | Useful practices expressed in the contract or focused risk references |
| `environment.yml`, `bin/run-python.sh` | Replace required launch path | Portable setup; optional local convenience only if still useful |
| Installer tests | Rewrite around v2 public setup | S01/S03/S05 and preservation behavior |
| Ceremony-specific tests | Retire from active suite | Record rationale; do not let them block v2 by demanding v1 transitions |

## 6. Coverage and change rules

All required capabilities must have an implementation owner, an acceptance feature, and observable proof. Static prose cannot count as proof of a runtime consumer, remote write, skill activation, or Cloud compatibility.

The feature list owns execution order and feature acceptance. This map owns capability boundaries and cross-feature coverage. The design owns architecture and global invariants. If the three conflict, resolve the conflict explicitly using the design's fixed decisions; do not silently weaken acceptance. A later user-approved scope change updates the affected documents and Issues together.

Keep live progress in GitHub after publication. This map may gain links to current implementation/docs, but do not add a second set of Ready/In progress/Done fields.

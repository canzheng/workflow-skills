# v2 rewrite acceptance evidence

Recorded 2026-10-04 for canzheng/workflow-skills, branch
`rewrite/workflow-skills-v2`, [draft PR #16](https://github.com/canzheng/workflow-skills/pull/16)
and [parent #1](https://github.com/canzheng/workflow-skills/issues/1).
This is acceptance evidence, not another backlog. GitHub owns live phases.

F01–F13 are implemented and locally verified; their implementation is ready for
review. F14 is partially completed, with required host/review/enforcement gates
pending. The branch is neither merged nor delivered; no release was published.

## Revision and actual verification

Actual clean starting commit: `d2aaf1904b2ccbe7fbab9733627e9c82fcf12f53` on `work`.
No reset to the research reference occurred. The approved clean-tree clarification
at main `e5747944a7e0520cf766db263834c8485fe63012` was integrated on this branch.

Implementation/test revision: `3386d008f809d32ebc6cf4f849b47750845c1cb6`.
This includes consumer CI, the clarified PR boundary, actual consumer-before-archive
proof and complete shaping output. The earlier bbbf1e5 revision passed 49 tests; its
affected setup/consumer/spec evidence was superseded by the following 51-test reruns.
Subsequent documentation-only review records do not extend this SHA's evidence to
an untested head. The exact final head and rerun outcomes are recorded in Issue #15
and PR #16 after publication; resolve that explicit SHA before continuing.

| Environment | Observed versions / preparation | Result at implementation SHA |
| --- | --- | --- |
| Managed Cloud task checkout, Debian 13 | Python 3.12.14, Node 24.19.0, npm 11.9.0, OpenSpec 1.14.0; fresh venv installation and rerun | `python3 tools/workflow/verify.py`: 51 tests, no skips, public source check passed; `check --repo . --specs --json`: strict current/delta validation passed; diff check passed |
| Actual Ubuntu container, fresh remote clone | Ubuntu 24.04.5 LTS amd64, Python 3.12.3, Git 2.43.0, Node 24.19.0, npm 11.17.0; venv dependency install twice, npm ci | Same 51 tests with no skips, public source and strict specs checks passed; clean tree; exit 0 |
| GitHub Actions | Real `v2 verification` job, pull_request event; Python 3.12, Node 24 | [Run 37205386850](https://github.com/canzheng/workflow-skills/actions/runs/37205386850), job 111445388641: all verification/spec/artifact steps succeeded |

Ubuntu image recipe is [ubuntu.Dockerfile](../../tests/v2/environments/ubuntu.Dockerfile),
base digest pinned; tested local image ID
`sha256:e83c8f9c800507cab5301055e31534ecc788506add79b84bfb1f45a67e1fab93`.
A fresh clone checked out the explicit detached SHA; no mounted checkout or prepared
home supplied skills. Session CA was mounted only for network access, not baked into
the image. Initial mounted-clone ownership and cross-device hardlink failures were
resolved by remote/copying clones, without changing global Git configuration.
This proves Ubuntu portability, not a particular user's private Ubuntu host.

The 51-test suite invokes the production pinned setup, installed checker, actual
consumer CLIs, failure injections and real pinned OpenSpec validate/archive.
Without Node, optional fixture checks are disclosed as skipped; that is not full
rewrite acceptance. Here no tests skipped. The offline required runner rejects an
empty/missing suite and missing required checker. CI uploads verification JSON with
14-day retention. Durable summaries remain here and in GitHub; temporary local logs
are not promised as retained artifacts.

## Feature acceptance mapping

Numbers refer to each feature's numbered acceptance in the approved catalog.
Every feature uses the tested implementation revision above; earlier per-feature
revisions/decisions are retained in the active rewrite's tasks. The common next
action for F01–F13 is review the implementation and complete the named external
proof, preserving their existing evidence. No feature is reported delivered.

| Feature / capabilities | Acceptance evidence and documentation impact | Remaining limitation / next action |
| --- | --- | --- |
| F01 / C01,C16 | 1: actual baseline and 321-path inventory; 2–3: test_bootstrap preserved rules, explicit v2 routing and final retirement; 4–5: approved links, single active rewrite plan, contract scope/docs/evidence. Docs: AGENTS, CLAUDE routing, index, contract, migration. | Fresh host instruction-chain discovery is F14; retain original baseline. |
| F02 / C02 | 1–2: clean venv and actual Ubuntu preparation/rerun; 3: token-free fixtures and required missing-runtime failures; 4: pinned Python development dependencies/Node/OpenSpec versions; 5: runner missing-suite/checker negatives and disclosed old-test dispositions. Docs: development, environment recipe. | Fresh published Cloud preparation/discovery remains pending. |
| F03 / C01,C03 | 1–2: test_setup public fresh/dry-run/apply, preserved unrelated data, source/marker/path/symlink/collision preflight; 3: no-op/update/conflicts; 4: staging/apply rollback and exact residual recovery; 5: bounded uninstall/user config; 6: doctor duplicate/legacy/config/target findings; 7: incomplete bundle rejection and test_scenarios actual production bundle. Docs: operations, consumer guides, bundle provenance; owned generic consumer CI with configured argv execution and collision/modified-workflow preservation proof in test_consumer_ci. | Filesystem presence is not host skill activation; do fresh discovery. |
| F04 / C04,C13 | 1–4: Issue forms, PR template, lifecycle guidance and test_records phase/modifier/closure/parent representation; 5: open/closed identity fixtures plus live identity-safe publication; 6: link-only index, no state mirror. Docs: GitHub runbook/templates/index. | Live cancel/reopen/closure are fixture-only; do not close partial rewrite. |
| F05 / C05 | 1–5: primary-author shaping/current.py inspection, design.md and candidates.md actual bounded bodies, dependencies, isolated unknown and excluded enhancements; 6: identity/human-edit fixtures plus live catalog reconciliation. Docs: skill/usage/evaluations. | Fresh host triggering and independent semantic review pending; no candidate execution authorization. |
| F06 / C06,C07,C10,C16 | 1–2: exact-target delivery instructions and actual ordinary feature/bug outputs; 3–4: shipping defaults/errors/example updated, quantity repair justified no-impact; 5–7: original 697 expectation retained, reviewable branch/PR, remote-denied continuation actually occurred. test_delivery/test_scenarios and primary-author record. Docs: contract/skill/usage/evaluation/templates. | Fresh host execution and ordinary PR review pending; PR open is not delivery. |
| F07 / C08 | 1–3: bounded repair without change, significant receipt change with sole change-owned plan; 4–5: partial-owner obligation, disposable final archive/current-spec synchronization, real rewrite kept active; 6: actual CLI 1.14.0 strict validation plus producer/consumer proof before archive. test_openspec. Docs: OpenSpec runbook, four implemented current specs. | Real rewrite archive waits for F14; structural CLI alone permits premature archive, so owner/review remains necessary. |
| F08 / C09,C15 | 1–2,6: risk-specific primary-author skill findings with honest authorship; 3: wrong 9975 vs hand-expected 7500; 4: ignored currency/missing target negatives; 5: weakened 498 assertion rejected against original 697. test_risk/test_setup. Docs: methods/L-001/L-002/evaluation. | Independent review and fresh-host risk selection pending. |
| F09 / C02,C10,C11,C13,C16 | 1: actual initial 403 did not stop code; 2: timeout/human-edit/duplicate/permission fixtures and live reconciliation; 3: missing/ambiguous branch/revision no fallback; 5: actual same-SHA Ubuntu; 6: dirty-content identity invalidation/affected reruns; 7: separate read/write/push/admin evidence, no credentials emitted. Docs: handoff/evidence/GitHub guide. | 4 fresh context resume remains F14; live lost-response/permission-loss cases are simulated only. |
| F10 / C04,C07,C10,C12 | 1: config argv has actual subprocess consumer; 2: missing sections/path/anchor negatives and installed checks; 3–4: head/body event and malicious-data fixtures, trusted-base/read-only code; 5: runbook and actual settings reads; 6: on-demand read-only Issue audit; 7: semantic limits explicitly documented. test_checks/test_consumer_ci, live source Actions. Generic consumer workflow actually executes declared commands, fails on exit7 and omits wrong-environment integration. Docs: checks/architecture/enforcement runbook. | Trusted-base metadata not active on first adoption; observed merge enforcement pending, no admin write. |
| F11 / C07,C09,C12,C15 | 1–3: ordinary/bug/cross-module/risk actual consumers, omission/contradiction/no-impact primary-author exercises and broken controls; 5–6: discriminating results, no widened expectations/hidden skips/model harness. test_scenarios/test_risk/corpus/evaluations. Docs: corpus/evidence/coverage. | 4 triggering only explicitly read in-turn, not automatic fresh Cloud discovery; retain gap. |
| F12 / C13,C14 | 1–3: test_migration read-only known-format active/Done/deferred/inconsistent/missing/unsafe/duplicate proof and baseline 19 Done/0 active; 4–6: explicit disposition/freeze/one-authority/rollback procedure and interrupted identity/human-edit fixtures. Docs: migration runbook/current spec. | No active source work exists to migrate; actual consumer cutover and remote rollback not performed; universal formats excluded. |
| F13 / C01,C08,C15 | 1: clean clone and pinned install have exactly 3 skills, no v1 tree/global installer; 2–3: all 321 baseline dispositions/destinations and retained risk regressions; 4–5: no ledger/synchronizer, current architecture; 6: active rewrite gate; 7: primary-author reviewed exhaustive manifest validated by test_retirement. Docs: all current routing/guides, disposition manifest, four specs, Git baseline. | Independent asset/spec/document review pending; no global cleanup performed. |
| F14 / C02,C08,C11,C12,C16 | 3: actual Ubuntu same-SHA pass; 4: real GitHub creation/updates/PR/push/Actions; 5–8: complete gap mapping, settings evidence, pilot overhead, honest release report; 9: rewrite deliberately active. Docs: this report, release notes and handoff. | 1–2 fresh Cloud discovery/resume, required review, trusted-base/check enforcement remain unperformed; archive only after all required gates. |

## Scenario proof and gaps

The following names are files under tests/v2. Skill evidence refers to
[actual primary-author evaluations](skill-evaluations.md), not independent review.

| Scenario | Actual proof | Residual obligation |
| --- | --- | --- |
| S01 | test_setup fresh public install and test_scenarios pinned production checker | Fresh Cloud discovery pending |
| S02 | fresh venv/reinstall, Ubuntu clean clone/rerun | Fresh published Cloud readiness pending |
| S03 | test_setup unsafe paths/markers/owned collisions, source/hash/schema omissions | No pending deterministic path |
| S04 | test_bootstrap instructions and test_migration preserved records; final clean head | Fresh instruction-chain evaluation pending |
| S05 | test_setup failure before/during apply, restore/residual/retry | No pending deterministic path |
| S06 | test_records phase/block/defer/cancel/reopen fixtures; actual live review labels | Live cancelled/reopened smoke not performed |
| S07 | closed-ID/duplicate fixtures and all-state live search/publication recheck | Ambiguous live create exercised only as fixture |
| S08 | actual design/current-code inspection and candidate bodies | Fresh-host shaping pending |
| S09 | unknown retention isolated, sync/dashboard excluded, candidates unapproved | Fresh-host scope evaluation pending |
| S10 | shipping consumed, 747 proof/docs and reviewable PR16 delivery contract | Fresh-host ordinary feature pending |
| S11 | original 697 contract restoration/no new OpenSpec fixture | Fresh-host bug pending |
| S12 | shipping omission detected/resolved in actual README exercise | Independent semantic review pending |
| S13 | default 50 docs vs actual 0 found/corrected by primary author | Independent semantic review pending |
| S14 | repaired quantity docs still true; reasoned no-impact | Fresh-host judgment pending |
| S15 | real disposable OpenSpec receipt: broken EUR 1.99 then expected EUR 3.98, archive and strict specs | Rewrite archive blocked by required F14 gates |
| S16 | actual 403 initial create, continued implementation, later confirmed IDs; permission-loss fixtures | Fresh-host degraded-mode pilot pending |
| S17 | same 3386d00 SHA on Cloud checkout and actual Ubuntu clone | Fresh independent Cloud continuation pending |
| S18 | write-success/response-loss fixture re-read avoids duplicate | No live response deliberately lost |
| S19 | wrong percent formula fails hand expectation 7500 | Fresh-host risk reasoning pending |
| S20 | parser-only currency fails EUR6.97 consumer, actual config argv executes | Fresh-host contract review pending |
| S21 | weakened 498 fixture rejected against697 | Independent semantic review pending |
| S22 | partial/open state retained, closure audit/stale/doc limits; no Issues closed | Final aggregate closure not attempted |
| S23 | duplicate/human-edit fixtures, compare-preserving live catalog updates | No simultaneous live race deliberately induced |
| S24 | partial OpenSpec tasks remain open, closing owner, disposable completion/archive | No live multi-PR delivering merge performed |
| S25 | original baseline/explicit dispositions, final clean clone, no dual ledger; rollback fixtures/guide | No active consumer rollback performed |
| S26 | missing worktree/branch/revision CLI fails without cwd fallback | No pending deterministic path |
| S27 | actual head Actions reruns; safe body/head event fixtures | Live consumer Actions and trusted-base body-edit rerun await adoption |
| S28 | SHA/dirty content invalidation fixtures and actual reruns after changed tests | Final docs head verification recorded remotely |
| S29 | exact checkpoint/next action below | Required fresh Cloud task unperformed |
| S30 | denied targets/permissions, staging/apply/interrupted migration negatives | Fresh-host targeted analysis pending |
| S31 | rulesets GET returned []; branch-protection GET403 | Required contexts/merge blocking unobserved |
| S32 | known v1 active/Done/deferred/malformed and partial remote success fixtures | Actual source0active means no live import |
| S33 | realistic new-project design, five actual candidate bodies, one approval/Ready separation, preserved detail/unknown/later scope; test_initial_backlog pinned fresh install, dependency/link and rerun negatives | Fresh-host shaping and actual consumer batch publication remain separate pilot obligations |

## GitHub, enforcement and review

After the user updated the connected app, writes succeeded. Parent #1 and F01–F14
Issues #2–#15 exist with stable source markers; searches covered open and closed
Issues before creation and on retry. Publication recheck found unique identities.
[Issue index](../v2/issue-links.md) holds links only. Draft PR16 and branch publication
are confirmed; no token was needed or exposed. Bodies/labels are read before scoped
updates, preserving human content and unrelated labels. Fault tests remain fixtures.

Read-only `GET /repos/canzheng/workflow-skills/rulesets` returned `[]`.
`GET /repos/canzheng/workflow-skills/branches/main/protection` returned403
Resource not accessible by integration. This does not prove classic protections
are absent. No protection settings were changed. Consumer CI is now installed automatically as
owned files, but live Actions in a newly adopted consumer repo remain unperformed. `v2 verification` is observed;
`v2 PR contract` trusted-base metadata cannot run for first adoption while main
lacks the new checker/workflow. Body-edit refresh and actual merge blocking must
be observed after authorized adoption/configuration; see [runbook](../workflow/checks.md).
No authorization to merge, configure protection, publish or delete branches exists.

Semantic evaluations and final documentation assessment are primary-author.
A user-supplied external reviewer examined architecture/skills/templates/Actions and
reported targeted comments, validated in reviewer-findings.md. That limited input is
not final independent acceptance review of the revised code/specs/docs/dispositions.
The host's current Cloud platform-guide fetch returned403; no current published
profile behavior, secret lifetime or automatic skill synchronization is inferred.

Pilot overhead: no normal-implementation confirmations, per-task plans, new ledger
or forced reviewer/subagent rounds. Shipping required actual updated docs; quantity
repair required no-impact reasoning. Receipt significant change used its single
OpenSpec plan; risk cases used targeted proof. No speedup metric is invented.

## Documentation/specification completion

Reviewed the final runtime, config consumers, setup ownership, commands, tests and
instruction chain. Updated root AGENTS/CLAUDE/README, docs index/architecture,
development/operations/migration, contract/GitHub/usage/OpenSpec/risk/handoff/check
guides, installed consumer guidance, Issue/PR forms, scenario/evaluation records,
release notes and asset manifest. Reconciled current source-vs-baseline inventory
and Git-only old archives during final assessment. The three approved scope docs
contain human-approved design, not live status. The Issue index has no phase mirror.

Current specs: workflow-v2-adoption, workflow-v2-delivery, workflow-v2-migration,
workflow-v2-quality. Actual strict checks passed. Active workflow-v2-rewrite owns
remaining release gates and the only rewrite plan. Do not archive merely because
CLI structural validation permits it. Final required acceptance, then archive/current
spec synchronization and post-archive verification remain the closing obligation.

## Exact next Cloud action

Start a new Codex Cloud task for this repository at the explicit final SHA recorded
in Issue #15/PR16 on `rewrite/workflow-skills-v2`. If branch/SHA differ or are missing,
stop that item; never select another checkout. Read AGENTS.md, docs/README.md,
contract, all three approved scope docs, this report and the active rewrite tasks.
Do not repeat F01–F13 or create another plan/backlog. Use Issue #15 for remaining work.

1. Capture clean branch/full SHA, versions and actual Cloud preparation profile;
   install pinned requirements and npm dependencies, rerun after preparation changes.
   Run verify.py and `workflow.py check --repo . --specs --json`.
2. In fresh context discover the three intended repository skill names, read their
   SKILL.md files, and install the real full-SHA bundle into an explicit clean Git
   consumer using documented setup/doctor commands. Capture actual host discovery,
   not only files or doctor diagnostics; do not alter globals.
3. Exercise shaping plus ordinary feature, bug, receipt cross-module and targeted
   risk prompts from tests/v2/scenarios. Record actual outputs, consumer proof,
   scope/unknown handling, omitted/contradictory docs, valid no-impact and denied
   remote handling. Identify author/environment and keep fixtures distinct from live
   operations. Record continuation using existing Issue/PR references.
4. Preserve passed Ubuntu/Actions evidence if content is unchanged; rerun affected
   proof at any changed implementation SHA. Obtain final independent semantic review.
5. In an authorized consumer repository, exercise the actual Ready Issue → claimed
   work → draft PR → generic CI → Ready PR/review → semantic review/fixes path.
   Ubuntu discovery must be observed in its actual agent host. Merge/completion can
   be observed only with separate merge authorization; until then keep that final
   path pending. Report trusted-base metadata adoption and administrative enforcement as still
   pending unless observed by an authorized owner. Changing protection or merging
   still needs separate authorization. Do not bypass gates or infer approval.
6. Only after required acceptance is satisfied, archive with pinned OpenSpec and
   rerun current-spec/docs/full verification on the archive diff; update PR/evidence
   and leave reviewable. Do not merge/publish or close delivery prematurely.

Ubuntu repeat recipe: build the tracked Dockerfile using the Cloud runtime's local
Docker socket and CA secret, then start that image with session CA mounted read-only.
Inside it clone the rewrite branch from GitHub, detach the explicitly recorded SHA,
create .venv, install requirements twice, run npm ci, verify.py, strict specs and Git
clean/diff checks. Do not reuse a mounted source checkout as fresh-host proof.

## User-authorized initial-backlog refinement

Follow-up scope explicitly approved by the user: make existing-design → initial/MVP
backlog the one-shot default, with internal optional decomposition, faithful detailed
design translation, delivery-level Issue granularity, one batch approval, separate
execution authority, stable reruns and lightweight direct prerequisite metadata.
S33 was added to the approved capability/feature/design contract and current delivery
spec, with realistic input/output and primary-author evaluation. This extends F05/F11
and the real F14 consumer pilot without a new state engine or mandatory artifact.
Earlier implementation-SHA results above remain historical evidence; the final revised
SHA/reruns and consumer pilot outcome are recorded in Issue15/PR16 after publication.

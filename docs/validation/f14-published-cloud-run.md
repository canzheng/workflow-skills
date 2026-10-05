# F14 published Cloud run: recovery passed, discovery pending

## Latest submitted tracked-skill diagnostic — 2026-10-05

The user supplied `Pasted text.txt`, 18,076 bytes, SHA256
`eeffe3cc30c3dfc83305b135618c58cb8ce760745aa77c2d6e3ae4abcf0ad6ca`.
This is submitted task evidence, not a directly inspected live session. Its expected
consumer/source pins are `0e3fbc530f21c4981230a5ef968eac2a5dda3d5e` /
`aceba7143652ba127dbc62c98608e1b9943be31d`. Actual branch `work` instead has
HEAD `5d05564919c55f1d4d0c2e1e020ad914252a2979` and schema-1 source pin
`139e66d5b43cfbd3821fe098c0119b93aaad4928`. This is the older main snapshot;
putting the expected revision in a prompt did not select it before startup.

Before explicit skill reads, the report records configured and shell cwd `/workspace`,
55 plugin skills with no workflow entries, an empty executor catalog and no matching
consumer project in the host project listing. Repository verification subsequently
used `/workspace/workflow-skills-test`. The complete automatic repository-skill
catalog was unavailable. These observations do not prove that every host catalog
omitted the skills, or establish the discovery implementation's root cause.

All four shared files were already committed, present and manifest-hash-matching
in the actual old checkout; effective ignores excluded none. Independent inspection
of consumer origin/main at that same SHA confirms the four shared blobs, identical
to the pilot branch's shared blobs. Thus absence from the default branch does not
explain this result. The [official skill documentation](https://learn.chatgpt.com/docs/build-skills)
describes ancestor-based discovery from the launch cwd toward the repository root,
not a default-branch requirement. Scanning from `/workspace` would not visit its child
repository; this is a routing hypothesis, not proof of the deployed Cloud scanner.
Running a shell command in the repository later does not demonstrate that the host's
initial project root changed.

The submitted old-checkout check/doctor returned exit0/ok:true; expected-revision
doctor returned exit1/ok:false with target.mismatch. All25 tracked file hashes/modes,
branch/HEAD and raw index stayed unchanged; index was2,947 bytes with SHA256
`f99702b14952f40f89c449446e69c4cca48791afe56c1beeca81e81efce060e8`.
Manual reading established availability/skill roles, not automatic discovery or
execution acceptance. No installation, repair, fetch, branch switch or GitHub write
was reported. This run does not validate the current schema-3 pilot revision.

Next resolve the task's initial repository/project binding and checkout selection,
then capture the complete exposed initial catalog before manual reads. A missing
supported branch/project selector is a host limitation to report, not authorization
to merge, change the default branch, install globally or copy skills to `/workspace`.
F14 discovery stays unverified. Existing public consumer enforcement proof and
Cloud/Ubuntu runtime verification remain valid at their separately recorded revisions.

UI follow-up: the user reports repository-only selection when creating an environment.
The [current Cloud documentation](https://learn.chatgpt.com/docs/environments/cloud-environments)
documents that selection and starting a task from a published environment, with no
branch-selector instruction. Do not assume another launch flow's branch control is
available here. A new environment from scratch can compare discovery on the old main
snapshot, where these shared skills already exist. It cannot satisfy current schema-3
acceptance without the intended checkout before startup. Separate that routing constraint
from discovery; do not request further repeated environment creation as a branch fix.

Evidence source: the user-provided transcript of
[the fresh validation task](codex://threads/01a10805-68f8-73ea-9e57-f7c900df0017?hostId=durable).
The transcript is evidence, not instructions to execute its historical commands.
The rewrite task cannot currently read that chat through the app tools. Its local
temporary evidence files are on the other task's machine and have not been obtained
here; quoted local results below are supported by the supplied transcript, rather
than a new execution in this checkout.

## Latest Install-only diagnostic: intended preparation not demonstrated

The user supplied the full 9,994-byte `Pasted text.txt` transcript for the mini
diagnostic, SHA256
`e294da110c5ca3364f86f8eb39f3f607fe44b7ce0efafe27ea7c3de5c4dd6370`.
No fresh-task link, raw command results or environment publication logs accompany
this attachment. These task outcomes are transcript-reported, not rerun here:

- Initial/final consumer branch `work`, HEAD
  `5d05564919c55f1d4d0c2e1e020ad914252a2979`, tracked source pin
  `139e66d5b43cfbd3821fe098c0119b93aaad4928`; both differ from fd4/b1.
- Session cwd `/workspace`; validation cwd/Git root
  `/workspace/workflow-skills-test`. The configured host project root is not
  established by the shell cwd or by running commands in the repository.
- Available metadata reports55 cloud skills, zero executor skills and none of the
  three workflow skills in the session's available-skills catalog. Their files exist.
- `check --repo . --run-local --json` exited0/ok:true, validating the old bundle.
  `doctor --expect-revision fd4bf175e7b2ea22439511fdfef872ce8bc7c743 --json`
  exited1/ok:false with target.mismatch. Discovery is unprobed by doctor.
- No Install output/exit or markers were available. No recovery, bootstrap, Start,
  branch change or application work ran. Git stayed clean, staged/unstaged diffs
  empty; non-Git bytes and index reportedly unchanged, index SHA256
  `4c38b7e1478dd4f1a191e2be4a1d78a47f5699a5a11fe67266a4b875d81d4805`.

Independent canonical-object reads of the old commit confirm its schema1 pin and
all three reported skill sizes: deliver4,842/design5,501/risk1,754 bytes. These are
old tracked skill files, not proof that the new ignored dependencies were prepared.
A repository marker search cannot establish whether a host-owned Install ran.
The report cannot distinguish nonexecution, failure, stale published configuration
or later checkout replacement; it does not establish a network/authentication cause.
Public Codex source7f892275 describes ancestor-based repo roots, making host cwd/root
routing a separate lead when shell cwd is the consumer's parent. That snapshot does
not prove the deployed Cloud implementation or a supported discovery refresh.

The user subsequently reported that the environment UI exposes no Install execution
log or exit status. The handoff therefore now captures each attempt's stdout/stderr,
exit status and initial/prepared HEAD/pin outside the checkout, under
`/workspace/.wf2-install-evidence/workflow-skills-test/`. The mini diagnostic reads
`latest` and its referenced structured `install-info.json`, `install.log` and
`exit-status` after initial catalog capture. The stronger receipt includes timestamp,
requested/fetched installer revision, initial/prepared consumer revision, actual
prepared workflow pin, all-three-skill presence assertions and log SHA256.
These are temporary diagnostic artifacts, not project policy, another backlog or
an installer. No tracked files/index or global skills/configuration are changed.
Receipt persistence must itself be tested; missing/stale receipts are inconclusive.

Next: publish/apply the capturing Install command and run the updated mini diagnostic.
If the receipt shows successful fd4/b1 preparation, compare that with fresh-task
checkout replacement/order. Investigate configured host cwd/project-root/catalog
routing separately. Start remains optional; no global installation, skill relocation
or distribution redesign is inferred.

The Ready PR review also found an independent pilot-command dirty-tree gap at
6b25df4: at expected HEAD, a modified schema-valid manifest pin was accepted and
WF2_INSTALL_END printed. A real Ubuntu run reproduced it, as did a failing-before
public-command regression. The handoff now checks cleanliness before the HEAD
condition, including already-correct HEAD. Git status runs with optional locks
disabled: the full regression also exposed index-stat refresh during refusal, and
now forces that condition while preserving the raw index assertion. This preserves
refusal boundaries; it does not explain the old checkout in this diagnostic. Exact repair verification
and new-head CI/review are recorded in Issue15/PR16 after testing/publication.
Repair/capture verification: final Install block SHA256
`b1177ebfb4218ce9bd5e7ac33cf1f3ce628bdcbf57515e628fa74c4e1dcde421`.
All82 tests/no skips and strict current/delta OpenSpec checks pass on managed Cloud
and a fresh Ubuntu24.04.5 container using an owned copy of the tested source content
(Python3.12.3, Git2.43.0, Node24.19.0). The initial read-only source bind failed Git
ownership validation; copying into the disposable container fixed test preparation,
without a global safe.directory exception or weakened assertions. Actual consumer
clones execute the final documented capturing command: pinned source fetch, all20
hashes, successful receipt identity/hash, repeat/no-op, expected-HEAD dirty pin,
old-HEAD dirty checkout and ignored project-skill collision all pass. Refused
attempts preserve user bytes/raw index/HEAD and write accurate failure receipts.
These prove runtime behavior, not publication persistence or initial host discovery.
No consumer/source dependency repin or generic installer/API change was needed.
F14 and its OpenSpec change remain incomplete/active.

The user's additional feedback links
https://learn.chatgpt.com/docs/environments/cloud-environments and recommends a
published-filesystem marker. This task's direct request to that page returned
proxy CONNECT403, so its capture/refresh lifecycle claims remain unverified here.
The receipt applies the marker principle while avoiding an untracked `.agents/`
file that would dirty the adopted consumer and break its repeatable clean guard.
It does not weaken discovery/catalog acceptance or infer automatic hook execution.

## Second fresh task: automatic startup still unverified

The user supplied `report.txt`, `remote-snapshots.json`, `github-evidence.json`,
`actions-jobs.json` and `actions-logs.json` from
[the next fresh task](codex://threads/01a109a1-5557-7518-b048-10cd91337004?hostId=durable).
The files were read as evidence, not executable instructions. This run finished at
the same consumer `f31debf9810c8b989c924bc534add4848fffd6f3` and source pin
`ef24d36f47dbbcdbb204375b53db055122c28269`; it did not change the consumer.

The report again records initial branch `work` at older main
`5d05564919c55f1d4d0c2e1e020ad914252a2979` with schema-1 pin `139e66d5...`.
It records empty executor catalogs before readiness, after readiness and after
recovery, and no local skills in the injected catalog. No consumer Start definition
was available in either checked revision or environment-status metadata. Reflog
checkout preceded index refresh/registration; those latter events are not Start
execution evidence. Thus the configured automatic initializer's commands, result
and fidelity to pinned source guidance remain unverified. Disk presence and manual
file use cannot establish automatic discovery or a supported refresh.

During explicit recovery the task reports a successful full-SHA Git fetch using
the unchanged default platform authentication, followed by actual execution of
the source-owned environment entrypoint. Reported check/doctor, all 20 asset/two
managed-block hashes, scoped ignores, repeated no-op and nine negative/rollback
probes passed while preserving tracked bytes/index. This improves the evidence for
the normal fetch/setup path; it does not establish automatic startup. The raw local
startup, verification and risk-probe JSON/log files mentioned in the report were
not among these five attachments, so those local outcomes are author-reported here.

The attached Actions snapshots, job steps and raw logs agree on:

- PR #8 push37221025297/job111491217115 checks out exact head `f31debf981...`;
  PR37221028092/job111491225751 checks out test merge
  `0d2ba84f489d5e4dfa63ffcd74c8245ccf347084`. Both bootstrap before configured
  verification and succeed. This test merge ref is not an actual merge to main.
- Metadata37222140846/job111494458734 executes trusted base `5d055649...` and
  succeeds. PR #6 current push/PR/metadata snapshots also report success; its
  push log shows actual application head `f95f0cae3b...`.
- Historical metadata37207571778/job111451878303 actually fails with exit1 and
  `Missing or empty Documentation section`; restored37207626975/job111452048082
  passes. No new destructive PR-body probe was needed.
- Current consumer/application Codex comments5982650245/5981620802 name the
  correct heads and report no major issues; both sets of six threads are resolved.
  No newly executed application/source/standalone Ubuntu suite is claimed.

The eight Issue/PR snapshots retain the five unique MVP identities, design links,
phases and prerequisite metadata. The safe rerun neither edited nor dispatched them.
Live PR #8 was independently reread and remains Ready/open at the same head.

The supplied main-branch summary and a new live read both report `protected:false`,
protection disabled, enforcement off and empty check contexts. This is a concrete
limited observation, rather than proof of required enforcement. Authoritative
protection/ruleset reads remain denied; effective required-check behavior and an
actual blocked merge remain unverified. No administrative mutation was attempted.

Attachment SHA256 identities for continuation:

| File | SHA256 |
| --- | --- |
| report.txt | dfcaaed555d4e7b0a788b9b5071a07fb1818ad38c642b2bccea1b01060ccdfac |
| remote-snapshots.json | 490ef0fb50a2a8d5f29c9defc9bba03154228741695e983fb7082404e7c18085 |
| github-evidence.json | 34497a7db1d755290a286e994b6d8836e41bab34066e2a252a3050f7b12b1302 |
| actions-jobs.json | 50a6d468090465d4c696da7f1c6279f76f46b34f4b92dae1e1b6b4134aeed822 |
| actions-logs.json | e4bd6a165ade0741a44b976c532ef608bb5831fe7a089658eec5c5e818ffc9dc |

Next, obtain the actual consumer Start definition and automatic run output from the
host that owns them; identify its checkout/execution/discovery ordering before
another task. This task's repository and runtime metadata did not expose them.
The environment being repository-scoped does not itself select the pilot branch.
Do not require a branch in generic adoption; this unmerged pilot's revision is a
specific test prerequisite. A normal initialized consumer uses its selected checkout
and tracked pin. Neither another recovery nor a simulated merge closes these gates.

## Subsequent repair and current consumer

The rewrite task reproduced the independent source review's replacement-ref finding
before accepting it, then fixed canonical object reads at source
`b1fe9e0242753db54cc16dfc8768502eb74cb3ea`. All 81 tests/no skips and strict specs
passed on Cloud and fresh Ubuntu24.04.5; source Actions37251965903/37251969459 passed.
Source Codex comment5986640964 reports no major issues at that code head.

Consumer branch `pilot/shared-skill-bootstrap` then advanced to
`fd4bf175e7b2ea22439511fdfef872ce8bc7c743`, with tracked source pin `b1fe9e0...`.
Only the runtime setup file, manifest pin/hash and README pin changed; the three
skills/four shared hashes remain identical. Connected Git-data publication's tree
`1155ae30e50c47031a83b066db55ed1c67748eec` matched the locally verified tree, used the
actual f31 parent and a guarded non-force ref update. The actual commit was fetched;
local metadata commit was preserved on a separate local branch, not reset away.

Actual consumer Cloud check/doctor and matching bootstrap no-op passed. Fresh Ubuntu
cloned real main, safely selected the authorized current pilot SHA, and executed the
actual README full-SHA fetch/run twice. All asset hashes, tracked bytes/index, project
skill and clean Git were preserved. This validates the proposed mechanical startup
sequence, not execution of the user-configured automatic Start skill. Current-head
push37252506795/PR37252510994/metadata37252507928 passed; current-head Codex
review5986706572 reports no major issues.

The changed README entrypoint was also executed twice on a fresh unborn Git root
on Ubuntu, adopting source b1 and preserving files/index on repeat. This task's
separate outer-Cloud temporary Git fetch returned an authentication error, while
its already-available source-owned entrypoint/checks passed. That host-specific
failure is not reassigned to the uploaded task, which reports successful normal
source fetch. No credential rebinding or implicit alternate revision was used.

The supplied consumer Start text required the pilot commit while forbidding branch
selection before proceeding. It could not initialize the intended pilot from either
reported initial older-main checkout. The author corrected those instructions in
[the current handoff](cloud-bootstrap-handoff.md#start-skill-entrypoint), explicitly
authorizing safe pilot-only selection and begin/end/failure markers. Generic startup
remains branch-agnostic. Whether the published Start actually ran is still unverified.
Use the handoff's current SHAs for continuation; retain both uploaded runs at their
original f31/ef24 identities. No merge, completion or administrative mutation occurred.

## Initial preparation and discovery

### Install/Start feedback and verification boundary

The user supplied external feedback recommending Install as primary dependency
preparation and Start for per-task verification/runtime services. That recommendation
matches the existing source-owned entrypoint and was accepted as a documentation
clarification, not a distribution redesign. The handoff now provides a bounded
pilot-only Install prelude to select its authorized unmerged revision. The user
then selected Install plus the mini diagnostic for this service-free pilot; Start
is optional for other projects' runtime needs, not a gate in this pilot.
Generic installation remains branch-agnostic;
the tracked dependency pin stays authoritative and only three shared namespaces
are ignored. Existing adoption/bootstrap responsibilities remain distinct from
Cloud's environment/task lifecycle. Modified dependencies fail without overwrite.

The feedback's citation placeholders contain no source URLs. Its claims about
published-filesystem capture, refresh preservation and automatic hook execution
are not independent proof. Direct Cloud/skills documentation requests still return
proxy403 in this rewrite instance; its spec38 reports the package-manager preset
with no custom allowed hosts. The runtime policy includes github.com, not
api.github.com, so that preset's name alone does not establish a denied Git fetch.
These are this instance's observations, not the consumer's effective policy.

Official public Codex source at `7f892275e31002f0422477c6219189284560e689` separates
host, executor and cloud skill catalogs, routes skills by explicit name or matching
description, and implements lifecycle hooks separately. An empty executor catalog
alone is not a complete discovery check. Capture initial available-skills context,
exact name/source, configured session cwd/project root, actual Install/Start output
and command exits. Compare the fresh consumer's HEAD/pin/materialized hashes with
the prepared state. Explicit invocation is a separate result from automatic Start
and pre-agent discovery; no undocumented Cloud guarantee is inferred from this
public implementation snapshot. Existing catalog/discovery gates stay unverified.

The exact revised handoff Install block (SHA256
`7628c465a8fb16b7a2e1b95912f61dcb60d9f7db7b365a5af9c22488d521b0f4`)
was executed in a fresh Ubuntu24.04.5 container (Python3.12.3, Git2.43.0). It cloned
real consumer main, safely selected fd4, fetched source b1, ran the source-owned
entrypoint and verified all20 manifest hashes. A second full execution preserved
tracked bytes/index and clean Git; only three shared namespaces were ignored and
the project skill stayed tracked. Separate disposable-clone negatives denied a
dirty checkout before selection and an ignored project-skill collision during
selection, preserving original user bytes/index/HEAD. These are actual mechanical
command results, not published Cloud Install execution or filesystem persistence.

The requested consumer was `canzheng/workflow-skills-test`, branch
`pilot/shared-skill-bootstrap`, commit
`f31debf9810c8b989c924bc534add4848fffd6f3`, with tracked source pin
`ef24d36f47dbbcdbb204375b53db055122c28269`.

The task instead initially observed branch `work`, consumer commit
`5d05564919c55f1d4d0c2e1e020ad914252a2979`, and old source revision
`139e66d5b43cfbd3821fe098c0119b93aaad4928`. Its initial host/executor catalogs
exposed no repository-local skills, despite the older checkout containing three
tracked skill files. Available executor logs contained registration/handshake
events, not install-hook output or ordering evidence. This run does not pass the
fresh pre-agent discovery gate. The revision mismatch and absent skill exposure
are separate observations; the transcript does not establish either root cause.

The agent preserved the clean baseline, fetched and switched the same checkout to
the requested branch, then ran bootstrap itself. Such recovery cannot retroactively
prove that preparation materialized skills before initial host discovery.

## Verified after recovery

- Final consumer branch/commit and tracked source pin match those requested above.
- Bootstrap exited 0 with `ok:true`, initially materializing four shared assets.
  Configured `check --run-local` and `doctor` exited 0 with `ok:true`; repeated
  bootstrap returned `changes:[]`. Tracked bytes/index were preserved and Git was clean.
- All 20 manifest hashes matched. Four materialized shared assets matched exact-pin
  source bytes obtained through the GitHub connector. Only the three canonical
  shared namespaces were ignored/untracked; `pantry-project` remained tracked.
  The consumer contained no copied environment setup entrypoint.
- The agent read and used the three skills for backlog reconciliation, delivery
  evidence/documentation and targeted risk proof after recovery. Explicit manual
  use establishes that exercise, not automatic host discovery.
- A safe shaping rerun searched open and closed Issues and reused all five MVP
  identities. It preserved acceptance, human prose, design links, dependencies and
  the dietary decision; it created no Issues and started no implementation.
  Ingredients remained review, recipes Ready, the decision backlog/blocked,
  planning blocked on #1/#2/#3, and shopping export blocked on #4.
- Installed-consumer negatives rejected modified/extra/symlinked dependencies,
  broad ignores, exposing negations, invalid versions, incomplete provenance and
  missing/nested targets. Injected transaction failure restored bytes/modes;
  probes were restored and affected checks rerun.

The workflow-only branch has no application implementation. These local commands
verify workflow integrity, not application acceptance. The validation task inspected
application PR #6 and its historical test/review/CI evidence; it did not rerun the
application tests or previous source/Ubuntu test suites.

## Independently rechecked GitHub evidence

The rewrite task read GitHub after receiving the transcript:

- [PR #8](https://github.com/canzheng/workflow-skills-test/pull/8) remains open and
  Ready at `f31debf9810c8b989c924bc534add4848fffd6f3`;
  [Issue #7](https://github.com/canzheng/workflow-skills-test/issues/7) remains open
  with `wf:review` and the fresh-discovery acceptance intact.
- Actual current-head [push verification](https://github.com/canzheng/workflow-skills-test/actions/runs/37221025297),
  [PR verification](https://github.com/canzheng/workflow-skills-test/actions/runs/37221028092),
  [metadata](https://github.com/canzheng/workflow-skills-test/actions/runs/37221026987)
  and [metadata rerun after the PR body correction](https://github.com/canzheng/workflow-skills-test/actions/runs/37222140846)
  all report success.
- [Current-head Codex review](https://github.com/canzheng/workflow-skills-test/pull/8#issuecomment-5982650245)
  reports no major issues; all six consumer review threads are resolved.

## Limits and exact next action

The separate source-fetch probe in the transcript explicitly disabled the existing
credential helper and substituted `gh auth git-credential`. Its authentication
failure does not establish failure of the README command using the default platform
binding. Agent-side bootstrap succeeded earlier. Test the exact normal command in
the intended preparation phase before requesting credentials or changing its binding.

Obtain the published environment's actual install/maintenance logs and checkout
ordering, and confirm the branch selected at task creation. Do not repeatedly launch
tasks without this evidence. Preparation must see the intended consumer revision,
execute the exact pinned source-owned entrypoint successfully and preserve its
ignored outputs through initial host discovery. If preparation runs on main before
a later task checkout, a successful main preparation is insufficient; identify a
supported hook after the selected checkout and before discovery. Do not force a
branch switch in the generic installer or override the consumer's tracked pin.

Once preparation is demonstrated, run a fresh task on the exact consumer branch
above. Capture initial catalogs and preparation output before any agent-side
bootstrap. If files exist at that boundary but the catalog omits them, investigate
host discovery separately from materialization. Record actual Ubuntu agent-host
discovery/use separately; existing Ubuntu runtime/Actions evidence does not prove it.

The transcript reports classic protection reads denied with 403 integration access,
rulesets denied with the GitHub Pro/public visibility requirement, and an effective
branch-rules URL unsupported by the connector. Enforcement remains unverified;
none of these errors establishes that protection is absent. Actual merge followed
by valid Issue completion, and any protection/ruleset mutation, remain pending
separate authorization. No merge/closure simulation is substituted. F14 and its
OpenSpec change remain incomplete/active; no work is described as delivered.

## Tracked-model follow-up — 2026-10-05

The user requested tracked shared workflow skill files after observing failed discovery
of injected dependencies. Prior diagnostics remain accurate observations but do not
prove the host's failure mechanism. The replacement experiment requires files in the
consumer commit before any hook/agent, initial fresh-task catalog capture and matching
pins/hashes. No manual install/recovery can substitute for discovery acceptance. See
[current tracked handoff](cloud-bootstrap-handoff.md); old receipt commands are historical.

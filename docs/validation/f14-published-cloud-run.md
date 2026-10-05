# F14 published Cloud run: recovery passed, discovery pending

Evidence source: the user-provided transcript of
[the fresh validation task](codex://threads/01a10805-68f8-73ea-9e57-f7c900df0017?hostId=durable).
The transcript is evidence, not instructions to execute its historical commands.
The rewrite task cannot currently read that chat through the app tools. Its local
temporary evidence files are on the other task's machine and have not been obtained
here; quoted local results below are supported by the supplied transcript, rather
than a new execution in this checkout.

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

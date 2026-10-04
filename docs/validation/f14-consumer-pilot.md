# F14 real consumer pilot

## Current source-owned setup checkpoint

This checkpoint supersedes the earlier consumer-owned script instructions below.
At user request, the source-owned `tools/workflow/environment-setup.sh` is excluded
from the consumer bundle. Workflow-skills README documents one pinned fetch-and-run
command for the Cloud environment **install script** field and local/Ubuntu Bash.
Consumer README links to the source; `.workflow/cloud-setup.sh` has been removed.
The outer command fetches its exact entrypoint each run; repeatable materialization
itself uses the tracked consumer pin and needs no fetch when skills already match.
No consumer policy/pin/index is rewritten by repeat setup. First adoption creates
trackable policy and exactly three scoped ignore entries; project skills stay trackable.

Tested implementation source `608b4e6ee16017bca3e63e98b2e1e91235b1a004` passes75 tests
without skips and strict OpenSpec checks on Debian Cloud and fresh Ubuntu24.04.5
(Python3.12.14/3.12.3, Git2.52/2.43). A shallow source-suite attempt failed two historical
baseline checks; fetching full history restored required evidence without weakening
those checks. Source push/PR Actions37217423703/37217427057 succeeded.
Consumer `pilot/shared-skill-bootstrap` at `102706c76b2ade368397f866057314f083c67bea`
pins that exact source; fresh Cloud-runtime/Ubuntu clones executed the actual README
fetch-and-run command twice, matched all four shared hashes, preserved tracked bytes
and index, kept pantry-project tracked and stayed Git-clean. Actual consumer push/PR/
metadata Actions37217514512/37217517130/37217516077 succeeded. Issue7 and ReadyPR8
remain open; PR6/Issue1 application evidence stays atf95f0cae3b87bc8031b00a4150cf9670251ae978.

Mandatory completeness now includes all20 destinations, including docs/templates/risk
reference; public negative tests proved omissions fail before install and cannot be
hidden by editing provenance. An actual fresh Git root with no first commit ran the
README command successfully, then repeated with identical bytes/index. Doctor reports
revision:null/dirty:true before commit and the actual clean commit afterward. The prior
fixture inventory assertion was updated to verify all four pinned shared files/bytes;
no acceptance/assertions were weakened to accommodate broken output.

Native independent current-head semantic review results must be read, not inferred
from CI. Fresh published Cloud pre-agent discovery/use and Ubuntu agent-host discovery
are still unperformed. The onboarding chat is not fresh-task evidence. Required-check
administration reads are access-limited; workflow YAML and successful Actions do not
prove enforced checks. No merge/Issue completion, protections/rulesets writes, release
or remote branch deletion occurred. Those mutations remain pending separate authority.
Use [the current Cloud handoff](cloud-bootstrap-handoff.md): publish/apply its install
script, select the exact consumer branch, launch a genuinely fresh task and record the
initial discovery catalog before agent-side bootstrap. F14 remains integration pending;
F01–F13 are implemented/locally verified and ready for review, not merged or delivered.

## Earlier implementation evidence


Recorded 2026-10-04. This is immutable acceptance evidence, not a second backlog.
Live scope/phases belong to GitHub. The user authorized this disposable consumer
pilot through review and environment verification, excluding merge/completed closure
and repository administration. F14 remains partial; nothing is reported delivered.

## Verified/completed under current authorization

Repository: [canzheng/workflow-skills-test](https://github.com/canzheng/workflow-skills-test),
an existing private repository. Actual inspected initial main was
`a2f84e768e42e900d47ace5e21897f7e02e71f2a`, containing only the user's README.
Pinned workflow source: `139e66d5b43cfbd3821fe098c0119b93aaad4928` on
`rewrite/workflow-skills-v2`. Production setup dry-run/apply installed the three
skills, contract, provenance, configured checker and two generic owned workflows,
preserving the README. No global installation or configuration was changed.

Adoption main: `5d05564919c55f1d4d0c2e1e020ad914252a2979`. This direct bootstrap
publication added workflow assets/design, with the user's F14 authorization; it was
not an implementation PR merge. Actual app changes use
`pilot/ingredient-catalog`, current tested head
`f95f0cae3b87bc8031b00a4150cf9670251ae978`,
[Ready PR #6](https://github.com/canzheng/workflow-skills-test/pull/6),
non-closing reference to [Issue #1](https://github.com/canzheng/workflow-skills-test/issues/1).
Private CLI push was unavailable; connected Git-data APIs published trees whose
SHA matched the locally tested Git tree, with actual parent/ref checks and no force.
The actual remote commit was fetched and verified. No credential values were read.

### Design to initial backlog

The primary author explicitly read and used installed workflow-design-to-backlog,
workflow-deliver-issue and workflow-risk-review. The realistic
[MVP design](https://github.com/canzheng/workflow-skills-test/blob/main/docs/design.md)
was shaped in one coherent batch, using the smallest five verifiable outcomes.
Existing explicit examples/acceptance were retained; later Cloud/account/mobile
scope was unmaterialized. No engineering-task Issues or editable backlog file exist.
All-state search preceded creation; confirmed URLs populated direct prerequisite
JSON and matching readable links after all Issues existed.

| Outcome / stable source ID suffix | Actual Issue | Initial approved disposition | Confirmed direct prerequisites |
| --- | --- | --- | --- |
| Ingredient catalog / ingredients | [#1](https://github.com/canzheng/workflow-skills-test/issues/1) | Ready, then explicitly selected execution | [] |
| Recipe catalog / recipes | [#2](https://github.com/canzheng/workflow-skills-test/issues/2) | Ready, unexecuted | [] |
| Owner dietary choice / dietary-policy | [#3](https://github.com/canzheng/workflow-skills-test/issues/3) | Backlog + blocked, exact choice remains unresolved | [] |
| Meal plan / meal-plan | [#4](https://github.com/canzheng/workflow-skills-test/issues/4) | Backlog + blocked | #1, #2, #3 |
| Shopping export / shopping-list | [#5](https://github.com/canzheng/workflow-skills-test/issues/5) | Backlog + blocked | #4 |

All IDs use the `pantry-planner:` prefix. The user's F14 launch already authorized
the evaluation batch and bounded ingredient execution; no separate approval click
or execution from readiness alone is invented. A subsequent open/closed search and
actual Issue collection read confirmed exactly these five unique identities and
consistent dependency URLs; no additional Issue was created. Human edits/rerun
contradictions are meaningful fixture proof in test_initial_backlog/test_records,
not claimed as deliberately induced live human edits. Fresh-task shaping rerun is
still required to establish independent continuation/discovery.

### Actual execution, Actions and review

Issue #1 was claimed with branch/base evidence, moved Ready → in-progress, and
implemented on its branch. Seven initial tests exercised actual CLI/storage:
oats500g/lentils300g, empty/zero, duplicate/invalid/malformed/missing/symlink,
denied staging, replacement interruption/retry and file-mode preservation.
Application argv verification was added to user-owned config. PR #6 began draft;
generic installed CI actually executed these project commands on GitHub runners.

| Actual event / tested head | Evidence and result |
| --- | --- |
| Bootstrap push, 5d055649 | [37207162368](https://github.com/canzheng/workflow-skills-test/actions/runs/37207162368): success |
| Implementation push, 382c5bc2 | [37207375910](https://github.com/canzheng/workflow-skills-test/actions/runs/37207375910): success |
| Draft PR, 382c5bc2 | [37207378478](https://github.com/canzheng/workflow-skills-test/actions/runs/37207378478): verification success; [37207378577](https://github.com/canzheng/workflow-skills-test/actions/runs/37207378577): trusted-base PR contract success |
| Body edit negative, 382c5bc2 | [37207571778](https://github.com/canzheng/workflow-skills-test/actions/runs/37207571778), job111451878303: expected failure, `pr.section` / Missing or empty Documentation section |
| Body restoration, 382c5bc2 | [37207626975](https://github.com/canzheng/workflow-skills-test/actions/runs/37207626975): success |
| Ready event, 382c5bc2 | [37207722331](https://github.com/canzheng/workflow-skills-test/actions/runs/37207722331): verification success; [37207722655](https://github.com/canzheng/workflow-skills-test/actions/runs/37207722655): PR contract success |
| Review-fix push, 9cf27f80 | [37208493878](https://github.com/canzheng/workflow-skills-test/actions/runs/37208493878): success |
| Review-fix PR, 9cf27f80 | [37208497635](https://github.com/canzheng/workflow-skills-test/actions/runs/37208497635): verification success; [37208495431](https://github.com/canzheng/workflow-skills-test/actions/runs/37208495431): PR contract success |
| Fixture-fix push, 2b4ecd69 | [37208863474](https://github.com/canzheng/workflow-skills-test/actions/runs/37208863474): success |
| Fixture-fix PR, 2b4ecd69 | [37208867389](https://github.com/canzheng/workflow-skills-test/actions/runs/37208867389): verification success; [37208865045](https://github.com/canzheng/workflow-skills-test/actions/runs/37208865045): PR contract success |
| Nested-data fix push, cec53770 | [37209327819](https://github.com/canzheng/workflow-skills-test/actions/runs/37209327819): success |
| Nested-data fix PR, cec53770 | [37209330624](https://github.com/canzheng/workflow-skills-test/actions/runs/37209330624): verification success; [37209329155](https://github.com/canzheng/workflow-skills-test/actions/runs/37209329155): PR contract success |
| Python-compatible schema fix push, 0b40f50e | [37209800631](https://github.com/canzheng/workflow-skills-test/actions/runs/37209800631): success |
| Python-compatible schema fix PR, 0b40f50e | [37209803102](https://github.com/canzheng/workflow-skills-test/actions/runs/37209803102): verification success; [37209801935](https://github.com/canzheng/workflow-skills-test/actions/runs/37209801935): PR contract success |

The PR became Ready before Issue #1 entered wf:review. It remains open/unmerged.
Independent native Codex review was requested at the Ready boundary through
[comment5980815385](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5980815385).
Bot review completed at 382c5bc2 on 2026-10-04T14:05:02Z, reporting two P2 findings:

- [Permission-loss cleanup](https://github.com/canzheng/workflow-skills-test/pull/6#discussion_r4177990682): reproduced denied replacement plus unlink masking the original error and leaving staging. Fixed best-effort cleanup to report both errors/path, documented recoverable residue, and added an actual unprivileged permission-revocation/recovery test (including a privileged-runner child dropping to UID65534).
- [Post-commit output failure](https://github.com/canzheng/workflow-skills-test/pull/6#discussion_r4177990683): an actual closed pipe exited120 after writing the new catalog. Documented the commit/output boundary and retry inspection; flushed output explicitly and added a real closed-pipe test asserting persisted data and duplicate retry rejection.

No original acceptance was weakened. Both fixes are at 9cf27f80, with nine local
tests and configured checks passing, no skips. Re-review was requested at
[comment5980926400](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5980926400);
review completed at 9cf27f80 on 2026-10-04T14:17:26Z and found one test-fixture
defect: root with umask077 created a0600 root-owned catalog, so its privilege-dropped
child failed before staging. A real Ubuntu root/umask077 negative reproduced this.
At 2b4ecd69, the child chowns both catalog and directory before dropping privileges;
application behavior and assertions are unchanged. Nine tests and configured
local/integration checks passed at that exact SHA in fresh Ubuntu with umask077,
alongside managed Cloud and GitHub runs. A final re-review was requested via
[comment5980979384](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5980979384);
the bot completed that review at2b4ecd69 on 2026-10-04T14:23:16Z and
[reported no major issues](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5981003869).
The three reproduced/remediated threads were replied to and resolved. This actual
review result does not waive the newly confirmed nested-JSON finding below, required
environment evidence, or independent final review of the rewrite itself.

### Cloud and Ubuntu evidence, with limits

Managed Cloud execution used Debian13/Python3.12.14. Production pinned setup,
doctor/check, actual skill reading/use, shaping/publication and ingredient execution
occurred here. The user supplied a separate consumer environment-onboarding chat;
its explicit reads/use and continuation are observed below, but fresh automatic
host discovery remains unproven. A prepared environment or an empty Start-skill UI
shortcut is not discovery.
Local `codex exec` and Cloud-task API attempts failed with proxy403 before model
execution; those failed attempts are not semantic/discovery evidence.

Actual fresh Ubuntu24.04.5 LTS remote clones at 382c5bc2, 9cf27f80 and 2b4ecd69 passed
the respective seven/nine/nine application tests and configured local/integration
verification, no skips; Python3.12.3, clean checkout and exit0. At 9cf27f80 the real
permission-loss test passed even though the container parent was root, because the
writer subprocess explicitly used an unprivileged UID. The pinned recipe/image is
recorded in [source acceptance](v2-acceptance.md). This proves Ubuntu portability,
not automatic skill discovery by an Ubuntu agent host or the user's private host.
The final 2b4ecd69 repeat used restrictive umask077, proving the fixture correction.

Docs reassessed/updated: consumer README, design references, docs/catalog.md
(CLI/schema/defaults/errors/examples, single-writer and crash durability limits,
cleanup residue and output commit boundary) and config verification. No prior
application specs existed; this bounded explicit CLI outcome needed no new OpenSpec
change, mandatory per-task plan or independent pre-PR review stage.

Still required under existing authorization: fresh Cloud task evidence and safe
rerun/continuation, Ubuntu agent discovery when that host is available, re-review
of the separately remediated nested-JSON finding, remaining representative fresh-host scenario obligations
and final rewrite-wide independent code/spec/doc review. F14 and the rewrite change
remain open; no archive or final completion is claimed.

### Earlier user-supplied Cloud report

The user supplied report-F14-before-fix.md from an earlier consumer continuation.
It reports clean adoption5d055649, successful Git fetch/selection of382c5bc2, explicit
reading/use of all three skills, seven baseline tests and eight tests after an
unpublished local repair64e5a4d7c1e37172aad7474fa52b0370e167e361. These are attributed
report results, not direct observations of that task's terminal or a published PR
revision. The supplied skill/method hashes exactly match the installed bundle here.

The report correctly separates filesystem reading/use from automatic host discovery:
its host skill catalog did not include the three skills and executor skills.list
returned empty. It also discloses that its context continued onboarding rather than
proving a fresh independent published task. Do not count this as F14 acceptance1.
Its safe one-shot MVP analysis retained all five outcomes/unknowns/exclusions, but
API proxy403 blocked live all-state identity/readiness reconciliation. Git reads
succeeded; reported CONNECT403 occurred before an API credential authorization
response, so supplying a token alone would not establish API network access.
The report says an api.github.com network draft was saved, not published/applied;
no effective environment change is inferred here.

Its nested-JSON finding was independently reproduced here on current2b4ecd69:
a10000-level invalid array causes show and add to exit1 with an uncaught
RecursionError traceback while preserving original bytes. This violates documented
actionable data-error reporting and was not fixed by the earlier PR review changes.
The report's local commit was not on the remote branch. Reading the user-supplied
Cloud thread01a1072e-11d1-72a1-aaf2-28f8b59af012, host durable, title
"Set up workflow-skills-test", directly confirmed its idle status, actual command
results and onboarding context. Its update fetched9cf27f80, preserved local64e5a4d7
on its branch, detached for verification and passed nine tests/configured checks.
It did not replay the nested-data repair. This is observed separate-context
continuation/verification, not a fresh task's automatic skill discovery or successful
API reconciliation. No active conflicting implementation was observed.

The confirmed nested-data fix was then implemented on the canonical branch at
cec53770c17f670615f8f3bd610bde70d424434c: decoder-only RecursionError becomes
an actionable flat-schema ValueError. An actual show/add regression failed before
the fix (two subtests), then all ten tests passed with preserved bytes, empty stdout,
no traceback/residue and original assertions intact. Docs now explain this invalid
input. Same-SHA managed Cloud, fresh Ubuntu root/umask077 and configured
local/integration verification passed; actual push/PR/metadata runs passed above.
Native re-review atcec53770 completed and found a Python3.14 decoder difference:
deep arrays can decode successfully and then received generic shape errors, missing
the promised flat-schema guidance. Actual Python3.14.8 reproduced the original
two failing regression subtests. At0b40f50e, existing root/value schema validation
provides flat-schema guidance independently of decoder recursion; no artificial
depth limit or support-range narrowing. The unchanged no-traceback/preservation
assertions now exercise actual show/add on deep arrays, deep amount values and
already decoded invalid root/value shapes. Ten tests pass on managed Python3.12.14,
fresh Ubuntu3.12.3 with root/umask077, and a separate Python3.14.8 container with
root/umask077 using the exact clean0b40f50e checkout mounted read-only. That container
is not claimed to be an Ubuntu/fresh-agent clone; observed image digest is
`python@sha256:c3e521df8b2b498a7a682e7e18676771cb80c6b75b8699af886b2d554ce40151`.
[Final native re-review requested](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5981120139),
That historical request found locale-dependent catalog reads, then surrogate-escaped
CLI IDs. Both were reproduced and repaired, with an actual ASCII-locale round-trip
regression retaining malformed/duplicate/unchanged-byte assertions. At
`f95f0cae3b87bc8031b00a4150cf9670251ae978`, all 11 tests pass on Cloud Python3.12,
fresh Ubuntu Python3.12 and actual Python3.14.8 under root/umask077. Current-head
Codex review [5981620802](https://github.com/canzheng/workflow-skills-test/pull/6#issuecomment-5981620802)
reports no major issues; all addressed inline threads are resolved. Actual push
[37213062645](https://github.com/canzheng/workflow-skills-test/actions/runs/37213062645),
PR [37213065265](https://github.com/canzheng/workflow-skills-test/actions/runs/37213065265)
and metadata [37213064024](https://github.com/canzheng/workflow-skills-test/actions/runs/37213064024)
pass. No unrelated backlog work is dispatched. The report's task-specific no-publication
limit is evidence about that task, not a new authorization instruction for this one.

## Pending authorization

1. **Real merge → completed Issue observation.** PR #6 is Ready, Issue #1 is open
   wf:review. No merge, completed closure or simulated merge/closure occurred.
   With later explicit authority, perform the real reviewed merge and observe valid
   Issue completion only after the remaining delivery contract is satisfied.
2. **Required-check/protection/ruleset configuration.** Read-only consumer rulesets
   returned403: Upgrade to GitHub Pro or make this repository public to enable this
   feature. Classic main protection returned403: Resource not accessible by
   integration. Neither proves classic protection is absent. Actual successful
   `v2 verification` and `v2 PR contract` jobs prove execution, not required-check
   enforcement or blocked merge. Do not change visibility, account plan, protections
   or rulesets without separate authority. An owner can inspect the existing state;
   any later mutation follows the [enforcement runbook](../workflow/checks.md).

Release publication and remote branch deletion also remain unauthorized; neither
is needed for the currently authorized pilot path.

## Exact next fresh Cloud action

Use the existing consumer environment and isolated checkout at
`/workspace/workflow-skills-test`, branch `pilot/ingredient-catalog`, full SHA
`f95f0cae3b87bc8031b00a4150cf9670251ae978`. Inspect/preserve changes, fetch and
confirm the actual head; if another task moved it, coordinate rather than reset.
Read AGENTS.md, workflow contract/index/config, docs/design.md, all three installed
skills, Issues #1–#5 and PR #6. Capture actual host-discovered names and actual use.
Perform an identity-safe one-shot design backlog rerun without duplicates, acceptance
rewrites or dispatch of #2–#5. Verify #1/remediation and native review state, run
configured verification, record exact revision/OS/results and post a handoff on #1.
Do not merge, close completed, change administration, publish or delete branches.
Source Issue #15 owns aggregate F14 acceptance; keep consumer and source SHAs distinct.


## Pinned ignored dependency refinement (S34)

The user subsequently approved tracked project policy/config plus tracked dependency
pin, with only shared skills materialized locally and ignored. The older application
pilot above does not prove that revised installation model. Independent infrastructure
outcome [Issue7](https://github.com/canzheng/workflow-skills-test/issues/7) was searched
across open/closed identities before creation and claimed Ready → in-progress.
New branch `pilot/shared-skill-bootstrap` from unchanged main5d055649 uses source pin
`47320c363e538d2c8423e11e5ca9121c2d0303da` and consumer SHA
`539580779e52eef5b976a0460d7d18e16833c2b0`.

Existing managed hashes were verified before migration. New setup refused tracked
shared files before writes; explicit index-only untracking of exactly three namespaces
preserved bytes. Setup then updated owned policy/tools/docs/CI/pin and added exactly
three anchored ignore rules. Project-owned `pantry-project` remains tracked. Config,
README/design, old application branch/PR and main were preserved. Repeated setup and
bootstrap each returned `changes: []`. The native published tree exactly matched
local Git tree `b3a090864684ccc388c4a277e384db1e28bfe357`.

Source47320c3 passed 62 tests with no skips and strict current/delta OpenSpec checks on
Debian Cloud and fresh Ubuntu24.04.5 clones; source Actions
[37213148746](https://github.com/canzheng/workflow-skills/actions/runs/37213148746) and
[37213152015](https://github.com/canzheng/workflow-skills/actions/runs/37213152015) pass.
An initial Ubuntu run without optional npm dependencies had two explicit skips;
the prepared repeat installed pinned tooling and passed all62 without skips.

Actual fresh consumer clones in Cloud runtime and Ubuntu lacked shared skills,
fetched the same pinned source via Git, materialized four pinned assets, passed
configured check/doctor, repeated bootstrap as a no-op and remained Git-clean.
All shared hashes and tracked project skill matched in both environments. The
consumer has no application implementation on this branch; default checks certify
workflow integrity only, not application acceptance or native agent discovery.

[PR8](https://github.com/canzheng/workflow-skills-test/pull/8) began draft. Actual push
[37213277277](https://github.com/canzheng/workflow-skills-test/actions/runs/37213277277),
draft PR [37213280986](https://github.com/canzheng/workflow-skills-test/actions/runs/37213280986)
and trusted-base metadata [37213281196](https://github.com/canzheng/workflow-skills-test/actions/runs/37213281196)
passed. Job111468589629 explicitly ran `Materialize pinned shared skills` successfully.
After self-verification/docs reassessment, PR8 became Ready before Issue7 entered
wf:review. Native semantic review was requested via comment5981635279; its result
must be read before claiming review completion. No merge/Issue closure occurred.

The exact published environment script and fresh-task prompt are in
[Cloud bootstrap handoff](cloud-bootstrap-handoff.md). Native pre-agent discovery/use
on a fresh Cloud task and Ubuntu agent discovery remain unperformed. Actual merge →
valid Issue completion and enforcement configuration mutations remain pending separate
authorization; runtime bootstrap and workflow checks do not substitute for them.

### Reviewed corrections and current pinned consumer

Subsequent independent consumer review found broad excludes hiding project skills
and negations exposing shared skills during setup. Both were reproduced against the
exact old consumer clone, then fixed at source133dcff with effective Git policy preview
before writes plus bootstrap/check/doctor validation. Consumer3b64cf re-review reports
no major issues (comment5981763538); addressed threads resolved.

Source ReadyPR16 review independently found incomplete installed runtime validation
and extra ignored assets reported clean. Failing-before public regressions confirmed
both; sourcecb2cde7 requires all seven runtime modules and marks unmanaged dependency
content dirty. Further source review found source-check completeness drift and an
external OpenSpec archive accepted through a symlink. Failing-before tests confirmed
both; source11fa051 shares runtime requirements and validates archive root/matches.
No original acceptance/assertions were weakened. Targeted final reviews were requested;
read actual results before claiming final semantic acceptance.

Current consumer branch `pilot/shared-skill-bootstrap`, SHA
`5efc5f5ffdcab46a440b2cb2237924ee476a5bd9`, pins source
`11fa051a7c4af359bd4728e1edf69cd8c7a61259`. Source68 tests/no skips, public check and
strict OpenSpec checks pass on Cloud Debian and fresh same-SHA Ubuntu24.04.5;
source push[37214817774](https://github.com/canzheng/workflow-skills/actions/runs/37214817774)
and PR[37214821507](https://github.com/canzheng/workflow-skills/actions/runs/37214821507)
pass. Consumer exact-head fresh Cloud-runtime/Ubuntu clones fetch that pin, materialize
four exact hashes, repeat changes:[], pass check/doctor and remain Git-clean with
project skill tracked. Actual consumer push
[37214896516](https://github.com/canzheng/workflow-skills-test/actions/runs/37214896516),
PR[37214899407](https://github.com/canzheng/workflow-skills-test/actions/runs/37214899407),
metadata[37214897768](https://github.com/canzheng/workflow-skills-test/actions/runs/37214897768)
pass. No merge/completed closure/admin mutation occurred.

The user clarified that environment setup must handle a brand-new repo without tools.
The [unified published setup script](cloud-bootstrap-handoff.md) now fetches an exact
seed/adopts only when no tracked manifest exists; otherwise it bootstraps the existing
pin. The exact script passed on a new Git checkout without tools, then repeated with
no fetch/file changes; tools and pin are trackable, shared skills ignored. Generated
adoption files must be reviewed/committed. This proves the script's behavior, not the
host's preparation persistence/ordering or initial agent discovery. Those remain the
fresh published Cloud gate. Ubuntu agent discovery is also unperformed; merge→Issue
completion and enforcement mutations remain separately pending authorization.

### Current unified environment entrypoint

Source `7e71186ec8146b682f4c4cf40c8da5ecb6d3f608` also closes validated installed
manifest completeness and ledger-symlink gaps. Both have failing-before public tests;
all70 tests/no skips and strict checks pass on Debian Cloud and fresh Ubuntu24.04.5.
Source push[37215771822](https://github.com/canzheng/workflow-skills/actions/runs/37215771822)
and PR[37215776553](https://github.com/canzheng/workflow-skills/actions/runs/37215776553)
pass. Partial uninstall provenance is preserved for recovery; diagnostics no longer
mistake it for a complete installed bundle.

Consumer current branch `pilot/shared-skill-bootstrap`, SHA
`79efd96276e25e2c1a706a3c7972dbebf32d2a0a`, pins that exact source. The real project-owned
`.workflow/cloud-setup.sh` and README expose the same complete pastable environment
command. It was executed against a new Git root without tools: pinned fetch/adoption
succeeded; repeat skipped fetch, changed no file/index and returned bootstrap changes:[].
Exact-head fresh consumer clones on Cloud runtime and Ubuntu both ran that actual
script twice, matched pinned shared hashes, kept project skill tracked and remained
Git-clean. Consumer push
[37215967922](https://github.com/canzheng/workflow-skills-test/actions/runs/37215967922),
PR[37215972442](https://github.com/canzheng/workflow-skills-test/actions/runs/37215972442),
metadata[37215970011](https://github.com/canzheng/workflow-skills-test/actions/runs/37215970011)
pass. These are script/runtime/CI results, not native pre-agent skill discovery.

Consumer review's stale README omission was confirmed and fixed. The request to make
workflow.py bootstrap implicitly adopt an absent pin was not accepted: an entirely
unadopted repo has no CLI. The standalone environment script performs pinned fetch
and adoption before invoking CLI, while repeatable bootstrap retains its approved
pin-only/project-preservation contract. Review replies provide actual script evidence;
the concrete project-owned entrypoint removes the earlier visibility ambiguity.
Final current source/consumer review outcomes remain required and must be read.

Use the latest [Cloud handoff](cloud-bootstrap-handoff.md), publish/apply the full
command in environment setup/maintenance, select the current consumer branch/SHA,
and start a genuinely new task outside onboarding. Capture initial host discovery
before agent-side installation. Generated adoption files must be committed in a
new project; this pilot has already committed them. Ubuntu agent discovery, remaining
fresh-context scenario/semantic acceptance, real merge→Issue completion and admin
mutations remain separately pending. No merge or completed closure is simulated.

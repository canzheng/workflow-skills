# Wider local boundary review — 2026-10-05

## Latest private-cleanup checkpoint — 2026-10-05

Tested source `7262627c3ff99d8f4e7ead714f264278630c1ef8`,
rewrite/workflow-skills-v2/Ready PR16, passes162/no skips on managed
Python3.12.14 (166.352s) and Ubuntu24.04.5/Python3.12.3 (144.640s), plus
strict OpenSpec all5/public checks. Consumer `32b0c0b699bc9b530cd3fdf851ba72683e44efb9`,
pilot/shared-skill-bootstrap/Ready PR8/Issue7, pins that source. Current Actions
and repaired-head semantic reviews are recorded separately in the PR checkpoint.
Source push37355342099 and consumer push37355461469/PR37355471904/existing-main
metadata37355466862 pass; source PR37355350465 is pending at recording time.
New trusted-base deployment/events still await authorized adoption merge.

The five-minute monitor observed source review5418785129 completed atf6b5479 and
consumer comment6000382283 clear at9c51df9, then disarmed both targets. Source P2s
4187260995/4187261007 independently reproduce: two old-code tests fail seven
subcases/no errors (six inode/symlink staging/removal replacements and one created-
directory replacement). Cleanup now atomically captures the actual public entry
into exclusive mode-0700 private storage on the same filesystem, then validates
its bytes/mode/inode before unlink/rmdir. Mismatches restore with no-replace;
recreated public paths preserve both entries and their quarantine location in
recovery-index.json. In-place edits through held captured descriptors still get
concurrent_backup recovery. Missing libc support preflights before staging.

Focused36 setup tests plus one quarantine-collision control and six global tests
pass. Existing destination/rollback/removal, parent-chain, bytes/mode/inode/symlink,
raw-index and backup assertions remain discriminating. No cleanup-storage rules
are added to .gitignore; only the same four dependency namespaces are ignored.
Private capture/recovery changes are documented in source/consumer operations,
architecture and current/active adoption scenarios. The earlier atomic mutation,
malformed native-input and PR-body-anchor repairs remain covered; detailed prior
proof is immutable at https://github.com/canzheng/workflow-skills/blob/f6b54794ea80d00bd18d40f2ed0ced1d084502ad/docs/validation/wider-boundary-review.md .
Recovery remains best-effort, without a process lock or multi-file atomic promise.

Actual installed39 tests pass managed (73.973s) and Ubuntu
(69.032s), including the new capture and restoration-collision cases.
Fresh managed local clone of the native-API-verified remote commit and fresh Ubuntu
remote clone materialize11 missing ignored dependencies, match20 managed hashes,
preserve four narrow ignores/project skill/files/raw index and repeat offline as
no-op. Retained force-tracking, index-only nested policy, layout, concurrency,
discovery and rendering negatives pass. Literal exact-pin Ubuntu GitHub fetch-and-run
first adoption/repeat exits0 without creating an index.

Native remote tree057265bacdf778b311a1b56b082005a97d8bcfed matches reviewed
local721f5e97eee8a499732217027cad783536cf6e3b, parent9c51df9. Exact native commit
bytes hash to its published SHA; guarded non-force publication and same-tree local
ref reconciliation preserve clean files/index. Source-owned update preserves config,
all skill bytes and raw index33540a322bb2a14b4f6c1687d031c9cd303bb922115cc6e2e1b3454ed9446d76
before caller staging. No shared skill files changed, so native Ubuntu startup catalog
and actual three-skill use remain revision-bound at9bd23d72/a75c3f2 with identical hashes.

F01–F13 implemented/verified/review-ready; F14 partial pending repaired-head semantic
review and native archive/final checks. Earlier consumer clear at9c51df9 predates this
repin. Five-minute active-turn monitoring follows each new review request and stops
on completion; it is not a persistent post-turn wakeup. Cloud remains deferred;
historical Ubuntu26 full-suite invalid-JSON cause remains unexplained. Actual global-
host installation/discovery is unperformed. Required-check enforcement was observed
read-only; new schema5 trusted-base metadata deployment/source PR-contract administration,
real merge and valid completed-Issue observation remain pending authorization.
No merge/closure/admin/global/auth/release/remote deletion. Next: repaired-head review,
then native archive/final checks; obtain separate authorization for real delivery.


## Latest source-check compatibility repair — 2026-10-05

This checkpoint supersedes earlier current/default claims below. Source
`9d5489ffa11cf8bbde3f4c569c17a526e5d86c98`, rewrite/workflow-skills-v2:143 tests/no skips
pass on managed Python3.12.14 (148.826s) and Ubuntu24.04.5/Python3.12.3
(124.375s). Public check, strict OpenSpec all5 items and diff hygiene pass.
Consumer `255371e48f46549b4099182d66c598d767235277`, pilot/shared-skill-bootstrap,
Ready PR8/Issue7, pins this source. Published tree6de3c30739d5664bc1709129d62ca248ce7f4b96
matches reviewed local2116f1ca tree, parent66913db, guarded non-force publication.
Update changes only ignored checks.py and tracked manifest; configuration/all
skill bytes/raw index3124b4a010d9d81d8c0eaeb19f7d66d5fbf3991c91c48814a272151f95a12be7
remain unchanged during setup, before caller staging. Consumer review5996447243
was clear at66913db; it is not approval of the repinned head.

Source review5416098884 at151476c returned P2 comment4185120389: a complete
legacy tracked bundle installs and its installed checker passes, but source check
reports seven nonexistent new-layout destinations as missing. The finding was
independently reproduced with public CLI calls. Wider author review additionally
finds mixed source inventories accepted despite setup rejecting them. Shared
required_assets now governs source checks as well as setup/provenance/bootstrap.
Both new and legacy tracked source/installed layouts pass. Each of seven missing
runtime mappings is rejected in each layout, and mixed inventories fail with
structured invalid-input status. Schema5 remains new-layout only. No existing
acceptance/assertions were weakened. Before control:3 tests/2 failures/no errors;
after focused tests3 pass (2.275s). An intermediate added fixture lacked a local
verification command; its harness error was corrected, not counted as a defect.
Development guidance is updated; existing compatibility specifications already
state this behavior, so no behavior-contract delta is needed.

Actual managed/Ubuntu fresh remote clones start without runtime/skills. Source-first
initialization materializes11 exact dependencies/matches20 managed hashes; installed
check/run-local/doctor/offline no-op, four narrow ignores, tracked project skill,
tracked-file and raw-index preservation pass. Installed rollback/concurrency,
force-tracked setup, index-only policy, native-input/discovery/rendering and28
namespace controls retain their original assertions. Actual installed fourteen-test
layout/CI/source-check suite passes both hosts (52.824s/46.296s). The literal pinned
GitHub fetch-and-run installer and repeat pass on fresh Ubuntu without an index.

Consumer current push[37330126608](https://github.com/canzheng/workflow-skills-test/actions/runs/37330126608),
PR[37330146379](https://github.com/canzheng/workflow-skills-test/actions/runs/37330146379)
and existing-main metadata[37330140351](https://github.com/canzheng/workflow-skills-test/actions/runs/37330140351)
pass. Source PR37330017724 passes; source push37330000692 and documentation-head
CI are tracked in the live checkpoint. New metadata executes locally against its
trusted base pin; actual main deployment/events await authorized adoption merge.

F01–F13 implemented/verified/review-ready; F14 partial pending repaired-head semantic
review, archive/final specs/docs checks, then separately authorized real merge and
valid completed Issue observation. Native Ubuntu catalog/actual use stays bound to
original9bd23d72/a75c3f2 with unchanged skill hashes. Cloud deferred, real global-host
use unperformed, historical Ubuntu26 invalid-JSON cause unexplained. Read-only
consumer two-check/source verification enforcement remains observed; source
PR-contract administration/base deployment pending. No merge/closure/admin/global/
auth/release/remote deletion. Next: current-head review; archive only after required
premerge acceptance. Five-minute review monitor is armed on each new request and
disarmed on completion; no persistent wake-up after this active turn is claimed.

## Latest runtime-layout and CI-provenance repair — 2026-10-05

This checkpoint supersedes earlier current/default statements below. Source
implementation/pin `4449a1e6d03b6e055446735b89c4630b0c8b9d85`,
rewrite/workflow-skills-v2: all142/no skips pass on managed Python3.12.14
(137.599s) and Ubuntu24.04.5/Python3.12.3 (116.116s), strict specs and public check.
Consumer `66913db29472d8277002b068205fc05db62b2bbf`,
pilot/shared-skill-bootstrap/Ready PR8/Issue7, pins this source. Published
bf8f8e5c1cba1b0858169a1053ab2991263c7add matches reviewed local740436647 tree,
parentb33b0d4 and guarded non-force publication. Update preserved config/all skills
and raw indexb56b1fa2e37bcd6cf57f47f6502fd1082a759be5f5145d281b53d95d4eb92d20.

The prior consumer review completed atb33b0d4 with no major issues (comment5996081813).
The source review5415759761 at946dffe returned P2s4184890020/4184890034.
Five-minute monitors detected completion and disarmed before fixes. Both findings
were independently reproduced before acceptance. Exact old946dffe helpers accept
legacy-layout ignored schema5 setup/check/run-local/doctor/bootstrap while the
installed CI command fails2 because the new CLI is absent. Before controls also
show both installed YAMLs selecting a nonexistent source checker when an unrelated
tracked bundle marker exists. New structural-layout/CLI controls fail before repair;
no fixture errors or permissive acceptance changes are counted as proof.

Schema5 now requires .agents/tools/workflow. Ignored setup from a legacy bundle
rejects before writes; existing schema3/4 verification and explicit tracked legacy
setup remain supported. Both CI preparations prioritize consumer provenance over
unrelated bundle markers. Verification chooses the installed runtime from the
manifest; PR metadata still uses only the trusted base pin. Doctor avoids probing
an unrelated source marker once consumer provenance exists. Regressions execute
both actual YAML preparations/commands, preserve unrelated marker bytes/raw index,
and prove legacy tracked verification succeeds at its real runtime path.
Current/delta adoption specs, source/consumer operations and architecture match.

Actual managed/Ubuntu fresh remote clones start with no helper/skills; source-first
initialization materializes11 exact files/matches20 managed hashes. Installed
check/run-local/doctor/offline repeat and raw-index/tracked-file proof pass; prior
rollback/native-input/index controls remain intact. The actual installed twelve-test
layout/CI suite passes on managed runtime (46.812s) and Ubuntu (42.605s). Literal
pinned GitHub fetch-and-run first adoption and repeat both pass on fresh Ubuntu
without an index or pre-existing helper. Four narrow ignore rules only; project
skills/tools and AGENTS/config/CI/docs/pin remain tracked.

Consumer current push[37322931564](https://github.com/canzheng/workflow-skills-test/actions/runs/37322931564),
PR[37322942245](https://github.com/canzheng/workflow-skills-test/actions/runs/37322942245)
and existing-main metadata[37322935924](https://github.com/canzheng/workflow-skills-test/actions/runs/37322935924)
pass. Source pin push37322805393/PR37322816322 and documentation-head CI are
recorded in the live PR checkpoint. New trusted-base metadata YAML is executed
locally; its actual deployment/events on main await authorized adoption merge.

Native Ubuntu catalog/use stays revision-bound to original9bd23d72/a75c3f2 and
unchanged skill hashes. F01–F13 implemented/verified/review-ready. F14 partial:
current semantic reviews, archive and final specs/docs checks remain, then real
merge→valid Issue completion and deployed-base observation require separate
permission. Cloud deferred, real global-host use unperformed, historical Ubuntu26
JSON error unexplained. Consumer two checks and source verification enforcement
were read-only confirmed; source PR-contract administrative configuration remains
pending. No merge/closure/admin/global/auth/release/remote deletion. Next: current
Ready-head review; archive only after premerge acceptance, then final checks/review.


## Current ancestor/index checkpoint — 2026-10-05

This checkpoint supersedes earlier current/default statements below. Tested source
implementation/pin `0f6b6766da7a86a039108891ec051306963425ae`,
`rewrite/workflow-skills-v2`: all138/no skips pass on managed Python3.12.14
(144.107s) and Ubuntu24.04.5/Python3.12.3 (120.835s). Strict specs and public
check pass. Consumer `b33b0d4a938b2718a3adb686f4899b4689d46b20`,
`pilot/shared-skill-bootstrap`, Ready PR8/Issue7, pins this source. Published
ce912ff51f434f04584e9875ab4356cf047b8271 matches reviewed local3fdef990 tree,
parentd8ed0ab, guarded non-force publication. Source-owned update preserves
config, all shared/project skill bytes and raw index
b8ab7d37b1ccbc2b9b088e892c95678d5da570a8d2cc8eff37d596023db5a659.

Additional wider review reproduced an index-only dependency ancestor file:
intact working directories hid a non-bootstrapable staged snapshot. The before
control fails3 subcases/no errors; centralized ancestor preflight now covers
setup, check, doctor, bootstrap and independently validated staged installation.
All reject without file/index changes; coherent migration still passes before
old HEAD is merged. Source/consumer operations, current/delta adoption specs,
README install example and Ubuntu handoff were reassessed. The delta now uses
MODIFIED for requirements already present in current specs and supplies the
release Purpose, so archive preparation does not duplicate implemented contracts.

Actual fresh remote clones on managed runtime and Ubuntu start with no shared
runtime/skills; source-first bootstrap installs11 canonical dependency files,
matches20 manifest hashes, passes check/run-local/doctor and offline no-op repeat,
and preserves tracked files/raw index. Prior installed rollback/native-input/
indexed-policy controls pass. The installed six-test layout suite passes on both
managed runtime (50.710s) and Ubuntu (37.311s). The literal pinned fetch-and-run
install command succeeds twice in a fresh Ubuntu Git root without creating an
index or requiring any existing consumer helper. Only the four dependency
namespaces are ignored; project skills/tools and v2 AGENTS routing remain tracked.
The first mounted-source Ubuntu attempt failed Git ownership policy; rerunning
with an owned source copy passed without changing global Git configuration.

Consumer current-head push[37320356900](https://github.com/canzheng/workflow-skills-test/actions/runs/37320356900),
PR[37320366947](https://github.com/canzheng/workflow-skills-test/actions/runs/37320366947)
and existing-main metadata[37320361118](https://github.com/canzheng/workflow-skills-test/actions/runs/37320361118)
pass. Source pin push37320277173/PR37320287331 and later documentation-head CI
are recorded in the live PR checkpoint. New trusted-base pin-fetch metadata is
locally exercised; actual deployment/event execution on main remains pending an
authorized merge, distinct from existing-main metadata success.

Native Ubuntu discovery/actual all3-skill use retains its original9bd23d72/a75c3f2
revision-bound evidence because all four shared skill hashes remain unchanged.
F01–F13 implemented/verified/review-ready; F14 partial pending final current-head
semantic review and rewrite archive/final specs/docs checks. Cloud deferred,
real global-host use unperformed, historical Ubuntu26 source JSON error unexplained.
Consumer two required checks and source required verification were observed;
source PR-contract configuration/deployment and real merge→valid completed Issue
observation remain separate authorization gates. No merge, completed closure,
admin, global/auth, release or remote branch deletion. Next: current-head semantic
reviews with awaited five-minute monitors; archive only after premerge acceptance.


## Final runtime relocation and ancestor repairs — 2026-10-05

This checkpoint supersedes earlier current/default revision statements below.
Source pin `f05cf27df47e008bf52e6f14a8dbd6bbf53e4f80`, rewrite/workflow-skills-v2:
all137/no skips pass on managed Python3.12.14 (133.209s) and Ubuntu24.04.5/
Python3.12.3 (113.295s), strict specs/check and diff hygiene. Consumer
`d8ed0abca40a7fa4ed092f4facfb25fefee30977`, pilot/shared-skill-bootstrap/ReadyPR8,
pins this exact source; reviewed tree6c449ba5f53319c81c9b98cf81be5e2642f16c6c
matches own localfdf5f3538298b313983238ef03f80ed999329ac9, parent4778478 and
guarded non-force publication. Source-owned update preserves config, all skill
bytes and raw index3cbd81ddf8b4146417f8f93f3a48c26c3b6517c1dc3a2b09b8b56aeef72e7602.

Completed review5415017418/5415023570 on prior heads returned source4184370571
(partial old-runtime deletion), source4184370585 (deleted namespace ancestor)
and consumer4184374853 (unmatched migration pathspec). All were independently
reproduced before acceptance. Four updated regression tests fail80 subcases/no
errors on the oldcfa1dfb CLI; a separate mixed-runtime source before-control fails
as well. Early harness errors were corrected before interpreting those controls.
The initial repair candidate at7c69 ran136 tests with one failure: the original
positive cleanup still expected setup to recreate a HEAD-owned namespace after
cached removal alone. Retained all original negative assertions, added the new
HEAD-deletion rejection/no-write proof, then committed explicit retirement only in
the owned fixture before the original successful adoption/index-preservation control.
Final137 passes; no broadening of accepted broken behavior or disabling of checks.

New validation rejects each of the seven retired shared Python filenames in a
new-layout index and staged snapshot, for ignored and tracked compatibility. All
14 destination ancestor paths preserve indexed/HEAD deletions through preview/apply,
three ownership states and both storage modes. Fresh reserved legacy collisions
are refused without overwrite. Bundles/provenance mixing old/new canonical runtimes
are invalid before writes; setup and isolated global-skill installer controls
preserve consumer bytes/index and absent global target. The exact documented
untrack command now uses --ignore-unmatch and executes successfully for old3/4
and new-layout tracked3 migrations. Unrelated old-directory project tools remain
tracked/unchanged. Current/delta adoption specs and source/consumer operations match.

Actual fresh remote clones on managed runtime and Ubuntu start with no shared CLI
or skills, then source-owned initialization materializes11 canonical files/matches20
managed hashes, passes installed check/run-local/doctor/offline repeat and preserves
tracked files/raw index. Retained installed public negative probes all pass. The
new five-test layout/index/mixed-inventory suite additionally runs against the
actual installed public CLI and uses its bytes in source fixtures: pass on managed
runtime and Ubuntu (34.573s). Pinned source fetched directly in a fresh Ubuntu repo
also passes first adoption and repeat without creating an index. Only four anchored
shared namespaces are ignored; project skills/tools remain trackable.

Consumer push[37318120161](https://github.com/canzheng/workflow-skills-test/actions/runs/37318120161),
PR[37318130720](https://github.com/canzheng/workflow-skills-test/actions/runs/37318130720)
and existing-main metadata[37318125172](https://github.com/canzheng/workflow-skills-test/actions/runs/37318125172)
succeed. Source pin push37318074374/PR37318081307 also succeed; later documentation-head
CI is recorded separately in the live PR checkpoint. New trusted-base pin-fetch metadata YAML
is locally executed; actual deployment/events on main await authorized adoption
merge. Native Ubuntu discovery/actual all3-skill use stays tied to original9bd23d72/
a75c3f2 and unchanged four skill hashes, rather than inferred from file existence.

F01–F13 implemented/verified/review-ready. F14 remains partial until current-head
semantic review and final rewrite archive/spec/docs checks. Five-minute active-turn
monitors disarmed completed reviews before repairs; no persistent wake-up is claimed.
Cloud deferred, real global-host use unperformed, historical Ubuntu26 source-suite
JSON error unexplained. Consumer required checks observed; source verification now
required, source PR-contract configuration/deployment and real merge→valid completed
Issue observation remain separately pending. No merge/closure/admin/global/auth/
release/remote-deletion action. Next: final current-head semantic review; archive
only after premerge acceptance, then rerun final specs/docs/checks/review.

## Shared runtime layout and final index preflight repairs — 2026-10-05

This checkpoint supersedes earlier current/default statements below; their exact
revision-specific results remain historical evidence. Shared skills and scripts
now have one consumer ownership model: schema5 ignores the three shared skill
namespaces and `.agents/tools/workflow/`, with one exact tracked pin. Project
policy/config/CI/templates/docs/project skills/tools remain tracked. Explicit
tracked compatibility stores both runtime and skills; source authors the runtime
in tools/workflow. Fresh clones fetch the pinned source-owned entrypoint before
an absent consumer CLI can be invoked. CI does the same; metadata selects only the
trusted base pin and treats head content as data. Existing schema3/4 startup does
not migrate. Reviewed updates retire only owned legacy runtime files, with caller
staging/untracking and config-path edits.

Source pin `ffe656fe8247ce96805fbf095fba8108c1253774`, branch rewrite/workflow-skills-v2.
Runtime commitc5c20d219c71d5367e69edec6795581f1a147a8f passed132/no skips on managed
Python3.12.14 (95.051s) and Ubuntu24.04.5/Python3.12.3 (79.927s), with strict specs.
Source verify132 passed (93.192s); the pinned follow-up changes documentation only.
Source push[37313633419](https://github.com/canzheng/workflow-skills/actions/runs/37313633419)
and PR[37313641419](https://github.com/canzheng/workflow-skills/actions/runs/37313641419) succeed.

Consumer `47784787f17803da3051deed92bd818bdae388c1`, pilot/shared-skill-bootstrap,
pinsffe656f. Tree5cde84d923738d051561e09ecfb5d10d119313b9 matches reviewed local
6d83f3ef8ebb519d4daeb851b6c7dd31d3c28d77 with parenta0401b8 preserved by guarded
non-force publication. Installer preserved raw index
44d1248704655708bef14b4024fcd75daef7f26359ef9c86762c962d1f47b020,
project configuration and pantry-project bytes before caller staging. Only the
workflow argv path was explicitly changed afterward. Old tracked runtime deletions
were reviewed/staged; all11 dependency files remain untracked and ignored.
Fresh actual remote clones on managed runtime and Ubuntu begin with no runtime or
shared skills; source-owned setup materializes11 exact files, matches20 managed
hashes, passes installed check/run-local/doctor/offline repeat and preserves tracked
files/raw index. Installed public negatives retain force-tracking/index-only nested
policy, concurrent file/directory/staging recovery, NUL/native argv/URL/discovery
and UTF8/ASCII controls; fresh shared/runtime indexed namespaces cover28 cases.
An initial proof harness imported Python modules before disabling bytecode and
created an unmanaged runtime cache. Corrected harness reruns pass; the public CLI
already disables bytecode. No product failure or weakened assertion is inferred.

Consumer push[37313732453](https://github.com/canzheng/workflow-skills-test/actions/runs/37313732453),
PR[37313742632](https://github.com/canzheng/workflow-skills-test/actions/runs/37313742632)
and metadata[37313737643](https://github.com/canzheng/workflow-skills-test/actions/runs/37313737643)
succeed. Push job111775163509 logs prove exactffe656f fetch,11-file bootstrap and
execution at .agents/tools/workflow. Metadata job111775182016 still runs the
existing main checker/YAML: the new base-pin fetch workflow is tested by executing
its actual YAML preparation locally, but deployment on main and its actual event
execution require the separately authorized adoption merge. These are distinct.

Latest P2 consumer4184018183 (policy-only initial staging) and source4184041079
(index/HEAD-owned missing initial destinations) were reproduced before acceptance.
The repair detects newly staged policy/config or newly introduced routing/ignore
blocks;5-context x3-command tests preserve files/raw index. Missing owned project
destinations reject before preview/apply, including committed removals from the
index;13 paths x3 ownership states x2 modes provide78 controls (all78 fail before
repair, all pass afterward). Fresh indexed dependency controls expand to runtime.
Project-specific tools remain trackable under working and staged ignore snapshots.
Existing discriminating assertions and rollback/global compatibility are retained.

Read-only enforcement now observes consumer Active24484016 requiring both checks,
no bypass; source Active24457981 now requires v2 verification, no bypass. Source
v2 PR contract enforcement/base deployment and real merge→valid completed Issue
observation remain separate authorization boundaries. Neither ruleset requires an
approval review; green/mergeable is not semantic approval. Original independent
Ubuntu26.04 native initial catalog/actual all3-skill use remains at unchanged skill
hashes and original revisions. Cloud deferred, optional real global-host use
unperformed, historical Ubuntu26 source JSON error unexplained. Final current-head
semantic reviews and rewrite archive/final docs/spec checks remain pending. No
merge/completed closure/admin/global/auth/release/remote-deletion mutation.

This is a targeted primary-author review requested by the user after serial PR P2
findings. It is not independent semantic approval or a new mandatory pre-PR stage.
The resolved GitHub NUL-path finding motivated inspection of core validation,
source setup/global setup, bootstrap, staged policy, mechanical checks, subprocess
execution and transaction/recovery ownership. The initial sweep reproduced three related local defects before repair; existing rollback controls were inspected and rerun.

## Latest review-driven boundary expansion

Staging review4183777792 and discovery review4183777800 were valid. cb6638ef fixes
exclusive/no-follow staging creation and fd-bound writes/chmod; cleanup retains changed
staging bytes/mode/device/inode or symlinks with recovery metadata. Invalid unrelated
UTF-8 discovery entries warn per file and scanning continues, including later duplicate
detection. Ten malformed project-text public invocations produce structured invalid2
without writes. The old transaction fails five ownership controls;125/no skips and
actual installed runtime/Ubuntu probes pass. Source push37308178339/PR37308184377 and
consumer e852af83 push37308357249/PR37308363528/metadata37308360632 succeeded.

The five-minute review timer then returned source4183853772 at bfee51c and
consumer4183885108 at0ec3e90. Both still reproduced on cb6638ef:

| Boundary | Reproduced failure | Latest repair/control |
| --- | --- | --- |
| Fresh adoption vs index | A deleted but indexed shared file is missed by worktree collision checks; setup writes then check rejects | Inspect the cached index before fresh ignored adoption;20 preview/apply cases cover3 canonical skills, an extra reference and a namespace-root file, staged or committed/deleted; files/provenance/raw index must remain unchanged |
| Diagnostic output | JSON-escaped lone-surrogate URL reaches a raw finding; default output crashes while encoding it | Central text output escapes characters unsupported by stdout encoding; malformed URL, unsafe local path and valid Unicode path use UTF8/ASCII subprocess output, preserving failure findings and files/index; JSON behavior retained |

Negative control using exact cb6638ef public runtime returns25 assertion failures
and no errors. Its fixture cleanup alone uses forced cached removal because the old
installer changes indexed working bytes; acceptance assertions/production regressions
remain unchanged. The repaired127-test suite passes at 9af59a503bc9d51f1570bb0d3c9385eaba7f528d on both runtimes.
Two early full-suite runs against dirty source assets correctly failed two canonical
pin checks; committed reruns passed without weakening those checks.

## Latest staging, discovery and adoption/output repairs — 2026-10-05

Required semantic review returned staging-symlink, invalid-discovery-text,
fresh-adoption index and plain-text output findings. Each was reproduced before
repair. The staging and discovery repair at cb6638ef6b3b43a942bb6a8b97f46f4281b8b64a
passed125/no skips on both runtimes and actual consumer e852af83ea086ae796e38ef69dc5f448a8bd04cb
fresh-clone/installed negative probes; its source/consumer Actions all succeeded.
The latest runtime is `9af59a503bc9d51f1570bb0d3c9385eaba7f528d`, with all127/no skips on managed Python3.12.14
(76.716s) and Ubuntu24.04.5/Python3.12.3 (67.470s), strict specs/check and diff hygiene.

Consumer `a0401b89702eca70a7956ce043e8b545364f78fb` pins that exact source. Its tree
a09356149c18e294768e3e94f22c334459223c69 matches own local
4b71e34134ebd26afa942db6c8f4cd0ce0d659b1, parent e852af83 preserved by guarded
non-force publication. Explicit update changes only core/setup/workflow, operations
and provenance; project policy, shared hashes and raw index remain unchanged before
caller staging. README now resolves source/setup links from the tracked manifest,
avoiding duplicated pin prose. Actual remote fresh clones on managed runtime and
Ubuntu materialize4 exact files/match20 hashes, pass check/run-local/doctor/offline
repeat, preserve project/index bytes and exercise installed negative paths: existing
force-tracking, three indexed-only nested policies, concurrent file/directory/staging
recovery, NUL/native argv/URL rejection, invalid discovery continuation,20 fresh
indexed-path preview/apply cases and default UTF8/ASCII diagnostics without traceback.

Current runtime source push37309308964/PR37309317868 and consumer
push37309447682/PR37309456606/metadata37309452510 succeed. These are exact-revision
implementation/integration results. Final current-head semantic review and archive
remain pending; older reviews do not approve this new content. The original independent
Ubuntu startup catalog/actual three-skill use remains valid at unchanged shared hashes.
No extra user workstation discovery session is required for these runtime-only repairs.
Cloud is deferred; real global installation unperformed; Ubuntu26 historical source
JSON error remains unexplained. Source required-check administration and real merge →
completed Issue observation remain pending separate authorization, not simulated.
See [wider boundary review](wider-boundary-review.md) for discriminating controls and documentation impact.

## Earlier patterns and actual results

| Boundary | Reproduced failure | Repair and discriminating evidence |
| --- | --- | --- |
| Native argv | Valid first command runs, then a NUL argument crashes verification with empty JSON stdout | Validate every argument in both configured categories before any execution; a marker-producing first command must never run when a later command is invalid |
| Native paths | Unpaired high-surrogate bundle source/destination raises UnicodeEncodeError | Shared native-text validation rejects NUL/unencodable text before filesystem use; public setup/global preview/apply keep files/index unchanged and isolated target absent |
| Markdown URLs | Malformed bracketed URL raises ValueError from urlsplit and crashes check | Catch that parser failure locally and emit links.url findings in project documentation and PR metadata; retain valid external URL behavior |
| Rollback ownership | Earlier reviewed byte/mode/directory defects treated concurrent user changes as installer-owned | Retained controls cover edited/deleted/replaced files, symlinks/ancestors, changed/replaced/nonempty created directories, exact backup metadata and raw-index preservation; ordinary restore/recovery/retry and absent global targets still pass |

Before repair, argv regression fails all4 local/integration × NUL/unencodable cases;
URL regression fails both malformed examples; expanded bundle-path regression fails
all8 unencodable-path setup/global preview/apply cases while the8 NUL cases already
pass at08346d2. Assertions were added before repair and not weakened. Tests exercise
public commands and observable outcomes, not helper implementation details.

Runtime repair `7be9f1538b96d7dd98247e7e5eadffa042350496` passes22 setup tests,
14 checks tests and all121/no skips on managed Python3.12.14 (70.305s) and
Ubuntu24.04.5/Python3.12.3 (56.668s). Strict specs/check and diff hygiene pass.
Existing valid non-UTF-8 filename round-trip regressions remain in that suite;
rejecting unencodable strings does not reject valid OS-encoded filename bytes.

Consumer `e1d59ab460c4fc8cb2196a75f3b3c8a87cf15524` pins7be9f15; reviewed tree
810ac5a501aa4e341cbdb2f6594ff0745434e2b9 matches own local23567f2906717c25e0c54ddb4f1d707df1056e26,
parentadaad276a preserved and publication guarded/non-force. Only core/checks and
provenance changed; project policy/shared skill hashes/raw index remained unchanged
before caller staging. Fresh actual remote clones on managed runtime and Ubuntu
materialize4 exact files/match20 hashes and pass installed checks, doctor and offline
repeat. Installed public negative proof covers invalid argv before any marker command,
malformed Markdown URL findings, NUL setup rejection, force-tracking/index-only nested
policy and concurrent file/directory rollback without clobbering user/index bytes.

The existing source-owned adoption script also passed a fresh project with unrelated
AGENTS policy and a project skill: exactly one v2 routing block, no duplicate on repeat,
project skill tracked/shared skills ignored, repeat raw index unchanged. Three legacy
skills supplied as isolated discovery fixtures produce warnings and remain untouched.
The README explains this existing behavior; no new routing mechanism was needed.

## Documentation and limits

These changes restore the existing invalid-configuration and structured-diagnostic
contracts. They do not change supported product behavior, install ownership, accepted
verification intent or skill contents; no new OpenSpec change is needed. Current
runtime specs and operations remain accurate, with exact evidence/handoff updated.
Final current-head independent PR review and Actions results remain separate.

This review adds representative negative controls; it cannot promise no future defect
or eliminate concurrent-process races. Recovery remains best-effort, with no locking
or atomic multi-file guarantee. Fixtures do not prove real global installation or host
wake-up support. Initial independent Ubuntu catalog/actual skill use remains at its
recorded unchanged shared hashes. Cloud is deferred; merge/completed closure/admin/
release and real global changes remain outside authorization.

## Consumer documentation pin repair

Consumer review4183725905 atadaad276a correctly identified stale README source-pin/setup
links after a runtime repin. Verified the mismatch before repair. Consumer
0ec3e90d3fe5726f4a06a8b2c897d38b82473839 changes only those two README references
to match manifest7be9f1538b96d7dd98247e7e5eadffa042350496. The original Ubuntu
session link retains its historical source identity. Tree0d1aed3ab5374d5d694bfa663be4c40511755b43
matches own locale0922723edcdcd3e633736da4add52ec123cde83 with parente1d59ab46
preserved, publication guarded/non-force. Installed check/run-local and explicit
README/manifest equality passed; current-head Actions and semantic review are
required separately. This adds documentation reassessment of executable pin/link
references to the broader review, without a second state document or new engine.

Runtime source push37306718180/PR37306726250 and consumere1d59ab46 push37306824242/
PR37306831387/metadata37306827849 succeeded. Those results retain their revisions;
new documentation heads require their own checks/review.


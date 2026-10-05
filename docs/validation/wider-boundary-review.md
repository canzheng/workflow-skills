# Wider local boundary review — 2026-10-05

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


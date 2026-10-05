# Wider local boundary review — 2026-10-05

This is a targeted primary-author review requested by the user after serial PR P2
findings. It is not independent semantic approval or a new mandatory pre-PR stage.
The resolved GitHub NUL-path finding motivated inspection of core validation,
source setup/global setup, bootstrap, staged policy, mechanical checks, subprocess
execution and transaction/recovery ownership. Three related local defects were
reproduced before repair; existing rollback controls were inspected and rerun.

## Patterns and actual results

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


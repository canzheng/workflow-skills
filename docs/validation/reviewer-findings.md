# External review findings validation

The user supplied this review on 2026-10-04. Each claim was checked against the
approved design, installed bundle, runtime/tests and native GitHub snapshots before
acceptance. This validates targeted comments; it does not establish full independent
review or final acceptance of the resulting changes.

| Comment | Validation / disposition |
| --- | --- |
| 1 Consumer CI absent | Confirmed: the reviewed bundle installed no workflows; source verify.yml requires this source's tests, Python dependencies and Node/OpenSpec. Generic consumer CI fits the bounded setup/C12/F10 responsibility, without copying those dependencies. Added owned workflow-v2-verify.yml and workflow-v2-pr-metadata.yml to the pinned bundle. The first invokes actual verification.local argv plus mechanical checks, the second reads metadata with trusted base/read-only permissions. Application prerequisites are explicit reviewed commands/customization. No repository settings writes; doctor reports enforcement/CI execution unprobed rather than absent. |
| 2 Review phase meaning | Confirmed permissive guidance: approved design5.2 allows reviewable implementation/evidence, and6.2 permits a branch fallback. This is a useful normal-path refinement, not proof the existing implementation violated that broader design. Contract/skill/GitHub guide/current spec now make Ready PR the normal canonical review surface; draft remains in progress, publication unavailable retains branch fallback, cumulative rewrite remains explicit bootstrap exception. |
| 3 Independent review boundary | Consistent with approved design6.3/10 and existing absence of a forced reviewer pipeline. Made PR-boundary wording explicit while retaining author self-verification, docs reassessment and targeted risk methods. No independent pre-PR stage added. |
| 4 Thin phase automation | Optional extension, not a required first-release gap. Native skill operations update phases preserving unrelated labels. Deferred until usage warrants it; no new bot/state engine/permissions. |
| 5 No closure bot | Already satisfied: closure is semantic, partial references are non-closing, native GitHub tools own writes and no bot infers acceptance. Retained. |
| 6 Actual consumer F14 path | Correct acceptance gap. Existing actual bundle installation/consumer commands, Ubuntu execution and source Actions do not prove fresh-host discovery or live newly-adopted consumer CI/Ready-PR/merge/completion. Added precise remaining pilot obligations; merge/protection configuration/new consumer repository creation are not authorized by a review comment. No green CI substituted for these gates. |
| 7 Stray plus | Confirmed in Issue index first table row, fixed; link-only identity meaning unchanged. |

Ownership remains bounded: unmanaged workflow collisions fail before writes; modified
owned workflows block update and survive uninstall. New public installed-workflow
integration tests execute the workflow's actual run step, prove a configured
application command runs, prove exit7 fails verification and prove environment-specific
integration commands are not launched. Metadata trust/body events retain malicious
head/metadata negative proof. Existing safety and source verification remain required.

The refinement invalidates affected installation/consumer/spec evidence from earlier
revisions. At `3386d008f809d32ebc6cf4f849b47750845c1cb6`, the full 51-test suite, public
source check and strict specs passed on both this checkout and a fresh Ubuntu clone;
Actions run 37205386850 succeeded. Final documentation-head reruns and exact handoff
are recorded in Issue15/PR16. Newly adopted consumer live CI, real fresh Cloud
and Ubuntu agent discovery, PR semantic review and authorized merge/closure remain
integration pending. The source draft PR and per-feature review labels are the
explicit cumulative bootstrap exception, never a consumer example to copy.

## Canonical Git objects in pinned setup

Independent source PR review of `c5045c1` found that local `git replace` mappings
could substitute bytes while setup recorded the original source SHA. This was
reproduced before accepting the finding: a real replacement commit changed a shared
skill, and the public setup command incorrectly returned success under the old pin.
Validation now disables replacement objects for commit resolution and asset reads.
The public regression rejects substituted worktree bytes before writes, preserves
the consumer's instructions/index and the source's replacement ref, then installs
canonical bytes and rematerializes them from a separate clone without replacements.
The current adoption spec and active delta record that identity requirement.
New exact-revision aggregate/Ubuntu/CI results belong in Issue15/PR16; the uploaded
consumer task remains bound to `f31debf981...` / `ef24d36...`, not this later repair.

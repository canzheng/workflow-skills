# Mechanical checks and enforcement

`python3 tools/workflow/workflow.py check --repo .` checks schema, configured paths,
source or installed bundle consistency, canonical skill headers and local Markdown
files/anchors. `--pr-json SNAPSHOT` validates matching repository, nonempty Assignment,
Changes, Evidence, Documentation and Remaining sections, and local links.
Plain saved snapshot: {"repository":"owner/name","body":"Markdown"}.
GitHub event snapshots use repository.full_name and pull_request body/base/head.sha.
A trusted checker reads head files through Git blobs, fetching the exact SHA if
needed; it never checks out/executes head content in the metadata job.
`--metadata-only` requires a PR snapshot and limits work to that contract.
`--specs` explicitly requires pinned OpenSpec 1.14.0 and validates actual specs;
missing tool is a failure, not a skipped pass. Historical references are outside
current local-link checking; v1-only archives are available in Git rather than
the final source tree.

`--issues-json SNAPSHOT` is an on-demand read-only inconsistency audit of native
Issue snapshots: repository + issues array with number/state/state_reason/labels.
A trusted adapter may supply delivery_evidence as an indexed reference; its truth
still requires review. Stale closed labels, missing evidence and multiple open
phases produce findings. This cannot prevent manual Issue closure.

Source CI head/push events run v2 tests and checks with read-only permissions.
Consumer setup installs a separate generic workflow that executes mechanical checks
and verification.local argv commands with --run-local; it copies neither source tests
nor Node/OpenSpec installation. Application preparation belongs in reviewed commands
or deliberate workflow customization, with conflicts preserved on managed updates.
Integration commands remain explicit environment-specific work. The default local
command checks only the bundle and cannot certify application behavior. Setup never
configures Actions permissions/rulesets/protection or marks missing enforcement passed. Body edits
and head updates rerun trusted-base pull_request_target metadata checks. No PR body
is interpolated into shell. Metadata can execute neither commands nor untrusted
head code. Changes to trusted checker/workflows themselves need ordinary review.
First adoption requires the trusted checker to exist on the base branch; a draft
rewrite PR cannot claim the new trusted-base job already runs before that adoption.

## Required checks runbook (administrative action)

In GitHub Settings → Rules → Rulesets, edit the existing main/default-branch ruleset
or create one if absent. Set enforcement Active and target the intended integration
branch. Require pull requests, resolve review conversations, block force pushes and
branch deletion, and keep bypass permissions deliberate. Configure required approvals
for the actual team: one when another eligible approver is available; zero can be
appropriate for a solo maintainer with independent semantic review. Codex COMMENTED
reviews do not count as GitHub APPROVED reviews, and an author cannot approve their
own PR. Do not silently introduce a new mandatory reviewer requirement.

Enable Require status checks to pass before merging, then Add checks. Enter the
observed GitHub Actions contexts `v2 verification` and `v2 PR contract`,
and require branches to be up to date if that is the chosen integration policy.
Verify the contexts on the actual PR/head and select their GitHub Actions provider.
For initial source adoption, the trusted-base metadata workflow may not exist on
main yet. Require the available verification check first; add `v2 PR contract` only
after reviewed base adoption and an actual subsequent PR emits it. Requiring an
absent check can block the bootstrap PR indefinitely. This does not authorize merge.

At the 2026-10-05 tracked-model pilot, workflow-skills-test emits both contexts;
workflow-skills emits only `v2 verification`. Source Protect-main (24457981) is Active
on main with deletion/non-fast-forward rules only. The consumer initially hit a
private-repository plan restriction; the user changed it to public. Consumer
Protect-main (24484016) is now Active on main, requiring both contexts from GitHub
Actions app15368, with no bypass actors. Strict/up-to-date is false. No PR-only,
conversation, deletion or force-push rule is currently configured on the consumer.

Actual consumer PR8 at6b9eb5d changed from clean to blocked when a temporary missing
Documentation section failed metadata run37269275157 (exit1), then back to clean after
exact body restoration and successful run37269365402. No merge was attempted, HEAD
and main stayed unchanged. This proves the configured check gate, not other absent
rules. Current required-check configuration is observed separately from complete
workflow acceptance, initial host discovery and final merge/Issue completion.

Only an authorized administrator changes these settings. After saving, read back
rulesets/branch protection with native settings or
`gh api repos/OWNER/REPO/rulesets` and
`gh api repos/OWNER/REPO/branches/BRANCH/protection`. Observe an invalid PR blocked and
a corrected PR eligible without merging. Record revision, exact contexts, conditions,
review/bypass policy and observation. A workflow file or green check does not prove
required-check enforcement. Current changes do not configure protection themselves.

Review semantic docs truth, omitted behavior, acceptance scope, skipped/stale evidence,
archive ownership and meaningful negative tests. A no-impact statement is allowed;
mechanical structure cannot prove it true. Required independent review, if any,
is reported by actual authorship. Artifact retention is 14 days; preserve durable
result summaries/revision in PRs/Issues. Missing write/admin access remains pending.

Declared verification has an actual consumer: `check --run-local` and
`check --run-integration` run reviewed config argv arrays with shell disabled and
report each launch/exit. Plain check does not claim those tests ran. Empty integration
arrays report no declared proof; required environment gates still apply. Metadata-only
rejects execution flags, preserving its data-only boundary. Captured command output
is not dumped into diagnostics; inspect the declared command directly for failures.

Source bundle schema checks use the installer's v2 version format (2.minor.patch);
a string with an invalid version cannot certify an installable source bundle.

Issue audit entries must be objects. Provided labels must be arrays of nonempty
strings or objects with nonempty name strings; provided state must be `open` or
`closed`, case-insensitive. Omitted state retains the open-snapshot default.
Optional `state_reason` accepts null or native `completed`, `not_planned`, `duplicate`, `reopened`
strings, case-insensitive. Unknown/non-string reasons are invalid; uppercase
`COMPLETED` receives the same missing-delivery-evidence finding as lowercase.
An evidence annotation still requires manual acceptance/merge inspection.
Malformed entries return exit2/ok:false/invalid JSON diagnostics without traceback
or snapshot/index changes. String labels and native GitHub label objects remain
supported; structural validity does not prove delivery acceptance.

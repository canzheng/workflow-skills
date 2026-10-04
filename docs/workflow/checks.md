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
missing tool is a failure, not a skipped pass. Historical docs/archives are outside
current local-link checking; they are labeled evidence, not executable guidance.

`--issues-json SNAPSHOT` is an on-demand read-only inconsistency audit of native
Issue snapshots: repository + issues array with number/state/state_reason/labels.
A trusted adapter may supply delivery_evidence as an indexed reference; its truth
still requires review. Stale closed labels, missing evidence and multiple open
phases produce findings. This cannot prevent manual Issue closure.

CI head/push events run v2 tests and checks with read-only permissions. Body edits
and head updates rerun trusted-base pull_request_target metadata checks. No PR body
is interpolated into shell. Metadata can execute neither commands nor untrusted
head code. Changes to trusted checker/workflows themselves need ordinary review.
First adoption requires the trusted checker to exist on the base branch; a draft
rewrite PR cannot claim the new trusted-base job already runs before that adoption.

## Required checks runbook (administrative action)
After Actions produces observed check contexts, an authorized administrator should
configure the intended default/integration branch ruleset to require `v2 verification`
and `v2 PR contract`, with the repository's review requirements and bypass policy.
This rewrite does not authorize changing protections. Read back rulesets/branch
protection with native GitHub settings or `gh api repos/OWNER/REPO/rulesets` and
`gh api repos/OWNER/REPO/branches/BRANCH/protection`; observe an invalid PR being
blocked and an allowed corrected PR eligible without merging. Record revision,
contexts and observation. A workflow file alone proves no merge enforcement.

Review semantic docs truth, omitted behavior, acceptance scope, skipped/stale evidence,
archive ownership and meaningful negative tests. A no-impact statement is allowed;
mechanical structure cannot prove it true. Required independent review, if any,
is reported by actual authorship. Artifact retention is 14 days; preserve durable
result summaries/revision in PRs/Issues. Missing write/admin access remains pending.

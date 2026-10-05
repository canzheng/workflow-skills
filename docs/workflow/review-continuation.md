# Optional host review continuation — design

This is a proposed host integration, requested on 2026-10-05, not an installed
workflow capability or a new acceptance gate. GitHub remains the review authority;
the host supplies wake-ups and the existing delivery skill supplies execution.
There is no additional workflow engine, backlog database or mandatory monitor.

## Trigger and target

Attach one optional monitor to the existing Codex chat and its authorized checkout.
Scope it to explicit repository/PR pairs. For the rewrite those are
`canzheng/workflow-skills#16` and `canzheng/workflow-skills-test#8`, with their
existing branches. Do not dispatch a second implementing agent or infer permission
to change another checkout. Preserve existing user edits and host policies.

Use a supported GitHub event subscription when the host can deliver it to this
chat. Review submissions alone are insufficient: Codex can finish through a PR
comment or a reaction on the review-request comment. Fetch the canonical PR and
review records after each wake-up. An event is a hint, not acceptance evidence.
Where event delivery is unavailable, a supported host monitor can poll. Report its
actual interval; the notification scheduler exposed in this chat permits at most
hourly condition checks and does not expose a Codex chat wake-up operation.

The monitor must keep the same chat/checkout available or support an explicit
handoff with the repository, branch, exact commit and existing Issue/PR checkpoint.
An alert to the user alone is notification, not automatic execution continuation.
Do not claim setup until a real wake-up resumes the authorized checkout.

## Completion and duplicate handling

Read the current PR head and the latest applicable review request. Accept completion
only with attributable reviewer evidence: a submitted review, a no-major-issues
comment identifying the reviewed commit, or the configured bot's completion reaction
on that exact request. Resolve shortened commit identities against actual repository
commits. An eyes reaction, an unknown-error comment, a resolved old thread, CI success
or a review of an older head is not current-head semantic approval.

Use the host's existing automation cursor/checkpoint to suppress duplicate events
and unchanged polls. Record completed work in the existing PR/Issue evidence;
do not create another repository task ledger. Allow only one executing continuation
for this chat. Re-read branch/review state after acquiring the host's execution slot.
If another task owns the branch or the expected revision changed unexpectedly,
report the conflict rather than resetting or overwriting it.

## Resumed action

1. Re-read applicable host/repository instructions, the delivery contract, current
   Issue/PR evidence, checkout status and exact revisions.
2. Independently reproduce new findings before accepting them. Fix valid findings,
   add discriminating tests, reassess docs/specs and run affected verification.
3. Commit/push within existing authorization. Repin the consumer and repeat affected
   consumer/environment/Actions checks when installed assets change. Request review
   on the repaired Ready PR head. Leave pending evidence explicit.
4. When all required premerge acceptance/reviews pass, archive the completed OpenSpec
   change on the delivering branch and verify/review the final archive diff.
5. Notify the user when merge approval or another action beyond authorization is
   required. Never merge, close an Issue as completed, publish, change protections,
   delete remote branches or alter real global skills/configuration automatically.

Stay quiet for unchanged/pending review state. Notify only about material progress,
completion, a failure or a required user action. Stop or pause the monitor at its
authorized completion boundary rather than repeatedly notifying about the same gate.

## Host acceptance

Before calling this integration operational, demonstrate one real completed review
waking this chat (or its explicit handoff), with the correct checkout and GitHub
access. Verify pending/old-head/duplicate event controls and the one-execution rule.
Show an authorized continuation and a stop at the merge boundary. A configured
schedule, workflow YAML or successful notification alone does not prove that path.

Current limitation: this chat exposes GitHub reads and a notification scheduler,
but no callable Codex automation/wake-up tool or GitHub event-subscription tool.
No review monitor has been enabled by this design. Notification-only monitoring
can be configured separately; it cannot promise automatic coding continuation.

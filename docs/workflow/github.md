# GitHub delivery records

Issues own scope/dependencies/shared status. An open workflow Issue has exactly one
phase: wf:backlog, wf:ready, wf:in-progress or wf:review. wf:blocked adds a reason,
missing input and next action to the current phase; wf:deferred requires backlog.
Ready requires authorized scope, usable acceptance and available dependencies.
Cancelled closes as not planned; completed closes only after the delivery contract.
Closure removes workflow labels when permitted, preserving unrelated labels.
Reopen restores a justified open phase and invalidates assumed completion.

Normally wf:review means the canonical linked PR is Ready for Review, following
implementation/self-verification; a draft PR remains wf:in-progress. Independent
semantic/code review and subsequent fixes use that PR. Conversion back to draft
restores in-progress. Update labels with native tools and re-read actual PR state;
labels do not assert review passed. A reviewable branch is a fallback when publication
is unavailable. The cumulative WF2 bootstrap is an explicitly documented exception.
PR-to-Issue phase automation is deferred; no extra issue-stage reviewer is required.

Parent acceptance remains open across partial PRs/children. Use Refs #N for partial
work; final closing keywords require aggregate acceptance at merge to the intended
branch. A phase label/comment is not an atomic execution lock. Record branch/session
ownership and re-read; conflicting execution stops only that item.

Before creating, search both open and closed Issues and inspect exact body marker
`<!-- workflow-source: WF2-Fxx -->`, paginating complete results. Zero matches allows
creation; one reuses even a closed item (inspect disposition before reopening);
multiple matches block creation. Timeout means unknown, not failed: re-read before
retry. Native tools or authenticated gh perform writes; no separate client database.
Re-read immediately before an update, compare the body snapshot, replace only an
explicit managed block and preserve human prose/labels. If changed, reconcile first.
Read/compare/update reduces conflicts but cannot guarantee atomic remote updates.

```sh
python3 tools/workflow/records.py --catalog docs/v2/v2-feature-list.md > /tmp/wf2-issues.json
```

This reproducible temporary output is not a backlog or sync source. Published Issue
links belong in a link-only index. Live status never goes back into approved catalogs.
No Project fields or closure bot is required. Audit can flag suspicious completed
claims but cannot enforce manual closure or prove that an evidence statement is true.

## Design batch traceability
Use stable logical design/outcome source IDs across reruns, not title/content hashes.
Generated Issue bodies carry workflow-requires as a JSON array of direct confirmed
Issue URLs (or []), alongside readable dependency reasons. See
[contract](contract.md#backlog-batches-and-dependencies). Temporary candidates may
use logical IDs until creation is confirmed; resolve URLs before making work Ready.
A missing link, cycle, unresolved decision or contradictory human acceptance blocks
only affected readiness. Available prerequisites require actual content/evidence.
One approved batch can have independent Ready groups and dependent backlog/blocked
work. Candidate publication/approval does not dispatch implementation. PR references
provide design→Issue→PR navigation without a second editable backlog or sync engine.

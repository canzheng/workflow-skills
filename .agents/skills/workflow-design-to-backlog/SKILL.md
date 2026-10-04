---
name: workflow-design-to-backlog
description: Shape a high-level design or refine candidate GitHub Issues into bounded outcomes with acceptance and dependencies. Do not use for an already-ready small implementation request.
---

Read [the delivery contract](../../../docs/workflow/contract.md). It owns workflow
rules; this skill supplies shaping decisions, not execution authorization.

Resolve user objective, repository instructions, current implementation/specs,
approved versus proposed design, first-release boundary and authorization extent.
Inspect actual code before claiming a capability exists. Save agreed intent in
an existing project design document; essential decisions cannot remain chat-only.

Identify observable independently verifiable outcomes, preferably usable vertical
slices. Explain real enabling dependencies. Draft candidate Issues with outcome,
in/out scope, concrete success/failure acceptance, design/spec links, dependencies,
risks, required environments and expected documentation impact. Link to durable
design rather than copying it. Do not create Issues for internal coding steps.

An unknown product decision becomes discovery or blocks only affected readiness.
Keep attractive excluded enhancements excluded. Candidate creation does not
approve execution. Ready requires authorized scope, usable acceptance and resolved
dependencies; a previously approved batch does not need repeated approval.
Select OpenSpec only for substantial contracts/risk/ambiguity; use one plan home.

When authorized to publish, resolve exact repository and source identity. Search
open AND closed Issues, paginate as needed: zero permits creation, one reuses,
multiple require reconciliation. Preserve human prose and unrelated labels;
re-read before a bounded managed-section update, and stop conflicting mutation.
After timeout re-read before retry. Native host tools or authenticated gh do the
operations. No write access: provide exact candidate bodies and continue shaping;
do not claim remote creation or build an outbox/synchronizer.

Return persistent design paths, bounded candidate/confirmed Issue references,
dependencies, excluded scope and exact unresolved decisions. Do not implement an
unapproved candidate or autonomously reprioritize the product.

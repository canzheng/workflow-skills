# Skill usage

For a new project, point to one or more existing design documents and say
"Create the initial backlog from this design" or "Create the MVP backlog from the
current design". workflow-design-to-backlog reads the design, repository/config,
existing code/specs and release boundary, then prepares one coherent Issue batch.
Detailed design becomes Issues without unnecessary reshaping; high-level intent gets
proportional acceptance/dependency shaping. No repeated call per capability or Issue.

Review/approve the batch once if scope is not already approved. Publication creates
candidates; approval can make specified, dependency-ready work wf:ready. Waiting or
unresolved items stay backlog/blocked; actionable authorized discovery can be Ready.
Approval does not start implementation. Request "implement the approved MVP batch"
separately when execution is wanted. Each Issue references design sections and direct
required Issue URLs using the contract's JSON-array marker; independent Ready items
can be dispatched separately. Later capabilities can remain in the design, with no
explosion into engineering-task Issues or another editable backlog document.

Rerun the same skill against an evolved design: stable logical identities reuse
open/closed Issues, new scope gets new candidates, and human edits/contradictions
are preserved for resolution. Closed matches are not silently reopened. See
[new-project scenario](../../tests/v2/scenarios/initial-backlog/README.md).

Use workflow-design-to-backlog for bounded candidate refinement;
use workflow-deliver-issue for an authorized Issue or approved bootstrap feature.
A ready small bug goes directly to delivery. Relevant material risk selects
workflow-risk-review; ordinary work needs no mandatory independent review.
Repository-local skill discovery is host-owned and must be tested separately.
Explicitly reading skill files can support a run when discovery is unavailable,
but does not prove discovery worked.

Example: receipt design yields a subtotal outcome and dependent formatting
outcome. Unknown retention is discovery; excluded cloud sync is not made Ready.
Persist agreed design in the application repository and link Issues to it.
No application documentation is stored in workflow-skills except evaluation fixtures.

For delivery, read the assignment and current behavior, then implement and verify
the bounded result. A quantity bug restoring the already documented subtotal
can use a reasoned no-impact statement. Adding shipping configuration needs updated
default/error/setup explanation and a checked example. The PR indexes actual
acceptance evidence and lists pending review/integration; a local pass is not
completed delivery. See the primary-author fixture record in
[skill evaluations](../validation/skill-evaluations.md).

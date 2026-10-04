# Skill evaluation evidence

These are primary-author, in-turn exercises using explicitly read repository skill
files. They do not count as independent review or fresh Cloud discovery. The
execution environment is the /workspace checkout, Python 3.12.14, Codex host.
No model API or mandatory orchestration is introduced.

## WF2-F05 shaping: S08/S09

Input: tests/v2/scenarios/shaping/design.md. Skill: workflow-design-to-backlog.
Observed decomposition after reading current/target intent:

| Candidate | Scope and observable acceptance | Dependency / readiness |
| --- | --- | --- |
| receipt-subtotal | Integer-cent quantity subtotal; 199*2+299=697; reject empty input, negative price or nonpositive quantity | Candidate only: shaping does not authorize execution |
| receipt-format | Format 697 as 6.97 with currency; consume actual subtotal output | Depends on receipt-subtotal; candidate only |
| retention-discovery | Obtain the retention-period decision before persistence design | Unknown decision blocks only retention |

Agreed design remains in the fixture input; candidate bodies reference it rather
than replacing it. Cloud sync/dashboard/authentication remain excluded. No remote
Issue writes occurred (integration forbids writes). Identity retry behavior is
covered separately by test_records.py. Actual fresh-host triggering remains pending.

## WF2-F06 ordinary feature and bug: S10/S11/S12/S14/S22

Read workflow-deliver-issue and delivery/prompts.md, inspected before/cart.py and
README, then authored after/cart.py, README and test_delivery.py as the actual
exercise artifacts. The original documented subtotal is 697; the broken producer
returns 498 and is distinguished by the preserved hand expectation. Quantity
repair leaves existing documentation true (reasoned no-impact). The approved
shipping option is consumed by total, default 0, rejects negative/noninteger
values and produces 747 with 50 cents. The after README documents those defaults,
errors and independently checked example; leaving before README would omit shipping.
No per-task plan, feature ledger or forced reviewer was created for the fixture.
These outputs are implemented and locally verified, not merged or delivered.
Remote publication, fresh discovery and required integration remain pending.
The evidence is primary-author; full semantic adversarial records follow in F11.

## WF2-F08 risk selection/analysis: S19/S20/S21/S30

Read workflow-risk-review and relevant methods; inspected the retained L-001/L-002
source lessons and missing-worktree regression. Actual findings/proof artifacts:

| Risk input | Primary-author finding | Proof/result |
| --- | --- | --- |
| Subtract 25 cents for 25% discount | Unit/formula mismatch; 10000 cents should become 7500 | Wrong formula produces 9975 and fails independent expectation |
| Parse currency but always format USD | L-001: emitted contract has no effective downstream consumer | broken_consumer fails EUR 6.97 proof; actual consumer passes |
| Accept 498 as quantity subtotal | Changes expected behavior rather than repairing it | Original 697 assertion still fails; weakening rejected |
| Missing/symlink setup target | L-002: cannot fall back to current checkout | Public setup negative tests fail before writes |

Risk methods apply to setup/remote/migration changes, while the clear quantity repair
needs no separate reviewer. Denied values and filesystem interruption are covered.
Auth/remote permission faults are fixture proof except the actual GitHub create 403.
No independent reviewer was invoked; fresh-host semantic triggering remains pending.

## WF2-F11 semantic adversarial and cross-module exercise

S12 omission: inspected after/cart.py with before/README.md. Finding: shipping is a
new public configuration value but default, denied values and effect are absent.
Resolved in after/README.md; observed missing docs means unfinished, not optional.
S13 contradiction: inspected delivery/contradiction.md with actual function default.
Finding: docs claim 50 while code defaults to 0. A Markdown edit alone is not a pass;
resolved current fixture docs say 0 and verified 50-cent example yields 747.
S14 no-impact: implemented repaired/cart.py separately; quantity subtotal now returns
697 under the unchanged before README, so its explanation is still accurate.
No new OpenSpec change or task plan is needed for this bounded restoration.

Cross-module pilot: receipt.py actually invokes cart.total with shipping and formats
EUR 7.47; denied quantity returns exit 1 and Invalid line items. The significant
protocol planning/validation/archive path is separately exercised by test_openspec
on disposable producer/consumer behavior. test_scenarios installs the actual pinned
three-skill bundle and invokes the installed checker; this proves consumer utility
execution, not model discovery. Primary-author methods caught the listed semantic
failures; fresh host/model triggering and independent semantic review remain pending.

Pilot overhead observed: no user confirmations for fixture structure, no mandatory
per-task plans/feature ledgers, and no forced review rounds. Shipping required one
accurate documentation update; quantity repair required a reasoned no-impact record.
No measured speedup or universal model-reliability claim is made.

Final shaping artifact completion: inspected shaping/current.py (single price only)
and produced shaping/candidates.md with full acceptance/dependencies/risk/environment/
documentation bodies, linked design and stable identities. Candidate status is
explicitly unapproved execution. This expands the initial observed table into actual
reviewable Issue-body artifacts without making a workflow backlog.

Final significant-change proof now runs actual cart producer/receipt consumer inside
the disposable OpenSpec project before archive: deliberately ignoring quantity gives
EUR 1.99; restoring multiplication gives independently expected EUR 3.98. Only after
that proof passes does the fixture mark implementation complete, archive and validate
current specs. This extends structural CLI proof with implemented behavior; CLI
validation remains insufficient by itself for semantic acceptance.

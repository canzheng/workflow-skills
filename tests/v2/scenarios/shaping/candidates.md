# Actual shaping exercise output

Immutable evaluation artifact, not a live backlog or authorization to execute.
Current implementation inspected: current.py only handles one nonnegative price.
Agreed target remains design.md. These are candidates because authorization only
covers shaping. Source markers support later reuse/refinement without duplicates.

## receipt-subtotal

<!-- workflow-source: receipt-subtotal -->
Outcome: calculate line-item integer-cent subtotal including quantity.
In scope: cents/quantity validation and subtotal. Out of scope: persistence/sync/UI.
Acceptance: [(199,2),(299,1)] -> 697; reject empty input, negative/noninteger price,
and nonpositive/noninteger quantity. Current single-item code does not satisfy it.
Design: design.md. Dependencies: none. Risk: units/formula, denied inputs; hand
expectation and consumer proof required. Environment: offline supported Python.
Docs impact: current API and verified example; no per-task plan required.

## receipt-format

<!-- workflow-source: receipt-format -->
Outcome: format the actual subtotal with currency and two decimal places.
In scope: USD/EUR and explicit unsupported-currency error. Out of scope: cloud sync.
Acceptance: subtotal 697/currency EUR -> EUR 6.97; actual upstream subtotal is consumed;
a hardcoded USD consumer fails the EUR case. Design: design.md. Depends on receipt-subtotal.
Risk: producer/consumer protocol; both positive and broken-consumer proof required.
Environment: offline Python. Docs impact: public format/protocol and error behavior.

## retention-discovery

<!-- workflow-source: retention-discovery -->
Outcome: obtain the exact retention-period/product decision before persistence design.
No persistence is approved or made Ready. Document the decision in design.md, then
shape only newly authorized scope. This unknown does not block subtotal/format shaping.
Dashboard, cloud sync and authentication remain explicitly excluded.

Refinement of an existing candidate must preserve human additions and re-read source
identity/managed sections. A conflicting human edit blocks that mutation, as exercised
in test_records/test_handoff; it does not authorize recreation or unapproved execution.

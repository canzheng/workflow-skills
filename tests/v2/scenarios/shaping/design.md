# Receipt tool design (evaluation input)

Approved first release: a CLI computes line-item subtotal in integer cents,
including quantity; a receipt formats that subtotal. Current code has only a
single-item calculator. Receipt depends on subtotal. Reject negative cents,
nonpositive quantity and empty input. No persistence is approved yet: retention
period is undecided, so retention design is a separate discovery candidate.
Cloud sync, dashboard and authentication are explicitly excluded.
Authorization: shape candidates; do not implement or mark unapproved work Ready.

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

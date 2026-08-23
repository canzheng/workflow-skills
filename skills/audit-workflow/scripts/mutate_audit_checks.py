#!/usr/bin/env python3
"""Mutation harness for the audit's own checks. Run after touching any check or its tests.

    python3 ~/.agents/skills/audit-workflow/scripts/mutate_audit_checks.py

Why this exists: `audit_workflow.py` gates every workflow operation in every consuming repo, and its
self-tests are the only thing verifying it. Five of those tests were DECORATIVE when first written
and none was findable by reading — a fixture with no dash before `Task` that neither regex matched, a
fixture with no colon after `T1` in the same shape, every fixture on line 1 so `re.M` was unpinned, a
canonical-set test that iterated the set it was testing, and two count-based assertions that broke on
an improvement rather than a regression.

Two harness bugs also cost real time and are fixed here, because both make a hollow test look proven:

- an unapplied snippet must report SKIPPED, never SURVIVED. A filtered or stale snippet proves nothing.
- a mutation that CRASHES the suite is caught, not survived. Loud is a detection.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

SCRIPT = pathlib.Path(__file__).with_name("audit_workflow.py")
TEST = str(pathlib.Path(__file__).with_name("test_audit_checks.py"))

# (label, old_snippet, new_snippet) — each reintroduces ONE defect the suite claims to pin.
MUTATIONS = [
    ("ledger: done-only guard dropped",
     '        if task.status != "done":\n            continue\n        if task.task_id not in recorded:',
     '        if task.task_id not in recorded:'),
    ("ledger: date requirement dropped from the regex",
     'completed\\s+`(?P<date>\\d{4}-\\d{2}-\\d{2})`', 'completed'),
    ("ledger: ^ anchor dropped (prose satisfies provenance)",
     '_LEDGER_LINE = re.compile(\n    r"^\\s*-\\s*Task', '_LEDGER_LINE = re.compile(\n    r"\\s*-\\s*Task'),
    ("ledger: re.M dropped (only line 1 scanned)",
     '`(?P<head>[0-9a-f]{7,40})`", re.M)', '`(?P<head>[0-9a-f]{7,40})`")'),
    ("ledger: substring instead of set membership (11 satisfies 1)",
     '        if task.task_id not in recorded:', '        if task.task_id not in "".join(recorded):'),
    ("ledger: pre-seed check removed (permanent immunity)", '        elif status != "done":', '        elif False:'),
    ("ledger: orphan-line check removed", '        if status is None:', '        if False:'),
    ("ledger: date sanity neutered", '    return _date(2000, 1, 1) <= parsed <= _date.today()', '    return True'),
    ("ledger: future dates allowed", '<= _date.today()', '<= _date(2999, 12, 31)'),
    ("ledger: grandfather marker ignored",
     '    if _grandfathered(feature_text, "Completion Audit"):\n        return []',
     '    if False:\n        return []'),
    ("inline shadow: check neutered",
     '    found = sorted({m.group(1) for m in _INLINE_TASK_HEADER.finditer(feature_text)})', '    found = []'),
    ("inline shadow: fires without a linked change",
     '    if not change_id:\n        return []', '    if False:\n        return []'),
    ("inline shadow: ### anchor dropped", 'r"^### (T\\d+):"', 'r"(T\\d+):"'),
    ("scope: hyphen removed, truncating the real recorded value",
     '(?P<scope>[A-Za-z_-]+)', '(?P<scope>[A-Za-z_]+)'),
    ("scope: capitals invisible again",
     '(?P<scope>[A-Za-z_-]+)', '(?P<scope>[a-z_-]+)'),
    ("scope: check neutered", '    unknown = sorted(seen - CANONICAL_REVIEW_SCOPES)', '    unknown = []'),
    ("scope canon: a member removed", '    "record_integrity",  # a correction to earlier notes\n', ''),
    ("scope canon: a bogus member added", '    "record_integrity",  # a correction to earlier notes\n',
     '    "record_integrity",  # a correction to earlier notes\n    "whatever",\n'),
    ("scope: grandfather marker ignored",
     '    if _grandfathered(feature_text, "Scope Audit"):\n        return []',
     '    if False:\n        return []'),
    ("verdict: check neutered", '        for value in sorted(seen - CANONICAL_REVIEW_VERDICTS)',
     '        for value in []'),
    ("verdict: canon member removed", '"approved", "changes_requested", "blocked"',
     '"approved", "changes_requested"'),
    ("verdict: grandfather marker ignored",
     '    if _grandfathered(feature_text, "Verdict Audit"):\n        return []',
     '    if False:\n        return []'),
    ("verdict: message loses the silent-gate consequence",
     'so a variant here disables that gate silently. "', '"'),
    ("disclosure: a marker unlisted, so it suppresses invisibly",
     '"Remediation Audit",\n                       "Verdict Audit")', '"Remediation Audit")'),
    # --- the two checks that had NO entries. My "23 CAUGHT, zero SURVIVED" was true and hollow:
    # the table covered only the checks I had written, and `_tasks_without_plans` - the one actually
    # catching the live defect - could be set to "never report" with a fully green suite.
    ("plans: never report",
     '        if not any((d / f"{task.task_id}.md").exists() for d in plan_dirs):', '        if False:'),
    ("plans: done-only guard dropped",
     '        if task.status != "done":\n            continue\n        if not any((d / f"{task.task_id}.md")',
     '        if not any((d / f"{task.task_id}.md")'),
    ("plans: grandfather marker ignored",
     'if not change_id or _grandfathered(feature_text, "Plan Audit"):', 'if not change_id or False:'),
    ("plans: archived-path fallback dropped (every DONE feature false-reports)",
     '    plan_dirs += [d / "implementation-plans"\n'
     '                  for d in sorted((root / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))]',
     '    plan_dirs += []'),
    ("gaps: never report", '            bad_pairs.append((pos_a, pos_b))', '            pass'),
    ("gaps: only the newest pair inspected (the original defect)",
     '    for (pos_a, verdict_a), (pos_b, verdict_b) in zip(finishes, finishes[1:]):',
     '    for (pos_a, verdict_a), (pos_b, verdict_b) in zip(finishes[:1], finishes[1:2]):'),
    ("gaps: verdict test inverted",
     '        if "changes_requested" not in (verdict_a, verdict_b):', '        if "changes_requested" in (verdict_a, verdict_b):'),
    ("gaps: window reverts to a bare substring test",
     '        if not any(scope == "remediation_code" for pos, scope in scopes if lo <= pos < hi):',
     '        if "remediation_code" not in feature_text[lo:hi]:'),
    ("gaps: verdict unbounded again (inherits the next entry's)",
     '            if pos < vpos < nxt:', '            if pos < vpos:'),
    ("gaps: missing-verdict finding removed",
     '            if verdict is None:', '            if False:'),
    ("gaps: grandfather marker ignored",
     '    if _grandfathered(feature_text, "Remediation Audit"):\n        return []',
     '    if False:\n        return []'),
    ("verdict regex: capitals invisible again",
     '(?P<verdict>[A-Za-z_-]+)', '(?P<verdict>[a-z_-]+)'),
    # --- ledger provenance: an unverified stamp is decoration ---
    ("provenance: digest never re-computed",
     '        if not actual.startswith(digest):', '        if False:'),
    ("provenance: head ancestry never checked",
     '        if probe.returncode != 0:', '        if False:'),
    ("provenance: missing plan not reported",
     '        if not plan.is_file():', '        if False and not plan.is_file():'),
    ("provenance: the bare hand-typeable shape silently ignored",
     '    for m in _LEDGER_LINE_UNVERIFIED.finditer(feature_text):', '    for m in []:'),
    ("ledger regex: provenance fields made optional again (hand-typeable)",
     '    r"\\s+plan-sha256\\s+`(?P<digest>[0-9a-f]{16,64})`\\s+head\\s+`(?P<head>[0-9a-f]{7,40})`", re.M)',
     '    r"(\\s+plan-sha256\\s+`(?P<digest>[0-9a-f]{16,64})`\\s+head\\s+`(?P<head>[0-9a-f]{7,40})`)?", re.M)'),
    ("audit error: reverts to dictating a typeable line",
     'f"`complete-task/scripts/write_completion_ledger.py --feature-id <id> --task-id "', 'f"(`- Task ` completed `<YYYY-MM-DD>``) "'),
]


def main() -> int:
    pristine = SCRIPT.read_text()
    caught = survived = skipped = 0
    survivors: list[str] = []
    for label, old, new in MUTATIONS:
        if old not in pristine:
            print(f"  SKIPPED  {label}")
            print("           *** snippet no longer matches: the code moved. RE-ANCHOR IT AND"
                  " RE-DERIVE THE SELECTOR - a skipped entry pins nothing. ***")
            skipped += 1
            continue
        SCRIPT.write_text(pristine.replace(old, new, 1))
        try:
            r = subprocess.run([sys.executable, TEST], capture_output=True, text=True)
        finally:
            SCRIPT.write_text(pristine)
        fails = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("FAIL")]
        if fails:
            print(f"  CAUGHT   {label}")
            caught += 1
        elif r.returncode != 0:
            # A crash is a detection, not a survival. Counting it as SURVIVED sends you hunting for
            # a hole that is already closed.
            print(f"  CAUGHT   {label}  (crashed loudly)")
            caught += 1
        else:
            print(f"  SURVIVED {label}  *** the named test does not pin this ***")
            survived += 1
            survivors.append(label)

    assert SCRIPT.read_text() == pristine, "FAILED TO RESTORE audit_workflow.py"
    print(f"\n{caught} CAUGHT, {survived} SURVIVED, {skipped} SKIPPED  (restored)")
    if survivors or skipped:
        print("\nOnly a full run with zero SURVIVED and zero SKIPPED proves the suite.")
        for s in survivors:
            print(f"  survivor: {s}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

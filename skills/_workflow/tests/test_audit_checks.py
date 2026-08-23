#!/usr/bin/env python3
"""Self-tests for the audit's provenance and vocabulary checks.

Dependency-free on purpose: `~/.agents` is not a git repo, has no test runner, and these checks gate
every workflow operation in every consuming repository. Run directly:

    bin/run-python.sh skills/_workflow/tests/test_audit_checks.py

Each test names the production change that would make it fail. A check that gates everything and is
itself unverified is the shape this whole round exists to remove.
"""
from __future__ import annotations

import pathlib
import sys
from collections import namedtuple
from pathlib import Path

# This file lives in `skills/_workflow/tests/` (repo-only, never installed), while its subject
# lives in the audit-workflow skill. Resolve that skill through the same helper the sibling tests
# use, so the path holds wherever the repo is cloned.
for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break
from _workflow.cli_helpers import resolve_skills_root  # noqa: E402

AUDIT_SCRIPT_DIR = resolve_skills_root(Path(__file__)) / "audit-workflow" / "scripts"
sys.path.insert(0, str(AUDIT_SCRIPT_DIR))
import audit_workflow as aw  # noqa: E402

T = namedtuple("T", "task_id status")
ROOT = Path("/repo")
FP = ROOT / "docs/planning/versions/v1/features/v1-f099-x.md"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        FAILURES.append(name)



def L(task_id, day="2026-08-04", digest="a" * 16, head="abc1234"):
    """A ledger line in the CURRENT shape. The provenance fields are required."""
    return f"- Task `{task_id}` completed `{day}` plan-sha256 `{digest}` head `{head}`\n"


def ledger(text, tasks):
    return aw._tasks_without_completion_record(text, FP, ROOT, tasks)


# --- the completion ledger -------------------------------------------------------------------
# Fails if the `task.status != "done"` guard is removed, or the recorded-set lookup is inverted.

check("a done task with no ledger line is reported",
      len(ledger("## 3. Task Completion Ledger\n", [T("1", "done")])) == 1)

check("a done task WITH its ledger line is not reported",
      ledger(L("1", "2026-08-04"), [T("1", "done")]) == [])

# Every other fixture puts the ledger on line 1, which no real feature file does - it sits under a
# heading, hundreds of lines down. Without re.M the `^` matches only at string start, so the check
# would find nothing in a real file and report false errors for every closed task.
check("a ledger line found deep in the document counts",
      ledger("# Feature: x\n\n## 0. Meta\n- Feature ID: `v1-f099`\n\n"
             "## 3. Task Completion Ledger\n" + L("1"),
             [T("1", "done")]) == [])

check("a todo task owes nothing",
      ledger("", [T("1", "todo")]) == [])

check("an in_progress task owes nothing",
      ledger("", [T("1", "in_progress")]) == [])

check("only the MISSING task is named, not every task",
      [e for e in ledger(L("1", "2026-08-04"),
                         [T("1", "done"), T("2", "done")])][0].find("task 2") > 0)

check("the grandfather marker suppresses it",
      ledger("- Completion Audit: `grandfathered` - predates the rule\n", [T("1", "done")]) == [])

# A near-miss ledger line must NOT count. Without the date group this passes on a line that
# records no date, which is the difference between provenance and a decoration.
check("a ledger line without a date does not count",
      len(ledger("- Task `1` completed\n", [T("1", "done")])) == 1)

check("a ledger line with a malformed date does not count",
      len(ledger("- Task `1` completed `2026-8-4`\n", [T("1", "done")])) == 1)

check("a ledger line for a DIFFERENT task does not satisfy this one",
      any("task 1 is done but has no completion-ledger line" in e
          for e in ledger(L("7", "2026-08-04"), [T("1", "done")])))

# Task ids are matched whole: `1` must not be satisfied by a line for task `11`.
check("task 1 is not satisfied by a line for task 11",
      any("task 1 is done but has no completion-ledger line" in e
          for e in ledger(L("11", "2026-08-04"), [T("1", "done")])))

# The ledger must be a STRUCTURED line, not a phrase. Without the `^` anchor, narrative prose that
# happens to contain the words satisfies the provenance record - a decoration standing in for a gate.
check("prose containing the phrase mid-line does NOT satisfy the ledger",
      len(ledger("  - Notes: fixed in the sweep - " + L("1").lstrip("- ").rstrip("\n")
                 + " was the trigger\n", [T("1", "done")])) == 1,
      "needs a dash immediately before `Task` mid-line, or the unanchored regex fails to match "
      "the fixture either and the case discriminates nothing")

check("the error points at the WRITER SCRIPT, not at a line to type",
      "write_completion_ledger.py" in ledger("", [T("3", "done")])[0])

check("the error does NOT dictate a typeable ledger line",
      "completed `<YYYY-MM-DD>`" not in ledger("", [T("3", "done")])[0],
      "handing the reader the exact string to forge is why the first ledger was ceremony")

check("the error still names the grandfather escape",
      "Completion Audit" in ledger("", [T("3", "done")])[0])


# --- the review-scope vocabulary -------------------------------------------------------------
def scopes(text):
    return aw._unknown_review_scopes(text, FP, ROOT)


EXPECTED_SCOPES = {  # written out independently; do NOT derive this from the module
    "ready", "task_readiness", "task_execution", "task_completion",
    "feature_finish", "remediation_code", "record_integrity",
}

check("the canonical set is exactly the documented one",
      aw.CANONICAL_REVIEW_SCOPES == EXPECTED_SCOPES,
      f"module has {sorted(aw.CANONICAL_REVIEW_SCOPES)}, expected {sorted(EXPECTED_SCOPES)}")

check("every documented scope is accepted",
      scopes("".join(f"- Review Scope: `{v}`\n" for v in EXPECTED_SCOPES)) == [])

# The value actually in the record is `remediation-evidence` (v1-f010:299). The previous version of
# this test asserted `remediation` — which was the OLD regex's truncation of that value, not anything
# a human wrote. It passed while the audit reported a string that appeared nowhere in the file.
check("the real non-canonical value is caught AND reported verbatim",
      len(scopes("- Review Scope: `remediation-evidence`\n")) == 1
      and "remediation-evidence" in scopes("- Review Scope: `remediation-evidence`\n")[0],
      "a hyphen-truncating regex reports `remediation`, a string not present in the file")

# A capitalised scope was invisible to the regex, so it was neither matched nor flagged - the same
# hole the verdict side had. Only the verdict case was tested.
check("a capitalised scope is flagged rather than invisible",
      len(scopes("- Review Scope: `Task_Completion`\n")) == 1,
      "[a-z_-]+ cannot match a capital, so the value slips past the vocabulary check entirely")

check("an all-caps scope is flagged",
      len(scopes("- Review Scope: `FEATURE_FINISH`\n")) == 1)

check("a hyphenated value is not silently split at the hyphen",
      scopes("- Review Scope: `remediation-evidence`\n")[0].count("remediation-evidence") == 1)

check("an unknown scope is named in the message",
      "made_up" in scopes("- Review Scope: `made_up`\n")[0])

check("the canonical set is listed so the author can self-correct",
      "task_completion" in scopes("- Review Scope: `made_up`\n")[0])

check("its grandfather marker works too",
      scopes("- Scope Audit: `grandfathered` - predates the rule\n- Review Scope: `made_up`\n") == [])

check("one error per distinct unknown value, not per occurrence",
      len(scopes("- Review Scope: `made_up`\n- Review Scope: `made_up`\n")) == 1)


# --- guard the guard ------------------------------------------------------------------------
# Named "covers every value the template offers" but tested the 4 values from feature_file.py's
# hardcoded fallback, not the 7 in the template — and the EXPECTED_SCOPES equality above already
# pins the set. What it was reaching for is that every scope a SKILL mandates is accepted.
for _skill_scope in ("ready", "task_readiness", "task_execution", "task_completion",
                    "feature_finish", "remediation_code", "record_integrity"):
    check(f"the scope `{_skill_scope}` mandated by a skill step is accepted",
          scopes(f"- Review Scope: `{_skill_scope}`\n") == [])


# --- review verdicts ---------------------------------------------------------------------------
def verdicts(text):
    return aw._unknown_review_verdicts(text, FP, ROOT)


EXPECTED_VERDICTS = {"approved", "changes_requested", "blocked"}   # independent of the module

check("the canonical verdict set is exactly the documented one",
      aw.CANONICAL_REVIEW_VERDICTS == EXPECTED_VERDICTS,
      f"module has {sorted(aw.CANONICAL_REVIEW_VERDICTS)}")

check("every documented verdict is accepted",
      verdicts("".join(f"- Review Verdict: `{v}`\n" for v in EXPECTED_VERDICTS)) == [])

# Both live values that exist in the record today.
check("the live `pending` verdict is caught (v1-f002)",
      len(verdicts("- Review Verdict: `pending`\n")) == 1)

check("the live `corrections_applied` verdict is caught (v1-f010)",
      len(verdicts("- Review Verdict: `corrections_applied`\n")) == 1)

# The whole reason this check exists: a near-miss on the one verdict a gate branches on.
check("a near-miss on `changes_requested` is caught, since _remediation_gap branches on it",
      len(verdicts("- Review Verdict: `changes-requested`\n")) == 1)

check("the verdict error explains the silent-gate consequence",
      "disables that gate silently" in verdicts("- Review Verdict: `oops`\n")[0])

check("the verdict check has its own grandfather marker",
      verdicts("- Verdict Audit: `grandfathered` - predates the rule\n- Review Verdict: `oops`\n") == [])

print()
if FAILURES:
    print(f"{len(FAILURES)} FAILED: {', '.join(FAILURES)}")
    sys.exit(1)
print("all audit-check self-tests passed")


# --- adversarial findings: pre-seeding, date sanity, inline-task shadowing ---------------------
# Each of these was PROVEN green on a fixture before the fix.

check("a ledger line for a task that is not done yet is reported",
      any("not `done`" in e for e in ledger(L("3", "2026-08-04"),
                                            [T("3", "todo")])),
      "pre-seeding lines for 1..N at shaping time gave permanent immunity, never reported")

check("pre-seeding stays reported after the task later closes",
      # the seeded line satisfies the missing-line check, so the ONLY signal is the status mismatch
      # at seed time; once done there is legitimately nothing to report. Assert the seed-time catch.
      len(ledger(L("1") + L("2"),
                 [T("1", "done"), T("2", "todo")])) == 1)

check("a ledger line for a task that does not exist is reported",
      any("does not exist" in e for e in ledger(L("9", "2026-08-04"),
                                                [T("1", "done")])))

check("an all-zero date is rejected",
      any("implausible date" in e for e in ledger(L("1", "0000-00-00"),
                                                  [T("1", "done")])))

check("a far-future date is rejected",
      any("implausible date" in e for e in ledger(L("1", "2999-01-01"),
                                                  [T("1", "done")])))

check("a real past date is accepted",
      ledger(L("1", "2026-08-04"), [T("1", "done")]) == [])


def inline(text, change_id="v1-f099-x"):
    return aw._inline_tasks_shadowing_openspec(text, FP, ROOT, change_id)


check("inline ### T1 headers on an OpenSpec-linked feature are reported",
      len(inline("### T1: Everything\n- Status: `shipped`\n")) == 1,
      "two lines substituted an invented ledger for the linked tasks.md, silently")

check("the inline-shadow error names every inline header found",
      "T1, T2" in inline("### T1: a\n### T2: b\n")[0])

check("a feature with no inline headers is clean",
      inline("## 2. Handoff Notes\n- Notes: nothing\n") == [])

check("with no linked change there is nothing to shadow",
      inline("### T1: Everything\n", change_id=None) == [])

check("prose mentioning T1 does not trip the inline check",
      inline("- Notes: task T1 was tricky\n") == [])

check("prose containing `T1:` mid-line does not trip the inline check",
      inline("  - Notes: the blocker was T1: the flat-file reader, now resolved\n") == [],
      "needs a COLON after T1 or the unanchored regex fails to match the fixture either")

check("every grandfather marker the audit honours is listed for disclosure",
      set(aw.GRANDFATHER_MARKERS) ==
      {"Plan Audit", "Completion Audit", "Scope Audit", "Remediation Audit", "Verdict Audit"},
      "an unlisted marker would suppress a check without appearing in the success disclosure")


# --- the checks that had NO tests and NO mutation entries --------------------------------------
# My "23 CAUGHT, zero SURVIVED" was TRUE and HOLLOW: the table covered only the checks I had written.
# `_tasks_without_plans` — the one actually catching the live f012 defect — could be set to
# "never report" with a fully green suite. An entry that does not exist pins nothing.

def plans(text, tasks, change_id="c1", tmp=None):
    return aw._tasks_without_plans(text, FP, ROOT, change_id, tasks)


def _plans_with_fixture(tmpdir, done_ids, present_ids, text=""):
    """Build a real plan directory so the check's filesystem probe is exercised, not stubbed."""
    d = tmpdir / "openspec" / "changes" / "c1" / "implementation-plans"
    d.mkdir(parents=True, exist_ok=True)
    for i in present_ids:
        (d / f"{i}.md").write_text("x")
    return aw._tasks_without_plans(text, tmpdir / "docs/f.md", tmpdir, "c1",
                                  [T(i, "done") for i in done_ids])


import tempfile  # noqa: E402
_tmp = pathlib.Path(tempfile.mkdtemp())
(_tmp / "docs").mkdir(parents=True, exist_ok=True)

check("a done task with no plan file is reported",
      len(_plans_with_fixture(_tmp / "a", ["1"], [])) == 1)

check("a done task WITH its plan file is clean",
      _plans_with_fixture(_tmp / "b", ["1"], ["1"]) == [])

check("only the task missing its plan is named",
      "task 2" in _plans_with_fixture(_tmp / "c", ["1", "2"], ["1"])[0])

check("a plan for a DIFFERENT task does not satisfy this one",
      len(_plans_with_fixture(_tmp / "d", ["1"], ["7"])) == 1)

check("task 1 is not satisfied by 11.md",
      len(_plans_with_fixture(_tmp / "e", ["1"], ["11"])) == 1)

check("the plan grandfather marker suppresses it",
      _plans_with_fixture(_tmp / "f", ["1"], [], text="- Plan Audit: `grandfathered` - predates the rule\n") == [])

# A DONE feature's change is archived to changes/archive/<date>-<change-id>/, so the check looks in
# both places. No fixture used the archived path, so dropping that fallback survived - and it would
# make every closed feature report a missing plan it actually has.
def _archived():
    root = _tmp / "h"
    d = root / "openspec" / "changes" / "archive" / "2026-01-01-c1" / "implementation-plans"
    d.mkdir(parents=True, exist_ok=True)
    (d / "1.md").write_text("x")
    (root / "docs").mkdir(parents=True, exist_ok=True)
    return aw._tasks_without_plans("", root / "docs/f.md", root, "c1", [T("1", "done")])


check("a plan at the ARCHIVED path satisfies the check",
      _archived() == [],
      "without the archive fallback every closed feature false-reports a missing plan")

check("a todo task owes no plan",
      aw._tasks_without_plans("", FP, ROOT, "c1", [T("1", "todo")]) == [])

# The fixture above cannot discriminate: with ONLY a todo task the function returns early at
# `if not any(task.status in ("done", "in_progress"))`, so dropping the done-only guard never
# reaches the loop. Mix a done task in, with its plan present, so the loop is entered and the
# only thing that can produce a finding is the guard.
def _mixed():
    d = (_tmp / "g") / "openspec" / "changes" / "c1" / "implementation-plans"
    d.mkdir(parents=True, exist_ok=True)
    (d / "1.md").write_text("x")
    return aw._tasks_without_plans("", (_tmp / "g") / "docs/f.md", _tmp / "g", "c1",
                                  [T("1", "done"), T("2", "todo")])

check("a todo task alongside a done one is not reported for a missing plan",
      _mixed() == [],
      "task 1 has its plan and task 2 is todo, so only a broken done-only guard reports")

check("with no linked change nothing is owed",
      aw._tasks_without_plans("", FP, ROOT, None, [T("1", "done")]) == [])


# --- _remediation_gaps -------------------------------------------------------------------------
def gaps(text, change_id=None):
    return aw._remediation_gaps(text, FP, ROOT, change_id)


def entry(scope, verdict=None):
    v = f"  - Review Verdict: `{verdict}`\n" if verdict else ""
    return f"- `2026-08-04`:\n  - Review Scope: `{scope}`\n{v}"


check("two finish gates, the older changes_requested, no remediation review -> reported",
      any("unreviewed" in e for e in
          gaps(entry("feature_finish", "approved") + entry("feature_finish", "changes_requested"))))

check("the same pair WITH a remediation_code review between them is clean",
      gaps(entry("feature_finish", "approved") + entry("remediation_code", "approved")
           + entry("feature_finish", "changes_requested")) == [])

# The defect that made 6 of 7 real violations invisible.
check("a violation in an OLDER pair is reported, not only the newest",
      any("unreviewed" in e for e in gaps(
          entry("feature_finish", "approved") + entry("remediation_code", "approved")
          + entry("feature_finish", "changes_requested")
          + entry("feature_finish", "changes_requested"))),
      "only finishes[0]/finishes[1] were inspected, so older pairs could never fail")

check("the count of violating pairs is reported",
      any("2 adjacent" in e for e in gaps(
          entry("feature_finish", "changes_requested") + entry("feature_finish", "changes_requested")
          + entry("feature_finish", "changes_requested"))))

# The window was a bare substring test, so prose asserting the violation satisfied the check.
check("prose mentioning remediation_code does NOT satisfy the window",
      any("unreviewed" in e for e in gaps(
          entry("feature_finish", "approved")
          + "  - Notes: no remediation_code review happened this round.\n"
          + entry("feature_finish", "changes_requested"))),
      "a substring test let a sentence asserting the violation stand in for the review")

# A verdict was read to end-of-file, so a gate with none inherited the next entry's.
check("a finish gate with no verdict in its own entry is reported",
      any("no `Review Verdict` inside its own entry" in e for e in
          gaps(entry("feature_finish") + entry("feature_finish", "approved"))))

check("a capitalised verdict is visible to the vocabulary check rather than silently skipped",
      len(verdicts("- Review Verdict: `Changes_Requested`\n")) == 1,
      "[a-z_-]+ could not match a capital, so it was invisible to BOTH regexes")

check("a single finish gate cannot form a pair",
      gaps(entry("feature_finish", "changes_requested")) == [])

check("the remediation grandfather marker suppresses it",
      gaps("- Remediation Audit: `grandfathered` - predates the rule\n"
           + entry("feature_finish", "approved")
           + entry("feature_finish", "changes_requested")) == [])


# --- _grandfathered: three measured holes -----------------------------------------------------
def gf(text, marker="Completion Audit"):
    return aw._grandfathered(text, marker)


check("a marker inside a fenced code block does NOT suppress",
      gf("## Notes\n```\n- Completion Audit: `grandfathered` - predates it\n```\n") is False,
      "quoting the rule in an example disabled the check")

check("a marker inside a ~~~ fence does not suppress either",
      gf("~~~\n- Completion Audit: `grandfathered` - predates it\n~~~\n") is False)

check("a BARE marker with no reason does not suppress",
      gf("- Completion Audit: `grandfathered`\n") is False,
      "the docstring and every error message demand a reason; none was ever parsed")

check("the backtick-wrapped form the error messages dictate DOES suppress",
      gf("- `Completion Audit: grandfathered` - predates the ledger rule") is True,
      "an author copying the instruction verbatim got no suppression and no explanation")

check("a marker with a reason suppresses",
      gf("- Completion Audit: `grandfathered` - predates the ledger rule") is True)

check("an absent marker does not suppress",
      gf("- Notes: nothing to see\n") is False)

check("the reason text is recoverable for the disclosure",
      aw._grandfather_reason("- Completion Audit: `grandfathered` - was rejected at review",
                            "Completion Audit") == "was rejected at review",
      "content cannot be judged mechanically, so the pass must show it to a human")

check("one marker does not satisfy a different marker",
      gf("- Plan Audit: `grandfathered` - predates it\n", "Completion Audit") is False)


# --- the three audit crashes, now reported ----------------------------------------------------
check("_rel never raises on a path outside the root",
      aw._rel(pathlib.Path("/elsewhere/f.md"), pathlib.Path("/repo")) == "/elsewhere/f.md",
      "relative_to raised ValueError at ~20 sites, including inside an error handler")

check("_rel still relativises a path inside the root",
      aw._rel(pathlib.Path("/repo/docs/f.md"), pathlib.Path("/repo")) == "docs/f.md")


# --- ledger provenance: the fields must be RE-VERIFIED, or they are decoration ------------------
import hashlib  # noqa: E402
import subprocess  # noqa: E402
import tempfile as _tf  # noqa: E402


def _repo_with_plan(plan_body="plan contents\n"):
    """A tiny git repo with one implementation plan, so the digest and head are real."""
    root = pathlib.Path(_tf.mkdtemp()) / "r"
    (root / "openspec/changes/c1/implementation-plans").mkdir(parents=True)
    plan = root / "openspec/changes/c1/implementation-plans/4.md"
    plan.write_text(plan_body)
    for a in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"],
              ["config", "user.name", "t"], ["add", "-A"], ["commit", "-qm", "init"]):
        subprocess.run(["git", *a], cwd=root, capture_output=True, text=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          capture_output=True, text=True).stdout.strip()[:12]
    return root, hashlib.sha256(plan.read_bytes()).hexdigest(), head


def prov(text, root, change_id="c1"):
    return aw._ledger_provenance_errors(text, root / "docs/f.md", root, change_id)


_r, _digest, _head = _repo_with_plan()

check("a correctly stamped line verifies clean",
      prov(f"- Task `4` completed `2026-08-06` plan-sha256 `{_digest[:16]}` head `{_head}`", _r) == [])

check("a WRONG plan digest is reported",
      any("digests to" in e for e in
          prov(f"- Task `4` completed `2026-08-06` plan-sha256 `{'b'*16}` head `{_head}`", _r)),
      "an unverified stamp is decoration; a guessed digest must not pass")

check("a head that is not an ancestor is reported",
      any("not an ancestor" in e for e in
          prov(f"- Task `4` completed `2026-08-06` plan-sha256 `{_digest[:16]}` head `deadbee`", _r)))

check("a line naming a nonexistent plan is reported",
      any("names a plan that does not exist" in e for e in
          prov(f"- Task `9` completed `2026-08-06` plan-sha256 `{_digest[:16]}` head `{_head}`", _r)))

# The old hand-typeable shape must be named as such, not silently ignored.
check("the bare hand-typeable shape is reported with its reason",
      any("no provenance fields" in e for e in prov("- Task `4` completed `2026-08-06`", _r)),
      "reporting it as 'no line at all' would hide WHY it does not count")

check("a bare line does NOT satisfy the completion requirement either",
      len(ledger("- Task `1` completed `2026-08-04`\n", [T("1", "done")])) == 1)

# The plan changing after the close is a real signal, not noise.
(_r / "openspec/changes/c1/implementation-plans/4.md").write_text("edited after the close\n")
check("editing the plan after the close breaks its stamp",
      any("changed after the task closed" in e for e in
          prov(f"- Task `4` completed `2026-08-06` plan-sha256 `{_digest[:16]}` head `{_head}`", _r)))

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, repo_root
from _workflow.workflow_state import (
    FEATURE_ID_RE,
    WorkflowStateError,
    WORKFLOW_SECTIONS,
    collect_openspec_change_linkage,
    compute_task_readiness_drift,
    current_task_reference_error,
    find_backlog_section_order_errors,
    find_openspec_task_structure_errors,
    find_legacy_inline_planning_sections,
    format_task_readiness_drift_messages,
    list_git_worktree_roots,
    list_git_worktrees,
    parse_backlog_document,
    validate_promoted_feature_openspec_specs,
    parse_current_task,
    parse_feature_openspec_status,
    parse_tasks,
    parse_feature_openspec_change,
)

BACKLOG_REF_RE = re.compile(r"^- Backlog Reference: `([^`]+)`$", re.MULTILINE)

# Every marker `_grandfathered` recognises, so the success disclosure can NAME an active one. A green
# that conceals disabled checks is textually identical to a clean green, and that property is what
# makes every scope-shrinking route cheap.
GRANDFATHER_MARKERS = ("Plan Audit", "Completion Audit", "Scope Audit", "Remediation Audit",
                       "Verdict Audit")

# Appended to during the walk, drained by main(). A list rather than a return value so the three
# existing `return errors, in_progress_records` sites keep their arity.
_DISCLOSURE: list[dict] = []


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", help="Override the repository root for fixture-backed workflow checks.")
    parser.add_argument(
        "--gate",
        choices=("start", "complete"),
        help=(
            "Gate-aware in_progress check. start: assert 0 in_progress tasks. "
            "complete: assert exactly 1 in_progress task; print its feature_id and task_id on success."
        ),
    )
    parser.add_argument(
        "--include-worktrees",
        action="store_true",
        help=(
            "Walk all git worktrees and aggregate the in_progress count across them. "
            "Detects cross-worktree drift where two worktrees claim different in_progress tasks."
        ),
    )
    return parser.parse_args(argv)


def _rel(path: Path, root: Path) -> str:
    """A display path that never raises.

    `relative_to` raises ValueError when a backlog link resolves OUTSIDE the root - one `../` too
    many, or a symlinked features/ directory - and it is called at ~20 sites including inside the
    handler for "BACKLOG.md is missing", so the crash replaced the error it was reporting.
    """
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


_FENCE = re.compile(r"^\s*(```|~~~)", re.M)


def _strip_fenced_blocks(text: str) -> str:
    """Blank out fenced code blocks, keeping line count so positions elsewhere stay comparable.

    A marker inside a fence SUPPRESSED its check - so quoting the rule in an example disabled it.
    """
    out, fenced = [], False
    for line in text.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


# Both forms the record and the error messages actually use. The second was NOT matched before, even
# though every error message tells the author to write exactly that: "record `Plan Audit:
# grandfathered` with a reason". An author who copied the instruction verbatim got no suppression and
# no explanation of why.
_MARKER_FORMS = (
    r"^\s*-?\s*{m}:\s*`?grandfathered`?(?P<reason>.*)$",
    r"^\s*-?\s*`{m}:\s*grandfathered`(?P<reason>.*)$",
)


def _grandfather_reason(feature_text: str, marker: str) -> str | None:
    """The marker's trailing reason, or None when the marker is absent.

    Returns "" when the marker is present with NO reason - which `_grandfathered` treats as not
    grandfathered, because the docstring and every error message demand a reason and nothing ever
    parsed one. A bare line used to disable an unbounded number of findings.
    """
    body = _strip_fenced_blocks(feature_text)
    for form in _MARKER_FORMS:
        m = re.search(form.format(m=re.escape(marker)), body, re.M)
        if m:
            return m.group("reason").strip(" -:\u2014\t")
    return None


def _grandfathered(feature_text: str, marker: str) -> bool:
    """An explicit, reasoned opt-out for work that predates a rule.

    Deliberately not a date cutoff: a marker has to be WRITTEN, with a reason, by someone who looked.
    A silent retroactive pass would let the rule appear to hold over history it never governed.

    Three measured holes, now closed: it fired from inside a fenced code block; it did NOT fire on
    the backtick-wrapped form the error messages instruct the author to write; and the "reason" the
    docstring demanded was never parsed, so a bare line disabled an unbounded number of findings.

    What it still CANNOT do is judge the reason's content - `grandfathered - was rejected at review`
    reads as a suppression. That is why every active marker and its reason text are printed in the
    success disclosure: a human reading the pass can see what was waived and why.
    """
    reason = _grandfather_reason(feature_text, marker)
    return bool(reason)


_REVIEW_SCOPE = re.compile(r"^\s*-?\s*Review Scope:\s*`?(?P<scope>[A-Za-z_-]+)`?", re.M)
_REVIEW_VERDICT = re.compile(r"^\s*-?\s*Review Verdict:\s*`?(?P<verdict>[A-Za-z_-]+)`?", re.M)

# Scopes were given a canonical set and a check; verdicts were not - yet `_remediation_gaps` branches
# on the exact spelling of `changes_requested`, so a typo there SILENTLY disables the unreviewed-
# remediation gate. That is the same defect class in the field with the worse consequence. Two
# independent reviews flagged it; live non-canonical values already exist (`pending` at v1-f002,
# `corrections_applied` at v1-f010).
CANONICAL_REVIEW_VERDICTS = frozenset({"approved", "changes_requested", "blocked"})


def _remediation_gaps(feature_text: str, feature_path: Path, root: Path,
                      change_id: str | None) -> list[str]:
    """Every adjacent pair of `feature_finish` gates, not just the newest one.

    Three defects, all measured against the real `v1-f010` with its marker neutralised:

    - **Only the newest pair was inspected.** That feature has 8 `feature_finish` gates, 7 of them
      `changes_requested`, and exactly 1 `remediation_code` review - 6 adjacent pairs violate the
      documented rule, and the single pair the check looked at was the one that complied. It returned
      clean. The docstring's own rationale is about that history and could not see it.
    - **The "newest-first" ordering was undocumented and already violated.** No template, no
      WORKFLOW_REFERENCE copy, and no SKILL.md states it; `v1-f005` is neither newest-first nor
      oldest-first, and section 1 is oldest-first while section 2 is newest-first in the same file
      that `finditer` scans as one string. So the check is now ORDER-AGNOSTIC: any two consecutive
      gates where EITHER carries `changes_requested` require a remediation review between them.
      Conservative on purpose - over-reporting is the safe direction for a gate.
    - **The window test was a bare substring.** `"remediation_code" not in window` meant a Notes line
      reading "no remediation_code review happened this round" satisfied the check against itself.
      It now requires an actual `Review Scope: remediation_code` line inside the window.

    A verdict is also bound to its OWN entry now: `verdict_after` scanned to end-of-file, so a gate
    with a missing or unparseable verdict silently inherited the next entry's `approved`.
    """
    if _grandfathered(feature_text, "Remediation Audit"):
        return []
    scopes = [(m.start(), m.group("scope")) for m in _REVIEW_SCOPE.finditer(feature_text)]
    if not scopes:
        return []
    verdicts = [(m.start(), m.group("verdict")) for m in _REVIEW_VERDICT.finditer(feature_text)]
    scope_starts = [pos for pos, _ in scopes]

    def verdict_for(pos: int) -> str | None:
        """The verdict inside THIS entry only - bounded by the next `Review Scope` line."""
        nxt = min((p for p in scope_starts if p > pos), default=len(feature_text))
        for vpos, verdict in verdicts:
            if pos < vpos < nxt:
                return verdict
        return None

    finishes = [(pos, verdict_for(pos)) for pos, scope in scopes if scope == "feature_finish"]
    rel = _rel(feature_path, root)
    out: list[str] = []
    bad_pairs: list[tuple[int, int]] = []
    for (pos_a, verdict_a), (pos_b, verdict_b) in zip(finishes, finishes[1:]):
        lo, hi = sorted((pos_a, pos_b))
        for pos, verdict in ((pos_a, verdict_a), (pos_b, verdict_b)):
            if verdict is None:
                out.append(
                    f"{rel} has a `feature_finish` gate with no `Review Verdict` inside its own "
                    f"entry - a missing or non-canonical verdict silently inherits the next entry's, "
                    f"and `changes_requested` is what triggers the remediation gate")
        if "changes_requested" not in (verdict_a, verdict_b):
            continue
        if not any(scope == "remediation_code" for pos, scope in scopes if lo <= pos < hi):
            bad_pairs.append((pos_a, pos_b))
        if change_id:
            rem_dir = root / "openspec" / "changes" / change_id / "remediation"
            if not rem_dir.exists() or not any(rem_dir.glob("gate-*.md")):
                out.append(
                    f"{rel} remediation round has no catalogue at "
                    f"openspec/changes/{change_id}/remediation/gate-<n>.md")
    if bad_pairs:
        out.insert(0,
            f"{rel} has {len(bad_pairs)} adjacent `feature_finish` gate pair(s) where one is "
            f"`changes_requested` and no `Review Scope: remediation_code` verdict appears between "
            f"them - that many remediation rounds went unreviewed (WORKFLOW_REFERENCE: REMEDIATION "
            f"ROUND). Only the NEWEST pair used to be inspected, so this count was reported as 0.")
    seen: set[str] = set()
    return [m for m in out if not (m in seen or seen.add(m))]


# The provenance fields are REQUIRED. Without them the line was hand-typeable, so a gated close and
# a forged one were byte-identical - and this error message dictated the exact string to type.
# `complete-task/scripts/write_completion_ledger.py` is the only writer; the digest and head are
# RE-VERIFIED below, so a guessed value is an error rather than a pass.
_LEDGER_LINE = re.compile(
    r"^\s*-\s*Task\s+`(?P<task_id>\d+)`\s+completed\s+`(?P<date>\d{4}-\d{2}-\d{2})`"
    r"\s+plan-sha256\s+`(?P<digest>[0-9a-f]{16,64})`\s+head\s+`(?P<head>[0-9a-f]{7,40})`", re.M)

# A line carrying only task + date: the old hand-typeable shape. Matched separately so the error can
# say WHY it does not count, instead of reporting the task as having no line at all.
_LEDGER_LINE_UNVERIFIED = re.compile(
    r"^\s*-\s*Task\s+`(?P<task_id>\d+)`\s+completed\s+`(?P<date>\d{4}-\d{2}-\d{2})`\s*$", re.M)

# The template and WORKFLOW_REFERENCE disagreed on this set, which is how `remediation` (a truncation
# of `remediation_code`) entered the record unchallenged. One authority now, and it is this constant.
CANONICAL_REVIEW_SCOPES = frozenset({
    "ready",             # ready-feature 9, feature-level readiness
    "task_readiness",    # start-task 7.1, per-task contract review
    "task_execution",    # start-task 8, pre-execution semantic review
    "task_completion",   # complete-task 6.5
    "feature_finish",    # finish-feature 3.5
    "remediation_code",  # a remediation round's own diff review
    "record_integrity",  # a correction to earlier notes
})

_INLINE_TASK_HEADER = re.compile(r"^### (T\d+):", re.M)


def _unknown_review_verdicts(feature_text: str, feature_path: Path, root: Path) -> list[str]:
    """A misspelled verdict silently disables the remediation gate, which needs `changes_requested`."""
    if _grandfathered(feature_text, "Verdict Audit"):
        return []
    seen = {m.group("verdict") for m in _REVIEW_VERDICT.finditer(feature_text)}
    return [
        f"{_rel(feature_path, root)} records unknown `Review Verdict: {value}` - canonical "
        f"values are {', '.join(sorted(CANONICAL_REVIEW_VERDICTS))}. `_remediation_gaps` branches on "
        f"the exact spelling of `changes_requested`, so a variant here disables that gate silently. "
        f"If this predates the rule, record `Verdict Audit: grandfathered` with a reason."
        for value in sorted(seen - CANONICAL_REVIEW_VERDICTS)
    ]


def _inline_tasks_shadowing_openspec(feature_text: str, feature_path: Path, root: Path,
                                     change_id: str | None) -> list[str]:
    """Inline `### T1:` headers REPLACE the linked tasks.md rather than supplementing it.

    `workflow_state.parse_tasks` returns feature-file tasks first and consults the linked change only
    when it finds none, so two lines substitute an invented ledger for the real one - and every
    task-derived check then reads the substitute. The inline `- Status:` value is taken verbatim with
    no vocabulary check, so `shipped` passes. `find_legacy_inline_planning_sections` does not reach
    this: it matches `##` section names, not `###` task headers.
    """
    if not change_id:
        return []
    found = sorted({m.group(1) for m in _INLINE_TASK_HEADER.finditer(feature_text)})
    if not found:
        return []
    return [
        f"{_rel(feature_path, root)} declares inline task headers {', '.join(found)} while "
        f"linked to OpenSpec change `{change_id}` - inline tasks SHADOW the linked tasks.md instead "
        f"of supplementing it, so every task-derived check would read the inline list. Remove them; "
        f"the linked change is the task authority."
    ]


def _plausible_ledger_date(value: str) -> bool:
    """A real calendar date, not in the future. `0000-00-00` and `9999-99-99` both matched the regex."""
    from datetime import date as _date
    try:
        parsed = _date.fromisoformat(value)
    except ValueError:
        return False
    return _date(2000, 1, 1) <= parsed <= _date.today()


def _ledger_provenance_errors(feature_text: str, feature_path: Path, root: Path,
                              change_id: str | None) -> list[str]:
    """Re-verify each ledger line's stamped fields. An unverified stamp is decoration.

    The digest must equal the CURRENT sha256 of the named plan, and the head must be a real commit
    reachable from the branch head. Neither can be produced by typing prose, and a wrong value is
    reported rather than accepted - which is the whole difference between this and the first version.
    """
    rel = _rel(feature_path, root)
    out: list[str] = []
    for m in _LEDGER_LINE_UNVERIFIED.finditer(feature_text):
        out.append(
            f"{rel} completion-ledger line for task {m.group('task_id')} carries no provenance "
            f"fields (`plan-sha256`, `head`). That shape is hand-typeable and cannot distinguish a "
            f"gated close from a forged one. Write it with "
            f"`complete-task/scripts/write_completion_ledger.py`.")
    if change_id is None:
        return out
    for m in _LEDGER_LINE.finditer(feature_text):
        task_id, digest, head = m.group("task_id"), m.group("digest"), m.group("head")
        plan = root / "openspec" / "changes" / change_id / "implementation-plans" / f"{task_id}.md"
        if not plan.is_file():
            out.append(f"{rel} ledger line for task {task_id} names a plan that does not exist: "
                       f"implementation-plans/{task_id}.md")
            continue
        actual = hashlib.sha256(plan.read_bytes()).hexdigest()
        if not actual.startswith(digest):
            out.append(
                f"{rel} ledger line for task {task_id} has plan-sha256 `{digest}` but the plan now "
                f"digests to `{actual[:16]}` - the plan changed after the task closed, or the stamp "
                f"was not produced from it")
        probe = subprocess.run(["git", "merge-base", "--is-ancestor", head, "HEAD"],
                               cwd=root, capture_output=True, text=True)
        if probe.returncode != 0:
            out.append(
                f"{rel} ledger line for task {task_id} stamps head `{head}`, which is not an "
                f"ancestor of the current branch head (git: "
                f"{probe.stderr.strip()[:60] or 'not reachable'})")
    return out


def _tasks_without_completion_record(feature_text: str, feature_path: Path, root: Path,
                                     tasks) -> list[str]:
    """Every done task must carry a completion-ledger line, because `done` is otherwise a CHARACTER.

    `workflow_state` derives `status="done"` from the `[x]` in `tasks.md`, so typing one letter IS
    the state transition and needs no tool. `complete-task` has real gates - its resolver refuses a
    missing implementation plan and refuses a task whose status is not `in_progress` - but a gate
    only bites if it is called.

    Worse, the bypass is SELF-CONCEALING: skipping `start-task` leaves `Current Task` unset, so no
    task is `in_progress`, so `complete-task` cannot be invoked at all (it raises "repository has no
    task with status `in_progress`"). The missing gate therefore erases the evidence that it was
    owed, and afterwards a hand-checked box and a fully gated one are textually identical.

    This is the only UNCONDITIONAL provenance record in the workflow. Note what cannot serve instead:

    - a `task_completion` review verdict is conditional (`complete-task` 6.5: "if the task crossed a
      review gate"), so its absence proves nothing. Measured: 63% of done tasks lack one, and almost
      none of those are violations.
    - an implementation plan is NECESSARY but not SUFFICIENT. Absence implies the gates were skipped;
      presence implies nothing about whether they ran. Two tasks on one feature had plans and no
      review at all.

    Scoped to OPEN features for the same reason `_tasks_without_plans` is: a closed feature's
    provenance is settled and unrecoverable, and reporting it forces grandfather markers that work
    around the scoping rather than around any real exemption.
    """
    if _grandfathered(feature_text, "Completion Audit"):
        return []
    recorded = {m.group("task_id"): m.group("date") for m in _LEDGER_LINE.finditer(feature_text)}
    known = {task.task_id: task.status for task in tasks}
    out = []
    # A line for a task that is NOT done defeats the check BEFORE the violation exists: seed lines
    # for 1..N at shaping time and every later close is pre-approved, with nothing ever reported.
    # That reads as diligence, so it never produces the friction the gate exists to create.
    for task_id, date in sorted(recorded.items()):
        status = known.get(task_id)
        if status is None:
            out.append(
                f"{_rel(feature_path, root)} has a completion-ledger line for task {task_id}, "
                f"which does not exist in the linked tasks.md")
        elif status != "done":
            out.append(
                f"{_rel(feature_path, root)} has a completion-ledger line for task {task_id} "
                f"but its status is `{status}`, not `done` - a line written before the task closes "
                f"pre-approves a close that has not happened")
        if not _plausible_ledger_date(date):
            out.append(
                f"{_rel(feature_path, root)} completion-ledger line for task {task_id} has an "
                f"implausible date `{date}`")
    for task in tasks:
        if task.status != "done":
            continue
        if task.task_id not in recorded:
            out.append(
                f"{_rel(feature_path, root)} task {task.task_id} is done but has no "
                f"completion-ledger line - `done` was reached without passing through "
                f"`complete-task`, or the line was not written. Write it by RUNNING "
                f"`complete-task/scripts/write_completion_ledger.py --feature-id <id> --task-id "
                f"{task.task_id}`; the line carries a plan digest and a commit that this audit "
                f"re-verifies, so it cannot be typed by hand. If this task predates the requirement, "
                f"record `Completion Audit: grandfathered` with a reason in its handoff notes."
            )
    return out


def _unknown_review_scopes(feature_text: str, feature_path: Path, root: Path) -> list[str]:
    """A `Review Scope` outside the canonical set is unconsumable by any downstream check."""
    if _grandfathered(feature_text, "Scope Audit"):
        return []
    seen = {m.group("scope") for m in _REVIEW_SCOPE.finditer(feature_text)}
    unknown = sorted(seen - CANONICAL_REVIEW_SCOPES)
    # The template's own placeholder line lists the alternatives inside angle brackets; the regex
    # cannot match those, so nothing here needs to exempt them.
    return [
        f"{_rel(feature_path, root)} records unknown `Review Scope: {value}` - "
        f"canonical values are {', '.join(sorted(CANONICAL_REVIEW_SCOPES))}"
        for value in unknown
    ]


def _tasks_without_plans(feature_text: str, feature_path: Path, root: Path, change_id: str | None,
                         tasks) -> list[str]:
    """Every done task must have an implementation plan.

    All of `start-task`'s deterministic gates key on that file, so a task executed without one
    silently receives none of them. On one feature, task 6 had no plan, never had one, and carried
    the longest defect tail of any task.
    """
    if not change_id or _grandfathered(feature_text, "Plan Audit"):
        return []
    # A change that has been archived keeps its implementation-plans, at the archived path. Look in
    # both, or every DONE feature reports a false violation.
    plan_dirs = [root / "openspec" / "changes" / change_id / "implementation-plans"]
    plan_dirs += [d / "implementation-plans"
                  for d in sorted((root / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))]
    # A plan is due only once a task has actually been executed. A feature still in [SHAPING] or
    # [READY] has no done or in_progress tasks and therefore owes no plans yet.
    if not any(task.status in ("done", "in_progress") for task in tasks):
        return []
    if not any(d.exists() for d in plan_dirs):
        # No plan directory anywhere: the feature predates the plan requirement. Report once, as a
        # single finding, rather than one per task.
        return [
            f"{_rel(feature_path, root)} has no implementation-plans directory for "
            f"{change_id}; every executable task needs a plan (WORKFLOW_REFERENCE). If this "
            f"feature predates the requirement, record `Plan Audit: grandfathered` with a reason "
            f"in its handoff notes."
        ]
    out = []
    for task in tasks:
        if task.status != "done":
            continue
        if not any((d / f"{task.task_id}.md").exists() for d in plan_dirs):
            out.append(
                f"{_rel(feature_path, root)} task {task.task_id} is done but has no "
                f"implementation plan at implementation-plans/{task.task_id}.md for {change_id}"
            )
    return out


def _audit_single_root(root: Path) -> tuple[list[str], list[tuple[str, str]]]:
    """Audit one checkout. Returns (errors, in_progress_records).

    in_progress_records is a list of (feature_id, task_id) tuples for tasks
    whose status is `in_progress` in this checkout's planning state.
    """
    errors: list[str] = []
    in_progress_records: list[tuple[str, str]] = []

    current_version = root / "docs" / "planning" / "current_version"
    if not current_version.exists():
        errors.append("docs/planning/current_version is missing")
        current_path = None
    else:
        if not current_version.is_symlink():
            errors.append("docs/planning/current_version is not a symlink")
        current_path = current_version.resolve()

    if current_path is None:
        return errors, in_progress_records

    openspec_root = root / "openspec"
    if not openspec_root.exists():
        errors.append("openspec is missing")
    else:
        if not (openspec_root / "specs").is_dir():
            errors.append("openspec/specs is missing")
        if not (openspec_root / "changes").is_dir():
            errors.append("openspec/changes is missing")

    backlog = current_path / "BACKLOG.md"
    if not backlog.exists():
        errors.append(f"{_rel(backlog, root)} is missing")
        return errors, in_progress_records

    backlog_text = backlog.read_text(encoding="utf-8")
    for section_error in find_backlog_section_order_errors(backlog_text):
        errors.append(f"{_rel(backlog, root)} {section_error}")

    version = current_path.name
    parsed_backlog = parse_backlog_document(backlog_text)
    for malformed_entry in parsed_backlog.malformed_entries:
        errors.append(f"{_rel(backlog, root)} {malformed_entry}")

    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed_backlog.feature_sections.get(section_name, []):
            feature_id = entry.feature_id
            link = entry.link
            feature_path = (backlog.parent / link).resolve()
            if not feature_path.exists():
                errors.append(
                    f"{_rel(backlog, root)} section [{section_name}] links missing feature file {link}"
                )
                continue
            # Three measured crashes became reported errors here. Each was an unhandled exception
            # that aborted the WHOLE audit, so one malformed feature hid every other finding.
            if feature_path.is_dir():
                errors.append(
                    f"{_rel(backlog, root)} section [{section_name}] link {link} resolves to a "
                    f"DIRECTORY, not a feature file"
                )
                continue
            if not feature_path.is_relative_to(root):
                errors.append(
                    f"{_rel(backlog, root)} section [{section_name}] link {link} resolves OUTSIDE "
                    f"the repo root ({feature_path}); a feature file must live inside the repo"
                )
                continue
            try:
                feature_text = feature_path.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                errors.append(f"{_rel(feature_path, root)} is not valid UTF-8 ({exc.reason})")
                continue
            except OSError as exc:
                errors.append(f"{_rel(feature_path, root)} could not be read: {exc.strerror}")
                continue

            feature_id_match = FEATURE_ID_RE.search(feature_text)
            if not feature_id_match:
                errors.append(f"{_rel(feature_path, root)} is missing Feature ID metadata")
            elif feature_id_match.group(1) != feature_id:
                errors.append(
                    f"{_rel(feature_path, root)} has Feature ID {feature_id_match.group(1)}, expected {feature_id}"
                )

            backlog_ref_match = BACKLOG_REF_RE.search(feature_text)
            expected_anchor = f"docs/planning/versions/{version}/BACKLOG.md#{section_name.lower()}"
            if not backlog_ref_match:
                errors.append(f"{_rel(feature_path, root)} is missing Backlog Reference metadata")
            elif backlog_ref_match.group(1) != expected_anchor:
                errors.append(
                    f"{_rel(feature_path, root)} has Backlog Reference {backlog_ref_match.group(1)}, expected {expected_anchor}"
                )

            change_id = parse_feature_openspec_change(feature_text)
            openspec_status = parse_feature_openspec_status(feature_text)
            legacy_inline_sections = find_legacy_inline_planning_sections(feature_text)

            if legacy_inline_sections and openspec_status != "legacy-exempt":
                errors.append(
                    f"{_rel(feature_path, root)} uses legacy inline planning sections: "
                    + ", ".join(legacy_inline_sections)
                )

            for specs_error in validate_promoted_feature_openspec_specs(feature_text, section_name=section_name):
                if specs_error == "feature is missing OpenSpec Specs metadata":
                    errors.append(f"{_rel(feature_path, root)} is missing OpenSpec Specs metadata")
                else:
                    errors.append(f"{_rel(feature_path, root)} {specs_error}")

            # DEFER is NOT settled: its change stays active and its tasks stay claimed,
            # so provenance still applies. Only [DONE] is settled (change archived).
            if section_name in {"SHAPING", "READY", "IN_PROGRESS", "DEFER"}:
                if openspec_status == "legacy-exempt":
                    errors.append(
                        f"{_rel(feature_path, root)} uses OpenSpec Status `legacy-exempt` outside [DONE]"
                    )
                if change_id is None:
                    errors.append(f"{_rel(feature_path, root)} is missing OpenSpec Change metadata")
                else:
                    change_dir = root / "openspec" / "changes" / change_id
                    if not change_dir.exists():
                        errors.append(
                            f"{_rel(feature_path, root)} links missing OpenSpec change openspec/changes/{change_id}"
                        )
                    if section_name in {"SHAPING", "READY"}:
                        for required_name in ("proposal.md", "design.md", "tasks.md"):
                            if not (change_dir / required_name).exists():
                                errors.append(
                                    f"{_rel(feature_path, root)} is in [{section_name}] but linked OpenSpec change is missing {required_name}"
                                )
                    tasks_file = change_dir / "tasks.md"
                    if tasks_file.exists():
                        structure_errors = find_openspec_task_structure_errors(
                            tasks_file.read_text(encoding="utf-8")
                        )
                        for structure_error in structure_errors:
                            errors.append(f"{_rel(feature_path, root)} {structure_error}")
            elif section_name == "DONE":
                if openspec_status == "legacy-exempt":
                    if change_id is not None:
                        errors.append(
                            f"{_rel(feature_path, root)} is marked `legacy-exempt` but still records OpenSpec Change {change_id}"
                        )
                else:
                    if change_id is None:
                        errors.append(
                            f"{_rel(feature_path, root)} is in [DONE] but has neither archived OpenSpec change metadata nor OpenSpec Status `legacy-exempt`"
                        )
                    else:
                        active_change_dir = root / "openspec" / "changes" / change_id
                        archive_matches = sorted((root / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))
                        if active_change_dir.exists():
                            errors.append(
                                f"{_rel(feature_path, root)} is in [DONE] but linked OpenSpec change is still active at openspec/changes/{change_id}"
                            )
                        if len(archive_matches) != 1:
                            errors.append(
                                f"{_rel(feature_path, root)} is in [DONE] but expected exactly one archived OpenSpec change for {change_id}"
                            )
            else:
                if change_id is None:
                    errors.append(f"{_rel(feature_path, root)} is missing OpenSpec Change metadata")
                else:
                    change_dir = root / "openspec" / "changes" / change_id
                    if not change_dir.exists():
                        errors.append(
                            f"{_rel(feature_path, root)} links missing OpenSpec change openspec/changes/{change_id}"
                        )

            try:
                tasks = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
            except ValueError as exc:
                errors.append(f"{_rel(feature_path, root)} {exc}")
                continue
            # OPEN features only. A [DONE] feature's plans and reviews are settled and its change is
            # archived; re-litigating them on every audit run reports history that cannot be changed
            # and drowns the findings that can. The first version of these rules omitted this and
            # threw 17 errors at 8 closed features, which forced grandfather markers that were
            # working around this omission rather than around any real exemption.
            # DEFER is NOT settled: its change stays active and its tasks stay claimed,
            # so provenance still applies. Only [DONE] is settled (change archived).
            if section_name in {"SHAPING", "READY", "IN_PROGRESS", "DEFER"}:
                errors.extend(
                    _remediation_gaps(feature_text, feature_path, root, change_id)
                )
                errors.extend(
                    _tasks_without_plans(feature_text, feature_path, root, change_id, tasks)
                )
                errors.extend(
                    _tasks_without_completion_record(feature_text, feature_path, root, tasks)
                )
                errors.extend(
                    _ledger_provenance_errors(feature_text, feature_path, root, change_id)
                )
                errors.extend(_unknown_review_scopes(feature_text, feature_path, root))
                errors.extend(_unknown_review_verdicts(feature_text, feature_path, root))
                errors.extend(
                    _inline_tasks_shadowing_openspec(feature_text, feature_path, root, change_id)
                )
            _DISCLOSURE.append({
                "root": str(root), "feature": feature_id, "section": section_name,
                "done": sum(1 for t in tasks if t.status == "done"),
                "suppressed": [(m, _grandfather_reason(feature_text, m) or "")
                               for m in GRANDFATHER_MARKERS if _grandfathered(feature_text, m)],
            })
            task_statuses = [task.status for task in tasks]
            for task in tasks:
                if task.status == "in_progress":
                    in_progress_records.append((feature_id, task.task_id))

            try:
                current_task = parse_current_task(feature_text)
            except ValueError as exc:
                errors.append(f"{_rel(feature_path, root)} {exc}")
                current_task = None
            reference_error = current_task_reference_error(current_task, tasks)
            if reference_error is not None:
                errors.append(f"{_rel(feature_path, root)} {reference_error}")

            if section_name == "READY" and "ready" not in task_statuses:
                errors.append(
                    f"{_rel(feature_path, root)} is in [READY] but has no task with status `ready`"
                )

            readiness_drift = compute_task_readiness_drift(feature_text, feature_file=feature_path, repo_root=root)
            for drift_message in format_task_readiness_drift_messages(
                readiness_drift,
                feature_label=str(_rel(feature_path, root)),
            ):
                errors.append(drift_message)

    if len(in_progress_records) > 1:
        errors.append(
            f"repository has {len(in_progress_records)} tasks with status `in_progress`, expected at most 1"
        )

    if current_path is not None and (openspec_root / "changes").is_dir():
        try:
            linkage = collect_openspec_change_linkage(root)
        except (WorkflowError, WorkflowStateError) as exc:
            errors.append(str(exc))
            linkage = None
        except Exception as exc:                          # noqa: BLE001 - never abort the audit
            errors.append(f"OpenSpec linkage walk failed: {type(exc).__name__}: {exc}")
            linkage = None
        for change_id in (linkage.orphan_active_change_ids if linkage else []):
            errors.append(f"orphan active OpenSpec change {change_id} is not linked from any promoted feature")

    return errors, in_progress_records


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        root = repo_root(args.repo_root)
    except WorkflowError as exc:
        print(f"ERROR: {exc}")
        return 1

    errors, in_progress_records = _audit_single_root(root)
    aggregated_records: list[tuple[Path, str, str]] = [
        (root, feature_id, task_id) for feature_id, task_id in in_progress_records
    ]

    detached_skipped: list[Path] = []
    if args.include_worktrees:
        _attached, detached_skipped = list_git_worktrees(root)
        for worktree_root in list_git_worktree_roots(root):
            if worktree_root == root.resolve():
                continue
            wt_errors, wt_records = _audit_single_root(worktree_root)
            for wt_error in wt_errors:
                errors.append(f"[worktree {worktree_root}] {wt_error}")
            for feature_id, task_id in wt_records:
                aggregated_records.append((worktree_root, feature_id, task_id))

        distinct_pairs = {(feature_id, task_id) for _, feature_id, task_id in aggregated_records}
        if len(distinct_pairs) > 1:
            errors.append(
                "cross-worktree drift: multiple distinct in_progress tasks across worktrees: "
                + ", ".join(
                    f"{feature_id}/{task_id} in {worktree_root}"
                    for worktree_root, feature_id, task_id in aggregated_records
                )
            )

    if args.gate == "start":
        if aggregated_records:
            scope = "across worktrees" if args.include_worktrees else "in this checkout"
            errors.append(
                f"--gate=start requires 0 in_progress tasks {scope}; found "
                + ", ".join(f"{feature_id}/{task_id}" for _, feature_id, task_id in aggregated_records)
            )
    elif args.gate == "complete":
        distinct_pairs = {(feature_id, task_id) for _, feature_id, task_id in aggregated_records}
        if len(distinct_pairs) != 1:
            scope = "across worktrees" if args.include_worktrees else "in this checkout"
            errors.append(
                f"--gate=complete requires exactly 1 in_progress task {scope}; found {len(distinct_pairs)}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.gate == "complete" and aggregated_records:
        feature_id, task_id = aggregated_records[0][1], aggregated_records[0][2]
        print(f"OK: gate=complete feature_id={feature_id} task_id={task_id}")
    else:
        current_version = root / "docs" / "planning" / "current_version"
        label = current_version.resolve().relative_to(root) if current_version.exists() else current_version
        print(f"OK: workflow audit passed for {label}")
    # A bare `OK` stated nothing about WHAT was checked, so redirecting the root, auditing one
    # checkout of several, or moving a feature to [DEFER]/[DONE] all produced a constant green. The
    # pass now states its own scope and names every check it did not run. This blocks no attack by
    # itself; it makes them visible in the artifact a human actually reads.
    _OPEN = {"SHAPING", "READY", "IN_PROGRESS", "DEFER"}
    roots = sorted({d["root"] for d in _DISCLOSURE}) or [str(root)]
    examined = [d for d in _DISCLOSURE if d["section"] in _OPEN]
    print(f"    root={root.resolve()}  checkouts={len(roots)}"
          + ("" if args.include_worktrees else "  (this checkout only; --include-worktrees unset)"))
    for wt in detached_skipped:
        print(f"    SKIPPED worktree (detached HEAD, not a feature checkout): {wt}")
    print(f"    examined {len(examined)} open feature(s) / "
          f"{sum(d['done'] for d in examined)} done task(s); "
          f"skipped {len(_DISCLOSURE) - len(examined)} settled feature(s)")
    suppressing = [d for d in _DISCLOSURE if d["suppressed"]]
    for d in suppressing:
        for marker, reason in d["suppressed"]:
            # The reason text is printed because its CONTENT cannot be judged mechanically -
            # `grandfathered - was rejected at review` reads as a suppression to the regex. A human
            # reading a pass can see what was waived and why.
            print(f"    DISABLED: {d['feature']} [{d['section']}] {marker} - {reason[:110]}")
    if not suppressing:
        print("    no checks suppressed by grandfather markers")
    return 0


if __name__ == "__main__":
    sys.exit(main())

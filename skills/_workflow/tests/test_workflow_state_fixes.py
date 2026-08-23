#!/usr/bin/env python3
"""Self-tests for the shared-library defects found by the correctness review.

    bin/run-python.sh skills/_workflow/tests/test_workflow_state_fixes.py

Dependency-free, and a SCRIPT rather than a pytest module: its checks run at import and
`sys.exit(1)` on failure, so `conftest.py` excludes it from collection. Each case names
the defect it pins and the production change that would make it fail.
"""
from __future__ import annotations

import os
import pathlib
import sys
import tempfile

for _candidate in pathlib.Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break
from _workflow import workflow_state as ws  # noqa: E402

FAIL: list[str] = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'} {name}" + (f"  {detail}" if not cond and detail else ""))
    if not cond:
        FAIL.append(name)


# --- read_text_or_error: three crashes that aborted the whole audit ---------------------------
_d = pathlib.Path(tempfile.mkdtemp())
(_d / "ok.txt").write_text("hello")
(_d / "bad.txt").write_bytes(b"\xff\xfe")

check("valid UTF-8 reads through", ws.read_text_or_error(_d / "ok.txt") == "hello")
for label, target in [("non-UTF-8", _d / "bad.txt"), ("a directory", _d),
                      ("a missing file", _d / "nope.txt")]:
    try:
        ws.read_text_or_error(target)
        check(f"{label} raises WorkflowStateError", False, "no error raised")
    except ws.WorkflowStateError:
        check(f"{label} raises WorkflowStateError", True)
    except Exception as exc:                                    # noqa: BLE001
        check(f"{label} raises WorkflowStateError", False, f"got {type(exc).__name__}")


# --- evidence categories: exact token, not an alias found inside prose ------------------------
norm = ws._normalize_validation_evidence_category
check("a bare category token matches", norm("schema") == "schema")
check("a backticked token matches", norm("`artifact_repair`") == "artifact_repair")
check("a NEGATION does not count as the category it denies",
      norm("no schema proof applicable") is None,
      "an alias found anywhere in prose used to win, so a negation satisfied the claim")
check("prose naming two categories resolves to neither",
      norm("manual inspection of the schema section") is None,
      "iteration order used to decide which alias won")
check("an unknown token is None, not an error", norm("banana") is None)


# --- ReviewVerdict: a missing `Review Terminal` no longer discards the verdict -----------------
def notes(order):
    new = ("- `2026-08-05`:\n  - Review Scope: `feature_finish`\n  - Review Target: `v1-f001`\n"
           "  - Review Verdict: `blocked`\n")                    # NO Review Terminal
    old = ("- `2026-08-01`:\n  - Review Scope: `feature_finish`\n  - Review Target: `v1-f001`\n"
           "  - Review Verdict: `approved`\n  - Review Terminal: `true`\n")
    return "## 2. Handoff Notes\n" + (new + old if order == "newest-first" else old + new)


check("a verdict missing Review Terminal is retained, not dropped",
      len(ws.parse_handoff_review_verdicts(notes("newest-first"))) == 2,
      "it used to be discarded silently, and the OLDER verdict was reported as current")

check("a missing terminal claim reads as False, not as terminal",
      ws.parse_handoff_review_verdicts(notes("newest-first"))[0].terminal is False)

for order in ("newest-first", "oldest-first"):
    v = ws.latest_review_verdict(notes(order), scope="feature_finish")
    check(f"latest verdict is the newest BY DATE under {order} ordering",
          v is not None and v.verdict == "blocked",
          f"got {v.verdict if v else None!r}; reversed() assumed oldest-first and returned the OLDEST")

check("the entry date is carried on the record",
      ws.parse_handoff_review_verdicts(notes("newest-first"))[0].entry_date == "2026-08-05")


# --- nested task items: indentation is not what makes an item nested --------------------------
check("an indented nested item is recognised",
      ws.OPEN_SPEC_NESTED_TASK_RE.match("  - [ ] 1.3 do a thing") is not None)
check("a ZERO-INDENT nested item is recognised too",
      ws.OPEN_SPEC_NESTED_TASK_RE.match("- [ ] 1.3 do a thing") is not None,
      "requiring indentation let two deleted spaces bypass complete-task's open-item gate")
check("a top-level item is NOT read as nested",
      ws.OPEN_SPEC_NESTED_TASK_RE.match("- [ ] 1 do a thing") is None)
check("a top-level item still matches the top-level pattern",
      ws.OPEN_SPEC_TASK_RE.match("- [ ] 1 do a thing") is not None)
check("a nested item does NOT match the top-level pattern",
      ws.OPEN_SPEC_TASK_RE.match("  - [ ] 1.3 do a thing") is None)


# --- Depends On cycle: a named error, not RecursionError ---------------------------------------
def _cyclic_repo():
    root = pathlib.Path(tempfile.mkdtemp())
    feats = root / "docs/planning/versions/v1/features"
    feats.mkdir(parents=True)
    os.symlink("versions/v1", root / "docs/planning/current_version")
    for a, b in (("v1-f001", "v1-f002"), ("v1-f002", "v1-f001")):
        cid = f"c-{a}"
        (root / "openspec/changes" / cid).mkdir(parents=True)
        (root / "openspec/changes" / cid / "tasks.md").write_text(
            f"- [ ] 1 A\n  - Depends On: `{b}/1`\n")
        (feats / f"{a}-x.md").write_text(
            f"# Feature\n\n## 0. Meta\n- Feature ID: `{a}`\n- OpenSpec Change: `{cid}`\n"
            f"- Current Task: `none`\n")
    return root, feats / "v1-f001-x.md"


_root, _f = _cyclic_repo()
try:
    ws.parse_tasks(_f.read_text(), feature_file=_f, repo_root=_root)
    check("a cross-feature Depends On cycle is reported", False, "no error raised")
except ws.WorkflowStateError as exc:
    check("a cross-feature Depends On cycle raises a NAMED error", "cycle" in str(exc).lower())
except RecursionError:
    check("a cross-feature Depends On cycle raises a NAMED error", False, "still RecursionError")

# The guard must be RELEASED on the way out. Re-parsing the cyclic feature cannot discriminate,
# because the cycle raises either way - so parse a HEALTHY feature TWICE. With a leaked guard the
# second call reports a cycle that does not exist.
def _healthy_repo():
    root = pathlib.Path(tempfile.mkdtemp())
    feats = root / "docs/planning/versions/v1/features"
    feats.mkdir(parents=True)
    os.symlink("versions/v1", root / "docs/planning/current_version")
    (root / "openspec/changes/c1").mkdir(parents=True)
    (root / "openspec/changes/c1/tasks.md").write_text("- [ ] 1 A\n")
    f = feats / "v1-f001-x.md"
    f.write_text("# Feature\n\n## 0. Meta\n- Feature ID: `v1-f001`\n"
                 "- OpenSpec Change: `c1`\n- Current Task: `none`\n")
    return root, f


_hr, _hf = _healthy_repo()
_first_ok = False
try:
    ws.parse_tasks(_hf.read_text(), feature_file=_hf, repo_root=_hr)
    _first_ok = True
except Exception as exc:                                        # noqa: BLE001
    check("a healthy feature parses once", False, f"{type(exc).__name__}: {exc}")
if _first_ok:
    check("a healthy feature parses once", True)
    try:
        ws.parse_tasks(_hf.read_text(), feature_file=_hf, repo_root=_hr)
        check("the cycle guard is released, so the SAME feature parses twice", True)
    except ws.WorkflowStateError as exc:
        check("the cycle guard is released, so the SAME feature parses twice", False,
              f"leaked guard reports a cycle that does not exist: {exc}")

print()
if FAIL:
    print(f"{len(FAIL)} FAILED: {', '.join(FAIL)}")
    sys.exit(1)
print("all workflow_state fix self-tests passed")


# --- worktree walk: a detached throwaway is not a feature checkout ------------------------------
# Measured: three detached fixture worktrees in another session's /tmp scratchpad were walked as
# feature checkouts, and their fixture planning state produced errors naming a REAL feature file.
import subprocess  # noqa: E402


def _git_repo_with_worktrees():
    root = pathlib.Path(tempfile.mkdtemp()) / "repo"
    root.mkdir()
    def g(*a, cwd=root):
        return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)
    g("init", "-q", "-b", "main")
    g("config", "user.email", "t@t"); g("config", "user.name", "t")
    (root / "f.txt").write_text("x")
    g("add", "-A"); g("commit", "-qm", "init")
    base = root.parent
    g("worktree", "add", "-q", "-b", "feat", str(base / "attached"), "HEAD")
    g("worktree", "add", "-q", "--detach", str(base / "throwaway"), "HEAD")
    return root, base


_r, _base = _git_repo_with_worktrees()
_att, _det = ws.list_git_worktrees(_r)
_att_names = {p.name for p in _att}
_det_names = {p.name for p in _det}

check("the branch-attached worktree is included", "attached" in _att_names)
check("the caller's own root is included", "repo" in _att_names)
check("the DETACHED worktree is separated out", _det_names == {"throwaway"},
      f"attached={sorted(_att_names)} detached={sorted(_det_names)}")
check("a detached worktree is NOT in the attached list", "throwaway" not in _att_names,
      "its fixture planning state produced errors attributed to a real feature file")
check("list_git_worktree_roots excludes detached trees",
      "throwaway" not in {p.name for p in ws.list_git_worktree_roots(_r)})
check("the detached tree is RETURNED, not dropped, so the caller can disclose it",
      len(_det) == 1)

# auditing from INSIDE a detached worktree must still include it: it is the caller's own root
_inside_att, _inside_det = ws.list_git_worktrees(_base / "throwaway")
check("auditing from inside a detached worktree still covers it",
      (_base / "throwaway").resolve() in [p.resolve() for p in _inside_att],
      "otherwise a detached checkout could never be audited at all")


# --- the completion-ledger template must survive template RESOLUTION, not just the repo copy ---
# Found 2026-08-09 by hand, invisible to every existing test. `feature_file` resolves its template
# from four sources; with `repo_root=None` (which is how module-level FEATURE_TEMPLATE is built, and
# what `init_workflow_artifacts` writes into a NEWLY initialized repo) the repo copy is never
# consulted. Both remaining sources — the installed template and the hardcoded fallback string —
# still carried the pre-gate prose telling the agent to hand-type `- Task \`N\` completed \`DATE\``.
# So every new repo was seeded with the exact bypass `write_completion_ledger.py` exists to close,
# while this repo looked correct because the renderer happens to pass repo_root.
from _workflow import feature_file as ff  # noqa: E402

# The two on-disk template files are layout-dependent: the TRACKED copy exists only in a repo
# checkout, the INSTALLED copy only under a synced skills root (install.sh generates it). Check
# whichever are present rather than a fixed one, or this file passes in one layout and crashes with
# FileNotFoundError in the other -- and it is the installed copy that seeds new repos.
_template_files = [("the tracked template file", ff._TRACKED_FEATURE_TEMPLATE_PATH),
                   ("the installed template file", ff._INSTALLED_FEATURE_TEMPLATE_PATH)]
_present = [(_l, _p.read_text(encoding="utf-8")) for _l, _p in _template_files if _p.is_file()]
check("at least one on-disk template file was found to check",
      bool(_present),
      "neither the tracked nor the installed template resolved, so this block proved nothing")

for _label, _text in ([("module-level FEATURE_TEMPLATE", ff.FEATURE_TEMPLATE),
                       ("repo_root=None resolution", ff._load_feature_template(None)),
                       ("the hardcoded fallback string", ff._FALLBACK_FEATURE_TEMPLATE)]
                      + _present):
    check(f"{_label} names the ledger WRITER script",
          "write_completion_ledger.py" in _text,
          "a template that omits it tells the agent to hand-type the line the audit rejects")
    check(f"{_label} carries the re-verified plan-sha256 field",
          "plan-sha256" in _text)
    check(f"{_label} does not still say the line is written BY complete-task itself",
          "written BY `complete-task`" not in _text,
          "that phrasing is what made a gated close and a forged one byte-identical")


# --- Depends On continuation: where a field's collection STOPS ---------------------------------
# `Depends On` and `OpenSpec Specs` collect backticked refs from the lines FOLLOWING their header,
# because both are written as a header plus indented bullets. That collection had no stop condition,
# so it ran to the next field header and swallowed whatever lay between. Two shapes leaked, both
# silently: a nested checklist item under the task contributed its filenames, and the FOLLOWING
# section heading and prose contributed theirs. Nothing errors -- the caller receives a plausible
# dependency list nobody wrote, and no code checks that a referenced task ID exists.
#
# Found 2026-08-22 while giving v1-f004 real task dependencies: `- Depends On: `1`` followed by its
# nested items parsed as ('1', 'test_universe_real.py', 'test_universe_size_real.py').
#
# Plain bullets must STILL continue a field: `- Depends On:` over indented `- `T01`` lines is the
# documented multi-line form and is used by existing feature files. So only headings, checklist
# items, and blank lines terminate. Each case below isolates ONE alternative -- no blank line
# precedes the checklist item or the heading -- so the mutation sweep can tell them apart.


def _deps(text, idx=0):
    return ws._parse_openspec_tasks_text(text)[idx].depends_on


check("Depends On stops at a nested checklist item",
      _deps("- [ ] 2 T\n  - Depends On: `1`\n  - [ ] 2.1 Migrate `mod.py`\n") == ("1",),
      "catches dropping the checklist alternative from FIELD_CONTINUATION_STOP_RE")
check("Depends On stops at an immediately following heading",
      _deps("- [ ] 2 T\n  - Depends On: `1`\n## 3. Migrate `security-identity`\n") == ("1",),
      "catches dropping the heading alternative")
check("Depends On stops at a blank line before prose",
      _deps("- [ ] 2 T\n  - Depends On: `1`\n\nProse citing `tests/conftest.py`.\n") == ("1",),
      "catches dropping the blank alternative")
check("Depends On does not resume collecting after it stops",
      _deps("- [ ] 2 T\n  - Depends On: `1`\n  - [ ] 2.1 a\n  plain line citing `x.py`\n") == ("1",),
      "catches stopping without clearing current_field")
check("multi-line bullet continuation still parses",
      _deps("- [ ] 2 T\n  - Depends On:\n    - `1`\n    - none\n") == ("1",),
      "CONTROL: the documented form must not regress")
check("refs on the header line still parse",
      _deps("- [ ] 5 T\n  - Depends On: `1`, `2`, `3`\n") == ("1", "2", "3"),
      "CONTROL")

_feat = ("## 6. Tasks\n\n### T02: Second\n- Status: `todo`\n- Depends On:\n  - `T01`\n\n"
         "### T03: Third\n- Status: `todo`\n- Depends On: `T02`\n- [ ] stray `nope.py`\n")
_recs = {r.task_id: r.depends_on for r in ws._parse_feature_file_tasks(_feat)}
check("feature-file parser keeps bullet continuation",
      _recs.get("T02") == ("T01",), "CONTROL")
check("feature-file parser stops at a checklist item",
      _recs.get("T03") == ("T02",),
      "the two parsers are duplicated; catches fixing only the tasks.md one")


# `OpenSpec Specs` collects the same way and had the same hole, guarded only against `## `. Measured
# before fixing: a checklist item or a blank-line-then-prose after the specs list contributed its
# backticks as spec paths. Parsed output for all five real feature files is byte-identical before and
# after, so the rule closes the hole without changing any legitimate parse.

_meta = "## 0. Meta\n- OpenSpec Specs:\n  - `openspec/changes/x/specs/cap/spec.md`\n"
_only = ["openspec/changes/x/specs/cap/spec.md"]
check("OpenSpec Specs keeps its bullet list",
      ws.parse_feature_openspec_specs(_meta + "- Current Task: `none`\n") == _only, "CONTROL")
check("OpenSpec Specs stops at a checklist item",
      ws.parse_feature_openspec_specs(_meta + "- [ ] stray citing `not-a-spec.md`\n") == _only)
check("OpenSpec Specs stops at a blank line before prose",
      ws.parse_feature_openspec_specs(_meta + "\nProse citing `also-not-a-spec.md`.\n") == _only)


# --- a dotted task reference is not a numeric pin -------------------------------------------------
# The claim-evidence lint's DECIMAL_OR_PERCENT_PIN_RE matches `\d+\.\d+`, so `task 3.2` read as a
# measurement and demanded an evidence block for a number nobody measured. Measured cost on
# technical-strategy v1-f005: it forced a rewrite of a sentence in a CLOSED task's implementation
# plan, which broke that task's `plan-sha256` completion stamp and failed the audit.
#
# The third case is the one that discriminates. Stripping the reference must remove the REFERENCE
# and nothing else: an implementation that dropped the whole line, or that stripped every decimal
# once it saw the word "task", would pass the first two cases and fail this one.
check("a bare decimal is still a pin",
      ws._line_has_numeric_pin("The ratio improved to 3.2 in the second run."), "CONTROL")
check("an explicit task reference is not a pin",
      not ws._line_has_numeric_pin("Task 3.2 settled that verification runs in the ingest."))
check("a real pin on the same line as a task reference still fires",
      ws._line_has_numeric_pin("Task 3.2 took 3.7 seconds to run."))
check("a bare dotted number stays a pin, because the tool would be guessing",
      ws._line_has_numeric_pin("and 3.2 left implicit what the pin compares against"))


# --- FINAL gate --------------------------------------------------------------------------------
# The summary at line ~157 sits MID-FILE: every block below it (the worktree walk, the template
# resolution checks) runs after that verdict, so before this gate existed their failures were
# appended to FAIL and never read. Proven 2026-08-09 by reintroducing the stale fallback template:
# the run printed two FAIL lines and still exited 0. A test whose failure cannot fail the suite is
# decorative, so the exit status is asserted HERE, after the last check.
print()
if FAIL:
    print(f"{len(FAIL)} FAILED: {', '.join(FAIL)}")
    sys.exit(1)
print("all workflow_state fix self-tests passed, INCLUDING the blocks below the mid-file summary")

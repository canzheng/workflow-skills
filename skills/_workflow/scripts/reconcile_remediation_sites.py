#!/usr/bin/env python3
"""Gate the NEXT round on every swept site being reconciled, and on the sweep having really run.

This is the half of the gate that cannot be done by reading text.

## Why it exists

`bt:v1-f047` took 23 remediation rounds. Grouped by defect CLASS rather than by round, ~6 classes were
spread across them, and the recurring shape was always the same: the reviewer named ONE site, the round
fixed THAT site, and the next review found the same shape one file over. Gates 10/11, 14/15 and 19/20 are
each a pair a completed sweep would have collapsed into one round.

The catalogue lint makes the author WRITE the sweep. It cannot make the fix GO there. This does:

  - **Every declared site must be reconciled** -- `fixed`, `deferred`, or `rejected` -- before the round
    may progress. A site left unmentioned is the instance-fixing failure, and it is exactly what a
    catalogue looks like when someone fixes the reported instance and moves on.
  - **`fixed` is checked against the diff.** If the site's file was not touched by this round, the claim
    is false. `deferred` and `rejected` need a reason, so dropping a site is a decision on the record
    rather than an omission.
  - **The sweep command is RUN.** Three attempts to decide "is this string a command?" from the string
    failed in both directions -- the last rejected `rg -n "is None" src/` because `is` and `None` are
    English function words, in a tool that gates sweeps of source code. Running it is decidable:
    prose does not execute, an unfilled `<pattern>` slot finds nothing, and -- the real prize -- a
    command that finds FIVE files when the catalogue lists ONE is an under-reported sweep, caught
    before the fix rather than one round after it.

## Safety

Commands come out of a file, so execution is bounded deliberately: an allowlist of read-only search
tools, no shell (`shell=False`, no pipes, redirection, `&&`, `;`, backticks or `$(...)`), a timeout, and
the repo root as cwd. Note the allowlist is a SAFETY boundary here, not a judgement about whether a
string is command-shaped -- conflating those two is what made the previous approach unsound.
"""
from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required", file=sys.stderr)
    raise SystemExit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint_remediation_round import extract_blocks, _StrictLoader, _blank, _clean_text  # noqa: E402

ALLOWED = {"grep", "rg", "ag", "ack", "git", "find", "fd", "ls"}
FORBIDDEN = re.compile(r"[|;&`><]|\$\(")
DISPOSITIONS = {"fixed", "deferred", "rejected"}
# A site is "file[:line] optional note"; only the path is load-bearing for the diff check.
SITE_PATH_RE = re.compile(r"^\s*([^\s:]+?\.[A-Za-z0-9_]+|[^\s:]+/[^\s:]*)")
# Build artefacts and VCS internals are not sites. Without this the under-declared-sweep check reports
# `__pycache__/*.pyc` as an unfixed sibling, which is noise that trains the reader to skim the finding.
IGNORE_RE = re.compile(r"(^|/)(__pycache__|\.git|\.mypy_cache|\.pytest_cache|node_modules|"
                       r"\.venv|venv|build|dist)(/|$)|\.(pyc|pyo|so|egg-info)$")


class Issue:
    def __init__(self, where: str, reason: str) -> None:
        self.where, self.reason = where, reason

    def render(self, path: Path) -> str:
        return f"ERROR: {path}: {self.where}: {self.reason}"


def site_path(site: str) -> str | None:
    m = SITE_PATH_RE.match(str(site))
    return m.group(1) if m else None


def changed_files(repo: Path, since: str | None) -> set[str] | None:
    args = ["git", "-C", str(repo), "diff", "--name-only"] + ([f"{since}...HEAD"] if since else ["HEAD"])
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0:
        return None
    out = {ln.strip() for ln in r.stdout.splitlines() if ln.strip()}
    if not since:      # uncommitted rounds also live in the index and in untracked files
        for extra in (["diff", "--name-only", "--cached"], ["ls-files", "--others", "--exclude-standard"]):
            rr = subprocess.run(["git", "-C", str(repo)] + extra, capture_output=True, text=True)
            out |= {ln.strip() for ln in rr.stdout.splitlines() if ln.strip()}
    return out


def run_sweep(cmd: str, repo: Path, timeout: int) -> tuple[bool, str, set[str]]:
    """(ran, note, files_found). `ran` is False when the command is refused or errors."""
    if FORBIDDEN.search(cmd):
        return False, "contains a shell metacharacter; commands are run without a shell", set()
    try:
        argv = shlex.split(cmd)
    except ValueError as exc:
        return False, f"is not parseable as a command ({exc})", set()
    if not argv:
        return False, "is empty", set()
    tool = Path(argv[0]).name
    if tool not in ALLOWED:
        return False, (f"starts with {tool!r}, which is not in the read-only allowlist "
                       f"({', '.join(sorted(ALLOWED))}). Re-express the sweep with one of those"), set()
    try:
        r = subprocess.run(argv, cwd=repo, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s", set()
    except OSError as exc:
        return False, f"could not be executed ({exc})", set()
    if r.returncode not in (0, 1):        # 1 == no matches for grep/rg
        return False, f"exited {r.returncode}: {r.stderr.strip().splitlines()[:1]}", set()
    files = set()
    for ln in r.stdout.splitlines():
        head = ln.split(":", 1)[0].strip().lstrip("./")
        if head and not IGNORE_RE.search(head):
            files.add(head)
    return True, f"{len(files)} file(s)", files


def check(path: Path, repo: Path, since: str | None, timeout: int, run: bool) -> list[Issue]:
    out: list[Issue] = []
    blocks = extract_blocks(path.read_text(encoding="utf-8"))
    if len(blocks) != 1:
        return [Issue("file", "expected exactly one ```yaml block; run the catalogue lint first")]
    try:
        doc = yaml.load(blocks[0][0], Loader=_StrictLoader)
    except yaml.YAMLError as exc:
        return [Issue("yaml", f"does not parse: {str(exc).splitlines()[0]}")]
    findings = (doc or {}).get("findings") or []
    if not isinstance(findings, list):
        return [Issue("findings", "must be a list; run the catalogue lint first")]

    diff = changed_files(repo, since)
    if diff is None:
        out.append(Issue("git", f"could not read the diff for {repo}; `fixed` claims cannot be checked"))

    for i, f in enumerate(findings, start=1):
        if not isinstance(f, dict):
            continue
        where = f"findings[{i}] ({f.get('id') or '?'})"
        sweep = f.get("class_sweep") or {}
        sites = sweep.get("sites") if isinstance(sweep, dict) else None
        if not isinstance(sites, list) or not sites:
            out.append(Issue(where, "no `class_sweep.sites` to reconcile; run the catalogue lint first"))
            continue

        rec = f.get("reconciliation")
        missing_rec = not isinstance(rec, list) or not rec
        if missing_rec:  # MUT:rec_required
            out.append(Issue(where, f"`reconciliation:` is missing. Every one of the {len(sites)} swept "
                                    f"site(s) must be `fixed`, `deferred` or `rejected` before the next "
                                    f"round -- an unmentioned site is the instance-fixing failure this "
                                    f"gate exists to stop"))
        if missing_rec:
            # Guarded separately so disabling the check above yields a PASS rather than a TypeError:
            # a mutant that crashes is indistinguishable from a fixture that discriminates.
            continue

        seen: dict[str, str] = {}
        for r in rec:
            if not isinstance(r, dict) or _blank(r.get("site")):
                out.append(Issue(where, f"each `reconciliation` entry needs a `site:`; got {r!r}"))
                continue
            site = _clean_text(str(r["site"]))
            disp = _clean_text(str(r.get("disposition", "")))
            if site in seen:
                out.append(Issue(where, f"site {site!r} reconciled twice"))
            seen[site] = disp
            if site not in {_clean_text(str(x)) for x in sites}:
                out.append(Issue(where, f"reconciles {site!r}, which the sweep never declared"))
            if disp not in DISPOSITIONS:  # MUT:disposition
                out.append(Issue(where, f"site {site!r}: `disposition` must be one of "
                                        f"{sorted(DISPOSITIONS)}, got {disp!r}"))
            elif disp in ("deferred", "rejected"):
                reason = r.get("reason")
                if _blank(reason) or len(_clean_text(str(reason)).split()) < 4:  # MUT:reason_required
                    out.append(Issue(where, f"site {site!r} is {disp} but gives no reason -- dropping a "
                                            f"swept site is a decision and goes on the record"))
            elif disp == "fixed" and diff is not None:
                sp = site_path(site)
                if sp and not any(c == sp or c.endswith("/" + sp) or sp.endswith("/" + c) for c in diff):  # MUT:fixed_in_diff
                    out.append(Issue(where, f"site {site!r} is marked `fixed` but {sp!r} is not in this "
                                            f"round's diff"))

        for s in sites:
            if _clean_text(str(s)) not in seen:  # MUT:unreconciled
                out.append(Issue(where, f"site {str(s)!r} is declared by the sweep and NOT reconciled"))

        cmd = sweep.get("command")
        if run and not _blank(cmd):
            ok, note, found = run_sweep(str(cmd), repo, timeout)
            if not ok:
                out.append(Issue(where, f"`class_sweep.command` {note}. A sweep that cannot be re-run is "
                                        f"not evidence that it ran"))
            elif not found:
                out.append(Issue(where, "`class_sweep.command` runs but finds nothing; it cannot be the "
                                        "search that produced these sites"))
            else:
                declared = {site_path(s) for s in sites} - {None}
                missed = {c for c in found if not any(c == d or c.endswith("/" + d) or
                                                      (d and d.endswith("/" + c)) for d in declared)}
                if missed:  # MUT:undeclared
                    out.append(Issue(where, f"the sweep command finds {len(found)} file(s) but only "
                                            f"{len(declared)} are declared; UNDECLARED: "
                                            f"{sorted(missed)[:6]}. An under-reported sweep is how the "
                                            f"same shape is found one file over, one round later"))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Reconcile every swept site before the next round.")
    ap.add_argument("gate_file")
    ap.add_argument("--repo", default=".", help="Repo root; sweeps run here and the diff is read here.")
    ap.add_argument("--since", help="Diff base (e.g. the previous round's commit). Default: working "
                                    "tree + index + untracked against HEAD.")
    ap.add_argument("--no-run", action="store_true", help="Skip executing sweep commands.")
    ap.add_argument("--timeout", type=int, default=60)
    a = ap.parse_args(sys.argv[1:] if argv is None else argv)

    path, repo = Path(a.gate_file), Path(a.repo)
    if not path.is_file():
        print(f"ERROR: not a file: {path}", file=sys.stderr)
        return 1
    issues = check(path, repo, a.since, a.timeout, not a.no_run)
    if issues:
        for it in issues:
            print(it.render(path), file=sys.stderr)
        print(f"\n{len(issues)} issue(s). Every swept site must be fixed, deferred or rejected before "
              f"the round progresses.", file=sys.stderr)
        return 1
    print(f"OK: {path} — every swept site is reconciled"
          + ("" if a.no_run else ", and every sweep command re-runs and finds no undeclared site"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

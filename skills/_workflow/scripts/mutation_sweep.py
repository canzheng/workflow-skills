#!/usr/bin/env python3
"""Run a mutation sweep in a DETACHED WORKTREE, so it cannot touch the tree you are editing.

    python mutation_sweep.py --repo <path> --spec <sweep.json> [--control <test id>] [--jobs N]

The spec is a JSON list of `{"label", "file", "anchor", "replacement"}`, `file` relative to the repo.

WHY A DETACHED WORKTREE. The obvious harness mutates the live checkout and restores with
`git checkout -- src/`. That restore is indiscriminate: it reverts UNCOMMITTED work the sweep did not
make. Measured -- a sweep wiped an uncommitted comment edit mid-run, and a killed sweep once left a
mutation stranded in `src/` because the restore never ran. Neither can happen here: the mutation and
the restore both live in a throwaway checkout of HEAD.

EVERY MUTATION IS CHECKED BEFORE ITS RESULT IS BELIEVED, because a mutation harness reports a
survivor for reasons that have nothing to do with the code:

- the anchor must match EXACTLY ONE site   (matched the wrong one of three occurrences)
- the file must actually change            (anchor unique in the file, replacement matched nothing)
- the result must compile                  (a non-compiling mutation read as a survivor)
- a CONTROL test must still pass under it  (a NameError raised before the defect could be observed,
                                            and eleven broad failures read as detection)

Anything failing those is reported as NOT RUN rather than as a survivor or a catch.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _run(cmd, cwd, timeout=1800):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def _summary(stdout: str) -> str:
    lines = [l for l in stdout.splitlines() if " passed" in l or " failed" in l or " error" in l]
    return lines[-1] if lines else "(no pytest summary)"


def _apply(worktree: Path, mutation: dict) -> str | None:
    """Apply one mutation. Returns an error string when it must NOT be run, else None."""
    target = worktree / mutation["file"]
    if not target.exists():
        return f"{mutation['file']} does not exist in the worktree"
    before = target.read_text()
    n = before.count(mutation["anchor"])
    if n != 1:
        return f"anchor matches {n} sites (needs exactly 1)"
    after = before.replace(mutation["anchor"], mutation["replacement"])
    if after == before:
        return "replacement left the file unchanged"
    if target.suffix == ".py":
        try:
            compile(after, str(target), "exec")
        except SyntaxError as exc:
            return f"mutation does not compile: {exc}"
    target.write_text(after)
    return None


def _sweep_one(repo: Path, head: str, mutation: dict, control: str | None,
               test_cmd: list[str]) -> dict:
    tmp = Path(tempfile.mkdtemp(prefix="mutsweep-"))
    worktree = tmp / "wt"
    try:
        _run(["git", "worktree", "add", "--detach", str(worktree), head], repo)
        problem = _apply(worktree, mutation)
        if problem:
            return {"label": mutation["label"], "verdict": "NOT RUN", "detail": problem}

        if control:
            probe = _run([*test_cmd, control], worktree)
            if probe.returncode != 0:
                return {"label": mutation["label"], "verdict": "NOT RUN",
                        "detail": f"control test {control} fails under the mutation, so the "
                                  f"defect is not cleanly reached: {_summary(probe.stdout)}"}

        r = _run(test_cmd, worktree)
        failed = [l for l in r.stdout.splitlines() if l.startswith("FAILED")]
        return {
            "label": mutation["label"],
            "verdict": "CAUGHT" if r.returncode != 0 else "SURVIVED",
            "detail": _summary(r.stdout),
            "failed": failed[:5],
        }
    finally:
        _run(["git", "worktree", "remove", "--force", str(worktree)], repo)
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--spec", required=True, type=Path)
    ap.add_argument("--control", default=None,
                    help="a test id that must PASS under every mutation, proving it is reached")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--test-cmd", default="uv run pytest -q")
    args = ap.parse_args()

    repo = args.repo.resolve()
    mutations = json.loads(args.spec.read_text())
    test_cmd = args.test_cmd.split()

    dirty = _run(["git", "status", "--porcelain"], repo).stdout.strip()
    if dirty:
        print("REFUSING: the repo has uncommitted changes. The sweep runs against HEAD in a "
              "detached worktree, so uncommitted work would be invisible and the result would "
              "describe code you are not running.\n" + dirty, file=sys.stderr)
        return 2
    head = _run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    print(f"sweeping {len(mutations)} mutation(s) against {head[:12]} in detached worktrees")

    results = []
    if args.jobs > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(_sweep_one, repo, head, m, args.control, test_cmd)
                       for m in mutations]
            for f in concurrent.futures.as_completed(futures):
                results.append(f.result())
    else:
        for m in mutations:
            results.append(_sweep_one(repo, head, m, args.control, test_cmd))

    order = {"SURVIVED": 0, "NOT RUN": 1, "CAUGHT": 2}
    caught = sum(1 for r in results if r["verdict"] == "CAUGHT")
    not_run = sum(1 for r in results if r["verdict"] == "NOT RUN")
    print()
    for r in sorted(results, key=lambda r: (order[r["verdict"]], r["label"])):
        mark = {"CAUGHT": "CAUGHT          ", "SURVIVED": "*** SURVIVED ***",
                "NOT RUN": "!! NOT RUN      "}[r["verdict"]]
        print(f"{mark} {r['label']}\n                 {r['detail']}")
        for line in r.get("failed", []):
            print(f"                 {line}")

    print(f"\ncaught {caught}/{len(mutations)}"
          + (f"; {not_run} NOT RUN (neither caught nor survived)" if not_run else ""))
    still = _run(["git", "status", "--porcelain"], repo).stdout.strip()
    print(f"source tree untouched: {still == ''}")
    return 1 if (caught + not_run) != len(mutations) or still else 0


if __name__ == "__main__":
    raise SystemExit(main())

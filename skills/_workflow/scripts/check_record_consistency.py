#!/usr/bin/env python3
"""Re-derive the checkable claims a feature's records make, against the tree as it stands.

    python check_record_consistency.py --repo <path> --feature-id v1-f006

WHY THIS EXISTS. Across one feature's five gates, the single most productive question was "does any
record assert something the tree does not contain?" -- it produced findings at three of them, and
each cost a full gate cycle plus a remediation round to discover by reading. Every one was
mechanically checkable:

- a completion ledger's `plan-sha256` against the plan it stamps -- a CLOSED plan edited afterwards
- a catalogue prescribing a fix, and the fix absent from the diff
- a handoff entry naming files a round did not touch on net
- a count stated in prose against the thing it counts

A reviewer reads for meaning and is poor at arithmetic over a large record. This is the opposite, so
it belongs in a script that runs in seconds rather than in a gate that costs a reviewer context.

WHAT IT DOES NOT DO: judge whether a record's PROSE is true. It checks the claims that can be
re-derived. A sentence asserting something unquantified still needs a reader.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


def _feature_file(repo: Path, feature_id: str) -> Path | None:
    hits = sorted((repo / "docs" / "planning").rglob(f"features/{feature_id}-*.md"))
    return hits[0] if len(hits) == 1 else None


def _change_dir(repo: Path, change_id: str) -> Path | None:
    active = repo / "openspec" / "changes" / change_id
    if (active / "tasks.md").exists():
        return active
    archived = sorted((repo / "openspec" / "changes" / "archive").glob(f"*-{change_id}"))
    return archived[0] if len(archived) == 1 else None


def check(repo: Path, feature_id: str) -> list[str]:
    problems: list[str] = []
    feat = _feature_file(repo, feature_id)
    if feat is None:
        return [f"no single feature file for {feature_id}"]
    text = feat.read_text()

    m = re.search(r"^- OpenSpec Change: `([^`]+)`", text, re.M)
    if not m:
        return [f"{feat.name} has no OpenSpec Change metadata"]
    change_id = m.group(1)
    if change_id.startswith("archive/") or re.match(r"^\d{4}-\d{2}-\d{2}-", change_id):
        problems.append(
            f"OpenSpec Change is {change_id!r}; it must stay the BARE change id -- the audit and "
            "resolvers treat it as a lookup key and derive archive state from filesystem globs"
        )
    change = _change_dir(repo, change_id)
    if change is None:
        return problems + [f"no active or archived change directory for {change_id!r}"]

    # 1. every completion-ledger stamp still matches the plan it was taken over
    ledger = [l for l in text.splitlines() if re.match(r"^- Task `[^`]+` completed ", l)]
    for line in ledger:
        task = re.search(r"Task `([^`]+)`", line).group(1)
        stamp = re.search(r"plan-sha256 `([0-9a-f]+)`", line)
        if not stamp:
            problems.append(f"ledger line for task {task} carries no plan-sha256")
            continue
        plan = change / "implementation-plans" / f"{task}.md"
        if not plan.exists():
            problems.append(f"ledger line for task {task} stamps a plan that does not exist")
            continue
        actual = hashlib.sha256(plan.read_bytes()).hexdigest()[: len(stamp.group(1))]
        if actual != stamp.group(1):
            problems.append(
                f"task {task}: plan digests to {actual} but the ledger stamps "
                f"{stamp.group(1)} -- the plan changed after the task closed"
            )

    # 2. one done task per ledger line, and vice versa
    tasks_md = (change / "tasks.md").read_text()
    done = len(re.findall(r"^- \[x\] ", tasks_md, re.M))
    if done != len(ledger):
        problems.append(f"{done} top-level tasks are done but {len(ledger)} ledger lines exist")

    # 3. every remediation catalogue names a gate that the record actually ran
    gates = {int(n) for n in re.findall(r"Gate Iteration: (\d+)", text)}
    for cat in sorted((change / "remediation").glob("gate-*.md")):
        n = int(re.search(r"gate-(\d+)", cat.name).group(1))
        if n not in gates:
            problems.append(f"{cat.name} catalogues a gate the feature file never records running")

    # 4. every scenario in the delta spec is closed exactly once, if a manifest exists
    manifest = change / "acceptance" / "scenario-closure.md"
    if manifest.exists():
        scenarios = sum(
            p.read_text().count("#### Scenario:") for p in sorted(change.glob("specs/**/spec.md"))
        )
        rows = len(re.findall(r"^\|\s*(?:test|out_of_band)\s*\|", manifest.read_text(), re.M))
        if scenarios != rows:
            problems.append(f"{scenarios} scenarios in the delta spec but {rows} manifest rows")

    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--feature-id", required=True)
    args = ap.parse_args(argv or sys.argv[1:])
    problems = check(args.repo.resolve(), args.feature_id)
    for p in problems:
        print(f"ERROR: {p}", file=sys.stderr)
    if problems:
        return 1
    print(f"OK: {args.feature_id}'s records agree with the tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

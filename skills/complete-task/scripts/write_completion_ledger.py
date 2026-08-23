#!/usr/bin/env python3
"""Write the completion-ledger line for a closed task. THE ONLY writer of that line.

    python3 write_completion_ledger.py --feature-id v1-f012 --task-id 4 [--repo-root PATH]

## Why this script exists

The ledger's first version was prose: `complete-task` step 8 told the agent to append
`- Task \\`N\\` completed \\`DATE\\`` by hand. Three independent reviews concluded that made it
ceremony, and they were right — a hand-written line and a gated one were **byte-identical by
construction**, so the record could not distinguish them. Worse, the audit's own error message
dictated the exact string to type and then named the opt-out in the next clause.

So the line now carries two fields an agent cannot produce by typing prose:

- `plan-sha256` — the digest of the task's implementation plan. Producing it requires reading that
  file; guessing it is not possible, and the audit RE-COMPUTES it, so a wrong value is an error
  rather than a pass.
- `head` — the commit HEAD pointed at when the task closed. The audit checks it is a real commit and
  an ancestor of the current branch head.

This does not make forgery impossible — an agent can shell out to `sha256sum` and `git rev-parse`.
It converts forgery from *"type the sentence the error message just dictated"* into *"assemble a
multi-field record and deliberately lie"*, which is a different act and one a code review can see.
That is the honest ceiling for a markdown-based workflow; claiming more would repeat the mistake
this script fixes.

## Preconditions, checked before writing

The task must already be `done` in the linked `tasks.md`, and its plan must exist. Writing a line
for a task that is not closed would pre-approve a close that has not happened — the exact attack the
audit's pre-seed check catches.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

for _candidate in Path(__file__).resolve().parents:
    if (_candidate / "_workflow").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from _workflow.cli_helpers import WorkflowError, load_backlog, repo_root  # noqa: E402
from _workflow.workflow_state import (  # noqa: E402
    WORKFLOW_SECTIONS,
    parse_feature_openspec_change,
    parse_tasks,
    read_text_or_error,
)

LEDGER_HEADING = "## 3. Task Completion Ledger"


def find_feature(root: Path, feature_id: str) -> tuple[Path, str]:
    backlog_path, _text, parsed = load_backlog(root)
    for section_name in WORKFLOW_SECTIONS[1:]:
        for entry in parsed.feature_sections.get(section_name, []):
            if entry.feature_id == feature_id:
                path = (backlog_path.parent / entry.link).resolve()
                if not path.is_file():
                    raise WorkflowError(f"feature file for {feature_id} is missing: {path}")
                return path, read_text_or_error(path)
    raise WorkflowError(f"feature {feature_id} not found in the active backlog")


def git_head(root: Path) -> str:
    r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
    if r.returncode:
        raise WorkflowError(f"could not read HEAD: {r.stderr.strip()}")
    return r.stdout.strip()[:12]


def ledger_line(task_id: str, day: str, plan_digest: str, head: str) -> str:
    return (f"- Task `{task_id}` completed `{day}` "
            f"plan-sha256 `{plan_digest[:16]}` head `{head}`")


def write(root: Path, feature_id: str, task_id: str, *, today: str | None = None) -> str:
    feature_path, feature_text = find_feature(root, feature_id)
    change_id = parse_feature_openspec_change(feature_text)
    if change_id is None:
        raise WorkflowError(f"{feature_path.name} is missing OpenSpec Change metadata")

    tasks = parse_tasks(feature_text, feature_file=feature_path, repo_root=root)
    match = next((t for t in tasks if t.task_id == task_id), None)
    if match is None:
        raise WorkflowError(f"task {task_id} not found in feature {feature_id}")
    if match.status != "done":
        # A line written before the close pre-approves a close that has not happened.
        raise WorkflowError(
            f"task {task_id} has status `{match.status}`, not `done`; mark it done in tasks.md "
            f"before writing its ledger line")

    plan = root / "openspec" / "changes" / change_id / "implementation-plans" / f"{task_id}.md"
    if not plan.is_file():
        raise WorkflowError(f"implementation plan is missing: {plan.relative_to(root)}")
    digest = hashlib.sha256(plan.read_bytes()).hexdigest()

    day = today or dt.date.today().isoformat()
    line = ledger_line(task_id, day, digest, git_head(root))

    if re.search(rf"^\s*-\s*Task\s+`{re.escape(task_id)}`\s+completed\s", feature_text, re.M):
        raise WorkflowError(
            f"a completion-ledger line for task {task_id} already exists; refusing to write a "
            f"second one. Remove the stale line deliberately if it is wrong.")

    if LEDGER_HEADING in feature_text:
        body = feature_text.rstrip("\n")
        head_part, _, tail = body.partition(LEDGER_HEADING)
        updated = head_part + LEDGER_HEADING + tail.rstrip("\n") + "\n" + line + "\n"
    else:
        updated = feature_text.rstrip("\n") + f"\n\n{LEDGER_HEADING}\n" + line + "\n"

    tmp = feature_path.with_name(feature_path.name + f".tmp-{os.getpid()}")
    try:
        tmp.write_text(updated, encoding="utf-8")
        os.replace(tmp, feature_path)
    except OSError as exc:
        tmp.unlink(missing_ok=True)
        raise WorkflowError(f"could not write {feature_path.name}: {exc}") from None
    return line


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root")
    ap.add_argument("--feature-id", required=True)
    ap.add_argument("--task-id", required=True)
    ap.add_argument("--today", help="Override the date. For tests only.")
    args = ap.parse_args(argv)
    try:
        root = repo_root(args.repo_root)
        print(write(root, args.feature_id, args.task_id, today=args.today))
    except WorkflowError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

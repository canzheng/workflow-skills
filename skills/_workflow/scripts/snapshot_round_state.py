#!/usr/bin/env python3
"""Catch a round's UNINTENDED changes: snapshot before, diff after, refuse undeclared deltas.

The third failure class, and the one no other gate covers. The catalogue lint checks a finding is
written as a class; the reconciler checks every swept site was reached; the per-guard mutation checks a
guard binds. None of them can see a fix in one file silently invalidating something in another.

## The defect this exists for

On `bt:v1-f047`, gate 20's own remediation edited the findings document and thereby made section 8's
`checks run: 124` false. Nothing was watching, so it surfaced as gate 21 -- a whole round spent on a
change the previous round had made and not looked at. Same shape as a skill documenting a `--require-blocks`
flag after the flag was cut: the fix was correct, its consequence elsewhere was not examined.

## How it works

  - `--baseline`, BEFORE implementing: run every declared command and record its output.
  - `--check`, AFTER: run them again and diff. Every difference must be ACKNOWLEDGED. An unacknowledged
    difference is, by definition, a change the round made without deciding to.

Acknowledgement is deliberately after-the-fact rather than predicted: you do not have to enumerate what
you intend to move, you have to LOOK at what moved. The value is exhaustiveness, not foresight.

## Noise is discovered, not configured

Command output carries timestamps, durations, temp paths and unstable ordering. The usual fix is
per-command regex filters -- configuration that rots silently and that nobody re-verifies, so the day it
stops matching is the day the snapshot stops covering.

Instead each command runs TWICE at baseline and any line differing between the two runs is dropped as
nondeterministic. The tool discovers its own noise floor. Two consequences worth stating:

  - a command whose output is ENTIRELY unstable contributes nothing, and is reported as such rather than
    being allowed to look like coverage. An empty snapshot and a clean snapshot print differently.
  - the noise floor is measured on THIS machine at THIS moment, so it is honest about what it covers and
    makes no claim about a line that happened to be stable across two runs and is not stable in general.

## The polarity, and how it meets test-first

This and the test-first obligation at `(b)` are ONE observation with opposite polarity, over two sets
that must be disjoint and jointly exhaustive:

  - the fix's own check MUST MOVE (fail -> pass). Movement is the evidence.
  - everything else MUST NOT MOVE. Stillness is the evidence.

An observable in NEITHER set is unwatched, and that gap is where the next round's finding lives. A pure
refactor is not a third case: it is this tool with an empty acknowledgement list.

The two meet at the acknowledgements. A test written test-first WILL appear here as a delta -- a new
test, going fail to pass -- and is acknowledged as that finding's fix-proof. So the lists reconcile:
every acknowledged delta should correspond to a finding. An acknowledged delta with no finding behind it
is work the round did without deciding to, which is this tool's own subject matter one level up.

## Choosing the commands

Do not invent the set. It is: every checker the round would already run at `(c)`, plus anything that
READS the artifacts the round touches.

READERS, NOT PRODUCERS -- and this is why the gate is cheap rather than a cost risk. A command that
reads derived state (a numbers verifier over persisted artifacts, a consistency checker, an inventory)
costs milliseconds; a command that PRODUCES state (a refit, an artifact regeneration, the suite) costs
minutes. The producers are also the wrong members: regeneration is the FIX, not the check, and the suite
is the least valuable member for the reasons below. So the cost criterion and the value criterion select
the same commands. Measured on `bt:v1-f047`'s real set -- numbers verifier, tracked-file inventory,
artifact inventory -- a full baseline is 0.4s for 1013 watched lines, 98% of it the verifier. Typically the test suite (name-level, never a tally), the schema
validators, the repo's record-consistency checker, and a tracked-file listing.

THE TEST SUITE IS THE LEAST VALUABLE MEMBER OF THE SET. Snapshotting it adds only two things over
RUNNING it, which `(c)` already does: a removed or renamed test (the suite stays green), and a change in
the COMPOSITION of a pre-existing failure set while its tally holds. Everything else it would report is
reported by the suite going red. The value of this tool lives in the commands that read surfaces the
suite cannot -- a numbers verifier, a doc-consistency checker, an artifact inventory. If the suite is
the only thing in the set, do not build this.

The set has a coverage property, and it is testable by PERTURBATION rather than by judgement: for each
file the round changed, make a trivial edit and re-run the set. If no command's output moves, that file
is outside the snapshot's reach and this tool is structurally blind to everything done there. Run the
control WITH THE SUITE EXCLUDED -- perturbing any source file moves the suite's output, so leaving it in
makes every surface look covered and the control reports nothing. Run it once when establishing the set
for a repo, not every round.

## When NOT to use it

Its value is proportional to how much of the deliverable lies OUTSIDE the test suite. A good suite
already answers "did this fix break something" for behavioural change; this adds coverage for documents,
generated artifacts, reports, counts and cross-references. On `bt:v1-f047` -- a research deliverable of
prose plus parquet -- `pytest` watched almost none of the blast radius, and gate 20's edit to a document
surfaced as gate 21. In a pure code repo with strong tests it is largely redundant with running the
suite, and running it there buys ceremony.

## Why TDD does not cover this

Test-first produces a test for the defect being FIXED. This class is damage to something the author was
not thinking about, so by construction there is no test they would have thought to write. TDD's coverage
is scoped to the author's model of the change; this is scoped to the project's observable surface, and
the defects that generate extra rounds are precisely the ones outside that model.

## What it is not

It does not decide whether a delta is good. It decides whether anyone LOOKED. Deciding is the round's
job, which is why acknowledgement carries a required reason.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

ALLOWED = {"pytest", "python", "python3", "grep", "rg", "git", "find", "fd", "ls", "openspec", "make", "npm", "cargo", "go"}
FORBIDDEN = re.compile(r"[|;&`><]|\$\(")
TIMEOUT_S = 1800


class Fail(Exception):
    pass


def run(cmd: str, repo: Path) -> list[str]:
    if FORBIDDEN.search(cmd):
        raise Fail(f"command uses shell metacharacters, which are not executed: {cmd!r}")
    try:
        argv = shlex.split(cmd)
    except ValueError as exc:
        raise Fail(f"command does not parse as a command line ({exc}): {cmd!r}")
    if not argv:
        raise Fail(f"empty command: {cmd!r}")
    if Path(argv[0]).name not in ALLOWED:
        raise Fail(f"{argv[0]!r} is not in the allowlist {sorted(ALLOWED)}. The allowlist bounds "
                   f"ACCIDENTS, not a hostile author; widen it in the source if the tool is legitimate.")
    try:
        p = subprocess.run(argv, cwd=repo, capture_output=True, text=True, timeout=TIMEOUT_S)
    except FileNotFoundError:
        raise Fail(f"{argv[0]!r} not found on PATH from {repo}. Snapshot commands must name the "
                   f"interpreter the repo actually uses (a conda env's python is not the ambient one).")
    except subprocess.TimeoutExpired:
        raise Fail(f"command timed out after {TIMEOUT_S}s: {cmd!r}")
    return [f"[exit {p.returncode}]"] + ((p.stdout or "") + (p.stderr or "")).splitlines()


ELAPSED: dict[str, float] = {}


def timed(cid: str, cmd: str, repo: Path) -> list[str]:
    t0 = time.monotonic()
    out = run(cmd, repo)
    ELAPSED[cid] = ELAPSED.get(cid, 0.0) + (time.monotonic() - t0)
    return out


def cost_report(label: str, budget: float | None) -> int:
    """Print what this gate cost, per command. A gate that does not report its own price gets adopted
    on the assumption it is free, and is then discovered to be expensive at the worst moment -- which is
    how the per-finding `fixed_when` gate died. The budget is set by what it is preventing: a review
    round costs tens of minutes, so seconds are free and minutes deserve an argument."""
    if not ELAPSED:
        return 0
    total = sum(ELAPSED.values())
    print(f"\n  cost ({label}): {total:.1f}s over {len(ELAPSED)} command(s)")
    for cid, t in sorted(ELAPSED.items(), key=lambda kv: -kv[1]):
        share = f"{100*t/total:.0f}%" if total else "n/a"
        print(f"    {cid:<24}{t:>7.1f}s  {share}")
    if budget is not None and total > budget:  # MUT:over_budget
        print(f"\nERROR: {total:.1f}s exceeds the {budget:.0f}s budget. Either drop the command "
              f"carrying most of it, or raise --max-seconds deliberately -- an unpriced gate is one "
              f"nobody re-examines.", file=sys.stderr)
        return 1
    return 0


def load_commands(path: Path) -> dict:
    """`{id: command}` from a JSON file, or from a ```json block in a markdown catalogue."""
    text = path.read_text()
    if path.suffix == ".json":
        doc = json.loads(text)
    else:
        blocks = re.findall(r"^```json[^\n]*\n(.*?)^```", text, re.M | re.S)
        if len(blocks) != 1:
            raise Fail(f"{path}: found {len(blocks)} ```json blocks; expected exactly one carrying "
                       f'{{"snapshot": {{"<id>": "<command>", ...}}}}')
        doc = json.loads(blocks[0])
    cmds = doc.get("snapshot")
    if not isinstance(cmds, dict) or not cmds:
        raise Fail(f"{path}: no non-empty `snapshot` mapping of id -> command")
    for k, v in cmds.items():
        if not isinstance(v, str) or not v.strip():
            raise Fail(f"{path}: snapshot[{k!r}] must be a command string")
    return cmds


def stable_lines(cid: str, cmd: str, repo: Path) -> tuple[list[str], int]:
    """The deterministic content of `cmd`: lines present in BOTH of two consecutive runs.

    Run twice on BOTH sides of the round, not just at baseline. Denoising only the baseline is wrong in
    a way that looks right: a timestamp emitted at check time has no counterpart in the baseline's
    stable set, so it registers as an APPEARED line and manufactures exactly the delta the calibration
    exists to suppress. Every command would then report a delta forever, the tool would be ignored, and
    it would have been the noise filter that broke it. Symmetric or nothing.

    `SequenceMatcher` keeps position, so a line that merely MOVED between runs is not counted stable.
    """
    a, b = timed(cid, cmd, repo), timed(cid, cmd, repo)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    stable = [x for tag, i1, i2, _, _ in sm.get_opcodes() if tag == "equal" for x in a[i1:i2]]
    return stable, len(a) - len(stable)


def baseline(cmds: dict, repo: Path, state: Path) -> int:
    rec, dead = {}, []
    for cid, cmd in sorted(cmds.items()):
        stable, noise = stable_lines(cid, cmd, repo)
        a = stable + [""] * noise          # only its length is used, for the report
        rec[cid] = {"command": cmd, "stable": stable, "noise_lines": noise, "raw_lines": len(a)}
        # Deadness is judged on CONTENT, excluding the synthetic `[exit N]` line `run()` prepends.
        # That line is stable for every command ever written, so counting it made the emptiness check
        # unable to fire on any input -- a guard that cannot fail, inside the tool built around not
        # shipping those. It stays in the COMPARISON, where an exit-code flip is a real delta.
        if not [l for l in stable if not l.startswith("[exit ")]:  # MUT:baseline_no_stable
            dead.append(f"{cid}: no line was stable across two runs, so this command contributes "
                        f"NOTHING to the comparison. A snapshot that cannot differ is not coverage.")
            print(f"  {cid:<24} DEAD   0 stable of {len(a)} lines")
        else:
            print(f"  {cid:<24} ok     {len(stable)} stable, {noise} nondeterministic")
    state.write_text(json.dumps({"mode": "baseline", "commands": rec}, indent=2))
    if dead:
        print("\n" + "\n".join(f"ERROR: {d}" for d in dead), file=sys.stderr)
        return 1
    total = sum(len(v["stable"]) for v in rec.values())
    print(f"\nOK: {len(rec)} command(s), {total} stable lines recorded to {state}. "
          f"Implement now, then re-run with --check.")
    return 0


def check(cmds: dict, repo: Path, state: Path, acks: dict) -> int:
    if not state.exists():
        raise Fail(f"no baseline at {state}. A check run alone cannot tell a change from a constant.")
    base = json.loads(state.read_text()).get("commands", {})
    missing = sorted(set(base) - set(cmds))
    added = sorted(set(cmds) - set(base))
    problems = []
    if missing:  # MUT:check_command_dropped
        problems.append(f"command(s) {missing} were baselined and are no longer declared. Dropping a "
                        f"snapshot command after the fact removes the evidence rather than the change.")
    if added:
        print(f"  note: {added} added since baseline; they have no before-state and are not compared")

    for cid in sorted(set(cmds) & set(base)):
        if base[cid]["command"] != cmds[cid]:  # MUT:check_command_edited
            problems.append(f"{cid}: command changed since baseline "
                            f"({base[cid]['command']!r} -> {cmds[cid]!r}); the two outputs are not "
                            f"comparable and the diff would be meaningless.")
            print(f"  {cid:<24} BAD    command edited")
            continue
        # ONE run in the common case. The second run exists only to denoise, and denoising can only
        # SHRINK a delta -- so when the single run already matches the baseline there is nothing a
        # second could change. Paying for symmetric denoising on every command every round, when most
        # commands do not move in most rounds, is the cost profile that made the previous gate
        # unaffordable; this pays it only where something actually moved.
        before = base[cid]["stable"]
        now = timed(cid, cmds[cid], repo)
        beforeset = set(before)
        gone = [l for l in before if l not in set(now)]
        appeared = [l for l in now if l not in beforeset and l != ""]
        if gone or appeared:
            now, _ = stable_lines(cid, cmds[cid], repo)   # denoise, same as the baseline side
            nowset = set(now)
            gone = [l for l in before if l not in nowset]
            appeared = [l for l in now if l not in beforeset and l != ""]
        delta = [f"-{l}" for l in gone] + [f"+{l}" for l in appeared]
        if not delta:
            print(f"  {cid:<24} same")
            continue
        reason = acks.get(cid)
        if not reason:  # MUT:check_unacknowledged
            problems.append(f"{cid}: {len(gone)} line(s) gone, {len(appeared)} appeared, and the round "
                            f"did not acknowledge it. This is a change the round made without deciding "
                            f"to.\n" + "\n".join("        " + d for d in delta[:12]) +
                            (f"\n        ... {len(delta)-12} more" if len(delta) > 12 else ""))
            print(f"  {cid:<24} DELTA  -{len(gone)} +{len(appeared)}  UNACKNOWLEDGED")
        else:
            print(f"  {cid:<24} DELTA  -{len(gone)} +{len(appeared)}  acknowledged: {reason}")

    stale = sorted(set(acks) - set(cmds))
    if stale:  # MUT:check_stale_ack
        problems.append(f"acknowledgement(s) for {stale} match no declared command -- an --accept that "
                        f"silences nothing reads as a decision that was made.")
    if problems:
        print("\n" + "\n".join(f"ERROR: {p}" for p in problems), file=sys.stderr)
        return 1
    print(f"\nOK: every delta is acknowledged with a reason; nothing moved unexamined.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Snapshot project state around a remediation round.")
    ap.add_argument("commands", help="JSON file, or markdown with one ```json block, giving {snapshot: {id: cmd}}")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--max-seconds", type=float, default=None,
                    help="fail if the gate's own runtime exceeds this. Set it; an unpriced gate is one "
                         "nobody re-examines.")
    ap.add_argument("--accept", action="append", default=[], metavar="ID=REASON",
                    help="acknowledge this command's delta, with why. Repeatable.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--baseline", action="store_true")
    g.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    try:
        acks = {}
        for s in a.accept:
            if "=" not in s or not s.split("=", 1)[1].strip():
                raise Fail(f"--accept must be ID=REASON with a non-empty reason, got {s!r}. An "
                           f"acknowledgement without a reason is a silencer, not a decision.")
            k, v = s.split("=", 1)
            acks[k.strip()] = v.strip()
        cmds = load_commands(Path(a.commands))
        repo = Path(a.repo).resolve()
        if not (repo / ".git").exists():
            raise Fail(f"{repo} is not a repo root (no .git)")
        print(f"{'baseline' if a.baseline else 'check'}: {len(cmds)} command(s)")
        if a.baseline:
            if acks:
                raise Fail("--accept is meaningless at baseline; there is nothing to acknowledge yet")
            rc = baseline(cmds, repo, Path(a.state))
            return max(rc, cost_report("baseline", a.max_seconds))
        rc = check(cmds, repo, Path(a.state), acks)
        return max(rc, cost_report("check", a.max_seconds))
    except Fail as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

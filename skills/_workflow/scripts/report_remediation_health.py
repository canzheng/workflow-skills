#!/usr/bin/env python3
"""Measure whether a feature's remediation loop is converging or multiplying.

The question this answers is the one that started the work: `bt:v1-f047` took 23 remediation rounds, and
the count alone did not say whether that was a hard feature or a bad process. Hand-counting the commit
subjects afterwards showed at least 14 of 23 named a PREVIOUS round's fix as their subject -- ~6 defect
CLASSES spread over 23 rounds. That number is the diagnosis, and it was only available in hindsight.

Now that the catalogue schema is machine-readable, it is available DURING the loop.

## The metrics, and which one to watch

- SELF-INFLICTED RATE -- findings attributed to an earlier round's fix, over all findings. This is the
  multiplication rate. On `v1-f047` it was ~60% counted by hand. A loop where most findings are the
  previous fix's fault is not converging, and the fix is to slow down on the FIX, not on the finding.
- SIBLING SITES CAUGHT -- class sweeps that found MORE THAN ONE site. This is the leading indicator and
  the one to actually watch: each extra site is a round that did NOT happen, because the shape was fixed
  everywhere at once instead of being rediscovered one file over. On `v1-f047` this was structurally
  zero -- no sweep existed -- and gates 10/11, 14/15 and 19/20 are each a pair that a sweep would have
  collapsed into one round.
- SINGLE-SITE RATE -- how often authors take the escape hatch. High is a smell: gate 14 declared its
  defect single-site ("it's the T9 driver") and gate 15 found it in a second caller.
- SUBSTITUTE COVERAGE -- guard findings carrying a substitute mutant. The revert-only guards are the ones
  that pass against a plausible wrong implementation.

## What this does NOT measure

Whether the findings were RIGHT, or whether a round was worth running. It reads what the catalogue
claims. A catalogue that lies passes this cleanly -- which is why the lint gates the catalogue and this
only reports on it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required", file=sys.stderr)
    raise SystemExit(2)

BLOCK_RE = re.compile(r"^[ \t]*```[ \t]*(?:yaml|yml)[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.S | re.M | re.I)
PRIOR_FIX_RE = re.compile(r"\bgate[-\s]?\d+\b|\bprevious round\b|\bearlier round\b", re.I)


def load(path: Path) -> list[dict]:
    blocks = BLOCK_RE.findall(path.read_text(encoding="utf-8", errors="replace"))
    if len(blocks) != 1:
        return []
    try:
        doc = yaml.safe_load(blocks[0])
    except yaml.YAMLError:
        return []
    if not isinstance(doc, dict):
        return []
    f = doc.get("findings")
    return [x for x in f if isinstance(x, dict)] if isinstance(f, list) else []


def gate_num(p: Path) -> int:
    m = re.search(r"gate-(\d+)", p.name)
    return int(m.group(1)) if m else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("remediation_dir", help="openspec/changes/<id>/remediation/")
    ap.add_argument("--glob", default="gate-*.md")
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)

    root = Path(args.remediation_dir)
    if not root.is_dir():
        print(f"ERROR: not a directory: {root}", file=sys.stderr)
        return 1
    files = sorted((p for p in root.rglob(args.glob) if p.is_file()), key=gate_num)
    if not files:
        print(f"ERROR: no files matching {args.glob!r} under {root}", file=sys.stderr)
        return 1

    rows, tot = [], {"n": 0, "self": 0, "sib": 0, "single": 0, "sweeps": 0, "guards": 0, "sub": 0}
    for p in files:
        fs = load(p)
        r = {"gate": p.name, "n": len(fs), "self": 0, "sib": 0, "single": 0, "guards": 0, "sub": 0}
        for f in fs:
            if PRIOR_FIX_RE.search(str(f.get("attribution", ""))):
                r["self"] += 1
            cs = f.get("class_sweep") or {}
            if isinstance(cs, dict):
                if "single_site" in cs:
                    r["single"] += 1
                else:
                    tot["sweeps"] += 1
                    sites = cs.get("sites")
                    if isinstance(sites, list) and len(sites) > 1:
                        r["sib"] += 1
            if f.get("guard") is True:
                r["guards"] += 1
                m = f.get("mutants") or {}
                if isinstance(m, dict) and str(m.get("substitute", "")).strip():
                    r["sub"] += 1
        rows.append(r)
        for k in ("n", "self", "sib", "single", "guards", "sub"):
            tot[k] += r[k]

    print(f"{'gate':<16}{'findings':>9}{'self-inflicted':>16}{'sibling sites':>15}{'single-site':>13}")
    for r in rows:
        print(f"{r['gate']:<16}{r['n']:>9}{r['self']:>16}{r['sib']:>15}{r['single']:>13}")
    n = tot["n"]
    if not n:
        print("\nNo findings parsed. Either the catalogues predate the yaml schema, or they do not "
              "carry exactly one ```yaml block each.")
        return 0
    pct = lambda x, d=n: f"{100*x/d:.0f}%" if d else "n/a"
    print(f"\n{len(files)} rounds, {n} findings")
    print(f"  self-inflicted        {tot['self']:>3} / {n}  ({pct(tot['self'])})  "
          f"-- findings caused by an earlier round's fix; the multiplication rate")
    print(f"  sweeps finding >1 site {tot['sib']:>2} / {tot['sweeps']}  "
          f"({pct(tot['sib'], tot['sweeps'])})  -- each extra site is a round that did NOT happen")
    print(f"  single-site claimed   {tot['single']:>3} / {n}  ({pct(tot['single'])})  "
          f"-- the escape hatch; high is a smell")
    print(f"  substitute coverage   {tot['sub']:>3} / {tot['guards']}  "
          f"({pct(tot['sub'], tot['guards'])})  -- guards proven against a wrong implementation")

    if tot["self"] > n / 2:
        print("\nWARNING: most findings are the previous fix's fault. The finding rate is not the "
              "problem; the FIX quality is. Slow down on (b), not on the review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

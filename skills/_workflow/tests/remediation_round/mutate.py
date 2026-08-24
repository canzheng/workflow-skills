#!/usr/bin/env python3
"""Disable ONE tagged check in the lint, by `# MUT:<tag>` comment rather than by source text.

Anchoring a mutant on literal source means a behaviour-preserving refactor turns the corpus red, and
the pressure that creates is to re-point the anchor -- which is how a mutant quietly comes to test
nothing. A tag survives refactors, and a MISSING tag is a hard failure rather than a skipped check.
"""
import sys
from pathlib import Path

src, dst, tag = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
lines = src.read_text().splitlines()
hits = [i for i, l in enumerate(lines) if l.rstrip().endswith(f"# MUT:{tag}")]
if not hits:
    print(f"no '# MUT:{tag}' tag in {src.name}", file=sys.stderr)
    raise SystemExit(1)
if len(hits) > 1:
    # Mutating one of N identically-tagged sites leaves the others live, so the "mutant" tests less
    # than it claims -- the quiet way a mutant comes to test nothing.
    print(f"tag '{tag}' appears {len(hits)} times; tags must be unique", file=sys.stderr)
    raise SystemExit(1)
i = hits[0]
ind = len(lines[i]) - len(lines[i].lstrip())
body = lines[i].lstrip()
lines[i] = " " * ind + ("return False  # MUT" if body.startswith("return") else "if False:  # MUT")
dst.write_text("\n".join(lines) + "\n")

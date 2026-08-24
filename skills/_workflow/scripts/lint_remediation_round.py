#!/usr/bin/env python3
"""Lint a remediation-round catalogue for the two things that make rounds multiply.

WHY THIS EXISTS, measured on `bt:v1-f047` (23 remediation rounds, ~16 hours): 6 rounds moved a published
number, but at least 14 of the 23 name a PREVIOUS round's fix as their subject. Grouped by defect CLASS
rather than by round, ~6 classes were spread over 23 rounds -- the reviewer named ONE instance, the round
fixed THAT instance, and the next review found the same shape one file over. Separately, SEVEN guards
written in those rounds could not discriminate, every one because the FIXTURE made the compared
quantities equal; the worst passed its revert mutant honestly while a plausible WRONG implementation also
passed. So a catalogue must carry, per finding, a CLASS SWEEP with a real command, and -- when the fix
adds a guard -- both a `revert:` and a distinct `substitute:` mutant, named BEFORE the guard is written.

## Why the findings are YAML and not prose

The first two versions of this lint hand-rolled a markdown parser, and both shipped false PASSes -- the
failure mode that is worse than having no gate, because it reports success:

  v1: a fenced ``` EXAMPLE of the schema parsed as a real finding, so a copy-pasted template satisfied
      the no-empty-catalogue check; the evidence test matched the WORD "grep" anywhere in the block, so
      "a grep would have been nice but I did not run one" passed; `-Finding:` and `* Finding:` were
      silently never linted while the run still reported every finding carried its keys.
  v2: fixed those, and grew four more of the same class -- a fence INSIDE a finding supplied every key
      (the copy-paste moved one indent level in); an unclosed fence silently swallowed all later
      findings; `CMD_RE` accepted prose that merely STARTED with a tool word; and bold/numbered finding
      lines (`- **Finding:** x`, `1. Finding: x`) were still silently ignored.

Every one of those is a PARSING defect, not a policy defect. Patching them is unbounded: markdown has
endless ways to write the same thing, and each patch moves the evasion one level in. So the schema is now
a single fenced ```yaml block parsed by `yaml.safe_load`. There is ONE way to express a finding, the
parser is not mine, a malformed block fails loudly instead of silently, and a schema example elsewhere in
the document is inert because it is not in the tagged block.

That is the same remedy the feature this was built from arrived at: do not police the many ways to
disagree -- remove the second way.

  v3: replaced the markdown parser with `yaml.safe_load` -- which removed the markdown PARSING class
      and relocated the same meta-class ("content a human sees is silently not linted, and the run
      reports success") into YAML's own permissive features. A review found eleven false PASSes: merge
      keys let ONE class_sweep satisfy N findings, a block scalar containing ``` truncated the block and
      dropped later findings, duplicate keys last-won, every value check was string-only so
      `mutants: {revert: 0, substitute: 1}` cleared required-ness AND placeholder AND distinctness at
      once, and `shape` -- the field naming the defect CLASS, the tool's whole premise -- was the one
      near-required field exempt from the placeholder check.

      The lesson worth carrying: `yaml.safe_load` is trustworthy as a PARSER and permissive as a
      VALIDATOR, and v3 treated the first property as if it implied the second. v4 keeps YAML and adds
      a strict loader (no merge keys, no duplicate keys), a CommonMark fence scanner (a ``` inside an
      indented block scalar is content, an unclosed fence is reported), and type-narrowed value checks.

## What is still policy, and therefore still mine to get right

Whether the class sweep names a real command, whether `substitute:` is genuinely a different edit from
`revert:`, and whether a field is a placeholder. Those are semantic and they have fixtures.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(2)

# --- extraction + loading: replaces BLOCK_RE, fixes F3/F10/F24 ------------------------------------
FENCE_OPEN_RE = re.compile(r"^(?P<ind>[ \t]{0,3})(?P<mark>`{3,}|~{3,})[ \t]*(?P<info>[^\s`]*)[^`]*$")
# A LOOSE detector for anything a reader would see as a yaml block, at any indent, through a blockquote,
# with an attribute list or in `{yaml}` form. It is not used to EXTRACT -- it is used to cross-check that
# the strict scanner treated every such opener as a block. v4 missed four spellings, and each one hid a
# second block containing findings that were then never linted while the run reported success.
LOOSE_YAML_FENCE_RE = re.compile(r"^[ \t>]*(?:`{3,}|~{3,})[ \t]*\{?(?:yaml|yml)\b", re.I | re.M)

def extract_blocks(text: str) -> list[tuple[str, bool]]:
    """Every fenced block tagged yaml/yml, using CommonMark fence rules rather than a regex.

    A regex that closes on the first bare ``` line is defeated by a YAML block scalar that CONTAINS
    one -- the block truncates, later findings vanish, and the file PASSES. That was the v3 defect and
    it is the same "content a human sees is silently not linted" class as v1's and v2's. Here a fence
    closes only on a marker of the SAME type, at least as long, and no more indented -- so a ``` inside
    an indented block scalar is content, and an unclosed fence runs to EOF and is reported.

    DELIBERATE DEVIATION FROM CommonMark (FF-3, reviewed and REJECTED -- do not "fix" it). CommonMark
    lets the closing fence be indented up to three spaces regardless of the opener's indent; this
    requires the closer to be no MORE indented than its opener. The spec rule would let a ``` sitting
    at indent 1-3 inside a block scalar close the block early -- truncating it, hiding every later
    finding, and PASSING. That is exactly the v3 defect this scanner replaced. The strict rule errs the
    other way: it reports a spec-legal closer as an unclosed fence, which FAILS loudly and is fixed by
    outdenting one line. A linter should be wrong in the direction that stops the file, not the
    direction that waves it through, so the deviation is the point rather than an oversight.
    """
    out, lines = [], text.splitlines()
    i, n = 0, len(lines)
    while i < n:
        m = FENCE_OPEN_RE.match(lines[i])
        if not m:
            i += 1
            continue
        ind, mark = len(m.group("ind")), m.group("mark")
        # `yaml linenums="1"` and `{yaml}` are the same block to a reader; take the first token and
        # strip the Quarto/RMarkdown braces rather than demanding a bare tag.
        info = m.group("info").lower().strip("{}").split()[0] if m.group("info").strip("{}") else ""
        char, need = mark[0], len(mark)
        body, i, closed = [], i + 1, False
        while i < n:
            c = FENCE_OPEN_RE.match(lines[i])
            if (c and c.group("mark")[0] == char and len(c.group("mark")) >= need
                    and len(c.group("ind")) <= ind and not c.group("info")):
                closed, i = True, i + 1
                break
            body.append(lines[i])
            i += 1
        if info in ("yaml", "yml"):  # MUT:fence_scanner
            out.append(("\n".join(body), closed))
    return out


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses the two features that let one finding stand in for several.

    `yaml.safe_load` is trustworthy as a PARSER and permissive as a VALIDATOR; v3 treated the first
    property as if it implied the second. Merge keys (`<<: *base`) let ONE class_sweep satisfy N
    findings -- the tool's own thesis defect, one instance reported as a class, in two lines. Duplicate
    keys silently last-win, so a `command: TBD` line above a real one disappears.
    """


def _no_duplicates(loader, node, deep=False):
    mapping = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        try:
            dup = key in mapping
        except TypeError:      # unhashable complex key (`? [a, b]`): a YAML error, not a crash
            raise yaml.YAMLError(f"unhashable key {key!r}; catalogue keys must be scalars")
        if dup:  # MUT:dup_keys
            raise yaml.YAMLError(f"duplicate key {key!r}; the later value would silently win")
        mapping[key] = loader.construct_object(v, deep=deep)
    return mapping


def _no_merge(loader, node):
    raise yaml.YAMLError("merge keys (`<<`) are not permitted: each finding must carry its own "
                         "class_sweep, or one sweep would stand in for several findings")


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates)
_StrictLoader.add_constructor("tag:yaml.org,2002:merge", _no_merge)


def _reject_aliases(body: str) -> str | None:
    """YAML has TWO mechanisms for one-node-N-references, and v4 blocked only merge keys.

    `class_sweep: &cs` / `class_sweep: *cs` makes one sweep stand in for three findings in two
    characters -- the tool's own thesis defect, one instance reported as a class. Rejected at the event
    level because an alias is resolved during construction and is invisible afterwards.
    """
    try:
        for ev in yaml.parse(body, Loader=yaml.SafeLoader):
            if isinstance(ev, yaml.AliasEvent):
                return (f"YAML alias `*{ev.anchor}`: each finding must carry its OWN class_sweep and "
                        f"mutants, or one node stands in for several findings")
    except yaml.YAMLError:
        return None          # the parse below reports it properly
    return None


# --- value quality ---------------------------------------------------------------------------------
# Deliberately small. Only properties decidable FROM THE STRING live here; everything about whether the
# string describes something that really happened is checked by executing it elsewhere.
PLACEHOLDER_RE = re.compile(r"^(?:tbd|todo|t\.b\.d\.?|n/?a|none|nil|null|\?+|-+|x{1,3}|foo|bar)$", re.I)

REQUIRED = ("id", "title", "attribution", "guard", "class_sweep")


class Issue:
    def __init__(self, path: Path, where: str, reason: str) -> None:
        self.path, self.where, self.reason = path, where, reason

    def render(self) -> str:
        return f"ERROR: {self.path}: {self.where}: {self.reason}"


def _clean_text(v: str) -> str:
    """NFKC-fold and strip zero-width characters before any value check (F11).

    `.strip()` does not remove U+200B, and `ＴＢＤ` is not `TBD` to a byte comparison, so both slipped
    past every placeholder check in v3.
    """
    t = v
    if True:  # MUT:zerowidth
        t = re.sub(r"[\u00ad\u200b-\u200f\u2060\ufeff]", "", t)
    return unicodedata.normalize("NFKC", t).strip()


def _blank(v) -> bool:
    """True for absent, non-string, or empty.

    NON-STRING COUNTS AS BLANK (F6). In v3 every value check was string-only, so `attribution: []`,
    `title: {}` and `mutants: {revert: 0, substitute: 1}` cleared required-ness, placeholder AND
    distinctness at once. A field that must read as prose must BE prose.
    """
    if v is None:
        return True
    if not isinstance(v, str):
        return True
    return not _clean_text(v)


def _placeholder(v) -> bool:
    if not isinstance(v, str):
        return False
    # NOT CHECKED HERE: `<...>` template slots. v3's detector rejected `a < b and c > d` and
    # `Optional<str>`; narrowing it to "slot must contain whitespace" then passed `<id>`, `<path>` and
    # `<...>`, so a fully unfilled template linted clean -- v1's headline defect, restored. Broad
    # catches real content, narrow misses slots; the rule itself is the problem, not its width.
    # An unfilled `command:` slot is caught by RUNNING it (see reconcile_remediation_sites.py).
    return bool(PLACEHOLDER_RE.match(_clean_text(v)))  # MUT:placeholder


def _norm(v: str) -> str:
    return re.sub(r"\W+", "", str(v)).lower()


def _check_sweep(sweep, where: str, path: Path, out: list[Issue]) -> None:
    if not isinstance(sweep, dict):
        out.append(Issue(path, where, "`class_sweep` must be a mapping with either "
                                      "`shape`+`command`+`sites`, or `single_site`+`command`"))
        return
    unknown = set(sweep) - {"shape", "command", "sites", "single_site"}
    if unknown:  # MUT:sweep_unknown
        out.append(Issue(path, where, f"`class_sweep` has unknown key(s) {sorted(map(str, unknown))} -- a typo "
                                      f"here silently drops the field it was meant to be"))
    cmd = sweep.get("command")
    if _blank(cmd):
        out.append(Issue(path, where, "`class_sweep.command` is required -- paste the search you RAN. "
                                      "Naming a tool in prose is not evidence that it ran"))
    elif _placeholder(cmd):
        out.append(Issue(path, where, f"`class_sweep.command` is a placeholder ({cmd!r})"))
    # NOT CHECKED HERE: whether this string is really a command, or really ran. Three mechanisms tried
    # and all three failed in both directions -- a word match, a leading-token match, and a stopword
    # heuristic. The last rejected `rg -n "is None" src/` because `is` and `None` are function words,
    # in a lint that gates sweeps OF SOURCE CODE. The author's rational response is to edit the command
    # until the linter accepts it, at which point the recorded command is no longer the command that
    # ran -- destroying the only property the field exists to preserve.
    # "Did it run?" is not decidable from a string. It IS decidable by RUNNING it, which is what
    # `reconcile_remediation_sites.py` does against the declared sites.
    single = "single_site" in sweep
    if single:
        if _blank(sweep["single_site"]) or _placeholder(sweep["single_site"]):
            out.append(Issue(path, where, "`class_sweep.single_site` must state WHY the shape cannot "
                                          "recur elsewhere"))
        elif len(_clean_text(str(sweep["single_site"])).split()) < 4:
            out.append(Issue(path, where, "`class_sweep.single_site` must be a REASON, not a token"))
        if "shape" in sweep:
            out.append(Issue(path, where, "`class_sweep` declares both `single_site` and `shape`; "
                                          "`single_site` replaces the shape, use one"))
    elif _blank(sweep.get("shape")) or _placeholder(sweep.get("shape")):
        out.append(Issue(path, where, "`class_sweep.shape` is required -- name the DEFECT SHAPE, not "
                                      "this instance (or use `single_site` with a reason)"))
    sites = sweep.get("sites")
    bad_sites = (not isinstance(sites, list) or not sites
                 or any(_blank(x) or _placeholder(x) for x in sites))
    # A tagged condition must fit on ONE line: the mutator replaces a single line, so a wrapped
    # condition would leave its continuation orphaned and the "mutant" would be a SyntaxError.
    if bad_sites:  # MUT:sites_required
        out.append(Issue(path, where, "`class_sweep.sites` is required and must be a non-empty list -- "
                                      "list every site the command found. Reconciliation is per SITE, "
                                      "so a finding with no sites would escape it"))
    # NOT CHECKED HERE (O-5, reviewed): the SHAPE of a site string, and "a class claim must list more
    # than one site". The first is decided by RUNNING the command -- `reconcile_remediation_sites.py`
    # matches every declared site against what the command found and against `git diff --name-only`, so
    # `sites: ["aaa"]` fails there, where the check has evidence. The second is refused on purpose: a
    # swept class can honestly have exactly one site, and requiring two would push the author to pad
    # the list or to take the `single_site` escape hatch -- both strictly worse than a truthful count.
    # The ratio is REPORTED instead (`report_remediation_health.py`, "sweeps finding >1 site"), where a
    # low value is a smell to read rather than a rule to satisfy.
    elif single and len(sites) != 1:  # MUT:single_site_cardinality
        out.append(Issue(path, where, f"`single_site` claims one site but `sites` lists {len(sites)}; "
                                      f"if the shape recurs, drop `single_site` and name the shape"))


def _check_mutants(mut, where: str, path: Path, out: list[Issue]) -> None:
    if not isinstance(mut, dict):
        out.append(Issue(path, where, "`guard: true` requires `mutants:` with `revert:` and "
                                      "`substitute:`"))
        return
    unknown = set(mut) - {"revert", "substitute"}
    if unknown:
        out.append(Issue(path, where, f"`mutants` has unknown key(s) {sorted(map(str, unknown))}"))
    rev, sub = mut.get("revert"), mut.get("substitute")
    if _blank(rev):  # MUT:revert_required
        out.append(Issue(path, where, "`mutants.revert` is required -- undo the behaviour; proves the "
                                      "test binds at all"))
    if _blank(sub):
        out.append(Issue(path, where,
                         "`mutants.substitute` is required -- name the most plausible WRONG "
                         "implementation. A revert proves the test binds to SOMETHING; only a "
                         "substitute proves it binds to the RIGHT thing, and a fixture that cannot "
                         "separate them cannot make it fail"))
    for name, val in (("revert", rev), ("substitute", sub)):
        if not _blank(val) and _placeholder(val):
            out.append(Issue(path, where, f"`mutants.{name}` is a placeholder ({val!r})"))
    # WHAT THIS VERIFIES: the two strings are identical after folding case, punctuation and space.
    # Nothing more. A REWORDED restatement ("drop the call" / "remove the call") passes, and no string
    # comparison can decide otherwise -- see the `command` note above for the same boundary. The
    # message therefore states what was found, and states the requirement separately as a requirement,
    # rather than implying the checker established the substitute is genuinely different.
    if not _blank(rev) and not _blank(sub) and _norm(rev) == _norm(sub):  # MUT:restates
        out.append(Issue(path, where,
                         "`mutants.substitute` is the same string as `mutants.revert` once case, "
                         "punctuation and whitespace are folded. The substitute is REQUIRED to be a "
                         "different, plausible wrong implementation: a revert proves the guard binds "
                         "to the behaviour's presence, only a substitute proves it binds to the right "
                         "thing. (This check catches verbatim restatement only -- a reworded "
                         "restatement passes it and is still a defect.)"))


def lint_file(path: Path, *, allow_empty: bool) -> tuple[list[Issue], int]:
    out: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [Issue(path, "file", f"cannot decode as UTF-8 ({exc.reason})")], 0
    if "\x00" in text:
        return [Issue(path, "file", "contains NUL bytes; not a text catalogue")], 0

    blocks = extract_blocks(text)
    loose = len(LOOSE_YAML_FENCE_RE.findall(text))
    if loose > len(blocks):  # MUT:loose_fence
        out.append(Issue(path, "file", f"{loose} yaml-tagged fence(s) are visible in this file but the "
                                       f"scanner recognised {len(blocks)}; one is indented, inside a "
                                       f"blockquote, or otherwise not a top-level block, and anything "
                                       f"in it would never be linted"))
    # F7: `--allow-empty` used to disable this too, so a catalogue that never adopted the schema
    # reported clean -- the v1/v2 prose failure mode, reachable by a flag. The flag now permits an
    # empty findings LIST and nothing else; a missing block is always an error.
    if not blocks:
        out.append(Issue(path, "file", "no ```yaml findings block. A catalogue must carry exactly one, "
                                       "listing every finding from the gate"))
        return out, 0
    if len(blocks) > 1:  # MUT:two_blocks
        out.append(Issue(path, "file", f"{len(blocks)} ```yaml blocks; expected exactly one so nothing "
                                       f"can hide in a second (quote the schema in an UNTAGGED fence)"))
        return out, 0
    body, closed = blocks[0]
    if not closed:
        out.append(Issue(path, "file", "the ```yaml fence is never closed; everything after it is "
                                       "inside the block and nothing later in the file is linted"))

    alias = _reject_aliases(body)
    if alias:  # MUT:alias
        return out + [Issue(path, "yaml", alias)], 0
    try:
        doc = yaml.load(body, Loader=_StrictLoader)
    except yaml.YAMLError as exc:
        return out + [Issue(path, "yaml", f"block does not parse: {str(exc).splitlines()[0]}")], 0

    if not isinstance(doc, dict) or "findings" not in doc:
        out.append(Issue(path, "yaml", "block must be a mapping with a top-level `findings:` list"))
        return out, 0
    findings = doc["findings"]
    if findings is None or (isinstance(findings, list) and not findings):
        if not allow_empty:
            out.append(Issue(path, "findings", "list is empty; a gate that passes an empty catalogue "
                                               "is not a gate (use --allow-empty deliberately)"))
        return out, 0
    if not isinstance(findings, list):
        out.append(Issue(path, "findings", "must be a list"))
        return out, 0

    seen: set[str] = set()
    for i, f in enumerate(findings, start=1):
        where = f"findings[{i}]"
        if not isinstance(f, dict):
            out.append(Issue(path, where, "each finding must be a mapping"))
            continue
        where = f"findings[{i}] ({f.get('id') or f.get('title') or '?'})"
        unknown = set(f) - set(REQUIRED) - {"mutants", "notes"}
        if unknown:
            out.append(Issue(path, where, f"unknown key(s) {sorted(map(str, unknown))} -- a typo "
                                          f"silently drops the field it was meant to be"))
        for k in REQUIRED:
            if k not in f:
                out.append(Issue(path, where, f"missing `{k}`"))
            elif k not in ("guard", "class_sweep") and (_blank(f[k]) or _placeholder(f[k])):  # MUT:field_quality
                out.append(Issue(path, where, f"`{k}` must be non-empty text, not {f[k]!r}"))
        if "id" in f and not _blank(f["id"]):
            key = _clean_text(str(f["id"]))
            if key in seen:
                out.append(Issue(path, where, f"duplicate finding id {key!r}"))
            seen.add(key)
        if "guard" in f and not isinstance(f["guard"], bool):  # MUT:guard_bool
            out.append(Issue(path, where, f"`guard` must be a YAML boolean (true/false), got "
                                          f"{f['guard']!r}"))
        if "class_sweep" in f:
            _check_sweep(f["class_sweep"], where, path, out)
        # `mutants` is examined whenever it is PRESENT, not only when `guard is True`. Under the old
        # `if guard is True: ... elif "mutants" in f and guard is False:` chain, a finding with a
        # non-bool or missing `guard` reported only the guard error and left a bogus `mutants` block
        # unread -- so fixing the guard surfaced a second, previously-invisible error, which is a round.
        # A gate that reveals its findings one repair at a time is the defect this whole file exists
        # to remove; it must not contain an instance of it.
        mut = f.get("mutants")
        if f.get("guard") is True and mut is None:  # MUT:mutants_required
            out.append(Issue(path, where, "`guard: true` requires `mutants:` with `revert:` and "
                                          "`substitute:`"))
        if mut is not None:
            _check_mutants(mut, where, path, out)
            if f.get("guard") is not True:  # MUT:mutants_without_guard
                out.append(Issue(path, where, "`mutants` given without `guard: true`; set `guard: true` "
                                              "or drop the mutants"))
    return out, len(findings)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint a remediation-round catalogue.")
    ap.add_argument("target", help="A remediation gate file, or a remediation/ directory.")
    ap.add_argument("--allow-empty", action="store_true",
                    help="Permit a catalogue with no findings (default: an error, because a gate that "
                         "passes an empty catalogue is not a gate).")
    ap.add_argument("--glob", default="gate-*.md", help="Filename pattern in directory mode.")
    args = ap.parse_args(sys.argv[1:] if argv is None else argv)

    target = Path(args.target)
    if not target.exists():
        print(f"ERROR: not found: {target}", file=sys.stderr)
        return 1
    files = [p for p in sorted(target.rglob(args.glob)) if p.is_file()] if target.is_dir() else [target]
    if not files:
        print(f"ERROR: no files matching {args.glob!r} under {target}", file=sys.stderr)
        return 1

    issues: list[Issue] = []
    total = 0
    for f in files:
        found, n = lint_file(f, allow_empty=args.allow_empty)
        issues.extend(found)
        total += n
    if issues:
        for it in issues:
            print(it.render(), file=sys.stderr)
        print(f"\n{len(issues)} issue(s) across {len(files)} file(s), {total} finding(s) parsed. "
              f"The catalogue gates implementation: fix these before step (b).", file=sys.stderr)
        return 1
    if total == 0:
        print(f"OK: {len(files)} file(s), 0 findings (--allow-empty)")
        return 0
    # State what was CHECKED, not what is true. The previous line claimed "a class sweep backed by an
    # invoked command" -- which this lint does not check at all, and did not check even before the
    # command test was removed. A gate's success message is the one line a reader will not re-derive.
    print(f"OK: {len(files)} file(s), {total} finding(s), 0 issue(s) — catalogue is WELL-FORMED: "
          f"required fields present, one yaml block, no aliases/merge/duplicate keys, mutants distinct. "
          f"Whether the sweep really ran is decided by reconcile_remediation_sites.py, not here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

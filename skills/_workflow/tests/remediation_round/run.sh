#!/usr/bin/env bash
# Negative-control corpus for lint_remediation_round.py.
#
# FOUR assertions. Each exists because a previous version of this harness lacked it:
#   1. every neg_* FAILS -- and with its EXPECTED reason. (v1 of the corpus checked exit status only;
#      4 of 8 fixtures were then found to fail for a different reason than their name, so the corpus
#      stayed green under 4 separate defect reintroductions.)
#   2. every neg_* HAS a WANT entry. (v2 skipped the reason check for any fixture missing one, so a new
#      fixture was checked for non-zero exit alone -- the same weakness, re-created in the mechanism
#      built to fix it.)
#   3. every pos_*/good PASSES.
#   4. each tagged check DISCRIMINATES: with that one check disabled, its fixture must PASS.
#
# Mutation is by `# MUT:<tag>` comment, not by literal source text. v2 anchored on source lines, so a
# behaviour-preserving refactor turned the corpus red -- and the pressure that creates is to re-point
# the anchor, which is how a mutant quietly comes to test nothing.
set -u
cd "$(dirname "$0")" || exit 2
L="../../scripts/lint_remediation_round.py"
SRC="$(cd ../../scripts && pwd)/lint_remediation_round.py"
fail=0

declare -A WANT=(
  [neg_no_command]="command\` is required"          [neg_single_site_no_command]="command\` is required" [neg_no_substitute]="substitute\` is required"
  [neg_substitute_restates]="restates"              [neg_placeholder_attr]="must be non-empty text"
  [neg_no_sites]="sites\` is required"              [neg_typo_key]="unknown key"
  [neg_guard_not_bool]="must be a YAML boolean"     [neg_empty]="list is empty"
  [neg_no_block]="no \`\`\`yaml findings block"     [neg_bad_yaml]="does not parse"
  [neg_unfilled_template]="must be non-empty text"  [neg_no_revert]="revert\` is required"
  [neg_guard_no_mutants]="requires \`mutants:\`"     [neg_two_blocks]="blocks; expected exactly one"
  [neg_merge_key]="merge keys"                      [neg_dup_key]="duplicate key"
  [neg_nonstring_value]="must be non-empty text"    [neg_nonstring_mutants]="revert\` is required"
  [neg_shape_placeholder]="shape\` is required"      [neg_single_site_token]="must be a REASON"
  [neg_scalar_fence]="must be non-empty text"
  [neg_zerowidth]="must be non-empty text"
  [neg_loose_fence]="yaml-tagged fence"
  [neg_alias]="alias"
  [neg_single_site_many]="claims one site but"
  [neg_mutants_no_guard]="without \`guard: true\`"
)

for f in neg_*.md; do
  n="${f%.md}"
  if [ -z "${WANT[$n]:-}" ]; then echo "FAIL: $f has no WANT entry -- add the expected reason"; fail=1; continue; fi
  out=$(python3 "$L" "$f" 2>&1)
  if [ $? -eq 0 ]; then echo "FAIL: $f passed but must fail"; fail=1; continue; fi
  grep -q "${WANT[$n]}" <<<"$out" || { echo "FAIL: $f failed for the WRONG reason (want '${WANT[$n]}'):"; sed 's/^/    /' <<<"$out"|head -3; fail=1; }
done
for f in good.md pos_*.md; do
  python3 "$L" "$f" >/dev/null 2>&1 || { echo "FAIL: $f must pass"; python3 "$L" "$f" 2>&1|head -3; fail=1; }
done

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT; DISC=0
disc() { # tag, fixture
  if ! python3 mutate.py "$SRC" "$TMP/m.py" "$1" 2>/dev/null; then
    echo "FAIL: no '# MUT:$1' tag in the source -- that mutant tests nothing"; fail=1; return
  fi
  DISC=$((DISC+1))
  python3 "$TMP/m.py" "$2.md" >/dev/null 2>&1 \
    || { echo "FAIL: $2 is HOLLOW -- still fails with '$1' disabled"; fail=1; }
}
disc alias            neg_alias
disc zerowidth        neg_zerowidth
disc loose_fence      neg_loose_fence
disc restates         neg_substitute_restates
disc sites_required   neg_no_sites
disc sweep_unknown    neg_typo_key
disc guard_bool       neg_guard_not_bool
disc revert_required  neg_no_revert
disc mutants_required neg_guard_no_mutants
disc two_blocks       neg_two_blocks
disc field_quality    neg_nonstring_value
disc single_site_cardinality neg_single_site_many
disc mutants_without_guard neg_mutants_no_guard
disc dup_keys          neg_dup_key
disc placeholder       neg_placeholder_attr



# ASSERTION 5: every `# MUT:` tag in the source has a `disc` line above.
#
# Without this the harness verified only that each LISTED tag discriminates, so adding a tagged check
# with no fixture passed silently -- a tally read as coverage, in the harness built to catch that. Four
# tags were unproven when this was added. An untestable tag goes in EXEMPT with a reason, so it is a
# decision on the record rather than an omission.
#
# The FIRST version of this check was itself vacuous: it read the source through the wrong relative
# path, found no tags, iterated an empty list and reported success. Hence the emptiness guard -- a
# coverage check that cannot see its subject must fail, not pass.
EXEMPT_TAGS="fence_scanner"   # fence_scanner: disabling it collects no blocks at all, so EVERY fixture fails
                         # and none can isolate it. It is core parsing, not a guard.
src_tags=$(grep -o '# MUT:[a-z_]*' "$SRC" | sed 's/.*://' | sort -u)
if [ -z "$src_tags" ]; then
  echo "FAIL: no '# MUT:' tags found in $SRC -- this check cannot see its subject and must not pass"
  fail=1
fi
have_tags=$(grep -oE '^[[:space:]]*disc[[:space:]]+[a-z_]+' run.sh | awk '{print $2}' | sort -u)
for t in $src_tags; do
  grep -qx "$t" <<<"$have_tags" && continue
  [ -n "$EXEMPT_TAGS" ] && grep -qw "$t" <<<"$EXEMPT_TAGS" && continue
  echo "FAIL: '# MUT:$t' has no discrimination fixture and is not EXEMPT -- tagged but unproven"
  fail=1
done

[ $fail -eq 0 ] && echo "OK: $(ls neg_*.md|wc -l) negative + $(ls good.md pos_*.md|wc -l) positive fixtures behave; $DISC discrimination mutants confirm the TAGGED checks are load-bearing (tagged checks only -- a green run is a regression net, not a coverage claim)"
exit $fail

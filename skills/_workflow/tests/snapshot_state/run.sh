#!/usr/bin/env bash
# Corpus for snapshot_round_state.py, over real throwaway git repos running real commands.
#
# The load-bearing fixture is `noise`. The tool's central claim is that it discovers its own
# nondeterminism, and the first implementation denoised only the BASELINE -- so a timestamp emitted at
# check time had no counterpart in the stable set, registered as an APPEARED line, and manufactured the
# exact delta the calibration exists to suppress. Every command would have reported a delta forever.
# That bug passed every other fixture here; only `noise` sees it.
set -u
cd "$(dirname "$0")" || exit 2
G="$(cd ../../scripts && pwd)/snapshot_round_state.py"
SRC="$G"
fail=0
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

mkrepo() { mkdir -p "$1"; git -C "$1" init -q; printf 'one\ntwo\n' > "$1/data.txt"
  printf 'print(open("data.txt").read())\n' > "$1/reader.py"
  printf 'import time\nprint("stable")\nprint(time.time())\n' > "$1/noisy.py"
  printf 'import time\nprint(time.time())\n' > "$1/dead.py"
  printf 'print(open("data.txt").read().upper())\n' > "$1/upper.py"; }
cfg() { printf '{"snapshot": {%s}}\n' "$2" > "$1/snap.json"; }
run_g() { python3 "$G" "$1/snap.json" --repo "$1" --state "$1/s.json" "${@:2}"; }
want() { grep -q "$2" <<<"$3" || { echo "FAIL: $1 -- wanted '$2' in:"; sed 's/^/    /' <<<"$3"|head -5; fail=1; }; }

DET='"read": "python3 reader.py"'
NOISY='"noisy": "python3 noisy.py"'
DEAD='"dead": "python3 dead.py"'

# --- positive: nothing changes ------------------------------------------------------------------
R="$TMP/pos"; mkrepo "$R"; cfg "$R" "$DET"
run_g "$R" --baseline >/dev/null 2>&1 || { echo "FAIL: pos baseline"; fail=1; }
out=$(run_g "$R" --check 2>&1); [ $? -eq 0 ] || { echo "FAIL: pos check must pass"; sed 's/^/    /' <<<"$out"|head -4; fail=1; }
want "positive" "nothing moved unexamined" "$out"

# --- THE design claim: a noisy line must NOT manufacture a delta ----------------------------------
R="$TMP/noise"; mkrepo "$R"; cfg "$R" "$NOISY"
run_g "$R" --baseline >/dev/null 2>&1 || { echo "FAIL: noise baseline"; fail=1; }
out=$(run_g "$R" --check 2>&1)
[ $? -eq 0 ] || { echo "FAIL: NOISE FIXTURE -- a timestamp manufactured a delta; the calibration is one-sided"; sed 's/^/    /' <<<"$out"|head -6; fail=1; }
want "noise" "nothing moved unexamined" "$out"

# --- neg: a real change, unacknowledged -----------------------------------------------------------
R="$TMP/delta"; mkrepo "$R"; cfg "$R" "$DET"
run_g "$R" --baseline >/dev/null 2>&1; printf 'one\nTHREE\n' > "$R/data.txt"
out=$(run_g "$R" --check 2>&1)
[ $? -ne 0 ] && want "neg unacknowledged" "did not acknowledge" "$out" || { echo "FAIL: unacknowledged delta must fail"; fail=1; }

# --- positive: the same change, acknowledged -------------------------------------------------------
out=$(run_g "$R" --check --accept "read=the fix rewrites data.txt on purpose" 2>&1)
[ $? -eq 0 ] || { echo "FAIL: acknowledged delta must pass"; sed 's/^/    /' <<<"$out"|head -4; fail=1; }
want "accepted" "acknowledged: the fix rewrites" "$out"

# --- neg: an entirely nondeterministic command contributes nothing ----------------------------------
R="$TMP/dead"; mkrepo "$R"; cfg "$R" "$DEAD"
out=$(run_g "$R" --baseline 2>&1)
[ $? -ne 0 ] && want "neg dead" "contributes NOTHING" "$out" || { echo "FAIL: all-noise command must be refused"; fail=1; }

# --- neg: baselined command dropped from the config -------------------------------------------------
R="$TMP/drop"; mkrepo "$R"; cfg "$R" "$DET,$NOISY"
run_g "$R" --baseline >/dev/null 2>&1; cfg "$R" "$NOISY"
out=$(run_g "$R" --check 2>&1)
[ $? -ne 0 ] && want "neg dropped" "no longer declared" "$out" || { echo "FAIL: dropped command must fail"; fail=1; }

# --- neg: command string edited between baseline and check -------------------------------------------
R="$TMP/edit"; mkrepo "$R"; cfg "$R" "$DET"
run_g "$R" --baseline >/dev/null 2>&1
cfg "$R" '"read": "python3 ./reader.py"'
out=$(run_g "$R" --check 2>&1)
[ $? -ne 0 ] && want "neg edited" "command changed since baseline" "$out" || { echo "FAIL: edited command must fail"; fail=1; }

# --- neg: acknowledgement naming no declared command --------------------------------------------------
R="$TMP/stale"; mkrepo "$R"; cfg "$R" "$DET"
run_g "$R" --baseline >/dev/null 2>&1
out=$(run_g "$R" --check --accept "nosuch=reason" 2>&1)
[ $? -ne 0 ] && want "neg stale-ack" "match no declared command" "$out" || { echo "FAIL: stale ack must fail"; fail=1; }

# --- neg: --accept with no reason ----------------------------------------------------------------------
out=$(run_g "$R" --check --accept "read=" 2>&1)
[ $? -ne 0 ] && want "neg reasonless-ack" "not a decision" "$out" || { echo "FAIL: reasonless ack must fail"; fail=1; }

# --- neg: check with no baseline -------------------------------------------------------------------------
R="$TMP/nobase"; mkrepo "$R"; cfg "$R" "$DET"
out=$(run_g "$R" --check 2>&1)
[ $? -ne 0 ] && want "neg no-baseline" "no baseline" "$out" || { echo "FAIL: check without baseline must fail"; fail=1; }

# --- neg: the gate's own runtime over budget ---------------------------------------------------------
R="$TMP/budget"; mkrepo "$R"; cfg "$R" "$DET"
out=$(run_g "$R" --baseline --max-seconds 0 2>&1)
[ $? -ne 0 ] && want "neg over-budget" "exceeds the 0s budget" "$out" || { echo "FAIL: over-budget must fail"; fail=1; }

# --- discrimination ---------------------------------------------------------------------------------------
DISC=0
disc() {
  if ! python3 ../remediation_round/mutate.py "$G" "$TMP/m.py" "$1" 2>/dev/null; then
    echo "FAIL: no '# MUT:$1' tag in the source -- that mutant tests nothing"; fail=1; return; fi
  DISC=$((DISC+1)); shift; "$@"
}
M() { python3 "$TMP/m.py" "$1/snap.json" --repo "$1" --state "$1/s.json" "${@:2}"; }
d_dead() { R="$TMP/x1"; mkrepo "$R"; cfg "$R" "$DEAD"; M "$R" --baseline >/dev/null 2>&1 \
  || { echo "FAIL: dead fixture HOLLOW"; fail=1; }; }
d_unack() { R="$TMP/x2"; mkrepo "$R"; cfg "$R" "$DET"; run_g "$R" --baseline >/dev/null 2>&1
  printf 'one\nTHREE\n' > "$R/data.txt"; M "$R" --check >/dev/null 2>&1 \
  || { echo "FAIL: unacknowledged fixture HOLLOW"; fail=1; }; }
d_drop() { R="$TMP/x3"; mkrepo "$R"; cfg "$R" "$DET,$NOISY"; run_g "$R" --baseline >/dev/null 2>&1
  cfg "$R" "$NOISY"; M "$R" --check >/dev/null 2>&1 || { echo "FAIL: dropped fixture HOLLOW"; fail=1; }; }
d_edit() { R="$TMP/x4"; mkrepo "$R"; cfg "$R" "$DET"; run_g "$R" --baseline >/dev/null 2>&1
  cfg "$R" '"read": "python3 ./reader.py"'
  M "$R" --check >/dev/null 2>&1 || { echo "FAIL: edited fixture HOLLOW"; fail=1; }; }
d_budget() { R="$TMP/x6"; mkrepo "$R"; cfg "$R" "$DET"
  M "$R" --baseline --max-seconds 0 >/dev/null 2>&1 || { echo "FAIL: over-budget fixture HOLLOW"; fail=1; }; }
d_stale() { R="$TMP/x5"; mkrepo "$R"; cfg "$R" "$DET"; run_g "$R" --baseline >/dev/null 2>&1
  M "$R" --check --accept "nosuch=reason" >/dev/null 2>&1 || { echo "FAIL: stale-ack fixture HOLLOW"; fail=1; }; }
disc baseline_no_stable     d_dead
disc check_unacknowledged   d_unack
disc check_command_dropped  d_drop
disc check_command_edited   d_edit
disc check_stale_ack        d_stale
disc over_budget            d_budget



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
EXEMPT_TAGS=""   # fence_scanner: disabling it collects no blocks at all, so EVERY fixture fails
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

[ $fail -eq 0 ] && echo "OK: 7 negative + 3 positive (incl. the noise-calibration fixture) over real git repos; $DISC discrimination mutants confirm the TAGGED checks are load-bearing (tagged checks only -- a green run is a regression net, not a coverage claim)"
exit $fail

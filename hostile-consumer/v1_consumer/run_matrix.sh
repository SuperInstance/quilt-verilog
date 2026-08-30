#!/usr/bin/env bash
# v1-consumer pass/reject matrix — regenerates nothing, runs the built consumer
# over the checked-in corpus. Corpus regeneration: tools/quf_epoch.py gen/forge.
set -u
cd "$(dirname "$0")"
B=${B:-./target/release/v1consumer}
K=$(xxd -p corpus/archive.key | tr -d '\n')
WK=$(xxd -p corpus/wrong.key | tr -d '\n')
pass=0; fail=0
chk() { # chk NAME EXPECTED_SUBSTR FILE KEY [extra args...]
  local name=$1 want=$2 file=$3 key=$4; shift 4
  local out; out=$($B "$1" "$file" "$key" "${@:2}" 2>&1); shift 0
  if grep -q "$want" <<<"$out"; then echo "PASS  $name"; pass=$((pass+1));
  else echo "FAIL  $name (wanted '$want', got: $(head -c 120 <<<"$out"))"; fail=$((fail+1)); fi
}
chk "honest n4 right key"       '"result":"ok"'   corpus/n4/all_demoted.quf  "$K" verify
chk "honest n16 right key"      '"result":"ok"'   corpus/n16/all_demoted.quf "$K" verify
chk "honest n64 right key"      '"result":"ok"'   corpus/n64/all_demoted.quf "$K" verify
chk "wrong key supplied"        '"code":"E3"'     corpus/n4/all_demoted.quf  "$WK" verify
chk "attacker resealed epoch0"  '"code":"E3"'     corpus/reseal.quf         "$K" verify
chk "flipped demotion bit"      '"code":"E3"'     corpus/flipbit.quf        "$K" skip-mount
chk "flipped bit (resurrect)"   '"code":"E3"'     corpus/flipbit_demoted.quf "$K" skip-mount
chk "bad magic"                 '"code":"E1"'     corpus/badmagic.quf       "$K" verify
chk "truncated"                 '"code":"E2"'     corpus/truncated.quf      "$K" verify
chk "epoch_no/name mismatch"    '"code":"E4"'     corpus/namemismatch.quf   "$K" verify
chk "two live epochs"           '"code":"E6"'     corpus/twolive.quf        "$K" skip-mount
chk "one live mounts"           '"epoch.0"'       corpus/n4/one_live.quf    "$K" skip-mount
chk "zero-epoch v1 base"        '"result":"ok"'   corpus/base_v1.quf        "$K" skip-mount
# gap 16 probe (documented spec gap, not a consumer bug): malformed epoch name
# is silently dropped by a §4-faithful consumer — neither E4 nor mounted.
GAP16=$($B skip-mount corpus/badname.quf "$K" 2>&1)
if grep -q 'epoch.05' <<<"$GAP16" || ! grep -q '"result":"ok"' <<<"$GAP16"; then
  echo "FAIL  gap-16 probe changed behavior (see RESULTS.md #12)"; fail=$((fail+1))
else
  echo "GAP16 malformed name silently dropped (documented, RESULTS.md #12)"
fi
echo "----"
echo "matrix: $pass pass, $fail fail (badname row is the documented gap-16 behavior, see RESULTS.md)"
echo "bench n4/n16/n64:"
for n in 4 16 64; do $B bench corpus/n$n/all_demoted.quf "$K" 200 | python3 -c "import json,sys,statistics;d=json.loads(sys.stdin.read());print(' N=$n per-epoch median %.1f us, skip-mount %.3f ms'%(statistics.median([e['micros'] for e in d['per_epoch_verify_us']]),d['skip_mount_avg_ms']))"; done

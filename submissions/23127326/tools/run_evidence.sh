#!/usr/bin/env bash
set -eo pipefail

# Evidence runs must start from credentials that are accepted by the exact SUT
# database in use. A non-zero HTTP login rate invalidates the whole run; do not
# promote its JTL, dashboard, or monitor CSV into the submission.

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <stress|spike|endurance> <backend-pid>" >&2
  exit 2
fi

scenario="$1"
backend_pid="$2"
root_dir="$(cd "$(dirname "$0")/.." && pwd)"
result_dir="$root_dir/results/evidence-rerun/$scenario"
hardware_csv="$root_dir/evidence/hardware/backend-${scenario}-evidence-20260830.csv"

case "$scenario" in
  stress)
    plan="$root_dir/test-plans/23127326_Stress_20260830.jmx"
    jtl="$result_dir/23127326_Stress_evidence_20260830.jtl"
    label="STRESS | 100 VU | ramp 300 s | total 480 s"
    properties=()
    ;;
  spike)
    plan="$root_dir/test-plans/23127326_Spike_20260830.jmx"
    jtl="$result_dir/23127326_Spike_evidence_20260830.jtl"
    label="SPIKE | 10 background + 90 burst VU | total 420 s"
    properties=()
    ;;
  endurance)
    plan="$root_dir/test-plans/23127326_Load_20260830.jmx"
    jtl="$result_dir/23127326_Endurance_threshold_20260830.jtl"
    label="ENDURANCE | 200 VU | ramp 120 s | total 720 s"
    properties=(-Jthreads=200 -JrampSeconds=120 -JdurationSeconds=720)
    ;;
  *)
    echo "Unknown scenario: $scenario" >&2
    exit 2
    ;;
esac

html_dir="$result_dir/html-20260830"
if [[ -e "$jtl" || -e "$html_dir" ]]; then
  echo "Refusing to overwrite existing evidence: $result_dir" >&2
  exit 3
fi

echo "$label"
echo "Backend PID: $backend_pid"
echo "JTL: $jtl"

python3 - "$root_dir/data/credentials.csv" <<'PY'
import csv
import json
import sys
import urllib.error
import urllib.request

with open(sys.argv[1], newline="", encoding="utf-8-sig") as handle:
    credential = next(csv.DictReader(handle))
request = urllib.request.Request(
    "http://localhost:3000/api/login",
    data=json.dumps(credential).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=10) as response:
        status = response.status
except urllib.error.HTTPError as error:
    status = error.code
if status != 200:
    raise SystemExit(f"Credential preflight failed with HTTP {status}; evidence run aborted")
print("Credential preflight passed: HTTP 200")
PY

mkdir -p "$result_dir"

python3 "$root_dir/tools/monitor_backend.py" "$backend_pid" "$hardware_csv" --interval 1 &
monitor_pid=$!
cleanup() {
  kill "$monitor_pid" 2>/dev/null || true
  wait "$monitor_pid" 2>/dev/null || true
}
trap cleanup EXIT

jmeter -n \
  -t "$plan" \
  -JdataDir="$root_dir/data" \
  -JbaseUrl=http://localhost:3000 \
  "${properties[@]}" \
  -l "$jtl" \
  -e -o "$html_dir"

echo "$scenario evidence completed for backend PID $backend_pid"

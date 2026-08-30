#!/usr/bin/env bash
set -eo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <stress|spike|endurance>" >&2
  exit 2
fi

scenario="$1"
scenario_upper="$(printf '%s' "$scenario" | tr '[:lower:]' '[:upper:]')"
submission_dir="/tmp/hw05-workspace/submission"
sut_backend="${SUT_BACKEND_DIR:-/tmp/hw05-eshop.OlFqz5/backend}"
port="${EVIDENCE_PORT:-3001}"
result_dir="$submission_dir/results/screenshot-rerun/$scenario"
hardware_csv="$submission_dir/evidence/hardware/backend-${scenario}-screenshot-20260830.csv"
current_run_file="/tmp/hw05-evidence-current"

case "$scenario" in
  stress)
    plan="$submission_dir/test-plans/23127326_Stress_20260830.jmx"
    jtl="$result_dir/23127326_Stress_screenshot_20260830.jtl"
    label="STRESS | 100 VU | ramp 300 s | total 480 s"
    process_title="HW05_STRESS_BE"
    properties=()
    ;;
  spike)
    plan="$submission_dir/test-plans/23127326_Spike_20260830.jmx"
    jtl="$result_dir/23127326_Spike_screenshot_20260830.jtl"
    label="SPIKE | 10 background + 90 burst VU | delay 120 s | total 420 s"
    process_title="HW05_SPIKE_BE"
    properties=()
    ;;
  endurance)
    plan="$submission_dir/test-plans/23127326_Load_20260830.jmx"
    jtl="$result_dir/23127326_Endurance_200VU_screenshot_20260830.jtl"
    label="ENDURANCE | 200 VU | ramp 120 s | total 720 s"
    process_title="HW05_ENDUR_BE"
    properties=(-Jthreads=200 -JrampSeconds=120 -JdurationSeconds=720)
    ;;
  *)
    echo "Unknown scenario: $scenario" >&2
    exit 2
    ;;
esac

if [[ ! -f "$sut_backend/server.js" ]]; then
  echo "SUT backend not found: $sut_backend" >&2
  exit 3
fi
if [[ -e "$result_dir" || -e "$hardware_csv" ]]; then
  echo "Refusing to overwrite existing screenshot evidence for $scenario" >&2
  exit 4
fi

mkdir -p "$result_dir"
cd "$sut_backend"
PORT="$port" PROCESS_TITLE="$process_title" node server.js >"$result_dir/backend.log" 2>&1 &
backend_pid=$!
monitor_pid=""
jmeter_pid=""

cleanup() {
  if [[ -n "$jmeter_pid" ]]; then
    kill "$jmeter_pid" 2>/dev/null || true
    wait "$jmeter_pid" 2>/dev/null || true
  fi
  if [[ -n "$monitor_pid" ]]; then
    kill "$monitor_pid" 2>/dev/null || true
    wait "$monitor_pid" 2>/dev/null || true
  fi
  kill "$backend_pid" 2>/dev/null || true
  wait "$backend_pid" 2>/dev/null || true
}
trap cleanup EXIT

for attempt in $(seq 1 30); do
  if curl -fsS "http://localhost:$port/api/products" >/dev/null; then
    break
  fi
  sleep 1
done
if ! curl -fsS "http://localhost:$port/api/products" >/dev/null; then
  echo "SUT did not become ready on port $port" >&2
  exit 5
fi

python3 "$submission_dir/tools/provision_sut.py" \
  --base-url "http://localhost:$port" --count 200 --data-dir "$submission_dir/data"
python3 "$submission_dir/tools/make_per_vu_inputs.py" \
  --count 200 --repeats 180 --data-dir "$submission_dir/data"

python3 - "$submission_dir/data/credentials.csv" "$port" <<'PY'
import csv
import json
import sys
import urllib.error
import urllib.request

with open(sys.argv[1], newline="", encoding="utf-8-sig") as handle:
    credential = next(csv.DictReader(handle))
request = urllib.request.Request(
    f"http://localhost:{sys.argv[2]}/api/login",
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
    raise SystemExit(f"Credential preflight failed with HTTP {status}")
print("Credential preflight passed: HTTP 200")
PY

python3 "$submission_dir/tools/monitor_backend.py" \
  "$backend_pid" "$hardware_csv" --interval 1 &
monitor_pid=$!

if [[ -t 1 && -n "${TERM:-}" ]]; then
  clear
fi
printf '\n============================================================\n'
printf ' HW05 REAL SAME-SESSION EVIDENCE\n'
printf ' SCENARIO: %s\n' "$label"
printf ' BACKEND: node | PID %s | PORT %s\n' "$backend_pid" "$port"
printf ' JMETER: non-GUI execution | START %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
printf '============================================================\n\n'
printf 'scenario=%s\nbackend_pid=%s\nport=%s\n' "$scenario" "$backend_pid" "$port" >"$current_run_file"

jmeter -n \
  -t "$plan" \
  -JdataDir="$submission_dir/data" \
  -JbaseUrl="http://localhost:$port" \
  "${properties[@]}" \
  -l "$jtl" \
  -e -o "$result_dir/html-20260830" &
jmeter_pid=$!

while kill -0 "$jmeter_pid" 2>/dev/null; do
  printf '[EVIDENCE ACTIVE] %-9s | BACKEND PID=%s | JMETER PID=%s | %s\n' \
    "$scenario_upper" "$backend_pid" "$jmeter_pid" "$(date '+%H:%M:%S')"
  sleep 5
done
wait "$jmeter_pid"
jmeter_pid=""

kill "$monitor_pid" 2>/dev/null || true
wait "$monitor_pid" 2>/dev/null || true
monitor_pid=""
printf '\n[EVIDENCE COMPLETE] %s | BACKEND PID=%s | %s\n' \
  "$scenario_upper" "$backend_pid" "$(date '+%Y-%m-%d %H:%M:%S %Z')"

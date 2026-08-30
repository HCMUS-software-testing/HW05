#!/usr/bin/env bash
set -eo pipefail

# Reproducible threshold experiment. The SUT recreates its SQLite tables on
# every startup, so accounts must be provisioned after the server is ready and
# before JMeter starts.

submission_dir="$(cd "$(dirname "$0")/.." && pwd)"
sut_backend="${SUT_BACKEND_DIR:-/tmp/hw05-eshop.OlFqz5/backend}"
result_root="$submission_dir/results/staircase-20260830"
hardware_root="$submission_dir/evidence/hardware/staircase-20260830"
metrics_root="$submission_dir/report/metrics-staircase-20260830"
plan="$submission_dir/test-plans/23127326_Load_20260830.jmx"
analyzer="$submission_dir/agent-skill/performance-test-workflow/scripts/analyze_jtl.py"

if [[ ! -f "$sut_backend/server.js" ]]; then
  echo "SUT backend not found: $sut_backend" >&2
  exit 2
fi
if [[ -e "$result_root" || -e "$hardware_root" || -e "$metrics_root" ]]; then
  echo "Refusing to overwrite an existing staircase experiment." >&2
  exit 3
fi

mkdir -p "$result_root" "$hardware_root" "$metrics_root"

cd "$sut_backend"
node server.js >"$result_root/backend.log" 2>&1 &
backend_pid=$!
monitor_pid=""
cleanup() {
  if [[ -n "$monitor_pid" ]]; then
    kill "$monitor_pid" 2>/dev/null || true
    wait "$monitor_pid" 2>/dev/null || true
  fi
  kill "$backend_pid" 2>/dev/null || true
  wait "$backend_pid" 2>/dev/null || true
}
trap cleanup EXIT

for attempt in $(seq 1 30); do
  if curl -fsS http://localhost:3000/api/products >/dev/null; then
    break
  fi
  sleep 1
done
if ! curl -fsS http://localhost:3000/api/products >/dev/null; then
  echo "SUT did not become ready." >&2
  exit 4
fi

python3 "$submission_dir/tools/provision_sut.py" --count 200 --data-dir "$submission_dir/data"
python3 "$submission_dir/tools/make_per_vu_inputs.py" --count 200 --repeats 180 --data-dir "$submission_dir/data"

run_stage() {
  vu="$1"
  ramp="$2"
  duration="$3"
  stage_dir="$result_root/${vu}vu"
  jtl="$stage_dir/23127326_Staircase_${vu}VU_20260830.jtl"
  monitor="$hardware_root/backend-staircase-${vu}vu-20260830.csv"
  mkdir -p "$stage_dir"
  python3 "$submission_dir/tools/monitor_backend.py" "$backend_pid" "$monitor" --interval 1 &
  monitor_pid=$!
  jmeter -n -t "$plan" \
    -JdataDir="$submission_dir/data" \
    -JbaseUrl=http://localhost:3000 \
    -Jthreads="$vu" \
    -JrampSeconds="$ramp" \
    -JdurationSeconds="$duration" \
    -l "$jtl"
  kill "$monitor_pid" 2>/dev/null || true
  wait "$monitor_pid" 2>/dev/null || true
  monitor_pid=""
  python3 "$analyzer" "$jtl" --format json >"$metrics_root/${vu}vu.json"
}

# Screening staircase: each stage includes a ramp followed by at least 90 s at
# the target concurrency. The final ceiling is then held for ten minutes.
run_stage 70 30 120
run_stage 100 30 120
run_stage 150 45 135
run_stage 200 60 150

endurance_dir="$result_root/endurance-200vu"
endurance_jtl="$endurance_dir/23127326_Endurance_200VU_20260830.jtl"
endurance_monitor="$hardware_root/backend-endurance-200vu-20260830.csv"
mkdir -p "$endurance_dir"
python3 "$submission_dir/tools/monitor_backend.py" "$backend_pid" "$endurance_monitor" --interval 1 &
monitor_pid=$!
jmeter -n -t "$plan" \
  -JdataDir="$submission_dir/data" \
  -JbaseUrl=http://localhost:3000 \
  -Jthreads=200 \
  -JrampSeconds=120 \
  -JdurationSeconds=720 \
  -l "$endurance_jtl" \
  -e -o "$endurance_dir/html-20260830"
kill "$monitor_pid" 2>/dev/null || true
wait "$monitor_pid" 2>/dev/null || true
monitor_pid=""
python3 "$analyzer" "$endurance_jtl" --format json >"$metrics_root/endurance-200vu.json"

printf 'Completed staircase and 200 VU endurance run with backend PID %s\n' "$backend_pid"

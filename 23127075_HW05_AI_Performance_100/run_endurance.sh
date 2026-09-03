#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

JMETER_BIN="${JMETER_BIN:-/opt/jmeter/bin/jmeter}"
RESULT_DIR="results/endurance"
mkdir -p "$RESULT_DIR"
rm -rf "$RESULT_DIR/html-report"
rm -f results/endurance/raw.jtl
rm -f "$RESULT_DIR/backend-resources.csv"

monitor_args=(
  --output "$RESULT_DIR/backend-resources.csv"
  --duration 605
  --interval 5
)
if [[ -n "${BACKEND_PID:-}" ]]; then
  monitor_args+=(--pid "$BACKEND_PID")
fi

python3 tools/monitor_backend.py "${monitor_args[@]}" &
monitor_pid=$!
trap 'kill "$monitor_pid" 2>/dev/null || true' EXIT

"$JMETER_BIN" -n \
  -t test-plans/23127075_Endurance_20260902.jmx \
  -l results/endurance/raw.jtl \
  -e -o results/endurance/html-report

wait "$monitor_pid"
trap - EXIT
python3 tools/analyze_jtl.py results/endurance/raw.jtl

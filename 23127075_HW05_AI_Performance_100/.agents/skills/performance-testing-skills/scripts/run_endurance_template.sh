#!/bin/bash
# Replace placeholders and run from src/. Set BACKEND_PID for deterministic monitoring.
set -euo pipefail

JMETER_BIN="${JMETER_BIN:-/opt/jmeter/bin/jmeter}"
PLAN="test-plans/{StudentID}_Endurance_{YYYYMMDD}.jmx"
RESULT_DIR="results/endurance"

mkdir -p "$RESULT_DIR"
rm -rf "$RESULT_DIR/html-report"
rm -f "$RESULT_DIR/raw.jtl" "$RESULT_DIR/backend-resources.csv"

python3 tools/monitor_backend.py \
  --pid "${BACKEND_PID:?Set BACKEND_PID to the SUT backend process}" \
  --duration 605 --interval 5 \
  --output "$RESULT_DIR/backend-resources.csv" &
monitor_pid=$!
trap 'kill "$monitor_pid" 2>/dev/null || true' EXIT

"$JMETER_BIN" -n -t "$PLAN" -l "$RESULT_DIR/raw.jtl" \
  -e -o "$RESULT_DIR/html-report"
wait "$monitor_pid"
trap - EXIT
python3 tools/analyze_jtl.py "$RESULT_DIR/raw.jtl"

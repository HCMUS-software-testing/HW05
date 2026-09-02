#!/usr/bin/env bash
# Run this from the user's graphical terminal while htop is the foreground pane.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

command -v gnome-screenshot >/dev/null || {
  echo "Missing gnome-screenshot. Install it first: sudo dnf install -y gnome-screenshot"
  exit 1
}

rm -rf results/spike/html-report
rm -f results/spike/raw.jtl
mkdir -p evidence/screenshots

echo "Starting Spike in 5 seconds. Keep htop visible."
sleep 5
/opt/jmeter/bin/jmeter -n \
  -t test-plans/23127075_Spike_20260901.jmx \
  -l results/spike/raw.jtl \
  -e -o results/spike/html-report &
jmeter_pid=$!

# The plan reaches peak concurrency almost immediately; capture during the run.
sleep 2
gnome-screenshot -f evidence/screenshots/htop_spike.png
wait "$jmeter_pid"

echo "Spike finished; evidence saved to evidence/screenshots/htop_spike.png"

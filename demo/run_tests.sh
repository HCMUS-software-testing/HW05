#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p results/{load,stress,spike}/html-report
rm -f results/load/raw.jtl results/stress/raw.jtl results/spike/raw.jtl
rm -rf results/load/html-report results/stress/html-report results/spike/html-report
mkdir -p results/{load,stress,spike}/html-report
jmeter -n -t test-plans/23127075_Load_20260903.jmx -l results/load/raw.jtl -e -o results/load/html-report
jmeter -n -t test-plans/23127075_Stress_20260903.jmx -l results/stress/raw.jtl -e -o results/stress/html-report
jmeter -n -t test-plans/23127075_Spike_20260903.jmx -l results/spike/raw.jtl -e -o results/spike/html-report

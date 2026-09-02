#!/bin/bash
# HW05 Performance Test Runner Script Template
# Replace {StudentID} and {DATE} placeholders before use.
#
# Usage: cd src && chmod +x run_tests.sh && ./run_tests.sh
#
# This script:
# 1. Sets working directory to its own location (src/)
# 2. Creates output and evidence directories
# 3. Cleans previous results
# 4. Runs Load, Stress, Spike tests sequentially
# 5. Generates HTML reports for each test

set -e

# Always set working directory to src (directory containing this script)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Configuration — edit these for your submission
STUDENT_ID="${STUDENT_ID:-XXXXXXX}"
DATE="${DATE:-YYYYMMDD}"

LOAD_PLAN="test-plans/${STUDENT_ID}_Load_${DATE}.jmx"
STRESS_PLAN="test-plans/${STUDENT_ID}_Stress_${DATE}.jmx"
SPIKE_PLAN="test-plans/${STUDENT_ID}_Spike_${DATE}.jmx"

# 1. Create output and evidence directories if they don't exist
mkdir -p results/load/html-report
mkdir -p results/stress/html-report
mkdir -p results/spike/html-report
mkdir -p evidence/screenshots
mkdir -p evidence/hardware

# 2. Clean previous report folders for clean HTML generation
rm -rf results/load/html-report/* results/stress/html-report/* results/spike/html-report/*
rm -f results/load/raw.jtl results/stress/raw.jtl results/spike/raw.jtl

# 3. Run Load Test
echo "=========================================================="
echo "🚀 1/3 Running Load Test..."
echo "=========================================================="
jmeter -n -t "$LOAD_PLAN" \
       -l results/load/raw.jtl \
       -e -o results/load/html-report

# 4. Run Stress Test
echo "=========================================================="
echo "🚀 2/3 Running Stress Test..."
echo "=========================================================="
jmeter -n -t "$STRESS_PLAN" \
       -l results/stress/raw.jtl \
       -e -o results/stress/html-report

# 5. Run Spike Test
echo "=========================================================="
echo "🚀 3/3 Running Spike Test..."
echo "=========================================================="
jmeter -n -t "$SPIKE_PLAN" \
       -l results/spike/raw.jtl \
       -e -o results/spike/html-report

echo "=========================================================="
echo "✅ ALL 3 PERFORMANCE TESTS COMPLETED SUCCESSFULLY!"
echo "Results generated in results/"
echo "=========================================================="

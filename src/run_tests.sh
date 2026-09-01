#!/bin/bash
# HW05 Performance Test Automated Execution Script
# Student: Le Trung Kien (23127075) - Member 4 (Admin Workflow)

set -e

# Always set working directory to src (directory containing this script)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 1. Create output and evidence directories if they don't exist
mkdir -p results/load/html-report
mkdir -p results/stress/html-report
mkdir -p results/spike/html-report
mkdir -p evidence/screenshots
mkdir -p evidence/hardware

# Clean previous report folders if needed for clean HTML generation
rm -rf results/load/html-report/*
rm -rf results/stress/html-report/*
rm -rf results/spike/html-report/*
rm -f results/load/raw.jtl
rm -f results/stress/raw.jtl
rm -f results/spike/raw.jtl

echo "=========================================================="
echo "🚀 1/3 Running Load Test (10 threads, ramp 10s)..."
echo "=========================================================="
jmeter -n -t test-plans/23127075_Load_20260901.jmx \
       -l results/load/raw.jtl \
       -e -o results/load/html-report

echo "=========================================================="
echo "🚀 2/3 Running Stress Test (50 threads, ramp 15s)..."
echo "=========================================================="
jmeter -n -t test-plans/23127075_Stress_20260901.jmx \
       -l results/stress/raw.jtl \
       -e -o results/stress/html-report

echo "=========================================================="
echo "🚀 3/3 Running Spike Test (100 threads, ramp 1s)..."
echo "=========================================================="
jmeter -n -t test-plans/23127075_Spike_20260901.jmx \
       -l results/spike/raw.jtl \
       -e -o results/spike/html-report

echo "=========================================================="
echo "✅ ALL 3 PERFORMANCE TESTS COMPLETED SUCCESSFULLY!"
echo "Results generated in results/"
echo "=========================================================="

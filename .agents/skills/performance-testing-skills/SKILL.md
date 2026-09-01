---
name: performance-testing-skills
description: Use when designing, executing, analyzing, or reporting JMeter performance tests (Load, Stress, Spike, Endurance) against a REST API backend for a software-testing homework assignment
---

# Performance Testing Skills

## Overview

Automate the full performance-testing homework workflow: from SUT analysis through JMeter test plan design, execution, AI-assisted analysis, misinterpretation hunting, continuous-testing proposal, and submission packaging. All theory is internalized from course slides — no external reference files required.

## When to Use

- Designing JMeter Load / Stress / Spike / Endurance test plans
- Creating CSV test data for parameterized API workflows
- Writing automated test runner scripts
- Collecting execution evidence (htop, fastfetch, screenshots)
- Analyzing `.jtl` raw logs with AI and hunting misinterpretations
- Generating performance reports with real metrics
- Proposing CI/CD continuous performance testing pipelines
- Packaging `src/` into a submission ZIP

## Performance Testing Theory (Internalized)

### Definition & Goals

Performance testing is **non-functional testing** ensuring software performs properly under expected workload. The goal is NOT to find bugs but to **eliminate performance bottlenecks**.

Three focus areas: **Speed** (response time), **Scalability** (max user load), **Stability** (under varying loads).

### 10 Key Metrics

| # | Metric | Category | Description |
|---|--------|----------|-------------|
| 01 | CPU utilization | Resource | % CPU capacity used |
| 02 | Memory utilization | Resource | Primary memory usage |
| 03 | Response times | Time | Request → Response duration |
| 04 | Average load time | Time | Time to complete loading |
| 05 | Throughput | Volume | Transactions per second |
| 06 | Average latency | Time | Queue wait time before processing |
| 07 | Bandwidth | Resource | Data volume transferred per second |
| 08 | Requests per second | Volume | RPS handled |
| 09 | Error rate | Volume | % requests resulting in errors |
| 10 | Transactions passed/failed | Volume | Pass vs fail ratio |

### 6 Test Types

1. **Load Testing**: Product ability under anticipated user loads. Find congestion before launch.
2. **Endurance (Soak)**: Software handles expected load over long period (10-15 min sustained).
3. **Stress Testing**: Extreme workloads to find **breaking point**.
4. **Volume Testing**: Performance under varying database volumes.
5. **Spike Testing**: Reaction to sudden large spikes in load.
6. **Scalability Testing**: Effectiveness in scaling up to support increased user load.

### 7-Step Process

1. **Identify test environment** — Hardware, software, network, tools inventory
2. **Determine performance criteria** — Metrics + success thresholds (e.g., latency < 500ms, error < 1%)
3. **Plan and design** — Key scenarios, user variability, test data, metrics to gather
4. **Configure test environment** — Set up tools, monitoring, runner scripts
5. **Implement test design** — Create `.jmx` test plans with assertions
6. **Run tests** — Execute and monitor (htop, resource usage)
7. **Analyze and retest** — Interpret results, fine-tune, re-run

## Workflow Phases

### Phase 1: SUT Analysis

Read the SUT source code to discover:
- **Endpoints**: URL paths, HTTP methods, request/response schemas
- **Authentication**: Login endpoint, token format (JWT/session), required headers
- **Database**: Type (SQLite/PostgreSQL/MySQL), seeded data, schema
- **Port**: Default backend port
- **Middleware**: Which endpoints require auth, rate limiting, account lockout

```
Output: A list of endpoints grouped into Auth-heavy, Read-heavy, Transactional
```

### Phase 2: Endpoint Selection & Workflow Design

Select 3 endpoint groups covering the required categories:

- **Auth-heavy**: Login, admin-protected routes, account lockout scenarios
- **Read-heavy**: List/search endpoints, detail views, public queries
- **Transactional**: Create/update/delete operations, cart, checkout

Design a single end-to-end workflow that all 3 test plans (Load, Stress, Spike) share. Example Admin workflow:
```
Login → Get Admin Users → List Products → List Categories → Create Product → Delete Product (cleanup)
```

### Phase 3: Test Data Creation

Create CSV files under `src/data/`:

- `credentials.csv` — Login credentials (at minimum: `email,password`)
- Additional CSVs as needed for the workflow (product data, order payloads, etc.)

**Rules:**
- Use data seeded in SUT's database (check `database.js` or seed scripts)
- Use unique test data for destructive operations (registration, coupon usage)
- Document account-lockout reset steps between runs

### Phase 4: JMeter Test Plan Design

Create 3 `.jmx` files under `src/test-plans/`:

**Naming**: `{StudentID}_{ScenarioType}_{YYYYMMDD}.jmx`

| Plan | Threads | Ramp-up | Think-time | Loops | Listener |
|------|---------|---------|------------|-------|----------|
| **Load** | 10 | 10s | 1-3s (Gaussian) | 5 | Aggregate Report |
| **Stress** | 50 | 15s | 0.5-1.5s | 10 | Summary Report |
| **Spike** | 100 | 1s | None | 3 | View Results Tree |

**IMPORTANT**: Use 3 **different** listener/report types across the 3 plans.

Each plan must include:
- **CSV Data Set Config** — pointing to `data/*.csv` (relative paths)
- **HTTP Request Defaults** — server, port, protocol
- **HTTP Header Manager** — Content-Type, Authorization bearer
- **JSON Extractor** — Extract tokens, IDs from responses
- **Response Assertion** — Verify HTTP 200/201 on each sampler
- **Timer** — Gaussian Random Timer (Load/Stress), none for Spike
- **Listener** — Output to `results/{type}/raw.jtl`

### Phase 5: Runner Script Creation

Create `src/run_tests.sh`:

```bash
#!/bin/bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create output directories
mkdir -p results/{load,stress,spike}/html-report
mkdir -p evidence/{screenshots,hardware}

# Clean previous results
rm -rf results/load/html-report/* results/stress/html-report/* results/spike/html-report/*
rm -f results/load/raw.jtl results/stress/raw.jtl results/spike/raw.jtl

# Run tests
jmeter -n -t test-plans/{StudentID}_Load_{DATE}.jmx -l results/load/raw.jtl -e -o results/load/html-report
jmeter -n -t test-plans/{StudentID}_Stress_{DATE}.jmx -l results/stress/raw.jtl -e -o results/stress/html-report
jmeter -n -t test-plans/{StudentID}_Spike_{DATE}.jmx -l results/spike/raw.jtl -e -o results/spike/html-report
```

**All paths must be relative to `src/`** so the folder works as a standalone submission.

### Phase 6: Test Execution & Evidence Collection

1. Start the SUT backend
2. Run `./run_tests.sh` from `src/`
3. While tests run, capture evidence:

**Required Screenshots:**
- `evidence/hardware/fastfetch.png` — Hardware specs (hostname must match)
- `evidence/screenshots/htop_load.png` — htop during Load test
- `evidence/screenshots/htop_stress.png` — htop during Stress test
- `evidence/screenshots/htop_spike.png` — htop during Spike test

**htop Screenshot Checklist:**
- Process list visible with node/java processes
- CPU% and MEM% columns visible
- System CPU/Memory bars at top visible
- Timestamp or test identification visible

**Account Lockout Reset:**
If stress/spike triggers login lockout (3 failed attempts), reset between runs and document the reset procedure.

### Phase 7: Report Generation

Create `src/report/main-report.md` with these sections:

#### Task 1: Design & Execution Results
- Scope & API endpoint groups
- Metrics table with real data from `.jtl` logs:
  - Threads, Ramp-up, Loops, Total Samples
  - Throughput (RPS), Avg/Min/Max/p95 Latency
  - Error Rate, Listener type, Log file path
- Per-scenario analysis
- Execution evidence links
- Endurance threshold (sustained RPS, memory ceiling from 10-15 min soak test)

#### Task 2: AI Analysis & Misinterpretation Hunt
- Feed `.jtl` logs to AI for analysis
- Identify WHERE AI misinterpreted metrics (quote correct values from raw logs)
- Evaluate AI optimization recommendations:
  - Classify each as **feasible** or **hallucination**
  - Example hallucinations: suggesting Redis for SQLite app, recommending connection pooling for single-file DB

#### Task 3: Continuous Performance Testing Proposal
- Mermaid flowchart showing CI/CD pipeline:
  - Trigger on commit/PR
  - Detect if performance tests needed
  - Run tests, collect metrics
  - Compare p95 against baseline
  - Flag regressions
- Trade-offs discussion: cost, false positives, infrastructure

### Phase 8: README & Self-Assessment

Create `src/README.md` with:
- Student info
- Self-assessment grading table (matching rubric)
- Directory structure
- Execution instructions
- Workflow coverage summary
- Endurance threshold numbers
- Bug/issue count
- YouTube demo link

### Phase 9: Video Demo

Record unlisted YouTube video (≥ 6 minutes total):
- Show JMeter tool AND resource monitor (htop) in same frame
- Vietnamese narration by the student
- Cover all 3 scenarios (Load, Stress, Spike)
- Can be split into 1 clip per scenario

### Phase 10: Submission Packaging

1. Update `src/git-commit-log.txt` with `git log --oneline`
2. Copy `src/` to staging folder
3. Rename copy to `{StudentID}_HW05_AI_Performance_{SelfAssessedGrade}`
4. Inspect for secrets, unwanted files, `.gitignore`d content
5. ZIP the renamed copy
6. **Never delete or rename the working `src/` folder**

## Deliverables Checklist

- [ ] 3 JMeter test plans (Load / Stress / Spike) with correct naming
- [ ] CSV data files under `data/`
- [ ] `run_tests.sh` with relative paths
- [ ] 3 raw `.jtl` log files under `results/`
- [ ] 3 HTML report directories under `results/`
- [ ] Hardware screenshot (fastfetch/screenfetch)
- [ ] htop screenshots per test scenario
- [ ] `report/main-report.md` — Task 1 + Task 2 + Task 3
- [ ] `README.md` — Self-assessment + summary
- [ ] `ai-audit/ai_audit_report.md` — Full audit log
- [ ] `git-commit-log.txt`
- [ ] YouTube video link (≥ 6 min, unlisted)
- [ ] GitHub Issues for bugs (if any)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Absolute paths in `.jmx` files | Use relative paths (`data/`, `results/`) — execute from `src/` |
| Same listener type across all 3 plans | Must use 3 different listeners |
| AI-generated metrics without verification | Always cross-check against raw `.jtl` log values |
| Missing hardware hostname match | Use same machine as previous homework submissions |
| No think-time in Load/Stress | Add Gaussian Random Timer for realistic simulation |
| Forgetting account lockout reset | Document reset steps between Stress/Spike runs |
| Submitting `src/` directly | Copy `src/`, rename copy, ZIP the copy |

## JMeter CLI Quick Reference

```bash
# Non-GUI execution with HTML report
jmeter -n -t plan.jmx -l results.jtl -e -o html-report/

# Flags:
# -n  Non-GUI mode
# -t  Test plan file
# -l  Log file output (.jtl)
# -e  Generate HTML report after test
# -o  HTML report output directory
```

---
name: performance-testing-agent
description: Comprehensive agent skill for end-to-end performance testing automation using Apache JMeter, data-driven CSV generation, custom thread groups (Stepping/Ultimate), raw JTL metrics ground-truth analysis, and automated audit logging.
---

# Performance Testing Agent Skill

## 1. Overview & Capability
The `performance-testing-agent` is an expert-level test automation skill designed to orchestrate and execute end-to-end performance testing workflows on RESTful API backends. It integrates Apache JMeter 5.6.3, Custom Thread Groups (`jpgc-casutg`), data-driven CSV parameterization, Ground Truth JTL log parsing, and AI audit reporting.

## 2. Core Architecture & Components

```text
.agents/skills/performance-testing-agent/
├── SKILL.md                          <-- Skill specification & AI guidance
└── scripts/                          <-- Executable automation toolset
    ├── seed_test_accounts.py         <-- Seeds 50+ test users into SQLite & exports credentials.csv
    ├── setup_jmeter.py               <-- Downloads/configures JMeter Portable + Plugins + JVM Heap
    ├── smoke_test_sut.py             <-- Validates API endpoints before load testing
    ├── run_jmeter.py                 <-- Cross-platform CLI runner with JVM Heap (-Xms1g -Xmx4g)
    ├── jmx_generator.py              <-- Programmatic XML generator for Standard/Stepping/Ultimate JMX plans
    ├── jtl_parser.py                 <-- Ground Truth statistical parser for raw .jtl log files
    ├── reset_lockout.py              <-- Clears locked_until and login_attempts in SQLite database
    ├── audit_logger.py               <-- Automatically records prompts & outputs to ai-audit-report.md
    └── verify_phase1.py              <-- Automated Phase 1 verification suite
```

---

## 3. Standard Performance Testing Workflow

When executing performance testing on a target System Under Test (SUT), follow this systematic procedure:

### Step 1: Pre-Test Setup & Verification
1. Ensure SUT Backend is active (e.g., `http://localhost:3000`).
2. Run `python scripts/seed_test_accounts.py` to populate realistic test credentials.
3. Run `python scripts/smoke_test_sut.py` to verify functional correctness of all workflow endpoints.

### Step 2: Test Plan Generation (`jmx_generator.py`)
Generate 3 distinct test plans with specific profiles according to testing objectives:
- **Load Test Plan (`<StudentID>_Load_<Date>.jmx`)**:
  - **Thread Group**: `StandardThreadGroup` (50 VUs, Ramp-up: 60s, Loop: 10).
  - **Think-Time**: `GaussianRandomTimer` (1500ms ± 500ms).
  - **Listener**: `Summary Report` (`SummaryCollector`).
- **Stress Test Plan (`<StudentID>_Stress_<Date>.jmx`)**:
  - **Thread Group**: `SteppingThreadGroup` (Start 50, Step +50 every 30s up to 250 VUs).
  - **Listener**: `Aggregate Report` (`StatVisualizer`).
- **Spike Test Plan (`<StudentID>_Spike_<Date>.jmx`)**:
  - **Thread Group**: `UltimateThreadGroup` (350 VUs, Startup: 10s, Hold: 30s, Shutdown: 10s).
  - **Listener**: `View Results Tree` (`ViewResultsFullVisualizer`).

### Step 3: Headless Execution & Evidence Collection (`run_jmeter.py`)
Execute test plans using non-GUI mode with full garbage collection optimization:
```bash
python scripts/run_jmeter.py -n -t <path_to_plan.jmx> -l <path_to_raw.jtl> -e -o <path_to_html_report>
```

### Step 4: Ground Truth Log Parsing & Misinterpretation Hunt (`jtl_parser.py`)
Parse raw `.jtl` log files to extract exact metrics:
- Total Samples, Error Rate (%).
- Average, Min, Max Latency (ms).
- Percentiles: **Median (p50), p90, p95, p99**.
- Throughput (Requests per second).
Cross-check AI analysis against these ground truth values to identify hallucinations or misinterpretations.

### Step 5: Database State Reset & Cleanup (`reset_lockout.py`)
After Stress/Spike test executions that may have triggered account lockouts or database locks, run:
```bash
python scripts/reset_lockout.py
```

### Step 6: Audit Logging (`audit_logger.py`)
Automatically log all prompt interactions, AI generation steps, and human review decisions into `ai-audit-report.md`.

---

## 4. Technical Rules & Constraints
- **JVM Heap Allocation**: Always maintain `-Xms1g -Xmx4g` when running load tests with > 100 threads to prevent client-side GC pauses.
- **CSV Sharing Mode**: Use `Sharing mode: All threads`, `Recycle on EOF: True`, `Stop thread on EOF: False`.
- **Bearer Token Handling**: Must extract JWT token using `JSONPostProcessor` (`$.token`) and inject via `HTTP Header Manager` (`Authorization: Bearer ${token}`).
- **Assertions**: Verify both HTTP status code (200) and response body payload text.

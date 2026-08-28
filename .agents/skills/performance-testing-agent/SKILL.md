---
name: performance-testing-agent
description: Comprehensive agent skill for end-to-end performance testing automation using Apache JMeter, data-driven CSV generation, custom thread groups (Stepping/Ultimate), raw JTL metrics ground-truth analysis, and automated audit logging.
---

# Performance Testing Agent Skill

## 1. Overview & Capability
The `performance-testing-agent` is an expert-level test automation skill designed to orchestrate and execute end-to-end performance testing workflows on RESTful API backends. It integrates Apache JMeter 5.6.3, Custom Thread Groups (`jpgc-casutg`), data-driven CSV parameterization, Ground Truth JTL log parsing, and AI audit reporting.

> **Design Paradigm:** **AI-Assisted with Human-in-the-Loop (HITL) Checkpoints** — Strictly rejects "Big-Bang" unverified execution. Every major phase requires human verification and approval gates.

---

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
    ├── verify_phase1.py              <-- Automated Phase 1 verification suite
    ├── verify_phase2.py              <-- Automated Phase 2 verification suite
    └── verify_phase3.py              <-- Automated Phase 3 verification suite
```

---

## 3. Human-in-the-Loop Verification Gates (Human Checkpoints)

To ensure academic integrity and prevent undetected AI hallucination, the agent operates through 4 strict Human Verification Gates:

```
[ AI Generates Assets ] ──► [ GATE 1: Human Plan Audit ] ──► [ AI Executes Test ]
                                       │
                                       ▼
[ AI Analyzes Logs ]    ──► [ GATE 2: Ground Truth Audit ] ──► [ Approved Final Report ]
```

### 🛡️ Gate 1: Pre-Execution Plan & Data Audit (Human Checkpoint 1)
- **Actor:** Human Tester / Student.
- **Verification Items:**
  1. Verify 3 distinct listeners are configured: *Summary Report* (Load), *Aggregate Report* (Stress), *View Results Tree* (Spike).
  2. Verify CSV paths use portable relative pathing (`../data/...`).
  3. Verify Think-Time timer (`GaussianRandomTimer` 1500ms ± 500ms).
  4. Verify Token extraction (`$.token`) and Authorization Header injection.
- **Rule:** AI is NOT permitted to launch headless test execution until Gate 1 is approved.

### 🛡️ Gate 2: Execution & Resource Monitoring Oversight (Human Checkpoint 2)
- **Actor:** Human Tester / Student.
- **Verification Items:**
  1. Monitor real-time CPU / RAM via OS Resource Monitor / Task Manager during test execution.
  2. Observe system behavior at breaking points (Stress test 250 VUs) and recovery (Spike test 350 VUs).
  3. Capture visual evidence (screenshots of JMeter + Resource Monitor side-by-side).

### 🛡️ Gate 3: Ground Truth Log Parsing & Misinterpretation Hunt (Human Checkpoint 3)
- **Actor:** Human Tester / Student vs. AI Analysis.
- **Verification Items:**
  1. Execute `jtl_parser.py` to extract absolute mathematical Ground Truth (p50, p90, p95, p99, Throughput, Error Rate).
  2. Cross-check AI interpretation against Ground Truth to identify and catch 3-4 hallucinated or misinterpreted claims.
  3. Reclassify AI recommendations into *Feasible / Verified* vs. *Hallucinated / Incorrect*.

### 🛡️ Gate 4: Continuous Testing Strategy & Deliverables Review (Human Checkpoint 4)
- **Actor:** Human Tester / Student.
- **Verification Items:**
  1. Review CI/CD pipeline design, p95 regression thresholds (>15%), and trade-off arguments.
  2. Review AI Audit Report entries, commit logs, and packaged ZIP archive.

---

## 4. Standard Performance Testing Workflow

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

## 5. Technical Rules & Constraints
- **JVM Heap Allocation**: Always maintain `-Xms1g -Xmx4g` when running load tests with > 100 threads to prevent client-side GC pauses.
- **CSV Sharing Mode**: Use `Sharing mode: All threads`, `Recycle on EOF: True`, `Stop thread on EOF: False`.
- **Bearer Token Handling**: Must extract JWT token using `JSONPostProcessor` (`$.token`) and inject via `HTTP Header Manager` (`Authorization: Bearer ${token}`).
- **Assertions**: Verify both HTTP status code (200) and response body payload text.

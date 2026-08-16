# HW05 Performance Testing - Team Task Division

## Purpose

This document divides HW05 work for a group of 4 members while respecting the assignment rule that no two members may test the same workflow. HW05 is an individual assignment, so each member must still produce their own test plans, logs, screenshots, video, AI audit report, critique, Git commits, README, and submission package.

## Assumptions

- SUT: EShop from <https://github.com/ttbhanh/eshop-sut>.
- Main tool: JMeter. k6 may be used by a member only if they can provide equivalent outputs.
- Each member tests one distinct end-to-end workflow.
- Every workflow must cover all three endpoint groups:
- Auth-heavy: login, registration, access control, lockout, password reset, or authenticated session handling.
- Read-heavy: product listing, search, category listing, product detail, dashboard, or history views.
- Transactional: cart mutation, checkout/order creation, coupon usage, admin CRUD, import, or order state changes.
- Common materials may be discussed, but prompts, reports, raw logs, screenshots, and final analysis must not be copied between members.

## Member Workflow Allocation

| Member | Suggested Workflow | Auth-heavy Coverage | Read-heavy Coverage | Transactional Coverage | Main Risk to Handle |
| --- | --- | --- | --- | --- | --- |
| Member 1 | Existing user login -> product search -> product detail -> add to cart -> checkout | Existing user login and session token/cookie handling | Product search and product detail | Add to cart and checkout/order creation | Realistic think-time and avoiding account lockout during Stress/Spike |
| Member 2 | New user registration/login -> category browsing -> product detail -> coupon checkout | Account registration and first login | Category product listing and product detail | Coupon validation and checkout | Data isolation: unique emails/users and reusable product/coupon data |
| Member 3 | Login with lockout-aware negative/positive path -> product listing pagination/filter -> cart quantity update -> checkout | Login plus documented 3-fail lockout reset process | Product listing pagination/filter | Cart update quantity and checkout | Correctly resetting locked accounts between Stress/Spike runs |
| Member 4 | Admin login -> dashboard/product list -> product/category CRUD or CSV import | Admin login and access control | Admin dashboard/product/category list | Product/category CRUD or CSV import | Avoiding destructive data changes; use test-only records and cleanup steps |

## Shared Team Work

These tasks can be coordinated once, then each member adapts the result to their own workflow.

| Task | Owner | Output |
| --- | --- | --- |
| Confirm SUT setup steps, ports, database seed command, and default accounts | Member 1 | Shared setup notes in team chat or shared README draft |
| Identify exact API endpoints for all 4 workflows | All members | Endpoint map per workflow |
| Agree on JMeter project folder structure and naming convention | Member 2 | Folder template and filename examples |
| Agree on screenshot naming convention and evidence checklist | Member 3 | Evidence checklist |
| Prepare common report skeleton sections | Member 4 | Markdown outline only; each member writes their own content |

## Individual Work Required From Every Member

Each member must complete the following for their assigned workflow.

### 1. Workflow and Endpoint Mapping

Deliverables:

- A short workflow description.
- Endpoint table with method, path, endpoint group, request data, expected response, and assertion.
- Justification that the workflow covers auth-heavy, read-heavy, and transactional endpoint groups.

Recommended commit:

```bash
git commit -m "docs: document selected performance workflow"
```

### 2. Data-Driven Inputs

Deliverables:

- CSV file for credentials.
- CSV file for product/category/search/order/coupon data as needed.
- Explanation of which JMeter CSV Data Set Config uses each CSV file.

Recommended commit:

```bash
git commit -m "test: add data-driven inputs"
```

### 3. Load Test Plan

Deliverables:

- JMeter test plan named `{StudentID}_Load_{YYYYMMDD}.jmx`.
- One distinct report/listener type used only for Load.
- Raw `.jtl` log.
- HTML report folder.
- Screenshot showing JMeter and backend resource monitor in the same run context.
- Human review note explaining what AI got wrong or missed in the generated Load plan.

Recommended commit:

```bash
git commit -m "test: add load performance plan"
```

### 4. Stress Test Plan

Deliverables:

- JMeter test plan named `{StudentID}_Stress_{YYYYMMDD}.jmx`.
- One distinct report/listener type used only for Stress.
- Raw `.jtl` log.
- HTML report folder.
- Screenshot showing JMeter and backend resource monitor.
- Documented account-lockout reset steps if the run triggers lockout.
- Human review note explaining what AI got wrong or missed in the generated Stress plan.

Recommended commit:

```bash
git commit -m "test: add stress performance plan"
```

### 5. Spike Test Plan

Deliverables:

- JMeter test plan named `{StudentID}_Spike_{YYYYMMDD}.jmx`.
- One distinct report/listener type used only for Spike.
- Raw `.jtl` log.
- HTML report folder.
- Screenshot showing JMeter and backend resource monitor.
- Documented account-lockout reset steps if the run triggers lockout.
- Human review note explaining what AI got wrong or missed in the generated Spike plan.

Recommended commit:

```bash
git commit -m "test: add spike performance plan"
```

### 6. Endurance / Soak Test

Deliverables:

- A 10-15 minute sustained-load run.
- Concrete endurance threshold numbers, such as maximum stable RPS, p95 latency, error rate, CPU usage, and memory ceiling.
- Screenshot or log evidence supporting the threshold.

Recommended commit:

```bash
git commit -m "docs: record endurance threshold"
```

### 7. AI Analysis and Misinterpretation Hunt

Deliverables:

- AI prompt asking the tool to analyse raw `.jtl` logs and suggest thresholds.
- AI output saved in the AI Audit Report.
- Human review identifying misread or misinterpreted metrics.
- Correct values cited from raw `.jtl` logs.
- Classification of AI optimization suggestions as feasible or hallucinated.

Recommended commit:

```bash
git commit -m "docs: add AI analysis review"
```

### 8. Continuous Performance Testing Proposal

Deliverables:

- A proposed continuous performance-testing model.
- Flow chart showing commit detection, test selection, execution, baseline comparison, and p95 regression flagging.
- Trade-off discussion covering cost, runtime, false alarms, environment noise, and maintenance.

Recommended commit:

```bash
git commit -m "docs: add continuous performance testing proposal"
```

### 9. Agent Skill

Deliverables:

- A reusable Agent Skill or rule that applies the performance-testing and log-analysis workflow.
- YouTube demo link showing the skill used end to end on a complete endpoint group.

Recommended commit:

```bash
git commit -m "skill: add reusable performance testing workflow"
```

### 10. Final Packaging

Deliverables:

- Main report in Markdown and PDF.
- AI Critique in Markdown and PDF.
- AI Audit Report in Markdown and PDF.
- Three `.jmx` test plans.
- Three raw `.jtl` logs.
- Three HTML report folders.
- Resource-monitor screenshots and hardware-spec screenshots.
- Unlisted YouTube demo video link.
- Git commit log text file.
- Bug reports with screenshots on GitHub Issues, if any.
- `README.md` with self-assessment table and test summary.
- Final zip named `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`.

Recommended commit:

```bash
git commit -m "docs: finalize HW05 submission package"
```

## Suggested Timeline

| Phase | Time Box | Team Activity | Individual Output |
| --- | --- | --- | --- |
| Phase 1 | 1 hour | Confirm SUT setup and endpoint map | Selected workflow and endpoint table |
| Phase 2 | 1 hour | Align naming, folders, and CSV style | Data-driven CSV files |
| Phase 3 | 3 hours | Run Load, Stress, and Spike plans | `.jmx`, `.jtl`, HTML reports, screenshots |
| Phase 4 | 1 hour | Compare common metric interpretation mistakes | Endurance threshold and AI analysis review |
| Phase 5 | 1 hour | Discuss CI/performance-regression model | Continuous testing proposal |
| Phase 6 | 2 hours | Peer-check evidence checklist only | Final report, audit, critique, video, README, zip |

## Evidence Checklist Per Member

| Evidence | Required |
| --- | --- |
| 3 distinct workflows across group? | Yes; all 4 should be distinct |
| Load test plan | Yes |
| Stress test plan | Yes |
| Spike test plan | Yes |
| CSV data-driven input | Yes |
| 3 distinct report/listener types | Yes |
| 3 raw `.jtl` logs | Yes |
| 3 HTML report folders | Yes |
| Resource monitor screenshots | Yes |
| Hardware report screenshot and spec table | Yes |
| Endurance threshold with numbers | Yes |
| AI analysis prompt and output | Yes |
| Human correction of AI misinterpretations | Yes |
| Continuous performance-testing flow chart | Yes |
| AI Critique, 200-300 words | Yes |
| AI Audit Report appendix | Yes |
| Git commit log text file | Yes |
| Unlisted YouTube demo, at least 6 minutes | Yes |
| README with self-assessment and summary | Yes |

## Peer Review Rules

- Members may review each other's checklist, screenshots, and report structure.
- Members must not copy prompts, AI outputs, report paragraphs, `.jtl` logs, or screenshots.
- Each member must cite values from their own raw `.jtl` files.
- Each member must record their own Vietnamese narration in the demo video.
- If two workflows become too similar, change one workflow before running the official tests.

## Recommended Folder Structure Per Member

```text
submissions/
  <StudentID>/
    README.md
    report/
      main-report.md
      main-report.pdf
      ai-critique.md
      ai-critique.pdf
      ai-audit-report.md
      ai-audit-report.pdf
    test-plans/
      <StudentID>_Load_<YYYYMMDD>.jmx
      <StudentID>_Stress_<YYYYMMDD>.jmx
      <StudentID>_Spike_<YYYYMMDD>.jmx
    data/
      credentials.csv
      products.csv
      orders.csv
    results/
      load/
        raw.jtl
        html-report/
      stress/
        raw.jtl
        html-report/
      spike/
        raw.jtl
        html-report/
    evidence/
      screenshots/
      hardware/
    git-commit-log.txt
```

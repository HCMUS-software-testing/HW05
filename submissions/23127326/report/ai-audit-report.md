# AI Audit Report

## Declaration

I use AI tools for the following tasks: endpoint mapping, workload/test-plan design, JMeter XML generation, correlation/assertion review, JTL analysis script design, threshold proposal, human-review checklist and continuous performance-testing proposal.

## Interaction log

| # | Tool | Date/time (Asia/Ho_Chi_Minh) | Prompt | Output / human review |
| ---: | --- | --- | --- | --- |
| 1 | Codex | 2026-08-29 | Read `plan/plan.md` and Vietnamese requirements; map deliverables and constraints. | Used to establish scope; checked against requirements manually. |
| 2 | Codex | 2026-08-29 | Review EShop API specification and backend implementation for the selected workflow. | Found lockout, pagination, cart update and checkout gaps; live evidence retained separately. |
| 3 | Codex | 2026-08-29–30 | Generate three JMeter plans with one shared data-driven workflow and scenario-specific load/report views. | Human review caught shared-CSV EOF unfairness; plans were changed to per-VU files. |
| 4 | Codex analyzer | 2026-08-30 | Analyze each raw JTL by label and classify failed samples. | Recomputed from 4 official JTLs: HTTP errors 0; failures are only expected post-checkout-cart assertions. JSON outputs are in `metrics-20260830/`. |
| 5 | Codex + human review | 2026-08-30 | Suggest optimizations and classify claims by evidence strength. | Accepted only contract/implementation-backed actions; CPU/RSS conclusions rejected because official monitor files were invalid. |

## Human review checklist

- [x] No raw JTL, screenshot, video, metric or issue was fabricated.
- [x] Every VU uses a distinct account and per-VU CSV EOF behavior is verified.
- [x] Lockout probe is excluded from official positive run and reset is documented.
- [x] Listener-derived views are not used as official non-GUI measurements.
- [x] Transport/HTTP errors are separated from expected business-gap assertions.
- [x] Every reported metric is reproducible from a raw JTL.
- [x] Optimization recommendations are classified using implementation/profiling evidence.
- [ ] GUI screenshots and student-recorded video remain pending.

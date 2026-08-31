# AI Audit Report

## Identity

- Student: Mai Thi Kim Duyen, 23127185
- Date: 2026-08-30
- AI-assisted agent: Codex GPT-5
- Human reviewer: Mai Thi Kim Duyen

## Audit log

| Step | Prompt/task | AI output/use | Human verification and correction |
|---|---|---|---|
| 1 | Inspect assignment and team division | Selected member-2 workflow: new registration, login, categories, product detail, coupon, checkout | Confirmed against `docs/team-task-division.vi.md`. |
| 2 | Inspect backend source and API specification | Produced endpoint map and identified auth/read/transaction groups | Compared every route with `server.js` and `api_specification.md`. |
| 3 | Design JMeter plans | Generated three plans with CSV, assertions, different listener names and workload values | XML was validated; corrected invalid ResultCollector XML and CSV header handling. |
| 4 | Run draft Load plan | JMeter produced 90 samples with assertion failures because protected calls had 401 | Kept raw JTL; traced cause to token extractor placement. Did not present this as a clean pass. |
| 5 | Implement reusable Agent Skill runner | Generated real API calls, unique test users, JTL output and metrics parser | Fixed a harness bug where GET requests sent a null body. Re-ran smoke and obtained 0 transport errors. |
| 6 | Run Load/Stress/Spike | JMeter produced 90/90/90 samples, 0 errors; runner runs also completed with 0 errors | Checked raw JTL labels and error fields. |
| 7 | Run Soak | 600,786 ms, 291,384 samples, 0 errors | Verified duration and counts from command output and raw JTL. |
| 8 | Interpret coupon/auth behavior | Identified implementation defects in source | Reproduced relevant response paths through workflow and documented them separately from performance metrics. |

## AI misinterpretation hunt

1. The initial JMeter artifact looked structurally complete but was not functionally correlated. AI-generated configuration must be checked in GUI/CLI with a protected request, not judged by XML existence.
2. A clean runner result does not prove production scalability because all calls use localhost, SQLite and one Node process.
3. Zero errors in the runner does not mean the SUT meets all functional requirements; it only means this positive path returned successfully.
4. The apparent low latency is expected for loopback and must not be used as an Internet-facing SLA.

## AI usage boundary

AI created scaffolding, commands, parsing and draft prose. It did not fabricate raw logs, screenshots, hardware values, video or GitHub issues. Human execution and review remain necessary for screenshots, resource monitoring, video narration, final defect confirmation and submission approval.

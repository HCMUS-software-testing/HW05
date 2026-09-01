# Repository Guidelines

## Project Structure & Module Organization

This repository contains the HW05 performance-testing assignment materials. `src/` is the working root for the actual deliverable:

- `req/` — English and Vietnamese assignment requirements, including the PDF brief.
- `docs/` — planning and coordination documents, currently including team workflow allocation.
- Root-level files — project overview and submission guidance such as `README.md`.
- `src/` — the submission folder itself, including all artifacts and the AI audit report directly under `src/ai-audit/`.

Keep requirements, planning notes, and agent tooling outside `src/`. Do not create a `submission/` wrapper inside `src/`. When the work is ready, copy `src/` to a staging folder, rename the copied folder as required for submission, inspect it, and zip the copy. Do not rename, delete, or zip the working `src/` folder itself.

Test artifacts should be organized under `src/` by workflow and test type as they are created. Keep JMeter plans, raw `.jtl` logs, HTML reports, CSV inputs, screenshots, and reports clearly named and separated; do not mix one member’s evidence with another’s.

## Build, Test, and Development Commands

There is no application build or automated test command in the current repository. Work is performed against the EShop system under test using Apache JMeter. Typical commands are run from JMeter’s installation directory, for example:

```text
jmeter -n -t <StudentID>_Load_<YYYYMMDD>.jmx -l results/load.jtl -e -o results/load-html
```

Use equivalent commands for `Stress` and `Spike`, and retain the raw log and generated HTML report for each run. Record setup details, ports, seeded accounts, and reset procedures in the relevant documentation.

## Coding Style & Naming Conventions

Use Markdown with descriptive headings, short paragraphs, and tables where they improve traceability. Use UTF-8 and preserve the bilingual source documents. Name performance plans under `src/` as `{StudentID}_{TestType}_{YYYYMMDD}.jmx`, such as `2212345_Stress_20260831.jmx`; use lowercase, descriptive names for supporting files and folders.

## Testing Guidelines

JMeter is the primary testing tool. Each individual workflow must cover auth-heavy, read-heavy, and transactional endpoint groups. Maintain separate Load, Stress, Spike, and endurance evidence, including assertions, resource-monitor screenshots, thresholds, and raw `.jtl` data. Use unique test data where registration, coupons, or destructive admin operations are involved.

## Commit & Pull Request Guidelines

Use imperative, scoped commit subjects consistent with the existing history and documented examples: `docs: ...`, `test: ...`, or `skill: ...` (for example, `test: add spike performance plan`). Pull requests should explain the workflow and test type, list produced artifacts, link any issue, and include relevant evidence or screenshots. Verify that personal deliverables are not copied between members.

## Security & Configuration Tips

Do not commit real credentials, secrets, or private environment details. Use test-only accounts, products, coupons, and admin records; document cleanup and account-lockout reset steps before running repeated tests.

## Token Optimization & Reference Guidelines

Always prioritize reading converted Markdown files (`.md`) inside reference directories (`ref/`) and requirement directories (`req/`) instead of raw PDF files to conserve context tokens and improve processing speed. Refer to `.agents/skills/ai-audit-entry/ref/13_Performance Testing.md` as the authoritative slide reference for performance testing concepts, metrics, and methodology.


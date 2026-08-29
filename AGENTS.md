# Repository Guidelines

## Project Structure & Module Organization

This repository currently contains documentation for the HW05 performance-testing assignment. `req/` holds the English and Vietnamese specifications, while `docs/` contains team workflow allocation and submission guidance. Keep the root `README.md` as the concise project entry point.

Place individual work under `submissions/<StudentID>/`. Use `test-plans/` for JMeter `.jmx` files, `data/` for CSV inputs, `results/` for raw `.jtl` files and HTML reports, `report/` for Markdown/PDF deliverables, and `evidence/` for screenshots and hardware records. Do not commit generated artifacts outside the appropriate student directory.

## Build, Test, and Development Commands

No build system or automated test runner is currently checked in. Use these commands when preparing changes:

```bash
git status --short
git diff --check
jmeter -n -t <plan>.jmx -l <results>.jtl -e -o <html-report>
```

The Git commands review pending files and detect whitespace errors. The JMeter command runs a plan non-interactively and generates raw results plus an HTML report; use real paths within your student directory.

## Coding Style & Naming Conventions

Write concise Markdown with descriptive headings, blank lines around lists, and fenced code blocks for commands. When manual `.jmx` editing is unavoidable, use two-space XML indentation and preserve JMeter-generated structure. CSV files must have stable, descriptive headers matching CSV Data Set Config variables.

Name plans `<StudentID>_<ScenarioType>_<YYYYMMDD>.jmx`, where the scenario is `Load`, `Stress`, or `Spike`. Keep report and evidence names similarly explicit.

## Testing Guidelines

Each workflow must cover auth-heavy, read-heavy, and transactional endpoints. Provide data-driven inputs, meaningful assertions, distinct report views for Load/Stress/Spike, raw `.jtl` logs, HTML reports, and resource-monitor evidence. Document account-lockout reset steps when relevant. Never fabricate execution evidence.

## Commit & Pull Request Guidelines

Use short imperative commits with documented prefixes, for example `docs: record endurance threshold`, `test: add load performance plan`, or `skill: add reusable workflow`. Keep commits focused. Pull requests should summarize the workflow, list validation performed, link relevant issues, and include screenshots for visual or performance evidence. Do not copy prompts, logs, screenshots, or report prose between members.

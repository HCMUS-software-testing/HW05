---
name: eshop-performance-testing
description: Use when designing or executing repeatable performance tests against the local EShop API, especially when JTL metrics, data-driven workflows, artifact audits, or AI usage records are required.
---

# EShop Performance Testing Skill

Use this skill for Mai Thi Kim Duyen's member-2 workflow:
`register -> login -> categories -> product list -> product detail -> add cart -> apply coupon -> checkout`.

## Rules

- Discover and verify endpoint contracts from the checked-out backend before generating plans.
- Use unique registration emails per iteration and CSV data for credentials/products/order fields.
- Preserve raw result files. Never invent samples, screenshots, hardware values, or conclusions.
- Treat HTTP status, response schema, token, product ID, coupon result, and order ID as assertions.
- Keep Load, Stress, Spike, and Soak profiles separate while preserving the same workflow.
- Record every AI-assisted decision in `report/ai-audit-report.md`, including human correction.
- Report implementation defects separately from performance observations.

## Reusable commands

Run from the repository root:

```bash
node submission/23127185_HW05/tools/run_workflow.js --scenario load
node submission/23127185_HW05/tools/run_workflow.js --scenario stress
node submission/23127185_HW05/tools/run_workflow.js --scenario spike
node submission/23127185_HW05/tools/run_workflow.js --scenario soak --duration 600
node submission/23127185_HW05/tools/analyze_results.js
```

The runner requires a live backend at `http://localhost:3000`. Its output is evidence from real API calls, not a substitute for manually captured JMeter/resource-monitor screenshots.

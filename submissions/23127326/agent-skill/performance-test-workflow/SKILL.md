---
name: performance-test-workflow
description: Build and review a data-driven JMeter performance workflow for Load, Stress, Spike and Endurance runs, with raw-JTL metric checks and explicit separation of transport errors from business assertions.
metadata:
  short-description: Reusable EShop performance workflow
---

# Performance test workflow

Use this skill when preparing or reviewing a JMeter API performance submission.

## Required workflow

1. Read the selected API contract and the SUT implementation. Record any contract/implementation gap as a test assertion or issue candidate; never change the SUT to make the run pass.
2. Use separate CSV rows per virtual user. Configure `Recycle on EOF=false`, `Stop thread on EOF=true`, and plan fixture creation outside measured time.
3. Correlate runtime values from responses: JWT token, product id/name/price and order id. Do not hard-code tokens or trust client-provided totals.
4. Keep one end-to-end flow across scenario plans: login, read/search, cart add, cart update probe, cart read, checkout and post-checkout cart check.
5. Keep lockout negative-path probes separate and disabled for official positive runs. Reset only the named test account between runs and record before/after state.
6. Use non-GUI JMeter for official runs. Keep one distinct listener/report view per scenario, but disable listeners while measuring.
7. Analyze raw JTL by label with `scripts/analyze_jtl.py`. Recalculate sample count, throughput, mean, median, p90, p95, p99, max and error categories before accepting any AI interpretation.
8. Report metrics only when traceable to raw JTL and resource evidence. Mark unverified optimization claims as hypotheses rather than causes.

## EShop-specific review points

- The current implementation may ignore `page` and `limit` on product search.
- A second `POST /api/cart` may create a second row instead of updating quantity.
- Checkout may accept `total_amount` from the client and may leave the cart populated.
- Login lockout behavior must be measured rather than inferred from the specification.

The API-specific notes are in [references/eshop-contract.md](references/eshop-contract.md). Use the analyzer in [scripts/analyze_jtl.py](scripts/analyze_jtl.py) for raw evidence only; it must not invent missing runs.


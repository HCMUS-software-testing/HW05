# Continuous Performance Testing proposal

```mermaid
flowchart TD
    A[Commit / Pull Request] --> B{Backend files changed?}
    B -- No --> C[Skip performance run; keep unit/integration checks]
    B -- Yes --> D[Start clean SUT and isolated test database]
    D --> E[Smoke: one VU, one iteration]
    E --> F{Smoke passes?}
    F -- No --> G[Fail check and upload logs]
    F -- Yes --> H{Run type}
    H -- PR --> I[Short Load]
    H -- Nightly --> J[Full Load + Stress + Spike]
    H -- Weekly --> K[Endurance 10-15 min]
    I --> L[Parse raw JTL and compare baseline]
    J --> L
    K --> L
    L --> M{p95 > baseline +20% and +100 ms, or error rate +1 pp?}
    M -- No --> N[Publish report and artifacts]
    M -- Yes --> O[Retry up to 3 times in same isolated environment]
    O --> P{Regression reproduced at least 2/3 runs?}
    P -- No --> Q[Flag flaky / investigate; do not block]
    P -- Yes --> R[Mark regression and block/require review]
```

## Operating model

- PR: smoke and short Load to give fast feedback.
- Nightly: full Load, Stress and Spike with fresh fixtures.
- Weekly: Endurance at 70% of the highest concurrency that remained stable.
- Store raw JTL, HTML report, JMeter version, SUT commit, fixture version and resource-monitor evidence together.
- Compare by stable label and scenario. Treat known business-gap assertions separately from transport/HTTP errors.

## Trade-offs

Self-hosted runner cost and runtime increase with Stress, Spike and Endurance. A local runner reduces cloud cost but adds CPU, memory, background-process and database-state noise. Fresh SQLite state improves repeatability but may differ from production data volume. A p95 threshold can create false positives when sample count is small, so the pipeline retries and requires reproduction in two of three runs. Retaining JTL and HTML artifacts improves auditability but consumes storage; retain full artifacts for failures and a shorter window for passing nightly runs. Baselines must be versioned with scenario parameters, otherwise a workload change can look like a product regression.


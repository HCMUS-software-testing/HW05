# Demo performance testing — 23127075

This standalone demo tests the workflow assigned in the root README: admin login → admin users → products/categories → product transaction cleanup. The SUT is `../eshop-sut`; `src/` was not read or used.

## Results

| Test | Samples | RPS | Avg | p95 | Errors |
|---|---:|---:|---:|---:|---:|
| Load | 300 | 4.40 | 9.6 ms | 17 ms | 16.67% |
| Stress | 2,000 | 37.22 | 4.5 ms | 7 ms | 25.00% |
| Spike | 1,200 | 1,046.21 | 56.4 ms | 89 ms | 25.00% |

Metrics were computed from the raw JTL files by `scripts/analyze_jtl.py`. Errors are retained as evidence: concurrent valid logins expose the SUT's login-attempt/lockout behavior. No endurance test or memory ceiling is claimed.

## Run

Start the backend from `eshop-sut/backend`, then run `./run_tests.sh` here. The plans use relative paths and seeded credentials in `data/credentials.csv`.

HTML reports: `results/{load,stress,spike}/html-report/`. Hardware capture: `evidence/hardware/fastfetch.txt`. GUI htop screenshots were not available in this headless execution environment.

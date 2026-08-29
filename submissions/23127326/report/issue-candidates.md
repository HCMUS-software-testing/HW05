# Issue candidates (not submitted)

These are local findings/candidates. No external GitHub Issue was created because no repository/account authorization was provided.

| Candidate | Expected | Actual to verify | Required evidence |
| --- | --- | --- | --- |
| Lockout counter/window | +1 per failed login; lock after 3; 30 s | **Reproduced**: statuses `401,401,403,403`; DB attempts `4`, locked window `180 s` | `evidence/issues/lockout-probe-20260830.jsonl`, `lockout-state-after-probe-20260830.txt` |
| Product pagination | `page`/`limit` change the returned slice | implementation currently only uses `search` | two requests with same search and different page/limit |
| Cart quantity update | same product remains one row with new quantity | second `POST /api/cart` may add another row | both request bodies and `GET /api/cart` response |
| Checkout cleanup/total | server recalculates total and empties cart | **Reproduced in official JTL**: `POST_CHECKOUT_CART` failed 359/359 Load, 1,789/1,789 Stress, 753/753 Spike, 2,700/2,700 Endurance; HTTP errors 0 | raw JTL + `report/metrics-20260830/*.json` |

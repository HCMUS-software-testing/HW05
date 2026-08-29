# Test data

`credentials.csv` contains 100 distinct synthetic rows provisioned on the local SUT outside the measured workflow. Passwords are test-only; do not replace them with personal credentials.

`products.csv` and `orders.csv` contain synthetic test input. The JMX uses `search`, `page`, `limit`, quantities and address from CSV, but extracts product `id`, `name` and `price` from the live product response before building cart/checkout requests. `product_id`, `product_name` and `price` are fixture references for review, not trusted correlation values.

`lockout-account.csv` is used only by the disabled negative-path thread group. Reset it between scenarios using the SQL documented in `report/main-report.md`.

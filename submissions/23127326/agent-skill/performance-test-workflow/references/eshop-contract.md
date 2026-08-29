# EShop contract notes

Source documents reviewed on 2026-08-29:

- API specification: <https://github.com/ttbhanh/eshop-sut/blob/main/api_specification.md>
- Backend implementation: <https://github.com/ttbhanh/eshop-sut/blob/main/backend/server.js>
- Seed data/setup: <https://github.com/ttbhanh/eshop-sut/blob/main/backend/database.js>

Selected calls:

| Method | Path | Runtime data |
| --- | --- | --- |
| POST | `/api/login` | `email`, `password`; extract `token` |
| GET | `/api/products` | `search`, `page`, `limit`; extract first `id`, `name`, `price` |
| POST | `/api/cart` | extracted product fields and CSV quantity |
| GET | `/api/cart` | verify one matching line and requested quantity |
| POST | `/api/checkout` | computed total and CSV shipping address; extract `orderId` |
| GET | `/api/cart` | expected empty after checkout |

Do not treat the specification as proof of actual behavior. Confirm contract gaps from the live SUT and raw responses.


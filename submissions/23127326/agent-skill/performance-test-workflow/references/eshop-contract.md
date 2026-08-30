# Ghi chú contract EShop

Tài liệu nguồn đã review ngày 2026-08-29:

- Đặc tả API: <https://github.com/ttbhanh/eshop-sut/blob/main/api_specification.md>
- Implementation backend: <https://github.com/ttbhanh/eshop-sut/blob/main/backend/server.js>
- Dữ liệu seed/setup: <https://github.com/ttbhanh/eshop-sut/blob/main/backend/database.js>

## Các request được chọn

| Method | Path | Dữ liệu runtime |
| --- | --- | --- |
| POST | `/api/login` | `email`, `password`; trích xuất `token` |
| GET | `/api/products` | `search`, `page`, `limit`; trích xuất `id`, `name`, `price` đầu tiên |
| POST | `/api/cart` | field sản phẩm đã trích xuất và quantity từ CSV |
| GET | `/api/cart` | kiểm tra một dòng matching và quantity yêu cầu |
| POST | `/api/checkout` | total đã tính và địa chỉ giao hàng từ CSV; trích xuất `orderId` |
| GET | `/api/cart` | kỳ vọng cart rỗng sau checkout |

Không xem đặc tả là bằng chứng cho hành vi thật. Phải xác nhận gap contract từ SUT đang chạy và raw response.

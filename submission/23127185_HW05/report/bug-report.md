# Báo cáo Lỗi, Khuyết tật & Bảo mật Ứng dụng (Full Bug & Vulnerability Report)

- **Sinh viên:** Mai Thị Kim Duyên
- **MSSV:** 23127185
- **Hệ thống kiểm thử:** Backend EShop SUT (`http://localhost:3000`)
- **Nguồn dữ liệu phân tích:** Quá trình thực thi JMeter 90 mẫu, Log thô JTL (`jmeter/results/`), HTML Report (`jmeter/reports/`) và Rà soát mã nguồn Backend (`eshop-sut/backend/server.js`).

---

## Phần 1: Phân tích Vấn đề Hiệu năng từ Kết quả JTL & HTML Report

Dựa trên phân tích 90 mẫu từ file JTL thô và file `statistics.json` của báo cáo HTML:

| Sampler / Transaction | Load Avg (ms) | Load P95 (ms) | Stress Avg (ms) | Spike Avg (ms) | Nhận xét điểm nghẽn (Bottleneck) | GitHub Issue |
|---|---:|---:|---:|---:|---|---|
| `Register` | **41.50** | **51.45** | 8.60 | 12.10 | **Nghẽn đĩa Ghi (Write-heavy):** Độ trễ cao nhất hệ thống. Do SQLite thực hiện ghi đĩa `INSERT INTO users` đồng bộ. | [#12](https://github.com/HCMUS-software-testing/HW05/issues/12) |
| `Checkout` | **34.70** | **54.70** | 2.90 | 3.40 | **Nghẽn đĩa Ghi (Write-heavy):** Độ trễ cao thứ 2. Do thao tác `INSERT INTO orders` đồng bộ. | [#12](https://github.com/HCMUS-software-testing/HW05/issues/12) |
| `Login` | 1.70 | 2.00 | 1.50 | 1.50 | Đáp ứng nhanh (xác thực JWT & query `SELECT`). | - |
| `Categories` | 0.90 | 1.90 | 0.80 | 0.80 | Rất nhanh (Read-heavy, query danh mục). | - |
| `ProductList` | 0.70 | 1.00 | 0.70 | 0.90 | Rất nhanh (Read-heavy, query tìm kiếm). | - |
| `ProductDetail` | 1.10 | 2.00 | 0.90 | 0.60 | Rất nhanh (Read-heavy, query chi tiết). | - |
| `AddToCart` | 0.90 | 1.00 | 0.90 | 1.00 | Rất nhanh (Lưu giỏ hàng trên RAM/In-memory). | - |
| `ApplyCoupon` | 1.30 | 2.00 | 0.90 | 1.20 | Nhanh, nhưng thiếu kiểm tra xác thực. | [#15](https://github.com/HCMUS-software-testing/HW05/issues/15) |
| `Orders` | 1.30 | 2.00 | 0.80 | 1.10 | Nhanh (Read-heavy, lấy lịch sử đơn). | - |

---

## Phần 2: Danh sách Toàn bộ 11 Bug, Khuyết tật Logic & Lỗ hổng Bảo mật trong SUT

Qua rà soát chuyên sâu source code `eshop-sut/backend/server.js`, tìm thấy tổng cộng **11 lỗi & lỗ hổng bảo mật**:

| STT | Loại Bug | Tên Bug / Lỗ hổng | Vị trí Source Code | Hành vi Kỳ vọng | Hành vi Thực tế trong Code | Mức độ | GitHub Issue Link |
|---|---|---|---|---|---|---|---|
| **1** | Performance | Nghẽn I/O đĩa synchronous SQLite | `database.js` & `server.js` | Ghi dữ liệu bất đồng bộ không làm nghẽn thread. | `INSERT` đồng bộ làm latency `Register` và `Checkout` cao gấp 40 lần Read. | High | [#12](https://github.com/HCMUS-software-testing/HW05/issues/12) |
| **2** | Security | Lỗ hổng SQL Injection | `server.js` (dòng 143–151) | Phải dùng parameterized query (`?`). | Nối chuỗi trực tiếp: `LIKE '%${searchQuery}%'`. Dễ bị tấn công SQLi. | Critical | [#16](https://github.com/HCMUS-software-testing/HW05/issues/16) |
| **3** | Security | Lỗ hổng Leo thang đặc quyền (Privilege Escalation) | `server.js` (dòng 118–128) | User thường không được tự sửa `role`. | `PUT /api/users/me` cho phép truyền `{ "role": "admin" }` để tự thăng cấp Admin. | Critical | [#17](https://github.com/HCMUS-software-testing/HW05/issues/17) |
| **4** | Security | Tin tưởng `total_amount` từ Client (Price Tampering) | `server.js` (dòng 297) | Backend phải tự tính lại tiền từ DB. | Nhận trực tiếp `total_amount` từ Client trong `req.body`. Hacker sửa giá 0 đ. | Critical | [#15](https://github.com/HCMUS-software-testing/HW05/issues/15) |
| **5** | Security | Thiếu Middleware xác thực API Coupon | `server.js` (dòng 363) | Phải đăng nhập (`authenticateToken`) mới được áp mã. | Route `POST /api/apply-coupon` công khai không có middleware xác thực token. | High | [#15](https://github.com/HCMUS-software-testing/HW05/issues/15) |
| **6** | Logic | Bộ đếm lần đăng nhập sai & thời gian khóa bị lặp | `server.js` (dòng 54–58) | Tăng 1 lần thử; khóa 30s sau 3 lần sai. | Code tăng `+2` (`login_attempts + 2`) và khóa 180s. Gõ sai 2 lần bị khóa 3 phút. | High | [#13](https://github.com/HCMUS-software-testing/HW05/issues/13) |
| **7** | Logic | Công thức tính giảm giá phần trăm bị sai | `server.js` (dòng 400 & 420) | Giảm `X%` = `total * (X / 100)`. | Code tính `total * (1 - discount_value)`. Giảm 10% tính thành giảm 90%. | High | [#14](https://github.com/HCMUS-software-testing/HW05/issues/14) |
| **8** | Logic | So sánh ngưỡng tối thiểu Coupon sai bất đẳng thức | `server.js` (dòng 379) | Đơn hàng đạt từ mức tối thiểu (`>= min`). | Dùng dấu `>` (`total_amount > min_order_amount`). Đơn bằng đúng giá min bị từ chối. | Medium | [#14](https://github.com/HCMUS-software-testing/HW05/issues/14) |
| **9** | Logic | Cho phép chuyển trạng thái đơn hàng Canceled -> Delivered | `server.js` (dòng 551) | Đơn bị hủy (`canceled`) không được chuyển sang `delivered`. | Code ghi: `if (currentStatus === "canceled" && status === "delivered") isValidTransition = true;`. | High | [#19](https://github.com/HCMUS-software-testing/HW05/issues/19) |
| **10** | Functional | Cho phép Hủy đơn hàng đang trong trạng thái Shipping | `server.js` (dòng 328–331) | Chỉ cho hủy đơn `pending` hoặc `confirmed`. | Khối `if` bỏ quên trạng thái `shipping`, cho phép user hủy đơn khi hàng đang giao. | Medium | [#19](https://github.com/HCMUS-software-testing/HW05/issues/19) |
| **11** | Functional | Bất đồng nhất kiểu dữ liệu Giá sản phẩm (Data Type Mismatch) | `server.js` (dòng 162–164) | Giá sản phẩm luôn là kiểu `Number`. | Code ép kiểu `if (row.id % 2 === 0) row.price = row.price.toString()`. ID chẵn trả String, lẻ trả Number. | Medium | [#18](https://github.com/HCMUS-software-testing/HW05/issues/18) |

---

## Phụ lục: Khuyên dùng Tối ưu & Remediation

1. **Khắc phục SQL Injection:** Dùng Parameterized Query: `db.all("SELECT * FROM products WHERE name LIKE ?", ['%' + searchQuery + '%'])`.
2. **Khắc phục Leo thang đặc quyền:** Loại bỏ trường `role` khỏi phần xử lý `PUT /api/users/me`.
3. **Tối ưu Hiệu năng SQLite:** Bật chế độ Write-Ahead Logging `PRAGMA journal_mode = WAL;`.
4. **Sửa Logic Đăng nhập & Mã giảm giá:** Đổi `attempts + 1`, thời gian khóa `30000ms`, sửa công thức coupon `total * (value / 100)` và điều kiện `>=`.
5. **Khắc phục Chuyển trạng thái Đơn hàng:** Sửa máy trạng thái trong `server.js` không cho phép chuyển từ `canceled` sang `delivered` hoặc `shipping`.

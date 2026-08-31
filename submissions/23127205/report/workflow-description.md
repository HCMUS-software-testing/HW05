# Mô tả Workflow & Ánh xạ API Endpoint Kiểm thử Hiệu năng (HW05)

**Sinh viên:** Lâm Hữu Khánh 
**MSSV:** 23127205 
**Vai trò nhóm:** Thành viên 1 (Member 1) 
**Tên Workflow:** Người dùng có sẵn đăng nhập -> Tìm kiếm sản phẩm -> Xem chi tiết sản phẩm -> Thêm vào giỏ hàng -> Đặt hàng (Checkout)

---

## 1. Mô tả Chi tiết Workflow End-to-End

Kịch bản mô phỏng hành vi của một khách hàng thực tế (Virtual User - VU) trên nền tảng thương mại điện tử EShop:
1. **Đăng nhập (Authentication)**: Người dùng mở ứng dụng và đăng nhập bằng tài khoản cá nhân có sẵn trong hệ thống (`email`, `password`). Hệ thống xác thực và cấp mã phiên JSON Web Token (JWT).
2. **Tìm kiếm sản phẩm (Search Discovery)**: Người dùng nhập từ khóa tìm kiếm (ví dụ: `iPhone`, `Samsung`, `MacBook`) để tìm các sản phẩm quan tâm.
3. **Xem chi tiết sản phẩm (Product Inspection)**: Người dùng bấm vào sản phẩm trong kết quả tìm kiếm để xem thông tin chi tiết (tên, giá tiền, mô tả).
4. **Thêm vào giỏ hàng (Cart Mutation)**: Người dùng chọn số lượng và thêm sản phẩm vào giỏ hàng cá nhân. Yêu cầu truyền JWT token ở Header.
5. **Thanh toán / Đặt hàng (Order Creation / Checkout)**: Người dùng tiến hành đặt hàng với địa chỉ giao hàng và tổng tiền. Hệ thống tạo bản ghi đơn hàng mới với trạng thái `pending`.

---

## 2. Bảng Ánh xạ API Endpoint (API Mapping Table)

| STT | Bước Workflow | Method & Path | Nhóm Endpoint | Request Headers | Request Payload (JSON / Query) | Expected HTTP Status & Response Body | Trích xuất & Assertions |
|:---:|---|---|:---:|---|---|---|---|
| **1** | Đăng nhập tài khoản | `POST /api/login` | **Auth-heavy** | `Content-Type: application/json` | `{"email": "${email}", "password": "${password}"}` | `200 OK`<br>`{"message": "Login successful", "token": "...", "user": {...}}` | • **JSON Extractor**: `$.token` -> biến `${token}`<br>• **Response Assertion**: Response Code = `200`, Body chứa `"token"`. |
| **2** | Tìm kiếm sản phẩm | `GET /api/products?search=${search_term}` | **Read-heavy** | `Content-Type: application/json` | Query parameter: `?search=${search_term}` | `200 OK`<br>`[{"id": 1, "name": "iPhone 15 Pro Max", "price": 30000000, ...}]` | • **Response Assertion**: Response Code = `200`, Content-Type chứa `application/json`. |
| **3** | Xem chi tiết sản phẩm | `GET /api/products/${product_id}` | **Read-heavy** | `Content-Type: application/json` | Path variable: `/${product_id}` | `200 OK`<br>`{"id": 1, "name": "...", "price": 30000000, "category_id": 1}` | • **Response Assertion**: Response Code = `200`, JSON chứa `"id": ${product_id}`. |
| **4** | Thêm vào giỏ hàng | `POST /api/cart` | **Transactional** | `Content-Type: application/json`<br>`Authorization: Bearer ${token}` | `{"id": ${product_id}, "name": "${product_name}", "price": ${price}, "quantity": 1}` | `200 OK`<br>`{"message": "Added to cart"}` | • **Response Assertion**: Response Code = `200`, Body chứa `"Added to cart"`. |
| **5** | Đặt hàng (Checkout) | `POST /api/checkout` | **Transactional** | `Content-Type: application/json`<br>`Authorization: Bearer ${token}` | `{"total_amount": ${total_amount}, "shipping_address": "${shipping_address}"}` | `200 OK`<br>`{"message": "Checkout successful", "orderId": 123}` | • **JSON Extractor**: `$.orderId` -> biến `${orderId}`<br>• **Response Assertion**: Response Code = `200`, Body chứa `"Checkout successful"` và `"orderId"`. |

---

## 3. Biện luận về Độ bao phủ các Nhóm Endpoint

Workflow đã chọn thỏa mãn 100% yêu cầu bao phủ của đề bài:

1. **Nhóm Auth-heavy (`POST /api/login`)**:
 - Kiểm tra khả năng xử lý xác thực, sinh chữ ký số JWT, và truy vấn bảng `users` trong SQLite.
 - Thử thách cơ chế khóa tài khoản (`locked_until`, `login_attempts` sau 3 lần sai liên tiếp).
 - Được tối ưu bằng giải pháp phân tán tải trên pool **50 tài khoản độc lập** (`loadtest_user01..50@eshop.com`).

2. **Nhóm Read-heavy (`GET /api/products?search=...` và `GET /api/products/:id`)**:
 - Thao tác đọc dữ liệu với tần suất cao.
 - Endpoint tìm kiếm thực hiện câu lệnh SQL `LIKE '%search%'` trên cơ sở dữ liệu chưa được đánh index, cho phép quan sát rõ sự suy giảm hiệu năng khi tải đọc tăng cao ở bài kiểm tra Stress/Spike.

3. **Nhóm Transactional (`POST /api/cart` và `POST /api/checkout`)**:
 - Yêu cầu xác thực Bearer token bắt buộc ở tầng Middleware Express.
 - Ghi dữ liệu vào bộ nhớ session giỏ hàng (`POST /api/cart`) và thực hiện thao tác INSERT giao dịch vào bảng `orders` trong SQLite (`POST /api/checkout`).
 - Cho phép phát hiện hiện tượng Database Lock Contention của SQLite (chế độ journal mặc định) khi có hàng trăm thread cùng ghi đồng thời.

---

## 4. Quản lý Dữ liệu Kiểm thử (Data-driven Configuration)

- **`credentials.csv`**: Chứa 50 tài khoản hợp lệ (`email,password`).
 - *Sharing mode*: `All threads`.
 - *Recycle on EOF*: `True`.
 - *Stop thread on EOF*: `False`.
- **`products.csv`**: Chứa danh mục 5 từ khóa tìm kiếm phổ biến và thông tin sản phẩm tương ứng (`search_term,product_id,product_name,price`).
- **`orders.csv`**: Chứa thông tin địa chỉ giao hàng và tổng tiền (`shipping_address,total_amount`).

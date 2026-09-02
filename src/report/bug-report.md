# Bug Report - Product CRUD thiếu kiểm soát truy cập

## Tóm tắt

- **Mức độ**: High
- **Phạm vi**: `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id`
- **Môi trường**: EShop backend tại `http://localhost:3000`, ngày 2026-09-03
- **GitHub Issue**: Chưa tạo được vì phiên đăng nhập `gh` của repository không hợp lệ; chưa có screenshot GitHub Issue.

Ba endpoint thay đổi sản phẩm không gắn middleware `authenticateToken`, trong khi các endpoint quản trị tương tự như category CRUD và import products đều yêu cầu token. Người dùng không xác thực có thể tạo, sửa hoặc xóa dữ liệu sản phẩm.

## Các bước tái hiện

```bash
curl -X POST http://localhost:3000/api/products \
  -H 'Content-Type: application/json' \
  --data '{"name":"HW05 unauthenticated probe","price":1,"description":"security reproduction","imageUrl":"","category_id":1}'
```

Kết quả thực tế ngày 2026-09-03, không gửi `Authorization` header:

```json
{"message":"Product created","id":8943}
```

Request trả HTTP 200 và tạo sản phẩm. Sau khi xác minh, dữ liệu probe đã được dọn bằng `DELETE /api/products/8943`, endpoint này cũng chấp nhận request không token và trả `{"message":"Product deleted"}`.

## Kết quả mong đợi

Các endpoint ghi dữ liệu sản phẩm phải dùng `authenticateToken` và kiểm tra role admin; request không có token phải bị từ chối bằng HTTP 401 hoặc 403.

## Đề xuất sửa

Gắn middleware xác thực và kiểm tra quyền admin vào cả ba route Product CRUD, sau đó thêm integration tests cho request không token, token user thường và token admin. Không sửa SUT trong repository bài làm này để giữ nguyên hệ thống mục tiêu đã được đo.

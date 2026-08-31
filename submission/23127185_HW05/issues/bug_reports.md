# Các phát hiện cần rà soát trước khi tạo GitHub Issue

Agent chưa tự động tạo GitHub Issue bên ngoài. Các phát hiện dưới đây đang chờ Mai xác nhận thủ công trước khi tạo issue.

| Phát hiện | Bằng chứng | Kỳ vọng | Thực tế |
|---|---|---|---|
| Bộ đếm lần đăng nhập | Nhánh login trong `eshop-sut/backend/server.js` | Tăng 1 lần và khóa 30 giây sau 3 lần sai | Tăng 2 lần và khóa 180 giây |
| Ngưỡng mã giảm giá | `server.js`, endpoint `/api/apply-coupon` | Chấp nhận tổng tiền đúng bằng mức tối thiểu | Sử dụng `total_amount > min_order_amount` |
| Tỷ lệ giảm giá | Nhánh xử lý phần trăm trong `server.js` | Tính theo `total * discount_value / 100` | Sử dụng `total * (1 - discount_value)` |
| Tính toàn vẹn tổng tiền checkout | `server.js`, endpoint `/api/checkout` | Backend tính lại tổng tiền từ giỏ hàng | Chấp nhận `total_amount` do client gửi |

Đây là các phát hiện về chức năng/bảo mật được tìm thấy khi rà soát source và thực thi positive path. Chỉ tạo GitHub Issue sau khi đã tái hiện thủ công và đính kèm ảnh chụp thật.

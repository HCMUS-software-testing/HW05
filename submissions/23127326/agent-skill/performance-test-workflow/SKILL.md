---
name: performance-test-workflow
description: Xây dựng và review workflow JMeter có dữ liệu, cho Load, Stress, Spike và Endurance, kèm kiểm tra metric từ JTL thô và tách rõ lỗi transport khỏi assertion nghiệp vụ.
metadata:
  short-description: Workflow kiểm thử hiệu năng EShop có thể tái sử dụng
---

# Workflow kiểm thử hiệu năng

Dùng skill này khi chuẩn bị hoặc review bài kiểm thử hiệu năng API bằng JMeter.

## Quy trình bắt buộc

1. Đọc contract API và implementation của SUT. Ghi mọi khoảng cách contract/implementation thành assertion hoặc candidate issue; không sửa SUT để làm run pass.
2. Dùng CSV riêng cho từng virtual user. Cấu hình `Recycle on EOF=false`, `Stop thread on EOF=true`, và tạo fixture ngoài thời gian đo.
3. Correlate giá trị runtime từ response: JWT token, product id/name/price và order id. Không hard-code token hoặc tin total do client gửi.
4. Giữ một E2E flow chung giữa các plan: login, search/read, cart add, cart update probe, cart read, checkout và kiểm tra cart sau checkout.
5. Tách lockout negative-path và tắt nó trong positive run chính thức. Chỉ reset đúng tài khoản test và ghi trạng thái trước/sau.
6. Dùng JMeter non-GUI cho lần chạy chính thức. Giữ một report view riêng cho từng kịch bản nhưng tắt listener khi đo.
7. Phân tích JTL thô theo label bằng `scripts/analyze_jtl.py`. Tính lại sample count, throughput, mean, median, p90, p95, p99, max và nhóm lỗi trước khi chấp nhận diễn giải của AI.
8. Chỉ báo cáo metric có thể truy nguyên về JTL thô và resource evidence. Claim tối ưu chưa được xác minh phải ghi là giả thuyết, không phải nguyên nhân.

## Điểm review riêng của EShop

- Implementation hiện tại có thể bỏ qua `page` và `limit` khi tìm sản phẩm.
- POST `/api/cart` lần hai có thể tạo dòng mới thay vì cập nhật quantity.
- Checkout có thể nhận `total_amount` từ client và không làm rỗng cart.
- Hành vi lockout phải được đo, không được suy ra chỉ từ đặc tả.

Ghi chú API nằm trong [references/eshop-contract.md](references/eshop-contract.md). Dùng analyzer tại [scripts/analyze_jtl.py](scripts/analyze_jtl.py) chỉ cho evidence JTL thô; không tự tạo run còn thiếu.

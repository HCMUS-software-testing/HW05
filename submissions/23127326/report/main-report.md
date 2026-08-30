# Báo cáo kiểm thử hiệu năng HW05

> MSSV: `23127326`; ngày chạy: `2026-08-30`. Số liệu lấy từ JTL thô chính thức và script analyzer đi kèm. Không dùng các lần chạy invalid trong `results/invalid-*`.

## 1. Thông tin thực thi

| Trường | Giá trị |
| --- | --- |
| MSSV | `23127326` |
| Hostname | `192.168.11.208` |
| Commit/phiên bản SUT | `85af3ba875c88283615e22cb108f13e2fccaf0e9` |
| Phiên bản JMeter | `5.6.3` |
| Hệ điều hành/phần cứng | MacBook Pro 18,3; Apple M1 Pro; 10 cores; 32 GB RAM; macOS 26.5.2 |
| Địa chỉ SUT | `http://localhost:3000` |
| Ngày chạy | `2026-08-30` |

Kho GitHub công khai: `https://github.com/HB4305/23127326-HW05-AI-Performance`

## 2. Workflow và endpoint map

1. `POST /api/login` với credentials riêng từng VU; lấy JWT từ response.
2. `GET /api/products` với `search`, `page`, `limit` từ CSV; kiểm tra 200, array không rỗng và tên khớp.
3. `POST /api/cart` với quantity ban đầu.
4. Gửi lại `POST /api/cart` với quantity cập nhật, rồi `GET /api/cart`.
5. Tính `orderTotal` từ giá đã extract và quantity cập nhật; `POST /api/checkout`.
6. `GET /api/cart` sau checkout để kiểm tra cart phải rỗng.

## 3. Review của người đối với các khoảng cách đã giữ lại

| Quy tắc đặc tả | Hành vi implementation cần xác minh | Cách đo/ghi nhận |
| --- | --- | --- |
| Sai login tăng đúng 1 và khóa sau lần 3 trong 30 s | server hiện cộng 2 và dùng 180 s | lockout probe riêng, ghi status/body và thời gian |
| `page`/`limit` phải phân trang | server hiện chỉ đọc `search` | so sánh response với nhiều page/limit |
| Thêm cùng sản phẩm tăng quantity trong một dòng | server hiện `push` dòng mới | cart response + số dòng matching |
| Checkout tự tính total và xóa cart | server nhận `total_amount` từ client và không xóa cart | so sánh request/response/cart sau checkout |

Các gap trên không được tính nhầm thành lỗi transport. Báo cáo riêng `HTTP/network`, `assertion/business-gap` và `thread stopped`.

## 4. Thiết lập kịch bản

| Kịch bản | Threads | Ramp-up | Thời lượng | JTL thô | Báo cáo HTML |
| --- | ---: | ---: | ---: | --- | --- |
| Load | 20 | 60 s | 300 s (tổng 360 s) | `results/load/23127326_Load_20260830.jtl` | `results/load/html-20260830/` |
| Stress | 100 | 300 s | 180 s (tổng 480 s) | `results/stress/23127326_Stress_20260830.jtl` | `results/stress/html-20260830/` |
| Spike | 10 nền + 90 spike | 5 s spike | nền 420 s, spike 120 s sau delay 120 s | `results/spike/23127326_Spike_20260830.jtl` | `results/spike/html-20260830/` |
| Endurance | 70 VU | 210 s | 600 s giữ tải (tổng 810 s) | `results/resource-rerun/endurance/23127326_Endurance_resource_20260830.jtl` | `results/resource-rerun/endurance/html-20260830/` |

## 5. Kết quả

Đã chạy analyzer bằng `agent-skill/.../analyze_jtl.py`; tính số mẫu, throughput, mean, median, p90, p95, p99, max và error rate theo từng label (`AUTH`, `READ`, `CART_ADD`, `CART_UPDATE`, `CART_GET`, `CHECKOUT`, `POST_CHECKOUT_CART`) sau khi đọc file metrics sinh ra.

| Kịch bản (resource-rerun) | Số mẫu | Lỗi transport/HTTP % | Assertion/gap nghiệp vụ % | p95 tổng / p95 label cao nhất | Throughput | CPU tối đa / RSS tối đa |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Load | 3,287 | 0.00% | 10.83% (356) | 6 / 7 ms | 9.1583/s | 16.4% / 75.8 MB |
| Stress | 16,433 | 0.00% | 10.83% (1,780) | 5 / 7 ms | 34.4137/s | 17.4% / 120.8 MB |
| Spike | 7,171 | 0.00% | 10.47% (751) | 5 / 7 ms | 17.1228/s | 25.5% / 90.5 MB |
| Endurance | 24,574 | 0.00% | 10.98% (2,699) | 6 / 8 ms | 30.4315/s | 19.6% / 85.6 MB |

Mean tổng thể: Load 2.642 ms; Stress 1.914 ms; Spike 2.041 ms; Endurance 2.443 ms. Mean/median/p90/p95/p99/max theo label được lưu trong `report/metrics-resource-rerun-20260830/*.json`; JTL thô và HTML của resource-rerun nằm trong `results/resource-rerun/`.

Diễn giải: mọi mẫu fail đều do assertion có chủ đích `POST_CHECKOUT_CART - expected empty`. Không có lỗi transport/HTTP. Đây là gap nghiệp vụ đã tái hiện của SUT, không phải lỗi hiệu năng. Response time đo được thấp hơn threshold p95 1.000 ms. Resource-rerun có CPU tối đa 16,4-25,5%; RSS tối đa 75,8-120,8 MB; tối đa 11 thread ở mọi run. RSS Endurance dao động 70,1-85,6 MB, vì vậy không kết luận leak vượt quá mẫu này.

Ngưỡng đánh giá: transport/HTTP < 1%, p95 < 1000 ms, CPU backend < 85%, memory không tăng liên tục và throughput không suy giảm trong ba cửa sổ liên tiếp. Điểm endurance duy trì được là 70 VU, 30.4315 RPS trong 600 giây giữ tải; đây là điểm đã quan sát, không khẳng định là giới hạn tối đa.

## 6. Lockout reset runbook

Không chạy lại toàn bộ `database.js` giữa các kịch bản vì việc đó xóa dữ liệu không liên quan. Với DB test local của SUT, chạy câu lệnh có điều kiện:

```sql
UPDATE users
SET login_attempts = 0, locked_until = NULL
WHERE email = '<lockout-test-email>';
```

Sau đó `SELECT email, login_attempts, locked_until FROM users WHERE email = '<lockout-test-email>';` để xác nhận. Ghi thời gian reset và ảnh/terminal evidence.

## 7. Issue và evidence

Đã tạo 4 GitHub Issue cho lockout, checkout cleanup, pagination và cart quantity; response và ảnh trang issue được lưu trong `evidence/issues/`. Tổng cộng 4 lỗi nghiệp vụ đã tái hiện.

## 8. Kiểm thử hiệu năng liên tục

`Commit -> phát hiện thay đổi backend -> khởi động SUT sạch -> smoke -> Load ngắn trên PR / Load+Stress+Spike đầy đủ hàng đêm / Endurance hàng tuần -> phân tích JTL -> so baseline -> chạy lại tối đa 3 lần -> đánh dấu regression p95/error -> lưu artifacts`

Đánh dấu regression khi p95 tăng trên 20% và ít nhất 100 ms, hoặc error rate tăng trên 1 điểm phần trăm; chỉ chặn sau khi tái hiện ít nhất 2/3 lần. Đánh đổi gồm thời gian runner self-hosted, nhiễu local, trạng thái SQLite, false positive, dung lượng artifacts và bảo trì baseline.

## 9. Video, AI audit và tự đánh giá

Video YouTube không công khai, tối thiểu 6 phút: `TODO_ADD_VIDEO_LINK` (sinh viên tự quay). Đã kèm AI audit/critique, JTL thô, báo cáo HTML, monitor tài nguyên và evidence ảnh. Chỉ link video còn chờ bổ sung thủ công.
